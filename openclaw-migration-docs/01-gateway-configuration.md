# OpenClaw Gateway Configuration Reference

*Scraped from https://docs.openclaw.ai/gateway/configuration — March 2026*

## Configuration File Location & Format
OpenClaw reads optional JSON5 configuration from `~/.openclaw/openclaw.json`. If absent, safe defaults apply. The file supports comments and trailing commas.

## Gateway Server Settings

**Port & Network:**
- `gateway.port` — server listening port (default: 18789)
- `gateway.bind` — bind address (`loopback`, `lan`, `tailnet`, `custom`)
- `gateway.tailscale` — Tailscale integration
- `gateway.auth.token` — authentication token via `"${OPENCLAW_GATEWAY_TOKEN}"` substitution

**Reload Behavior:**
```
gateway.reload.mode: "hybrid" (default) | "hot" | "restart" | "off"
gateway.reload.debounceMs: 300 (default)
```

The gateway watches `~/.openclaw/openclaw.json` for changes. In `hybrid` mode, safe changes apply instantly; critical changes trigger automatic restart.

**Hot-Reload Categories:**
- No restart: Channels, agents, models, hooks, cron, sessions, tools, media, UI
- Restart required: `gateway.*` (port, bind, auth, TLS, HTTP), discovery, plugins

## Environment Variables

**Loading precedence:**
1. Parent process environment
2. `.env` (current working directory)
3. `~/.openclaw/.env` (global fallback)

**Inline config declaration:**
```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
    shellEnv: { enabled: true, timeoutMs: 15000 }
  }
}
```

**Variable substitution:** `${VAR_NAME}` syntax (uppercase only). Missing vars throw load-time errors.

## Data & Workspace Directories
- `agents.defaults.workspace` — agent workspace (default: `~/.openclaw/workspace`)
- Per-agent workspaces: `agents.list[].workspace`
- Session data: `sessions.json`
- Cron logs: `cron/runs/<jobId>.jsonl`

## Environment Variable Overrides
- `OPENCLAW_HOME` — home directory path resolution
- `OPENCLAW_STATE_DIR` — state directory location
- `OPENCLAW_CONFIG_PATH` — config file location

## File Inclusion
Use `$include` to split configuration:
```json5
{
  agents: { $include: "./agents.json5" },
  broadcast: { $include: ["./clients/a.json5", "./clients/b.json5"] }
}
```
Supports single-file replacement or array-based deep merge. Nested includes supported up to 10 levels.

## Configuration CLI
```bash
openclaw onboard              # Interactive setup wizard
openclaw configure            # Config wizard
openclaw config get <key>
openclaw config set <key> <value>
openclaw config unset <key>
openclaw doctor               # Validation diagnostics
openclaw doctor --fix         # Auto-repair
```
