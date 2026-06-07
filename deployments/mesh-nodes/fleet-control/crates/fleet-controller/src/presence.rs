use fleet_proto::Heartbeat;
use std::collections::HashMap;

pub struct Presence {
    down_after: u64,
    last: HashMap<String, (u64, Heartbeat)>,
}
impl Presence {
    pub fn new(down_after_secs: u64) -> Self {
        Presence {
            down_after: down_after_secs,
            last: HashMap::new(),
        }
    }
    /// Record a heartbeat stamped with the CONTROLLER's receive time, not the
    /// agent's `hb.ts` — node NTP skew (seen up to ~25 min) would otherwise
    /// break down-detection. `hb.ts` stays informational on the stored payload.
    pub fn observe(&mut self, hb: Heartbeat, received_at: u64) {
        self.last.insert(hb.node.clone(), (received_at, hb));
    }
    pub fn is_up(&self, node: &str, now: u64) -> bool {
        self.last
            .get(node)
            .map(|(ts, _)| now.saturating_sub(*ts) <= self.down_after)
            .unwrap_or(false)
    }
    /// (node, up, last_seen_ts, latest heartbeat) for every node ever seen.
    /// Returns owned data so callers can drop the lock immediately.
    pub fn snapshot(&self, now: u64) -> Vec<(String, bool, u64, Heartbeat)> {
        self.last
            .iter()
            .map(|(n, (ts, hb))| {
                (n.clone(), now.saturating_sub(*ts) <= self.down_after, *ts, hb.clone())
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use fleet_proto::Heartbeat;
    fn hb(node: &str, ts: u64) -> Heartbeat {
        Heartbeat {
            node: node.into(),
            ts,
            uptime_s: 1,
            load1: 0.0,
            mem_free_mb: 1,
            overlay_free_mb: 1,
            mesh_peers: 1,
            mesh_signals: vec![],
            nats_connected: true,
            agent_version: "x".into(),
        }
    }
    #[test]
    fn tracks_and_marks_down() {
        let mut p = Presence::new(90);
        // hb.ts deliberately skewed (0) — presence must use received_at (1000).
        p.observe(hb("mesh-ap-07", 0), 1000);
        assert!(p.is_up("mesh-ap-07", 1050));
        assert!(!p.is_up("mesh-ap-07", 1100));
        assert!(!p.is_up("mesh-ap-99", 1000));
    }
    #[test]
    fn down_then_recovers() {
        let mut p = Presence::new(90);
        p.observe(hb("n", 0), 1000);
        assert!(!p.is_up("n", 1200));
        p.observe(hb("n", 0), 1200);
        assert!(p.is_up("n", 1210));
    }
}
