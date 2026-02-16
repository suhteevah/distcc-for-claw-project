#!/bin/bash
# =============================================================================
# Dr Paper Fleet Health Check
# Deploy on: dr-paper (Swoop's Linux orchestrator)
# Cron: */5 * * * * /usr/local/bin/fleet-health-check.sh
# =============================================================================

set -uo pipefail

AGENTS=(
  "localhost:3284|dr-paper-local"
  "swoop-macbook1:3284|swoop-macbook1"
  "swoop-imac:3284|swoop-imac"
  "swoop-rpi1:3284|swoop-rpi1"
  "swoop-rpi2:3284|swoop-rpi2"
  "swoop-rpi3:3284|swoop-rpi3"
)

HOSTS=("swoop-macbook1" "swoop-macbook2" "swoop-imac" "swoop-rpi1" "swoop-rpi2" "swoop-rpi3" "swoop-windows-desktop" "swoop-windows-laptop")

LOGFILE="/var/log/fleet-health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Dr Paper Health Check: ${TIMESTAMP} ===" | tee -a "$LOGFILE"

echo "--- Claude Code Agents ---" | tee -a "$LOGFILE"
UP=0; DOWN=0
for entry in "${AGENTS[@]}"; do
  IFS='|' read -r endpoint name <<< "$entry"
  status=$(curl -s --connect-timeout 3 "http://${endpoint}/status" 2>/dev/null)
  if [ $? -eq 0 ] && [ -n "$status" ]; then
    echo "[OK]   ${name}: ${status}" | tee -a "$LOGFILE"
    ((UP++))
  else
    echo "[DOWN] ${name}: unreachable" | tee -a "$LOGFILE"
    ((DOWN++))
  fi
done
echo "Agents: ${UP} up, ${DOWN} down" | tee -a "$LOGFILE"

echo "--- Icecream ---" | tee -a "$LOGFILE"
systemctl is-active --quiet icecc-scheduler 2>/dev/null \
  && echo "[OK]   icecc-scheduler" | tee -a "$LOGFILE" \
  || echo "[DOWN] icecc-scheduler" | tee -a "$LOGFILE"

echo "--- Tailscale ---" | tee -a "$LOGFILE"
for host in "${HOSTS[@]}"; do
  tailscale ping --timeout 3s "$host" &>/dev/null \
    && echo "[OK]   ${host}" | tee -a "$LOGFILE" \
    || echo "[DOWN] ${host}" | tee -a "$LOGFILE"
done

echo "--- Orchestrator ---" | tee -a "$LOGFILE"
systemctl is-active --quiet claude-orchestrator 2>/dev/null \
  && echo "[OK]   dr-paper orchestrator" | tee -a "$LOGFILE" \
  || echo "[DOWN] dr-paper orchestrator" | tee -a "$LOGFILE"

echo "" | tee -a "$LOGFILE"
