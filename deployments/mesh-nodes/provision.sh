#!/bin/sh
# Layer 0 provisioner for AC-1304 mesh nodes running OpenWrt 24.10.1.
#
# Run ON the target router AFTER flashing + SSH key install + initial connectivity:
#   ssh -i ~/.ssh/claude-mesh_ed25519 root@<NEW_NODE_IP> 'sh -s' < provision.sh NODE_NAME
# OR copy and run locally:
#   scp provision.sh root@<NEW_NODE_IP>:/tmp/ && ssh root@<NEW_NODE_IP> "sh /tmp/provision.sh NODE_NAME"
#
# Idempotent: safe to re-run. Re-running re-applies config, does not double-install packages.

set -eu

NODE_NAME="${1:-}"
if [ -z "$NODE_NAME" ]; then
  echo "Usage: $0 <node_name>   (e.g. mesh-ap-02)" >&2
  exit 1
fi

# Fleet targets (tailnet IPs)
SYSLOG_SINK="${SYSLOG_SINK:-100.108.202.49}"   # cnc-server tailnet
SYSLOG_PORT="${SYSLOG_PORT:-514}"

echo "=== $(date -Iseconds) provisioning $NODE_NAME ==="

# --- opkg index refresh + package install ---
opkg update
opkg install \
  prometheus-node-exporter-lua \
  prometheus-node-exporter-lua-wifi \
  prometheus-node-exporter-lua-wifi_stations \
  prometheus-node-exporter-lua-openwrt \
  prometheus-node-exporter-lua-netstat \
  prometheus-node-exporter-lua-nft-counters \
  watchcat \
  tailscale \
  kmod-tun \
  ca-bundle

# --- hostname ---
uci set system.@system[0].hostname="$NODE_NAME"

# --- remote syslog + larger local ring ---
uci set system.@system[0].log_size='512'
uci set system.@system[0].log_ip="$SYSLOG_SINK"
uci set system.@system[0].log_port="$SYSLOG_PORT"
uci set system.@system[0].log_proto='udp'
uci delete system.@system[0].log_prefix 2>/dev/null || true
uci commit system

# --- prometheus node exporter: listen on all interfaces ---
uci set prometheus-node-exporter-lua.main.listen_interface='*'
uci set prometheus-node-exporter-lua.main.listen_port='9100'
uci delete prometheus-node-exporter-lua.main.listen_ipv4 2>/dev/null || true
uci commit prometheus-node-exporter-lua

# --- watchcat: ping gateway + 1.1.1.1, reboot on extended outage ---
uci set watchcat.@watchcat[0].pinghosts='1.1.1.1 10.0.0.1'
uci set watchcat.@watchcat[0].pingperiod='5m'
uci set watchcat.@watchcat[0].period='10m'
uci set watchcat.@watchcat[0].forcedelay='30'
uci set watchcat.@watchcat[0].mode='ping_reboot'
uci commit watchcat

# --- restart services ---
/etc/init.d/system reload || true
/etc/init.d/log restart
/etc/init.d/prometheus-node-exporter-lua enable
/etc/init.d/prometheus-node-exporter-lua restart
/etc/init.d/watchcat enable
/etc/init.d/watchcat restart
/etc/init.d/tailscale enable
/etc/init.d/tailscale start || true

# --- tailscale up (interactive auth URL if not already authed) ---
# If a TAILSCALE_AUTHKEY env var is set, use it for unattended join.
if [ -n "${TAILSCALE_AUTHKEY:-}" ]; then
  tailscale up --authkey="$TAILSCALE_AUTHKEY" --hostname="$NODE_NAME" --accept-routes --reset
else
  echo ""
  echo ">>> run this next, then follow the printed URL in a browser:"
  echo "    tailscale up --hostname='$NODE_NAME' --accept-routes"
fi

echo ""
echo "=== Layer 0 applied to $NODE_NAME ==="
echo "  metrics:    http://$(uci get network.lan.ipaddr 2>/dev/null):9100/metrics"
echo "  syslog ->:  $SYSLOG_SINK:$SYSLOG_PORT udp"
echo "  watchcat:   ping 1.1.1.1 + 10.0.0.1 every 5m, reboot after 10m down"
echo ""
echo "Verify from kokonoe:"
echo "  curl http://<tailnet-ip>:9100/metrics | head"
echo "  ssh cnc-server 'sudo tail /var/log/fleet/$NODE_NAME/*.log'"
