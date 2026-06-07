use fleet_proto::{Command, Verb};

#[derive(Debug, Clone)]
pub struct Gates {
    pub allow_raw: bool,
    pub allow_reboot: bool,
}

#[derive(Debug, PartialEq)]
pub enum Plan {
    Run(Vec<String>),  // execute this argv (no shell unless it IS /bin/sh -c for raw)
    FetchFile(String), // read a file back, size-capped (handled by exec layer)
    Reboot,            // special: schedule reboot after replying
    Reject(String),    // refused; string is the reason (audited)
}

fn arg<'a>(c: &'a Command, k: &str) -> Option<&'a str> {
    c.args.get(k).and_then(|v| v.as_str())
}

/// Pure policy: Command -> Plan. Enforces allow-list, confirm-gate, raw-gate, reboot-gate.
pub fn plan(c: &Command, g: &Gates) -> Plan {
    let v = match Verb::parse(&c.verb) {
        Some(v) => v,
        None => return Plan::Reject(format!("unknown verb '{}'", c.verb)),
    };
    if v.is_mutating() && !c.confirm {
        return Plan::Reject(format!("verb '{}' requires confirm:true", c.verb));
    }
    if v.is_raw() && !g.allow_raw {
        return Plan::Reject("exec.raw disabled (MESH_AGENT_ALLOW_RAW unset)".into());
    }
    if v.needs_reboot_gate() && !g.allow_reboot {
        return Plan::Reject("reboot disabled (MESH_AGENT_ALLOW_REBOOT unset)".into());
    }
    let need = |k: &str| arg(c, k).map(String::from);
    use Verb::*;
    match v {
        SvcRestart => match need("name") {
            Some(n) => Plan::Run(vec![format!("/etc/init.d/{n}"), "restart".into()]),
            None => Plan::Reject("svc.restart needs args.name".into()),
        },
        SvcStatus => match need("name") {
            Some(n) => Plan::Run(vec![format!("/etc/init.d/{n}"), "status".into()]),
            None => Plan::Reject("svc.status needs args.name".into()),
        },
        UciGet => match need("path") {
            Some(p) => Plan::Run(vec!["uci".into(), "get".into(), p]),
            None => Plan::Reject("uci.get needs args.path".into()),
        },
        UciSet => match (need("path"), need("value")) {
            (Some(p), Some(val)) => Plan::Run(vec!["uci".into(), "set".into(), format!("{p}={val}")]),
            _ => Plan::Reject("uci.set needs args.path+value".into()),
        },
        UciCommit => Plan::Run(
            vec!["uci".into(), "commit".into(), need("config").unwrap_or_default()]
                .into_iter()
                .filter(|s| !s.is_empty())
                .collect(),
        ),
        WifiReload => Plan::Run(vec!["wifi".into(), "reload".into()]),
        NetReload => Plan::Run(vec!["/etc/init.d/network".into(), "reload".into()]),
        PkgAdd => match need("name") {
            Some(n) => Plan::Run(vec!["apk".into(), "add".into(), n]),
            None => Plan::Reject("pkg.add needs args.name".into()),
        },
        PkgDel => match need("name") {
            Some(n) => Plan::Run(vec!["apk".into(), "del".into(), n]),
            None => Plan::Reject("pkg.del needs args.name".into()),
        },
        FileFetch => match need("path") {
            Some(p) => Plan::FetchFile(p),
            None => Plan::Reject("file.fetch needs args.path".into()),
        },
        Reboot => Plan::Reboot,
        ExecRaw => match need("cmd") {
            Some(cmd) => Plan::Run(vec!["/bin/sh".into(), "-c".into(), cmd]),
            None => Plan::Reject("exec.raw needs args.cmd".into()),
        },
        ProbePing | ProbeDns | ProbeHttp => {
            Plan::Reject("probe.* via fleet.probe subject, not fleet.ctl".into())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use fleet_proto::Command;
    use serde_json::json;
    fn gates(raw: bool, reboot: bool) -> Gates {
        Gates {
            allow_raw: raw,
            allow_reboot: reboot,
        }
    }
    fn cmd(verb: &str, args: serde_json::Value, confirm: bool) -> Command {
        Command {
            verb: verb.into(),
            args,
            confirm,
        }
    }
    #[test]
    fn unknown_verb_rejected() {
        assert!(matches!(
            plan(&cmd("rm.rf", json!({}), true), &gates(true, true)),
            Plan::Reject(_)
        ));
    }
    #[test]
    fn svc_status_ok() {
        match plan(&cmd("svc.status", json!({"name":"nats"}), false), &gates(false, false)) {
            Plan::Run(a) => assert_eq!(a, vec!["/etc/init.d/nats", "status"]),
            _ => panic!(),
        }
    }
    #[test]
    fn mutating_without_confirm_rejected() {
        assert!(matches!(
            plan(&cmd("pkg.add", json!({"name":"tcpdump"}), false), &gates(true, true)),
            Plan::Reject(_)
        ));
    }
    #[test]
    fn pkg_add_with_confirm_ok() {
        match plan(&cmd("pkg.add", json!({"name":"tcpdump"}), true), &gates(false, false)) {
            Plan::Run(a) => assert_eq!(a, vec!["apk", "add", "tcpdump"]),
            _ => panic!(),
        }
    }
    #[test]
    fn raw_blocked_without_gate() {
        assert!(matches!(
            plan(&cmd("exec.raw", json!({"cmd":"id"}), true), &gates(false, true)),
            Plan::Reject(_)
        ));
    }
    #[test]
    fn raw_allowed_with_gate() {
        match plan(&cmd("exec.raw", json!({"cmd":"id -u"}), true), &gates(true, true)) {
            Plan::Run(a) => assert_eq!(a, vec!["/bin/sh", "-c", "id -u"]),
            _ => panic!(),
        }
    }
    #[test]
    fn reboot_needs_confirm_and_gate() {
        assert!(matches!(
            plan(&cmd("reboot", json!({}), true), &gates(true, false)),
            Plan::Reject(_)
        ));
        assert!(matches!(
            plan(&cmd("reboot", json!({}), false), &gates(true, true)),
            Plan::Reject(_)
        ));
        assert!(matches!(
            plan(&cmd("reboot", json!({}), true), &gates(true, true)),
            Plan::Reboot
        ));
    }
    #[test]
    fn uci_set_argv() {
        match plan(
            &cmd(
                "uci.set",
                json!({"path":"wireless.@wifi-iface[0].disabled","value":"0"}),
                false,
            ),
            &gates(false, false),
        ) {
            Plan::Run(a) => assert_eq!(a, vec!["uci", "set", "wireless.@wifi-iface[0].disabled=0"]),
            _ => panic!(),
        }
    }
    #[test]
    fn file_fetch_is_special() {
        match plan(&cmd("file.fetch", json!({"path":"/etc/config/wireless"}), false), &gates(false, false)) {
            Plan::FetchFile(p) => assert_eq!(p, "/etc/config/wireless"),
            _ => panic!(),
        }
    }
}
