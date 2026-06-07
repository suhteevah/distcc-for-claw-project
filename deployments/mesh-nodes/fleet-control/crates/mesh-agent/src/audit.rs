use serde_json::json;
use std::io::Write;

pub fn audit_line(
    ts: u64,
    verb: &str,
    args: &serde_json::Value,
    confirm: bool,
    exit: i32,
    output_bytes: usize,
) -> String {
    json!({
        "ts": ts,
        "verb": verb,
        "args": args,
        "confirm": confirm,
        "exit": exit,
        "output_bytes": output_bytes
    })
    .to_string()
}
pub fn append(path: &str, line: &str) {
    if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(path) {
        let _ = writeln!(f, "{line}");
    } else {
        tracing::warn!(%path, "audit append failed");
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    #[test]
    fn line_is_valid_json_with_fields() {
        let line = audit_line(1700, "pkg.add", &json!({"name":"x"}), true, 0, 12);
        let v: serde_json::Value = serde_json::from_str(&line).unwrap();
        assert_eq!(v["verb"], "pkg.add");
        assert_eq!(v["confirm"], true);
        assert_eq!(v["exit"], 0);
        assert_eq!(v["output_bytes"], 12);
    }
}
