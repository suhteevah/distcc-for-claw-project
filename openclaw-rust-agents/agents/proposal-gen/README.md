# Proposal Gen

Business proposal and statement of work generation agent. Produces dual-variant Upwork proposals, full SOW documents, and deterministic pricing calculations based on hardcoded service rates.

## Port: 8004
## LLM Tier: heavy

## Capabilities
`upwork_proposal`, `consulting_sow`, `pricing`

## API Endpoints

### `POST /propose`
Generate a dual-variant Upwork proposal.

**Request:**
```json
{
  "job_title": "React Developer for E-commerce Rebuild",
  "job_text": "We need a developer to rebuild our Shopify store...",
  "budget_range": "$5,000-$10,000"
}
```

**Response:**
```json
{
  "job_title": "React Developer for E-commerce Rebuild",
  "conservative_proposal": "Your e-commerce migration is a project I've handled...",
  "aggressive_proposal": "I can have your new storefront live in 3 weeks...",
  "tokens_used": 3200,
  "model": "..."
}
```

The two variants are split by a `---VARIANT_SPLIT---` delimiter in the LLM output.

### `POST /sow`
Generate a full Statement of Work document.

**Request:**
```json
{
  "client_name": "Acme Corp",
  "project_scope": "Full website redesign with SEO migration",
  "deliverables": [
    "Responsive website design (10 pages)",
    "SEO audit and 301 redirect map",
    "Content migration from old CMS"
  ]
}
```

**Response:**
```json
{
  "client_name": "Acme Corp",
  "sow_document": "# STATEMENT OF WORK\n\n## 1. PROJECT OVERVIEW\n...",
  "tokens_used": 4500,
  "model": "..."
}
```

SOW sections: Project Overview, Scope of Work, Deliverables Table, Timeline, Pricing, Terms & Conditions (50/25/25 payment, 2 revision rounds, IP transfer, 30-day cancellation).

### `GET /price`
Calculate pricing based on the hardcoded SERVICE_RATES table. No LLM involved — pure math.

**Request (POST body):**
```json
{
  "scope_description": "Build a React e-commerce website with SEO optimization",
  "complexity": "medium"
}
```

**Response:**
```json
{
  "scope_description": "Build a React e-commerce website with SEO optimization",
  "complexity": "medium",
  "matches": [
    {
      "category": "web_development",
      "estimated_hours_min": 17,
      "estimated_hours_max": 222,
      "hourly_rate_min": 75,
      "hourly_rate_max": 150,
      "project_range_min": 2000,
      "project_range_max": 25000,
      "recommended_price": 15800
    }
  ]
}
```

**Complexity multipliers:**
| Level | Hours | Price |
|-------|-------|-------|
| low/simple | 0.6x | 0.7x |
| medium (default) | 1.0x | 1.0x |
| high/complex | 1.5x | 1.3x |
| very_high/enterprise | 2.0x | 1.6x |

### `GET /portfolio`
Returns Ridge Cell Repair's portfolio context and service rates.

## Service Rates (hardcoded)
| Category | Hourly Min | Hourly Max | Project Min | Project Max |
|----------|-----------|-----------|-------------|-------------|
| web_development | $75 | $150 | $2,000 | $25,000 |
| seo_consulting | $60 | $120 | $1,000 | $10,000 |
| device_repair | $50 | $100 | $50 | $500 |
| content_creation | $40 | $80 | $500 | $5,000 |

## Task Types

### `upwork_proposal`
**Payload:** `{ "job_title": "...", "job_text": "...", "budget_range": "..." }`

### `consulting_sow`
**Payload:** `{ "client_name": "...", "project_scope": "...", "deliverables": ["...", "..."] }`

### `pricing`
**Payload:** `{ "scope_description": "...", "complexity": "medium" }`

## Dependencies
- `openclaw-sdk` (workspace) — agent framework, LLM client, task polling
- `axum` (workspace) — HTTP server
- `serde` / `serde_json` (workspace) — serialization
- `tracing` (workspace) — structured logging
- `async-trait` (workspace) — async trait support

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (default: `proposal-gen`) |
| `AGENT_PORT` | HTTP listen port (default: `8004`) |
| `AGENT_CAPABILITIES` | Comma-separated capability list (default: `upwork_proposal,consulting_sow,pricing`) |
| `OPENCLAW_CORE_URL` | Core API base URL for task polling |
| `LLM_API_KEY` | API key for LLM provider |
| `LLM_BASE_URL` | LLM API base URL |
