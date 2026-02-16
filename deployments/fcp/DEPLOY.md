# First Choice Plastics (FCP) -- Claude Code Deployment

## Overview

Starter deployment for First Choice Plastics. Begins with a single Windows gaming
laptop, with a clear upgrade path to add a Raspberry Pi and eventually a Mac Mini.

## Current Fleet

| Machine | Hostname | Role | Setup Script |
|---------|----------|------|-------------|
| Gaming Laptop (Windows) | `fcp-laptop` | Primary workstation + orchestrator | `01-windows-primary.ps1` |

## Planned Expansion

| Machine | Hostname | Role | Setup Script | Status |
|---------|----------|------|-------------|--------|
| Raspberry Pi | `fcp-rpi` | Headless agent + build worker | `02-raspberry-pi.sh fcp-rpi` | Pending acquisition |
| Mac Mini | `fcp-mac-mini` | Headless agent + build worker | `03-mac-mini.sh` | If things go well |

## Architecture (Phase 1 -- Laptop Only)

```
    [FCP User: Gaming Laptop]
              |
        Claude Code
        (interactive)
        fcp-laptop

    No distributed compilation yet.
    Single-machine setup with Tailscale
    pre-installed for future expansion.
```

## Architecture (Phase 2 -- Add Raspberry Pi)

```
    [FCP User: Gaming Laptop]
              |
        [AgentAPI :3284]
        fcp-laptop (orchestrator)
              |
        [AgentAPI :3284]
        fcp-rpi (headless agent + icecc worker)

        [Icecream Scheduler]
        fcp-laptop (WSL2) :8765
              |
        iceccd on fcp-rpi + WSL2
```

## Architecture (Phase 3 -- Add Mac Mini)

```
    [FCP User: Gaming Laptop]
              |
        [AgentAPI :3284]
        fcp-laptop (orchestrator)
              |
        +-----+-----+
        |           |
  [AgentAPI]  [AgentAPI]
  fcp-rpi     fcp-mac-mini
  :3284       :3284

  [Icecream Scheduler]
  fcp-mac-mini:8765 (promoted to scheduler)
        |
  iceccd on all 3 machines
```

## Prerequisites

### 1. Get an Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new key -- name it "fcp"
5. Copy the key (starts with `sk-ant-api03-...`)
6. Keep it safe -- you'll enter it during setup

## Deployment

### Phase 1: Gaming Laptop (do this now)

Run PowerShell as Administrator:
```powershell
.\setup-scripts\01-windows-primary.ps1
```

This installs:
- Tailscale (pre-positioned for future expansion)
- Node.js, Git, ripgrep
- Claude Code
- Claude Code authentication

After setup, use Claude Code interactively: just run `claude` in any terminal.

### Phase 2: Add Raspberry Pi (when acquired)

1. Flash 64-bit Raspberry Pi OS on the Pi
2. Copy this deployment folder to the Pi
3. Run:
```bash
chmod +x setup-scripts/02-raspberry-pi.sh
./setup-scripts/02-raspberry-pi.sh fcp-rpi
```
4. On the laptop, start the agent coordinator:
```powershell
.\setup-scripts\01b-enable-orchestrator.ps1
```

### Phase 3: Add Mac Mini (when ready)

1. Copy this deployment folder to the Mac Mini
2. Run:
```bash
chmod +x setup-scripts/03-mac-mini.sh
./setup-scripts/03-mac-mini.sh
```
3. The Mac Mini becomes an additional headless agent and build worker.
4. Optionally promote it to icecream scheduler (it's the most powerful stable node).

## Verification

### Phase 1
- [ ] `claude --version` works on the laptop
- [ ] `tailscale status` shows the laptop connected
- [ ] `claude` launches interactively and responds

### Phase 2 (after Pi)
- [ ] `tailscale ping fcp-rpi` from laptop succeeds
- [ ] `curl http://fcp-rpi:3284/status` returns OK
- [ ] Pi can receive and execute tasks from laptop

### Phase 3 (after Mac Mini)
- [ ] `tailscale ping fcp-mac-mini` from laptop succeeds
- [ ] `curl http://fcp-mac-mini:3284/status` returns OK
- [ ] `icecream-sundae` shows all 3 nodes in cluster

## Budget Caps

| Machine | Max $/session | Rationale |
|---------|--------------|-----------|
| Gaming Laptop | $10 | Primary machine, human-supervised |
| Raspberry Pi | $5 | Worker, limited resources |
| Mac Mini | $10 | Capable worker |
