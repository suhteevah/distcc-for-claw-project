# MailClaw + Discord Channel Architecture

**Date:** 2026-03-02
**Status:** Approved

## Overview

Add a dedicated email management agent (MailClaw) to OpenClaw and migrate automated outputs to Discord channels. Telegram becomes the direct line to the main Claw agent only.

## Channel Architecture

| Agent / Job        | Channel              | Purpose                                |
|--------------------|----------------------|----------------------------------------|
| **Claw** (main)    | Telegram             | Direct conversation, on-demand tasks   |
| **MailClaw** (new) | Discord `#mailclaw`  | Email management, inbox digests        |
| **Briefing**       | Discord `#briefing`  | Daily 6am briefing, evening wrap-up    |

**Discord server admin:** `gambleordie` (full admin)

## MailClaw Agent

### Identity

- **Name:** `mailclaw`
- **Emoji:** 📧
- **Model:** `gemini` (free tier, 1M context — email threads get long)
- **Workspace:** Isolated (`~/.openclaw/agents/mailclaw/`)
- **Channel:** Discord, routed to `#mailclaw` channel

### Email Backend: Himalaya CLI

- Existing Himalaya skill in OpenClaw sandbox — promote to MailClaw workspace
- All Gmail accounts via IMAP/SMTP
- App passwords stored via Windows Credential Manager or `pass`
- Multi-account switching: `himalaya --account <name> <command>`
- JSON output mode for structured parsing

### Accounts

```toml
# ~/.config/himalaya/config.toml
[accounts.personal]
email = "<personal>@gmail.com"
default = true
# IMAP/SMTP config...

[accounts.business1]
email = "<business1>@gmail.com"
# IMAP/SMTP config...

[accounts.business2]
email = "<business2>@gmail.com"
# IMAP/SMTP config...

# + project emails as needed
```

### Capabilities

| Capability       | Implementation                                    |
|------------------|---------------------------------------------------|
| Inbox triage     | `himalaya envelope list --output json` all accounts |
| Read emails      | `himalaya message read <id>` — summarize          |
| Reply/compose    | Draft via MML template, show draft, send on approval |
| Forward          | `himalaya message forward <id>`                   |
| Search           | `himalaya envelope list from:x subject:y`         |
| Organize         | Move, archive, flag, delete                       |
| Attachments      | `himalaya attachment download <id>`               |

### Safety

- **All outbound emails** shown as drafts for approval before sending
- No auto-sending without explicit "yes" in Discord

### Cron Jobs

| Job              | Schedule          | Action                                      |
|------------------|-------------------|---------------------------------------------|
| Morning digest   | `0 6 * * *` PST   | Scan all accounts, summarize, flag urgent   |
| Evening wrap-up  | `0 18 * * *` PST  | Catch-up, unanswered thread reminders       |

Delivery: Discord `#mailclaw` channel

## Briefing Reroute

- Move daily briefing delivery from Telegram to Discord `#briefing`
- Same cron job (`0 6 * * *`), same Gemini model, just change delivery channel
- Keeps Telegram clean for direct Claw interaction

## Discord Setup (Prerequisites)

1. **Create Discord bot** at https://discord.com/developers/applications
   - Bot permissions: Send Messages, Read Message History, Embed Links, Attach Files
   - Privileged intents: Message Content Intent
2. **Create Discord server** (or use existing)
   - `gambleordie` as full admin
   - Channels: `#mailclaw`, `#briefing`, `#general`
3. **Invite bot** to server with appropriate permissions
4. **Add bot token** to OpenClaw: `openclaw channels add --channel discord --token <bot-token>`
5. **Enable Discord** in openclaw.json
6. **Resolve allowlist** — convert `sativa2720` and `jitk123` to stable Discord IDs

## Implementation Steps

1. **Discord infrastructure**
   - Create bot application + token
   - Create server with channels (#mailclaw, #briefing)
   - Set gambleordie as admin
   - Add bot token to OpenClaw, enable Discord channel

2. **Install Himalaya**
   - `scoop install himalaya` or `cargo install himalaya`
   - Verify: `himalaya --version`

3. **Configure Gmail accounts**
   - Generate app passwords for each Gmail account
   - Create `~/.config/himalaya/config.toml` with all accounts
   - Test: `himalaya envelope list` per account

4. **Create MailClaw agent**
   - `openclaw agents add mailclaw --model gemini --bind discord`
   - Copy Himalaya skill from sandbox to MailClaw workspace
   - Customize skill with account-specific instructions
   - Set up agent identity (emoji, name)

5. **Route Discord channels**
   - Bind MailClaw to #mailclaw channel
   - Set up routing rules

6. **Add cron jobs**
   - Morning digest: 6am PST, deliver to Discord #mailclaw
   - Evening wrap-up: 6pm PST, deliver to Discord #mailclaw

7. **Reroute briefing**
   - Edit existing briefing cron job delivery from Telegram to Discord #briefing

8. **Test end-to-end**
   - Test inbox listing across all accounts
   - Test read/reply flow with approval
   - Test cron digests deliver to correct Discord channels
   - Test briefing shows up in #briefing
   - Verify Telegram stays clean (Claw direct only)
