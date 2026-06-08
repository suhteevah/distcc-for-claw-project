use crate::config::ControllerConfig;

/// Surface a fleet event. Always logs. If FLEET_NOTIFY_CMD is set, runs it with the
/// message as a single argv arg (no shell — injection-safe). If FLEET_NOTIFY_URL is set,
/// POSTs {source,text} JSON. Both are best-effort; failures are logged, never fatal.
pub async fn event(cfg: &ControllerConfig, msg: &str) {
    tracing::warn!(event = %msg, "fleet event");

    if let Some(cmd) = &cfg.notify_cmd {
        // msg passed as a positional arg, NOT interpolated into a shell string.
        match tokio::process::Command::new(cmd).arg(msg).output().await {
            Ok(o) if !o.status.success() => {
                tracing::warn!(code = ?o.status.code(), "notify cmd nonzero");
            }
            Err(e) => tracing::warn!(%e, "notify cmd spawn failed"),
            _ => {}
        }
    }

    if let Some(url) = &cfg.notify_url {
        let body = serde_json::json!({"source":"fleet-controller","text":msg});
        if let Err(e) = reqwest::Client::new().post(url).json(&body).send().await {
            tracing::warn!(%e, "notify post failed");
        }
    }
}
