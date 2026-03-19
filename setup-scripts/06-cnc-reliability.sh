#!/bin/bash
# =============================================================================
# CNC-Server Reliability Bundle
# Prevents unattended downtime on openSUSE Leap Micro 6.2
#
# Deploys:
#   1. Disable rebootmgr (no more surprise reboots after transactional-update)
#   2. Healthcheck ping timer (external uptime monitoring)
#   3. Hardware watchdog (auto-reboot on kernel panic/hang)
#   4. Fleet ping monitor (alerts Discord #briefing if services are down)
#   5. Safe update script (manual updates with pre-checks)
# =============================================================================

set -euo pipefail

HEALTHCHECK_URL="${HEALTHCHECK_URL:-}"  # Set to your healthchecks.io or UptimeRobot ping URL
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"  # Discord webhook for #briefing channel
OPENCLAW_SERVICES="openclaw-seo-auditor openclaw-lead-responder openclaw-content-mill openclaw-proposal-gen openclaw-job-hunter openclaw-client-dashboard openclaw-wow-economy openclaw-legal-team openclaw-coder"

info()  { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
fail()  { echo -e "\033[1;31m[FAIL]\033[0m  $*"; exit 1; }
ok()    { echo -e "\033[1;32m[ OK ]\033[0m  $*"; }

[[ $(id -u) -eq 0 ]] || fail "Run as root"

# =============================================================================
# 1. Disable rebootmgr — no more unattended reboots
# =============================================================================
info "Disabling rebootmgr (automatic reboot after updates)..."
if systemctl is-active --quiet rebootmgr 2>/dev/null; then
    systemctl disable --now rebootmgr
    ok "rebootmgr disabled"
else
    ok "rebootmgr already inactive"
fi

# Also prevent transactional-update from triggering reboots via its own config
if [[ -f /etc/transactional-update.conf ]]; then
    sed -i 's/^REBOOT_METHOD=.*/REBOOT_METHOD=none/' /etc/transactional-update.conf
    ok "transactional-update REBOOT_METHOD set to none"
elif [[ -d /etc ]]; then
    echo 'REBOOT_METHOD=none' > /etc/transactional-update.conf
    ok "Created /etc/transactional-update.conf with REBOOT_METHOD=none"
fi

# =============================================================================
# 2. Healthcheck ping timer — pings external URL every 5 minutes
# =============================================================================
info "Installing healthcheck ping timer..."

cat > /etc/systemd/system/healthcheck-ping.service <<'EOF'
[Unit]
Description=Healthcheck ping to external monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/healthcheck-ping.sh
TimeoutStartSec=30
EOF

cat > /etc/systemd/system/healthcheck-ping.timer <<'EOF'
[Unit]
Description=Healthcheck ping every 5 minutes

[Timer]
OnBootSec=60
OnUnitActiveSec=5min
AccuracySec=30s

[Install]
WantedBy=timers.target
EOF

cat > /usr/local/bin/healthcheck-ping.sh <<'PING_EOF'
#!/bin/bash
# Ping external healthcheck URL + include basic system info
HEALTHCHECK_URL_FILE="/etc/healthcheck-url"

if [[ ! -f "$HEALTHCHECK_URL_FILE" ]]; then
    exit 0  # No URL configured, silently skip
fi

URL=$(cat "$HEALTHCHECK_URL_FILE")
[[ -z "$URL" ]] && exit 0

# Build a quick status payload
LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
MEM=$(free -m | awk '/Mem:/{printf "%d/%dMB", $3, $2}')
UPTIME=$(uptime -p)
CONTAINERS=$(podman ps --format '{{.Names}}' 2>/dev/null | wc -l)
SERVICES=$(systemctl list-units 'openclaw-*' --state=running --no-legend 2>/dev/null | wc -l)

curl -fsS -m 10 "$URL" \
    --data-raw "load=$LOAD mem=$MEM uptime=$UPTIME containers=$CONTAINERS agents=$SERVICES" \
    >/dev/null 2>&1 || true
PING_EOF

chmod +x /usr/local/bin/healthcheck-ping.sh

# Write URL if provided
if [[ -n "$HEALTHCHECK_URL" ]]; then
    echo "$HEALTHCHECK_URL" > /etc/healthcheck-url
    ok "Healthcheck URL configured"
else
    warn "No HEALTHCHECK_URL set — create /etc/healthcheck-url later"
fi

systemctl daemon-reload
systemctl enable --now healthcheck-ping.timer
ok "Healthcheck ping timer installed (every 5 min)"

# =============================================================================
# 3. Hardware watchdog — auto-reboot on kernel panic/hang
# =============================================================================
info "Configuring hardware watchdog..."

# Ensure kernel panic triggers reboot after 10 seconds
current_panic=$(sysctl -n kernel.panic 2>/dev/null || echo 0)
if [[ "$current_panic" -eq 0 ]]; then
    echo "kernel.panic = 10" > /etc/sysctl.d/90-watchdog.conf
    echo "kernel.panic_on_oops = 1" >> /etc/sysctl.d/90-watchdog.conf
    sysctl -p /etc/sysctl.d/90-watchdog.conf
    ok "Kernel panic auto-reboot configured (10s delay)"
else
    ok "Kernel panic reboot already set to ${current_panic}s"
fi

# Enable systemd's built-in watchdog support
if [[ -f /etc/systemd/system.conf ]]; then
    # Set RuntimeWatchdogSec if not already set
    if ! grep -q '^RuntimeWatchdogSec=' /etc/systemd/system.conf; then
        sed -i 's/^#RuntimeWatchdogSec=.*/RuntimeWatchdogSec=30/' /etc/systemd/system.conf
        ok "systemd hardware watchdog enabled (30s)"
    else
        ok "systemd watchdog already configured"
    fi
fi

# =============================================================================
# 4. Fleet self-monitor — checks local services + alerts Discord
# =============================================================================
info "Installing fleet self-monitor..."

cat > /etc/systemd/system/fleet-monitor.service <<'EOF'
[Unit]
Description=OpenClaw fleet self-monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/fleet-monitor.sh
TimeoutStartSec=60
EOF

cat > /etc/systemd/system/fleet-monitor.timer <<'EOF'
[Unit]
Description=Fleet monitor every 10 minutes

[Timer]
OnBootSec=120
OnUnitActiveSec=10min
AccuracySec=60s

[Install]
WantedBy=timers.target
EOF

cat > /usr/local/bin/fleet-monitor.sh <<'MONITOR_EOF'
#!/bin/bash
# Check OpenClaw services and containers, alert Discord on failures
WEBHOOK_FILE="/etc/discord-webhook-url"
STATE_DIR="/var/lib/fleet-monitor"
mkdir -p "$STATE_DIR"

# Load webhook
WEBHOOK=""
[[ -f "$WEBHOOK_FILE" ]] && WEBHOOK=$(cat "$WEBHOOK_FILE")

failures=()
recoveries=()

# Check Rust agent services
for svc in openclaw-seo-auditor openclaw-lead-responder openclaw-content-mill \
           openclaw-proposal-gen openclaw-job-hunter openclaw-client-dashboard \
           openclaw-wow-economy openclaw-legal-team openclaw-coder; do
    state_file="$STATE_DIR/$svc"
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        # Service is up — check if it was previously down (recovery)
        if [[ -f "$state_file" ]]; then
            recoveries+=("$svc")
            rm -f "$state_file"
        fi
    else
        # Service is down
        if [[ ! -f "$state_file" ]]; then
            failures+=("$svc")
            date > "$state_file"
        fi
    fi
done

# Check key containers
for ctr in openclaw-gateway redis postgres; do
    state_file="$STATE_DIR/ctr-$ctr"
    if podman ps --format '{{.Names}}' 2>/dev/null | grep -q "^${ctr}$"; then
        if [[ -f "$state_file" ]]; then
            recoveries+=("container:$ctr")
            rm -f "$state_file"
        fi
    else
        if [[ ! -f "$state_file" ]]; then
            failures+=("container:$ctr")
            date > "$state_file"
        fi
    fi
done

# Send Discord alert if there are new failures or recoveries
if [[ -n "$WEBHOOK" && ( ${#failures[@]} -gt 0 || ${#recoveries[@]} -gt 0 ) ]]; then
    HOSTNAME=$(hostname)
    MSG=""
    if [[ ${#failures[@]} -gt 0 ]]; then
        FAIL_LIST=$(printf '`%s`\\n' "${failures[@]}")
        MSG="**:red_circle: CNC-Server Alert**\\nServices DOWN:\\n${FAIL_LIST}"
    fi
    if [[ ${#recoveries[@]} -gt 0 ]]; then
        REC_LIST=$(printf '`%s`\\n' "${recoveries[@]}")
        MSG="${MSG}\\n**:green_circle: Recovered:**\\n${REC_LIST}"
    fi

    curl -fsS -m 10 "$WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{\"content\": \"${MSG}\"}" \
        >/dev/null 2>&1 || true
fi

# Also attempt auto-restart for any failed services (one attempt)
for svc in "${failures[@]}"; do
    if [[ "$svc" != container:* ]]; then
        systemctl restart "$svc" 2>/dev/null || true
    fi
done
MONITOR_EOF

chmod +x /usr/local/bin/fleet-monitor.sh

if [[ -n "$DISCORD_WEBHOOK" ]]; then
    echo "$DISCORD_WEBHOOK" > /etc/discord-webhook-url
    chmod 600 /etc/discord-webhook-url
    ok "Discord webhook configured"
else
    warn "No DISCORD_WEBHOOK set — create /etc/discord-webhook-url later"
fi

systemctl daemon-reload
systemctl enable --now fleet-monitor.timer
ok "Fleet self-monitor installed (every 10 min)"

# =============================================================================
# 5. Safe manual update script
# =============================================================================
info "Installing safe-update script..."

cat > /usr/local/bin/safe-update <<'UPDATE_EOF'
#!/bin/bash
# Safe manual update for CNC-Server
# Runs transactional-update but does NOT reboot automatically.
# Checks NVIDIA DKMS and critical modules before suggesting reboot.
set -euo pipefail

echo "=== CNC-Server Safe Update ==="
echo ""

# Step 1: Run transactional-update
echo "[1/4] Running transactional-update..."
transactional-update --non-interactive up

# Step 2: Check if a new snapshot was created
CURRENT=$(snapper list --columns number,active | grep 'yes' | awk '{print $1}')
LATEST=$(snapper list --columns number | tail -1 | tr -d ' ')
echo "[2/4] Current snapshot: $CURRENT, Latest: $LATEST"

if [[ "$CURRENT" == "$LATEST" ]]; then
    echo "No new snapshot created — system is up to date."
    exit 0
fi

# Step 3: Verify NVIDIA DKMS in new snapshot
echo "[3/4] Checking NVIDIA DKMS status in new snapshot..."
NEW_KERNEL=$(ls /boot/vmlinuz-* 2>/dev/null | sort -V | tail -1 | sed 's/.*vmlinuz-//')
if [[ -n "$NEW_KERNEL" ]]; then
    NVIDIA_KO=$(find "/.snapshots/${LATEST}/snapshot/lib/modules/${NEW_KERNEL}/" -name 'nvidia*.ko*' 2>/dev/null | head -1)
    if [[ -z "$NVIDIA_KO" ]]; then
        echo "WARNING: NVIDIA kernel module NOT found for kernel $NEW_KERNEL in new snapshot!"
        echo "The DKMS rebuild may have failed. Reboot at your own risk."
        echo "To rollback: snapper rollback $CURRENT"
        exit 1
    else
        echo "NVIDIA module found: $NVIDIA_KO"
    fi
fi

# Step 4: Summary
echo "[4/4] Update ready in snapshot $LATEST."
echo ""
echo "To apply: reboot"
echo "To rollback: snapper rollback $CURRENT"
echo ""
echo "Recommended: reboot during a maintenance window."
UPDATE_EOF

chmod +x /usr/local/bin/safe-update
ok "safe-update script installed at /usr/local/bin/safe-update"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "============================================="
echo "  Reliability bundle installed!"
echo "============================================="
echo ""
echo "  [x] rebootmgr disabled"
echo "  [x] transactional-update REBOOT_METHOD=none"
echo "  [x] Healthcheck ping timer (5 min)"
echo "  [x] Kernel panic auto-reboot (10s)"
echo "  [x] systemd hardware watchdog (30s)"
echo "  [x] Fleet self-monitor + Discord alerts (10 min)"
echo "  [x] safe-update script for manual updates"
echo ""
echo "Remaining setup:"
echo "  1. Set healthcheck URL:  echo 'https://hc-ping.com/YOUR-UUID' > /etc/healthcheck-url"
echo "  2. Set Discord webhook:  echo 'https://discord.com/api/webhooks/...' > /etc/discord-webhook-url"
echo "  3. Test: systemctl start healthcheck-ping && systemctl start fleet-monitor"
echo ""
