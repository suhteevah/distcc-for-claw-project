#!/bin/bash
# =============================================================================
# The Right Wire — Wraith Enterprise Scraper
#
# Scrapes all active X/Twitter sources via Wraith Browser's swarm API,
# then pushes results to Supabase. Runs on the CNC box where Wraith is local.
#
# Environment (from /etc/wire-cron/env):
#   WRAITH_API_URL  — Wraith Enterprise API (http://localhost:8090/api/v1)
#   WRAITH_USER     — Wraith auth username
#   WRAITH_PASS     — Wraith auth password
#   SUPABASE_URL    — Supabase project URL
#   SUPABASE_KEY    — Supabase publishable key (for reading sources)
#   SUPABASE_SECRET — Supabase secret key (for writing posts)
#   CRON_SECRET     — Not used here, but kept in env for wire-cron.sh
#
# Usage: ./wraith-scraper.sh [--phase x|rss|all]
# =============================================================================

set -uo pipefail

# Load environment
if [ -f /etc/wire-cron/env ]; then
  source /etc/wire-cron/env
fi

WRAITH_API="${WRAITH_API_URL:-http://localhost:8090/api/v1}"
SUPABASE_URL="${SUPABASE_URL:-https://acrkhojoxeutwmwrpkpi.supabase.co}"
SUPABASE_KEY="${SUPABASE_KEY:-sb_publishable_GZ65hRYWgBIEoYcscaRHQw_fVc1kxxJ}"
SUPABASE_SECRET="${SUPABASE_SECRET:?SUPABASE_SECRET must be set}"
WRAITH_USER="${WRAITH_USER:?WRAITH_USER must be set}"
WRAITH_PASS="${WRAITH_PASS:?WRAITH_PASS must be set}"

LOG="[wraith-scraper]"
PHASE="${1:---phase}"
PHASE_VAL="${2:-all}"
if [ "$PHASE" = "--phase" ]; then
  PHASE_VAL="${PHASE_VAL}"
else
  PHASE_VAL="all"
fi

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# ─── Step 1: Authenticate with Wraith ──────────────────────────────────────

echo "$LOG Authenticating with Wraith Enterprise..."
WRAITH_TOKEN=$(curl -s -X POST "${WRAITH_API}/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${WRAITH_USER}\",\"password\":\"${WRAITH_PASS}\"}" \
  | jq -r '.token // .access_token // empty')

if [ -z "$WRAITH_TOKEN" ]; then
  echo "$LOG FATAL: Failed to authenticate with Wraith"
  exit 1
fi
echo "$LOG Authenticated."

# ─── Step 2: Fetch active sources from Supabase ───────────────────────────

echo "$LOG Fetching active sources from Supabase..."
SOURCES=$(curl -s "${SUPABASE_URL}/rest/v1/curated_sources?select=x_handle,display_name,category&is_active=eq.true" \
  -H "apikey: ${SUPABASE_KEY}")

SOURCE_COUNT=$(echo "$SOURCES" | jq length)
echo "$LOG Found ${SOURCE_COUNT} active sources"

if [ "$SOURCE_COUNT" -eq 0 ]; then
  echo "$LOG No active sources. Exiting."
  exit 0
fi

# ─── Step 3: Build URLs for swarm fan-out ──────────────────────────────────

echo "$LOG Building swarm fan-out request..."
URLS=$(echo "$SOURCES" | jq -r '.[].x_handle' | while read -r handle; do
  echo "https://x.com/${handle}"
done | jq -R -s 'split("\n") | map(select(length > 0))')

# ─── Step 4: Launch swarm fan-out ──────────────────────────────────────────

echo "$LOG Launching swarm fan-out for ${SOURCE_COUNT} URLs..."
SWARM_RESPONSE=$(curl -s -X POST "${WRAITH_API}/swarm/fan-out" \
  -H "Authorization: Bearer ${WRAITH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"urls\": ${URLS}, \"max_concurrent\": 12}")

SWARM_ID=$(echo "$SWARM_RESPONSE" | jq -r '.id // .swarm_id // .job_id // empty')

if [ -z "$SWARM_ID" ]; then
  echo "$LOG FATAL: Failed to launch swarm. Response: ${SWARM_RESPONSE}"
  exit 1
fi
echo "$LOG Swarm launched: ${SWARM_ID}"

# ─── Step 5: Poll for completion ──────────────────────────────────────────

echo "$LOG Waiting for swarm to complete..."
MAX_WAIT=180  # 3 minutes max
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  STATUS=$(curl -s "${WRAITH_API}/swarm/${SWARM_ID}" \
    -H "Authorization: Bearer ${WRAITH_TOKEN}" \
    | jq -r '.status // "unknown"')

  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "done" ] || [ "$STATUS" = "finished" ]; then
    echo "$LOG Swarm completed in ${ELAPSED}s"
    break
  elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
    echo "$LOG FATAL: Swarm failed. Status: ${STATUS}"
    exit 1
  fi

  sleep 5
  ELAPSED=$((ELAPSED + 5))
  echo "$LOG Waiting... (${ELAPSED}s, status: ${STATUS})"
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
  echo "$LOG WARNING: Swarm timed out after ${MAX_WAIT}s. Proceeding with partial results."
fi

# ─── Step 6: Extract tweets from each session ────────────────────────────

echo "$LOG Collecting results..."
RESULTS=$(curl -s "${WRAITH_API}/swarm/${SWARM_ID}/results" \
  -H "Authorization: Bearer ${WRAITH_TOKEN}")

# The results should contain session IDs for each URL
SESSION_IDS=$(echo "$RESULTS" | jq -r '.[].session_id // empty' 2>/dev/null || \
  echo "$RESULTS" | jq -r '.results[].session_id // empty' 2>/dev/null || \
  echo "$RESULTS" | jq -r 'keys[]' 2>/dev/null)

TOTAL_TWEETS=0
ALL_POSTS="[]"

# JS extraction script for tweet data from x.com DOM
read -r -d '' EXTRACT_JS << 'JSEOF' || true
var out='';var arts=document.querySelectorAll('article');for(var i=0;i<Math.min(arts.length,10);i++){var a=arts[i];var tt=a.querySelector('[data-testid="tweetText"]');var te=a.querySelector('time');var av=a.querySelector('img[src*="profile_images"]');var ls=a.querySelectorAll('a');var sid='';for(var j=0;j<ls.length;j++){var h=ls[j].href||'';if(h.indexOf('/status/')>-1){var p=h.split('/status/');sid=p[1]?p[1].split('?')[0].split('/')[0]:'';break}}if(tt&&sid){out+=(out?'|||':'')+'{'+('"id":"'+sid+'",')+'"text":"'+tt.innerText.substring(0,500).replace(/"/g,'\\"').replace(/\n/g,' ')+'",'+('"time":"'+(te?te.getAttribute('datetime'):'')+'",')+'"avatar":"'+(av?av.src.replace(/"/g,'\\"'):'')+'"'+'}'}}('['+out+']')
JSEOF

# For each source, extract tweets via eval-js on its session
echo "$SOURCES" | jq -c '.[]' | while read -r source; do
  HANDLE=$(echo "$source" | jq -r '.x_handle')
  DISPLAY=$(echo "$source" | jq -r '.display_name')
  CATEGORY=$(echo "$source" | jq -r '.category')

  # Create a session and navigate to the profile
  SESSION=$(curl -s -X POST "${WRAITH_API}/sessions" \
    -H "Authorization: Bearer ${WRAITH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"engine": "cdp"}' | jq -r '.id // .session_id // empty')

  if [ -z "$SESSION" ]; then
    echo "$LOG SKIP @${HANDLE}: failed to create session"
    continue
  fi

  # Navigate to profile
  curl -s -X POST "${WRAITH_API}/sessions/${SESSION}/navigate" \
    -H "Authorization: Bearer ${WRAITH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://x.com/${HANDLE}\"}" > /dev/null

  # Wait for page to render
  sleep 3

  # Extract tweets via JS
  TWEET_JSON=$(curl -s -X POST "${WRAITH_API}/sessions/${SESSION}/eval-js" \
    -H "Authorization: Bearer ${WRAITH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"code\": $(echo "$EXTRACT_JS" | jq -Rs .)}" \
    | jq -r '.result // empty')

  if [ -z "$TWEET_JSON" ] || [ "$TWEET_JSON" = "[]" ] || [ "$TWEET_JSON" = "null" ]; then
    echo "$LOG SKIP @${HANDLE}: no tweets extracted"
    continue
  fi

  # Parse tweets and build Supabase upsert payload
  TWEET_COUNT=$(echo "$TWEET_JSON" | jq length 2>/dev/null || echo 0)
  echo "$LOG OK   @${HANDLE}: ${TWEET_COUNT} tweets"

  # Build posts array for this source
  POSTS=$(echo "$TWEET_JSON" | jq -c --arg handle "$HANDLE" --arg display "$DISPLAY" --arg cat "$CATEGORY" '
    [.[] | select(.id != "" and .text != "") | {
      source: "x",
      x_tweet_id: .id,
      x_author_handle: $handle,
      x_author_name: $display,
      x_author_avatar: (if .avatar != "" then .avatar else null end),
      content: .text,
      media_urls: [],
      video_url: null,
      external_url: ("https://x.com/" + $handle + "/status/" + .id),
      category: $cat,
      created_at: (if .time != "" then .time else null end)
    }]')

  # Upsert to Supabase
  if [ "$POSTS" != "[]" ] && [ "$POSTS" != "null" ]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -X POST "${SUPABASE_URL}/rest/v1/posts?on_conflict=x_tweet_id" \
      -H "apikey: ${SUPABASE_KEY}" \
      -H "Authorization: Bearer ${SUPABASE_SECRET}" \
      -H "Content-Type: application/json" \
      -H "Prefer: resolution=merge-duplicates" \
      -d "$POSTS")

    if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
      TOTAL_TWEETS=$((TOTAL_TWEETS + TWEET_COUNT))
    else
      echo "$LOG WARN @${HANDLE}: Supabase upsert returned ${HTTP_CODE}"
    fi
  fi

done

echo "$LOG Complete. Total tweets upserted: ${TOTAL_TWEETS}"
