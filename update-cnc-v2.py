#!/usr/bin/env python3
"""Fix remaining update items: git safe.directory, NVIDIA package names, orchestrator git pull."""

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
# 1. Fix git safe.directory and pull latest
# ═══════════════════════════════════════════════════════════════════════
run("""
git config --global --add safe.directory /opt/claude-code-by-agents
cd /opt/claude-code-by-agents

echo "Before pull:"
git log --oneline -3
echo ""
echo "Branch: $(git branch --show-current)"
echo "Remote: $(git remote -v | head -1)"
echo ""

git fetch origin 2>&1
BRANCH=$(git branch --show-current)
git pull origin "$BRANCH" 2>&1

echo ""
echo "After pull:"
git log --oneline -3
""", timeout=60, label="1. Git pull orchestrator")

# ═══════════════════════════════════════════════════════════════════════
# 2. Check if version changed, rebuild if needed
# ═══════════════════════════════════════════════════════════════════════
run("""
cd /opt/claude-code-by-agents/backend
OLD_VER=$(cat cli/version.ts 2>/dev/null | grep -oP 'VERSION = "\\K[^"]+')
NEW_VER=$(cat package.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','unknown'))")

echo "Old version: $OLD_VER"
echo "New version: $NEW_VER"

if [ "$OLD_VER" != "$NEW_VER" ]; then
    echo "Version changed! Regenerating + rebuilding..."
    node scripts/generate-version.js 2>&1

    sudo -u claude-agent bash -c '
        export HOME=/home/claude-agent
        export DENO_DIR=/home/claude-agent/.cache/deno
        cd /opt/claude-code-by-agents/backend
        /usr/local/bin/deno install --node-modules-dir 2>&1
    ' | tail -5

    cd /opt/claude-code-by-agents/frontend
    npm install 2>&1 | tail -3
    npm run build 2>&1 | tail -3

    cd /opt/claude-code-by-agents/backend
    sudo -u claude-agent bash -c '
        export HOME=/home/claude-agent
        cd /opt/claude-code-by-agents/backend
        /usr/local/bin/deno task copy-frontend 2>&1
    ' | tail -3

    chown -R claude-agent:claude-agent /opt/claude-code-by-agents

    systemctl restart claude-orchestrator
    sleep 5
    echo "Orchestrator: $(systemctl is-active claude-orchestrator)"
else
    echo "Version unchanged, no rebuild needed"
fi
""", timeout=180, label="2. Rebuild if needed")

# ═══════════════════════════════════════════════════════════════════════
# 3. Find correct NVIDIA package names
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Finding NVIDIA packages ==="
echo "GPU:"
lspci | grep -i vga
echo ""

echo "All NVIDIA-related packages in repos:"
zypper se nvidia 2>&1 | grep -v "^$" | head -30
echo ""

echo "Recommended for GTX 980 (Maxwell):"
zypper se nvidia-driver 2>&1 | grep -i "G05\\|G06\\|open" | head -10
echo ""

echo "Also checking nvidia-open:"
zypper se nvidia-open 2>&1 | grep -v "^$" | head -10
""", timeout=30, label="3. Find NVIDIA packages")

# ═══════════════════════════════════════════════════════════════════════
# 4. Try installing with correct package names
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Checking what NVIDIA repos are configured ==="
zypper lr -u 2>&1 | grep -i nvidia
echo ""

echo "The NVIDIA repo may need to be added first."
echo "Checking if we can add the openSUSE NVIDIA repo..."

# Add NVIDIA repo for Leap Micro 6.2
zypper ar -f https://download.nvidia.com/opensuse/leap/15.6/ nvidia 2>&1 || echo "Repo may already exist or URL wrong"

# Also try the community repo
zypper ar -f https://download.opensuse.org/repositories/hardware/15.6/ hardware 2>&1 || echo "hardware repo may already exist"

zypper --gpg-auto-import-keys ref 2>&1 | tail -5

echo ""
echo "Now searching NVIDIA packages again:"
zypper se nvidia 2>&1 | grep -i "driver\\|utils\\|kmp" | head -15
""", timeout=60, label="4. Add NVIDIA repo + search")

# ═══════════════════════════════════════════════════════════════════════
# 5. Install icecream separately (should work without NVIDIA)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Installing icecream + distcc via transactional-update ==="

# Check exact package names
echo "Available icecream packages:"
zypper se -s icecream 2>&1 | grep "^[[:space:]]*|" | head -10
echo ""
echo "Available distcc packages:"
zypper se -s distcc 2>&1 | grep "^[[:space:]]*|" | head -10

echo ""
echo "Installing icecream and distcc..."
transactional-update --non-interactive pkg install icecream distcc 2>&1 | tail -20
""", timeout=300, label="5. Install icecream + distcc")

# ═══════════════════════════════════════════════════════════════════════
# 6. Final status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server Update Complete                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Services (all 8):"
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
printf "  %-12s %s\\n" "claude:" "$(claude --version 2>&1 | head -1)"
printf "  %-12s %s\\n" "agentapi:" "$(agentapi --version 2>&1 | head -1)"
printf "  %-12s %s\\n" "deno:" "$(/usr/local/bin/deno --version 2>&1 | head -1)"
printf "  %-12s %s\\n" "node:" "$(node --version 2>&1)"
printf "  %-12s %s\\n" "ollama:" "$(ollama --version 2>&1 | head -1)"

echo ""
echo "Endpoints:"
echo "  Orchestrator: HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/) — $(curl -s http://localhost:8080/api/health 2>&1 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get(\"version\",\"?\"))' 2>/dev/null)"
echo "  AgentAPI:     HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3284/)"
echo "  Ollama:       HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:11434/)"

echo ""
PENDING=$(ls /var/lib/overlay 2>/dev/null | head -1)
if [ -n "$PENDING" ]; then
    echo "⚠  Pending reboot: YES — transactional-update snapshot ready"
    echo "   Run 'reboot' to activate icecream/distcc"
else
    echo "Pending reboot: checking snapshots..."
    snapper list 2>&1 | tail -5
fi
""", label="6. FINAL STATUS")

client.close()
print("\nDone!")
