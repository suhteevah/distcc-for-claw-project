# Legal Team

Drafts, reviews, and analyzes legal documents for Ridge Cell Repair LLC. Handles contract review, NDA/agreement generation, compliance research, and dispute letters. All outputs include a mandatory attorney-review disclaimer.

## Port: 8008
## LLM Tier: heavy

## Capabilities
- `contract_review` — Risk analysis, missing clause detection, unfavorable term identification
- `legal_draft` — NDA, service agreement, and document generation with Ridge Cell Repair details
- `compliance_research` — Regulatory and compliance requirement research
- `dispute_letter` — Demand and dispute letter drafting

## API Endpoints

### POST /review
Review a contract for risks and issues.
- **Request:** `{ "document": "string", "focus_areas": ["string"] }`
- **Response:** `{ "risks": [{ "severity": "high|medium|low", "clause": "string", "issue": "string", "recommendation": "string" }], "summary": "string", "disclaimer": "string" }`

### POST /draft
Draft a legal document.
- **Request:** `{ "document_type": "nda|service_agreement|terms_of_service|...", "parameters": { "party_name": "string", "terms": "string", ... } }`
- **Response:** `{ "document": "string", "type": "string", "disclaimer": "string" }`

### POST /compliance
Research compliance requirements.
- **Request:** `{ "topic": "string", "jurisdiction": "string" }`
- **Response:** `{ "requirements": [{ "regulation": "string", "summary": "string", "action_items": ["string"] }], "disclaimer": "string" }`

### POST /dispute
Draft a dispute or demand letter.
- **Request:** `{ "recipient": "string", "issue": "string", "desired_outcome": "string", "facts": "string" }`
- **Response:** `{ "letter": "string", "disclaimer": "string" }`

## Task Types
- `contract_review` — Analyzes provided contract text. Returns severity-rated list of risks, missing standard clauses, and unfavorable terms with specific clause references.
- `legal_draft` — Generates legal documents (NDA, service agreements, etc.) pre-filled with Ridge Cell Repair LLC details (business name, address, standard terms).
- `compliance_research` — Researches regulatory requirements for a given topic and jurisdiction. Returns structured list of applicable regulations and action items.
- `dispute_letter` — Drafts formal dispute/demand letters based on provided facts and desired outcome.

**CRITICAL:** Every response from every endpoint includes a disclaimer stating that the output is not legal advice and should be reviewed by a licensed attorney before use.

## System Prompt
> You are a legal assistant for Ridge Cell Repair LLC. You provide legal document drafts and analysis for review by qualified counsel. IMPORTANT: Always include a disclaimer at the end stating that this output is not legal advice and should be reviewed by a licensed attorney before use.

## Dependencies
- `openclaw-sdk` (workspace) — Agent SDK, task queue, LLM client
- `axum` (workspace) — HTTP server
- `tokio` (workspace) — Async runtime
- `serde` / `serde_json` (workspace) — Serialization
- `tracing` (workspace) — Structured logging
- `chrono` (workspace) — Date/time handling
- `anyhow` (workspace) — Error handling
- `async-trait` (workspace) — Async trait support

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | `legal-team` |
| `AGENT_PORT` | `8008` |
| `AGENT_CAPABILITIES` | `contract_review,legal_draft,compliance_research,dispute_letter` |
| `LLM_TIER` | `heavy` |
| `MAX_CONCURRENT_TASKS` | `2` |
| `LOG_LEVEL` | `info` |
