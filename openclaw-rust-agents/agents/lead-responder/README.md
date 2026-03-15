# Lead Responder

Lead classification and response drafting agent with a human-in-the-loop approval queue. Classifies inbound messages, drafts responses, and queues everything for Matt's review before anything is sent.

## Port: 8002
## LLM Tier: fast

## Capabilities
`lead_classify`, `email_draft`, `upwork_respond`, `inbox_scan`

## API Endpoints

### `POST /classify`
Classify a lead/message into a category.

**Request:**
```json
{
  "email_from": "john@example.com",
  "subject": "Website redesign inquiry",
  "body": "Hi, I found your company through a Google search..."
}
```

**Response:**
```json
{
  "category": "cold_inquiry",
  "confidence": 0.92,
  "reasoning": "Unsolicited inquiry from unknown contact via search"
}
```

**Categories:** `cold_inquiry`, `referral`, `existing_client`, `upwork_opportunity`, `spam`, `newsletter`, `transactional`

### `POST /draft`
Classify a message and draft a response. The draft is queued for approval — never auto-sent.

**Request:**
```json
{
  "email_from": "john@example.com",
  "subject": "Website redesign inquiry",
  "body": "Hi, I found your company...",
  "tone": "professional"
}
```

**Response:**
```json
{
  "approval_id": "550e8400-e29b-41d4-a716-446655440000",
  "category": "cold_inquiry",
  "confidence": 0.92,
  "draft": "Thank you for reaching out...",
  "status": "pending_approval"
}
```

### `POST /upwork`
Draft an Upwork proposal cover letter. Queued for approval.

**Request:**
```json
{
  "job_title": "React Developer for E-commerce Site",
  "job_description": "We need a developer to...",
  "relevant_experience": "Built 3 e-commerce sites...",
  "portfolio_highlights": "Ridge Cell Repair storefront..."
}
```

**Response:**
```json
{
  "approval_id": "...",
  "draft": "Your product catalog challenge is...",
  "status": "pending_approval"
}
```

### `GET /leads/pending`
List all drafts waiting for approval.

**Response:**
```json
{
  "pending": [{ "id": "...", "type": "email_draft", "status": "pending_approval", ... }],
  "count": 3
}
```

### `POST /leads/approve/:id`
Approve a pending draft. Returns 409 if already approved/rejected.

### `POST /leads/reject/:id`
Reject a pending draft. Returns 409 if already approved/rejected.

## Task Types

### `lead_classify`
**Payload:** `{ "email_from": "...", "subject": "...", "body": "..." }`

### `email_draft`
**Payload:** `{ "email_from": "...", "subject": "...", "body": "...", "tone": "professional" }`
Classifies first, then drafts. Result includes `approval_id` and `status: "pending_approval"`.

### `upwork_respond`
**Payload:** `{ "job_title": "...", "job_description": "...", "relevant_experience": "...", "portfolio_highlights": "..." }`

### `inbox_scan`
Placeholder — returns `{ "message": "inbox_scan not yet implemented", "processed": 0 }`.

## Dependencies
- `openclaw-sdk` (workspace) — agent framework, LLM client, task polling
- `axum` (workspace) — HTTP server
- `reqwest` (workspace) — HTTP client
- `dashmap` 6 — lock-free concurrent HashMap for the approval queue
- `uuid` 1 (v4) — unique approval IDs
- `serde` / `serde_json` (workspace) — serialization
- `chrono` (workspace) — timestamps
- `tracing` (workspace) — structured logging

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (default: `lead-responder`) |
| `AGENT_PORT` | HTTP listen port (default: `8002`) |
| `AGENT_CAPABILITIES` | Comma-separated capability list (default: `lead_classify,email_draft,upwork_respond,inbox_scan`) |
| `OPENCLAW_CORE_URL` | Core API base URL for task polling |
| `LLM_API_KEY` | API key for LLM provider |
| `LLM_BASE_URL` | LLM API base URL |
