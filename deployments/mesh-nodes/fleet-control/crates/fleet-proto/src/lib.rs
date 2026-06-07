//! Shared wire contract between mesh-agent (nodes) and fleet-controller (cnc).
use serde::{Deserialize, Serialize};
pub mod verb;
pub use verb::Verb;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Heartbeat {
    pub node: String,
    pub ts: u64,
    pub uptime_s: u64,
    pub load1: f64,
    pub mem_free_mb: u64,
    pub overlay_free_mb: u64,
    pub mesh_peers: u32,
    pub mesh_signals: Vec<i32>,
    pub nats_connected: bool,
    pub agent_version: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ProbeKind {
    Ping,
    Dns,
    Http,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProbeRequest {
    pub kind: ProbeKind,
    pub target: String,
    #[serde(default)]
    pub timeout_ms: u64,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProbeReply {
    pub node: String,
    pub kind: ProbeKind,
    pub target: String,
    pub ok: bool,
    pub latency_ms: u64,
    pub detail: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Command {
    pub verb: String,
    #[serde(default)]
    pub args: serde_json::Value,
    #[serde(default)]
    pub confirm: bool,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CommandReply {
    pub ok: bool,
    #[serde(default)]
    pub exit: i32,
    #[serde(default)]
    pub stdout: String,
    #[serde(default)]
    pub stderr: String,
    #[serde(default)]
    pub duration_ms: u64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}
impl CommandReply {
    pub fn err(msg: impl Into<String>) -> Self {
        CommandReply {
            ok: false,
            exit: -1,
            stdout: String::new(),
            stderr: String::new(),
            duration_ms: 0,
            error: Some(msg.into()),
        }
    }
}

pub mod subjects {
    pub const PROBE_ALL: &str = "fleet.probe.all";
    pub const HEARTBEAT_WILDCARD: &str = "fleet.heartbeat.*";
    pub fn heartbeat(node: &str) -> String {
        format!("fleet.heartbeat.{node}")
    }
    pub fn ctl(node: &str) -> String {
        format!("fleet.ctl.{node}")
    }
    pub fn probe(node: &str) -> String {
        format!("fleet.probe.{node}")
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn heartbeat_roundtrips() {
        let h = Heartbeat {
            node: "mesh-ap-07".into(),
            ts: 1,
            uptime_s: 60,
            load1: 0.1,
            mem_free_mb: 320,
            overlay_free_mb: 3200,
            mesh_peers: 5,
            mesh_signals: vec![-42, -50],
            nats_connected: true,
            agent_version: "0.1.0".into(),
        };
        let j = serde_json::to_string(&h).unwrap();
        assert_eq!(serde_json::from_str::<Heartbeat>(&j).unwrap(), h);
    }
    #[test]
    fn subjects_format() {
        assert_eq!(subjects::heartbeat("mesh-ap-07"), "fleet.heartbeat.mesh-ap-07");
        assert_eq!(subjects::ctl("mesh-ap-07"), "fleet.ctl.mesh-ap-07");
        assert_eq!(subjects::probe("mesh-ap-07"), "fleet.probe.mesh-ap-07");
        assert_eq!(subjects::PROBE_ALL, "fleet.probe.all");
    }
}
