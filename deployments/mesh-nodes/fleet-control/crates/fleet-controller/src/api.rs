use crate::{config::ControllerConfig, audit, dispatch, metrics::Metrics, nats, notify, presence::Presence};
use anyhow::Result;
use axum::{
    extract::{Path, State},
    routing::{get, post},
    Json, Router,
};
use fleet_proto::{Command, Heartbeat, ProbeKind, ProbeRequest};
use futures::StreamExt;
use std::{
    sync::Arc,
    time::{SystemTime, UNIX_EPOCH},
};
use tokio::sync::Mutex;

fn now() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
}

/// Grace beyond `down_after` before a silence is alerted. Lets a staggered wave of
/// simultaneous silences fully land so the mass-blip guard sees the whole wave (one blip)
/// instead of leaking per-node DOWN alerts for the early-crossing nodes.
const ALERT_GRACE_SECS: u64 = 45;

/// Publish a durable event to `fleet.event.*` (captured by the FLEET JetStream stream).
/// Plain core publish (no reply subject) so it never shadows request/reply.
async fn publish_event(nats: &async_nats::Client, subject: String, v: serde_json::Value) {
    if let Ok(p) = serde_json::to_vec(&v) {
        let _ = nats.publish(subject, p.into()).await;
    }
}

#[derive(Clone)]
struct App {
    nats: async_nats::Client,
    presence: Arc<Mutex<Presence>>,
    metrics: Arc<Metrics>,
    cfg: ControllerConfig,
}

pub async fn run(cfg: ControllerConfig) -> Result<()> {
    let nats = nats::connect(&cfg.nats_url).await?;
    tracing::info!("connected to NATS cluster");
    let app = App {
        nats: nats.clone(),
        presence: Arc::new(Mutex::new(Presence::new(cfg.down_after_secs))),
        metrics: Arc::new(Metrics::new()),
        cfg: cfg.clone(),
    };

    // heartbeat ingest
    {
        let app = app.clone();
        let mut sub = nats
            .subscribe(fleet_proto::subjects::HEARTBEAT_WILDCARD.to_string())
            .await?;
        tokio::spawn(async move {
            while let Some(msg) = sub.next().await {
                if let Ok(hb) = serde_json::from_slice::<Heartbeat>(&msg.payload) {
                    let node = hb.node.clone();
                    let overlay = hb.overlay_free_mb;
                    let peers = hb.mesh_peers;
                    let signals = hb.mesh_signals.clone();
                    let recovery = app.presence.lock().await.observe(hb, now());
                    app.metrics.set_node(&node, true, overlay);
                    app.metrics.set_mesh(&node, peers, &signals);
                    // Only announce recovery for nodes that had a per-node DOWN alert.
                    // Suppressed (visibility-blip) recoveries are silent; None = nothing.
                    if matches!(recovery, crate::presence::Recovery::Node) {
                        notify::event(&app.cfg, &format!("node {node} back UP")).await;
                        publish_event(&app.nats, format!("fleet.event.status.{node}"),
                            serde_json::json!({"node":node,"status":"up","ts":now()})).await;
                    }
                }
            }
        });
    }

    // down-sweep
    {
        let app = app.clone();
        tokio::spawn(async move {
            let mut tick = tokio::time::interval(std::time::Duration::from_secs(30));
            loop {
                tick.tick().await;
                let t = now();
                // refresh all gauges
                let snap = app.presence.lock().await.snapshot(t);
                for (node, up, _ts, hb) in &snap {
                    app.metrics.set_node(node, *up, hb.overlay_free_mb);
                    app.metrics.set_mesh(node, hb.mesh_peers, &hb.mesh_signals);
                }
                // down-detection with an all-nodes-down guard: a mass simultaneous silence
                // is a controller/mesh visibility blip, not N independent node outages.
                let (pending, down_now, known) = {
                    let p = app.presence.lock().await;
                    (p.pending_down(t, ALERT_GRACE_SECS), p.down_count(t), p.known_count())
                };
                if !pending.is_empty() {
                    let mass = known >= 4 && down_now >= (known + 1) / 2;
                    app.presence.lock().await.set_alert(&pending, mass);
                    if mass {
                        let msg = format!(
                            "fleet visibility blip: {}/{} nodes went silent at once — likely a NATS/mesh transient, NOT a node outage (nodes auto-recover; see /fleet/status)",
                            down_now,
                            known
                        );
                        notify::event(&app.cfg, &msg).await;
                        publish_event(
                            &app.nats,
                            "fleet.event.visibility".to_string(),
                            serde_json::json!({"status":"blip","silent":down_now,"known":known,"ts":t}),
                        )
                        .await;
                    } else {
                        for node in &pending {
                            notify::event(&app.cfg, &format!("node {node} DOWN (no heartbeat)")).await;
                            publish_event(
                                &app.nats,
                                format!("fleet.event.status.{node}"),
                                serde_json::json!({"node":node,"status":"down","ts":t}),
                            )
                            .await;
                        }
                    }
                }
            }
        });
    }

    // scheduled probes — gateway reachability from each up node (latency -> prometheus,
    // failures -> fleet.event for durable history)
    if cfg.probe_interval_secs > 0 {
        let app = app.clone();
        let interval = cfg.probe_interval_secs;
        let target = cfg.probe_target.clone();
        tokio::spawn(async move {
            let mut tick = tokio::time::interval(std::time::Duration::from_secs(interval));
            loop {
                tick.tick().await;
                let nodes: Vec<String> = app
                    .presence
                    .lock()
                    .await
                    .snapshot(now())
                    .into_iter()
                    .filter(|(_, up, _, _)| *up)
                    .map(|(n, _, _, _)| n)
                    .collect();
                for node in nodes {
                    let req = ProbeRequest {
                        kind: ProbeKind::Ping,
                        target: target.clone(),
                        timeout_ms: 2000,
                    };
                    match dispatch::probe(&app.nats, &node, &req, 5).await {
                        Ok(pr) => {
                            app.metrics.set_probe(&node, &target, pr.ok, pr.latency_ms);
                            if !pr.ok {
                                publish_event(&app.nats, format!("fleet.event.probe_fail.{node}"),
                                    serde_json::json!({"node":node,"target":target,"ts":now(),"detail":pr.detail})).await;
                            }
                        }
                        Err(e) => {
                            app.metrics.set_probe(&node, &target, false, 0);
                            tracing::warn!(%node, %e, "scheduled probe failed");
                            publish_event(&app.nats, format!("fleet.event.probe_fail.{node}"),
                                serde_json::json!({"node":node,"target":target,"ts":now(),"detail":e.to_string()})).await;
                        }
                    }
                }
            }
        });
    }

    // daily config backup (fires once shortly after start, then every interval)
    if cfg.backup_interval_secs > 0 {
        let app = app.clone();
        let interval = cfg.backup_interval_secs;
        tokio::spawn(async move {
            let mut tick = tokio::time::interval(std::time::Duration::from_secs(interval));
            loop {
                tick.tick().await;
                let nodes: Vec<String> = app
                    .presence
                    .lock()
                    .await
                    .snapshot(now())
                    .into_iter()
                    .filter(|(_, up, _, _)| *up)
                    .map(|(n, _, _, _)| n)
                    .collect();
                crate::backup::run_backup(&app.nats, &app.cfg, &nodes, now()).await;
            }
        });
    }

    // metrics server
    {
        let metrics = app.metrics.clone();
        let port = cfg.metrics_port;
        tokio::spawn(async move {
            let r = Router::new().route(
                "/metrics",
                get(move || {
                    let m = metrics.clone();
                    async move { m.render() }
                }),
            );
            match tokio::net::TcpListener::bind(("0.0.0.0", port)).await {
                Ok(l) => {
                    let _ = axum::serve(l, r).await;
                }
                Err(e) => tracing::error!(%e, "metrics bind failed"),
            }
        });
    }

    // control API
    let api = Router::new()
        .route("/fleet/status", get(status))
        .route("/fleet/ctl/:node", post(ctl_node))
        .route("/fleet/probe/:node", post(probe_node))
        .route("/fleet/backup", post(backup_now))
        .with_state(app.clone());
    let l = tokio::net::TcpListener::bind(("0.0.0.0", cfg.http_port)).await?;
    tracing::info!(port = cfg.http_port, "control API listening");
    axum::serve(l, api).await?;
    Ok(())
}

async fn status(State(a): State<App>) -> Json<serde_json::Value> {
    let snap = a.presence.lock().await.snapshot(now());
    Json(serde_json::json!({
        "nodes": snap.iter().map(|(n, up, ts, _)| serde_json::json!({"node":n,"up":up,"last_seen":ts})).collect::<Vec<_>>()
    }))
}

async fn backup_now(State(a): State<App>) -> Json<serde_json::Value> {
    let nodes: Vec<String> = a
        .presence
        .lock()
        .await
        .snapshot(now())
        .into_iter()
        .filter(|(_, up, _, _)| *up)
        .map(|(n, _, _, _)| n)
        .collect();
    let (n, committed) = crate::backup::run_backup(&a.nats, &a.cfg, &nodes, now()).await;
    Json(serde_json::json!({"nodes_backed_up": n, "committed": committed}))
}

async fn ctl_node(
    State(a): State<App>,
    Path(node): Path<String>,
    Json(cmd): Json<Command>,
) -> Json<serde_json::Value> {
    audit::append(
        &a.cfg.audit_path,
        &serde_json::json!({"ts":now(),"node":node,"verb":cmd.verb,"confirm":cmd.confirm}).to_string(),
    );
    match dispatch::ctl(&a.nats, &node, &cmd, 35).await {
        Ok(r) => Json(serde_json::to_value(r).unwrap()),
        Err(e) => Json(serde_json::json!({"ok":false,"error":e.to_string()})),
    }
}

async fn probe_node(
    State(a): State<App>,
    Path(node): Path<String>,
    Json(req): Json<ProbeRequest>,
) -> Json<serde_json::Value> {
    match dispatch::probe(&a.nats, &node, &req, 10).await {
        Ok(r) => Json(serde_json::to_value(r).unwrap()),
        Err(e) => Json(serde_json::json!({"ok":false,"error":e.to_string()})),
    }
}
