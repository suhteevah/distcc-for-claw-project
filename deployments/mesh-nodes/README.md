# mesh-nodes — AC-1304 fleet baseline (P1)

OpenWrt **25.12.3** dumb-AP mesh fleet (`ipq40xx/chromium`, apk) on the SonicWall LAN
(`192.168.168.0/24`), broadcasting `Home_EXT` + 802.11s `homemesh` on ch149. Offloads the
flaky TP-Link; all nodes are dumb-APs (firewall/odhcpd/dnsmasq off, DHCP from the SonicWall).

## Usage (from kokonoe, over tailnet)
```bash
export FLEET_PSK='<Home_EXT key>'          # never commit it
export CNC_LOG_IP=192.168.168.100          # cnc (default)
bash audit.sh <node>|all                   # READ-ONLY compliance check
bash deploy.sh <node>                       # apk install + baseline + role overlay (dead-man protected)
```

## Files
- `packages.list` — Layer-0 apk packages (baked image + deploy install).
- `manifest.tsv` — node → role → tailnet IP (authoritative inventory).
- `lib/common.sh` — kokonoe helpers (manifest lookup, tailnet ssh w/ warning filter, push_file).
- `baseline.sh` — on-node idempotent common config (dumb-AP, log_ip, node-exporter LAN bind, service enables).
- `roles/{relay,anchor,office}.sh` — on-node role overlays (wireless + role services).
- `audit.sh` / `deploy.sh` — kokonoe orchestrators (deploy arms a 300s dead-man rollback around wireless changes).
- `assets/watchcat/` — watchcat init+script+config (apk fetch for watchcat is unreliable on this feed → pushed from these assets for relay nodes).
- `image/build-image.sh` — OpenWrt ImageBuilder wrapper (run on cnc) → baked factory+sysupgrade.

## Roles
- **anchor** (mesh-ap-06): wired, rsyncd on, watchcat off, 2.4 ch11.
- **relay** (mesh-ap-01/02/04/07/08): wireless backhaul, watchcat on, 2.4 ch6 + 5GHz ch149 AP + homemesh.
- **office** (mesh-ap-03): wired, 5GHz-only ch36, 2.4 off, no mesh.
- **spare** (mesh-ap-05): locked-down, OUT OF SCOPE (reflash later).

## Observability (cnc, 192.168.168.100)
- **Logs:** nodes forward syslog (busybox `logd`, uci `system.log_ip`) → `fleet-syslog.service`
  (`/opt/fleet-syslog/fleet-syslog.py`, UDP 514) → `/var/log/fleet/<host>/<date>.log`.
- **Metrics:** `prometheus-node-exporter-lua` on each node, **bound to the LAN** (`listen_interface=lan`,
  NOT loopback) → scraped by `openclaw-prometheus` (job `mesh-fleet`) via the nodes' **LAN IPs**.
  - ⚠️ The prometheus container reaches nodes via **LAN, not tailnet** (it can't route to tailscale0).
    Targets in `/opt/openclaw/openclaw-agents/monitoring/prometheus/prometheus.yml` use the LAN IPs below.
  - ✅ **Stable: SonicWall DHCP reservations (MAC-pinned, outside the dynamic pool) — won't drift:**
    `01=.140 02=.141 03=.142 04=.143 06=.144 07=.145 08=.146` (set 2026-06-07 via the SonicOS API).

## Future node bring-up
1. Flash the baked image (`firmware/openwrt-25.12.3-google_wifi/`) per the flash-procedure wiki doc:
   **write eMMC (factory.bin via USB+dd) → power-cycle-verify eMMC boot → sysupgrade if needed**.
   (The #1 trap is skipping the eMMC write — see `feedback_emmc_vs_initramfs_verify`.)
2. Set hostname, `tailscale up` (auth), add the node to `manifest.tsv`.
3. `bash deploy.sh <node>` → baseline + role.
4. Add its LAN IP to the prometheus `mesh-fleet` job; logs auto-flow once `log_ip` is set by baseline.

## Access model
Nodes use **empty-password root** over dropbear (no SSH key); survives sysupgrade keep-config.
tailnet SSH-in requires the firewall OFF (dumb-AP nodes have it off). OpenWrt has no sftp →
`cat file | ssh node 'cat > /path'` (that's what `push_file` does).
