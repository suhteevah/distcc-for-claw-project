#!/usr/bin/env bash
# P3 — deploy mesh-agent to fleet nodes. Run from kokonoe (git-bash).
#   export NATS_TOKEN=...   (or it is read from nats/.tokens.env)
#   bash fleet-control/deploy/mesh-agent-deploy.sh [node ...]   (default: all_nodes)
set -uo pipefail
cd "$(dirname "$0")/../.." && source lib/common.sh   # -> mesh-nodes/
[ -f nats/.tokens.env ] && . nats/.tokens.env
: "${NATS_TOKEN:?export NATS_TOKEN (client token)}"
FC=fleet-control
BIN="$FC/deploy/assets/mesh-agent"
[ -f "$BIN" ] || { echo "ERR: $BIN missing — cross-build it first"; exit 1; }

# node -> the NATS endpoint its agent connects to (cluster nodes use localhost)
nats_url() {
  case "$1" in
    mesh-ap-06|mesh-ap-07|mesh-ap-08) echo "nats://${NATS_TOKEN}@localhost:4222" ;;
    *) echo "nats://${NATS_TOKEN}@192.168.168.144:4222,nats://${NATS_TOKEN}@192.168.168.145:4222,nats://${NATS_TOKEN}@192.168.168.146:4222" ;;
  esac
}

TARGETS="${*:-$(all_nodes)}"
rc=0
for node in $TARGETS; do
  echo "=== $node ==="
  push_file "$node" "$BIN" /usr/sbin/mesh-agent
  printf 'MESH_AGENT_NODE=%s\nMESH_AGENT_NATS=%s\n' "$node" "$(nats_url "$node")" \
    | node_ssh "$node" 'cat > /etc/mesh-agent.env; chmod 600 /etc/mesh-agent.env'
  push_file "$node" "$FC/deploy/mesh-agent.init" /etc/init.d/mesh-agent
  node_ssh "$node" 'chmod +x /usr/sbin/mesh-agent /etc/init.d/mesh-agent; /etc/init.d/mesh-agent enable; /etc/init.d/mesh-agent restart; sleep 2;
    pid=$(pidof mesh-agent);
    if [ -n "$pid" ]; then echo "  '"$node"': mesh-agent up (pid $pid)"; else echo "  '"$node"': DOWN"; logread | grep mesh-agent | tail -5; fi'
  [ $? -eq 0 ] || rc=1
done
echo "=== deploy done (rc=$rc) ==="
exit $rc
