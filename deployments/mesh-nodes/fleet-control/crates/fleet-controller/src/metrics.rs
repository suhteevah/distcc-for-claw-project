use prometheus::{opts, Encoder, GaugeVec, Registry, TextEncoder};

pub struct Metrics {
    reg: Registry,
    up: GaugeVec,
    overlay: GaugeVec,
    probe_latency: GaugeVec,
    probe_ok: GaugeVec,
    peers: GaugeVec,
    sig_worst: GaugeVec,
    sig_avg: GaugeVec,
}
impl Metrics {
    pub fn new() -> Self {
        let reg = Registry::new();
        let up = GaugeVec::new(opts!("mesh_node_up", "node present"), &["node"]).unwrap();
        let overlay =
            GaugeVec::new(opts!("mesh_node_overlay_free_mb", "overlay MB free"), &["node"]).unwrap();
        let probe_latency = GaugeVec::new(
            opts!("mesh_probe_latency_ms", "last scheduled probe latency"),
            &["node", "target"],
        )
        .unwrap();
        let probe_ok = GaugeVec::new(
            opts!("mesh_probe_ok", "last scheduled probe success (1/0)"),
            &["node", "target"],
        )
        .unwrap();
        let peers =
            GaugeVec::new(opts!("mesh_node_peers", "mesh peer count"), &["node"]).unwrap();
        let sig_worst = GaugeVec::new(
            opts!("mesh_node_signal_worst_dbm", "weakest mesh peer signal (dBm)"),
            &["node"],
        )
        .unwrap();
        let sig_avg = GaugeVec::new(
            opts!("mesh_node_signal_avg_dbm", "mean mesh peer signal (dBm)"),
            &["node"],
        )
        .unwrap();
        reg.register(Box::new(up.clone())).unwrap();
        reg.register(Box::new(overlay.clone())).unwrap();
        reg.register(Box::new(probe_latency.clone())).unwrap();
        reg.register(Box::new(probe_ok.clone())).unwrap();
        reg.register(Box::new(peers.clone())).unwrap();
        reg.register(Box::new(sig_worst.clone())).unwrap();
        reg.register(Box::new(sig_avg.clone())).unwrap();
        Metrics { reg, up, overlay, probe_latency, probe_ok, peers, sig_worst, sig_avg }
    }
    pub fn set_node(&self, node: &str, up: bool, overlay_free_mb: u64) {
        self.up.with_label_values(&[node]).set(if up { 1.0 } else { 0.0 });
        self.overlay
            .with_label_values(&[node])
            .set(overlay_free_mb as f64);
    }
    pub fn set_probe(&self, node: &str, target: &str, ok: bool, latency_ms: u64) {
        self.probe_latency
            .with_label_values(&[node, target])
            .set(latency_ms as f64);
        self.probe_ok
            .with_label_values(&[node, target])
            .set(if ok { 1.0 } else { 0.0 });
    }
    /// Export mesh link health carried in the heartbeat: peer count, plus the weakest and
    /// mean per-peer signal. Skips the signal gauges when there are no peers (e.g. a wired
    /// node with no mesh links) so they never read a misleading 0 dBm.
    pub fn set_mesh(&self, node: &str, peers: u32, signals: &[i32]) {
        self.peers.with_label_values(&[node]).set(peers as f64);
        if !signals.is_empty() {
            let worst = *signals.iter().min().unwrap(); // most negative = weakest link
            let avg = signals.iter().map(|&s| s as f64).sum::<f64>() / signals.len() as f64;
            self.sig_worst.with_label_values(&[node]).set(worst as f64);
            self.sig_avg.with_label_values(&[node]).set(avg);
        }
    }
    pub fn render(&self) -> String {
        let mut buf = Vec::new();
        TextEncoder::new().encode(&self.reg.gather(), &mut buf).unwrap();
        String::from_utf8(buf).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn renders_node_up_gauge() {
        let m = Metrics::new();
        m.set_node("mesh-ap-07", true, 3200);
        let text = m.render();
        assert!(text.contains("mesh_node_up{node=\"mesh-ap-07\"} 1"));
        assert!(text.contains("mesh_node_overlay_free_mb{node=\"mesh-ap-07\"} 3200"));
    }
    #[test]
    fn renders_probe_gauges() {
        let m = Metrics::new();
        m.set_probe("mesh-ap-07", "192.168.168.168", true, 3);
        let text = m.render();
        assert!(text.contains("mesh_probe_latency_ms{node=\"mesh-ap-07\",target=\"192.168.168.168\"} 3"));
        assert!(text.contains("mesh_probe_ok{node=\"mesh-ap-07\",target=\"192.168.168.168\"} 1"));
    }
    #[test]
    fn renders_mesh_gauges() {
        let m = Metrics::new();
        m.set_mesh("mesh-ap-04", 3, &[-47, -61, -53]);
        let text = m.render();
        assert!(text.contains("mesh_node_peers{node=\"mesh-ap-04\"} 3"));
        assert!(text.contains("mesh_node_signal_worst_dbm{node=\"mesh-ap-04\"} -61"));
        assert!(text.contains("mesh_node_signal_avg_dbm{node=\"mesh-ap-04\"} -53.6"));
    }
    #[test]
    fn mesh_skips_signal_gauges_when_no_peers() {
        let m = Metrics::new();
        m.set_mesh("wired", 0, &[]);
        let text = m.render();
        assert!(text.contains("mesh_node_peers{node=\"wired\"} 0"));
        assert!(!text.contains("mesh_node_signal_worst_dbm{node=\"wired\"}"));
    }
}
