use crate::{config::ControllerConfig, audit, dispatch, metrics::Metrics, nats, notify, presence::Presence};
use anyhow::Result;
use axum::{
    extract::{Path, State},
    routing::{get, post},
    Json, Router,
};
use fleet_proto::{Command, Heartbeat, ProbeRequest};
use futures::StreamExt;
use std::{
    sync::Arc,
    time::{SystemTime, UNIX_EPOCH},
};
use tokio::sync::Mutex;

fn now() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
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
                    let was_up = app.presence.lock().await.is_up(&hb.node, now());
                    app.metrics.set_node(&hb.node, true, hb.overlay_free_mb);
                    if !was_up {
                        notify::event(&app.cfg, &format!("node {} back UP", hb.node)).await;
                    }
                    app.presence.lock().await.observe(hb, now());
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
                let snap = app.presence.lock().await.snapshot(now());
                for (node, up, _ts, hb) in snap {
                    app.metrics.set_node(&node, up, hb.overlay_free_mb);
                    if !up {
                        notify::event(&app.cfg, &format!("node {node} DOWN (no heartbeat)")).await;
                    }
                }
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
