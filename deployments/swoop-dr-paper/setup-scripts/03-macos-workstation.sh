#!/bin/bash
set -euo pipefail

# =============================================================================
# Dr Paper -- macOS Human Workstation Setup
# Run this on: Swoop's MacBook 2 (human at keyboard)
# Role: Interactive Claude Code + icecream build worker
# =============================================================================

HOSTNAME="swoop-macbook2"

echo "=== Setting up ${HOSTNAME} as Swoop's workstation ==="

if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew update
brew install node@20 git ripgrep ccache

# Tailscale
brew list --cask tailscale &>/dev/null || brew install --cask tailscale
echo ">>> Open Tailscale.app, authenticate, then:"
echo ">>> sudo tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after authenticated..."

# Icecream worker
brew install icecream
if ! dscl . -read /Users/icecc &>/dev/null 2>&1; then
  sudo dscl . -create /Users/icecc
  sudo dscl . -create /Users/icecc UserShell /usr/bin/false
  ICECC_UID=$(dscl . -list /Users UniqueID | awk '{print $2}' | sort -n | tail -1 | awk '{print $1+1}')
  sudo dscl . -create /Users/icecc UniqueID "$ICECC_UID"
  sudo dscl . -create /Users/icecc PrimaryGroupID 20
  sudo dscl . -create /Users/icecc NFSHomeDirectory /var/empty
fi

# iceccd launchd service
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHD_DIR="${SCRIPT_DIR}/../service-files/launchd"
if [ -f "${LAUNCHD_DIR}/org.icecc.iceccd.plist" ]; then
  sudo cp "${LAUNCHD_DIR}/org.icecc.iceccd.plist" /Library/LaunchDaemons/
  sudo launchctl load /Library/LaunchDaemons/org.icecc.iceccd.plist
fi

# Claude Code
npm install -g @anthropic-ai/claude-code
claude --version

# Shell profile
PROFILE="${HOME}/.zshrc"
[ -f "${HOME}/.bashrc" ] && [ ! -f "${HOME}/.zshrc" ] && PROFILE="${HOME}/.bashrc"
if ! grep -q "icecc/bin" "$PROFILE" 2>/dev/null; then
  cat >> "$PROFILE" << 'EOF'

# Icecream distributed compilation (Dr Paper cluster)
export PATH=/usr/local/lib/icecc/bin:$PATH
export CCACHE_PREFIX=icecc
EOF
fi

echo ""
echo "============================================"
echo "  ${HOSTNAME} workstation ready"
echo "============================================"
echo ""
echo "Usage: claude       (interactive Claude Code)"
echo "Compile: make -j\$(nproc) CC=icecc CXX=icecc"
