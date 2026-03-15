# OpenClaw Troubleshooting Reference

*Scraped from https://docs.openclaw.ai/gateway/troubleshooting — March 2026*

## Diagnostic Commands
```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

## Gateway Won't Start
- Check `gateway.mode=local` is set
- Port conflict: `EADDRINUSE` → another instance running
- Auth binding: non-loopback without auth → refuses to bind

## Post-Upgrade Issues
- Reinstall service: `openclaw gateway install --force`
- Check auth/URL override behavior changes
- Stricter bind/auth guardrails in newer versions

## API Rate Limits (429)
- Disable `context1m` for the model
- Use billing-enabled API key
- Configure fallback models

## Messages Not Flowing
- Check pairing status for DM senders
- Verify `requireMention` / `mentionPatterns` for groups
- Check channel/allowlist alignment
- Examine DM policy settings

## Control UI Issues
- `device identity required` → non-secure context
- `device nonce mismatch` → incomplete challenge auth
- `AUTH_TOKEN_MISMATCH` → attempt trusted retry

## Cron Not Running
- `"cron: scheduler disabled"` → `cron.enabled: false`
- Check heartbeat skip reasons: `quiet-hours`, `requests-in-flight`, `alerts-disabled`
- Verify valid account ID for delivery targets

## Tool Execution
- `NODE_BACKGROUND_UNAVAILABLE` → app must be in foreground
- `SYSTEM_RUN_DENIED` → exec approval pending
