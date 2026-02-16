#!/bin/bash
set -euo pipefail

# =============================================================================
# Dr Paper -- macOS Headless Agent Setup
# Run this on: Swoop's MacBook 1 or iMac
# Role: Headless Claude Code agent + icecream build worker
# Controlled by: Dr Paper (orchestrator)
# =============================================================================

HOSTNAME="${1:-}"
if [ -z "$HOSTNAME" ]; then
  echo "Usage: $0 <hostname>"
  echo "  e.g.: $0 swoop-macbook1"
  echo "  e.g.: $0 swoop-imac"
  exit 1
fi

echo "=== Setting up ${HOSTNAME} for Dr Paper ==="

# Install Homebrew if needed
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "=== Install Dependencies ==="
brew update
brew install node@20 git ripgrep ccache

echo "=== Tailscale ==="
brew list --cask tailscale &>/dev/null || brew install --cask tailscale
echo ">>> Open Tailscale.app and authenticate."
echo ">>> Then: sudo tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after authenticated..."

echo "=== Icecream Worker ==="
brew install icecream

# Create icecc user if needed
if ! dscl . -read /Users/icecc &>/dev/null 2>&1; then
  sudo dscl . -create /Users/icecc
  sudo dscl . -create /Users/icecc UserShell /usr/bin/false
  ICECC_UID=$(dscl . -list /Users UniqueID | awk '{print $2}' | sort -n | tail -1 | awk '{print $1+1}')
  sudo dscl . -create /Users/icecc UniqueID "$ICECC_UID"
  sudo dscl . -create /Users/icecc PrimaryGroupID 20
  sudo dscl . -create /Users/icecc NFSHomeDirectory /var/empty
fi

echo "=== Claude Code ==="
npm install -g @anthropic-ai/claude-code
claude --version

echo "=== AgentAPI ==="
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
sudo curl -fsSL \
  "https://github.com/coder/agentapi/releases/latest/download/agentapi-${OS}-${ARCH_HW}" \
  -o /usr/local/bin/agentapi
sudo chmod +x /usr/local/bin/agentapi

echo "=== API Key ==="
echo ""
echo "You need an Anthropic API key."
echo "Get one at: https://console.anthropic.com/"
echo ""
sudo mkdir -p /etc/claude && sudo chmod 700 /etc/claude
if [ ! -f /etc/claude/api-key ]; then
  read -sp "Enter Anthropic API key: " API_KEY
  echo
  echo "ANTHROPIC_API_KEY=${API_KEY}" | sudo tee /etc/claude/api-key > /dev/null
  sudo chmod 600 /etc/claude/api-key
fi

echo "=== Authenticate Claude Code ==="
echo ">>> Run: claude auth login"
read -p "Press Enter after authenticating..."

echo "=== Install Services ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHD_DIR="${SCRIPT_DIR}/../service-files/launchd"

# iceccd -- point to Dr Paper as scheduler
if [ -f "${LAUNCHD_DIR}/org.icecc.iceccd.plist" ]; then
  sudo cp "${LAUNCHD_DIR}/org.icecc.iceccd.plist" /Library/LaunchDaemons/
  sudo launchctl load /Library/LaunchDaemons/org.icecc.iceccd.plist
fi

# AgentAPI
if [ -f "${LAUNCHD_DIR}/com.claude.agentapi.plist" ]; then
  API_KEY=$(grep ANTHROPIC_API_KEY /etc/claude/api-key | cut -d= -f2)
  sed "s|__ANTHROPIC_API_KEY__|${API_KEY}|g" \
    "${LAUNCHD_DIR}/com.claude.agentapi.plist" > /tmp/com.claude.agentapi.plist
  sudo mv /tmp/com.claude.agentapi.plist ~/Library/LaunchAgents/
  launchctl load ~/Library/LaunchAgents/com.claude.agentapi.plist
fi

echo "=== GPU Detection + Local Ollama ==="
SHARED_MODULE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../shared" 2>/dev/null && pwd)/ollama-gpu-detect.sh"
if [ -f "$SHARED_MODULE" ]; then
  source "$SHARED_MODULE"
  install_ollama_with_model
else
  echo "WARNING: ollama-gpu-detect.sh not found. Skipping local Ollama."
fi

# Check for LAN Ollama (Swoop's existing instance)
echo ""
echo "=== LAN Ollama Discovery ==="
echo "Dr Paper's network has an existing Ollama server."
echo "Checking if it's reachable..."
LAN_OLLAMA_REACHABLE=0

# Try to pull config from Dr Paper orchestrator
if ssh -o ConnectTimeout=3 -o BatchMode=yes dr-paper "cat /etc/claude/ollama-lan.conf" &>/dev/null; then
  eval "$(ssh dr-paper 'cat /etc/claude/ollama-lan.conf' 2>/dev/null)"
  if [ -n "${OLLAMA_LAN_URL:-}" ]; then
    if curl -s --connect-timeout 3 "${OLLAMA_LAN_URL}/api/tags" &>/dev/null; then
      echo "  [OK] LAN Ollama reachable at ${OLLAMA_LAN_URL}"
      LAN_OLLAMA_REACHABLE=1
    else
      echo "  [--] LAN Ollama configured (${OLLAMA_LAN_URL}) but not reachable from here"
    fi
  fi
else
  echo "  Could not pull LAN Ollama config from Dr Paper."
  echo "  You can set it manually later:"
  echo "    export OLLAMA_HOST=<ollama-server>:11434"
fi

echo ""
echo "============================================"
echo "  ${HOSTNAME} reporting to Dr Paper"
echo "============================================"
echo ""
echo "Verify:"
echo "  curl http://localhost:3284/status"
echo "  curl http://${HOSTNAME}:3284/status  (from Dr Paper)"
if [ "$OLLAMA_INSTALLED" = "1" ]; then
echo "  Ollama (local): ${OLLAMA_MODEL}"
fi
if [ "$LAN_OLLAMA_REACHABLE" = "1" ]; then
echo "  Ollama (LAN):   ${OLLAMA_LAN_URL}"
fi
