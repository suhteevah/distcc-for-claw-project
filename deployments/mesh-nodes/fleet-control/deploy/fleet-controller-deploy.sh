#!/usr/bin/env bash
# P3 — install/refresh fleet-controller on cnc. Run ON cnc (or via ssh).
# Assumes the release binary is built at /opt/openclaw/fleet-control/target/release/fleet-controller
# and NATS_TOKEN is exported (or passed as $1).
set -euo pipefail
TOKEN="${1:-${NATS_TOKEN:?export NATS_TOKEN or pass as arg}}"
SRC=/opt/openclaw/fleet-control
HERE="$(cd "$(dirname "$0")" && pwd)"

install -m755 "$SRC/target/release/fleet-controller" /usr/local/bin/fleet-controller

# env file (token only here, mode 600)
umask 077
cat > /etc/fleet-controller.env <<EOF
FLEET_NATS=nats://${TOKEN}@192.168.168.144:4222,nats://${TOKEN}@192.168.168.145:4222,nats://${TOKEN}@192.168.168.146:4222
FLEET_HTTP_PORT=9096
FLEET_METRICS_PORT=9094
# MUST stay > the agent heartbeat interval (30s). 180 = 6 missed beats — rides out
# the ~2-min mesh/NATS delivery blips that caused false full-fleet flaps (2026-06-08).
FLEET_DOWN_AFTER_SECS=180
# node down/up alerts -> Telegram via the existing cnc helper (msg passed as argv arg)
FLEET_NOTIFY_CMD=/opt/nightdrive/tools/notify-telegram.sh
# scheduled probes: ping each up node's path to the gateway every 60s
FLEET_PROBE_INTERVAL_SECS=60
FLEET_PROBE_TARGET=192.168.168.168
# daily fleet config backup (git-tracked, local-only) to cnc
FLEET_BACKUP_DIR=/opt/openclaw/fleet-config-backup
FLEET_BACKUP_INTERVAL_SECS=86400
EOF
chmod 600 /etc/fleet-controller.env

install -m644 "$HERE/openclaw-fleet-controller.service" /etc/systemd/system/openclaw-fleet-controller.service
systemctl daemon-reload
systemctl enable --now openclaw-fleet-controller
sleep 3
systemctl is-active openclaw-fleet-controller && echo "fleet-controller active" || { journalctl -u openclaw-fleet-controller -n 20 --no-pager; exit 1; }
