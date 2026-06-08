use prometheus::{opts, Encoder, GaugeVec, Registry, TextEncoder};

pub struct Metrics {
    reg: Registry,
    up: GaugeVec,
    overlay: GaugeVec,
    probe_latency: GaugeVec,
    probe_ok: GaugeVec,
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
        reg.register(Box::new(up.clone())).unwrap();
        reg.register(Box::new(overlay.clone())).unwrap();
        reg.register(Box::new(probe_latency.clone())).unwrap();
        reg.register(Box::new(probe_ok.clone())).unwrap();
        Metrics { reg, up, overlay, probe_latency, probe_ok }
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
}
