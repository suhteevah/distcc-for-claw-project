# OpenClaw Remote Access & Daemon Reference

*Scraped from https://docs.openclaw.ai/gateway/remote + /cli/daemon — March 2026*

## Deployment Models

**Always-On Gateway (Recommended for servers):**
Run gateway on persistent host, reach via Tailscale or SSH.

**SSH Tunnel:**
```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

**Remote Config:**
```json5
{
  gateway: {
    mode: "remote",
    remote: { url: "ws://127.0.0.1:18789", token: "your-token" }
  }
}
```

## Daemon/Service Management

`openclaw daemon` is legacy alias for `openclaw gateway`.

**Commands:**
```bash
openclaw gateway status     # Check state
openclaw gateway install    # Register service (systemd/launchd/schtasks)
openclaw gateway install --force  # Reinstall metadata
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

**Platform support:**
- Linux: systemd
- macOS: launchd
- Windows: schtasks

## Security
- Keep gateway loopback-only unless you need wider access
- Non-loopback requires auth tokens or passwords
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` for trusted private networks only

## Key Notes
- `gateway.mode=local` required for service startup
- Token drift checks include both `Environment=` and `EnvironmentFile=` sources
- If both token and password auth configured without explicit mode, installation blocks
