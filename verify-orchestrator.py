#!/usr/bin/env python3
"""Verify orchestrator is actually functional — test API endpoints."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

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
# 1. Test orchestrator API routes
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Testing Orchestrator API Routes ==="
echo ""

echo "GET / (root — serves frontend, 500 expected if no static files):"
curl -sI http://localhost:8080/ 2>&1 | head -5
echo ""

echo "GET /api/health:"
curl -s http://localhost:8080/api/health 2>&1
echo ""

echo "GET /api/rooms:"
curl -s http://localhost:8080/api/rooms 2>&1 | head -5
echo ""

echo "GET /api/config:"
curl -s http://localhost:8080/api/config 2>&1 | head -5
echo ""

echo "POST /api/rooms (create a test room):"
curl -s -X POST http://localhost:8080/api/rooms \
  -H "Content-Type: application/json" \
  -d '{"name":"test-room"}' 2>&1 | head -5
echo ""
""", label="1. Test API routes")

# ═══════════════════════════════════════════════════════════════════════
# 2. Check what the ENOENT is about
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Investigating 500 error ==="
echo ""

echo "Full error from journal:"
journalctl -u claude-orchestrator -n 30 --no-pager 2>&1 | grep -A 3 "ENOENT\\|Error\\|error"
echo ""

echo "Static files dir:"
ls -la /opt/claude-code-by-agents/backend/dist/ 2>/dev/null || echo "No dist/ directory"
ls -la /opt/claude-code-by-agents/frontend/ 2>/dev/null || echo "No frontend/ directory"
echo ""

echo "Check app.ts for static file serving:"
grep -n "static\\|dist\\|ENOENT\\|serveStatic" /opt/claude-code-by-agents/backend/app.ts 2>/dev/null | head -15
echo ""

echo "What the orchestrator process looks like:"
ps aux | grep deno | grep -v grep
""", label="2. Investigate 500 error")

# ═══════════════════════════════════════════════════════════════════════
# 3. Build frontend if needed
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Check if frontend needs building ==="
cd /opt/claude-code-by-agents

echo "Project structure:"
ls -la
echo ""

if [ -d "frontend" ]; then
    echo "Frontend dir:"
    ls frontend/
    echo ""
    echo "Frontend package.json:"
    cat frontend/package.json 2>/dev/null | head -20 || echo "No package.json"
fi

echo ""
echo "Backend dist/ dir:"
ls -la backend/dist/ 2>/dev/null || echo "No backend/dist"
echo ""
echo "Backend dist/static:"
ls -la backend/dist/static/ 2>/dev/null || echo "No backend/dist/static"
""", label="3. Check frontend build")

# ═══════════════════════════════════════════════════════════════════════
# 4. Build frontend
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Building frontend ==="
cd /opt/claude-code-by-agents

# Check if there's a top-level build or a frontend build
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    cd frontend
    echo "Installing frontend deps..."
    npm install 2>&1 | tail -5
    echo ""
    echo "Building frontend..."
    npm run build 2>&1 | tail -10
    echo ""

    # Copy build output to backend/dist/static
    if [ -d "dist" ] || [ -d "build" ] || [ -d ".next" ]; then
        echo "Frontend build output:"
        ls dist/ 2>/dev/null || ls build/ 2>/dev/null || ls .next/ 2>/dev/null
    fi
else
    echo "No frontend directory with package.json"
    echo ""
    echo "Try deno task to copy frontend:"
    cd /opt/claude-code-by-agents/backend
    sudo -u claude-agent bash -c '
        export HOME=/home/claude-agent
        cd /opt/claude-code-by-agents/backend
        /usr/local/bin/deno task copy-frontend 2>&1
    ' || echo "copy-frontend task failed"
fi

# Ensure backend owns dist
chown -R claude-agent:claude-agent /opt/claude-code-by-agents
""", timeout=180, label="4. Build frontend")

# ═══════════════════════════════════════════════════════════════════════
# 5. Final verification
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Final Orchestrator Verification ==="
echo ""

# Restart with fresh state
systemctl restart claude-orchestrator
sleep 5

echo "Service: $(systemctl is-active claude-orchestrator)"
echo ""

echo "API endpoints:"
echo "  /api/health: $(curl -s http://localhost:8080/api/health 2>&1)"
echo "  /api/rooms:  $(curl -s http://localhost:8080/api/rooms 2>&1 | head -c 200)"
echo "  /api/config: $(curl -s http://localhost:8080/api/config 2>&1 | head -c 200)"
echo ""

echo "Root endpoint (HTTP code): $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/)"
echo ""

echo "Process:"
ps aux | grep "deno.*cli/deno.ts" | grep -v grep
""", label="5. Final verification")

client.close()
print("\nDone!")
