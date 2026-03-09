---
name: cnc
description: Control the fleet — check status, dispatch tasks, SSH into hosts, manage services. Use when the user wants to interact with cnc-server, kokonoe, faye, or any fleet host.
user-invocable: true
allowed-tools: Bash(ssh *), Bash(scp *), Bash(curl *), Bash(tailscale *), Bash(./cnc-remote.sh *), Bash(./cnc-cmd.sh *), Read, Grep
---

# Fleet Command Center

You are the fleet controller for a Claude Code agent mesh. The user can issue
commands to any host in the fleet from this session.

## Host Registry

Read the current fleet config:

!`cat cnc-hosts.conf 2>/dev/null || echo "No cnc-hosts.conf found"`

## Available Tools

Two scripts are available in this repo:

- **`./cnc-cmd.sh <command>`** — Run locally (if this machine is in the fleet)
- **`./cnc-remote.sh [-H host] <command>`** — Run on a remote host via SSH

### Commands

| Command | What it does |
|---------|-------------|
| `status` | Full fleet status (agents, services, network, ollama) |
| `agents` | Check all agent endpoints |
| `services` | Check systemd services on a host |
| `ping [host]` | Tailscale ping all hosts or a specific one |
| `ollama` | Check Ollama availability across the fleet |
| `icecc` | Icecream distributed compilation status |
| `task "msg"` | Send a task to the local agent via AgentAPI |
| `dispatch <host> "msg"` | Send a task to a remote host's agent |
| `ssh <host> [cmd]` | SSH into a fleet host or run a command |
| `logs [service]` | Tail service logs (default: claude-agentapi) |
| `restart [service]` | Restart a service |
| `bootstrap` | Show bootstrap phase state |
| `hosts` | List all known hosts |

### Examples

```bash
# Check fleet health
./cnc-remote.sh status
./cnc-remote.sh -H kokonoe status

# Send a task to an agent
./cnc-remote.sh task "review the PR and summarize changes"
./cnc-remote.sh dispatch rpi1 "run the test suite"

# SSH into a host
./cnc-remote.sh -H faye shell
./cnc-remote.sh -H kokonoe ssh faye   # hop: this → kokonoe → faye

# Check Ollama on a specific host
./cnc-remote.sh -H kokonoe ollama

# Restart a service
./cnc-remote.sh -H cnc-server restart claude-agentapi

# Direct SSH command (no wrapper needed)
ssh root@kokonoe "systemctl status ollama"
ssh root@faye "uptime"
```

## How to Handle User Requests

When the user says things like:
- "check status" → run `./cnc-remote.sh status`
- "is kokonoe up?" → run `./cnc-remote.sh -H kokonoe ping` or `tailscale ping kokonoe`
- "send a task to rpi1" → run `./cnc-remote.sh dispatch rpi1 "the task"`
- "restart the agent on cnc-server" → run `./cnc-remote.sh -H cnc-server restart claude-agentapi`
- "SSH into faye" → run `./cnc-remote.sh -H faye shell`
- "what's ollama doing?" → run `./cnc-remote.sh ollama`
- "deploy the toolkit" → run `./cnc-remote.sh install-all`

For anything not covered by the toolkit, use direct SSH:
```bash
ssh root@<host> "<command>"
```

## Environment

- All hosts connect via **Tailscale** mesh VPN with MagicDNS
- SSH user is `root` by default (override with `-U`)
- AgentAPI runs on port **3284** on hosts with agents
- Orchestrator web UI on port **8080** on cnc-server
- Ollama API on port **11434**

$ARGUMENTS
