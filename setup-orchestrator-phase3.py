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

# Fix 1: Set hostname
print("=== Fix 1: Set hostname ===")
print(run(r"""
hostnamectl set-hostname cnc-server
echo "Hostname set to: $(hostname)"
"""))

# Fix 2: Create Ollama service and start it
print("\n=== Fix 2: Create & start Ollama service ===")
print(run(r"""
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
systemctl enable ollama
systemctl start ollama
sleep 3
systemctl is-active ollama
echo "Ollama version: $(ollama --version 2>&1)"
"""))

# Fix 3: Start firewalld and configure
print("\n=== Fix 3: Configure firewall ===")
print(run(r"""
systemctl enable firewalld 2>&1
systemctl start firewalld 2>&1
sleep 2
if systemctl is-active firewalld &>/dev/null; then
    echo "firewalld is running"
    # Trust Tailscale interface
    firewall-cmd --zone=trusted --add-interface=tailscale0 --permanent 2>&1
    # Open service ports
    firewall-cmd --add-port=3284/tcp --permanent 2>&1   # AgentAPI
    firewall-cmd --add-port=8080/tcp --permanent 2>&1   # Orchestrator UI
    firewall-cmd --add-port=11434/tcp --permanent 2>&1  # Ollama
    firewall-cmd --add-port=8765/tcp --permanent 2>&1   # Icecream scheduler
    firewall-cmd --reload 2>&1
    echo ""
    echo "Active zones:"
    firewall-cmd --get-active-zones 2>&1
    echo ""
    echo "Open ports:"
    firewall-cmd --list-ports 2>&1
else
    echo "firewalld not running, skipping"
fi
"""))

# Fix 4: Pull a small Ollama model
print("\n=== Fix 4: Pull small model ===")
print(run(r"""
echo "Testing Ollama API..."
curl -s http://localhost:11434/api/tags 2>&1 | head -3
echo ""
echo "Pulling qwen2.5:0.5b..."
ollama pull qwen2.5:0.5b 2>&1 | tail -5
""", timeout=300))

# Fix 5: Test Ollama
print("\n=== Fix 5: Test Ollama ===")
print(run(r"""
echo '{"model":"qwen2.5:0.5b","prompt":"Say hello in one sentence.","stream":false}' | \
    curl -s http://localhost:11434/api/generate -d @- 2>&1 | \
    python3 -c "import json,sys; r=json.load(sys.stdin); print('Response:', r.get('response','ERROR')[:200])" 2>&1
""", timeout=60))

# Fix 6: Set up claude-code-by-agents orchestrator
print("\n=== Fix 6: Install Deno + orchestrator ===")
print(run(r"""
# Install Deno
if ! which deno &>/dev/null; then
    echo "Installing Deno..."
    curl -fsSL https://deno.land/install.sh | sh 2>&1 | tail -5
    export DENO_INSTALL="/root/.deno"
    export PATH="$DENO_INSTALL/bin:$PATH"
    # Add to bashrc
    grep -q DENO_INSTALL /root/.bashrc || echo 'export DENO_INSTALL="/root/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"' >> /root/.bashrc
    echo "Deno: $(deno --version 2>&1 | head -1)"
else
    echo "Deno already installed"
fi
""", timeout=120))

# Clone orchestrator
print("\n=== Clone orchestrator ===")
print(run(r"""
if [ ! -d /opt/claude-code-by-agents ]; then
    echo "Cloning claude-code-by-agents..."
    git clone https://github.com/baryhuang/claude-code-by-agents.git /opt/claude-code-by-agents 2>&1 | tail -5
else
    echo "claude-code-by-agents already exists"
    ls /opt/claude-code-by-agents/
fi
""", timeout=120))

# Summary
print("\n=== FINAL STATUS ===")
print(run(r"""
echo "=== Tools ==="
for cmd in node npm claude agentapi ollama tailscale deno; do
    LOC=$(which $cmd 2>/dev/null || echo "NOT FOUND")
    if [ "$LOC" != "NOT FOUND" ]; then
        VER=$($cmd --version 2>&1 | head -1)
        echo "  [OK] $cmd: $VER"
    else
        # Check .deno/bin
        if [ -f "/root/.deno/bin/$cmd" ]; then
            VER=$(/root/.deno/bin/$cmd --version 2>&1 | head -1)
            echo "  [OK] $cmd (in .deno/bin): $VER"
        else
            echo "  [--] $cmd: NOT FOUND"
        fi
    fi
done

echo ""
echo "=== Services ==="
for svc in tailscaled ollama claude-agentapi rtw88-wifi wpa-wifi dhcpcd-wifi; do
    STATUS=$(systemctl is-active $svc 2>&1)
    ENABLED=$(systemctl is-enabled $svc 2>&1)
    echo "  $svc: active=$STATUS enabled=$ENABLED"
done

echo ""
echo "=== Network ==="
echo "  Hostname:   $(hostname)"
echo "  Ethernet:   $(ip -4 addr show enp3s0 | grep inet | awk '{print $2}')"
echo "  WiFi:       $(ip -4 addr show wlp0s20u9 | grep inet | awk '{print $2}' | head -1)"
echo "  Tailscale:  $(tailscale ip -4 2>&1)"
echo "  Ollama API: $(curl -s http://localhost:11434/api/tags 2>&1 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("models",[])), "models loaded")' 2>&1 || echo 'unreachable')"
"""))

client.close()
print("\n=== DONE ===")
