# NATS messaging fabric (P2)

3-node **NATS + JetStream** cluster on the AC-1304 mesh fleet — the messaging backbone
P3's Rust `mesh-agent` will use for heartbeat + work distribution.

## Cluster

| node       | role   | LAN IP (reserved) | ports                          |
|------------|--------|-------------------|--------------------------------|
| mesh-ap-06 | anchor | 192.168.168.144   | 4222 client · 6222 cluster · 8222 monitor |
| mesh-ap-07 | relay  | 192.168.168.145   | "                              |
| mesh-ap-08 | relay  | 192.168.168.146   | "                              |

- **Cluster name:** `clawmesh-nats`. Routes are full-mesh by LAN IP (cluster + JetStream
  traffic stays on the LAN, never tailnet).
- **JetStream:** file store at `/overlay/nats-js` (the expanded 3.4G overlay — see P2 plan
  Tasks 1–2), `max_file_store 512MB`, `max_memory_store 64MB`.
- **nats-server** `v2.14.2`, **natscli** `v0.4.0` — prebuilt linux-arm7 static binaries in
  `assets/` (committed; pushed to `/usr/sbin/{nats-server,nats}`).
- **Auth:** shared token (client) + cluster `user/password` (route auth). v2.14 rejects a
  bare `token` in the `cluster{}` block — must be user/password.

## Streams

- **`FLEET`** — subjects `fleet.>`, **replicas=3**, file storage, retention=limits,
  max-age 24h, max-bytes 256MB, discard=old, dupe-window 2m.
- Planned subjects (P3): `fleet.heartbeat.<node>`, `fleet.work.<type>` (queue-group consumers).

## Files

| file              | what                                                            |
|-------------------|----------------------------------------------------------------|
| `assets/nats-server` · `assets/nats` | arm7 static binaries (cached)               |
| `nats.conf.tmpl`  | per-node config template (`__NODE__ __TOKEN__ __CLUSTER_TOKEN__ __ROUTES__`) |
| `nats.init`       | procd init (`/etc/init.d/nats`, respawn, SIGHUP reload)        |
| `nats-deploy.sh`  | kokonoe orchestrator — render config + push binary/conf(600)/init + enable |
| `nats-verify.sh`  | health: each node serving + JetStream `cluster_size==3` + leader |

## Operate

Tokens are **env-only, never committed** (gitignored `nats/.tokens.env`, mode 600):

```bash
cd "/j/distcc for claw project/deployments/mesh-nodes"
# (re)deploy the whole cluster — idempotent
bash nats/nats-deploy.sh                 # sources nats/.tokens.env automatically
# health check
bash nats/nats-verify.sh

# add a client / inspect (natscli on any cluster node)
source lib/common.sh && . nats/.tokens.env
node_ssh mesh-ap-06 'export NATS_URL="nats://'"$NATS_TOKEN"'@localhost:4222"; nats stream ls'
```

A client elsewhere connects with `nats://<NATS_TOKEN>@192.168.168.144:4222` (or .145/.146 —
any cluster node; the cluster routes the rest).

## Monitoring

`prometheus-nats-exporter` runs on **cnc** (`--network host`, port `7777`, `unless-stopped`)
scraping all 3 nodes' `:8222`; cnc prometheus job `nats` scrapes `host.containers.internal:7777`.
NATS itself only serves JSON on `:8222` (`/varz`,`/jsz`,`/healthz`) — not Prometheus format —
hence the exporter.

```bash
# redeploy the exporter on cnc if needed
podman run -d --name nats-exporter --restart unless-stopped --network host \
  docker.io/natsio/prometheus-nats-exporter:latest -port 7777 -varz -jsz=all \
  http://192.168.168.144:8222 http://192.168.168.145:8222 http://192.168.168.146:8222
```

## Notes

- **num_routes is not a peer count** — NATS 2.10+ pools ~3 connections per peer, so 2 peers
  shows `num_routes:8`. Verify cluster health via JetStream `cluster_size` + an elected leader
  (`nats-verify.sh` does this), not raw route count.
- Deploy scripts run under busybox `ash`; the repo `.gitattributes` forces LF on `*.sh/*.init/*.tmpl`.
- 24MB natscli pushes over tailnet can flap the link — natscli is only needed on one node for
  stream ops; the round-trip test pointed one node's client at peers' `:4222` over the LAN.
