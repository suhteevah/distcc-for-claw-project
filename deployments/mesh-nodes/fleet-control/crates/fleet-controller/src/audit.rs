use std::io::Write;

pub fn append(path: &str, line: &str) {
    if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(path) {
        let _ = writeln!(f, "{line}");
    } else {
        tracing::warn!(%path, "audit append failed");
    }
}
