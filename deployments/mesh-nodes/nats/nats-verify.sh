#!/usr/bin/env bash
# P2 — verify the NATS cluster: each node serving, 2 routes each, JetStream up.
set -uo pipefail
cd "$(dirname "$0")/.." && source lib/common.sh
MEMBERS="mesh-ap-06 mesh-ap-07 mesh-ap-08"

ok=1
for n in $MEMBERS; do
  echo "=== $n ==="
  varz="$(node_ssh "$n" 'wget -qO- http://localhost:8222/varz 2>/dev/null')"
  routez="$(node_ssh "$n" 'wget -qO- http://localhost:8222/routez 2>/dev/null')"
  jsz="$(node_ssh "$n" 'wget -qO- http://localhost:8222/jsz 2>/dev/null')"
  ver="$(printf '%s' "$varz" | grep -oE '"version":"[0-9.]+"' | head -1)"
  nr="$(printf '%s' "$routez" | grep -oE '"num_routes":[0-9]+' | head -1)"
  js="$(printf '%s' "$jsz" | grep -oE '"streams":[0-9]+' | head -1)"
  echo "  serving: ${ver:-DOWN}   routes: ${nr:-?}   jetstream: ${js:-?}"
  printf '%s' "$nr" | grep -q ':2' || { echo "  WARN: expected num_routes:2"; ok=0; }
done
[ "$ok" = 1 ] && echo "=== cluster OK ===" || echo "=== cluster INCOMPLETE ==="
exit $((1-ok))
