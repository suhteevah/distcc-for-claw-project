# OpenClaw Heartbeat Reference

*Scraped from https://docs.openclaw.ai/gateway/heartbeat — March 2026*

## Overview
Heartbeat enables periodic agent turns — model surfaces urgent matters without constant notifications.

## Scheduling
- Default interval: 30 minutes (1 hour for Anthropic OAuth)
- Configure: `agents.defaults.heartbeat.every` or disable with `0m`

## Active Hours (Quiet Hours)
```json5
{
  activeHours: {
    start: "09:00",
    end: "22:00",
    timezone: "America/New_York"
  }
}
```
Start inclusive, end exclusive. Omit for 24/7.

## Configuration Fields

| Field | Purpose |
|-------|---------|
| `target` | Delivery: "last", "none", or specific channel |
| `to` | Recipient override |
| `lightContext` | Only inject HEARTBEAT.md |
| `prompt` | Custom heartbeat instruction |
| `ackMaxChars` | Max chars after "HEARTBEAT_OK" (default: 300) |

## Response Protocol
- "HEARTBEAT_OK" = nothing urgent (gets stripped/dropped)
- Omit for alerts — return only alert text

## HEARTBEAT.md
Optional workspace file. Default prompt reads it if it exists. Empty files skipped.

## Manual Trigger
```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

## Cost
Full agent turn at each interval. Keep HEARTBEAT.md brief, use cheaper models.
