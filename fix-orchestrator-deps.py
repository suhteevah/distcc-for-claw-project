#!/usr/bin/env python3
"""Fix orchestrator: run deno install to resolve npm deps from package.json."""

import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120, label=None):
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
            for line in result.strip().split('\n')[:60]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Examine the project structure to understand what deps are needed
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Orchestrator project structure ==="
cd /opt/claude-code-by-agents/backend
echo "package.json:"
cat package.json 2>/dev/null || echo "No package.json"
echo ""
echo "deno.json:"
cat deno.json 2>/dev/null || echo "No deno.json"
echo ""
echo "deno.jsonc:"
cat deno.jsonc 2>/dev/null || echo "No deno.jsonc"
echo ""
echo "deno.lock exists: $([ -f deno.lock ] && echo YES || echo NO)"
echo "node_modules exists: $([ -d node_modules ] && echo YES || echo NO)"
echo ""
ls -la
""", label="1. Examine project files")

# ═══════════════════════════════════════════════════════════════════════
# 2. Stop orchestrator while we fix deps
# ═══════════════════════════════════════════════════════════════════════
run("""
systemctl stop claude-orchestrator
echo "Stopped orchestrator"
""", label="2. Stop orchestrator")

# ═══════════════════════════════════════════════════════════════════════
# 3. Run deno install as claude-agent to resolve npm deps
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Running deno install ==="
cd /opt/claude-code-by-agents/backend

# Ensure claude-agent owns the directory
chown -R claude-agent:claude-agent /opt/claude-code-by-agents

# Run deno install as claude-agent
sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    export DENO_DIR=/home/claude-agent/.cache/deno
    mkdir -p "$DENO_DIR"
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno install 2>&1
'
echo ""
echo "node_modules exists now: $([ -d node_modules ] && echo YES || echo NO)"
if [ -d node_modules ]; then
    echo "node_modules contents:"
    ls node_modules/ | head -20
fi
""", timeout=180, label="3. deno install")

# ═══════════════════════════════════════════════════════════════════════
# 4. Also cache the main entry point
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Caching main entry point ==="
cd /opt/claude-code-by-agents/backend

sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    export DENO_DIR=/home/claude-agent/.cache/deno
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno cache cli/deno.ts 2>&1
'
""", timeout=180, label="4. deno cache cli/deno.ts")

# ═══════════════════════════════════════════════════════════════════════
# 5. Restart orchestrator and verify
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Restarting orchestrator ==="
systemctl restart claude-orchestrator
sleep 8

STATUS=$(systemctl is-active claude-orchestrator)
echo "Orchestrator status: $STATUS"

if [ "$STATUS" = "active" ]; then
    echo ""
    echo "Testing endpoint..."
    curl -s -o /dev/null -w "  HTTP status: %{http_code}\\n" http://localhost:8080/ 2>/dev/null || echo "  Endpoint not responding yet"
    echo ""
    echo "Recent journal (last 10 lines):"
    journalctl -u claude-orchestrator -n 10 --no-pager 2>&1
else
    echo ""
    echo "FAILED — journal output:"
    journalctl -u claude-orchestrator -n 20 --no-pager 2>&1
fi
""", label="5. Restart + verify")

# ═══════════════════════════════════════════════════════════════════════
# 6. Full service status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server Service Status                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  ● %-24s %s\\n" "$svc" "$STATUS"
    else
        printf "  ✗ %-24s %s\\n" "$svc" "$STATUS"
    fi
done

echo ""
echo "Endpoints:"
curl -s -o /dev/null -w "  AgentAPI  (3284): %{http_code}\\n" http://localhost:3284/ 2>/dev/null || echo "  AgentAPI  (3284): unreachable"
curl -s -o /dev/null -w "  Orchestr  (8080): %{http_code}\\n" http://localhost:8080/ 2>/dev/null || echo "  Orchestr  (8080): unreachable"
curl -s -o /dev/null -w "  Ollama   (11434): %{http_code}\\n" http://localhost:11434/ 2>/dev/null || echo "  Ollama   (11434): unreachable"

echo ""
echo "DNS: $(ping -c 1 -W 2 google.com &>/dev/null && echo 'WORKING' || echo 'BROKEN')"
""", label="6. FULL STATUS")

client.close()
print("\nDone!")
