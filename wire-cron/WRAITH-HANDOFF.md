# Wraith Enterprise — TRW Integration Blocked

## Problem
Wraith Enterprise migrations fail because `pgvector` is not available in the postgres container (`postgres:16-alpine`). Migration `20260320000001_create_extensions.sql` tries to `CREATE EXTENSION vector` and fails. Wraith catches this and marks all migrations as "skipped (error)", which causes auth routes to return `{"error":"database_error"}`.

## Fix Needed
Replace the postgres container image with one that has pgvector:

```bash
# Stop current container
podman stop openclaw-postgres
podman rm openclaw-postgres

# Start with pgvector image
podman run -d --name openclaw-postgres \
  -e POSTGRES_USER=openclaw \
  -e POSTGRES_PASSWORD=openclaw2026cnc \
  -e POSTGRES_DB=openclaw \
  -p 127.0.0.1:5432:5432 \
  --restart=always \
  pgvector/pgvector:pg16

# Then restart Wraith Enterprise — it will run clean migrations
pkill -f wraith-enterprise
cd /opt/openclaw/core/crates/api-server
nohup ./target/release/wraith-enterprise --listen 0.0.0.0:8090 > /var/log/wraith-enterprise.log 2>&1 &
```

NOTE: The schema was dropped during debugging (`DROP SCHEMA public CASCADE`). Wraith will need to run fresh migrations. The WoW economy tables (ah_items, ah_snapshots, ah_prices) were also in that schema — they'll need to be recreated.

## After Fix — Register TRW Account

```bash
curl -X POST http://localhost:8090/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"wire@the-right-wire.com","password":"Wr3B0tKx9mPqL2","org_name":"TRW"}'
```

Then update `/etc/wire-cron/env` on cnc-server:
```
WRAITH_USER=wire@the-right-wire.com
WRAITH_PASS=Wr3B0tKx9mPqL2
```

And restart: `sudo systemctl restart wire-cron`

## What TRW Has Ready
- `/opt/wire-cron/wire-cron.sh` — cron scheduler (running, confirmed working)
- `/opt/wire-cron/wraith-scraper.sh` — parallel scraper via Wraith swarm API
- Wraith API prefix: `/api/v1/`
- Auth: JWT via `/api/v1/auth/login`
- Scraping: `/api/v1/swarm/fan-out`, sessions, eval-js
