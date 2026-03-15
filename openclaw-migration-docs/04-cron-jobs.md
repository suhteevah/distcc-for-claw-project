# OpenClaw Cron Jobs Reference

*Scraped from https://docs.openclaw.ai/automation/cron-jobs — March 2026*

## Storage
- Job store: `~/.openclaw/cron/jobs.json` (Gateway-managed)
- Run history: `~/.openclaw/cron/runs/<jobId>.jsonl`

## Schedule Types

| Type | Field | Format | Example |
|------|-------|--------|---------|
| One-shot | `at` | ISO 8601 | `2026-02-01T16:00:00Z` |
| Interval | `everyMs` | Milliseconds | `300000` (5 min) |
| Recurring | `expr` | Cron expression | `0 7 * * *` |

Timezone via `tz` parameter (IANA format). Defaults to host timezone.

## Job Payload Types

**System Event:**
```json
{ "kind": "systemEvent", "text": "Event text" }
```

**Agent Turn:**
```json
{
  "kind": "agentTurn",
  "message": "Prompt text",
  "model": "anthropic/claude-sonnet-4-20250514",
  "thinking": "high",
  "timeoutSeconds": 300,
  "lightContext": true
}
```

## Session Targets
- `"main"` — runs in main session
- `"isolated"` — dedicated session per run (`cron:<jobId>`)
- `"current"` — binds to creation session
- `"session:custom-id"` — persistent custom session

## Delivery Modes
- `"announce"` — posts to channel via outbound adapter
- `"webhook"` — POSTs to URL
- `"none"` — internal only

Channel targeting: Discord/Slack use `channel:<id>` prefix.

## Error Handling

**Transient (retried):** 429 rate limits, 5xx errors, network timeouts
**Permanent (disables job):** auth failures, validation errors

**Recurring jobs:** exponential backoff (30s → 1m → 5m → 15m → 60m), job stays enabled

## Configuration
```json5
{
  cron: {
    enabled: true,
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1,
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000]
    },
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 }
  }
}
```

Disable: `cron.enabled: false` or `OPENCLAW_SKIP_CRON=1`

## CLI
```bash
openclaw cron list
openclaw cron add --name "Job" --cron "0 7 * * *" --session isolated --message "Task" --announce
openclaw cron edit <jobId> --message "Updated"
openclaw cron remove <jobId>
openclaw cron run <jobId>
openclaw cron runs --id <jobId> --limit 50
```

## Stagger
Top-of-hour jobs auto-stagger up to 5 min. Override: `schedule.staggerMs`, `--stagger 30s`, `--exact`.
