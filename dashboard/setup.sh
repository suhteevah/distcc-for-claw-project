#!/bin/bash
# =============================================================================
# Dashboard Setup Script
# Run on the CNC server to install and start the life dashboard
# Exposes it publicly via Tailscale Funnel
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="/opt/dashboard"
SERVICE_NAME="life-dashboard"
PORT=8888

echo "=== Life Dashboard Setup ==="

# 1. Copy files
echo "[1/4] Installing dashboard to ${INSTALL_DIR}..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp "$SCRIPT_DIR/server.ts" "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR/index.html" "$INSTALL_DIR/"

# Preserve existing config if present
if [ ! -f "$INSTALL_DIR/dashboard.json" ]; then
  echo '{}' | sudo tee "$INSTALL_DIR/dashboard.json" > /dev/null
  echo "  Created default dashboard.json (configure via Settings in the UI)"
fi

# 2. Create systemd service
echo "[2/4] Creating systemd service..."
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null <<EOF
[Unit]
Description=Life Dashboard
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${INSTALL_DIR}
ExecStart=$(which deno) run --allow-net --allow-read --allow-write --allow-run --allow-env --allow-sys ${INSTALL_DIR}/server.ts
Environment=DASHBOARD_PORT=${PORT}
Environment=DASHBOARD_CONFIG=${INSTALL_DIR}/dashboard.json
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"
echo "  Service started: systemctl status ${SERVICE_NAME}"

# 3. Configure Tailscale Funnel
echo "[3/4] Setting up Tailscale Funnel on port ${PORT}..."
if command -v tailscale &>/dev/null; then
  # Serve locally first
  tailscale serve --bg "${PORT}" 2>/dev/null || true
  # Enable Funnel for public access
  tailscale funnel --bg "${PORT}" 2>/dev/null || true
  echo "  Funnel enabled. Dashboard accessible at: https://$(tailscale status --self --json 2>/dev/null | grep -o '"DNSName":"[^"]*"' | cut -d'"' -f4 | sed 's/\.$//')"
else
  echo "  WARNING: Tailscale not found. Dashboard only accessible on LAN at http://$(hostname):${PORT}"
fi

# 4. Firewall rule (if firewalld is running)
echo "[4/4] Configuring firewall..."
if systemctl is-active --quiet firewalld 2>/dev/null; then
  sudo firewall-cmd --permanent --add-port="${PORT}/tcp" 2>/dev/null || true
  sudo firewall-cmd --reload 2>/dev/null || true
  echo "  Firewall: port ${PORT} opened"
else
  echo "  Firewall: not running, skipping"
fi

echo ""
echo "=== Setup Complete ==="
echo "Local:  http://localhost:${PORT}"
echo "LAN:    http://$(hostname):${PORT}"
echo "Public: Check 'tailscale funnel status' for your public URL"
echo ""
echo "To configure weather, open the dashboard and click Settings."
echo "You'll need a free OpenWeatherMap API key: https://openweathermap.org/api"
