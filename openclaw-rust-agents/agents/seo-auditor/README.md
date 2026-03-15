# SEO Auditor

Comprehensive on-page SEO auditing agent. Fetches a URL, parses the full HTML document, extracts all SEO-relevant signals, scores the page out of 100, identifies issues by severity, and generates an LLM-powered executive summary.

## Port: 8001
## LLM Tier: heavy

## Capabilities
`seo_audit`, `lighthouse_scan`, `keyword_research`, `competitor_analysis`

## API Endpoints

### `POST /audit`
Run a full SEO audit on a URL.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "score": 72,
  "summary": "3-paragraph LLM-generated executive summary...",
  "page_data": {
    "url": "https://example.com",
    "status_code": 200,
    "redirect_chain": [],
    "title": "Example Domain",
    "title_length": 14,
    "meta_description": null,
    "meta_description_length": 0,
    "h1_count": 1,
    "h1_texts": ["Example Domain"],
    "h2_count": 0,
    "h2_texts": [],
    "image_count": 0,
    "images_missing_alt": 0,
    "internal_links": 0,
    "external_links": 1,
    "has_canonical": false,
    "canonical_url": null,
    "robots_meta": null,
    "has_og_tags": false,
    "has_schema": false,
    "word_count": 28,
    "html_size_kb": 1.3,
    "load_time_ms": 245
  },
  "issues": [
    {
      "severity": "critical",
      "category": "meta_description",
      "issue": "Page has no meta description",
      "fix": "Add a meta description between 120-160 characters summarizing the page"
    }
  ],
  "recommendations": ["..."],
  "audited_at": "2026-03-14T12:00:00Z"
}
```

## Task Types

### `seo_audit`
Full page analysis dispatched from the OpenClaw Core task queue.

**Payload:** `{ "url": "<target URL>" }`

**Scoring deductions:**
| Issue | Severity | Deduction |
|-------|----------|-----------|
| No title tag | critical | -15 |
| Title too short (<30 chars) | warning | -5 |
| Title too long (>60 chars) | info | -3 |
| No meta description | critical | -10 |
| Placeholder meta description | critical | -20 |
| Short meta description (<120 chars) | warning | -5 |
| No H1 tag | critical | -10 |
| Multiple H1 tags | warning | -5 |
| Images missing alt text | warning | -2 per image (max -10) |
| Thin content (<300 words) | warning | -10 |
| No canonical URL | info | -5 |
| No Open Graph tags | info | -5 |
| No Schema.org markup | info | -5 |
| Slow load time (>3000ms) | warning | -10 |
| Non-200 HTTP status | critical | -20 |

## Dependencies
- `openclaw-sdk` (workspace) — agent framework, LLM client, task polling
- `axum` (workspace) — HTTP server
- `reqwest` (workspace) — HTTP client for fetching pages
- `scraper` 0.21 — HTML parsing and CSS selector queries
- `serde` / `serde_json` (workspace) — serialization
- `chrono` (workspace) — timestamps
- `tracing` (workspace) — structured logging

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (default: from env) |
| `AGENT_PORT` | HTTP listen port (default: `8001`) |
| `AGENT_CAPABILITIES` | Comma-separated capability list |
| `OPENCLAW_CORE_URL` | Core API base URL for task polling |
| `LLM_API_KEY` | API key for LLM provider |
| `LLM_BASE_URL` | LLM API base URL |
