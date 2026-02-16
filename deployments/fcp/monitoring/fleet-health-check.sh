#!/bin/bash
# =============================================================================
# FCP Fleet Health Check (lightweight)
# Run from any machine with tailscale
# =============================================================================

set -uo pipefail

echo "=== FCP Fleet Status: $(date '+%Y-%m-%d %H:%M:%S') ==="

NODES=("fcp-laptop" "fcp-rpi" "fcp-mac-mini")

echo "--- Network ---"
for node in "${NODES[@]}"; do
  if tailscale ping --timeout 3s "$node" &>/dev/null; then
    echo "[OK]   ${node}: reachable"
  else
    echo "[----] ${node}: not found"
  fi
done

echo "--- Agents ---"
AGENTS=("fcp-rpi:3284" "fcp-mac-mini:3284")
for agent in "${AGENTS[@]}"; do
  status=$(curl -s --connect-timeout 3 "http://${agent}/status" 2>/dev/null)
  if [ $? -eq 0 ] && [ -n "$status" ]; then
    echo "[OK]   ${agent}: ${status}"
  else
    echo "[----] ${agent}: not responding"
  fi
done
