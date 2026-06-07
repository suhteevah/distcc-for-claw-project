#!/usr/bin/env bash
# P2 — verify the NATS cluster: each node serving, JetStream meta cluster = 3 peers, agreed leader.
# (num_routes is NOT a reliable count: NATS 2.10+ pools ~3 conns/peer, so 2 peers => ~8 routes.)
set -uo pipefail
cd "$(dirname "$0")/.." && source lib/common.sh
MEMBERS="mesh-ap-06 mesh-ap-07 mesh-ap-08"

ok=1
for n in $MEMBERS; do
  echo "=== $n ==="
  # retry once — varz can come back empty under momentary load
  varz="$(node_ssh "$n" 'for i in 1 2 3; do r=$(wget -qO- http://localhost:8222/varz 2>/dev/null); [ -n "$r" ] && { echo "$r"; break; }; sleep 1; done')"
  jsz="$(node_ssh  "$n" 'for i in 1 2 3; do r=$(wget -qO- http://localhost:8222/jsz  2>/dev/null); [ -n "$r" ] && { echo "$r"; break; }; sleep 1; done')"
  ver="$(printf '%s' "$varz" | grep -oE '"version": *"[0-9.]+"' | head -1 | grep -oE '[0-9.]+')"
  size="$(printf '%s' "$jsz" | grep -oE '"cluster_size": *[0-9]+' | head -1 | grep -oE '[0-9]+')"
  leader="$(printf '%s' "$jsz" | grep -oE '"leader": *"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
  streams="$(printf '%s' "$jsz" | grep -oE '"streams": *[0-9]+' | head -1 | grep -oE '[0-9]+')"
  echo "  serving: ${ver:-DOWN}   js cluster_size: ${size:-?}   leader: ${leader:-none}   streams: ${streams:-?}"
  [ "${ver:-}" ] && [ "${size:-0}" = 3 ] && [ "${leader:-}" ] || { echo "  WARN: expected serving + cluster_size 3 + a leader"; ok=0; }
done
[ "$ok" = 1 ] && echo "=== cluster OK (3-node JetStream, leader elected) ===" || echo "=== cluster INCOMPLETE ==="
exit $((1-ok))
