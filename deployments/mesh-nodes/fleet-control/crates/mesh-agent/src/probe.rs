use fleet_proto::{ProbeKind, ProbeReply, ProbeRequest};
use std::time::Instant;

/// Pure: build the argv for a probe. No shell, no string interpolation into a command line.
pub fn probe_argv(kind: &ProbeKind, target: &str, timeout_ms: u64) -> Vec<String> {
    let secs = (timeout_ms.max(1000) / 1000).to_string();
    let argv: Vec<&str> = match kind {
        ProbeKind::Ping => vec!["ping", "-c", "1", "-W", &secs, target],
        ProbeKind::Dns => vec!["nslookup", target],
        ProbeKind::Http => vec!["wget", "-q", "-O", "/dev/null", "-T", &secs, target],
    };
    argv.into_iter().map(String::from).collect()
}

pub async fn run_probe(node: &str, req: ProbeRequest) -> ProbeReply {
    let timeout = if req.timeout_ms == 0 { 3000 } else { req.timeout_ms };
    let argv = probe_argv(&req.kind, &req.target, timeout);
    let start = Instant::now();
    let out = tokio::process::Command::new(&argv[0])
        .args(&argv[1..])
        .output()
        .await;
    let latency_ms = start.elapsed().as_millis() as u64;
    let (ok, detail) = match out {
        Ok(o) => (
            o.status.success(),
            String::from_utf8_lossy(&o.stdout).chars().take(400).collect(),
        ),
        Err(e) => (false, e.to_string()),
    };
    ProbeReply {
        node: node.into(),
        kind: req.kind,
        target: req.target,
        ok,
        latency_ms,
        detail,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use fleet_proto::ProbeKind;
    #[test]
    fn ping_argv_no_shell() {
        let a = probe_argv(&ProbeKind::Ping, "8.8.8.8", 1000);
        assert_eq!(a, vec!["ping", "-c", "1", "-W", "1", "8.8.8.8"]);
    }
    #[test]
    fn dns_argv() {
        assert_eq!(
            probe_argv(&ProbeKind::Dns, "example.com", 2000),
            vec!["nslookup", "example.com"]
        );
    }
    #[test]
    fn http_argv() {
        assert_eq!(
            probe_argv(&ProbeKind::Http, "http://x/healthz", 3000),
            vec!["wget", "-q", "-O", "/dev/null", "-T", "3", "http://x/healthz"]
        );
    }
}
