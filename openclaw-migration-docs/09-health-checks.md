# OpenClaw Health Check Reference

*Scraped from https://docs.openclaw.ai/gateway/health — March 2026*

## Unauthenticated Probes
```bash
curl -fsS http://127.0.0.1:18789/healthz  # Liveness (process up)
curl -fsS http://127.0.0.1:18789/readyz   # Readiness (channels connected)
```

## CLI Commands
```bash
openclaw status              # Local summary
openclaw status --all        # Full diagnosis
openclaw status --deep       # + Gateway probes
openclaw health --json       # Full health snapshot (WS-only)
openclaw health --timeout 10000  # Custom timeout
```

## In-App
Send `/status` as WhatsApp/WebChat message

## Docker Health Check
Built-in `HEALTHCHECK` pings `/healthz` automatically.

## What's Checked
- Gateway reachability/mode
- Linked credentials and auth age
- Per-channel probe summaries
- Session-store summary
- Non-zero exit code if unreachable or probe fails

## Key Paths
- Credentials: `~/.openclaw/credentials/`
- Sessions: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Logs: `/tmp/openclaw/openclaw-*.log`
