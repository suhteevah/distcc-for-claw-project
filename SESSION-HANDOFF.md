# Session Handoff — Complete Project Context

Everything a new Claude Code session needs to continue work on this project.
Read this entire file before doing anything.

---

## What This Project Is

**distcc-for-claw-project** is a deployment repo for a **Claude Code agent mesh** +
**distributed compilation cluster** (icecream/distcc). It provisions fleets of
machines — Linux, macOS, Windows, Raspberry Pi — into a coordinated network where:

- **Claude Code agents** run headless on every node via AgentAPI
- **An orchestrator** (claude-code-by-agents, Deno) dispatches tasks to agents
- **Icecream** distributes C/C++ compilation across all nodes
- **Tailscale** provides the mesh VPN connecting everything
- **Ollama** provides local LLM inference (on machines with GPUs)
- **OpenClaw** provides a gateway/dashboard for the whole thing

The repo lives at: `https://github.com/suhteevah/distcc-for-claw-project`

---

## The Three Deployments

There are three independent fleet deployments in this repo:

### 1. Matt's Fleet (root of repo)

| Machine | Hostname | Role |
|---------|----------|------|
| Arch Linux (i7-4790K, 32GB, GTX 980) | `arch-orchestrator` | Central orchestrator + scheduler |
| MacBook 1 (Intel) | `macbook1` | Headless agent + worker |
| iMac (Intel) | `imac` | Headless agent + worker |
| MacBook 2 (Intel) | `macbook2` | Interactive workstation + worker |
| Raspberry Pi x3 | `rpi1`, `rpi2`, `rpi3` | Headless agents + workers |
| Windows Desktop | `windows-desktop` | Interactive + worker (WSL) |
| Windows Laptop | `windows-laptop` | Interactive + worker (WSL) |

Scripts: `setup-scripts/01-arch-orchestrator.sh` through `05-windows-workstation.ps1`
Docs: `DEPLOY.md`

### 2. Dr Paper / Swoop (deployments/swoop-dr-paper/)

Mirrors Matt's fleet architecture. Swoop's independent fleet.

| Machine | Hostname | Role |
|---------|----------|------|
| Linux box | `dr-paper` | Orchestrator + scheduler |
| MacBook 1 (Intel) | `swoop-macbook1` | Headless agent |
| iMac (Intel) | `swoop-imac` | Headless agent |
| MacBook 2 (Intel) | `swoop-macbook2` | Interactive workstation |
| Raspberry Pi x3 | `swoop-rpi1/2/3` | Headless agents |
| Windows Desktop | `swoop-windows-desktop` | Interactive |
| Windows Laptop | `swoop-windows-laptop` | Interactive |

Scripts: `deployments/swoop-dr-paper/setup-scripts/`
Docs: `deployments/swoop-dr-paper/DEPLOY.md`

### 3. FCP — First Choice Plastics (deployments/fcp/)

Lean starter deployment. Phased expansion.

| Phase | Machine | Hostname | Status |
|-------|---------|----------|--------|
| 1 (now) | Gaming Laptop (Windows) | `fcp-laptop` | Production |
| 2 (planned) | Raspberry Pi | `fcp-rpi` | Pending |
| 3 (if needed) | Mac Mini | `fcp-mac-mini` | Future |

Scripts: `deployments/fcp/setup-scripts/`
Docs: `deployments/fcp/DEPLOY.md`

---

## The Current Work: cnc-server on MicroOS

**This is the active development focus.** We're setting up a new orchestrator
on openSUSE MicroOS / Leap Micro (atomic/immutable OS with btrfs snapshots).

### Branch

```
claude/fix-microos-prompt-limit-NMNFT
```

Based on `master`. All cnc-server work happens here.

### The Machine

- **Role:** C&C (Command & Control) orchestrator — replaces the Arch box concept
- **OS:** openSUSE Leap Micro (MicroOS variant, atomic, btrfs, read-only root)
- **Tailscale hostname:** `cnc-server`
- **Status:** Being reinstalled from USB (Leap Micro installer)

### The Bootstrap Script

`cnc-server-bootstrap.sh` — fully unattended, zero interactive prompts.

**10 phases, auto-reboot between Phase 1 and 2:**

| Phase | What it does |
|-------|-------------|
| 1 | SSH + transactional-update (install packages into btrfs snapshot) → **auto-reboot** |
| 2 | Verify packages + Tailscale auth (uses baked-in pre-auth key) |
| 3 | Icecream scheduler + worker (distributed compilation) |
| 4 | GPU detection + Ollama (install local if GPU, otherwise use LAN) |
| 5 | Claude Code + AgentAPI + API key placeholder |
| 6 | Deno + claude-code-by-agents orchestrator |
| 7 | Model Load Optimizer plugin + OpenClaw config |
| 8 | Systemd services (claude-agentapi, claude-orchestrator) |
| 9 | Firewalld rules |
| 10 | Verification + cleanup auto-resume service |

**Auto-resume mechanism:** Phase 1 installs a oneshot systemd service
(`cnc-bootstrap-resume.service`) that re-runs the script after reboot.
The service removes itself when bootstrap completes.

### Secrets

Secrets are in `.secrets` (gitignored). The bootstrap sources this file.

```bash
# .secrets (not in git — see .secrets.example for template)
TS_AUTH_KEY="tskey-auth-kVHj9zhNNB11CNTRL-SeAkaSdz6e7quGLGcks9e7JUbherSdLk"
ANTHROPIC_API_KEY=""  # empty — using Ollama only
```

The script looks for secrets in this order:
1. Same directory as the script (`$SCRIPT_DIR/.secrets`)
2. `/root/.secrets`
3. `/etc/cnc-secrets`

If no `TS_AUTH_KEY` is found, the script exits with an error.

**Important:** Tailscale pre-auth keys expire after 90 days.
Generate new ones at: https://login.tailscale.com/admin/settings/keys

### Combustion (first-boot automation)

The `combustion/` directory contains files to drop onto the USB installer
for fully unattended first-boot setup:

- `combustion/script` — sets root password, copies bootstrap + secrets, installs oneshot service
- Copy `.secrets` and `cnc-server-bootstrap.sh` alongside it on the USB's combustion partition

**To prepare a combustion USB:**
```bash
# Mount the combustion partition on the Leap Micro USB
sudo mount /dev/sdX3 /mnt  # find the right partition with lsblk

# Copy files
cp combustion/script /mnt/combustion/
cp cnc-server-bootstrap.sh /mnt/combustion/
cp .secrets /mnt/combustion/

sudo umount /mnt
```

Then boot the target PC from the USB. It installs, reboots, and the bootstrap
runs automatically with zero human interaction.

---

## LAN Infrastructure

### Ollama Servers (LLM Inference)

No Anthropic API key is being used right now. All inference goes through Ollama
on these two machines via Tailscale MagicDNS:

| Machine | Tailscale Hostname | Ollama Endpoint | Role |
|---------|-------------------|-----------------|------|
| Satibook | `satibook` | `http://satibook:11434` | Primary Ollama server |
| Kokonoe | `kokonoe` | `http://kokonoe:11434` | Fallback Ollama server |

The cnc-server bootstrap configures:
- Primary: `http://satibook:11434`
- Fallback: `http://kokonoe:11434`
- Model: `qwen2.5-coder:7b` (default)

If the cnc-server has a discrete GPU, it also installs Ollama locally
and uses localhost as primary instead.

### Tailscale Mesh

All machines communicate over Tailscale. MagicDNS resolves hostnames
automatically (`cnc-server`, `satibook`, `kokonoe`, etc.).

The cnc-server's Tailscale auth key is in `.secrets`.

### Ports

| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 3284 | AgentAPI (Claude Code headless) | TCP |
| 8080 | Orchestrator Web UI (claude-code-by-agents) | TCP |
| 8765 | Icecream scheduler | TCP |
| 8766 | Icecream telnet monitor | TCP |
| 10245 | Icecream worker | TCP |
| 11434 | Ollama API | TCP |
| 18789 | OpenClaw gateway | TCP |

---

## Complete File Tree

```
distcc-for-claw-project/
├── .gitignore
├── .secrets                          # GITIGNORED — Tailscale key + API keys
├── .secrets.example                  # Template for .secrets
├── README.md                         # Repo overview (minimal)
├── DEPLOY.md                         # Matt's fleet deployment guide
├── DEPLOYMENTS.md                    # Index of all 3 deployments
├── SESSION-HANDOFF.md                # THIS FILE
│
├── cnc-server-bootstrap.sh           # ★ MicroOS orchestrator (ACTIVE WORK)
├── combustion/
│   └── script                        # Combustion first-boot for MicroOS USB
│
├── dr-paper-bootstrap.sh             # Dr Paper Linux orchestrator (standalone)
├── dr-paper.sh                       # Dr Paper shortcut
├── fcp-laptop-bootstrap.ps1          # FCP Windows laptop (standalone)
├── fcp-laptop.ps1                    # FCP laptop shortcut
├── fcp-mac-bootstrap.sh              # FCP Mac Mini (standalone)
├── fcp-mac.sh                        # FCP Mac shortcut
├── fcp-pi-bootstrap.sh               # FCP Raspberry Pi (standalone)
├── fcp-pi.sh                         # FCP Pi shortcut
├── go.sh                             # Generic setup entry point
├── imac-bootstrap.sh                 # iMac headless agent (standalone)
├── matt-windows-bootstrap.ps1        # Matt's Windows bootstrap
├── matt-windows.ps1                  # Matt's Windows shortcut
├── swoop-windows-bootstrap.ps1       # Swoop's Windows bootstrap
├── swoop-windows.ps1                 # Swoop's Windows shortcut
├── setup-icecream-wsl.sh             # Icecream setup for WSL2
│
├── setup-scripts/                    # Matt's fleet setup scripts
│   ├── 01-arch-orchestrator.sh       # Arch Linux orchestrator
│   ├── 02-macos-headless-agent.sh    # macOS headless (MacBook 1, iMac)
│   ├── 03-macos-workstation.sh       # macOS interactive (MacBook 2)
│   ├── 04-raspberry-pi.sh            # Raspberry Pi agent
│   └── 05-windows-workstation.ps1    # Windows workstation
│
├── service-files/                    # Matt's fleet service configs
│   ├── systemd/
│   │   ├── claude-agentapi.service
│   │   └── claude-orchestrator.service
│   └── launchd/
│       ├── com.claude.agentapi.plist
│       └── org.icecc.iceccd.plist
│
├── shared/                           # Shared modules sourced by scripts
│   ├── ollama-gpu-detect.sh          # GPU detection + Ollama model selection (bash)
│   └── ollama-gpu-detect.ps1         # GPU detection (PowerShell)
│
├── monitoring/                       # Matt's fleet monitoring
│   ├── fleet-health-check.sh         # Check all agent statuses
│   └── install-monitoring.sh         # Install monitoring on orchestrator
│
└── deployments/
    ├── swoop-dr-paper/               # Swoop's deployment
    │   ├── DEPLOY.md
    │   ├── setup-scripts/
    │   │   ├── 01-linux-orchestrator.sh
    │   │   ├── 02-macos-headless-agent.sh
    │   │   ├── 03-macos-workstation.sh
    │   │   ├── 04-raspberry-pi.sh
    │   │   └── 05-windows-workstation.ps1
    │   ├── service-files/
    │   │   ├── systemd/
    │   │   │   ├── claude-agentapi.service
    │   │   │   └── claude-orchestrator.service
    │   │   └── launchd/
    │   │       ├── com.claude.agentapi.plist
    │   │       └── org.icecc.iceccd.plist
    │   └── monitoring/
    │       ├── fleet-health-check.sh
    │       └── install-monitoring.sh
    │
    ├── swoop-dr-paper.7z             # Archived copy of swoop deployment
    │
    └── fcp/                          # First Choice Plastics deployment
        ├── DEPLOY.md
        ├── setup-scripts/
        │   ├── 01-windows-primary.ps1
        │   ├── 01b-enable-orchestrator.ps1
        │   ├── 02-raspberry-pi.sh
        │   └── 03-mac-mini.sh
        ├── service-files/
        │   └── systemd/
        │       └── claude-agentapi.service
        └── monitoring/
            └── fleet-health-check.sh
```

---

## Git State

### Branches

| Branch | Purpose |
|--------|---------|
| `master` | Stable base (local) |
| `main` | Remote default (same as master) |
| `claude/fix-microos-prompt-limit-NMNFT` | **Active** — cnc-server MicroOS work |

### Recent Commits (on fix branch)

```
b617f99 Add combustion first-boot directory (WIP)
2170371 Rewrite bootstrap as fully unattended combustion script
9bdc447 Fix MicroOS bootstrap blocking on Leap Micro: add non-interactive mode
d32edb6 Replace broken PayPal link with Ko-fi donation button
c44cad0 Initial commit - uploaded via github-uploader-buildout
dd52f02 Split Phase 1 packages into core + optional groups
dccd961 Fix symlink bug, add --allow-write, improve dep caching
f62e972 Fix deno permission denied: install system-wide to /usr/local/bin
a3c839e Fix orchestrator crash: wrong DENO_DIR, missing --claude-path, no --host
25b6681 Fix headless auth: replace broken OAuth flow with API key validation
656e508 Fix snapshot branching: chain transactional-update with --continue
a4e79e7 Integrate Swoop's field-tested MicroOS fixes
c310d9d C&C script: ensure SSH is enabled before reboot
ae9d857 C&C script: handle no-GPU, default to LAN Ollama (192.168.10.242)
1ebabe2 Rewrite C&C bootstrap for openSUSE MicroOS (atomic, hardened)
1b9aff9 Add C&C server bootstrap for Ubuntu Server 24.04 LTS
```

### Remote

```
origin → https://github.com/suhteevah/distcc-for-claw-project
```

Push to: `git push -u origin claude/fix-microos-prompt-limit-NMNFT`

---

## What's In Progress Right Now

The user is **reinstalling Leap Micro on the cnc-server machine from a USB drive**.
The USB is currently plugged into **kokonoe** (one of the Ollama LAN machines).

### What needs to happen next

1. **Prepare the USB combustion partition** — copy `combustion/script`,
   `cnc-server-bootstrap.sh`, and `.secrets` onto the USB's combustion partition.
   This must be done from kokonoe's actual terminal (not this container).

2. **Boot the target PC from the USB** — Leap Micro installs, reboots,
   combustion runs `script` which stages the bootstrap, reboots again,
   and the bootstrap runs Phases 1-10 automatically.

3. **Verify** — after bootstrap completes:
   - `tailscale ping cnc-server` from satibook/kokonoe
   - `curl http://cnc-server:8080` (orchestrator UI)
   - `curl http://cnc-server:3284/status` (AgentAPI)
   - `journalctl -u claude-agentapi -f` on cnc-server

4. **Add Anthropic API key later** (optional, when needed):
   ```bash
   ssh cnc-server
   echo 'ANTHROPIC_API_KEY=sk-ant-...' > /etc/claude/api-key
   systemctl restart claude-agentapi
   ```

### Commands for the user to run on kokonoe

```bash
# 1. Find the USB
lsblk -o NAME,SIZE,LABEL,FSTYPE,MOUNTPOINT

# 2. Mount the combustion partition (usually partition 3 or labeled "combustion")
sudo mkdir -p /mnt/usb
sudo mount /dev/sdX3 /mnt/usb  # replace sdX3

# 3. Set up combustion files
sudo mkdir -p /mnt/usb/combustion
sudo cp ~/distcc-for-claw-project/combustion/script /mnt/usb/combustion/
sudo cp ~/distcc-for-claw-project/cnc-server-bootstrap.sh /mnt/usb/combustion/
sudo cp ~/distcc-for-claw-project/.secrets /mnt/usb/combustion/

# 4. Unmount and move USB to target PC
sudo umount /mnt/usb
```

Then plug the USB into the target PC and boot from it.

---

## Key Design Decisions

- **No Anthropic API key** — inference runs through Ollama on satibook/kokonoe.
  The API key can be added later if needed. The systemd services use
  `EnvironmentFile=-` (dash prefix) so they don't crash without one.

- **Tailscale pre-auth key baked in** — stored in `.secrets` (gitignored),
  sourced by the bootstrap at runtime. No interactive prompts.

- **MicroOS atomic updates** — packages install via `transactional-update`
  into btrfs snapshots. A reboot activates the new snapshot. The script
  handles this reboot automatically.

- **Auto-resume after reboot** — a oneshot systemd service
  (`cnc-bootstrap-resume.service`) re-runs the script after the Phase 1
  reboot. It cleans itself up after Phase 10.

- **Ollama model routing** — the OpenClaw config + Model Load Optimizer
  plugin handle routing requests to satibook (primary) or kokonoe (fallback).
  Default model: `qwen2.5-coder:7b`.

---

## Software Stack Reference

| Component | What it is | Where it lives |
|-----------|-----------|---------------|
| Claude Code | Anthropic's CLI agent | `npm -g @anthropic-ai/claude-code` → `/usr/local/bin/claude` |
| AgentAPI | Headless wrapper for Claude Code | Binary at `/usr/local/bin/agentapi` (from github.com/coder/agentapi) |
| claude-code-by-agents | Multi-agent orchestrator (Deno) | `/opt/claude-code-by-agents` (github.com/baryhuang/claude-code-by-agents) |
| Ollama | Local LLM server | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Tailscale | Mesh VPN | System package |
| Icecream | Distributed C/C++ compilation | System package (openSUSE invented it) |
| Deno | JS/TS runtime for orchestrator | `/usr/local/bin/deno` |
| OpenClaw | Gateway + dashboard | Config at `/home/claude-agent/.openclaw/openclaw.json` |
| Model Load Optimizer | Ollama routing plugin | `/home/claude-agent/.openclaw/plugins/model-load-optimizer` (github.com/suhteevah/model-load-optimizer) |
| Firewalld | Firewall | System service |
| Podman | Container runtime (Docker alternative) | System package |

---

## Budget Caps (per session)

| Role | Max $/session |
|------|--------------|
| Orchestrator | $20 |
| Standard worker (Mac/Linux) | $10 |
| Raspberry Pi | $5 |
| Human workstation | $5 |

Set in AgentAPI ExecStart: `--max-budget-usd 10.00`

---

## Troubleshooting

### Bootstrap fails after reboot
```bash
# Check what phase it's on
cat /root/.cnc-bootstrap-state

# Check the auto-resume service
journalctl -u cnc-bootstrap-resume -e

# Re-run manually
sudo bash /root/cnc-server-bootstrap.sh
```

### Tailscale auth fails
Pre-auth key may be expired (90-day default). Generate a new one:
https://login.tailscale.com/admin/settings/keys

Update `.secrets` and re-run bootstrap, or manually:
```bash
tailscale up --hostname cnc-server --authkey tskey-auth-NEWKEY
```

### Packages missing after reboot
MicroOS transactional-update creates btrfs snapshots. If packages are missing,
the snapshot wasn't activated:
```bash
snapper list              # see snapshots
transactional-update pkg install <package>
reboot                    # activates new snapshot
```

### Ollama unreachable from cnc-server
Verify Tailscale is connected and MagicDNS works:
```bash
tailscale ping satibook
curl http://satibook:11434/api/tags   # should list models
curl http://kokonoe:11434/api/tags    # fallback
```

### Services not starting
```bash
systemctl status claude-agentapi
systemctl status claude-orchestrator
journalctl -u claude-agentapi -e --no-pager
journalctl -u claude-orchestrator -e --no-pager

# Common fix: API key missing (service starts but claude errors)
echo 'ANTHROPIC_API_KEY=sk-ant-...' > /etc/claude/api-key
systemctl restart claude-agentapi
```
