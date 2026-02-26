#!/usr/bin/env python3
"""Fix AgentAPI + Orchestrator to allow Tailscale/remote origins."""

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
            for line in result.strip().split('\n')[:50]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Update AgentAPI service — add wildcard allowed hosts/origins
# ═══════════════════════════════════════════════════════════════════════
run(r"""
cat > /etc/systemd/system/claude-agentapi.service << 'UNIT'
[Unit]
Description=Claude Code AgentAPI Server
After=network-online.target tailscaled.service ollama.service
Wants=network-online.target

[Service]
Type=simple
User=claude-agent
WorkingDirectory=/home/claude-agent
EnvironmentFile=-/etc/claude/api-key
ExecStart=/usr/local/bin/agentapi server \
  --type claude \
  --allowed-hosts '*' \
  --allowed-origins '*' \
  -- /usr/local/bin/claude \
  --dangerously-skip-permissions \
  --max-budget-usd 10.00
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=claude-agentapi

[Install]
WantedBy=multi-user.target
UNIT

echo "AgentAPI service updated"
""", label="1. Update AgentAPI service")

# ═══════════════════════════════════════════════════════════════════════
# 2. Reload and restart both services
# ═══════════════════════════════════════════════════════════════════════
run("""
systemctl daemon-reload
systemctl restart claude-agentapi
sleep 3
systemctl restart claude-orchestrator
sleep 3

echo "=== AgentAPI status ==="
systemctl is-active claude-agentapi
echo ""

echo "=== AgentAPI logs (check allowed hosts/origins) ==="
journalctl -u claude-agentapi --no-pager -n 10 2>&1
echo ""

echo "=== Orchestrator status ==="
systemctl is-active claude-orchestrator
""", label="2. Restart services")

# ═══════════════════════════════════════════════════════════════════════
# 3. Test endpoints
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Test with Tailscale-like Origin header ==="

echo "AgentAPI (port 3284):"
curl -s -o /dev/null -w "  HTTP %{http_code}" \
  -H "Origin: http://100.93.211.48" \
  -H "Host: 100.108.202.49:3284" \
  http://localhost:3284 2>&1
echo ""

echo "Orchestrator (port 8080):"
curl -s -o /dev/null -w "  HTTP %{http_code}" \
  -H "Origin: http://100.93.211.48" \
  -H "Host: 100.108.202.49:8080" \
  http://localhost:8080/api/health 2>&1
echo ""

echo ""
echo "Orchestrator root (simulating iPhone access):"
curl -s -o /dev/null -w "  HTTP %{http_code}" \
  -H "Origin: http://cnc-server.tailb85819.ts.net:8080" \
  http://localhost:8080 2>&1
echo ""
""", label="3. Test with remote origin headers")

client.close()
print("\nDone!")
