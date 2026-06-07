//! Cluster connect helper — extracts the token from `nats://TOKEN@host:port` URLs
//! (async-nats needs it via ConnectOptions, not URL-embedded) and connects with failover.
use anyhow::Result;

fn split_token(raw: &str) -> (Option<String>, String) {
    if let Some(scheme_end) = raw.find("://") {
        let (scheme, rest) = raw.split_at(scheme_end + 3);
        if let Some(at) = rest.find('@') {
            let tok = &rest[..at];
            let host = &rest[at + 1..];
            if !tok.is_empty() && !tok.contains(':') {
                return (Some(tok.to_string()), format!("{scheme}{host}"));
            }
        }
    }
    (None, raw.to_string())
}

pub async fn connect(url_csv: &str) -> Result<async_nats::Client> {
    let mut token: Option<String> = None;
    let mut addrs = Vec::new();
    for raw in url_csv.split(',').map(|s| s.trim()).filter(|s| !s.is_empty()) {
        let (tok, addr) = split_token(raw);
        if token.is_none() {
            token = tok;
        }
        if let Ok(a) = addr.parse::<async_nats::ServerAddr>() {
            addrs.push(a);
        }
    }
    let mut opts = async_nats::ConnectOptions::new().retry_on_initial_connect();
    if let Some(t) = token {
        opts = opts.token(t);
    }
    Ok(async_nats::connect_with_options(addrs, opts).await?)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn token_extracted() {
        let (t, a) = split_token("nats://hex@192.168.168.144:4222");
        assert_eq!(t.as_deref(), Some("hex"));
        assert_eq!(a, "nats://192.168.168.144:4222");
    }
}
