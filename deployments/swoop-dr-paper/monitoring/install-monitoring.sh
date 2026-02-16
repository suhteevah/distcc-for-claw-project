#!/bin/bash
set -euo pipefail

# Install Dr Paper fleet monitoring
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo cp "${SCRIPT_DIR}/fleet-health-check.sh" /usr/local/bin/fleet-health-check.sh
sudo chmod +x /usr/local/bin/fleet-health-check.sh
sudo touch /var/log/fleet-health.log
sudo chmod 644 /var/log/fleet-health.log

CRON_LINE="*/5 * * * * /usr/local/bin/fleet-health-check.sh >> /var/log/fleet-health.log 2>&1"
(crontab -l 2>/dev/null | grep -v fleet-health-check; echo "$CRON_LINE") | crontab -

echo "Dr Paper monitoring installed."
echo "  Script: /usr/local/bin/fleet-health-check.sh"
echo "  Log:    /var/log/fleet-health.log"
echo "  Cron:   every 5 minutes"
