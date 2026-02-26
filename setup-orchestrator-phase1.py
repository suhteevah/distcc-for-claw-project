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

# Phase 1: Install Node.js (binary from nodejs.org)
print("=== Phase 1: Install Node.js ===")
print(run(r"""
if which node &>/dev/null; then
    echo "Node.js already installed: $(node --version)"
else
    echo "Downloading Node.js v22 LTS..."
    cd /tmp
    curl -fsSL https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz -o node.tar.xz
    echo "Extracting..."
    tar -xf node.tar.xz
    cp -r node-v22.14.0-linux-x64/bin/* /usr/local/bin/
    cp -r node-v22.14.0-linux-x64/lib/* /usr/local/lib/
    cp -r node-v22.14.0-linux-x64/include/* /usr/local/include/ 2>/dev/null || true
    cp -r node-v22.14.0-linux-x64/share/* /usr/local/share/ 2>/dev/null || true
    rm -rf node.tar.xz node-v22.14.0-linux-x64
    echo "Node.js installed: $(node --version)"
    echo "npm: $(npm --version)"
fi
""", timeout=180))

# Phase 2: Install Claude Code
print("\n=== Phase 2: Install Claude Code ===")
print(run(r"""
if which claude &>/dev/null; then
    echo "Claude Code already installed: $(claude --version 2>&1 | head -1)"
else
    echo "Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code 2>&1 | tail -10
    echo "Claude Code: $(claude --version 2>&1 | head -1)"
fi
""", timeout=300))

# Phase 3: Install AgentAPI
print("\n=== Phase 3: Install AgentAPI ===")
print(run(r"""
if which agentapi &>/dev/null; then
    echo "AgentAPI already installed"
else
    echo "Installing AgentAPI..."
    curl -fsSL \
        "https://github.com/coder/agentapi/releases/latest/download/agentapi-linux-amd64" \
        -o /usr/local/bin/agentapi
    chmod +x /usr/local/bin/agentapi
    echo "AgentAPI installed"
fi
ls -la /usr/local/bin/agentapi 2>/dev/null
""", timeout=120))

# Phase 4: Setup API key
print("\n=== Phase 4: API Key Setup ===")
API_KEY = "***ANTHROPIC_KEY_REDACTED***"
print(run(f"""
mkdir -p /etc/claude
chmod 700 /etc/claude
echo "ANTHROPIC_API_KEY={API_KEY}" > /etc/claude/api-key
chmod 600 /etc/claude/api-key
echo "API key saved to /etc/claude/api-key"

# Also put it in environment for root
grep -q ANTHROPIC_API_KEY /root/.bashrc 2>/dev/null || echo 'export ANTHROPIC_API_KEY="{API_KEY}"' >> /root/.bashrc
echo "API key added to root's .bashrc"
"""))

# Phase 5: Install Ollama
print("\n=== Phase 5: Install Ollama ===")
print(run(r"""
if which ollama &>/dev/null; then
    echo "Ollama already installed: $(ollama --version 2>&1)"
else
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh 2>&1 | tail -10
    echo "Ollama installed: $(ollama --version 2>&1)"
fi
""", timeout=300))

# Phase 6: Start Ollama and pull a model
print("\n=== Phase 6: Start Ollama ===")
print(run(r"""
# Enable and start ollama service
systemctl enable ollama 2>&1 || true
systemctl start ollama 2>&1 || true
sleep 3
systemctl is-active ollama 2>&1

# Check GPU detection
echo ""
echo "=== GPU Detection ==="
nvidia-smi 2>&1 | head -8 || echo "nvidia-smi not available"
echo ""
ollama ps 2>&1 || echo "Ollama not running yet"
"""))

# Phase 7: Check NVIDIA driver status
print("\n=== Phase 7: NVIDIA driver status ===")
print(run(r"""
lsmod | grep -i nvidia | head -5 || echo "No NVIDIA kernel modules loaded"
ls /dev/nvidia* 2>/dev/null || echo "No /dev/nvidia devices"
echo ""
# Check if nouveau is loaded instead
lsmod | grep nouveau && echo "nouveau is loaded (need NVIDIA proprietary driver for Ollama GPU)" || echo "nouveau not loaded"
"""))

# Phase 8: Summary
print("\n=== Phase 8: Summary ===")
print(run(r"""
echo "=== Installed Tools ==="
for cmd in node npm claude agentapi ollama tailscale; do
    if which $cmd &>/dev/null; then
        VER=$($cmd --version 2>&1 | head -1)
        echo "  $cmd: $VER"
    else
        echo "  $cmd: NOT INSTALLED"
    fi
done
echo ""
echo "=== Services ==="
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi; do
    STATUS=$(systemctl is-active $svc 2>&1)
    ENABLED=$(systemctl is-enabled $svc 2>&1)
    echo "  $svc: active=$STATUS enabled=$ENABLED"
done
"""))

client.close()
print("\n=== DONE ===")
