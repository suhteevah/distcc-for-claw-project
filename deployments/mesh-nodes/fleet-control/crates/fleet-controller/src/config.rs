use anyhow::{anyhow, Result};

#[derive(Debug, Clone)]
pub struct ControllerConfig {
    pub nats_url: String,
    pub http_port: u16,
    pub metrics_port: u16,
    pub down_after_secs: u64,
    pub audit_path: String,
    pub notify_url: Option<String>,
    pub notify_cmd: Option<String>,
    pub probe_interval_secs: u64, // 0 = scheduled probes disabled
    pub probe_target: String,
}
impl ControllerConfig {
    pub fn from_env() -> Result<Self> {
        Self::from_env_with(|k| std::env::var(k).ok())
    }
    pub fn from_env_with(get: impl Fn(&str) -> Option<String>) -> Result<Self> {
        let num = |k: &str, d: u64| get(k).and_then(|v| v.parse().ok()).unwrap_or(d);
        Ok(ControllerConfig {
            nats_url: get("FLEET_NATS").ok_or_else(|| anyhow!("missing FLEET_NATS"))?,
            http_port: num("FLEET_HTTP_PORT", 9095) as u16,
            metrics_port: num("FLEET_METRICS_PORT", 9094) as u16,
            down_after_secs: num("FLEET_DOWN_AFTER_SECS", 90),
            audit_path: get("FLEET_AUDIT_PATH")
                .unwrap_or_else(|| "/var/log/fleet-controller-audit.jsonl".into()),
            notify_url: get("FLEET_NOTIFY_URL"),
            notify_cmd: get("FLEET_NOTIFY_CMD"),
            probe_interval_secs: num("FLEET_PROBE_INTERVAL_SECS", 60),
            probe_target: get("FLEET_PROBE_TARGET").unwrap_or_else(|| "192.168.168.168".into()),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn defaults() {
        let get = |k: &str| match k {
            "FLEET_NATS" => Some("nats://t@192.168.168.144:4222".into()),
            _ => None,
        };
        let c = ControllerConfig::from_env_with(get).unwrap();
        assert_eq!(c.http_port, 9095);
        assert_eq!(c.metrics_port, 9094);
        assert_eq!(c.down_after_secs, 90);
    }
    #[test]
    fn missing_nats_errors() {
        assert!(ControllerConfig::from_env_with(|_| None).is_err());
    }
}
