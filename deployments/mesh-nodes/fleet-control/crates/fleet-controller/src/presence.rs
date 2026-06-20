use fleet_proto::Heartbeat;
use std::collections::HashMap;

#[derive(Clone, Copy, PartialEq)]
enum Alert {
    None,
    DownPerNode,    // we fired a per-node DOWN alert for this node
    DownSuppressed, // marked down as part of a fleet-visibility blip (no per-node alert)
}

struct Entry {
    received_at: u64,
    hb: Heartbeat,
    alert: Alert,
}

/// What a heartbeat means for alerting when it lands.
#[derive(Debug, PartialEq)]
pub enum Recovery {
    None,       // node was up (or first sighting) — nothing to announce
    Node,       // node had a per-node DOWN alert — announce "back UP"
    Suppressed, // node was part of a visibility blip — recover silently
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
    /// seen up to ~45h — would otherwise break down-detection). Returns how this heartbeat
    /// should be announced (edge-triggered; first sighting is silent).
    pub fn observe(&mut self, hb: Heartbeat, received_at: u64) -> Recovery {
        match self.nodes.get_mut(&hb.node) {
            Some(e) => {
                let rec = match e.alert {
                    Alert::DownPerNode => Recovery::Node,
                    Alert::DownSuppressed => Recovery::Suppressed,
                    Alert::None => Recovery::None,
                };
                e.received_at = received_at;
                e.hb = hb;
                e.alert = Alert::None;
                rec
            }
            None => {
                self.nodes.insert(
                    hb.node.clone(),
                    Entry {
                        received_at,
                        hb,
                        alert: Alert::None,
                    },
                );
                Recovery::None
            }
        }
    }

    #[allow(dead_code)] // used by tests + a useful query API; prod path uses snapshot/pending_down
    pub fn is_up(&self, node: &str, now: u64) -> bool {
        self.nodes
            .get(node)
            .map(|e| now.saturating_sub(e.received_at) <= self.down_after)
            .unwrap_or(false)
    }

    pub fn known_count(&self) -> usize {
        self.nodes.len()
    }

    /// Nodes silent for more than `down_after + grace` that have NOT yet been alerted. The
    /// grace lets a *wave* of simultaneous silences fully land before any per-node alert fires,
    /// so the mass-blip guard (which tests `down_count`) sees the whole wave instead of only the
    /// first sweep's staggered subset. Pure (no mutation).
    pub fn pending_down(&self, now: u64, grace: u64) -> Vec<String> {
        let threshold = self.down_after + grace;
        self.nodes
            .iter()
            .filter(|(_, e)| {
                e.alert == Alert::None && now.saturating_sub(e.received_at) > threshold
            })
            .map(|(n, _)| n.clone())
            .collect()
    }

    /// Count of nodes silent past `down_after`, REGARDLESS of alert state. The true size of a
    /// simultaneous silence, and what the mass-blip guard tests: using it (not just this sweep's
    /// un-alerted `pending_down`) means a staggered wave reads as one mass event rather than
    /// leaking per-node DOWN alerts for the early-crossing nodes.
    pub fn down_count(&self, now: u64) -> usize {
        self.nodes
            .values()
            .filter(|e| now.saturating_sub(e.received_at) > self.down_after)
            .count()
    }

    /// Mark the given nodes as alerted — per-node (suppressed=false) or visibility-blip
    /// (suppressed=true). Prevents re-alerting each sweep; recovery uses the stored kind.
    pub fn set_alert(&mut self, nodes: &[String], suppressed: bool) {
        let kind = if suppressed {
            Alert::DownSuppressed
        } else {
            Alert::DownPerNode
        };
        for n in nodes {
            if let Some(e) = self.nodes.get_mut(n) {
                e.alert = kind;
            }
        }
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
            ts: 0,
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
        assert_eq!(p.observe(hb("n"), 1000), Recovery::None);
    }
    #[test]
    fn per_node_down_then_recovers() {
        let mut p = Presence::new(90);
        p.observe(hb("n"), 1000);
        assert!(p.pending_down(1050, 0).is_empty()); // not down yet
        assert_eq!(p.pending_down(1200, 0), vec!["n".to_string()]); // crossed down
        p.set_alert(&["n".to_string()], false); // per-node alert
        assert!(p.pending_down(1300, 0).is_empty()); // already alerted -> no repeat
        assert_eq!(p.observe(hb("n"), 1400), Recovery::Node); // recovery announced per-node
        assert_eq!(p.pending_down(1600, 0), vec!["n".to_string()]); // future outage re-detects
    }
    #[test]
    fn suppressed_down_recovers_silently() {
        let mut p = Presence::new(90);
        p.observe(hb("n"), 1000);
        let _ = p.pending_down(1200, 0);
        p.set_alert(&["n".to_string()], true); // visibility-blip suppression
        assert!(p.pending_down(1300, 0).is_empty()); // no repeat
        assert_eq!(p.observe(hb("n"), 1400), Recovery::Suppressed); // recovers silently
    }
    #[test]
    fn known_count_tracks_nodes() {
        let mut p = Presence::new(90);
        assert_eq!(p.known_count(), 0);
        p.observe(hb("a"), 1);
        p.observe(hb("b"), 1);
        assert_eq!(p.known_count(), 2);
    }

    #[test]
    fn grace_delays_pending() {
        let mut p = Presence::new(90);
        p.observe(hb("n"), 1000);
        // silent past down_after (90) but within grace (45) -> not yet eligible to alert
        assert!(p.pending_down(1100, 45).is_empty()); // 100s < 90+45
        // past down_after + grace -> eligible
        assert_eq!(p.pending_down(1140, 45), vec!["n".to_string()]); // 140s > 135
    }
    #[test]
    fn down_count_ignores_alert_state() {
        let mut p = Presence::new(90);
        p.observe(hb("a"), 1000);
        p.observe(hb("b"), 1000);
        assert_eq!(p.down_count(1050), 0); // both fresh
        assert_eq!(p.down_count(1200), 2); // both silent past 90
        p.set_alert(&["a".to_string()], false); // alerting does NOT change down_count
        assert_eq!(p.down_count(1200), 2);
    }
    #[test]
    fn staggered_wave_reads_as_mass_not_per_node() {
        // 7 nodes whose last-seen times are staggered across a 30s window, then all go silent.
        // With grace, by the time the earliest node is eligible to alert, down_count already
        // counts the whole wave -> the sweep classifies it mass (one blip), zero per-node.
        let mut p = Presence::new(90);
        for (i, n) in ["n1", "n2", "n3", "n4", "n5", "n6", "n7"].iter().enumerate() {
            p.observe(hb(n), 1000 + i as u64 * 5); // last-seen spread 1000..=1030
        }
        let grace = 45u64;
        // earliest node (received 1000) becomes eligible at 1000+90+45 = 1135
        assert!(!p.pending_down(1140, grace).is_empty());
        let known = p.known_count();
        let down = p.down_count(1140); // received <= 1045 -> all 7 (spread ends 1030)
        assert_eq!(down, 7);
        assert!(known >= 4 && down >= (known + 1) / 2); // -> ONE visibility blip, not per-node spam
    }
}
