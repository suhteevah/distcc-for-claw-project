# distcc-for-claw-project

Deployment repo for a Claude Code agent mesh + distributed compilation cluster.
Read `SESSION-HANDOFF.md` for full project context.

## Fleet Command Center (SSH)

This repo includes tools for controlling any host in the fleet via SSH.
When the user asks to check status, dispatch tasks, SSH into hosts, restart
services, or interact with cnc-server/kokonoe/faye/any fleet host, use these tools.

### Fleet Hosts (from cnc-hosts.conf)

| Role | Hostname | Agent Port | Description |
|------|----------|-----------|-------------|
| orchestrator | cnc-server | 3284 | CNC Server (MicroOS orchestrator) |
| agent | macbook1 | 3284 | MacBook 1 (headless agent) |
| agent | imac | 3284 | iMac (headless agent) |
| agent | rpi1-3 | 3284 | Raspberry Pis |
| workstation | macbook2 | 3284 | MacBook 2 (interactive) |
| ollama | satibook | - | Primary Ollama LAN server |
| ollama | kokonoe | - | Fallback Ollama, general purpose |
| ollama | faye | - | Faye |

### How to Run Commands

Use `./cnc-remote.sh` to SSH into any host and run commands:

```bash
./cnc-remote.sh status                        # fleet status via cnc-server
./cnc-remote.sh -H kokonoe status             # status from kokonoe
./cnc-remote.sh -H faye shell                 # SSH shell into faye
./cnc-remote.sh task "review the PR"          # send task to cnc-server agent
./cnc-remote.sh dispatch rpi1 "run tests"     # send task to rpi1's agent
./cnc-remote.sh -H kokonoe ollama             # check Ollama on kokonoe
./cnc-remote.sh -H cnc-server restart claude-agentapi
./cnc-remote.sh install-all                   # deploy toolkit to entire fleet
```

Or use direct SSH for anything:
```bash
ssh root@kokonoe "systemctl status ollama"
ssh root@faye "uptime"
ssh root@cnc-server "cnc-cmd.sh agents"
```

### Translating User Requests

- "check status" / "how's the fleet" -> `./cnc-remote.sh status`
- "is kokonoe up?" -> `ssh root@kokonoe "uptime"` or `./cnc-remote.sh -H kokonoe ping`
- "send a task to rpi1" -> `./cnc-remote.sh dispatch rpi1 "the task"`
- "restart the agent" -> `./cnc-remote.sh -H cnc-server restart claude-agentapi`
- "SSH into faye" -> `ssh root@faye` (interactive)
- "what's ollama doing?" -> `./cnc-remote.sh -H kokonoe ollama`
- "deploy the toolkit" -> `./cnc-remote.sh install-all`

### Network

- All hosts on **Tailscale** mesh VPN with MagicDNS
- SSH user: `root` (default)
- AgentAPI: port **3284** | Orchestrator UI: port **8080** | Ollama: port **11434**
