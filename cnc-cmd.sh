#!/bin/bash
# =============================================================================
# cnc-cmd.sh — Modular Fleet Command Toolkit
# =============================================================================
# Run on any machine in the fleet. Reads host registry from cnc-hosts.conf.
# Works locally, over SSH, or via cnc-remote.sh.
#
# Usage:
#   cnc-cmd.sh <command> [args...]
#   cnc-cmd.sh                        # interactive menu (iPhone-friendly)
#
# Commands:
#   status              Full fleet status (agents, services, network)
#   agents              List all agent statuses from config
#   ping [host]         Tailscale ping (all hosts or specific)
#   task <msg>          Send a task to the local agent via AgentAPI
#   dispatch <host> <msg>   Send a task to a remote agent
#   ssh <host> [cmd]    SSH into any fleet host (or run a command)
#   logs [service]      Tail logs (default: claude-agentapi)
#   restart [service]   Restart a service
#   services            Show all CNC-related service statuses
#   ollama              Check Ollama availability (local + LAN)
#   icecc               Show Icecream cluster status
#   bootstrap           Show bootstrap state
#   hosts               List all known hosts from config
#   menu                Interactive menu (default if no args)
# =============================================================================

set -uo pipefail

# --- Resolve config file ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CNC_CONF="${CNC_CONF:-}"

# Search order for config: env var, same dir as script, /etc/cnc, home dir
if [ -z "$CNC_CONF" ]; then
  for candidate in \
    "${SCRIPT_DIR}/cnc-hosts.conf" \
    "/etc/cnc/cnc-hosts.conf" \
    "${HOME}/.cnc-hosts.conf"; do
    if [ -f "$candidate" ]; then
      CNC_CONF="$candidate"
      break
    fi
  done
fi

# --- Colors (skip if not a terminal) ---
if [ -t 1 ]; then
  GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'
  CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
else
  GREEN=''; RED=''; YELLOW=''; CYAN=''; BOLD=''; NC=''
fi

# --- Parse config into arrays ---
declare -a AGENT_ENTRIES=()      # "host:port|label" for hosts with agent_port > 0
declare -a ALL_HOSTS=()          # "hostname" for all unique hosts
declare -a OLLAMA_ENDPOINTS=()   # "host:port|label"
declare -a HOST_DESCRIPTIONS=()  # "hostname|role|description"

load_config() {
  if [ -z "$CNC_CONF" ] || [ ! -f "$CNC_CONF" ]; then
    # Fallback defaults if no config found
    AGENT_ENTRIES=("localhost:3284|cnc-local")
    ALL_HOSTS=("localhost")
    OLLAMA_ENDPOINTS=("localhost:11434|Local")
    return
  fi

  while IFS='|' read -r role hostname port description; do
    # Skip comments and blanks
    [[ "$role" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$role" ]] && continue
    role=$(echo "$role" | xargs)  # trim whitespace
    hostname=$(echo "$hostname" | xargs)
    port=$(echo "$port" | xargs)
    description=$(echo "$description" | xargs)

    case "$role" in
      ollama-endpoint)
        OLLAMA_ENDPOINTS+=("${hostname}|${description:-$hostname}")
        ;;
      *)
        # Track all unique hostnames for ping/network checks
        local found=0
        for h in "${ALL_HOSTS[@]+"${ALL_HOSTS[@]}"}"; do
          [ "$h" = "$hostname" ] && found=1 && break
        done
        [ "$found" -eq 0 ] && ALL_HOSTS+=("$hostname")

        # Track hosts with agents
        if [ "${port:-0}" -gt 0 ]; then
          AGENT_ENTRIES+=("${hostname}:${port}|${description:-$hostname}")
        fi

        HOST_DESCRIPTIONS+=("${hostname}|${role}|${description}")
        ;;
    esac
  done < "$CNC_CONF"
}

load_config

# --- Locally-relevant services (checked on whatever host runs this script) ---
CNC_SERVICES=(
  "claude-agentapi"
  "claude-orchestrator"
  "icecc-scheduler"
  "iceccd"
  "tailscaled"
  "ollama"
)

# --- Helper functions ---
ok()   { echo -e "  ${GREEN}[OK]${NC}   $*"; }
fail() { echo -e "  ${RED}[DOWN]${NC} $*"; }
warn() { echo -e "  ${YELLOW}[WARN]${NC} $*"; }
header() { echo -e "\n${BOLD}${CYAN}=== $* ===${NC}"; }

check_agent() {
  local endpoint="$1" name="$2"
  local resp
  resp=$(curl -s --connect-timeout 3 "http://${endpoint}/status" 2>/dev/null)
  if [ $? -eq 0 ] && [ -n "$resp" ]; then
    ok "${name}"
  else
    fail "${name}: unreachable"
  fi
}

# --- Commands ---
cmd_hosts() {
  header "Known Hosts (from ${CNC_CONF:-defaults})"
  printf "  ${BOLD}%-18s %-14s %s${NC}\n" "HOSTNAME" "ROLE" "DESCRIPTION"
  printf "  %-18s %-14s %s\n" "--------" "----" "-----------"
  for entry in "${HOST_DESCRIPTIONS[@]+"${HOST_DESCRIPTIONS[@]}"}"; do
    IFS='|' read -r hostname role desc <<< "$entry"
    printf "  %-18s %-14s %s\n" "$hostname" "$role" "$desc"
  done
}

cmd_agents() {
  header "Claude Code Agents"
  if [ ${#AGENT_ENTRIES[@]} -eq 0 ]; then
    warn "No agents configured"
    return
  fi
  for entry in "${AGENT_ENTRIES[@]}"; do
    IFS='|' read -r endpoint name <<< "$entry"
    check_agent "$endpoint" "$name"
  done
}

cmd_services() {
  header "Local Services ($(hostname 2>/dev/null || echo 'this host'))"
  for svc in "${CNC_SERVICES[@]}"; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
      ok "$svc: active"
    elif systemctl is-enabled --quiet "$svc" 2>/dev/null; then
      warn "$svc: enabled but not running"
    else
      fail "$svc: inactive"
    fi
  done
}

cmd_ping() {
  local target="${1:-}"
  if [ -n "$target" ]; then
    header "Tailscale Ping: $target"
    tailscale ping --timeout 3s "$target" 2>&1
  else
    header "Tailscale Network"
    for host in "${ALL_HOSTS[@]+"${ALL_HOSTS[@]}"}"; do
      [ "$host" = "localhost" ] && continue
      if tailscale ping --timeout 3s "$host" &>/dev/null; then
        ok "$host: reachable"
      else
        fail "$host: unreachable"
      fi
    done
  fi
}

cmd_ollama() {
  header "Ollama Availability"
  if [ ${#OLLAMA_ENDPOINTS[@]} -eq 0 ]; then
    warn "No Ollama endpoints configured"
    return
  fi
  for entry in "${OLLAMA_ENDPOINTS[@]}"; do
    IFS='|' read -r endpoint name <<< "$entry"
    local resp
    resp=$(curl -s --connect-timeout 3 "http://${endpoint}/api/tags" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$resp" ]; then
      local models
      models=$(echo "$resp" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"//' | tr '\n' ', ' | sed 's/,$//')
      ok "${name}: online — models: ${models:-none}"
    else
      fail "${name}: unreachable"
    fi
  done
}

cmd_icecc() {
  header "Icecream Cluster"
  if systemctl is-active --quiet icecc-scheduler 2>/dev/null; then
    ok "Scheduler: active"
    if command -v nc &>/dev/null; then
      echo -e "  Querying scheduler on port 8766..."
      echo "listcs" | nc -w 2 localhost 8766 2>/dev/null || warn "Could not query scheduler"
    fi
  else
    fail "Scheduler: not running"
  fi
  if systemctl is-active --quiet iceccd 2>/dev/null; then
    ok "Local worker (iceccd): active"
  else
    fail "Local worker (iceccd): not running"
  fi
}

cmd_task() {
  local message="${1:-}"
  if [ -z "$message" ]; then
    echo "Usage: cnc-cmd.sh task \"your task message\""
    return 1
  fi
  header "Sending Task to Local Agent"
  echo "  Message: $message"
  curl -s -X POST "http://localhost:3284/message" \
    -H "Content-Type: application/json" \
    -d "{\"message\": $(printf '%s' "$message" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$message\"")}" 2>/dev/null
  echo ""
}

cmd_dispatch() {
  local host="${1:-}" message="${2:-}"
  if [ -z "$host" ] || [ -z "$message" ]; then
    echo "Usage: cnc-cmd.sh dispatch <host> \"your task message\""
    echo ""
    echo "Available agent hosts:"
    for entry in "${AGENT_ENTRIES[@]+"${AGENT_ENTRIES[@]}"}"; do
      IFS='|' read -r endpoint name <<< "$entry"
      echo "  ${endpoint%%:*}  — $name"
    done
    return 1
  fi
  # Find the agent port for this host
  local port="3284"
  for entry in "${AGENT_ENTRIES[@]+"${AGENT_ENTRIES[@]}"}"; do
    IFS='|' read -r endpoint name <<< "$entry"
    local ehost="${endpoint%%:*}"
    if [ "$ehost" = "$host" ]; then
      port="${endpoint#*:}"
      break
    fi
  done
  header "Dispatching Task to ${host}:${port}"
  echo "  Message: $message"
  curl -s -X POST "http://${host}:${port}/message" \
    -H "Content-Type: application/json" \
    -d "{\"message\": $(printf '%s' "$message" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$message\"")}" 2>/dev/null
  echo ""
}

cmd_ssh() {
  local host="${1:-}"
  shift 2>/dev/null || true
  if [ -z "$host" ]; then
    echo "Usage: cnc-cmd.sh ssh <host> [command...]"
    echo ""
    echo "Known hosts:"
    for h in "${ALL_HOSTS[@]+"${ALL_HOSTS[@]}"}"; do
      [ "$h" = "localhost" ] && continue
      echo "  $h"
    done
    return 1
  fi
  if [ $# -gt 0 ]; then
    ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "root@${host}" "$@"
  else
    ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "root@${host}"
  fi
}

cmd_logs() {
  local service="${1:-claude-agentapi}"
  header "Logs: $service (last 50 lines, follow)"
  journalctl -u "$service" -n 50 -f --no-pager
}

cmd_restart() {
  local service="${1:-claude-agentapi}"
  header "Restarting: $service"
  sudo systemctl restart "$service"
  sleep 1
  if systemctl is-active --quiet "$service"; then
    ok "$service: restarted successfully"
  else
    fail "$service: failed to start"
    journalctl -u "$service" -n 10 --no-pager
  fi
}

cmd_bootstrap() {
  header "Bootstrap State"
  if [ -f /root/.cnc-bootstrap-state ]; then
    echo "  State file: /root/.cnc-bootstrap-state"
    echo "  Phase: $(cat /root/.cnc-bootstrap-state)"
  else
    ok "Bootstrap complete (no state file)"
  fi
  if systemctl is-enabled --quiet cnc-bootstrap-resume 2>/dev/null; then
    warn "Auto-resume service still enabled"
  fi
}

cmd_status() {
  echo -e "${BOLD}${CYAN}Fleet Status — $(date '+%Y-%m-%d %H:%M:%S')${NC}"
  echo -e "${CYAN}Host: $(hostname 2>/dev/null || echo unknown) | Uptime: $(uptime -p 2>/dev/null || uptime)${NC}"
  echo -e "${CYAN}Config: ${CNC_CONF:-built-in defaults}${NC}"
  cmd_agents
  cmd_services
  cmd_ollama
  cmd_ping
  cmd_icecc
}

# --- Interactive menu (iPhone-friendly) ---
cmd_menu() {
  while true; do
    echo ""
    echo -e "${BOLD}${CYAN}╔═══════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║      Fleet Command Center         ║${NC}"
    echo -e "${BOLD}${CYAN}╠═══════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC}  1) Full status overview            ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  2) Agent status                    ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  3) Service status                  ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  4) Ollama check                    ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  5) Network ping all                ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  6) Icecream cluster                ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  7) Send task to local agent        ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  8) Dispatch task to remote host    ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  9) SSH into a fleet host           ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  0) Tail logs                       ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  r) Restart a service               ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  h) List known hosts                ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  b) Bootstrap state                 ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  q) Quit                            ${CYAN}║${NC}"
    echo -e "${BOLD}${CYAN}╚═══════════════════════════════════╝${NC}"
    echo -n "  > "
    read -r choice

    case "$choice" in
      1) cmd_status ;;
      2) cmd_agents ;;
      3) cmd_services ;;
      4) cmd_ollama ;;
      5) cmd_ping ;;
      6) cmd_icecc ;;
      7)
        echo -n "  Task message: "
        read -r msg
        cmd_task "$msg"
        ;;
      8)
        echo "  Available hosts:"
        for entry in "${AGENT_ENTRIES[@]+"${AGENT_ENTRIES[@]}"}"; do
          IFS='|' read -r endpoint name <<< "$entry"
          echo "    ${endpoint%%:*} — $name"
        done
        echo -n "  Target host: "
        read -r host
        echo -n "  Task message: "
        read -r msg
        cmd_dispatch "$host" "$msg"
        ;;
      9)
        echo "  Known hosts:"
        for h in "${ALL_HOSTS[@]+"${ALL_HOSTS[@]}"}"; do
          [ "$h" = "localhost" ] && continue
          echo "    $h"
        done
        echo -n "  SSH to host: "
        read -r host
        cmd_ssh "$host"
        ;;
      0)
        echo "  Services: ${CNC_SERVICES[*]}"
        echo -n "  Which service? [claude-agentapi]: "
        read -r svc
        cmd_logs "${svc:-claude-agentapi}"
        ;;
      r|R)
        echo "  Services: ${CNC_SERVICES[*]}"
        echo -n "  Which service? [claude-agentapi]: "
        read -r svc
        cmd_restart "${svc:-claude-agentapi}"
        ;;
      h|H) cmd_hosts ;;
      b|B) cmd_bootstrap ;;
      q|Q) echo "  Bye."; exit 0 ;;
      *) echo "  Invalid choice." ;;
    esac
  done
}

# --- Main dispatch ---
case "${1:-menu}" in
  status)    cmd_status ;;
  agents)    cmd_agents ;;
  services)  cmd_services ;;
  ping)      cmd_ping "${2:-}" ;;
  ollama)    cmd_ollama ;;
  icecc)     cmd_icecc ;;
  task)      cmd_task "${2:-}" ;;
  dispatch)  cmd_dispatch "${2:-}" "${3:-}" ;;
  ssh)       shift; cmd_ssh "$@" ;;
  logs)      cmd_logs "${2:-}" ;;
  restart)   cmd_restart "${2:-}" ;;
  bootstrap) cmd_bootstrap ;;
  hosts)     cmd_hosts ;;
  menu)      cmd_menu ;;
  help|-h|--help)
    echo "Usage: cnc-cmd.sh <command> [args...]"
    echo ""
    echo "Config: ${CNC_CONF:-none found (using defaults)}"
    echo ""
    echo "Commands:"
    echo "  status              Full fleet status"
    echo "  agents              Agent status check"
    echo "  services            Local service status"
    echo "  ping [host]         Tailscale ping (all or specific)"
    echo "  ollama              Ollama availability"
    echo "  icecc               Icecream cluster status"
    echo "  task \"message\"      Send task to local agent"
    echo "  dispatch host msg   Send task to a remote agent"
    echo "  ssh host [cmd]      SSH into any fleet host"
    echo "  logs [service]      Tail service logs"
    echo "  restart [service]   Restart a service"
    echo "  bootstrap           Bootstrap state"
    echo "  hosts               List all known hosts"
    echo "  menu                Interactive menu (default)"
    echo "  help                This help"
    echo ""
    echo "Environment:"
    echo "  CNC_CONF   Path to cnc-hosts.conf (auto-detected)"
    ;;
  *)
    echo "Unknown command: $1"
    echo "Run 'cnc-cmd.sh help' for usage."
    exit 1
    ;;
esac
