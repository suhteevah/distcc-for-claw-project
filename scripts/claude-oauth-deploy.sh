#!/usr/bin/env bash
# claude-oauth-deploy.sh — ship local Claude Max OAuth credentials to a fleet node
#
# Prerequisite: this workstation has a working `claude` login
# (~/.claude/.credentials.json exists). Get there with:
#   claude   # complete the browser login flow, then quit
#
# Usage:
#   ./claude-oauth-deploy.sh <node-hostname> [target-user]
#
# Example:
#   ./claude-oauth-deploy.sh cnc-server
#   ./claude-oauth-deploy.sh swoop-rpi1 claude-agent
#
# What it does:
#   1. Verifies a local .credentials.json exists
#   2. SCPs it to the node via Tailscale
#   3. Installs it under /home/claude-agent/.claude/.credentials.json (mode 600, owned by claude-agent)
#   4. Restarts claude-agentapi + claude-orchestrator services so they pick up the new auth

set -euo pipefail

NODE="${1:-}"
REMOTE_USER="${2:-root}"

if [ -z "$NODE" ]; then
    echo "Usage: $0 <node-hostname> [target-user]" >&2
    exit 1
fi

LOCAL_CREDS="${CLAUDE_CREDENTIALS_FILE:-$HOME/.claude/.credentials.json}"
if [ ! -f "$LOCAL_CREDS" ]; then
    echo "FATAL: No local credentials at $LOCAL_CREDS" >&2
    echo "Run \`claude\` and complete the login flow first." >&2
    exit 1
fi

echo "[INFO] Source: $LOCAL_CREDS"
echo "[INFO] Target: $REMOTE_USER@$NODE:/home/claude-agent/.claude/.credentials.json"
echo

# Ship to a staging path the remote user can read, then move into place as root
STAGING="/tmp/.credentials.json.$$"
scp -q "$LOCAL_CREDS" "${REMOTE_USER}@${NODE}:${STAGING}"

ssh "${REMOTE_USER}@${NODE}" bash -s -- "$STAGING" <<'REMOTE'
set -euo pipefail
STAGING="$1"
TARGET="/home/claude-agent/.claude/.credentials.json"

if ! id claude-agent >/dev/null 2>&1; then
    echo "FATAL: user 'claude-agent' does not exist on this node — bootstrap not run yet?" >&2
    rm -f "$STAGING"
    exit 1
fi

install -d -o claude-agent -g claude-agent -m 700 /home/claude-agent/.claude
install -o claude-agent -g claude-agent -m 600 "$STAGING" "$TARGET"
rm -f "$STAGING"

# Empty out api-key file so EnvironmentFile load doesn't override OAuth
if [ -f /etc/claude/api-key ]; then
    : > /etc/claude/api-key
    chmod 600 /etc/claude/api-key
    chown claude-agent:claude-agent /etc/claude/api-key
fi

# Restart services if present
for svc in claude-agentapi claude-orchestrator; do
    if systemctl list-unit-files | grep -q "^${svc}.service"; then
        systemctl restart "${svc}.service" || echo "WARN: ${svc} restart failed (check journalctl -u ${svc})"
    fi
done

echo "[OK] OAuth credentials deployed and services restarted"
REMOTE

echo
echo "[OK] Done. Verify with:"
echo "  ssh ${REMOTE_USER}@${NODE} 'sudo -u claude-agent claude --version'"
echo "  ssh ${REMOTE_USER}@${NODE} 'systemctl status claude-agentapi'"
