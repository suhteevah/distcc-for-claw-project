import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Check if Ollama got installed (the script may have succeeded before timeout)
print("=== Check Ollama status ===")
print(run(r"""
which ollama 2>/dev/null && ollama --version 2>&1 || echo "Ollama not installed"
systemctl is-active ollama 2>&1 || echo "ollama service not running"
"""))

# If not installed, install via direct binary download
print("\n=== Install Ollama if needed ===")
print(run(r"""
if ! which ollama &>/dev/null; then
    echo "Installing Ollama via direct binary..."
    curl -fsSL -o /usr/local/bin/ollama https://ollama.com/download/ollama-linux-amd64
    chmod +x /usr/local/bin/ollama
    echo "Ollama binary: $(ollama --version 2>&1)"

    # Create systemd service
    cat > /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3
Environment="HOME=/root"
Environment="OLLAMA_HOST=0.0.0.0"

[Install]
WantedBy=default.target
EOF
    systemctl daemon-reload
else
    echo "Ollama already installed: $(ollama --version 2>&1)"
fi
""", timeout=180))

# Start Ollama
print("\n=== Start Ollama ===")
print(run(r"""
systemctl enable ollama 2>&1
systemctl start ollama 2>&1
sleep 3
systemctl is-active ollama 2>&1
"""))

# Check NVIDIA/GPU status
print("\n=== GPU Status ===")
print(run(r"""
# Check NVIDIA
lsmod | grep -i nvidia | head -5 || echo "No NVIDIA modules"
lsmod | grep nouveau && echo "nouveau loaded (Ollama will use CPU)" || echo "nouveau not loaded"
ls /dev/nvidia* 2>/dev/null || echo "No NVIDIA devices"
echo ""
# Ollama will use CPU if no GPU driver - that's OK for now
echo "Ollama API test:"
curl -s http://localhost:11434/api/tags 2>&1 | head -3
"""))

# Pull a small model for testing (qwen2.5:0.5b is tiny)
print("\n=== Pull small model ===")
print(run(r"""
echo "Pulling qwen2.5:0.5b (small test model)..."
ollama pull qwen2.5:0.5b 2>&1 | tail -5
""", timeout=300))

# Phase 2: Create AgentAPI service
print("\n=== Create AgentAPI Service ===")
API_KEY = "***ANTHROPIC_KEY_REDACTED***"
print(run(f"""
cat > /etc/systemd/system/claude-agentapi.service << 'SERVICEEOF'
[Unit]
Description=Claude Code AgentAPI
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
Environment="ANTHROPIC_API_KEY={API_KEY}"
Environment="HOME=/root"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/agentapi server --port 3284 -- /usr/local/bin/claude --dangerously-skip-permissions
WorkingDirectory=/root
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
echo "AgentAPI service created"
"""))

# Phase 3: Create firewall rules
print("\n=== Firewall Rules ===")
print(run(r"""
# Check what firewall is in use
which firewall-cmd && echo "firewalld available" || echo "no firewalld"
which ufw && echo "ufw available" || echo "no ufw"
which nft && echo "nft available" || echo "no nft"

# Open ports for our services via firewalld (if available)
if which firewall-cmd &>/dev/null; then
    echo "Configuring firewalld..."
    # Allow from Tailscale interface
    firewall-cmd --zone=trusted --add-interface=tailscale0 --permanent 2>&1 || true
    # Open specific ports on the main interface
    firewall-cmd --add-port=3284/tcp --permanent 2>&1 || true  # AgentAPI
    firewall-cmd --add-port=8080/tcp --permanent 2>&1 || true  # Orchestrator UI
    firewall-cmd --add-port=11434/tcp --permanent 2>&1 || true # Ollama
    firewall-cmd --add-port=8765/tcp --permanent 2>&1 || true  # Icecream scheduler
    firewall-cmd --reload 2>&1 || true
    echo "Firewall rules applied"
else
    echo "No firewalld, checking iptables..."
    iptables -L INPUT -n 2>&1 | head -10
fi
"""))

# Summary
print("\n=== Final Summary ===")
print(run(r"""
echo "=== Installed Tools ==="
for cmd in node npm claude agentapi ollama tailscale; do
    if which $cmd &>/dev/null; then
        VER=$($cmd --version 2>&1 | head -1)
        echo "  OK  $cmd: $VER"
    else
        echo "  --  $cmd: NOT INSTALLED"
    fi
done

echo ""
echo "=== Services ==="
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi; do
    STATUS=$(systemctl is-active $svc 2>&1)
    ENABLED=$(systemctl is-enabled $svc 2>&1)
    echo "  $svc: active=$STATUS enabled=$ENABLED"
done

echo ""
echo "=== Network ==="
echo "  Local IP: $(ip -4 addr show enp3s0 | grep inet | awk '{print $2}')"
echo "  WiFi IP:  $(ip -4 addr show wlp0s20u9 | grep inet | awk '{print $2}' | head -1)"
echo "  Tailscale: $(tailscale ip -4 2>&1)"
echo "  Hostname: $(hostname)"

echo ""
echo "=== Remaining Setup ==="
echo "  - Enable AgentAPI service (start on demand)"
echo "  - Install icecream (optional, can use podman)"
echo "  - Install orchestrator frontend (claude-code-by-agents)"
echo "  - Pull larger Ollama model (if GPU driver installed)"
"""))

client.close()
print("\n=== DONE ===")
