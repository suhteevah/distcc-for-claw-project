#!/usr/bin/env python3
"""Finish cnc-server orchestrator setup — fills in all gaps from bootstrap."""

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
            for line in result.strip().split('\n')[:40]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. DNS Fix
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
# Test current DNS
if ping -c 1 -W 2 google.com &>/dev/null; then
    echo "DNS already working"
else
    echo "Fixing DNS..."
    # Add DNS servers to resolv.conf
    cat > /etc/resolv.conf << 'EOF'
nameserver 8.8.8.8
nameserver 1.1.1.1
nameserver 10.0.0.1
EOF
    # Configure dhcpcd to preserve DNS
    if [ -f /etc/dhcpcd.conf ]; then
        if ! grep -q 'static domain_name_servers' /etc/dhcpcd.conf; then
            echo '' >> /etc/dhcpcd.conf
            echo '# Ensure DNS servers are set' >> /etc/dhcpcd.conf
            echo 'static domain_name_servers=8.8.8.8 1.1.1.1' >> /etc/dhcpcd.conf
        fi
    fi
    # Test
    if ping -c 1 -W 3 google.com &>/dev/null; then
        echo "DNS: FIXED"
    else
        echo "DNS: still failing via WiFi (may need resolv.conf hook)"
    fi
fi
""", label="1. Fix WiFi DNS")

# ═══════════════════════════════════════════════════════════════════════
# 2. claude-agent user + API key
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
# Create service user if needed
if ! id claude-agent &>/dev/null; then
    useradd -r -m -s /bin/bash claude-agent
    echo "Created claude-agent user"
else
    echo "claude-agent user already exists"
fi

# API key file
mkdir -p /etc/claude
chmod 700 /etc/claude
echo 'ANTHROPIC_API_KEY=***ANTHROPIC_KEY_REDACTED***' > /etc/claude/api-key
chmod 600 /etc/claude/api-key
chown claude-agent:claude-agent /etc/claude/api-key 2>/dev/null || true
echo "API key configured"

# Ensure claude-agent home exists and has right permissions
mkdir -p /home/claude-agent
chown -R claude-agent:claude-agent /home/claude-agent
""", label="2. Service user + API key")

# ═══════════════════════════════════════════════════════════════════════
# 3. AgentAPI systemd service
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
cat > /etc/systemd/system/claude-agentapi.service << 'EOF'
[Unit]
Description=Claude Code AgentAPI Server
After=network-online.target tailscaled.service ollama.service
Wants=network-online.target

[Service]
Type=simple
User=claude-agent
WorkingDirectory=/home/claude-agent
EnvironmentFile=-/etc/claude/api-key
ExecStart=/usr/local/bin/agentapi server --type claude -- /usr/local/bin/claude \
  --dangerously-skip-permissions \
  --max-budget-usd 10.00
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=claude-agentapi

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable claude-agentapi.service
systemctl restart claude-agentapi.service
sleep 3
systemctl is-active claude-agentapi.service && echo "AgentAPI: RUNNING" || echo "AgentAPI: FAILED to start"
""", label="3. AgentAPI service")

# ═══════════════════════════════════════════════════════════════════════
# 4. Orchestrator (claude-code-by-agents)
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
ORCHESTRATOR_DIR="/opt/claude-code-by-agents"

# Clone if not present
if [ ! -d "$ORCHESTRATOR_DIR" ]; then
    echo "Cloning claude-code-by-agents..."
    git clone https://github.com/baryhuang/claude-code-by-agents.git "$ORCHESTRATOR_DIR"
    chown -R claude-agent:claude-agent "$ORCHESTRATOR_DIR"
else
    echo "Orchestrator repo already exists"
    ls "$ORCHESTRATOR_DIR"
fi

# Ensure deno is accessible
DENO_PATH=""
if [ -x /usr/local/bin/deno ]; then
    DENO_PATH="/usr/local/bin/deno"
elif [ -x /root/.deno/bin/deno ]; then
    DENO_PATH="/root/.deno/bin/deno"
    cp /root/.deno/bin/deno /usr/local/bin/deno 2>/dev/null || true
    chmod 755 /usr/local/bin/deno 2>/dev/null || true
    DENO_PATH="/usr/local/bin/deno"
fi

if [ -z "$DENO_PATH" ]; then
    echo "ERROR: Deno not found"
    exit 1
fi
echo "Deno: $($DENO_PATH --version 2>/dev/null | head -1)"

# Create symlink for claude-agent
sudo -u claude-agent mkdir -p /home/claude-agent/.deno/bin 2>/dev/null || true
ln -sf /usr/local/bin/deno /home/claude-agent/.deno/bin/deno 2>/dev/null || true
""", timeout=60, label="4. Orchestrator repo + Deno")

out, _ = run("""
# Cache orchestrator deps
ORCHESTRATOR_DIR="/opt/claude-code-by-agents"
if [ -d "$ORCHESTRATOR_DIR/backend" ]; then
    cd "$ORCHESTRATOR_DIR/backend"
    # Check what entry point exists
    if [ -f "cli/deno.ts" ]; then
        echo "Caching cli/deno.ts deps..."
        sudo -u claude-agent bash -c "export HOME=/home/claude-agent && cd $ORCHESTRATOR_DIR/backend && /usr/local/bin/deno cache cli/deno.ts 2>&1" || echo "Cache had warnings (OK)"
    elif [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then
        echo "Found deno.json, caching..."
        ls *.ts *.json 2>/dev/null | head -5
    fi
    echo "Orchestrator dir contents:"
    ls -la "$ORCHESTRATOR_DIR/backend/" | head -10
fi
""", timeout=60, label="4b. Cache orchestrator deps")

out, _ = run("""
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
ExecStart=/usr/local/bin/deno run \
  --allow-net --allow-run --allow-read --allow-write --allow-env \
  cli/deno.ts \
  --host 0.0.0.0 \
  --port 8080 \
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
systemctl enable claude-orchestrator.service
systemctl restart claude-orchestrator.service
sleep 5
systemctl is-active claude-orchestrator.service && echo "Orchestrator: RUNNING" || {
    echo "Orchestrator: checking journal..."
    journalctl -u claude-orchestrator -n 10 --no-pager 2>&1
}
""", label="4c. Orchestrator service")

# ═══════════════════════════════════════════════════════════════════════
# 5. Icecream check / install
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
# Check what's available
echo "=== Checking icecream packages ==="
if command -v iceccd &>/dev/null; then
    echo "icecream already installed"
    iceccd --version 2>&1 || true
else
    echo "icecream not installed, checking repos..."
    zypper se -s icecream 2>&1 | head -10

    # Try installing via transactional-update
    echo ""
    echo "NOTE: On Leap Micro, icecream requires transactional-update + reboot:"
    echo "  transactional-update pkg install icecream"
    echo "  reboot"
    echo ""
    echo "Checking if it's in any configured repo..."
    zypper info icecream 2>&1 | grep -E 'Name|Version|Repository|Status' || echo "Package not found in repos"
fi

# Also check distcc
if command -v distcc &>/dev/null; then
    echo "distcc installed: $(distcc --version 2>&1 | head -1)"
else
    echo "distcc not installed"
    zypper info distcc 2>&1 | grep -E 'Name|Version|Repository|Status' || echo "distcc not in repos"
fi
""", label="5. Icecream / distcc status")

# ═══════════════════════════════════════════════════════════════════════
# 6. NVIDIA driver check
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
echo "=== GPU Status ==="
lspci | grep -i vga
echo ""

if command -v nvidia-smi &>/dev/null; then
    nvidia-smi | head -10
else
    echo "No NVIDIA driver installed"
    echo "Current module: $(lsmod | grep nouveau | head -1)"
    echo ""
    echo "Checking available NVIDIA packages..."
    zypper se nvidia-driver 2>&1 | grep -i "nvidia-driver" | head -10
    echo ""
    echo "Recommended install:"
    echo "  transactional-update pkg install nvidia-driver-G06-signed nvidia-utils-G06"
    echo "  reboot"
fi
""", label="6. NVIDIA GPU driver")

# ═══════════════════════════════════════════════════════════════════════
# 7. OpenClaw setup
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
echo "=== OpenClaw Status ==="
OPENCLAW_DIR="/home/claude-agent/.openclaw"

# Check if openclaw exists
if [ -d "$OPENCLAW_DIR" ]; then
    echo "OpenClaw dir exists:"
    ls -la "$OPENCLAW_DIR/"
    echo ""
    if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
        echo "Config exists:"
        cat "$OPENCLAW_DIR/openclaw.json" | head -30
    fi
else
    echo "OpenClaw directory not found at $OPENCLAW_DIR"
fi

# Check for model-load-optimizer plugin
PLUGIN_DIR="$OPENCLAW_DIR/plugins/model-load-optimizer"
if [ -d "$PLUGIN_DIR" ]; then
    echo ""
    echo "Plugin exists:"
    ls "$PLUGIN_DIR/" | head -10
else
    echo "Plugin not installed"
fi

# Check if openclaw has a gateway process
ps aux | grep -i "openclaw\|gateway" | grep -v grep || echo "No openclaw/gateway process running"
""", label="7. OpenClaw check")

# ═══════════════════════════════════════════════════════════════════════
# 8. Firewall — ensure all needed ports are open
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
echo "=== Firewall update ==="
# Add missing ports
for port in 3284/tcp 8080/tcp 8765/tcp 8766/tcp 10245/tcp 11434/tcp 18789/tcp; do
    firewall-cmd --permanent --add-port=$port 2>/dev/null && echo "  Added $port" || echo "  $port already open"
done
firewall-cmd --reload
echo ""
echo "Open ports: $(firewall-cmd --list-ports)"
echo "Trusted: $(firewall-cmd --zone=trusted --list-interfaces)"
""", label="8. Firewall ports")

# ═══════════════════════════════════════════════════════════════════════
# 9. Final status
# ═══════════════════════════════════════════════════════════════════════
out, _ = run("""
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server Final Status                          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator; do
    STATUS=$(systemctl is-active $svc 2>&1)
    ENABLED=$(systemctl is-enabled $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        echo "  ● $svc: $STATUS ($ENABLED)"
    else
        echo "  ✗ $svc: $STATUS ($ENABLED)"
    fi
done

echo ""
echo "Network:"
echo "  Ethernet: $(ip -4 addr show enp3s0 2>/dev/null | grep 'inet ' | awk '{print $2}')"
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "  WiFi:     $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}')"
echo "  Tailscale: $(tailscale ip -4 2>/dev/null)"

echo ""
echo "DNS: $(ping -c 1 -W 2 google.com &>/dev/null && echo 'WORKING' || echo 'BROKEN')"

echo ""
echo "Endpoints:"
echo "  AgentAPI:      http://cnc-server:3284"
echo "  Orchestrator:  http://cnc-server:8080"
echo "  Ollama:        http://cnc-server:11434"
""", label="9. FINAL STATUS")

client.close()
print("\nDone!")
