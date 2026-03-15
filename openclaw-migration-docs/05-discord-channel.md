# OpenClaw Discord Configuration Reference

*Scraped from https://docs.openclaw.ai/channels/discord — March 2026*

## Token Setup
```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN"
    }
  }
}
```

Env fallback: `DISCORD_BOT_TOKEN` (default account only)

## Required Bot Intents (Discord Developer Portal)
- Message Content Intent (required)
- Server Members Intent (recommended)
- Presence Intent (optional)

## Guild Access Control
```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "SERVER_ID": {
          requireMention: true,
          users: ["USER_ID"],
          roles: ["ROLE_ID"],
          channels: { "channel_name": { allow: true } }
        }
      }
    }
  }
}
```

## DM Policy
Options: `pairing`, `allowlist`, `open`, `disabled`

## Multi-Account
```json5
{
  channels: {
    discord: {
      accounts: {
        default: { token: "TOKEN_1" },
        secondary: { token: "TOKEN_2" }
      }
    }
  }
}
```

## Streaming
Options: `off`, `partial`, `block`, `progress`

## Presence
```json5
{
  channels: {
    discord: {
      status: "online",
      activity: "Focus time",
      activityType: 4,
      autoPresence: { enabled: true, intervalMs: 30000 }
    }
  }
}
```

## History
```json5
{
  channels: {
    discord: {
      historyLimit: 20,
      dmHistoryLimit: 50
    }
  }
}
```

## Event Queue
```json5
{
  channels: {
    discord: {
      eventQueue: {
        listenerTimeout: 120000,
        maxQueueSize: 1000,
        maxConcurrency: 10
      },
      inboundWorker: { runTimeoutMs: 1800000 }
    }
  }
}
```

## Container Deployment Checklist
1. Set bot token via env or config
2. Enable required intents in Discord Developer Portal
3. Configure guild allowlist
4. Set DM policy (pairing recommended)
5. Adjust timeouts
6. Enable action gates as needed
7. Configure streaming
8. Test with `openclaw channels status --probe`
