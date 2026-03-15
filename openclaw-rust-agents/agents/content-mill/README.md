# Content Mill

Multi-format content generation agent for Ridge Cell Repair LLC. Produces blog posts, social media content, email campaigns, and SEO-optimized page copy through a unified task handler and separate direct API endpoints.

## Port: 8003
## LLM Tier: heavy (blog, email, SEO) / fast (social media)

## Capabilities
`blog_post`, `social_media`, `email_campaign`, `seo_content`

## API Endpoints

### `POST /blog`
Generate a blog post with optional metadata.

**Request:**
```json
{
  "topic": "Why Local SEO Matters for Small Businesses",
  "keywords": ["local seo", "google business profile", "small business marketing"],
  "tone": "professional",
  "word_count": 1200,
  "target_audience": "small business owners",
  "include_meta": true
}
```

**Response:**
```json
{
  "content_type": "blog_post",
  "topic": "Why Local SEO Matters for Small Businesses",
  "body": "# Why Local SEO Matters...\n\n...",
  "word_count": 1187,
  "generated_at": "2026-03-14T12:00:00Z",
  "meta": {
    "title": "Why Local SEO Matters for Small Businesses in 2026",
    "meta_description": "Learn how local SEO drives foot traffic...",
    "slug": "local-seo-small-businesses",
    "excerpt": "...",
    "tags": ["local seo", "small business"]
  },
  "model": "...",
  "tokens_used": 2048
}
```

When `include_meta` is true, the LLM appends metadata after a `---META---` separator in the output, which is parsed into the `meta` field.

### `POST /social`
Generate platform-optimized social media posts.

**Request:**
```json
{
  "topic": "New phone repair service launch",
  "platforms": ["twitter", "linkedin", "instagram"],
  "tone": "casual",
  "include_hashtags": true,
  "cta": "Book your repair at ridgecellrepair.com"
}
```

**Response:**
```json
{
  "content_type": "social_media",
  "topic": "New phone repair service launch",
  "body": {
    "twitter": { "text": "...", "character_count": 240, "hashtags": ["#PhoneRepair"] },
    "linkedin": { "text": "...", "character_count": 890, "hashtags": [] },
    "instagram": { "text": "...", "character_count": 1200, "hashtags": ["#PhoneRepair"] }
  },
  "word_count": 320,
  "generated_at": "2026-03-14T12:00:00Z",
  "model": "...",
  "tokens_used": 512
}
```

### `POST /email-campaign`
Generate a multi-email campaign sequence.

**Request:**
```json
{
  "campaign_type": "nurture",
  "subject_context": "New customer onboarding for web development services",
  "target_audience": "small business owners",
  "product_service": "Custom website development",
  "num_emails": 3,
  "tone": "professional"
}
```

**Campaign types:** `nurture`, `promo`, `cold_outreach`, `follow_up`

**Response:** JSON with `emails` array containing `sequence_number`, `subject_line`, `preview_text`, `body_html`, `body_text`, `send_delay_days`, and `notes` per email.

### `POST /seo-content`
Generate SEO-optimized page content.

**Request:**
```json
{
  "url": "https://ridgecellrepair.com/services/seo",
  "primary_keyword": "SEO consulting services",
  "secondary_keywords": ["technical seo audit", "local seo"],
  "content_type": "service_page",
  "word_count": 1200
}
```

**Content types:** `landing_page`, `service_page`, `about_page`

## Task Types

All four content types are handled via the OpenClaw Core task queue. Payloads match the corresponding API request bodies above.

- `blog_post` — Blog article generation
- `social_media` — Multi-platform social posts
- `email_campaign` — Email sequence generation
- `seo_content` — SEO-optimized page copy

## Dependencies
- `openclaw-sdk` (workspace) — agent framework, LLM client, task polling
- `axum` (workspace) — HTTP server
- `serde` / `serde_json` (workspace) — serialization
- `chrono` (workspace) — timestamps
- `tracing` (workspace) — structured logging
- `async-trait` (workspace) — async trait support

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (default: `content-mill`) |
| `AGENT_PORT` | HTTP listen port (default: `8003`) |
| `AGENT_CAPABILITIES` | Comma-separated capability list (default: `blog_post,social_media,email_campaign,seo_content`) |
| `OPENCLAW_CORE_URL` | Core API base URL for task polling |
| `LLM_API_KEY` | API key for LLM provider |
| `LLM_BASE_URL` | LLM API base URL |
