#!/usr/bin/env python3
"""Fix DNS on cnc-server, then fix orchestrator and OpenClaw."""

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
# 1. Diagnose DNS
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "Current resolv.conf:"
cat /etc/resolv.conf
echo ""
echo "Is resolv.conf a symlink?"
ls -la /etc/resolv.conf
echo ""
echo "Check systemd-resolved:"
systemctl is-active systemd-resolved 2>&1 || echo "not active"
echo ""
echo "Check NetworkManager DNS:"
nmcli dev show enp3s0 2>/dev/null | grep DNS || echo "NM not managing enp3s0 DNS"
echo ""
echo "Route table:"
ip route | head -5
echo ""
echo "DNS via ethernet (directly):"
ping -I enp3s0 -c 1 -W 2 8.8.8.8 2>&1 | tail -1
echo ""
echo "DNS test with nslookup/dig:"
nslookup google.com 8.8.8.8 2>&1 | head -5 || host google.com 8.8.8.8 2>&1 | head -3 || echo "No nslookup or host command"
echo ""
echo "Direct DNS query test with python:"
python3 -c "import socket; print('Resolved:', socket.gethostbyname('google.com'))" 2>&1
""", label="1. DNS Diagnosis")

# ═══════════════════════════════════════════════════════════════════════
# 2. Fix DNS properly
# ═══════════════════════════════════════════════════════════════════════
run("""
# The real fix: ensure resolv.conf has proper nameservers and isn't being overwritten

# First check if it's managed by something
if [ -L /etc/resolv.conf ]; then
    echo "resolv.conf is a symlink to: $(readlink /etc/resolv.conf)"
    # Break the symlink and create a static file
    rm -f /etc/resolv.conf
fi

# Write a proper resolv.conf
cat > /etc/resolv.conf << 'EOF'
# Static DNS configuration
nameserver 8.8.8.8
nameserver 1.1.1.1
nameserver 10.0.0.1
search local
EOF

# Prevent dhcpcd from overwriting it
if [ -f /etc/dhcpcd.conf ]; then
    # Tell dhcpcd not to touch resolv.conf
    if ! grep -q 'nohook resolv.conf' /etc/dhcpcd.conf; then
        echo '' >> /etc/dhcpcd.conf
        echo '# Prevent dhcpcd from overwriting DNS config' >> /etc/dhcpcd.conf
        echo 'nohook resolv.conf' >> /etc/dhcpcd.conf
        echo "Added nohook resolv.conf to dhcpcd.conf"
    fi
fi

# Also make it immutable so nothing overwrites it
chattr +i /etc/resolv.conf 2>/dev/null && echo "Made resolv.conf immutable" || echo "chattr not available"

# Test immediately
echo ""
echo "Testing DNS resolution..."
ping -c 1 -W 3 google.com 2>&1 | tail -2
python3 -c "import socket; print('Python resolves google.com to:', socket.gethostbyname('google.com'))" 2>&1
""", label="2. Fix DNS")

# ═══════════════════════════════════════════════════════════════════════
# 3. Fix zypper repos (now that DNS works)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "Testing repo connectivity..."
zypper --gpg-auto-import-keys ref 2>&1 | tail -10
""", timeout=60, label="3. Refresh zypper repos")

# ═══════════════════════════════════════════════════════════════════════
# 4. Fix Orchestrator (Deno deps need DNS)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Caching Deno deps for orchestrator ==="
cd /opt/claude-code-by-agents/backend

# First verify DNS works for jsr.io
ping -c 1 -W 3 jsr.io 2>&1 | tail -1

# Cache deps
sudo -u claude-agent bash -c "export HOME=/home/claude-agent && cd /opt/claude-code-by-agents/backend && /usr/local/bin/deno cache cli/deno.ts 2>&1" | tail -20

echo ""
echo "Restarting orchestrator..."
systemctl restart claude-orchestrator
sleep 5
systemctl is-active claude-orchestrator && echo "Orchestrator: RUNNING" || {
    echo "Orchestrator journal:"
    journalctl -u claude-orchestrator -n 15 --no-pager
}
""", timeout=120, label="4. Fix Orchestrator deps")

# ═══════════════════════════════════════════════════════════════════════
# 5. Set up OpenClaw
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Setting up OpenClaw ==="
OPENCLAW_DIR="/home/claude-agent/.openclaw"
PLUGIN_DIR="$OPENCLAW_DIR/plugins/model-load-optimizer"

# Create dirs
sudo -u claude-agent mkdir -p "$OPENCLAW_DIR/plugins"

# Clone model-load-optimizer plugin
if [ ! -d "$PLUGIN_DIR" ]; then
    echo "Cloning model-load-optimizer..."
    sudo -u claude-agent git clone https://github.com/suhteevah/model-load-optimizer.git "$PLUGIN_DIR" 2>&1 || {
        echo "Clone failed — checking if repo exists..."
        # May not exist yet, create placeholder config
        echo "Using config without plugin"
    }
fi

# Write OpenClaw config
sudo -u claude-agent tee "$OPENCLAW_DIR/openclaw.json" > /dev/null << 'OCEOF'
{
  "env": { "OLLAMA_API_KEY": "ollama-local" },
  "auth": {
    "profiles": {
      "ollama:default": { "provider": "ollama", "mode": "api_key" }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen2.5:0.5b",
        "fallbacks": ["ollama/qwen2.5-coder:7b"]
      },
      "models": {
        "ollama/qwen2.5:0.5b": { "alias": "primary" },
        "ollama/qwen2.5-coder:7b": { "alias": "coder" }
      },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 }
    }
  },
  "tools": {
    "agentToAgent": { "enabled": true, "allow": ["exec"] },
    "exec": { "security": "full", "ask": "off" }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "0.0.0.0",
    "auth": { "mode": "token" },
    "tailscale": { "mode": "off" }
  },
  "plugins": {
    "load": { "paths": [] },
    "entries": {}
  }
}
OCEOF

echo "OpenClaw config written"
ls -la "$OPENCLAW_DIR/"
echo ""
cat "$OPENCLAW_DIR/openclaw.json" | head -15
""", timeout=60, label="5. OpenClaw config")

# ═══════════════════════════════════════════════════════════════════════
# 6. NVIDIA + Icecream status (require transactional-update)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Packages needing transactional-update + reboot ==="
echo ""
echo "These require a btrfs snapshot and reboot on Leap Micro:"
echo ""
echo "1. NVIDIA driver (GTX 980 — currently on nouveau):"
echo "   transactional-update pkg install nvidia-driver-G06-signed nvidia-utils-G06"
echo "   reboot"
echo ""
echo "2. Icecream (distributed compilation):"
echo "   transactional-update pkg install icecream icecream-clang-wrappers"
echo "   reboot"
echo ""
echo "Both can be combined into one snapshot:"
echo "   transactional-update --non-interactive pkg install nvidia-driver-G06-signed nvidia-utils-G06 icecream"
echo "   reboot"
echo ""
echo "NOTE: NVIDIA driver install requires working repos."
echo "Testing repo access..."
curl -sI https://download.opensuse.org/ 2>&1 | head -3
""", label="6. Remaining (need reboot)")

# ═══════════════════════════════════════════════════════════════════════
# 7. Final comprehensive status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server Status — Post-Fix                     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Services:"
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator; do
    STATUS=$(systemctl is-active $svc 2>&1)
    ENABLED=$(systemctl is-enabled $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  %-24s %s (%s)\\n" "$svc" "$STATUS" "$ENABLED"
    else
        printf "  %-24s %s (%s)\\n" "$svc" "$STATUS" "$ENABLED"
    fi
done

echo ""
echo "DNS: $(ping -c 1 -W 2 google.com &>/dev/null && echo 'WORKING' || echo 'BROKEN')"
echo ""
echo "Endpoints reachable:"
curl -s -o /dev/null -w "  AgentAPI  (3284): %{http_code}\\n" http://localhost:3284/ 2>/dev/null || echo "  AgentAPI  (3284): unreachable"
curl -s -o /dev/null -w "  Orchestr  (8080): %{http_code}\\n" http://localhost:8080/ 2>/dev/null || echo "  Orchestr  (8080): unreachable"
curl -s -o /dev/null -w "  Ollama   (11434): %{http_code}\\n" http://localhost:11434/ 2>/dev/null || echo "  Ollama   (11434): unreachable"
""", label="7. FINAL STATUS")

client.close()
print("\nDone!")
