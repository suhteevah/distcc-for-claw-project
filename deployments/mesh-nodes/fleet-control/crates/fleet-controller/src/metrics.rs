use prometheus::{opts, Encoder, GaugeVec, Registry, TextEncoder};

pub struct Metrics {
    reg: Registry,
    up: GaugeVec,
    overlay: GaugeVec,
}
impl Metrics {
    pub fn new() -> Self {
        let reg = Registry::new();
        let up = GaugeVec::new(opts!("mesh_node_up", "node present"), &["node"]).unwrap();
        let overlay =
            GaugeVec::new(opts!("mesh_node_overlay_free_mb", "overlay MB free"), &["node"]).unwrap();
        reg.register(Box::new(up.clone())).unwrap();
        reg.register(Box::new(overlay.clone())).unwrap();
        Metrics { reg, up, overlay }
    }
    pub fn set_node(&self, node: &str, up: bool, overlay_free_mb: u64) {
        self.up.with_label_values(&[node]).set(if up { 1.0 } else { 0.0 });
        self.overlay
            .with_label_values(&[node])
            .set(overlay_free_mb as f64);
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
}
