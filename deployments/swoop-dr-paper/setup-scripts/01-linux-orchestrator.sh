#!/bin/bash
set -euo pipefail

# =============================================================================
# Dr Paper -- Linux Orchestrator Setup
# Run this on: Swoop's dedicated Linux box
# Role: Central orchestrator (Dr Paper) + icecream scheduler + build worker
# =============================================================================

HOSTNAME="dr-paper"

echo "============================================"
echo "  Deploying Dr Paper on $(hostname)"
echo "  Tailscale hostname: ${HOSTNAME}"
echo "============================================"

echo "=== Phase 1: System Update ==="
# Detect package manager
if command -v pacman &>/dev/null; then
  PKG="pacman"
  sudo pacman -Syu --noconfirm
elif command -v apt &>/dev/null; then
  PKG="apt"
  sudo apt update && sudo apt upgrade -y
elif command -v dnf &>/dev/null; then
  PKG="dnf"
  sudo dnf upgrade -y
else
  echo "ERROR: Unsupported package manager. Install packages manually."
  exit 1
fi

echo "=== Phase 2: Install Base Dependencies ==="
case $PKG in
  pacman)
    sudo pacman -S --noconfirm --needed \
      nodejs npm git ripgrep base-devel ccache clang tailscale icecream curl jq
    ;;
  apt)
    sudo apt install -y git ripgrep build-essential ccache clang curl jq
    # Node.js 20
    if ! command -v node &>/dev/null || [ "$(node -v | cut -d. -f1 | tr -d v)" -lt 20 ]; then
      curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
      sudo apt-get install -y nodejs
    fi
    # Tailscale
    if ! command -v tailscale &>/dev/null; then
      curl -fsSL https://tailscale.com/install.sh | sh
    fi
    # Icecream
    sudo apt install -y icecc
    ;;
  dnf)
    sudo dnf install -y nodejs npm git ripgrep gcc gcc-c++ ccache clang curl jq
    if ! command -v tailscale &>/dev/null; then
      curl -fsSL https://tailscale.com/install.sh | sh
    fi
    sudo dnf install -y icecream || echo "WARNING: Install icecream manually"
    ;;
esac

echo "=== Phase 3: Tailscale ==="
sudo systemctl enable --now tailscaled
echo ">>> Run: sudo tailscale up --hostname ${HOSTNAME}"
echo ">>> Authenticate in your browser."
read -p "Press Enter after Tailscale is authenticated..."

echo "=== Phase 4: Icecream Scheduler + Worker ==="
sudo mkdir -p /opt/icecc-envs

# Start scheduler
if systemctl list-unit-files | grep -q icecc-scheduler; then
  sudo systemctl enable --now icecc-scheduler.service
else
  echo "Starting icecc-scheduler manually..."
  nohup icecc-scheduler -d &>/dev/null &
  echo "WARNING: No systemd unit for icecc-scheduler. Consider creating one."
fi

# Configure and start worker daemon
if [ -f /etc/conf.d/icecream ]; then
  sudo sed -i 's/^#\?ICECC_SCHEDULER_HOST=.*/ICECC_SCHEDULER_HOST="localhost"/' /etc/conf.d/icecream
elif [ -f /etc/default/icecc ]; then
  sudo sed -i 's/^#\?ICECC_SCHEDULER_HOST=.*/ICECC_SCHEDULER_HOST="localhost"/' /etc/default/icecc
fi

# Start iceccd
for svc in iceccd icecc-daemon icecc; do
  if systemctl list-unit-files | grep -q "^${svc}.service"; then
    sudo systemctl enable --now "${svc}.service"
    break
  fi
done

# Create toolchain tarball
echo "Creating toolchain tarball..."
cd /tmp
icecc-create-env --clang /usr/bin/clang /usr/bin/clang++ 2>/dev/null || true
TARBALL=$(ls -t /tmp/*.tar.gz 2>/dev/null | head -1)
if [ -n "$TARBALL" ]; then
  sudo mv "$TARBALL" /opt/icecc-envs/x86_64-clang.tar.gz
  echo "Toolchain: /opt/icecc-envs/x86_64-clang.tar.gz"
fi

echo "=== Phase 5: Claude Code ==="
npm install -g @anthropic-ai/claude-code
claude --version

echo "=== Phase 6: AgentAPI ==="
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
sudo curl -fsSL \
  "https://github.com/coder/agentapi/releases/latest/download/agentapi-${OS}-${ARCH_HW}" \
  -o /usr/local/bin/agentapi
sudo chmod +x /usr/local/bin/agentapi

echo "=== Phase 7: Create claude-agent user ==="
if ! id claude-agent &>/dev/null; then
  sudo useradd -r -m -s /bin/bash claude-agent
fi

echo "=== Phase 8: API Key Setup ==="
echo ""
echo "You need an Anthropic API key."
echo "Get one at: https://console.anthropic.com/"
echo ""
sudo mkdir -p /etc/claude
sudo chmod 700 /etc/claude
if [ ! -f /etc/claude/api-key ]; then
  read -sp "Enter your Anthropic API key: " API_KEY
  echo
  echo "ANTHROPIC_API_KEY=${API_KEY}" | sudo tee /etc/claude/api-key > /dev/null
  sudo chmod 600 /etc/claude/api-key
  sudo chown claude-agent:claude-agent /etc/claude/api-key
  echo "API key saved to /etc/claude/api-key"
else
  echo "API key file already exists"
fi

echo "=== Phase 9: Install Service Files ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_DIR="${SCRIPT_DIR}/../service-files/systemd"

if [ -f "${SERVICE_DIR}/claude-agentapi.service" ]; then
  sudo cp "${SERVICE_DIR}/claude-agentapi.service" /etc/systemd/system/
  sudo cp "${SERVICE_DIR}/claude-orchestrator.service" /etc/systemd/system/
  sudo systemctl daemon-reload
fi

echo "=== Phase 10: Authenticate Claude Code ==="
echo ">>> Run: sudo -u claude-agent claude auth login"
echo ">>> Authenticate in your browser."
read -p "Press Enter after authenticating..."

echo "=== Phase 11: Install Orchestrator (claude-code-by-agents) ==="
if ! command -v deno &>/dev/null; then
  curl -fsSL https://deno.land/install.sh | sudo -u claude-agent sh
  echo 'export PATH="/home/claude-agent/.deno/bin:$PATH"' | sudo -u claude-agent tee -a /home/claude-agent/.bashrc > /dev/null
fi

if [ ! -d /opt/claude-code-by-agents ]; then
  sudo git clone https://github.com/baryhuang/claude-code-by-agents.git /opt/claude-code-by-agents
  sudo chown -R claude-agent:claude-agent /opt/claude-code-by-agents
  cd /opt/claude-code-by-agents/backend
  sudo -u claude-agent /home/claude-agent/.deno/bin/deno install
fi

echo "=== Phase 12: GPU Detection + Local Ollama ==="
SHARED_MODULE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../shared" 2>/dev/null && pwd)/ollama-gpu-detect.sh"
if [ -f "$SHARED_MODULE" ]; then
  source "$SHARED_MODULE"
  install_ollama_with_model
else
  echo "WARNING: ollama-gpu-detect.sh not found. Skipping local Ollama."
fi

echo "=== Phase 12b: Existing LAN Ollama Configuration ==="
echo ""
echo "============================================"
echo "  Dr Paper detected an existing Ollama"
echo "  instance on your LAN."
echo "============================================"
echo ""
echo "We'll configure Dr Paper to use your existing Ollama server"
echo "as a shared resource alongside any local GPU installs."
echo ""
echo "What is the hostname or IP of your existing Ollama server?"
echo ""
echo "  Default: 192.168.10.242 (press Enter to accept)"
echo ""
echo "  Options:"
echo "    - Press Enter to use 192.168.10.242"
echo "    - Tailscale hostname (e.g., 'swoops-ollama-server')"
echo "      Best option: works across networks, encrypted, stable"
echo "    - Different LAN IP address"
echo "    - 'skip' to configure later"
echo ""
read -p "Ollama server hostname/IP [192.168.10.242]: " OLLAMA_LAN_HOST
OLLAMA_LAN_HOST="${OLLAMA_LAN_HOST:-192.168.10.242}"

if [ -n "$OLLAMA_LAN_HOST" ] && [ "$OLLAMA_LAN_HOST" != "skip" ]; then
  OLLAMA_LAN_PORT=11434
  OLLAMA_LAN_URL="http://${OLLAMA_LAN_HOST}:${OLLAMA_LAN_PORT}"

  echo ""
  echo "Testing connection to ${OLLAMA_LAN_URL}..."
  if curl -s --connect-timeout 5 "${OLLAMA_LAN_URL}/api/tags" &>/dev/null; then
    echo "  [OK] Connected! Listing available models:"
    curl -s "${OLLAMA_LAN_URL}/api/tags" | jq -r '.models[]?.name // empty' 2>/dev/null | while read -r model; do
      echo "    - ${model}"
    done
    LAN_OLLAMA_REACHABLE=1
  else
    echo "  [FAIL] Could not connect to ${OLLAMA_LAN_URL}"
    echo ""
    echo "  This usually means Ollama is bound to localhost only."
    echo "  To fix this on the Ollama server, do ONE of these:"
    echo ""
    echo "  Option A: Set the environment variable (recommended)"
    echo "    On the Ollama server, edit the systemd service or shell profile:"
    echo "      export OLLAMA_HOST=0.0.0.0"
    echo "    Then restart Ollama:"
    echo "      sudo systemctl restart ollama"
    echo ""
    echo "  Option B: If Ollama is running via systemd:"
    echo "    sudo systemctl edit ollama"
    echo "    Add these lines:"
    echo "      [Service]"
    echo "      Environment=\"OLLAMA_HOST=0.0.0.0\""
    echo "    Save, then: sudo systemctl restart ollama"
    echo ""
    echo "  Option C: If on Tailscale, make sure both machines are on"
    echo "    the same Tailnet. Install Tailscale on the Ollama server:"
    echo "      curl -fsSL https://tailscale.com/install.sh | sh"
    echo "      sudo tailscale up --hostname swoops-ollama"
    echo "    Then set OLLAMA_HOST=0.0.0.0 and restart."
    echo ""
    read -p "Fix it now and press Enter to re-test, or type 'skip': " RETRY
    if [ "$RETRY" != "skip" ]; then
      if curl -s --connect-timeout 5 "${OLLAMA_LAN_URL}/api/tags" &>/dev/null; then
        echo "  [OK] Connected!"
        LAN_OLLAMA_REACHABLE=1
      else
        echo "  [FAIL] Still can't connect. You can configure this later."
        LAN_OLLAMA_REACHABLE=0
      fi
    else
      LAN_OLLAMA_REACHABLE=0
    fi
  fi

  # Save LAN Ollama config
  if [ "${LAN_OLLAMA_REACHABLE:-0}" = "1" ]; then
    sudo mkdir -p /etc/claude
    echo "OLLAMA_LAN_URL=${OLLAMA_LAN_URL}" | sudo tee /etc/claude/ollama-lan.conf > /dev/null
    echo "OLLAMA_LAN_HOST=${OLLAMA_LAN_HOST}" | sudo tee -a /etc/claude/ollama-lan.conf > /dev/null
    sudo chmod 644 /etc/claude/ollama-lan.conf
    echo ""
    echo "  LAN Ollama configured: ${OLLAMA_LAN_URL}"
    echo "  Config saved to /etc/claude/ollama-lan.conf"
    echo ""
    echo "  To use the LAN Ollama from any machine:"
    echo "    export OLLAMA_HOST=${OLLAMA_LAN_HOST}:${OLLAMA_LAN_PORT}"
    echo "    ollama run <model>"
    echo ""
    echo "  Or point tools directly at: ${OLLAMA_LAN_URL}"
  fi
else
  echo "  Skipping LAN Ollama configuration. You can set this up later by"
  echo "  creating /etc/claude/ollama-lan.conf with:"
  echo "    OLLAMA_LAN_URL=http://<host>:11434"
fi

echo "=== Phase 13: Start Services ==="
sudo systemctl enable --now claude-agentapi.service
sudo systemctl enable --now claude-orchestrator.service

echo ""
echo "============================================"
echo "  Dr Paper is ONLINE"
echo "============================================"
echo ""
echo "Services:"
echo "  - icecc-scheduler:   $(systemctl is-active icecc-scheduler 2>/dev/null || echo 'check manually')"
echo "  - claude-agentapi:   $(systemctl is-active claude-agentapi 2>/dev/null || echo 'check manually')"
echo "  - claude-orchestr.:  $(systemctl is-active claude-orchestrator 2>/dev/null || echo 'check manually')"
if [ "$OLLAMA_INSTALLED" = "1" ]; then
echo "  - Ollama (local):    ${OLLAMA_MODEL}"
fi
if [ "${LAN_OLLAMA_REACHABLE:-0}" = "1" ]; then
echo "  - Ollama (LAN):      ${OLLAMA_LAN_URL}"
fi
echo ""
echo "Next:"
echo "  1. Open http://dr-paper:8080 in a browser"
echo "  2. Deploy agents on other machines"
echo "  3. Register them in Dr Paper's web UI"
