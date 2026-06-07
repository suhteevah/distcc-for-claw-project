# Fleet Control Plane (P3)

A control plane over the P2 NATS bus: a Rust **`mesh-agent`** on all 7 AC-1304 nodes
(heartbeat + on-demand probes + structured remote command/config) driven by a dedicated
cnc **`fleet-controller`** systemd service (presence ingest, HTTP→NATS dispatch, prometheus
gauges, event surfacing).

## Workspace

```
fleet-control/                Cargo workspace
  crates/fleet-proto          shared wire contract (Heartbeat/Command/Probe types, subjects)
  crates/mesh-agent           node binary (armv7-musl static, ~2.2 MB) — all 7 nodes
  crates/fleet-controller     cnc binary (x86_64) — systemd service
  deploy/                     procd init, systemd unit, deploy scripts, cached armv7 binary
```

## Subjects

| subject | dir | pattern |
|---|---|---|
| `fleet.heartbeat.<node>` | agent → controller | pub (also captured by JetStream `FLEET`) |
| `fleet.ctl.<node>`       | controller → agent | **request/reply** (ephemeral — NOT streamed) |
| `fleet.probe.<node>` / `fleet.probe.all` | controller → agent | **request/reply** |

> ⚠️ The JetStream `FLEET` stream captures `fleet.heartbeat.>` + `fleet.event.>` ONLY.
> It must NOT capture `fleet.ctl.*` / `fleet.probe.*` — a stream over a request/reply subject
> returns a JetStream PubAck to the requester's inbox and shadows the agent's reply.
> (P2 created FLEET as `fleet.>`; P3 narrowed it.)

## mesh-agent

- NATS client; cluster nodes (06/07/08) → `localhost:4222`, client-only (01/02/04/03) →
  cluster LAN IPs with failover. Token extracted from the URL → `ConnectOptions::token`
  (async-nats needs it explicit; natscli's URL-embedded form doesn't apply).
- **Heartbeat** every 30s: uptime/load/mem/overlay/mesh-peers+signals/version.
- **Probes**: ping/dns/http (argv-built, no shell).
- **Commands** (`fleet.ctl.<node>`), allow-listed verbs only:
  `svc.restart|status`, `uci.get|set|commit`, `wifi.reload`, `net.reload`,
  `pkg.add|del`, `file.fetch`, `reboot`, `probe.*`, `exec.raw`.
- **Gates:** mutating verbs (`uci.commit`,`pkg.*`,`reboot`) need `confirm:true`;
  `exec.raw` + `reboot` also need per-node env (`MESH_AGENT_ALLOW_RAW=1` / `MESH_AGENT_ALLOW_REBOOT=1`).
  Unknown verb → structured reject, never crash. Per-command timeout + output cap.
- **Audit:** `/var/log/mesh-agent-audit.jsonl` (every command). Config in `/etc/mesh-agent.env` (600).

Build (armv7-musl static, on cnc — has cross+podman):
```bash
# cnc's ~/.cargo/config.toml forces linker=clang+mold which isn't in the cross image:
cp ~/.cargo/config.toml ~/.cargo/config.toml.bak && printf '[build]\n' > ~/.cargo/config.toml
cd /opt/openclaw/fleet-control && CROSS_CONTAINER_ENGINE=podman cross build -p mesh-agent --release --target armv7-unknown-linux-musleabihf
mv ~/.cargo/config.toml.bak ~/.cargo/config.toml          # restore
```
Deploy (from kokonoe, binary cached in `deploy/assets/`):
```bash
cd "/j/distcc for claw project/deployments/mesh-nodes"
export NATS_TOKEN=$(. nats/.tokens.env; echo $NATS_TOKEN)
bash fleet-control/deploy/mesh-agent-deploy.sh            # all nodes (or pass node names)
```

## fleet-controller (cnc)

- systemd `openclaw-fleet-controller.service`; direct NATS client (failover .144/.145/.146).
- **Presence:** subscribes `fleet.heartbeat.*`, stamps **its own receive time** (node NTP skew
  seen up to ~25 min would otherwise break down-detection), marks down after `FLEET_DOWN_AFTER_SECS` (90).
- **Metrics** (`:9094/metrics`): `mesh_node_up{node}`, `mesh_node_overlay_free_mb{node}` →
  cnc prometheus job `fleet-controller` (`host.containers.internal:9094`).
- **Dispatch API** (`:9096`):
  - `GET  /fleet/status` — presence JSON
  - `POST /fleet/ctl/<node>`   `{verb,args,confirm?}` → agent reply
  - `POST /fleet/probe/<node>` `{kind,target,timeout_ms?}` → probe reply
- **Surfacing:** events logged (journald) + `mesh_node_up` gauge (alert via prometheus on `==0`).
  Optional webhook via `FLEET_NOTIFY_URL`. (No openclaw-core notify HTTP endpoint exists; a
  Telegram/Discord bridge is a fast-follow.)
- Config in `/etc/fleet-controller.env` (600, holds the token). Port note: **9095 is prometheus**
  on cnc → control API uses **9096**.

Install/refresh on cnc:
```bash
cd /opt/openclaw/fleet-control && RUSTC_WRAPPER= cargo build -p fleet-controller --release
NATS_TOKEN=... bash deploy/fleet-controller-deploy.sh    # installs binary+unit+env, enables
```

## Examples
```bash
curl -s localhost:9096/fleet/status
curl -s -XPOST localhost:9096/fleet/ctl/mesh-ap-07   -d '{"verb":"svc.status","args":{"name":"mesh-agent"}}'
curl -s -XPOST localhost:9096/fleet/probe/mesh-ap-07 -d '{"kind":"ping","target":"192.168.168.144"}'
# mutating needs confirm:
curl -s -XPOST localhost:9096/fleet/ctl/mesh-ap-07   -d '{"verb":"pkg.add","args":{"name":"tcpdump"},"confirm":true}'
```

## Known follow-ups
- **Node NTP skew** (ap-02 ~25 min, ap-07 ~2 min behind cnc) — fleet hygiene; presence is already
  immune (receive-time stamped) but worth fixing the nodes' `sysntpd`.
- Scheduled/periodic probes + JetStream history capture (the spec's fast-follow).
- Telegram/Discord alert bridge for `notify::event`.
- Build is on cnc (Windows host's mingw dlltool can't handle the spaced repo path).
