#!/bin/bash
set -euo pipefail

# =============================================================================
# First Choice Plastics -- Mac Mini Setup
# Run this on: FCP's Mac Mini (Phase 3 expansion)
# Role: Headless Claude Code agent + icecream worker
#       Can optionally become the icecream scheduler
# =============================================================================

HOSTNAME="fcp-mac-mini"

echo "============================================"
echo "  First Choice Plastics"
echo "  Setting up: ${HOSTNAME} (Mac Mini)"
echo "============================================"

# Homebrew
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew update
brew install node@20 git ripgrep ccache

# Tailscale
brew list --cask tailscale &>/dev/null || brew install --cask tailscale
echo ">>> Open Tailscale.app and authenticate."
echo ">>> Then: sudo tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after authenticated..."

# Icecream
brew install icecream

# Create icecc user
if ! dscl . -read /Users/icecc &>/dev/null 2>&1; then
  sudo dscl . -create /Users/icecc
  sudo dscl . -create /Users/icecc UserShell /usr/bin/false
  ICECC_UID=$(dscl . -list /Users UniqueID | awk '{print $2}' | sort -n | tail -1 | awk '{print $1+1}')
  sudo dscl . -create /Users/icecc UniqueID "$ICECC_UID"
  sudo dscl . -create /Users/icecc PrimaryGroupID 20
  sudo dscl . -create /Users/icecc NFSHomeDirectory /var/empty
fi

# Start iceccd pointing to laptop as scheduler
# (Change to localhost if promoting Mac Mini to scheduler)
sudo iceccd -d -s fcp-laptop -u icecc

# Claude Code
npm install -g @anthropic-ai/claude-code

# AgentAPI
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
sudo curl -fsSL \
  "https://github.com/coder/agentapi/releases/latest/download/agentapi-${OS}-${ARCH_HW}" \
  -o /usr/local/bin/agentapi
sudo chmod +x /usr/local/bin/agentapi

# API Key
echo ""
echo "You need an Anthropic API key: https://console.anthropic.com/"
echo ""
sudo mkdir -p /etc/claude && sudo chmod 700 /etc/claude
if [ ! -f /etc/claude/api-key ]; then
  read -sp "Enter Anthropic API key: " API_KEY
  echo
  echo "ANTHROPIC_API_KEY=${API_KEY}" | sudo tee /etc/claude/api-key > /dev/null
  sudo chmod 600 /etc/claude/api-key
fi

echo ">>> Run: claude auth login"
read -p "Press Enter after authenticating..."

# Start AgentAPI as a background process
# For persistent service, create a launchd plist (see parent deployment for template)
echo "Starting AgentAPI..."
API_KEY_VAL=$(grep ANTHROPIC_API_KEY /etc/claude/api-key | cut -d= -f2)
export ANTHROPIC_API_KEY="$API_KEY_VAL"
nohup agentapi server --type claude --allowed-hosts '*' -- claude \
  --dangerously-skip-permissions \
  --max-budget-usd 10.00 \
  > /tmp/claude-agentapi.log 2>&1 &

echo "=== GPU Detection + Ollama ==="
SHARED_MODULE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../shared" 2>/dev/null && pwd)/ollama-gpu-detect.sh"
if [ -f "$SHARED_MODULE" ]; then
  source "$SHARED_MODULE"
  install_ollama_with_model
else
  echo "WARNING: ollama-gpu-detect.sh not found. Skipping Ollama."
fi

echo ""
echo "============================================"
echo "  FCP Mac Mini ONLINE"
echo "  Hostname: ${HOSTNAME}"
if [ "$OLLAMA_INSTALLED" = "1" ]; then
echo "  Ollama: ${OLLAMA_MODEL}"
fi
echo "============================================"
echo ""
echo "Verify from the laptop:"
echo "  curl http://${HOSTNAME}:3284/status"
echo ""
echo "To make this persistent, create a launchd plist."
echo "To promote to icecream scheduler:"
echo "  brew services start icecc-scheduler"
echo "  Then update other machines to point to ${HOSTNAME}"
