use crate::{
    audit,
    command::{self, Gates},
    config::AgentConfig,
    exec, heartbeat, probe,
};
use anyhow::Result;
use fleet_proto::{subjects, Command, CommandReply, ProbeRequest};
use futures::StreamExt;
use std::time::{SystemTime, UNIX_EPOCH};

fn now() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
}

/// Split `nats://TOKEN@host:port` into (Some(TOKEN), "nats://host:port").
/// Userinfo containing ':' is user:pass (left as-is). Pure + tested.
fn split_token(raw: &str) -> (Option<String>, String) {
    if let Some(scheme_end) = raw.find("://") {
        let (scheme, rest) = raw.split_at(scheme_end + 3);
        if let Some(at) = rest.find('@') {
            let tok = &rest[..at];
            let host = &rest[at + 1..];
            if !tok.is_empty() && !tok.contains(':') {
                return (Some(tok.to_string()), format!("{scheme}{host}"));
            }
        }
    }
    (None, raw.to_string())
}

fn build_conn(url_csv: &str) -> (Vec<async_nats::ServerAddr>, async_nats::ConnectOptions) {
    let mut token: Option<String> = None;
    let mut addrs = Vec::new();
    for raw in url_csv.split(',').map(|s| s.trim()).filter(|s| !s.is_empty()) {
        let (tok, addr) = split_token(raw);
        if token.is_none() {
            token = tok;
        }
        if let Ok(a) = addr.parse::<async_nats::ServerAddr>() {
            addrs.push(a);
        }
    }
    let mut opts = async_nats::ConnectOptions::new().retry_on_initial_connect();
    if let Some(t) = token {
        opts = opts.token(t);
    }
    (addrs, opts)
}

pub async fn serve(c: AgentConfig) -> Result<()> {
    let (servers, opts) = build_conn(&c.nats_url);
    let client = async_nats::connect_with_options(servers, opts).await?;
    tracing::info!(node = %c.node, "connected to NATS");

    let mut ctl = client.subscribe(subjects::ctl(&c.node)).await?;
    let mut pr_node = client.subscribe(subjects::probe(&c.node)).await?;
    let mut pr_all = client.subscribe(subjects::PROBE_ALL.to_string()).await?;

    // heartbeat task
    {
        let client = client.clone();
        let c = c.clone();
        tokio::spawn(async move {
            let mut tick =
                tokio::time::interval(std::time::Duration::from_secs(c.heartbeat_secs));
            loop {
                tick.tick().await;
                let hb = heartbeat::collect(&c.node, now(), true).await;
                if let Ok(p) = serde_json::to_vec(&hb) {
                    let _ = client.publish(subjects::heartbeat(&c.node), p.into()).await;
                    tracing::debug!(peers = hb.mesh_peers, "heartbeat sent");
                }
            }
        });
    }

    let gates = Gates {
        allow_raw: c.allow_raw,
        allow_reboot: c.allow_reboot,
    };
    loop {
        tokio::select! {
            Some(msg) = ctl.next() => {
                let reply = match msg.reply.clone() { Some(r) => r, None => continue };
                let cmd: Command = match serde_json::from_slice(&msg.payload) {
                    Ok(v) => v,
                    Err(e) => {
                        let body = serde_json::to_vec(&CommandReply::err(format!("bad command json: {e}"))).unwrap();
                        let _ = client.publish(reply, body.into()).await;
                        continue;
                    }
                };
                tracing::info!(verb = %cmd.verb, confirm = cmd.confirm, "ctl received");
                let p = command::plan(&cmd, &gates);
                let (cr, do_reboot) = exec::execute(p, c.cmd_timeout_secs, c.max_output_bytes).await;
                audit::append(&c.audit_path, &audit::audit_line(now(), &cmd.verb, &cmd.args, cmd.confirm, cr.exit, cr.stdout.len()));
                let _ = client.publish(reply, serde_json::to_vec(&cr).unwrap().into()).await;
                if do_reboot {
                    let _ = client.flush().await;
                    tokio::time::sleep(std::time::Duration::from_millis(500)).await;
                    let _ = tokio::process::Command::new("reboot").spawn();
                }
            }
            Some(msg) = pr_node.next() => { handle_probe(&client, &c.node, msg).await; }
            Some(msg) = pr_all.next()  => { handle_probe(&client, &c.node, msg).await; }
            else => break,
        }
    }
    Ok(())
}

async fn handle_probe(client: &async_nats::Client, node: &str, msg: async_nats::Message) {
    let reply = match msg.reply {
        Some(r) => r,
        None => return,
    };
    let req: ProbeRequest = match serde_json::from_slice(&msg.payload) {
        Ok(v) => v,
        Err(_) => return,
    };
    let pr = probe::run_probe(node, req).await;
    let _ = client.publish(reply, serde_json::to_vec(&pr).unwrap().into()).await;
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn extracts_token() {
        let (t, a) = split_token("nats://abc123@192.168.168.144:4222");
        assert_eq!(t.as_deref(), Some("abc123"));
        assert_eq!(a, "nats://192.168.168.144:4222");
    }
    #[test]
    fn no_token_passthrough() {
        let (t, a) = split_token("nats://localhost:4222");
        assert_eq!(t, None);
        assert_eq!(a, "nats://localhost:4222");
    }
    #[test]
    fn userpass_left_alone() {
        let (t, a) = split_token("nats://u:p@host:4222");
        assert_eq!(t, None);
        assert_eq!(a, "nats://u:p@host:4222");
    }
}
