#!/bin/bash
# =============================================================================
# CNC Server Status Check
# Run from any machine on the Tailscale network to check CNC server health
# Usage: ./check-cnc-server.sh [hostname]
# =============================================================================

set -uo pipefail

CNC_HOST="${1:-cnc-server}"
TIMEOUT=5

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
down() { echo -e "${RED}[DOWN]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

PASS=0
FAIL=0

echo "============================================"
echo "  CNC Server Status: ${CNC_HOST}"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo ""

# 1. Tailscale connectivity
echo "--- Network ---"
if command -v tailscale &>/dev/null; then
  if tailscale ping --timeout "${TIMEOUT}s" "$CNC_HOST" &>/dev/null; then
    ok "Tailscale: ${CNC_HOST} reachable"
    ((PASS++))
  else
    down "Tailscale: ${CNC_HOST} unreachable"
    ((FAIL++))
  fi
else
  warn "Tailscale CLI not found, falling back to ping"
  if ping -c 1 -W "$TIMEOUT" "$CNC_HOST" &>/dev/null; then
    ok "Ping: ${CNC_HOST} reachable"
    ((PASS++))
  else
    down "Ping: ${CNC_HOST} unreachable"
    ((FAIL++))
    echo ""
    echo "Cannot reach ${CNC_HOST}. Remaining checks skipped."
    exit 1
  fi
fi
echo ""

# 2. SSH connectivity
echo "--- SSH ---"
if ssh -o ConnectTimeout="$TIMEOUT" -o BatchMode=yes "$CNC_HOST" "echo ok" &>/dev/null; then
  ok "SSH: connected"
  ((PASS++))
else
  warn "SSH: cannot connect (key auth may not be configured)"
fi
echo ""

# 3. AgentAPI (port 3284)
echo "--- Claude Code AgentAPI ---"
agent_status=$(curl -s --connect-timeout "$TIMEOUT" "http://${CNC_HOST}:3284/status" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$agent_status" ]; then
  ok "AgentAPI (port 3284): ${agent_status}"
  ((PASS++))
else
  down "AgentAPI (port 3284): unreachable"
  ((FAIL++))
fi
echo ""

# 4. Orchestrator Web UI (port 8080)
echo "--- Orchestrator ---"
orch_status=$(curl -s --connect-timeout "$TIMEOUT" -o /dev/null -w "%{http_code}" "http://${CNC_HOST}:8080" 2>/dev/null)
if [ "$orch_status" -ge 200 ] && [ "$orch_status" -lt 400 ] 2>/dev/null; then
  ok "Orchestrator UI (port 8080): HTTP ${orch_status}"
  ((PASS++))
else
  down "Orchestrator UI (port 8080): HTTP ${orch_status:-timeout}"
  ((FAIL++))
fi
echo ""

# 5. Icecream Scheduler (port 8765)
echo "--- Icecream (Distributed Compilation) ---"
if nc -z -w "$TIMEOUT" "$CNC_HOST" 8765 &>/dev/null; then
  ok "Icecream Scheduler (port 8765): listening"
  ((PASS++))
else
  down "Icecream Scheduler (port 8765): not listening"
  ((FAIL++))
fi

if nc -z -w "$TIMEOUT" "$CNC_HOST" 10245 &>/dev/null; then
  ok "Icecream Worker (port 10245): listening"
  ((PASS++))
else
  down "Icecream Worker (port 10245): not listening"
  ((FAIL++))
fi
echo ""

# 6. Ollama (port 11434)
echo "--- Ollama (LLM Inference) ---"
ollama_resp=$(curl -s --connect-timeout "$TIMEOUT" "http://${CNC_HOST}:11434/api/tags" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$ollama_resp" ]; then
  model_count=$(echo "$ollama_resp" | grep -o '"name"' | wc -l)
  ok "Ollama (port 11434): running, ${model_count} model(s) loaded"
  ((PASS++))
else
  down "Ollama (port 11434): unreachable"
  ((FAIL++))
fi
echo ""

# 7. OpenClaw Gateway (port 18789)
echo "--- OpenClaw Gateway ---"
claw_status=$(curl -s --connect-timeout "$TIMEOUT" -o /dev/null -w "%{http_code}" "http://${CNC_HOST}:18789" 2>/dev/null)
if [ "$claw_status" -ge 200 ] && [ "$claw_status" -lt 400 ] 2>/dev/null; then
  ok "OpenClaw Gateway (port 18789): HTTP ${claw_status}"
  ((PASS++))
else
  down "OpenClaw Gateway (port 18789): HTTP ${claw_status:-timeout}"
  ((FAIL++))
fi
echo ""

# 8. Remote systemd service status (if SSH works)
echo "--- Systemd Services (via SSH) ---"
SERVICES=("claude-agentapi" "claude-orchestrator" "icecc-scheduler" "iceccd" "ollama" "tailscaled")
ssh_ok=false
if ssh -o ConnectTimeout="$TIMEOUT" -o BatchMode=yes "$CNC_HOST" "echo ok" &>/dev/null; then
  ssh_ok=true
  for svc in "${SERVICES[@]}"; do
    svc_state=$(ssh -o ConnectTimeout="$TIMEOUT" -o BatchMode=yes "$CNC_HOST" "systemctl is-active $svc 2>/dev/null" 2>/dev/null)
    if [ "$svc_state" = "active" ]; then
      ok "${svc}: active"
      ((PASS++))
    else
      down "${svc}: ${svc_state:-unknown}"
      ((FAIL++))
    fi
  done
else
  warn "SSH not available — skipping systemd checks"
fi
echo ""

# Summary
echo "============================================"
TOTAL=$((PASS + FAIL))
if [ "$FAIL" -eq 0 ]; then
  echo -e "  ${GREEN}All ${TOTAL} checks passed${NC}"
else
  echo -e "  ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC} (${TOTAL} total)"
fi
echo "============================================"

exit "$FAIL"
