use fleet_proto::Heartbeat;

#[derive(Debug, PartialEq)]
pub struct Stats {
    pub uptime_s: u64,
    pub load1: f64,
    pub mem_free_mb: u64,
    pub overlay_free_mb: u64,
    pub mesh_peers: u32,
    pub mesh_signals: Vec<i32>,
}
impl Stats {
    /// Pure: parse the raw text of /proc/uptime, /proc/loadavg, /proc/meminfo,
    /// `df -k /overlay` (last line), and `iw dev phy1-mesh0 station dump`.
    pub fn parse(uptime: &str, loadavg: &str, meminfo: &str, df: &str, iw: &str) -> Stats {
        let uptime_s = uptime
            .split('.')
            .next()
            .and_then(|v| v.trim().parse().ok())
            .unwrap_or(0);
        let load1 = loadavg
            .split_whitespace()
            .next()
            .and_then(|v| v.parse().ok())
            .unwrap_or(0.0);
        let mem_free_mb = meminfo
            .lines()
            .find(|l| l.starts_with("MemAvailable"))
            .and_then(|l| l.split_whitespace().nth(1))
            .and_then(|v| v.parse::<u64>().ok())
            .map(|kb| kb / 1024)
            .unwrap_or(0);
        let overlay_free_mb = df
            .split_whitespace()
            .nth(3)
            .and_then(|v| v.parse::<u64>().ok())
            .map(|kb| kb / 1024)
            .unwrap_or(0);
        let mesh_signals: Vec<i32> = iw
            .lines()
            .filter_map(|l| {
                l.find("signal:")
                    .and_then(|i| l[i + 7..].split_whitespace().next())
                    .and_then(|v| v.parse().ok())
            })
            .collect();
        let mesh_peers = iw.matches("Station").count() as u32;
        Stats {
            uptime_s,
            load1,
            mem_free_mb,
            overlay_free_mb,
            mesh_peers,
            mesh_signals,
        }
    }
    pub fn into_heartbeat(self, node: &str, ts: u64, nats_connected: bool) -> Heartbeat {
        Heartbeat {
            node: node.into(),
            ts,
            uptime_s: self.uptime_s,
            load1: self.load1,
            mem_free_mb: self.mem_free_mb,
            overlay_free_mb: self.overlay_free_mb,
            mesh_peers: self.mesh_peers,
            mesh_signals: self.mesh_signals,
            nats_connected,
            agent_version: env!("CARGO_PKG_VERSION").into(),
        }
    }
}

/// Side-effecting collector used at runtime (reads files / runs `iw`). Not unit-tested.
pub async fn collect(node: &str, ts: u64, nats_connected: bool) -> Heartbeat {
    use tokio::process::Command;
    let read = |p: &str| std::fs::read_to_string(p).unwrap_or_default();
    let df = Command::new("df")
        .args(["-k", "/overlay"])
        .output()
        .await
        .map(|o| {
            String::from_utf8_lossy(&o.stdout)
                .lines()
                .last()
                .unwrap_or("")
                .to_string()
        })
        .unwrap_or_default();
    let iw = Command::new("iw")
        .args(["dev", "phy1-mesh0", "station", "dump"])
        .output()
        .await
        .map(|o| String::from_utf8_lossy(&o.stdout).into_owned())
        .unwrap_or_default();
    Stats::parse(
        &read("/proc/uptime"),
        &read("/proc/loadavg"),
        &read("/proc/meminfo"),
        &df,
        &iw,
    )
    .into_heartbeat(node, ts, nats_connected)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn parses_proc_and_iw() {
        let uptime = "1234.50 5678.0\n";
        let loadavg = "0.15 0.10 0.08 1/60 999\n";
        let meminfo = "MemTotal: 512000 kB\nMemAvailable: 327680 kB\n";
        let df = "/dev/loop0  3500000  100000  3300000  3% /overlay\n";
        let iw = "Station aa:bb signal: -42 dBm\nStation cc:dd signal: -50 dBm\n";
        let s = Stats::parse(uptime, loadavg, meminfo, df, iw);
        assert_eq!(s.uptime_s, 1234);
        assert_eq!(s.load1, 0.15);
        assert_eq!(s.mem_free_mb, 320);
        assert_eq!(s.overlay_free_mb, 3300000 / 1024);
        assert_eq!(s.mesh_peers, 2);
        assert_eq!(s.mesh_signals, vec![-42, -50]);
    }
}
