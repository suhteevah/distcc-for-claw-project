# Job Hunter

Job application pipeline agent. Scores resume matches, generates tailored cover letters, tracks submissions, and handles Upwork proposal submission (stubbed pending browser automation port).

## Port: 8005
## LLM Tier: heavy (cover letters, resume matching) / fast (job scanning)

## Capabilities
`job_scan`, `resume_match`, `cover_letter`, `application_track`, `upwork_submit`

## API Endpoints

### `POST /submit`
Submit a single Upwork proposal. Currently returns `pending_implementation` — browser automation is not yet ported.

**Request:**
```json
{
  "job_url": "https://www.upwork.com/jobs/~01234567890",
  "cover_letter": "Your project caught my eye because...",
  "bid_amount": 5000.0,
  "bid_type": "fixed"
}
```

**Response:**
```json
{
  "status": "pending_implementation",
  "job_url": "https://www.upwork.com/jobs/~01234567890",
  "bid_amount": 5000.0,
  "bid_type": "fixed",
  "message": "Browser automation not yet ported to Rust",
  "timestamp": "2026-03-14T12:00:00Z"
}
```

### `POST /bulk_submit`
Submit multiple proposals at once. Same stub behavior as `/submit`.

**Request:**
```json
{
  "proposals": [
    { "job_url": "...", "cover_letter": "...", "bid_amount": 5000.0, "bid_type": "fixed" }
  ],
  "variant": "standard"
}
```

### `POST /cover-letter`
Generate a tailored cover letter using LLM.

**Request:**
```json
{
  "job_description": "We need a React developer to build...",
  "resume": "Matt Gates — 5+ years full-stack development...",
  "tone": "professional yet personable",
  "highlights": ["Built 3 e-commerce sites with Next.js", "Local SEO expertise"]
}
```

**Response:**
```json
{
  "status": "completed",
  "cover_letter": "Your product catalog challenge maps directly to...",
  "generated_at": "2026-03-14T12:00:00Z"
}
```

### `POST /resume-match`
Score how well a resume matches a job description.

**Request:**
```json
{
  "job_description": "Senior React Developer with e-commerce experience...",
  "resume": "Matt Gates — Ridge Cell Repair LLC..."
}
```

**Response:**
```json
{
  "match_score": 78,
  "analysis": "Strong match on web development and React experience...",
  "strengths": ["5+ years React experience", "E-commerce portfolio"],
  "gaps": ["No enterprise-scale experience mentioned"],
  "recommendations": ["Highlight Shopify integration work", "Add metrics on traffic growth"]
}
```

**Scoring bands:**
| Score | Meaning |
|-------|---------|
| 90-100 | Near-perfect match, exceeds requirements |
| 70-89 | Strong match, meets most requirements |
| 50-69 | Partial match, transferable skills but gaps |
| 30-49 | Weak match, significant skill gaps |
| 0-29 | Poor match, few relevant qualifications |

### `GET /submissions`
List all tracked submissions (in-memory).

### `GET /check-login`
Check Upwork login status. Returns `pending_implementation`.

## Task Types

### `cover_letter`
**Payload:** `{ "job_description": "...", "resume": "...", "tone": "...", "highlights": ["..."] }`

### `resume_match`
**Payload:** `{ "job_description": "...", "resume": "..." }`

### `upwork_submit`
**Payload:** `{ "job_url": "...", "cover_letter": "...", "bid_amount": 5000.0, "bid_type": "fixed" }`
Returns `pending_implementation` status.

### `upwork_bulk_submit`
**Payload:** `{ "proposals": [...], "variant": "standard" }`

### `check_login`
No payload. Returns `pending_implementation`.

## Dependencies
- `openclaw-sdk` (workspace) — agent framework, LLM client, task polling
- `axum` (workspace) — HTTP server
- `reqwest` (workspace) — HTTP client
- `tokio` (workspace) — async runtime (Mutex for submission log)
- `serde` / `serde_json` (workspace) — serialization
- `chrono` (workspace) — timestamps
- `tracing` (workspace) — structured logging

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (default: from env) |
| `AGENT_PORT` | HTTP listen port (default: `8005`) |
| `AGENT_CAPABILITIES` | Comma-separated capability list |
| `OPENCLAW_CORE_URL` | Core API base URL for task polling |
| `LLM_API_KEY` | API key for LLM provider |
| `LLM_BASE_URL` | LLM API base URL |
