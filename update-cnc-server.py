#!/usr/bin/env python3
"""Comprehensive update of cnc-server: pull latest code, update packages, install remaining items."""

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

# ═══════════════════════════════════════════════════════════════════════
# 1. Current state snapshot
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "Hostname: $(hostname)"
echo "Kernel:   $(uname -r)"
echo "Uptime:   $(uptime -p)"
echo ""
echo "Services:"
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator; do
    STATUS=$(systemctl is-active $svc 2>&1)
    printf "  %-24s %s\\n" "$svc" "$STATUS"
done
echo ""
echo "DNS: $(ping -c 1 -W 2 google.com &>/dev/null && echo 'OK' || echo 'BROKEN')"
echo "Tailscale: $(tailscale ip -4 2>/dev/null)"
""", label="1. Current state")

# ═══════════════════════════════════════════════════════════════════════
# 2. Update orchestrator repo (git pull)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Updating orchestrator repo ==="
cd /opt/claude-code-by-agents
echo "Current commit: $(git log --oneline -1)"
echo ""

git fetch origin 2>&1
git pull origin main 2>&1 || git pull origin master 2>&1

echo ""
echo "Updated commit: $(git log --oneline -1)"
""", timeout=60, label="2. Git pull orchestrator")

# ═══════════════════════════════════════════════════════════════════════
# 3. Rebuild orchestrator deps + frontend if code changed
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Reinstalling orchestrator deps ==="
cd /opt/claude-code-by-agents/backend

# Regenerate version.ts
node scripts/generate-version.js 2>&1 || {
    VERSION=$(cat package.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','0.0.0'))")
    echo "export const VERSION = \\"$VERSION\\";" > cli/version.ts
    echo "Generated version.ts manually: $VERSION"
}

# Reinstall deno deps
sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    export DENO_DIR=/home/claude-agent/.cache/deno
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno install --node-modules-dir 2>&1
' | tail -10

echo ""
echo "node_modules OK: $([ -d node_modules ] && echo YES || echo NO)"
""", timeout=180, label="3. Reinstall orchestrator deps")

run("""
echo "=== Rebuilding frontend ==="
cd /opt/claude-code-by-agents/frontend

npm install 2>&1 | tail -3
npm run build 2>&1 | tail -5

echo ""
echo "Copying to backend/dist/static..."
cd /opt/claude-code-by-agents/backend
sudo -u claude-agent bash -c '
    export HOME=/home/claude-agent
    cd /opt/claude-code-by-agents/backend
    /usr/local/bin/deno task copy-frontend 2>&1
' | tail -5

chown -R claude-agent:claude-agent /opt/claude-code-by-agents
echo "Frontend rebuilt"
""", timeout=120, label="3b. Rebuild frontend")

# ═══════════════════════════════════════════════════════════════════════
# 4. Restart orchestrator + AgentAPI
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Restarting services ==="
systemctl restart claude-agentapi
systemctl restart claude-orchestrator
sleep 8

echo "AgentAPI:     $(systemctl is-active claude-agentapi)"
echo "Orchestrator: $(systemctl is-active claude-orchestrator)"
echo ""
echo "API health: $(curl -s http://localhost:8080/api/health 2>&1)"
echo "Root page:  HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/)"
""", label="4. Restart services")

# ═══════════════════════════════════════════════════════════════════════
# 5. Update Ollama models
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Updating Ollama models ==="
echo "Current models:"
curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
for m in d.get('models',[]):
    size_gb = m.get('size',0) / 1e9
    print(f'  {m[\"name\"]:30s} {size_gb:.1f}GB')
" 2>&1

echo ""
echo "Pulling latest model versions..."
ollama pull qwen2.5:0.5b 2>&1 | tail -3
ollama pull qwen2.5-coder:7b 2>&1 | tail -3
""", timeout=300, label="5. Update Ollama models")

# ═══════════════════════════════════════════════════════════════════════
# 6. Update system tools (claude, agentapi, deno, node, tailscale)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Current tool versions ==="
echo "  claude:    $(claude --version 2>&1 | head -1)"
echo "  agentapi:  $(agentapi --version 2>&1 | head -1)"
echo "  deno:      $(/usr/local/bin/deno --version 2>&1 | head -1)"
echo "  node:      $(node --version 2>&1)"
echo "  tailscale: $(tailscale version 2>&1 | head -1)"
echo "  ollama:    $(ollama --version 2>&1 | head -1)"
""", label="6a. Current tool versions")

run("""
echo "=== Updating Claude CLI ==="
npm update -g @anthropic-ai/claude-code 2>&1 | tail -5
echo "  claude: $(claude --version 2>&1 | head -1)"
""", timeout=120, label="6b. Update Claude CLI")

run("""
echo "=== Updating Deno ==="
/usr/local/bin/deno upgrade 2>&1 | tail -5
echo "  deno: $(/usr/local/bin/deno --version 2>&1 | head -1)"
""", timeout=60, label="6c. Update Deno")

# ═══════════════════════════════════════════════════════════════════════
# 7. Transactional-update for NVIDIA + icecream
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Checking zypper repos ==="
zypper --gpg-auto-import-keys ref 2>&1 | tail -5
""", timeout=60, label="7a. Refresh repos")

run("""
echo "=== Checking available packages ==="
echo "NVIDIA driver:"
zypper se nvidia-driver-G06 2>&1 | grep -i nvidia | head -5
echo ""
echo "Icecream:"
zypper se icecream 2>&1 | grep -i icecream | head -5
echo ""
echo "distcc:"
zypper se distcc 2>&1 | grep -i distcc | head -5
""", timeout=30, label="7b. Check available packages")

run("""
echo "=== Running transactional-update ==="
echo "Installing NVIDIA driver + icecream in one snapshot..."
transactional-update --non-interactive pkg install \
    nvidia-driver-G06-signed nvidia-utils-G06 \
    icecream icecream-clang-wrappers 2>&1 | tail -30
""", timeout=600, label="7c. transactional-update install")

# ═══════════════════════════════════════════════════════════════════════
# 8. Final status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server — Post-Update Status                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Services:"
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  ● %-24s %s\\n" "$svc" "$STATUS"
    else
        printf "  ✗ %-24s %s\\n" "$svc" "$STATUS"
    fi
done

echo ""
echo "Tools:"
echo "  claude:    $(claude --version 2>&1 | head -1)"
echo "  agentapi:  $(agentapi --version 2>&1 | head -1)"
echo "  deno:      $(/usr/local/bin/deno --version 2>&1 | head -1)"
echo "  node:      $(node --version 2>&1)"
echo "  ollama:    $(ollama --version 2>&1 | head -1)"

echo ""
echo "Endpoints:"
echo "  AgentAPI:     HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3284/)"
echo "  Orchestrator: HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/)"
echo "  Ollama:       HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:11434/)"

echo ""
echo "DNS: $(ping -c 1 -W 2 google.com &>/dev/null && echo 'WORKING' || echo 'BROKEN')"
echo "Tailscale: $(tailscale ip -4 2>/dev/null)"

echo ""
echo "Pending reboot: $([ -d /var/lib/overlay/etc ] && echo 'YES — transactional-update snapshot ready' || echo 'NO')"
""", label="8. FINAL STATUS")

client.close()
print("\nDone!")
