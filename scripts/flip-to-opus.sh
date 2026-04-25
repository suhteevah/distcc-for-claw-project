#!/usr/bin/env bash
# flip-to-opus.sh — full OAuth + Opus rollout to a fleet node, in one shot.
#
# What it does (idempotent):
#   1. Pushes updated systemd service files (claude-agentapi, claude-orchestrator)
#   2. Writes /etc/claude/model-env with ANTHROPIC_MODEL=claude-opus-4-7
#   3. Ships local ~/.claude/.credentials.json → /home/claude-agent/.claude/.credentials.json
#   4. Empties /etc/claude/api-key so OAuth takes over
#   5. systemctl daemon-reload && restarts both services
#   6. Reports status
#
# Prerequisites:
#   - Local box has working `claude` OAuth (~/.claude/.credentials.json present)
#   - Target node has been bootstrapped via cnc-server-bootstrap.sh (claude-agent user exists)
#   - SSH key auth to root@<node>
#
# Usage:
#   ./flip-to-opus.sh <node-hostname> [ssh-user]
#
# Example:
#   ./flip-to-opus.sh cnc-server
#   ./flip-to-opus.sh cnc-server-tailscale root

set -euo pipefail

NODE="${1:-}"
REMOTE_USER="${2:-root}"

if [ -z "$NODE" ]; then
    echo "Usage: $0 <node-hostname> [ssh-user]" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_CREDS="${CLAUDE_CREDENTIALS_FILE:-$HOME/.claude/.credentials.json}"
MODEL="${ANTHROPIC_MODEL:-claude-opus-4-7}"

SERVICE_AGENTAPI="$REPO_ROOT/service-files/systemd/claude-agentapi.service"
SERVICE_ORCH="$REPO_ROOT/service-files/systemd/claude-orchestrator.service"

for f in "$LOCAL_CREDS" "$SERVICE_AGENTAPI" "$SERVICE_ORCH"; do
    if [ ! -f "$f" ]; then
        echo "FATAL: missing required file: $f" >&2
        exit 1
    fi
done

echo "[INFO] Node:    $REMOTE_USER@$NODE"
echo "[INFO] Model:   $MODEL"
echo "[INFO] Creds:   $LOCAL_CREDS"
echo

# 1. Stage everything in /tmp on the remote
STAGE="/tmp/.flip-to-opus.$$"
ssh "${REMOTE_USER}@${NODE}" "mkdir -p ${STAGE}"
scp -q "$SERVICE_AGENTAPI" "${REMOTE_USER}@${NODE}:${STAGE}/claude-agentapi.service"
scp -q "$SERVICE_ORCH"     "${REMOTE_USER}@${NODE}:${STAGE}/claude-orchestrator.service"
scp -q "$LOCAL_CREDS"      "${REMOTE_USER}@${NODE}:${STAGE}/credentials.json"

# 2. Apply on the remote (must be root for systemd + /etc writes)
ssh "${REMOTE_USER}@${NODE}" bash -s -- "$STAGE" "$MODEL" <<'REMOTE'
set -euo pipefail
STAGE="$1"
MODEL="$2"

if ! id claude-agent >/dev/null 2>&1; then
    echo "FATAL: user 'claude-agent' missing — run cnc-server-bootstrap.sh first" >&2
    rm -rf "$STAGE"
    exit 1
fi

# Service files
install -m 644 "$STAGE/claude-agentapi.service"     /etc/systemd/system/claude-agentapi.service
install -m 644 "$STAGE/claude-orchestrator.service" /etc/systemd/system/claude-orchestrator.service
echo "[OK] systemd service files updated"

# Model env
mkdir -p /etc/claude
chmod 700 /etc/claude
echo "ANTHROPIC_MODEL=${MODEL}" > /etc/claude/model-env
chmod 644 /etc/claude/model-env
echo "[OK] model-env: ${MODEL}"

# Empty old api-key file so OAuth wins (keep file for systemd EnvironmentFile)
: > /etc/claude/api-key
chmod 600 /etc/claude/api-key
chown claude-agent:claude-agent /etc/claude/api-key

# OAuth credentials
install -d -o claude-agent -g claude-agent -m 700 /home/claude-agent/.claude
install -o claude-agent -g claude-agent -m 600 \
    "$STAGE/credentials.json" \
    /home/claude-agent/.claude/.credentials.json
echo "[OK] OAuth credentials installed"

# Reload + restart
systemctl daemon-reload
for svc in claude-agentapi claude-orchestrator; do
    if systemctl list-unit-files | grep -q "^${svc}.service"; then
        systemctl restart "${svc}.service" || echo "[WARN] ${svc} restart failed"
        systemctl is-active "${svc}.service" >/dev/null && echo "[OK] ${svc} active" || echo "[WARN] ${svc} not active"
    else
        echo "[INFO] ${svc} not installed on this node, skipping"
    fi
done

# Wipe staging
rm -rf "$STAGE"
REMOTE

echo
echo "[OK] Flip complete on $NODE"
echo
echo "Verify with:"
echo "  ssh ${REMOTE_USER}@${NODE} 'systemctl status claude-agentapi --no-pager'"
echo "  ssh ${REMOTE_USER}@${NODE} 'journalctl -u claude-agentapi -n 30 --no-pager'"
