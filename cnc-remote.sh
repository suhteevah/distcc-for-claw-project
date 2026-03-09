#!/bin/bash
# =============================================================================
# cnc-remote.sh — SSH into any fleet host and run commands
# =============================================================================
# Use from your iPhone (Termius/Blink), laptop, or this Claude Code window
# to remotely control any machine in the fleet over Tailscale.
#
# Usage:
#   cnc-remote.sh                              # SSH to cnc-server, interactive menu
#   cnc-remote.sh status                       # Run status on cnc-server
#   cnc-remote.sh -H kokonoe status            # Run status on kokonoe
#   cnc-remote.sh -H faye shell                # SSH shell into faye
#   cnc-remote.sh install                      # Deploy toolkit to cnc-server
#   cnc-remote.sh install-all                  # Deploy toolkit to all hosts
#   cnc-remote.sh task "fix the bug"           # Send task via cnc-server
#
# Target any host with -H:
#   cnc-remote.sh -H kokonoe ollama            # Check Ollama on kokonoe
#   cnc-remote.sh -H faye services             # Check services on faye
#   cnc-remote.sh -H rpi1 agents               # Check agents from rpi1
#
# Prerequisites:
#   - Tailscale running on this machine
#   - SSH access to target host (key-based or password)
#   - cnc-cmd.sh deployed on target (use 'install' to deploy)
#
# iPhone Setup:
#   1. Install Termius or Blink Shell from the App Store
#   2. Add hosts: cnc-server, kokonoe, faye (Tailscale MagicDNS)
#   3. Set auth: SSH key or password
#   4. Run: /usr/local/bin/cnc-cmd.sh   (launches interactive menu)
#
# =============================================================================

set -uo pipefail

# --- Parse -H flag before anything else ---
TARGET_HOST="${CNC_HOST:-cnc-server}"
TARGET_USER="${CNC_USER:-root}"

while getopts "H:U:" opt; do
  case "$opt" in
    H) TARGET_HOST="$OPTARG" ;;
    U) TARGET_USER="$OPTARG" ;;
    *) ;;
  esac
done
shift $((OPTIND - 1))

# --- Config ---
CNC_CMD_PATH="/usr/local/bin/cnc-cmd.sh"
CNC_CONF_PATH="/etc/cnc/cnc-hosts.conf"
SSH_OPTS="-o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_CNC_CMD="${SCRIPT_DIR}/cnc-cmd.sh"
LOCAL_CNC_CONF="${SCRIPT_DIR}/cnc-hosts.conf"

# --- Colors ---
if [ -t 1 ]; then
  GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'
  YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
else
  GREEN=''; RED=''; CYAN=''; YELLOW=''; BOLD=''; NC=''
fi

# --- Parse hosts from local config for install-all ---
get_all_hosts() {
  if [ ! -f "$LOCAL_CNC_CONF" ]; then
    echo "cnc-server"
    return
  fi
  while IFS='|' read -r role hostname _port _desc; do
    [[ "$role" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$role" ]] && continue
    role=$(echo "$role" | xargs)
    hostname=$(echo "$hostname" | xargs)
    [ "$role" = "ollama-endpoint" ] && continue
    echo "$hostname"
  done < "$LOCAL_CNC_CONF" | sort -u
}

# --- Functions ---
ssh_cmd() {
  local host="$1"; shift
  local user="$2"; shift 2>/dev/null || true
  # shellcheck disable=SC2086
  ssh $SSH_OPTS "${TARGET_USER}@${host}" "$@"
}

check_connection() {
  local host="$1"
  echo -e "${CYAN}Connecting to ${host}...${NC}"
  if command -v tailscale &>/dev/null; then
    if ! tailscale ping --timeout 5s "$host" &>/dev/null 2>&1; then
      # Tailscale ping failed, try direct SSH anyway (might be on same LAN)
      echo -e "${YELLOW}Tailscale ping failed, trying direct SSH...${NC}"
      return 0
    fi
  fi
  echo -e "${GREEN}Reachable.${NC}"
}

cmd_install() {
  local host="${1:-$TARGET_HOST}"
  echo -e "${BOLD}${CYAN}Deploying toolkit to ${host}...${NC}"

  if [ ! -f "$LOCAL_CNC_CMD" ]; then
    echo -e "${RED}cnc-cmd.sh not found at ${LOCAL_CNC_CMD}${NC}"
    exit 1
  fi

  check_connection "$host"

  # Deploy cnc-cmd.sh
  # shellcheck disable=SC2086
  scp $SSH_OPTS "$LOCAL_CNC_CMD" "${TARGET_USER}@${host}:${CNC_CMD_PATH}"
  # shellcheck disable=SC2086
  ssh $SSH_OPTS "${TARGET_USER}@${host}" "chmod +x ${CNC_CMD_PATH}"

  # Deploy config file if it exists
  if [ -f "$LOCAL_CNC_CONF" ]; then
    # shellcheck disable=SC2086
    ssh $SSH_OPTS "${TARGET_USER}@${host}" "mkdir -p /etc/cnc"
    # shellcheck disable=SC2086
    scp $SSH_OPTS "$LOCAL_CNC_CONF" "${TARGET_USER}@${host}:${CNC_CONF_PATH}"
    echo -e "${GREEN}Config deployed to ${host}:${CNC_CONF_PATH}${NC}"
  fi

  echo -e "${GREEN}Toolkit deployed to ${host}:${CNC_CMD_PATH}${NC}"
}

cmd_install_all() {
  echo -e "${BOLD}${CYAN}Deploying toolkit to all fleet hosts...${NC}"
  local hosts
  hosts=$(get_all_hosts)
  for host in $hosts; do
    [ "$host" = "localhost" ] && continue
    echo ""
    cmd_install "$host" || warn "Failed to deploy to $host (skipping)"
  done
  echo ""
  echo -e "${GREEN}Done. Toolkit deployed to all reachable hosts.${NC}"
}

cmd_shell() {
  check_connection "$TARGET_HOST"
  echo -e "${CYAN}Opening SSH shell to ${TARGET_HOST}...${NC}"
  # shellcheck disable=SC2086
  ssh $SSH_OPTS "${TARGET_USER}@${TARGET_HOST}"
}

cmd_run() {
  check_connection "$TARGET_HOST"
  # shellcheck disable=SC2086
  ssh $SSH_OPTS "${TARGET_USER}@${TARGET_HOST}" "${CNC_CMD_PATH}" "$@"
}

# --- Main ---
case "${1:-}" in
  "")
    # No args = interactive menu over SSH
    check_connection "$TARGET_HOST"
    echo -e "${CYAN}Launching interactive menu on ${TARGET_HOST}...${NC}"
    # shellcheck disable=SC2086
    ssh $SSH_OPTS -t "${TARGET_USER}@${TARGET_HOST}" "${CNC_CMD_PATH} menu"
    ;;
  install)
    cmd_install "${2:-$TARGET_HOST}"
    ;;
  install-all)
    cmd_install_all
    ;;
  shell)
    cmd_shell
    ;;
  help|-h|--help)
    echo "Usage: cnc-remote.sh [-H host] [-U user] [command] [args...]"
    echo ""
    echo "SSH wrapper for running cnc-cmd.sh on any fleet host."
    echo "Default target: ${TARGET_HOST} (override with -H or CNC_HOST env)"
    echo ""
    echo "  (no args)           Launch interactive menu on target host"
    echo "  shell               Open a plain SSH shell"
    echo "  install [host]      Deploy toolkit to a host (default: target)"
    echo "  install-all         Deploy toolkit to all hosts in cnc-hosts.conf"
    echo "  status              Full fleet status"
    echo "  agents              Agent status check"
    echo "  services            Service status check"
    echo "  task \"message\"      Send task to the agent on target host"
    echo "  dispatch host msg   Send task to a remote agent"
    echo "  ssh host [cmd]      SSH hop to another host"
    echo "  hosts               List all known hosts"
    echo "  logs [service]      Tail service logs"
    echo "  restart [service]   Restart a service"
    echo "  help                This help"
    echo ""
    echo "Flags:"
    echo "  -H host   Target host (default: cnc-server, or CNC_HOST env)"
    echo "  -U user   SSH user (default: root, or CNC_USER env)"
    echo ""
    echo "Examples:"
    echo "  cnc-remote.sh                         # menu on cnc-server"
    echo "  cnc-remote.sh -H kokonoe status       # status from kokonoe"
    echo "  cnc-remote.sh -H faye ollama          # ollama check on faye"
    echo "  cnc-remote.sh -H rpi1 shell           # SSH shell into rpi1"
    echo "  cnc-remote.sh install-all             # deploy to entire fleet"
    echo ""
    echo "iPhone quick-start:"
    echo "  1. Install Termius or Blink Shell"
    echo "  2. Add host: cnc-server (or any host, via Tailscale)"
    echo "  3. Run: cnc-cmd.sh  (interactive menu)"
    ;;
  *)
    cmd_run "$@"
    ;;
esac
