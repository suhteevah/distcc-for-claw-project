//! Fleet config backup: pull `uci export` per node, redact secrets, write + git commit.
use crate::{config::ControllerConfig, dispatch};
use fleet_proto::Command;
use serde_json::json;

/// Replace the value of any `option key '…'` / `option password "…"` (single OR double
/// quoted) with `<redacted>`. Leaves all other lines untouched. Pure.
pub fn redact(input: &str) -> String {
    input
        .lines()
        .map(|line| {
            let t = line.trim_start();
            if t.starts_with("option key ") || t.starts_with("option password ") {
                let indent_len = line.len() - t.len();
                let indent = &line[..indent_len];
                // prefix = "option <name>" (two words)
                let name_end = t
                    .find(' ')
                    .and_then(|i| t[i + 1..].find(' ').map(|j| i + 1 + j));
                if let Some(ne) = name_end {
                    let prefix = &t[..ne];
                    let rest = t[ne..].trim_start();
                    let q = if rest.starts_with('"') { '"' } else { '\'' };
                    return format!("{indent}{prefix} {q}<redacted>{q}");
                }
            }
            line.to_string()
        })
        .collect::<Vec<_>>()
        .join("\n")
}

/// Pull config.dump from every node in `nodes`, redact, write <node>.uci, git commit.
/// Returns (nodes_backed_up, committed). Best-effort: a failing node is skipped.
pub async fn run_backup(
    nats: &async_nats::Client,
    cfg: &ControllerConfig,
    nodes: &[String],
    ts: u64,
) -> (usize, bool) {
    if let Err(e) = tokio::fs::create_dir_all(&cfg.backup_dir).await {
        tracing::error!(%e, dir = %cfg.backup_dir, "backup mkdir failed");
        return (0, false);
    }
    ensure_git_repo(&cfg.backup_dir).await;
    let cmd = Command {
        verb: "config.dump".into(),
        args: json!({}),
        confirm: false,
    };
    let mut n = 0;
    for node in nodes {
        match dispatch::ctl(nats, node, &cmd, 15).await {
            Ok(reply) if reply.ok => {
                let redacted = redact(&reply.stdout);
                let path = format!("{}/{}.uci", cfg.backup_dir, node);
                let tmp = format!("{path}.tmp");
                if tokio::fs::write(&tmp, redacted.as_bytes()).await.is_ok()
                    && tokio::fs::rename(&tmp, &path).await.is_ok()
                {
                    n += 1;
                } else {
                    tracing::warn!(%node, "backup write failed");
                }
            }
            Ok(reply) => tracing::warn!(%node, err = ?reply.error, "config.dump not ok"),
            Err(e) => tracing::warn!(%node, %e, "config.dump dispatch failed"),
        }
    }
    let committed = git_commit(&cfg.backup_dir, ts).await;
    tracing::info!(nodes = n, committed, "fleet config backup done");
    (n, committed)
}

async fn ensure_git_repo(dir: &str) {
    if tokio::fs::metadata(format!("{dir}/.git")).await.is_err() {
        let _ = run_git(dir, &["init"]).await;
        let _ = run_git(dir, &["config", "user.email", "fleet-controller@cnc"]).await;
        let _ = run_git(dir, &["config", "user.name", "fleet-controller"]).await;
    }
}

async fn git_commit(dir: &str, ts: u64) -> bool {
    let _ = run_git(dir, &["add", "-A"]).await;
    // `diff --cached --quiet` exits non-zero when there ARE staged changes
    let has_changes = matches!(
        tokio::process::Command::new("git")
            .args(["-C", dir, "diff", "--cached", "--quiet"])
            .status()
            .await,
        Ok(s) if !s.success()
    );
    if !has_changes {
        return false;
    }
    run_git(dir, &["commit", "-m", &format!("fleet config backup {ts}")]).await
}

async fn run_git(dir: &str, args: &[&str]) -> bool {
    let mut full = vec!["-C", dir];
    full.extend_from_slice(args);
    matches!(
        tokio::process::Command::new("git").args(&full).status().await,
        Ok(s) if s.success()
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn redacts_keys_and_passwords_single_and_double_quote() {
        let input = "\
config wifi-iface
    option ssid 'Home_EXT'
    option key 'sup3rs3cret'
    option encryption 'psk2'
config foo
    option password \"hunter2\"
    option other 'keepme'
";
        let out = redact(input);
        assert!(out.contains("option ssid 'Home_EXT'"));
        assert!(out.contains("option other 'keepme'"));
        assert!(out.contains("option encryption 'psk2'"));
        assert!(!out.contains("sup3rs3cret"));
        assert!(!out.contains("hunter2"));
        assert!(out.contains("option key '<redacted>'"));
        assert!(out.contains("option password \"<redacted>\""));
    }
}
