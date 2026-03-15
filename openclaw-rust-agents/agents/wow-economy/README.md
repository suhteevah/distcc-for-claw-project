# WoW Economy

Analyzes World of Warcraft Auction House economy data. Imports TradeSkillMaster snapshots, scans for arbitrage, calculates crafting profitability, and generates LLM-powered market trend analysis.

## Port: 8007
## LLM Tier: fast

## Capabilities
- `tsm_import` — Import TradeSkillMaster market data
- `arbitrage_scan` — Find underpriced items for flipping
- `crafting_profit` — Calculate recipe profitability
- `market_trend` — LLM-powered trend analysis

## API Endpoints

### POST /tsm/import
Import a TradeSkillMaster data snapshot.
- **Request:** `{ "data": "string (TSM export format)", "realm": "string" }`
- **Response:** `{ "imported": usize, "updated": usize, "realm": "string" }`

### GET /arbitrage
Scan for arbitrage opportunities across stored item data.
- **Response:** `[{ "item_id": u64, "name": "string", "buy_price": u64, "market_value": u64, "profit_margin": f64 }, ...]`

### POST /crafting/profit
Calculate profitability for a crafting recipe.
- **Request:** `{ "recipe_id": "string", "materials": [{ "item_id": u64, "quantity": u32 }], "product_item_id": u64 }`
- **Response:** `{ "material_cost": u64, "product_value": u64, "profit": i64, "margin_pct": f64, "ah_cut": u64 }`

### POST /market/trend
Generate LLM-powered market trend analysis.
- **Request:** `{ "item_ids": [u64], "timeframe": "string" }`
- **Response:** `{ "analysis": "string", "trends": [{ "item_id": u64, "direction": "string", "confidence": f64 }] }`

### GET /items
List all tracked items in the store.
- **Response:** `[{ "item_id": u64, "name": "string", "market_value": u64, "min_buyout": u64, "last_updated": "string" }, ...]`

## Task Types
- `tsm_import` — Parse and store TradeSkillMaster export data into in-memory item store.
- `arbitrage_scan` — Compare current buyout prices against market values to find flip opportunities.
- `crafting_profit` — Compute profit/loss for a recipe given current material and product prices. Accounts for AH cut (5%).
- `market_trend` — Uses LLM to analyze price history and generate trend predictions with confidence scores.

## Dependencies
- `openclaw-sdk` (workspace) — Agent SDK, task queue, LLM client
- `axum` (workspace) — HTTP server
- `tokio` (workspace) — Async runtime
- `reqwest` (workspace) — HTTP client
- `serde` / `serde_json` (workspace) — Serialization
- `tracing` (workspace) — Structured logging
- `chrono` (workspace) — Date/time handling
- `anyhow` (workspace) — Error handling
- `async-trait` (workspace) — Async trait support
- `dashmap` 6 — Concurrent in-memory item and recipe stores

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | `wow-economy` |
| `AGENT_PORT` | `8007` |
| `AGENT_CAPABILITIES` | `tsm_import,arbitrage_scan,crafting_profit,market_trend` |
| `LLM_TIER` | `fast` |
| `MAX_CONCURRENT_TASKS` | `2` |
| `LOG_LEVEL` | `info` |
| `DATABASE_URL` | PostgreSQL connection string |
