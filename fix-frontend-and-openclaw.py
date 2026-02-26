#!/usr/bin/env python3
"""Fix: copy frontend build to backend/dist/static + investigate OpenClaw on kokonoe."""

import paramiko
import sys
import io

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
# 1. Copy frontend build output to where backend expects it
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Copying frontend build to backend/dist/static ==="
cd /opt/claude-code-by-agents

# The copy-frontend script should handle this
echo "Running backend copy-frontend task..."
sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno task copy-frontend 2>&1
'

echo ""
echo "Check if backend/dist/static now has files:"
ls -la backend/dist/static/ 2>/dev/null || {
    echo "copy-frontend didn't work, doing manual copy..."
    mkdir -p backend/dist/static
    cp -r frontend/dist/* backend/dist/static/
    chown -R claude-agent:claude-agent backend/dist
    echo "Manually copied. Contents:"
    ls -la backend/dist/static/
}
""", label="1. Copy frontend build")

# ═══════════════════════════════════════════════════════════════════════
# 2. Restart orchestrator and verify frontend works
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Restart orchestrator with frontend ==="
systemctl restart claude-orchestrator
sleep 5

STATUS=$(systemctl is-active claude-orchestrator)
echo "Orchestrator: $STATUS"
echo ""

echo "Testing endpoints:"
echo "  GET / (root):    HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/)"
echo "  GET /api/health: $(curl -s http://localhost:8080/api/health 2>&1)"
echo ""

# Check if index.html is served
echo "Root page content (first 3 lines):"
curl -s http://localhost:8080/ 2>&1 | head -3
""", label="2. Restart + verify frontend")

# ═══════════════════════════════════════════════════════════════════════
# 3. Investigate API routes more deeply
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== API Route Investigation ==="
cd /opt/claude-code-by-agents/backend

echo "Available API routes in code:"
grep -rn 'app\\.get\\|app\\.post\\|app\\.put\\|app\\.delete\\|router\\.' *.ts handlers/*.ts routes/*.ts 2>/dev/null | grep -oP '(get|post|put|delete)\\("[^"]*"' | sort -u | head -30

echo ""
echo "Route file structure:"
ls handlers/ routes/ 2>/dev/null

echo ""
echo "Testing various endpoints:"
for ep in "/api/health" "/api/v1/health" "/api/sessions" "/api/v1/sessions" "/api/agents" "/sessions" "/rooms"; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080$ep)
    echo "  $ep → HTTP $CODE"
done
""", label="3. API route investigation")

client.close()
print("\ncnc-server orchestrator done!")
print("\nNow investigating OpenClaw on kokonoe (localhost)...")
