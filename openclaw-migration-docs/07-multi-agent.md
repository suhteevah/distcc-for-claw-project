# OpenClaw Multi-Agent Configuration Reference

*Scraped from https://docs.openclaw.ai/concepts/multi-agent — March 2026*

## Agent Structure
Each agent requires:
- **Workspace**: Contains `SOUL.md`, `AGENTS.md`, `USER.md`, `skills/`
- **agentDir**: `~/.openclaw/agents/<agentId>/agent` (auth profiles, model registry)
- **Session Store**: `~/.openclaw/agents/<agentId>/sessions`

**CRITICAL**: Never reuse `agentDir` across agents (causes auth/session collisions).

## Configuration
```json5
{
  agents: {
    list: [
      {
        id: "agent-name",
        workspace: "~/.openclaw/workspace-name",
        agentDir: "~/.openclaw/agents/agent-name/agent",
        model: "anthropic/claude-sonnet-4-5",
        name: "Display Name",
        default: true,
      },
    ],
  },
  bindings: [
    { agentId: "agent-name", match: { channel: "whatsapp" } },
  ],
}
```

## Per-Agent Auth
Each agent reads from: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
Copy to share credentials between agents.

## Routing (Bindings)
Specificity hierarchy:
1. Exact peer match (DM/group/channel ID)
2. Parent peer match (thread inheritance)
3. Guild ID + roles
4. Guild ID alone
5. Team ID
6. Account ID match
7. Channel-level match
8. Default agent fallback

Multiple match fields use AND semantics.

## Per-Agent Features (v2026.1.6+)
```json5
{
  agents: {
    list: [{
      id: "family",
      sandbox: { mode: "all", scope: "agent" },
      tools: { allow: ["read", "exec"], deny: ["write", "browser"] },
      groupChat: { mentionPatterns: ["@family"] }
    }]
  }
}
```

## Agent-to-Agent Messaging
```json5
{
  tools: {
    agentToAgent: { enabled: false, allow: ["home", "work"] }
  }
}
```

## CLI
```bash
openclaw agents add coding
openclaw agents add social
openclaw channels login --channel whatsapp --account work
openclaw agents list --bindings
openclaw channels status --probe
openclaw gateway restart
```
