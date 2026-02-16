# Dr Paper -- Swoop's Claude Code Agent Mesh + Distributed Compilation

## Overview

Dr Paper is the central command and control system for Swoop's Claude Code agent fleet.
Architecture mirrors the primary deployment with a dedicated Linux orchestrator.

## Fleet Overview

| Machine | Hostname | Role | Setup Script |
|---------|----------|------|-------------|
| Linux Box (orchestrator) | `dr-paper` | Central orchestrator + scheduler + worker | `01-linux-orchestrator.sh` |
| MacBook 1 (Intel) | `swoop-macbook1` | Headless agent + worker | `02-macos-headless-agent.sh swoop-macbook1` |
| iMac (Intel) | `swoop-imac` | Headless agent + worker | `02-macos-headless-agent.sh swoop-imac` |
| MacBook 2 (Intel) | `swoop-macbook2` | Interactive (human) + worker | `03-macos-workstation.sh` |
| Raspberry Pi 1 | `swoop-rpi1` | Headless agent + worker | `04-raspberry-pi.sh swoop-rpi1` |
| Raspberry Pi 2 | `swoop-rpi2` | Headless agent + worker | `04-raspberry-pi.sh swoop-rpi2` |
| Raspberry Pi 3 | `swoop-rpi3` | Headless agent + worker | `04-raspberry-pi.sh swoop-rpi3` |
| Windows Desktop | `swoop-windows-desktop` | Interactive (human) + worker (via WSL) | `05-windows-workstation.ps1` |
| Windows Laptop | `swoop-windows-laptop` | Interactive (human) + worker (via WSL) | `05-windows-workstation.ps1` |

## Architecture

```
              [Swoop: MacBook 2 / Windows Desktop / Windows Laptop]
                                    |
                          [Dr Paper Web UI]
                          dr-paper:8080
                                    |
                +-------+-------+-------+-------+
                |       |       |       |       |
            AgentAPI AgentAPI AgentAPI AgentAPI AgentAPI
            :3284    :3284    :3284    :3284    :3284
            swoop-   swoop-   swoop-   swoop-   swoop-
            macbook1  imac    rpi1    rpi2    rpi3
                |       |       |       |       |
            claude-p claude-p claude-p claude-p claude-p
            (headless agents with root access)

                      [Icecream Scheduler]
                      dr-paper:8765
                                |
            All machines run iceccd, jobs routed to fastest node
```

## Prerequisites

### 1. Get an Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new key -- name it "dr-paper" or "swoop-fleet"
5. Copy the key (starts with `sk-ant-api03-...`)
6. Keep it safe -- you'll enter it during setup on each machine

### 2. Network Requirements
All machines must be on the same network OR use Tailscale (recommended).
Tailscale is free for up to 100 devices: https://tailscale.com/

## Deployment Order

**Do these in order. Dr Paper (the Linux box) must be first.**

### Step 1: Network (all machines)
Install Tailscale on every machine:
```bash
# Linux: sudo pacman -S tailscale  OR  sudo apt install tailscale
#   OR:  curl -fsSL https://tailscale.com/install.sh | sh
# macOS: brew install --cask tailscale
# Windows: choco install tailscale  OR  download from tailscale.com
```
Then authenticate: `tailscale up --hostname <name-from-table-above>`

### Step 2: Dr Paper (Linux orchestrator -- FIRST!)
```bash
chmod +x setup-scripts/01-linux-orchestrator.sh
./setup-scripts/01-linux-orchestrator.sh
```

### Step 3: macOS Headless Agents
```bash
chmod +x setup-scripts/02-macos-headless-agent.sh
./setup-scripts/02-macos-headless-agent.sh swoop-macbook1   # on MacBook 1
./setup-scripts/02-macos-headless-agent.sh swoop-imac        # on iMac
```

### Step 4: macOS Workstation
```bash
chmod +x setup-scripts/03-macos-workstation.sh
./setup-scripts/03-macos-workstation.sh
```

### Step 5: Raspberry Pis (must be 64-bit!)
```bash
chmod +x setup-scripts/04-raspberry-pi.sh
./setup-scripts/04-raspberry-pi.sh swoop-rpi1   # on Pi 1
./setup-scripts/04-raspberry-pi.sh swoop-rpi2   # on Pi 2
./setup-scripts/04-raspberry-pi.sh swoop-rpi3   # on Pi 3
```

### Step 6: Windows Workstations
Run PowerShell as Administrator:
```powershell
.\setup-scripts\05-windows-workstation.ps1 -Hostname swoop-windows-desktop
.\setup-scripts\05-windows-workstation.ps1 -Hostname swoop-windows-laptop
```

### Step 7: Cross-Compilation Tarballs
From Dr Paper:
```bash
for host in swoop-macbook1 swoop-macbook2 swoop-imac swoop-rpi1 swoop-rpi2 swoop-rpi3; do
  ssh $host "sudo mkdir -p /opt/icecc-envs"
  scp /opt/icecc-envs/*.tar.gz ${host}:/opt/icecc-envs/
done
```

### Step 8: Monitoring
```bash
chmod +x monitoring/install-monitoring.sh
./monitoring/install-monitoring.sh
```

### Step 9: Register Agents in Dr Paper
Open `http://dr-paper:8080` and register:
- `http://localhost:3284` (dr-paper-local)
- `http://swoop-macbook1:3284`
- `http://swoop-imac:3284`
- `http://swoop-rpi1:3284`
- `http://swoop-rpi2:3284`
- `http://swoop-rpi3:3284`

## Verification Checklist

- [ ] `tailscale ping dr-paper` works from all nodes
- [ ] `icecream-sundae` on Dr Paper shows all nodes connected
- [ ] `curl http://swoop-macbook1:3284/status` returns OK
- [ ] `curl http://swoop-imac:3284/status` returns OK
- [ ] `curl http://swoop-rpi1:3284/status` returns OK
- [ ] Dr Paper web UI at `:8080` shows all registered agents
- [ ] Test compile distributes across cluster
- [ ] Test agent dispatch works end-to-end

## Budget Caps

| Machine | Max $/session | Rationale |
|---------|--------------|-----------|
| Dr Paper (orchestrator) | $20 | Task decomposition is token-heavy |
| MacBook 1 / iMac | $10 | Standard worker tasks |
| Raspberry Pis | $5 | Simpler tasks, limited resources |
| MacBook 2 / Windows (both) | $5 | Human-supervised |

## Useful Commands

```bash
# Fleet health check
fleet-health-check.sh

# Watch compilation
icecream-sundae

# Agent logs (Linux)
journalctl -u claude-agentapi -f

# Agent logs (macOS)
tail -f /tmp/claude-agentapi.log

# Send task to specific agent
curl -X POST http://swoop-macbook1:3284/message \
  -H 'Content-Type: application/json' \
  -d '{"content": "List files in the current directory"}'

# Restart agent (Linux)
sudo systemctl restart claude-agentapi

# Restart agent (macOS)
launchctl unload ~/Library/LaunchAgents/com.claude.agentapi.plist
launchctl load ~/Library/LaunchAgents/com.claude.agentapi.plist
```
