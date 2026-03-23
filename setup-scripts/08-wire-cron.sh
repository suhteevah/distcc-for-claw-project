#!/bin/bash
set -euo pipefail

# =============================================================================
# The Right Wire - Cron Scheduler Setup
# Run this on: arch-orchestrator
# Role: Fires HTTP GET requests to the-right-wire.com/api/cron/* on schedule
# Replaces: GitHub Actions cron workflows (banned)
# =============================================================================

echo "=== Wire Cron Scheduler Setup ==="

# Create directories
sudo mkdir -p /opt/wire-cron
sudo mkdir -p /etc/wire-cron
sudo mkdir -p /var/log/wire-cron

# Write env file
if [ ! -f /etc/wire-cron/env ]; then
  cat <<'ENVEOF' | sudo tee /etc/wire-cron/env > /dev/null
WIRE_BASE_URL=https://the-right-wire.com
CRON_SECRET=7685642082472675f4542edf9d4d0971d56aa21d9196968048fa924c3f13165f

# Wraith Enterprise (local on CNC box)
WRAITH_API_URL=http://localhost:8090/api/v1
WRAITH_USER=changeme
WRAITH_PASS=changeme

# Supabase (for Wraith scraper to push posts directly)
SUPABASE_URL=https://acrkhojoxeutwmwrpkpi.supabase.co
SUPABASE_KEY=sb_publishable_GZ65hRYWgBIEoYcscaRHQw_fVc1kxxJ
SUPABASE_SECRET=sb_secret_5q7i5WmGVXJ6h0hl_lkpUw_Qc5Asocc
ENVEOF
  sudo chmod 600 /etc/wire-cron/env
  echo "Environment file created at /etc/wire-cron/env"
else
  echo "Environment file already exists"
fi

# Copy the cron + scraper scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sudo cp "${SCRIPT_DIR}/../wire-cron/wire-cron.sh" /opt/wire-cron/wire-cron.sh
sudo cp "${SCRIPT_DIR}/../wire-cron/wraith-scraper.sh" /opt/wire-cron/wraith-scraper.sh
sudo chmod +x /opt/wire-cron/wire-cron.sh
sudo chmod +x /opt/wire-cron/wraith-scraper.sh

# Install systemd service
sudo cp "${SCRIPT_DIR}/../service-files/systemd/wire-cron.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now wire-cron.service

echo ""
echo "=========================================="
echo "  Wire Cron Scheduler Setup Complete"
echo "=========================================="
echo ""
echo "Service status: $(systemctl is-active wire-cron)"
echo "View logs:      journalctl -u wire-cron -f"
echo "Restart:        sudo systemctl restart wire-cron"
echo ""
echo "Cron jobs configured:"
echo "  - Scrape X:           every 2h"
echo "  - Scrape RSS:         every 2h"
echo "  - Daily Digest:       12:00 UTC (7am EST)"
echo "  - Intelligence Brief: 11:00 UTC (6am EST)"
echo "  - Weekly Newsletter:  Mon 13:00 UTC (8am EST)"
echo "  - WIRE Morning:       12:00 UTC (7am EST)"
echo "  - WIRE Evening:       02:00 UTC (9pm EST prev day)"
echo "  - WIRE Hot Takes:     every 30min"
echo "  - WIRE Column Draft:  Mon 00:00 UTC (Sun midnight EST)"
echo "  - WIRE Column Publish:Mon 12:00 UTC (7am EST)"
echo "  - Telegram Distribute:17:00 UTC (12pm EST)"
echo "  - X Thread:           17:00 UTC (12pm EST)"
