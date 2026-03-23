#!/bin/bash
# =============================================================================
# The Right Wire — Cron Scheduler
#
# Pure bash cron loop. Checks time every 60s and fires HTTP GET requests
# to the-right-wire.com API endpoints on schedule.
#
# Environment (from /etc/wire-cron/env):
#   WIRE_BASE_URL   — base URL (https://the-right-wire.com)
#   CRON_SECRET     — Bearer token for cron endpoints
#
# All times are UTC. Logging goes to stdout (journalctl via systemd).
# =============================================================================

set -uo pipefail

# Load environment
if [ -f /etc/wire-cron/env ]; then
  source /etc/wire-cron/env
fi

WIRE_BASE_URL="${WIRE_BASE_URL:-https://the-right-wire.com}"
CRON_SECRET="${CRON_SECRET:?CRON_SECRET must be set in /etc/wire-cron/env}"

LOG_PREFIX="[wire-cron]"

# ─── Helper: fire a cron endpoint ───────────────────────────────────────────

fire() {
  local path="$1"
  local url="${WIRE_BASE_URL}${path}"
  echo "${LOG_PREFIX} $(date -u '+%Y-%m-%d %H:%M:%S UTC') FIRE ${path}"

  local http_code
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 10 \
    --max-time 300 \
    -H "Authorization: Bearer ${CRON_SECRET}" \
    "${url}" 2>/dev/null) || true

  if [ "$http_code" = "200" ]; then
    echo "${LOG_PREFIX} $(date -u '+%Y-%m-%d %H:%M:%S UTC') OK   ${path} -> ${http_code}"
  else
    echo "${LOG_PREFIX} $(date -u '+%Y-%m-%d %H:%M:%S UTC') FAIL ${path} -> ${http_code}"
  fi
}

# Fire in background so multiple jobs at the same minute don't block each other
fire_bg() {
  fire "$1" &
}

# ─── Main loop ──────────────────────────────────────────────────────────────

echo "${LOG_PREFIX} Starting cron scheduler"
echo "${LOG_PREFIX} Target: ${WIRE_BASE_URL}"
echo "${LOG_PREFIX} PID: $$"

while true; do
  # Get current UTC time components
  HOUR=$(date -u '+%-H')     # 0-23, no leading zero
  MIN=$(date -u '+%-M')      # 0-59, no leading zero
  DOW=$(date -u '+%u')       # 1=Mon, 7=Sun

  # ── Every 30 minutes: WIRE Hot Takes ──
  if [ "$MIN" -eq 0 ] || [ "$MIN" -eq 30 ]; then
    fire_bg "/api/cron/wire-hot-takes"
  fi

  # ── Every 2 hours (on the hour): Scrape X (via Wraith) + RSS (via Vercel) ──
  if [ "$MIN" -eq 0 ] && [ $(( HOUR % 2 )) -eq 0 ]; then
    # X scrape runs locally via Wraith Enterprise (parallel, ~60s)
    /opt/wire-cron/wraith-scraper.sh &
    # RSS scrape still hits the Vercel endpoint
    fire_bg "/api/cron/fetch-posts?phase=rss"
  fi

  # ── 02:00 UTC (9pm EST prev day): WIRE Evening Recap ──
  if [ "$HOUR" -eq 2 ] && [ "$MIN" -eq 0 ]; then
    fire_bg "/api/cron/wire-briefing?type=evening"
  fi

  # ── 11:00 UTC (6am EST): Intelligence Brief ──
  if [ "$HOUR" -eq 11 ] && [ "$MIN" -eq 0 ]; then
    fire_bg "/api/cron/intelligence-brief"
  fi

  # ── 12:00 UTC (7am EST): Daily Digest + WIRE Morning ──
  if [ "$HOUR" -eq 12 ] && [ "$MIN" -eq 0 ]; then
    fire_bg "/api/cron/daily-digest"
    fire_bg "/api/cron/wire-briefing?type=morning"
  fi

  # ── 17:00 UTC (12pm EST): Telegram + X Thread ──
  if [ "$HOUR" -eq 17 ] && [ "$MIN" -eq 0 ]; then
    fire_bg "/api/cron/telegram-distribute"
    fire_bg "/api/cron/x-thread"
  fi

  # ── Monday-only jobs ──
  if [ "$DOW" -eq 1 ]; then
    # 00:00 UTC (Sun midnight EST): WIRE Column Draft
    if [ "$HOUR" -eq 0 ] && [ "$MIN" -eq 0 ]; then
      fire_bg "/api/cron/wire-column"
    fi

    # 12:00 UTC (7am EST): WIRE Column Publish
    if [ "$HOUR" -eq 12 ] && [ "$MIN" -eq 0 ]; then
      fire_bg "/api/cron/wire-column-publish"
    fi

    # 13:00 UTC (8am EST): Weekly Newsletter
    if [ "$HOUR" -eq 13 ] && [ "$MIN" -eq 0 ]; then
      fire_bg "/api/cron/weekly-newsletter"
    fi
  fi

  # Wait for background jobs to finish (don't pile up)
  wait

  # Sleep until the next minute boundary
  SECS_INTO_MIN=$(date -u '+%-S')
  SLEEP_SECS=$(( 60 - SECS_INTO_MIN ))
  sleep "${SLEEP_SECS}"
done
