use anyhow::{anyhow, Result};
use fleet_proto::{subjects, Command, CommandReply, ProbeReply, ProbeRequest};
use std::time::Duration;

pub async fn ctl(
    client: &async_nats::Client,
    node: &str,
    cmd: &Command,
    timeout_s: u64,
) -> Result<CommandReply> {
    let payload = serde_json::to_vec(cmd)?;
    let resp = tokio::time::timeout(
        Duration::from_secs(timeout_s),
        client.request(subjects::ctl(node), payload.into()),
    )
    .await
    .map_err(|_| anyhow!("node {node} no reply (timeout)"))??;
    Ok(serde_json::from_slice(&resp.payload)?)
}

pub async fn probe(
    client: &async_nats::Client,
    node: &str,
    req: &ProbeRequest,
    timeout_s: u64,
) -> Result<ProbeReply> {
    let payload = serde_json::to_vec(req)?;
    let resp = tokio::time::timeout(
        Duration::from_secs(timeout_s),
        client.request(subjects::probe(node), payload.into()),
    )
    .await
    .map_err(|_| anyhow!("node {node} probe no reply"))??;
    Ok(serde_json::from_slice(&resp.payload)?)
}
