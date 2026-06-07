use anyhow::{anyhow, Result};

#[derive(Debug, Clone)]
pub struct AgentConfig {
    pub node: String,
    pub nats_url: String, // comma-separated allowed (failover)
    pub heartbeat_secs: u64,
    pub cmd_timeout_secs: u64,
    pub max_output_bytes: usize,
    pub allow_raw: bool,
    pub allow_reboot: bool,
    pub audit_path: String,
}
impl AgentConfig {
    pub fn from_env() -> Result<Self> {
        Self::from_env_with(|k| std::env::var(k).ok())
    }
    pub fn from_env_with(get: impl Fn(&str) -> Option<String>) -> Result<Self> {
        let req = |k: &str| get(k).ok_or_else(|| anyhow!("missing env {k}"));
        let flag = |k: &str| get(k).as_deref() == Some("1");
        let num = |k: &str, d: u64| get(k).and_then(|v| v.parse().ok()).unwrap_or(d);
        Ok(AgentConfig {
            node: req("MESH_AGENT_NODE")?,
            nats_url: req("MESH_AGENT_NATS")?,
            heartbeat_secs: num("MESH_AGENT_HEARTBEAT_SECS", 30),
            cmd_timeout_secs: num("MESH_AGENT_CMD_TIMEOUT_SECS", 30),
            max_output_bytes: num("MESH_AGENT_MAX_OUTPUT_BYTES", 262144) as usize,
            allow_raw: flag("MESH_AGENT_ALLOW_RAW"),
            allow_reboot: flag("MESH_AGENT_ALLOW_REBOOT"),
            audit_path: get("MESH_AGENT_AUDIT_PATH")
                .unwrap_or_else(|| "/var/log/mesh-agent-audit.jsonl".into()),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn from_map_defaults_and_gates() {
        let get = |k: &str| match k {
            "MESH_AGENT_NODE" => Some("mesh-ap-07".to_string()),
            "MESH_AGENT_NATS" => Some("nats://tok@localhost:4222".to_string()),
            "MESH_AGENT_ALLOW_RAW" => Some("1".to_string()),
            _ => None,
        };
        let c = AgentConfig::from_env_with(get).unwrap();
        assert_eq!(c.node, "mesh-ap-07");
        assert_eq!(c.heartbeat_secs, 30);
        assert!(c.allow_raw);
        assert!(!c.allow_reboot);
        assert_eq!(c.cmd_timeout_secs, 30);
    }
    #[test]
    fn missing_required_errors() {
        assert!(AgentConfig::from_env_with(|_| None).is_err());
    }
}
