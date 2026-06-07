#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"; source lib/common.sh
node="${1:?usage: deploy.sh <node>}"
role="$(node_role "$node")"; ip="$(node_ip "$node")"
[ -n "$role" ] && [ "$role" != spare ] || { echo "refusing: $node role='$role'"; exit 2; }
: "${FLEET_PSK:?export FLEET_PSK before running (the Home_EXT key)}"
CNC_LOG_IP="${CNC_LOG_IP:-192.168.168.100}"

echo "=== deploy $node (role=$role, ip=$ip) ==="

# 1) install Layer-0 packages (apk; idempotent)
echo "--- apk install ---"
pkgs="$(grep -vE '^\s*#|^\s*$' packages.list | tr '\n' ' ')"
node_ssh "$node" "apk update >/dev/null 2>&1; apk add $pkgs 2>&1 | tail -1; modprobe tun 2>/dev/null; echo apk-done"

# 2) arm dead-man ON the node (revert /etc/config + reboot in 300s unless /tmp/deploy_ok)
echo "--- arm dead-man (300s) ---"
node_ssh "$node" '
  cp -r /etc/config /etc/config.bak.deploy 2>/dev/null
  rm -f /tmp/deploy_ok
  setsid sh -c "sleep 300; [ -f /tmp/deploy_ok ] && exit 0; cp -r /etc/config.bak.deploy/* /etc/config/; logger -t meshdeploy auto-revert; reboot" >/dev/null 2>&1 &
  echo armed'

# 3) push + run baseline then role overlay
push_file "$node" baseline.sh /tmp/baseline.sh
push_file "$node" "roles/$role.sh" /tmp/role.sh
# relay nodes need watchcat staged from repo assets (apk fetch for watchcat is unreliable here)
if [ "$role" = relay ]; then
  push_file "$node" assets/watchcat/watchcat.init   /etc/init.d/watchcat
  push_file "$node" assets/watchcat/watchcat.sh     /usr/bin/watchcat.sh
  push_file "$node" assets/watchcat/watchcat.config /etc/config/watchcat
  node_ssh "$node" 'chmod +x /etc/init.d/watchcat /usr/bin/watchcat.sh; echo watchcat-staged'
fi
echo "--- run baseline + $role ---"
node_ssh "$node" "CNC_LOG_IP='$CNC_LOG_IP' sh /tmp/baseline.sh && FLEET_PSK='$FLEET_PSK' sh /tmp/role.sh"

# 4) independently re-confirm access (fresh connection) BEFORE disarming
echo "--- reconfirm access ---"
if node_ssh "$node" 'echo REACHABLE; uci get system.@system[0].hostname' | grep -q REACHABLE; then
  node_ssh "$node" 'touch /tmp/deploy_ok; echo "dead-man disarmed"'
else
  echo "!! could not reconfirm $node — leaving dead-man to auto-revert in <300s"; exit 1
fi

# 5) verify
echo "--- verify ---"
bash audit.sh "$node"
