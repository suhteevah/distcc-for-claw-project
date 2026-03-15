# OpenClaw Security Reference

*Scraped from https://docs.openclaw.ai/gateway/security — March 2026*

## Authentication Modes
- `token`: `gateway.auth.token` with long random value
- `password`: `OPENCLAW_GATEWAY_PASSWORD` env var
- `trusted-proxy`: identity-aware reverse proxy

Fail-closed: no token/password = no WebSocket connections.

## Tailscale Auth
`gateway.auth.allowTailscale: true` — accepts `tailscale-user-login` header from Serve.

## File Permissions
- `~/.openclaw/openclaw.json`: `600`
- `~/.openclaw/`: `700`

## Credential Locations
- WhatsApp: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- Telegram tokens: config/env or `channels.telegram.tokenFile`
- Discord/Slack tokens: config/env or SecretRef
- Model auth: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

**WARNING**: "Assume anything under `~/.openclaw/` may contain secrets"

## Network Binding
- `loopback` (default): localhost only
- `lan`, `tailnet`, `custom`: wider exposure
- Funnel: public HTTPS (critical risk)

## Docker/UFW
Docker published ports bypass host `INPUT` rules. Restrict in `DOCKER-USER` chain:
```
-A DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
-A DOCKER-USER -s 127.0.0.0/8 -j RETURN
-A DOCKER-USER -m conntrack --ctstate NEW -j DROP
```

## Reverse Proxy
Configure `gateway.trustedProxies` with proxy IPs. Set `proxy_set_header X-Forwarded-For $remote_addr`.

## Plugin Security
- Plugins run in-process
- Use `plugins.allow` allowlists
- Pin exact npm versions
- Review before enabling

## Credential Rotation
1. Generate new secret
2. Restart Gateway
3. Update remote clients
4. Verify old creds rejected
