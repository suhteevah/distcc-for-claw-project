# Client Dashboard

Generates client-facing reports (weekly/monthly), tracks SEO performance via cross-agent calls, and maintains client health scores. Uses LLM to turn raw metrics into readable narratives.

## Port: 8006
## LLM Tier: fast

## Capabilities
- `weekly_report` — Generate LLM-powered weekly performance narrative
- `monthly_report` — Generate comprehensive monthly summary
- `seo_tracking` — Fetch SEO audit data from SEO Auditor agent (HTTP)
- `client_health` — Compute composite health score for a client

## API Endpoints

### POST /report/weekly
Generate a weekly report for a client.
- **Request:** `{ "client_id": "string" }`
- **Response:** `{ "report": "string", "period": "string", "metrics": {...} }`

### POST /report/monthly
Generate a monthly report for a client.
- **Request:** `{ "client_id": "string" }`
- **Response:** `{ "report": "string", "period": "string", "metrics": {...} }`

### GET /clients
List all registered clients.
- **Response:** `[{ "id": "string", "name": "string", "health_score": f64 }, ...]`

### POST /clients
Register a new client.
- **Request:** `{ "name": "string", "website": "string" }`
- **Response:** `{ "id": "string", "name": "string" }`

### GET /clients/:id
Get details for a specific client.
- **Response:** `{ "id": "string", "name": "string", "website": "string", "health_score": f64, "history": [...] }`

### POST /seo/track
Trigger an SEO tracking update for a client (calls SEO Auditor).
- **Request:** `{ "client_id": "string", "url": "string" }`
- **Response:** `{ "audit_result": {...}, "tracked": true }`

## Task Types
- `weekly_report` — Pulled from Core task queue. Generates LLM-powered narrative report for the specified client.
- `monthly_report` — Pulled from Core task queue. Generates comprehensive monthly summary.
- `seo_tracking` — Cross-agent HTTP call to `seo-auditor` to fetch fresh audit data, stored in client profile.
- `client_health` — Computes a composite health score from SEO trends, report history, and service metrics.

## Dependencies
- `openclaw-sdk` (workspace) — Agent SDK, task queue, LLM client
- `axum` (workspace) — HTTP server
- `tokio` (workspace) — Async runtime
- `reqwest` (workspace) — HTTP client for cross-agent calls
- `serde` / `serde_json` (workspace) — Serialization
- `tracing` (workspace) — Structured logging
- `chrono` (workspace) — Date/time handling
- `anyhow` (workspace) — Error handling
- `async-trait` (workspace) — Async trait support
- `dashmap` 6 — Concurrent in-memory client store

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | `client-dashboard` |
| `AGENT_PORT` | `8006` |
| `AGENT_CAPABILITIES` | `weekly_report,monthly_report,seo_tracking,client_health` |
| `LLM_TIER` | `fast` |
| `MAX_CONCURRENT_TASKS` | `2` |
| `LOG_LEVEL` | `info` |
