#!/bin/bash
set -euo pipefail

# =============================================================================
# First Choice Plastics -- Raspberry Pi Setup
# Run this on: FCP's Raspberry Pi (must be 64-bit)
# Role: Headless Claude Code agent + icecream build worker
# Controlled by: fcp-laptop
# =============================================================================

HOSTNAME="${1:-fcp-rpi}"

ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
  echo "ERROR: 32-bit OS detected (${ARCH}). Claude Code requires 64-bit."
  echo "Reflash with 64-bit Raspberry Pi OS and re-run."
  exit 1
fi

echo "============================================"
echo "  First Choice Plastics"
echo "  Setting up: ${HOSTNAME} (Raspberry Pi)"
echo "============================================"

echo "=== System Update ==="
sudo apt update && sudo apt upgrade -y
sudo apt install -y git ripgrep build-essential ccache clang curl jq

echo "=== Node.js 20 ==="
if ! command -v node &>/dev/null || [ "$(node -v | cut -d. -f1 | tr -d v)" -lt 20 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
echo "Node.js: $(node --version)"

echo "=== Tailscale ==="
command -v tailscale &>/dev/null || (curl -fsSL https://tailscale.com/install.sh | sh)
sudo systemctl enable --now tailscaled
echo ">>> Run: sudo tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after authenticated..."

echo "=== Icecream Worker ==="
sudo apt install -y icecc
ICECC_CONF="/etc/default/icecc"
if [ -f "$ICECC_CONF" ]; then
  sudo sed -i 's/^#\?ICECC_SCHEDULER_HOST=.*/ICECC_SCHEDULER_HOST="fcp-laptop"/' "$ICECC_CONF"
else
  echo 'ICECC_SCHEDULER_HOST="fcp-laptop"' | sudo tee "$ICECC_CONF"
fi
for svc in icecc-daemon iceccd icecc; do
  if systemctl list-unit-files | grep -q "^${svc}.service"; then
    sudo systemctl enable --now "${svc}.service"
    break
  fi
done

echo "=== Claude Code ==="
export DISABLE_AUTOUPDATER=1
sudo npm install -g @anthropic-ai/claude-code

echo "=== AgentAPI ==="
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
sudo curl -fsSL \
  "https://github.com/coder/agentapi/releases/latest/download/agentapi-${OS}-${ARCH_HW}" \
  -o /usr/local/bin/agentapi
sudo chmod +x /usr/local/bin/agentapi

echo "=== Agent User + API Key ==="
if ! id claude-agent &>/dev/null; then
  sudo useradd -r -m -s /bin/bash claude-agent
fi

echo ""
echo "You need an Anthropic API key: https://console.anthropic.com/"
echo ""
sudo mkdir -p /etc/claude && sudo chmod 700 /etc/claude
if [ ! -f /etc/claude/api-key ]; then
  read -sp "Enter Anthropic API key: " API_KEY
  echo
  echo "ANTHROPIC_API_KEY=${API_KEY}" | sudo tee /etc/claude/api-key > /dev/null
  sudo chmod 600 /etc/claude/api-key
  sudo chown claude-agent:claude-agent /etc/claude/api-key
fi

echo ">>> Run: sudo -u claude-agent claude auth login"
read -p "Press Enter after authenticating..."

echo "=== Service Setup ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_DIR="${SCRIPT_DIR}/../service-files/systemd"

if [ -f "${SERVICE_DIR}/claude-agentapi.service" ]; then
  sudo cp "${SERVICE_DIR}/claude-agentapi.service" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable --now claude-agentapi.service
fi

echo "=== GPU Detection + Ollama ==="
SHARED_MODULE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../shared" 2>/dev/null && pwd)/ollama-gpu-detect.sh"
if [ -f "$SHARED_MODULE" ]; then
  source "$SHARED_MODULE"
  install_ollama_with_model
else
  echo "No discrete GPU expected on Pi. Skipping Ollama."
fi

echo ""
echo "============================================"
echo "  FCP Raspberry Pi ONLINE"
echo "  Hostname: ${HOSTNAME}"
echo "  Arch: $(uname -m)"
echo "  RAM: $(free -h | awk '/^Mem:/{print $2}')"
if [ "$OLLAMA_INSTALLED" = "1" ]; then
echo "  Ollama: ${OLLAMA_MODEL}"
fi
echo "============================================"
echo ""
echo "Verify from the laptop:"
echo "  curl http://${HOSTNAME}:3284/status"
