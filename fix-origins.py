#!/usr/bin/env python3
"""Fix origin/CORS restrictions on orchestrator and AgentAPI to allow Tailscale access."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.25", username="root", password="cnc-server-2024!", timeout=10)

def run(cmd, timeout=60, label=None):
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        if label:
            for line in result.strip().split('\n')[:80]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Check current error and config
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== AgentAPI recent logs (origin errors) ==="
journalctl -u claude-agentapi --no-pager -n 20 2>&1 | grep -i "origin\|allow\|reject\|forbid\|cors" || echo "(no origin errors in last 20 lines)"
echo ""

echo "=== Orchestrator recent logs ==="
journalctl -u claude-orchestrator --no-pager -n 20 2>&1 | grep -i "origin\|allow\|reject\|forbid\|cors" || echo "(no origin errors in last 20 lines)"
echo ""

echo "=== Current AgentAPI service ==="
cat /etc/systemd/system/claude-agentapi.service
echo ""

echo "=== Current Orchestrator service ==="
cat /etc/systemd/system/claude-orchestrator.service
""", label="1. Current config & errors")

# ═══════════════════════════════════════════════════════════════════════
# 2. Check AgentAPI flags for allowed hosts/origins
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== AgentAPI help (host/origin flags) ==="
agentapi server --help 2>&1 | grep -iE "host|origin|allow|cors" || echo "(no matching flags)"
echo ""
agentapi server --help 2>&1
""", label="2. AgentAPI available flags")

# ═══════════════════════════════════════════════════════════════════════
# 3. Check orchestrator CORS config in source
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Orchestrator CORS in source ==="
grep -rn -i "cors\|origin\|allowed.*host\|ALLOWED" /opt/claude-code-by-agents/backend/ --include="*.ts" --include="*.json" 2>&1 | head -30
echo ""

echo "=== Orchestrator env vars ==="
grep -rn "ALLOWED\|CORS\|ORIGIN\|HOST" /opt/claude-code-by-agents/backend/ --include="*.ts" 2>&1 | head -20
echo ""

echo "=== deno.json ==="
cat /opt/claude-code-by-agents/backend/deno.json
""", label="3. Orchestrator CORS source")

client.close()
print("\nDone!")
