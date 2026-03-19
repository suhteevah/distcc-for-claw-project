#!/bin/bash
# =============================================================================
# Remote Watchdog for CNC-Server
# Run on Satibook, Faye, or any other fleet node via cron/systemd timer
# Pings CNC-Server and alerts Discord if it's unreachable
# =============================================================================

set -euo pipefail

# Config
CNC_IP="${CNC_IP:-192.168.168.100}"          # SonicWall wired IP (preferred)
CNC_TAILSCALE="${CNC_TAILSCALE:-100.108.202.49}"
CNC_API_PORT="9000"                           # Core API port
DISCORD_WEBHOOK_FILE="${DISCORD_WEBHOOK_FILE:-$HOME/.cnc-watchdog-webhook}"
STATE_FILE="${STATE_FILE:-/tmp/cnc-watchdog-state}"
CHECK_NAME="$(hostname)-watchdog"

# Load Discord webhook
WEBHOOK=""
if [[ -f "$DISCORD_WEBHOOK_FILE" ]]; then
    WEBHOOK=$(cat "$DISCORD_WEBHOOK_FILE")
fi

send_discord() {
    local msg="$1"
    if [[ -n "$WEBHOOK" ]]; then
        curl -fsS -m 10 "$WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"$msg\"}" \
            >/dev/null 2>&1 || true
    fi
}

# Try to reach CNC-Server
reachable=false

# Method 1: TCP check on API port via SonicWall IP
if timeout 5 bash -c "echo > /dev/tcp/$CNC_IP/$CNC_API_PORT" 2>/dev/null; then
    reachable=true
# Method 2: Try Tailscale IP
elif timeout 5 bash -c "echo > /dev/tcp/$CNC_TAILSCALE/$CNC_API_PORT" 2>/dev/null; then
    reachable=true
# Method 3: Simple ping
elif ping -c 2 -W 3 "$CNC_IP" >/dev/null 2>&1; then
    reachable=true
elif ping -c 2 -W 3 "$CNC_TAILSCALE" >/dev/null 2>&1; then
    reachable=true
fi

if $reachable; then
    # CNC-Server is up
    if [[ -f "$STATE_FILE" ]]; then
        # It was down before — send recovery
        DOWN_SINCE=$(cat "$STATE_FILE")
        send_discord "**:green_circle: CNC-Server is BACK UP** (was down since $DOWN_SINCE) — reported by \`$CHECK_NAME\`"
        rm -f "$STATE_FILE"
    fi
else
    # CNC-Server is down
    if [[ ! -f "$STATE_FILE" ]]; then
        # First detection — record and alert
        date '+%Y-%m-%d %H:%M' > "$STATE_FILE"
        send_discord "**:red_circle: CNC-Server is UNREACHABLE** — no response on $CNC_IP:$CNC_API_PORT, $CNC_TAILSCALE:$CNC_API_PORT, or ping. Reported by \`$CHECK_NAME\`"
    fi
    # If already recorded, stay quiet (don't spam)
fi
