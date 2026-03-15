# OpenClaw CNC-Server Consolidation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Move the entire OpenClaw stack (gateway, Discord bot, cron scheduler, MailClaw agent, email pipeline) from Kokonoe (Windows) to CNC-Server (openSUSE Leap Micro 6.2), running everything as Podman containers in one compose file.

**Architecture:** Add an `openclaw-gateway` container (using the official `ghcr.io/openclaw/openclaw:latest` image) to the existing `docker-compose.yml` on CNC-Server alongside the 7 business agents, Core, Redis, Postgres, and monitoring stack. The gateway handles Discord/Telegram bots, cron scheduling, and agent routing. MailClaw uses Himalaya CLI (volume-mounted Linux binary) for email operations. All config is bind-mounted from `/opt/openclaw/gateway-config/`.

**Tech Stack:** Podman (Docker-compatible), OpenClaw gateway (Node.js), Himalaya email CLI (Rust static binary), Gemini 2.5 Flash (LLM), systemd (auto-restart via Podman)

**Machines:**
- **CNC-Server**: 192.168.168.100 (wired LAN), 100.108.202.49 (Tailscale), root SSH, openSUSE Leap Micro 6.2
- **Kokonoe**: Windows PC (source of config files), SSH from CNC-Server not available — SCP from Kokonoe to CNC-Server

**Key Docs:**
- Official Docker guide: `J:\distcc for claw project\openclaw-docs-upstream\docs\install\docker.md`
- Official Podman guide: `J:\distcc for claw project\openclaw-docs-upstream\docs\install\podman.md`
- Official compose: `J:\distcc for claw project\openclaw-docs-upstream\docker-compose.yml`
- Official Dockerfile: `J:\distcc for claw project\openclaw-docs-upstream\Dockerfile`
- Cron docs: `J:\distcc for claw project\openclaw-docs-upstream\docs\automation\cron-jobs.md`
- Discord docs: `J:\distcc for claw project\openclaw-docs-upstream\docs\channels\discord.md`
- Our scraped reference: `J:\distcc for claw project\openclaw-migration-docs\*.md`

---

### Task 1: Prepare CNC-Server Directory Structure

**Context:** CNC-Server already has `/opt/openclaw/openclaw-agents/` for the existing stack. We'll create a parallel directory for the gateway config.

**Step 1: Create gateway config directories on CNC-Server**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "mkdir -p /opt/openclaw/gateway-config/{agents,cron,workspace,workspace-mailclaw,credentials,memory,plugins,extensions,identity,media,fleet,completions,config,devices,delivery-queue,subagents,sessions} && mkdir -p /opt/openclaw/himalaya && echo 'done'"
```

Expected: `done`

**Step 2: Verify directory structure**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "ls /opt/openclaw/gateway-config/"
```

Expected: All subdirectories listed

**Step 3: Commit note** — No git commit for this task (remote infra setup)

---

### Task 2: Download Himalaya Linux Binary

**Context:** Himalaya is a Rust CLI for IMAP/SMTP. MailClaw agent uses it to check/send email. We need the Linux x86_64 musl static binary on CNC-Server.

**Step 1: Download Himalaya v1.2.0 Linux binary to CNC-Server**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "curl -L -o /opt/openclaw/himalaya/himalaya 'https://github.com/pimalaya/himalaya/releases/download/v1.2.0/himalaya-x86_64-linux-musl.tar.gz' 2>&1 | tail -3"
```

NOTE: If this is a tarball, extract it:
```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "cd /opt/openclaw/himalaya && tar xzf himalaya 2>/dev/null; ls -la /opt/openclaw/himalaya/"
```

If extraction produces a binary named `himalaya`, we're good. If the release format is different, adapt. The goal is a single executable at `/opt/openclaw/himalaya/himalaya`.

**Step 2: Make it executable and test**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "chmod +x /opt/openclaw/himalaya/himalaya && /opt/openclaw/himalaya/himalaya --version"
```

Expected: `himalaya 1.2.0` (or similar version string)

**Step 3: No commit** — Remote infra setup

---

### Task 3: Copy Himalaya Email Config

**Context:** The Himalaya config has Gmail App Passwords for 3 accounts (ridgecell, suhteevah, mmichels). Copy from Windows to CNC-Server.

**Step 1: SCP the Himalaya config to CNC-Server**

```bash
scp "C:/Users/Matt/.config/himalaya/config.toml" root@192.168.168.100:/opt/openclaw/himalaya/config.toml
```

Expected: File transferred successfully

**Step 2: Set restrictive permissions (contains passwords)**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "chmod 600 /opt/openclaw/himalaya/config.toml && ls -la /opt/openclaw/himalaya/config.toml"
```

Expected: `-rw-------` permissions

**Step 3: Test Himalaya can connect to Gmail from CNC-Server**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "/opt/openclaw/himalaya/himalaya -c /opt/openclaw/himalaya/config.toml envelope list -a ridgecell --page-size 3"
```

Expected: List of recent emails from ridgecellrepair@gmail.com (or connection error if domain issues — suhteevah account is more reliable as a test)

If ridgecell fails, test with suhteevah:
```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "/opt/openclaw/himalaya/himalaya -c /opt/openclaw/himalaya/config.toml envelope list -a suhteevah --page-size 3"
```

**Step 4: No commit** — Remote config deployment

---

### Task 4: Copy and Adapt OpenClaw Config

**Context:** The main `openclaw.json` has Windows paths that need updating to Linux container paths. Agent directories, workspaces, and cron job Himalaya paths all need to change.

**Step 1: Copy openclaw.json to CNC-Server**

```bash
scp "C:/Users/Matt/.openclaw/openclaw.json" root@192.168.168.100:/opt/openclaw/gateway-config/openclaw.json
```

**Step 2: Update paths in openclaw.json on CNC-Server**

The key changes needed:
- All `~/.openclaw/` references resolve correctly because the container mounts `/opt/openclaw/gateway-config` as `/home/node/.openclaw`
- `gateway.bind` needs to be `"lan"` (not `"loopback"`) for container networking
- `gateway.mode` must be `"local"`

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 'python3 -c "
import json
with open(\"/opt/openclaw/gateway-config/openclaw.json\") as f:
    config = json.load(f)

# Ensure gateway mode and bind are correct for container
config[\"gateway\"][\"mode\"] = \"local\"
config[\"gateway\"][\"bind\"] = \"lan\"

with open(\"/opt/openclaw/gateway-config/openclaw.json\", \"w\") as f:
    json.dump(config, f, indent=2)
print(\"Config updated\")
"'
```

Expected: `Config updated`

**Step 3: Copy agent directories**

```bash
scp -r "C:/Users/Matt/.openclaw/agents/" root@192.168.168.100:/opt/openclaw/gateway-config/agents/
```

**Step 4: Copy cron jobs and update Himalaya paths**

```bash
scp -r "C:/Users/Matt/.openclaw/cron/" root@192.168.168.100:/opt/openclaw/gateway-config/cron/
```

Then update Himalaya paths in jobs.json:
```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "sed -i 's|C:\\\\Users\\\\Matt\\\\.cargo\\\\bin\\\\himalaya.exe|/usr/local/bin/himalaya|g' /opt/openclaw/gateway-config/cron/jobs.json && grep -c himalaya /opt/openclaw/gateway-config/cron/jobs.json"
```

Expected: Count of replacements (should be 5 — the 3 MailClaw jobs reference himalaya)

**Step 5: Copy remaining config directories**

```bash
scp -r "C:/Users/Matt/.openclaw/credentials/" root@192.168.168.100:/opt/openclaw/gateway-config/credentials/ 2>/dev/null
scp -r "C:/Users/Matt/.openclaw/memory/" root@192.168.168.100:/opt/openclaw/gateway-config/memory/ 2>/dev/null
scp -r "C:/Users/Matt/.openclaw/workspace/" root@192.168.168.100:/opt/openclaw/gateway-config/workspace/ 2>/dev/null
scp -r "C:/Users/Matt/.openclaw/workspace-mailclaw/" root@192.168.168.100:/opt/openclaw/gateway-config/workspace-mailclaw/ 2>/dev/null
scp -r "C:/Users/Matt/.openclaw/identity/" root@192.168.168.100:/opt/openclaw/gateway-config/identity/ 2>/dev/null
scp -r "C:/Users/Matt/.openclaw/plugins/" root@192.168.168.100:/opt/openclaw/gateway-config/plugins/ 2>/dev/null
scp "C:/Users/Matt/.openclaw/memory.db" root@192.168.168.100:/opt/openclaw/gateway-config/ 2>/dev/null
scp "C:/Users/Matt/.openclaw/vector_store.db" root@192.168.168.100:/opt/openclaw/gateway-config/ 2>/dev/null
scp "C:/Users/Matt/.openclaw/exec-approvals.json" root@192.168.168.100:/opt/openclaw/gateway-config/ 2>/dev/null
```

**Step 6: Set ownership for container user (node = uid 1000)**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "chown -R 1000:1000 /opt/openclaw/gateway-config/ && chown -R 1000:1000 /opt/openclaw/himalaya/ && echo 'ownership set'"
```

Expected: `ownership set`

**Step 7: No commit** — Remote config deployment

---

### Task 5: Pull the Official OpenClaw Docker Image

**Context:** The official pre-built image eliminates the need to build from source.

**Step 1: Pull the image on CNC-Server**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman pull ghcr.io/openclaw/openclaw:latest 2>&1 | tail -5"
```

Expected: Image pulled successfully (may take 1-3 minutes, ~500MB)

**Step 2: Verify the image**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman image inspect ghcr.io/openclaw/openclaw:latest --format '{{.Id}} {{.Size}}'"
```

Expected: Image ID and size

**Step 3: No commit** — Remote infra setup

---

### Task 6: Add Gateway to docker-compose.yml

**Context:** This is the core change. Add the `openclaw-gateway` service to the existing compose file that already has 16 services.

**Step 1: Copy compose file from CNC-Server to local for editing**

```bash
scp root@192.168.168.100:/opt/openclaw/openclaw-agents/docker-compose.yml "C:/Users/Matt/tmp_compose_gateway.yml"
```

**Step 2: Add the gateway service to the compose file**

Add this service block after the `cadvisor` service and before the `volumes:` section:

```yaml
  # ═══════════════════════════════════════
  # OPENCLAW GATEWAY (Discord, Telegram, Cron, Agent Routing)
  # ═══════════════════════════════════════
  openclaw-gateway:
    image: ghcr.io/openclaw/openclaw:latest
    container_name: openclaw-gateway
    restart: unless-stopped
    dns:
      - 8.8.8.8
      - 1.1.1.1
    ports:
      - "18789:18789"
      - "18790:18790"
    environment:
      HOME: /home/node
      TERM: xterm-256color
      TZ: America/Los_Angeles
      OPENCLAW_GATEWAY_TOKEN: "${OPENCLAW_GATEWAY_TOKEN}"
      DISCORD_BOT_TOKEN: "${DISCORD_BOT_TOKEN}"
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
      OPENCLAW_ALLOW_INSECURE_PRIVATE_WS: "1"
    volumes:
      - /opt/openclaw/gateway-config:/home/node/.openclaw
      - /opt/openclaw/gateway-config/workspace:/home/node/.openclaw/workspace
      - /opt/openclaw/gateway-config/workspace-mailclaw:/home/node/.openclaw/workspace-mailclaw
      - /opt/openclaw/himalaya/himalaya:/usr/local/bin/himalaya:ro
      - /opt/openclaw/himalaya/config.toml:/home/node/.config/himalaya/config.toml:ro
    init: true
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "lan",
        "--port",
        "18789",
      ]
    healthcheck:
      test:
        [
          "CMD",
          "node",
          "-e",
          "fetch('http://127.0.0.1:18789/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))",
        ]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 20s
    logging:
      driver: "json-file"
      options: { max-size: "50m", max-file: "5" }
```

**Step 3: Add gateway env vars to .env on CNC-Server**

Append to `/opt/openclaw/openclaw-agents/.env`:

```bash
# ── OpenClaw Gateway ──────────────────
OPENCLAW_GATEWAY_TOKEN=e11eae272cfc948070062045faff1aca9c9277af3d52aba3
DISCORD_BOT_TOKEN=***DISCORD_TOKEN_REDACTED***
```

NOTE: The `ANTHROPIC_API_KEY` is already in the `.env` file from the existing agent setup.

**Step 4: SCP the updated compose file back to CNC-Server**

```bash
scp "C:/Users/Matt/tmp_compose_gateway.yml" root@192.168.168.100:/opt/openclaw/openclaw-agents/docker-compose.yml
```

**Step 5: No commit** — Remote infra (but consider committing the compose file to the project repo)

---

### Task 7: Deploy the Gateway Container

**Context:** Bring up just the new gateway container without disrupting the existing 16 running containers.

**Step 1: Pull image and start only the gateway**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "cd /opt/openclaw/openclaw-agents && docker compose up -d openclaw-gateway 2>&1"
```

Expected: Gateway container created and started

**Step 2: Wait for health check and verify**

```bash
# Wait 30 seconds for startup
sleep 30
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman ps --filter name=openclaw-gateway --format '{{.Names}} {{.Status}}'"
```

Expected: `openclaw-gateway Up X seconds (healthy)` or `(health: starting)`

**Step 3: Check gateway logs for successful Discord connection**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman logs openclaw-gateway 2>&1 | tail -30"
```

Expected: Logs showing gateway startup, Discord bot login, cron scheduler initialization. Look for:
- `gateway listening on 0.0.0.0:18789`
- `discord: logged in as gambleordie`
- `cron: scheduler started` or similar
- No `ECONNREFUSED` or DNS errors

**Step 4: Test health endpoint from host**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "curl -s http://localhost:18789/healthz"
```

Expected: HTTP 200 response

**Step 5: Test Tailscale access from Kokonoe**

```bash
curl -s http://100.108.202.49:18789/healthz
```

Expected: HTTP 200 response (proves Tailscale routing works)

**Step 6: Test LAN access from Kokonoe**

```bash
curl -s http://192.168.168.100:18789/healthz
```

Expected: HTTP 200 response

**Step 7: No commit** — Deployment verification

---

### Task 8: Verify Discord Bot Connection

**Context:** The Discord bot (gambleordie) should have connected to the Openclaw guild.

**Step 1: Check Discord connection in logs**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman logs openclaw-gateway 2>&1 | grep -i discord"
```

Expected: Discord connection success messages

**Step 2: Send a test message in Discord**

From the Discord client (Openclaw server), send a message in any channel the bot monitors. Verify the bot responds.

**Step 3: Verify cron scheduler is active**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman logs openclaw-gateway 2>&1 | grep -i cron"
```

Expected: Cron scheduler started, jobs loaded

**Step 4: No commit** — Verification

---

### Task 9: Verify MailClaw Email Pipeline

**Context:** MailClaw cron jobs need Himalaya accessible inside the container at `/usr/local/bin/himalaya`.

**Step 1: Verify Himalaya is accessible inside the container**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman exec openclaw-gateway /usr/local/bin/himalaya --version"
```

Expected: `himalaya 1.2.0`

**Step 2: Verify Himalaya config is mounted**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman exec openclaw-gateway ls -la /home/node/.config/himalaya/config.toml"
```

Expected: File exists, readable

**Step 3: Test email access from inside the container**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman exec openclaw-gateway /usr/local/bin/himalaya -c /home/node/.config/himalaya/config.toml envelope list -a suhteevah --page-size 3"
```

Expected: List of recent emails

**Step 4: Manually trigger the MailClaw triage cron to verify end-to-end**

Check if the gateway provides a way to trigger a cron job (via logs or API). Or simply wait for the next 30-minute triage cycle and watch `#mailclaw` in Discord.

**Step 5: No commit** — Verification

---

### Task 10: Kill the Windows Gateway

**Context:** Once CNC-Server gateway is confirmed working, shut down the Windows gateway permanently.

**Step 1: Kill the running gateway process on Kokonoe**

```powershell
Get-Process -Id 101792 -ErrorAction SilentlyContinue | Stop-Process -Force
# Or find and kill any openclaw gateway:
Get-Process node | Where-Object { (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine -match 'openclaw.*gateway' } | Stop-Process -Force
```

**Step 2: Disable the Windows Scheduled Task**

```powershell
Disable-ScheduledTask -TaskName "OpenClaw Gateway" -ErrorAction SilentlyContinue
# Or:
schtasks /Change /TN "OpenClaw Gateway" /Disable
```

**Step 3: Verify no gateway running on Kokonoe**

```bash
curl -s http://localhost:18789/healthz
```

Expected: Connection refused (gateway is gone from Windows)

**Step 4: Verify CNC-Server gateway is still serving**

```bash
curl -s http://192.168.168.100:18789/healthz
```

Expected: HTTP 200

**Step 5: No commit** — Cleanup

---

### Task 11: Open Firewall Port on CNC-Server

**Context:** Port 18789 needs to be accessible from the LAN and Tailscale. CNC-Server uses firewalld.

**Step 1: Open the port**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "firewall-cmd --add-port=18789/tcp --permanent && firewall-cmd --add-port=18790/tcp --permanent && firewall-cmd --reload && echo 'done'"
```

Expected: `done`

**Step 2: Verify**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "firewall-cmd --list-ports"
```

Expected: `50052/tcp 18789/tcp 18790/tcp` (50052 was already open for llama RPC)

**Step 3: No commit** — Firewall config

---

### Task 12: Update MEMORY.md

**Context:** Update project memory to reflect the new architecture.

**Step 1: Update MEMORY.md**

Update the following sections:
- OpenClaw Gateway is now on CNC-Server (not Kokonoe)
- MailClaw + Himalaya running in container on CNC-Server
- Port 18789 on CNC-Server for gateway access
- Windows Scheduled Task disabled
- Add the Himalaya Linux binary path and config location

**Step 2: Commit**

```bash
git add MEMORY.md
git commit -m "docs: update MEMORY.md for OpenClaw CNC-Server consolidation"
```

---

### Task 13: Verify All 5 Cron Jobs Fire Correctly

**Context:** Monitor over the next few hours to confirm all cron jobs work.

**Verification checklist:**
- [ ] MailClaw Email Triage (every 30 min) → delivers to Discord #mailclaw
- [ ] MailClaw Morning Digest (6am PST) → delivers to Discord #mailclaw
- [ ] MailClaw Evening Wrap-up (6pm PST) → delivers to Discord #mailclaw
- [ ] Daily Briefing (6am PST) → delivers to Discord #briefing
- [ ] Daily Context Compilation (3am PST) → runs internally

**Step 1: Watch the next triage run**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman logs -f openclaw-gateway 2>&1 | grep -i 'cron\|mailclaw\|triage'"
```

Wait up to 30 minutes. Expected: Cron fires, MailClaw agent runs, message delivered to Discord.

**Step 2: If triage doesn't fire, check cron state**

```bash
ssh -o ConnectTimeout=5 root@192.168.168.100 "podman exec openclaw-gateway cat /home/node/.openclaw/cron/jobs.json | head -20"
```

Verify `enabled: true` and `nextRunAtMs` is in the future.

---

## Rollback Plan

If the CNC-Server gateway fails:

1. Stop the container: `ssh root@192.168.168.100 "podman stop openclaw-gateway"`
2. Re-enable Windows Scheduled Task: `Enable-ScheduledTask -TaskName "OpenClaw Gateway"`
3. Start Windows gateway: Run `C:\Users\Matt\.openclaw\gateway.cmd`

The Windows config is unchanged — we copied files, didn't move them.

---

## Post-Migration Architecture

```
CNC-Server (192.168.168.100 / Tailscale 100.108.202.49)
├── openclaw-gateway       ← Discord, Telegram, Cron, MailClaw, Himalaya
├── openclaw-core          ← API routing, LLM proxy
├── openclaw-redis         ← Session cache
├── openclaw-postgres      ← Persistent data
├── openclaw-caddy         ← Reverse proxy
├── openclaw-seo-auditor   ← Agent 1
├── openclaw-lead-responder ← Agent 2
├── openclaw-content-mill  ← Agent 3
├── openclaw-proposal-gen  ← Agent 4
├── openclaw-job-hunter    ← Agent 5
├── openclaw-client-dashboard ← Agent 6
├── openclaw-wow-economy   ← Agent 7
├── openclaw-prometheus    ← Metrics
├── openclaw-grafana       ← Dashboards
├── openclaw-redis-exporter
├── openclaw-postgres-exporter
└── openclaw-cadvisor      ← Container metrics

Kokonoe (Windows)
├── llama-server           ← Local LLM inference (3B/7B models)
├── rpc-server             ← CUDA RPC worker (RTX 3070 Ti)
└── Claude Code            ← Your dev environment (this session)

Total: 17 containers on CNC-Server, 0 OpenClaw on Kokonoe
```
