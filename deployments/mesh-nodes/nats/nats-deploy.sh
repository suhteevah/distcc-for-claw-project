#!/usr/bin/env bash
# P2 — deploy the 3-node NATS+JetStream cluster (mesh-ap-06/07/08).
# Run from kokonoe (git-bash). Tokens are env-only; never commit them.
#   export NATS_TOKEN=...  NATS_CLUSTER_TOKEN=...   (or source nats/.tokens.env)
#   bash nats/nats-deploy.sh
set -uo pipefail
cd "$(dirname "$0")/.." && source lib/common.sh

# allow a gitignored token file
[ -f nats/.tokens.env ] && . nats/.tokens.env
: "${NATS_TOKEN:?export NATS_TOKEN (client token)}"
: "${NATS_CLUSTER_TOKEN:?export NATS_CLUSTER_TOKEN (cluster route token)}"

# cluster members -> reserved LAN IP (cluster + JS traffic stays on the LAN, not tailnet)
declare -A LAN=( [mesh-ap-06]=192.168.168.144 [mesh-ap-07]=192.168.168.145 [mesh-ap-08]=192.168.168.146 )
MEMBERS="mesh-ap-06 mesh-ap-07 mesh-ap-08"

rc=0
for node in $MEMBERS; do
  echo "=== $node (${LAN[$node]}) ==="
  # full-mesh routes to the OTHER two peers, by LAN IP
  routes=""
  for peer in $MEMBERS; do
    [ "$peer" = "$node" ] && continue
    routes="${routes}nats-route://${NATS_CLUSTER_TOKEN}@${LAN[$peer]}:6222, "
  done
  routes="${routes%, }"

  conf="$(sed \
    -e "s/__NODE__/$node/g" \
    -e "s/__TOKEN__/$NATS_TOKEN/g" \
    -e "s/__CLUSTER_TOKEN__/$NATS_CLUSTER_TOKEN/g" \
    -e "s#__ROUTES__#$routes#g" \
    nats/nats.conf.tmpl)"

  push_file "$node" nats/assets/nats-server /usr/sbin/nats-server
  node_ssh "$node" 'chmod +x /usr/sbin/nats-server; mkdir -p /etc/nats /overlay/nats-js'
  printf '%s\n' "$conf" | node_ssh "$node" 'cat > /etc/nats/nats.conf; chmod 600 /etc/nats/nats.conf'
  push_file "$node" nats/nats.init /etc/init.d/nats
  node_ssh "$node" '/etc/init.d/nats enable; /etc/init.d/nats restart; sleep 2;
    if pgrep -x nats-server >/dev/null; then echo "  '"$node"': nats up (pid $(pgrep -x nats-server))"; else echo "  '"$node"': NATS DOWN"; logread | grep -i nats | tail -5; fi'
  [ $? -eq 0 ] || rc=1
done
echo "=== deploy done (rc=$rc) ==="
exit $rc
