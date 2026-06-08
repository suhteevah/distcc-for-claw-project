use fleet_proto::Heartbeat;
use std::collections::HashMap;

struct Entry {
    received_at: u64,
    hb: Heartbeat,
    down_alerted: bool,
}

pub struct Presence {
    down_after: u64,
    nodes: HashMap<String, Entry>,
}
impl Presence {
    pub fn new(down_after_secs: u64) -> Self {
        Presence {
            down_after: down_after_secs,
            nodes: HashMap::new(),
        }
    }

    /// Record a heartbeat stamped with the CONTROLLER's receive time (node NTP skew —
    /// seen up to ~45h — would otherwise break down-detection). Returns `true` only when
    /// this heartbeat RECOVERS a node that was previously alerted DOWN (edge-triggered;
    /// first-ever sighting does NOT alert).
    pub fn observe(&mut self, hb: Heartbeat, received_at: u64) -> bool {
        let node = hb.node.clone();
        match self.nodes.get_mut(&node) {
            Some(e) => {
                let recovery = e.down_alerted;
                e.received_at = received_at;
                e.hb = hb;
                e.down_alerted = false;
                recovery
            }
            None => {
                self.nodes.insert(
                    node,
                    Entry {
                        received_at,
                        hb,
                        down_alerted: false,
                    },
                );
                false
            }
        }
    }

    #[allow(dead_code)] // used by tests + a useful query API; prod path uses snapshot/newly_down
    pub fn is_up(&self, node: &str, now: u64) -> bool {
        self.nodes
            .get(node)
            .map(|e| now.saturating_sub(e.received_at) <= self.down_after)
            .unwrap_or(false)
    }

    /// Nodes that JUST crossed into DOWN (down now + not yet alerted). Marks them alerted
    /// so each outage alerts exactly once.
    pub fn newly_down(&mut self, now: u64) -> Vec<String> {
        let mut out = Vec::new();
        for (node, e) in self.nodes.iter_mut() {
            let down = now.saturating_sub(e.received_at) > self.down_after;
            if down && !e.down_alerted {
                e.down_alerted = true;
                out.push(node.clone());
            }
        }
        out
    }

    /// (node, up, last_seen_ts, latest heartbeat) — owned, for status + metrics.
    pub fn snapshot(&self, now: u64) -> Vec<(String, bool, u64, Heartbeat)> {
        self.nodes
            .iter()
            .map(|(n, e)| {
                (
                    n.clone(),
                    now.saturating_sub(e.received_at) <= self.down_after,
                    e.received_at,
                    e.hb.clone(),
                )
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use fleet_proto::Heartbeat;
    fn hb(node: &str) -> Heartbeat {
        Heartbeat {
            node: node.into(),
            ts: 0, // deliberately skewed — presence must use received_at
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
        p.observe(hb("mesh-ap-07"), 1000);
        assert!(p.is_up("mesh-ap-07", 1050));
        assert!(!p.is_up("mesh-ap-07", 1100));
        assert!(!p.is_up("mesh-ap-99", 1000));
    }
    #[test]
    fn first_sighting_is_not_a_recovery() {
        let mut p = Presence::new(90);
        assert!(!p.observe(hb("n"), 1000)); // brand new -> no "back UP" alert
    }
    #[test]
    fn down_alerts_once_then_recovers() {
        let mut p = Presence::new(90);
        p.observe(hb("n"), 1000);
        // not down yet
        assert!(p.newly_down(1050).is_empty());
        // crosses down -> alerted once
        assert_eq!(p.newly_down(1200), vec!["n".to_string()]);
        // still down, already alerted -> no repeat
        assert!(p.newly_down(1300).is_empty());
        // heartbeat after a down-alert -> recovery
        assert!(p.observe(hb("n"), 1400));
        // can alert down again on a future outage
        assert_eq!(p.newly_down(1600), vec!["n".to_string()]);
    }
}
