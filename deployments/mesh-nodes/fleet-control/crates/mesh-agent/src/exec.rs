use crate::command::Plan;
use fleet_proto::CommandReply;
use std::time::{Duration, Instant};
use tokio::process::Command as PCommand;

pub fn cap(s: &str, max: usize) -> String {
    if s.len() <= max {
        s.to_string()
    } else {
        s.chars().take(max).collect()
    }
}

/// Execute a vetted Plan. Reboot is signalled to the caller (reply first, then reboot).
pub async fn execute(plan: Plan, timeout_secs: u64, max_out: usize) -> (CommandReply, bool /*do_reboot*/) {
    match plan {
        Plan::Reject(why) => (CommandReply::err(why), false),
        Plan::Reboot => (
            CommandReply {
                ok: true,
                exit: 0,
                stdout: "rebooting".into(),
                stderr: String::new(),
                duration_ms: 0,
                error: None,
            },
            true,
        ),
        Plan::FetchFile(p) => match tokio::fs::read(&p).await {
            Ok(bytes) => {
                let s = String::from_utf8_lossy(&bytes);
                (
                    CommandReply {
                        ok: true,
                        exit: 0,
                        stdout: cap(&s, max_out),
                        stderr: String::new(),
                        duration_ms: 0,
                        error: None,
                    },
                    false,
                )
            }
            Err(e) => (CommandReply::err(format!("file.fetch {p}: {e}")), false),
        },
        Plan::Run(argv) => {
            let start = Instant::now();
            let fut = PCommand::new(&argv[0]).args(&argv[1..]).output();
            let res = tokio::time::timeout(Duration::from_secs(timeout_secs), fut).await;
            let duration_ms = start.elapsed().as_millis() as u64;
            match res {
                Err(_) => (
                    CommandReply {
                        ok: false,
                        exit: -1,
                        stdout: String::new(),
                        stderr: format!("timeout after {timeout_secs}s"),
                        duration_ms,
                        error: Some("timeout".into()),
                    },
                    false,
                ),
                Ok(Err(e)) => (CommandReply::err(format!("spawn {}: {e}", argv[0])), false),
                Ok(Ok(o)) => (
                    CommandReply {
                        ok: o.status.success(),
                        exit: o.status.code().unwrap_or(-1),
                        stdout: cap(&String::from_utf8_lossy(&o.stdout), max_out),
                        stderr: cap(&String::from_utf8_lossy(&o.stderr), max_out),
                        duration_ms,
                        error: None,
                    },
                    false,
                ),
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn caps_output() {
        let s = "x".repeat(1000);
        assert_eq!(cap(&s, 10).len(), 10);
        assert_eq!(cap("short", 10), "short");
    }
}
