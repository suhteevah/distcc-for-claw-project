use crate::config::ControllerConfig;

/// Surface a fleet event. Logs always; if FLEET_NOTIFY_URL is set, POSTs
/// {source,text} to it (openclaw-core notify endpoint / webhook bridge).
pub async fn event(cfg: &ControllerConfig, msg: &str) {
    tracing::warn!(event = %msg, "fleet event");
    if let Some(url) = &cfg.notify_url {
        let body = serde_json::json!({"source":"fleet-controller","text":msg});
        if let Err(e) = reqwest::Client::new().post(url).json(&body).send().await {
            tracing::warn!(%e, "notify post failed");
        }
    }
}
