#!/bin/bash
set -euo pipefail

# =============================================================================
# Dr Paper -- Raspberry Pi Setup
# Run this on: Each of Swoop's Raspberry Pis (must be 64-bit)
# Role: Headless Claude Code agent + icecream build worker
# Controlled by: Dr Paper
# =============================================================================

HOSTNAME="${1:-}"
if [ -z "$HOSTNAME" ]; then
  echo "Usage: $0 <hostname>"
  echo "  e.g.: $0 swoop-rpi1"
  exit 1
fi

ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
  echo "ERROR: 32-bit OS detected (${ARCH}). Claude Code requires 64-bit."
  echo "Reflash with 64-bit Raspberry Pi OS and re-run."
  exit 1
fi

echo "=== Setting up ${HOSTNAME} for Dr Paper ==="

sudo apt update && sudo apt upgrade -y
sudo apt install -y git ripgrep build-essential ccache clang curl jq

# Node.js 20
if ! command -v node &>/dev/null || [ "$(node -v | cut -d. -f1 | tr -d v)" -lt 20 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi

# Tailscale
command -v tailscale &>/dev/null || (curl -fsSL https://tailscale.com/install.sh | sh)
sudo systemctl enable --now tailscaled
echo ">>> Run: sudo tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after authenticated..."

# Icecream worker
sudo apt install -y icecc
ICECC_CONF="/etc/default/icecc"
if [ -f "$ICECC_CONF" ]; then
  sudo sed -i 's/^#\?ICECC_SCHEDULER_HOST=.*/ICECC_SCHEDULER_HOST="dr-paper"/' "$ICECC_CONF"
else
  echo 'ICECC_SCHEDULER_HOST="dr-paper"' | sudo tee "$ICECC_CONF"
fi
for svc in icecc-daemon iceccd icecc; do
  if systemctl list-unit-files | grep -q "^${svc}.service"; then
    sudo systemctl enable --now "${svc}.service"
    break
  fi
done

# Toolchain tarball
sudo mkdir -p /opt/icecc-envs
cd /tmp
icecc-create-env --clang /usr/bin/clang /usr/bin/clang++ 2>/dev/null || true
TARBALL=$(ls -t /tmp/*.tar.gz 2>/dev/null | head -1)
if [ -n "$TARBALL" ]; then
  sudo mv "$TARBALL" /opt/icecc-envs/aarch64-clang.tar.gz
  echo ">>> Copy tarball to Dr Paper:"
  echo "    scp /opt/icecc-envs/aarch64-clang.tar.gz dr-paper:/opt/icecc-envs/"
fi

# Claude Code
export DISABLE_AUTOUPDATER=1
sudo npm install -g @anthropic-ai/claude-code

# AgentAPI
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
sudo curl -fsSL \
  "https://github.com/coder/agentapi/releases/latest/download/agentapi-${OS}-${ARCH_HW}" \
  -o /usr/local/bin/agentapi
sudo chmod +x /usr/local/bin/agentapi

# User + API key
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

# Service
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_DIR="${SCRIPT_DIR}/../service-files/systemd"
if [ -f "${SERVICE_DIR}/claude-agentapi.service" ]; then
  sudo cp "${SERVICE_DIR}/claude-agentapi.service" /etc/systemd/system/
  sudo sed -i 's/--max-budget-usd 10.00/--max-budget-usd 5.00/' /etc/systemd/system/claude-agentapi.service
  if ! grep -q "MemoryMax" /etc/systemd/system/claude-agentapi.service; then
    sudo sed -i '/\[Service\]/a MemoryMax=512M' /etc/systemd/system/claude-agentapi.service
  fi
  sudo systemctl daemon-reload
  sudo systemctl enable --now claude-agentapi.service
fi

echo "=== GPU Detection + Local Ollama ==="
SHARED_MODULE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../shared" 2>/dev/null && pwd)/ollama-gpu-detect.sh"
if [ -f "$SHARED_MODULE" ]; then
  source "$SHARED_MODULE"
  install_ollama_with_model
else
  echo "No discrete GPU expected on Pi. Skipping local Ollama."
fi

# LAN Ollama discovery
echo "=== LAN Ollama Discovery ==="
LAN_OLLAMA_REACHABLE=0
if ssh -o ConnectTimeout=3 -o BatchMode=yes dr-paper "cat /etc/claude/ollama-lan.conf" &>/dev/null; then
  eval "$(ssh dr-paper 'cat /etc/claude/ollama-lan.conf' 2>/dev/null)"
  if [ -n "${OLLAMA_LAN_URL:-}" ] && curl -s --connect-timeout 3 "${OLLAMA_LAN_URL}/api/tags" &>/dev/null; then
    echo "  [OK] LAN Ollama: ${OLLAMA_LAN_URL}"
    LAN_OLLAMA_REACHABLE=1
  else
    echo "  LAN Ollama not reachable. Set manually: export OLLAMA_HOST=<server>:11434"
  fi
else
  echo "  Could not reach Dr Paper for LAN Ollama config."
fi

echo ""
echo "============================================"
echo "  ${HOSTNAME} reporting to Dr Paper"
echo "  Arch: $(uname -m) | RAM: $(free -h | awk '/^Mem:/{print $2}')"
if [ "$OLLAMA_INSTALLED" = "1" ]; then
echo "  Ollama (local): ${OLLAMA_MODEL}"
fi
if [ "$LAN_OLLAMA_REACHABLE" = "1" ]; then
echo "  Ollama (LAN):   ${OLLAMA_LAN_URL}"
fi
echo "============================================"
