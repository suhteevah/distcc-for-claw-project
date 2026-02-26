#!/usr/bin/env python3
"""Fix orchestrator v2: resolve node_modules path + generate missing version.ts."""

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
            for line in result.strip().split('\n')[:80]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# Stop orchestrator first
run("systemctl stop claude-orchestrator", label="0. Stop orchestrator")

# ═══════════════════════════════════════════════════════════════════════
# 1. Investigate — where did deno install put node_modules?
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Investigating node_modules location ==="
cd /opt/claude-code-by-agents/backend

echo "node_modules in backend dir:"
ls -la node_modules 2>/dev/null | head -5 || echo "NOT FOUND in backend/"

echo ""
echo "node_modules in project root:"
ls -la ../node_modules 2>/dev/null | head -5 || echo "NOT FOUND in root/"

echo ""
echo "Find node_modules anywhere under claude-code-by-agents:"
find /opt/claude-code-by-agents -name node_modules -type d 2>/dev/null

echo ""
echo "Find node_modules in claude-agent home:"
find /home/claude-agent -name node_modules -type d 2>/dev/null | head -5

echo ""
echo "deno.json nodeModulesDir setting:"
cat deno.json 2>/dev/null | grep -i "node" || echo "No nodeModules config in deno.json"
cat deno.jsonc 2>/dev/null | grep -i "node" || echo "No deno.jsonc"

echo ""
echo "Full deno.json:"
cat deno.json 2>/dev/null || echo "No deno.json"

echo ""
echo "ls backend dir:"
ls -la /opt/claude-code-by-agents/backend/
""", label="1. Investigate node_modules")

# ═══════════════════════════════════════════════════════════════════════
# 2. Check the version.ts generation script
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Version.ts investigation ==="
cd /opt/claude-code-by-agents/backend

echo "Looking for version generation scripts:"
ls scripts/ 2>/dev/null
echo ""
echo "generate-version.js:"
cat scripts/generate-version.js 2>/dev/null | head -30 || echo "Not found"
echo ""
echo "cli/args.ts import of version:"
grep -n "version" cli/args.ts 2>/dev/null | head -10
echo ""
echo "What's in cli/ dir:"
ls cli/ 2>/dev/null
""", label="2. Investigate version.ts")

# ═══════════════════════════════════════════════════════════════════════
# 3. Generate version.ts and setup node_modules properly
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Fix: Generate version.ts ==="
cd /opt/claude-code-by-agents/backend

# Try running the generate-version script
if [ -f scripts/generate-version.js ]; then
    echo "Running generate-version.js..."
    node scripts/generate-version.js 2>&1 || {
        echo "node script failed, creating version.ts manually..."
        VERSION=$(cat package.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','0.0.0'))" 2>/dev/null || echo "0.1.46")
        echo "export const VERSION = \\"$VERSION\\";" > cli/version.ts
        echo "Created cli/version.ts with version $VERSION"
    }
else
    echo "No generate-version.js, creating version.ts manually..."
    VERSION=$(cat package.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','0.0.0'))" 2>/dev/null || echo "0.1.46")
    echo "export const VERSION = \\"$VERSION\\";" > cli/version.ts
    echo "Created cli/version.ts with version $VERSION"
fi

echo ""
echo "cli/version.ts contents:"
cat cli/version.ts

# Ensure ownership
chown -R claude-agent:claude-agent /opt/claude-code-by-agents
""", label="3. Generate version.ts")

# ═══════════════════════════════════════════════════════════════════════
# 4. Run deno install properly WITH nodeModulesDir
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Proper deno install with node_modules ==="
cd /opt/claude-code-by-agents/backend

# The issue is deno needs to be told to use a local node_modules dir
# Check if deno.json already has nodeModulesDir
if ! grep -q 'nodeModulesDir' deno.json 2>/dev/null; then
    echo "Adding nodeModulesDir to deno.json..."
    # Add nodeModulesDir: true to deno.json
    python3 -c "
import json
with open('deno.json', 'r') as f:
    d = json.load(f)
d['nodeModulesDir'] = 'auto'
with open('deno.json', 'w') as f:
    json.dump(d, f, indent=2)
print('Added nodeModulesDir: auto to deno.json')
" 2>&1 || echo "deno.json update failed"
fi

echo ""
echo "Updated deno.json:"
cat deno.json | head -20

# Re-run deno install
sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    export DENO_DIR=/home/claude-agent/.cache/deno
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno install --node-modules-dir 2>&1
' || {
    echo "Trying without flag..."
    sudo -u claude-agent bash -c '
        export HOME=/home/claude-agent
        export DENO_DIR=/home/claude-agent/.cache/deno
        cd /opt/claude-code-by-agents/backend
        /usr/local/bin/deno install 2>&1
    '
}

echo ""
echo "node_modules now exists: $([ -d node_modules ] && echo YES || echo NO)"
echo "node_modules contents:"
ls node_modules/ 2>/dev/null | head -20 || echo "empty"
""", timeout=180, label="4. deno install with node_modules")

# ═══════════════════════════════════════════════════════════════════════
# 5. Try caching again now that version.ts exists
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Cache entry point ==="
cd /opt/claude-code-by-agents/backend

sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    export DENO_DIR=/home/claude-agent/.cache/deno
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno cache cli/deno.ts 2>&1
'
""", timeout=120, label="5. deno cache cli/deno.ts")

# ═══════════════════════════════════════════════════════════════════════
# 6. Update service to pass --node-modules-dir if needed
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Update orchestrator service ==="

# Check what's in the current service file
grep "ExecStart" /etc/systemd/system/claude-orchestrator.service

# Update service file to include --node-modules-dir flag
cat > /etc/systemd/system/claude-orchestrator.service << 'EOF'
[Unit]
Description=Claude Code Orchestrator (claude-code-by-agents)
After=network-online.target claude-agentapi.service tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=claude-agent
WorkingDirectory=/opt/claude-code-by-agents/backend
EnvironmentFile=-/etc/claude/api-key
Environment="HOME=/home/claude-agent"
Environment="DENO_DIR=/home/claude-agent/.cache/deno"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/deno run \\
  --allow-net --allow-run --allow-read --allow-write --allow-env \\
  --node-modules-dir \\
  cli/deno.ts \\
  --host 0.0.0.0 \\
  --port 8080 \\
  --claude-path /usr/local/bin/claude
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=claude-orchestrator

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo "Service updated"
""", label="6. Update service file")

# ═══════════════════════════════════════════════════════════════════════
# 7. Restart + verify
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Final restart ==="
systemctl restart claude-orchestrator
sleep 10

STATUS=$(systemctl is-active claude-orchestrator)
echo "Orchestrator status: $STATUS"

if [ "$STATUS" = "active" ]; then
    echo ""
    echo "SUCCESS! Testing endpoint..."
    curl -s -o /dev/null -w "  HTTP %{http_code}\\n" http://localhost:8080/ 2>/dev/null
    echo ""
    echo "Journal (recent):"
    journalctl -u claude-orchestrator -n 10 --no-pager 2>&1
else
    echo ""
    echo "Journal (debug):"
    journalctl -u claude-orchestrator -n 25 --no-pager 2>&1
fi
""", label="7. Final restart + verify")

# ═══════════════════════════════════════════════════════════════════════
# 8. Complete status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server Complete Status                       ║"
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
for port in 3284 8080 11434; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/ 2>/dev/null)
    echo "  localhost:$port → HTTP $CODE"
done
""", label="8. COMPLETE STATUS")

client.close()
print("\nDone!")
