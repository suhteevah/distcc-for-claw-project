//! The command allow-list. Anything not here is rejected before any OS call.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verb {
    SvcRestart,
    SvcStatus,
    UciGet,
    UciSet,
    UciCommit,
    WifiReload,
    NetReload,
    PkgAdd,
    PkgDel,
    FileFetch,
    Reboot,
    ProbePing,
    ProbeDns,
    ProbeHttp,
    ExecRaw,
    ConfigDump,
}
impl Verb {
    pub fn parse(s: &str) -> Option<Verb> {
        use Verb::*;
        Some(match s {
            "svc.restart" => SvcRestart,
            "svc.status" => SvcStatus,
            "uci.get" => UciGet,
            "uci.set" => UciSet,
            "uci.commit" => UciCommit,
            "wifi.reload" => WifiReload,
            "net.reload" => NetReload,
            "pkg.add" => PkgAdd,
            "pkg.del" => PkgDel,
            "file.fetch" => FileFetch,
            "reboot" => Reboot,
            "probe.ping" => ProbePing,
            "probe.dns" => ProbeDns,
            "probe.http" => ProbeHttp,
            "exec.raw" => ExecRaw,
            "config.dump" => ConfigDump,
            _ => return None,
        })
    }
    /// Persistent/destructive ops requiring `confirm:true`.
    pub fn is_mutating(self) -> bool {
        use Verb::*;
        matches!(self, UciCommit | PkgAdd | PkgDel | Reboot | ExecRaw)
    }
    pub fn is_raw(self) -> bool {
        self == Verb::ExecRaw
    }
    pub fn needs_reboot_gate(self) -> bool {
        self == Verb::Reboot
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn known_verbs_parse() {
        for v in [
            "svc.restart", "svc.status", "uci.get", "uci.set", "uci.commit", "wifi.reload",
            "net.reload", "pkg.add", "pkg.del", "file.fetch", "reboot", "probe.ping",
            "probe.dns", "probe.http", "exec.raw",
        ] {
            assert!(Verb::parse(v).is_some(), "{v} should parse");
        }
    }
    #[test]
    fn unknown_verb_rejected() {
        assert!(Verb::parse("rm.rf").is_none());
    }
    #[test]
    fn config_dump_parses_and_is_readonly() {
        let v = Verb::parse("config.dump").expect("config.dump should parse");
        assert!(!v.is_mutating());
        assert!(!v.is_raw());
        assert!(!v.needs_reboot_gate());
    }
    #[test]
    fn classification() {
        assert!(Verb::parse("uci.commit").unwrap().is_mutating());
        assert!(Verb::parse("pkg.add").unwrap().is_mutating());
        assert!(Verb::parse("reboot").unwrap().is_mutating());
        assert!(!Verb::parse("svc.status").unwrap().is_mutating());
        assert!(Verb::parse("exec.raw").unwrap().is_raw());
        assert!(Verb::parse("reboot").unwrap().needs_reboot_gate());
        assert!(!Verb::parse("wifi.reload").unwrap().is_mutating());
    }
}
