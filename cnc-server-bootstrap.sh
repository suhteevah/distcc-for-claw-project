#!/bin/bash
set -euo pipefail

# =============================================================================
# C&C Server Bootstrap — openSUSE MicroOS / Leap Micro  (Unattended)
#
# Fully non-interactive. Designed for combustion first-boot.
# All configuration is hardcoded below — flash and boot.
#
# After first boot:
#   Phase 1 installs packages, installs a oneshot systemd service for
#   auto-resume, and reboots. The rest finishes automatically on second boot.
#
# What this sets up:
#   - Tailscale mesh VPN (pre-auth key baked in)
#   - Icecream scheduler + local worker (distributed compilation)
#   - Claude Code + AgentAPI (headless AI agent)
#   - claude-code-by-agents orchestrator (multi-agent dispatch)
#   - LAN Ollama via Tailscale (satibook / kokonoe — no Anthropic key needed)
#   - Model Load Optimizer plugin (intelligent model routing)
#   - OpenClaw gateway (chat + Discord + dashboard)
#   - Firewalld rules for all services
#   - Systemd services for everything (auto-start on boot)
#
# Usage (combustion / first-boot):
#   Drop this script into the combustion config and boot.
#   It handles everything including the reboot.
#
# Usage (manual):
#   sudo bash cnc-server-bootstrap.sh
#   # (reboots automatically, finishes on second boot)
#
# To add an Anthropic API key later:
#   echo 'ANTHROPIC_API_KEY=sk-ant-...' > /etc/claude/api-key
# =============================================================================

# ── Configuration ─────────────────────────────────────────────────────────────
# No prompts — what you see is what runs.

TS_HOSTNAME="cnc-server"

# LAN Ollama servers (Tailscale MagicDNS hostnames)
# These machines run Ollama — no Anthropic API key required.
LAN_OLLAMA_PRIMARY="http://satibook:11434"
LAN_OLLAMA_FALLBACK="http://kokonoe:11434"

# Compile jobs — empty = auto-detect (cores - 2, minimum 1)
MAX_JOBS=""

# ── Secrets (not committed to git) ───────────────────────────────────────────
# Source .secrets from the same directory as this script, or from /root/.secrets
# Contains: TS_AUTH_KEY, ANTHROPIC_API_KEY
# See .secrets.example for the template.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for secrets_path in "${SCRIPT_DIR}/.secrets" /root/.secrets /etc/cnc-secrets; do
    if [ -f "$secrets_path" ]; then
        source "$secrets_path"
        break
    fi
done

# Validate Tailscale key
TS_AUTH_KEY="${TS_AUTH_KEY:-}"
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
if [ -z "$TS_AUTH_KEY" ]; then
    echo "FATAL: No TS_AUTH_KEY found. Create .secrets file from .secrets.example"
    echo "  cp .secrets.example .secrets && \$EDITOR .secrets"
    exit 1
fi

# ── Colors & helpers ──────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[  OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()  { echo -e "${RED}[FAIL]${NC} $1"; }
phase() { echo -e "\n${BOLD}${YELLOW}=== $1 ===${NC}\n"; }

# ── Root check ────────────────────────────────────────────────────────────────

if [ "$(id -u)" -ne 0 ]; then
    fail "Must be root. Try: sudo bash $0"
    exit 1
fi

# ── OS detection ──────────────────────────────────────────────────────────────

if [ ! -f /etc/os-release ]; then
    fail "Cannot detect OS. Is this openSUSE MicroOS?"
    exit 1
fi

source /etc/os-release

case "${ID:-}" in
    opensuse-microos|opensuse-tumbleweed-microos|opensuse-leap-micro|sle-micro)
        ok "Detected: ${PRETTY_NAME:-$ID}"
        ;;
    *)
        warn "Expected MicroOS/Leap Micro, got: ${PRETTY_NAME:-unknown} — continuing anyway"
        ;;
esac

# ── State file (resume after reboot) ─────────────────────────────────────────

STATE_FILE="/root/.cnc-bootstrap-state"
CURRENT_PHASE=1

if [ -f "$STATE_FILE" ]; then
    source "$STATE_FILE"
    info "Resuming from Phase ${CURRENT_PHASE}"
fi

save_state() {
    cat > "$STATE_FILE" << EOF
CURRENT_PHASE=$1
TS_HOSTNAME="${TS_HOSTNAME}"
MAX_JOBS="${MAX_JOBS:-}"
LAN_OLLAMA_PRIMARY="${LAN_OLLAMA_PRIMARY}"
LAN_OLLAMA_FALLBACK="${LAN_OLLAMA_FALLBACK}"
GPU_NAME="${GPU_NAME:-}"
GPU_VRAM_GB="${GPU_VRAM_GB:-0}"
GPU_VENDOR="${GPU_VENDOR:-}"
OLLAMA_INSTALLED="${OLLAMA_INSTALLED:-0}"
OLLAMA_MODEL="${OLLAMA_MODEL:-}"
SELECTED_MODEL="${SELECTED_MODEL:-}"
SIDECAR_MODEL="${SIDECAR_MODEL:-}"
EOF
}

# ── Auto-detect compile jobs ─────────────────────────────────────────────────

if [ -z "$MAX_JOBS" ]; then
    TOTAL_CORES=$(nproc)
    MAX_JOBS=$(( TOTAL_CORES > 2 ? TOTAL_CORES - 2 : 1 ))
    info "Auto-detected: ${TOTAL_CORES} cores → ${MAX_JOBS} compile jobs"
fi

echo -e "${BOLD}${CYAN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║     C&C Server Bootstrap — openSUSE MicroOS          ║"
echo "║     Unattended · Atomic · Zero Prompts                ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
info "Hostname:     ${TS_HOSTNAME}"
info "Compile jobs: ${MAX_JOBS}"
info "LAN Ollama:   ${LAN_OLLAMA_PRIMARY} (fallback: ${LAN_OLLAMA_FALLBACK})"
[ -n "$ANTHROPIC_API_KEY" ] && info "API key:      provided" || info "API key:      skipped (Ollama only)"
echo ""


# ==============================================================================
# Phase 1: SSH + Transactional Update — Core Packages
# ==============================================================================
if [ "$CURRENT_PHASE" -le 1 ]; then
    phase "Phase 1: SSH + Transactional Update"

    # Restore sshd_config from vendor defaults if missing (MicroOS stores them in /usr/etc)
    if [ ! -f /etc/ssh/sshd_config ] && [ -f /usr/etc/ssh/sshd_config ]; then
        mkdir -p /etc/ssh
        cp /usr/etc/ssh/sshd_config /etc/ssh/sshd_config
        ok "Restored sshd_config from vendor defaults"
    fi

    # Ensure SSH is enabled before reboot so we don't get locked out
    info "Ensuring SSH..."
    if systemctl is-enabled sshd &>/dev/null; then
        ok "sshd already enabled"
    elif systemctl is-enabled ssh &>/dev/null; then
        ok "ssh already enabled"
    else
        systemctl enable --now sshd.service 2>/dev/null || \
            systemctl enable --now ssh.service 2>/dev/null || true
    fi
    systemctl restart sshd.service 2>/dev/null || systemctl restart ssh.service 2>/dev/null || true

    # Open SSH in firewall if firewalld is running
    if command -v firewall-cmd &>/dev/null && systemctl is-active firewalld &>/dev/null; then
        firewall-cmd --permanent --add-service=ssh 2>/dev/null || true
        firewall-cmd --reload 2>/dev/null || true
    fi

    info "Installing core packages via transactional-update..."
    info "This creates a new btrfs snapshot — takes a minute."

    # CRITICAL: --continue chains onto the SAME snapshot.
    # Without it, each call forks a new snapshot from the original base,
    # orphaning the previous snapshot's changes.

    # Core packages
    transactional-update --non-interactive pkg install \
        openssh-server \
        git curl wget jq htop tmux \
        gcc gcc-c++ make ccache clang lld \
        podman \
        nodejs npm \
        tailscale \
        firewalld \
        unzip tar

    # Optional packages — nice to have, don't abort if missing
    transactional-update --non-interactive --continue pkg install \
        ripgrep icecream distrobox \
        2>/dev/null || warn "Some optional packages unavailable — continuing"

    transactional-update --non-interactive --continue pkg install \
        icecream-clang-wrappers podman-docker \
        2>/dev/null || warn "icecream-clang-wrappers or podman-docker not found — skipping"

    # Enable sshd in the new snapshot
    transactional-update --non-interactive --continue run systemctl enable sshd.service 2>/dev/null || true

    ok "Packages staged in btrfs snapshot"

    # Install auto-resume service so bootstrap continues after reboot
    SCRIPT_PATH="/root/cnc-server-bootstrap.sh"
    cp "$(readlink -f "$0")" "$SCRIPT_PATH" 2>/dev/null || cp "$0" "$SCRIPT_PATH"
    chmod +x "$SCRIPT_PATH"

    cat > /etc/systemd/system/cnc-bootstrap-resume.service << SVCEOF
[Unit]
Description=Resume C&C bootstrap after reboot
After=network-online.target
Wants=network-online.target
ConditionPathExists=${STATE_FILE}

[Service]
Type=oneshot
ExecStart=/bin/bash ${SCRIPT_PATH}
StandardOutput=journal
StandardError=journal
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
SVCEOF

    systemctl daemon-reload
    systemctl enable cnc-bootstrap-resume.service

    save_state 2
    warn "Rebooting to activate new snapshot..."
    sleep 2
    reboot
    # Script exits here — resumes from Phase 2 after reboot via systemd
fi


# ==============================================================================
# Phase 2: Verify Packages + Tailscale
# ==============================================================================
if [ "$CURRENT_PHASE" -le 2 ]; then
    phase "Phase 2: Verify Packages + Tailscale"

    # Verify SSH survived the reboot
    if systemctl is-active sshd &>/dev/null || systemctl is-active ssh &>/dev/null; then
        ok "SSH: active"
    else
        systemctl enable --now sshd.service 2>/dev/null || systemctl enable --now ssh.service 2>/dev/null || true
    fi

    # Verify the transactional update took effect
    for cmd in git clang iceccd node tailscale podman; do
        if command -v "$cmd" &>/dev/null; then
            ok "$cmd: $(command -v $cmd)"
        else
            fail "$cmd not found! transactional-update may not have applied."
            exit 1
        fi
    done

    ok "Node.js $(node --version 2>/dev/null || echo unknown)"

    # Tailscale — authenticate with baked-in pre-auth key (zero interaction)
    systemctl enable --now tailscaled
    info "Authenticating Tailscale with pre-auth key..."
    tailscale up --hostname "${TS_HOSTNAME}" --authkey "${TS_AUTH_KEY}" && \
        ok "Tailscale authenticated" || \
        warn "Tailscale auth failed — key may be expired. Generate a new one at https://login.tailscale.com/admin/settings/keys"

    TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")
    [ "$TS_IP" != "not connected" ] && ok "Tailscale IP: ${TS_IP}" || warn "Tailscale not yet connected"

    save_state 3
fi


# ==============================================================================
# Phase 3: Icecream Scheduler + Worker
# ==============================================================================
if [ "$CURRENT_PHASE" -le 3 ]; then
    phase "Phase 3: Icecream Distributed Compilation"

    mkdir -p /opt/icecc-envs

    # Configure worker
    if [ -f /etc/sysconfig/icecream ]; then
        sed -i 's/^ICECREAM_SCHEDULER_HOST=.*/ICECREAM_SCHEDULER_HOST="localhost"/' /etc/sysconfig/icecream
        sed -i "s/^ICECREAM_MAX_JOBS=.*/ICECREAM_MAX_JOBS=\"${MAX_JOBS}\"/" /etc/sysconfig/icecream
    fi

    systemctl enable --now icecc-scheduler.service 2>/dev/null || {
        warn "icecc-scheduler.service not found — starting manually"
        nohup icecc-scheduler -d -l /var/log/icecc-scheduler.log &>/dev/null &
    }

    systemctl enable --now iceccd.service 2>/dev/null || {
        for svc in icecc-daemon icecc; do
            if systemctl list-unit-files | grep -q "^${svc}.service"; then
                systemctl enable --now "${svc}.service"
                break
            fi
        done
    }

    ok "Icecream scheduler + worker (${MAX_JOBS} jobs)"

    # Create clang toolchain tarball
    info "Creating clang toolchain tarball..."
    cd /tmp
    icecc-create-env --clang /usr/bin/clang /usr/bin/clang++ 2>/dev/null || true
    TARBALL=$(ls -t /tmp/*.tar.gz 2>/dev/null | head -1)
    if [ -n "$TARBALL" ]; then
        mv "$TARBALL" /opt/icecc-envs/x86_64-clang.tar.gz
        ok "Toolchain: /opt/icecc-envs/x86_64-clang.tar.gz"
    fi

    save_state 4
fi


# ==============================================================================
# Phase 4: GPU Detection + Ollama
# ==============================================================================
if [ "$CURRENT_PHASE" -le 4 ]; then
    phase "Phase 4: GPU Detection + Ollama"

    GPU_NAME=""
    GPU_VRAM_GB=0
    GPU_VENDOR=""
    OLLAMA_INSTALLED=0
    OLLAMA_MODEL=""
    SELECTED_MODEL="qwen2.5-coder:7b"
    SIDECAR_MODEL=""
    INSTALL_LOCAL_OLLAMA=0

    # Detect NVIDIA
    if lspci 2>/dev/null | grep -qi nvidia; then
        if command -v nvidia-smi &>/dev/null; then
            GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d '\n')
            GPU_VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d '\n')
            GPU_VRAM_GB=$(( GPU_VRAM_MB / 1024 ))
            GPU_VENDOR="NVIDIA"
            ok "GPU: ${GPU_NAME} — ${GPU_VRAM_GB} GB VRAM"
            INSTALL_LOCAL_OLLAMA=1
        else
            warn "NVIDIA detected but no driver — using LAN Ollama"
            warn "  Install drivers later: transactional-update pkg install nvidia-driver-G06-signed && reboot"
            GPU_NAME=$(lspci | grep -i nvidia | head -1 | sed 's/.*: //')
            GPU_VENDOR="NVIDIA"
        fi
    fi

    # Detect AMD (skip integrated GPUs)
    if [ -z "$GPU_VENDOR" ] && lspci 2>/dev/null | grep -i "vga\|3d" | grep -qi "amd\|radeon"; then
        AMD_CARD=$(lspci | grep -i "vga\|3d" | grep -i "amd\|radeon" | grep -iv "cezanne\|renoir\|barcelo\|phoenix\|rembrandt" | head -1 || true)
        if [ -n "$AMD_CARD" ]; then
            GPU_NAME=$(echo "$AMD_CARD" | sed 's/.*: //')
            GPU_VENDOR="AMD"
            GPU_VRAM_GB=4
            ok "GPU: ${GPU_NAME} — ~${GPU_VRAM_GB} GB (estimated)"
            INSTALL_LOCAL_OLLAMA=1
        fi
    fi

    if [ -z "$GPU_VENDOR" ]; then
        info "No discrete GPU — inference via LAN Ollama (satibook / kokonoe)"
    fi

    # Install Ollama locally only if we have a GPU
    if [ "$INSTALL_LOCAL_OLLAMA" = "1" ]; then
        if ! command -v ollama &>/dev/null; then
            info "Installing Ollama..."
            curl -fsSL https://ollama.com/install.sh | sh
        fi

        systemctl enable --now ollama 2>/dev/null || {
            warn "Ollama service not found — starting manually"
            ollama serve &>/dev/null &
            sleep 3
        }

        # Model selection based on VRAM
        if [ "$GPU_VRAM_GB" -ge 12 ]; then
            SELECTED_MODEL="deepseek-coder-v2:16b"
            SIDECAR_MODEL="qwen2.5-coder:7b"
            info "GPU tier: Large — primary + sidecar"
        elif [ "$GPU_VRAM_GB" -ge 8 ]; then
            SELECTED_MODEL="qwen2.5-coder:7b"
            SIDECAR_MODEL="deepseek-coder-v2:lite"
            info "GPU tier: Medium — primary + lite sidecar"
        elif [ "$GPU_VRAM_GB" -ge 4 ]; then
            SELECTED_MODEL="qwen2.5-coder:7b"
            info "GPU tier: Small — primary only"
        else
            SELECTED_MODEL="qwen2.5-coder:7b"
            info "CPU-only — lightweight model"
        fi

        info "Pulling ${SELECTED_MODEL}..."
        if ollama pull "$SELECTED_MODEL" 2>/dev/null; then
            OLLAMA_INSTALLED=1
            OLLAMA_MODEL="$SELECTED_MODEL"
            ok "Primary: ${SELECTED_MODEL}"
        else
            warn "Failed to pull ${SELECTED_MODEL} — will use LAN Ollama"
        fi

        [ -n "$SIDECAR_MODEL" ] && {
            info "Pulling sidecar: ${SIDECAR_MODEL}..."
            ollama pull "$SIDECAR_MODEL" 2>/dev/null && ok "Sidecar: ${SIDECAR_MODEL}" || true
        }

        # Expose Ollama to LAN
        mkdir -p /etc/systemd/system/ollama.service.d
        cat > /etc/systemd/system/ollama.service.d/override.conf << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
EOF
        systemctl daemon-reload
        systemctl restart ollama
        ok "Ollama exposed on 0.0.0.0:11434 (LAN accessible)"
    fi

    save_state 5
fi


# ==============================================================================
# Phase 5: Claude Code + AgentAPI
# ==============================================================================
if [ "$CURRENT_PHASE" -le 5 ]; then
    phase "Phase 5: Claude Code + AgentAPI"

    # On MicroOS, /usr/local is writable. npm global installs go there.
    npm install -g @anthropic-ai/claude-code 2>/dev/null || {
        warn "npm global install failed on read-only root — installing to /usr/local"
        mkdir -p /usr/local/lib/node_modules
        npm install --prefix /usr/local -g @anthropic-ai/claude-code
    }
    ok "Claude Code: $(/usr/local/bin/claude --version 2>/dev/null || echo installed)"

    # AgentAPI binary
    ARCH_HW=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
    curl -fsSL \
        "https://github.com/coder/agentapi/releases/latest/download/agentapi-linux-${ARCH_HW}" \
        -o /usr/local/bin/agentapi
    chmod +x /usr/local/bin/agentapi
    ok "AgentAPI installed"

    # Service user
    if ! id claude-agent &>/dev/null; then
        useradd -r -m -s /bin/bash claude-agent
        ok "User 'claude-agent' created"
    fi

    # API key file — from env var or empty placeholder
    mkdir -p /etc/claude
    chmod 700 /etc/claude
    if [ -n "${ANTHROPIC_API_KEY}" ]; then
        echo "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}" > /etc/claude/api-key
        ok "API key saved"
    else
        touch /etc/claude/api-key
        info "No API key — Ollama handles inference. Add later if needed:"
        info "  echo 'ANTHROPIC_API_KEY=sk-ant-...' > /etc/claude/api-key"
    fi
    chmod 600 /etc/claude/api-key
    chown claude-agent:claude-agent /etc/claude/api-key

    save_state 6
fi


# ==============================================================================
# Phase 6: Deno + Orchestrator
# ==============================================================================
if [ "$CURRENT_PHASE" -le 6 ]; then
    phase "Phase 6: Orchestrator (claude-code-by-agents)"

    # Install Deno system-wide to /usr/local/bin (not in home dirs where
    # MicroOS permissions block systemd from executing it)
    DENO_BIN="/usr/local/bin/deno"
    if [ ! -x "$DENO_BIN" ]; then
        info "Installing Deno..."
        export DENO_INSTALL="/tmp/deno-install"
        curl -fsSL https://deno.land/install.sh | sh
        cp /tmp/deno-install/bin/deno /usr/local/bin/deno
        chmod 755 /usr/local/bin/deno
        rm -rf /tmp/deno-install
        unset DENO_INSTALL
    fi
    ok "Deno: $($DENO_BIN --version 2>/dev/null | head -1)"

    ORCHESTRATOR_DIR="/opt/claude-code-by-agents"
    if [ ! -d "$ORCHESTRATOR_DIR" ]; then
        info "Cloning claude-code-by-agents..."
        git clone https://github.com/baryhuang/claude-code-by-agents.git "$ORCHESTRATOR_DIR"
    fi
    chown -R claude-agent:claude-agent "$ORCHESTRATOR_DIR"

    info "Caching orchestrator dependencies..."
    sudo -u claude-agent bash -c "export HOME=/home/claude-agent && cd ${ORCHESTRATOR_DIR}/backend && ${DENO_BIN} cache cli/deno.ts 2>&1" || {
        warn "Dependency caching had errors — service may download on first start"
    }

    sudo -u claude-agent mkdir -p /home/claude-agent/.deno/bin
    ln -sf /usr/local/bin/deno /home/claude-agent/.deno/bin/deno 2>/dev/null || true

    save_state 7
fi


# ==============================================================================
# Phase 7: Model Load Optimizer + OpenClaw Config
# ==============================================================================
if [ "$CURRENT_PHASE" -le 7 ]; then
    phase "Phase 7: Model Load Optimizer + OpenClaw Config"

    OPENCLAW_DIR="/home/claude-agent/.openclaw"
    PLUGIN_DIR="$OPENCLAW_DIR/plugins/model-load-optimizer"

    sudo -u claude-agent mkdir -p "$OPENCLAW_DIR/plugins"

    if [ ! -d "$PLUGIN_DIR" ]; then
        info "Cloning model-load-optimizer..."
        sudo -u claude-agent git clone https://github.com/suhteevah/model-load-optimizer.git "$PLUGIN_DIR" 2>/dev/null
    fi

    if [ -f "$PLUGIN_DIR/package.json" ]; then
        info "Building plugin..."
        cd "$PLUGIN_DIR"
        sudo -u claude-agent npm install --silent 2>/dev/null
        sudo -u claude-agent npx tsc 2>/dev/null
        ok "Model Load Optimizer built"
    else
        warn "Plugin clone failed — install manually later"
    fi

    # Determine Ollama endpoint
    OPTIMIZER_OLLAMA_HOST="${LAN_OLLAMA_PRIMARY}"
    if [ "${OLLAMA_INSTALLED:-0}" = "1" ]; then
        OPTIMIZER_OLLAMA_HOST="http://localhost:11434"
    fi

    PRIMARY_MODEL="${OLLAMA_MODEL:-qwen2.5-coder:7b}"
    PRIMARY_REF="ollama/${PRIMARY_MODEL}"

    SIDECAR_MODELS_JSON=""
    SIDECAR_FALLBACK_JSON=""
    SIDECAR_OPT_JSON='"sidecarModel": "",'
    if [ -n "${SIDECAR_MODEL:-}" ]; then
        SIDECAR_MODELS_JSON="\"ollama/${SIDECAR_MODEL}\": { \"alias\": \"sidecar\" },"
        SIDECAR_FALLBACK_JSON="\"ollama/${SIDECAR_MODEL}\","
        SIDECAR_OPT_JSON="\"sidecarModel\": \"${SIDECAR_MODEL}\","
    fi

    # Ollama-only config — no Anthropic API dependency
    sudo -u claude-agent tee "$OPENCLAW_DIR/openclaw.json" > /dev/null << OCEOF
{
  "env": { "OLLAMA_API_KEY": "ollama-local" },
  "auth": {
    "profiles": {
      "ollama:default": { "provider": "ollama", "mode": "api_key" }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "${PRIMARY_REF}",
        "fallbacks": [${SIDECAR_FALLBACK_JSON} "ollama/qwen2.5-coder:7b"]
      },
      "models": {
        "${PRIMARY_REF}": { "alias": "primary" },
        ${SIDECAR_MODELS_JSON}
        "ollama/qwen2.5-coder:7b": { "alias": "coder" }
      },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 }
    }
  },
  "tools": {
    "agentToAgent": { "enabled": true, "allow": ["exec"] },
    "exec": { "security": "full", "ask": "off" }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "0.0.0.0",
    "auth": { "mode": "token" },
    "tailscale": { "mode": "off" }
  },
  "plugins": {
    "load": {
      "paths": ["${PLUGIN_DIR}"]
    },
    "entries": {
      "model-load-optimizer": {
        "enabled": true,
        "config": {
          "ollamaHost": "${OPTIMIZER_OLLAMA_HOST}",
          "ollamaFallbackHost": "${LAN_OLLAMA_FALLBACK}",
          "primaryModel": "${PRIMARY_MODEL}",
          ${SIDECAR_OPT_JSON}
          "fallbackModel": "qwen2.5-coder:7b",
          "keepAliveMinutes": 30,
          "gpuMemoryThreshold": 0.85,
          "healthCheckIntervalSec": 30,
          "preloadOnStart": true,
          "autoRoute": true,
          "dashboardEnabled": true
        }
      }
    }
  }
}
OCEOF

    ok "OpenClaw config written (Ollama-only, satibook primary, kokonoe fallback)"
    save_state 8
fi


# ==============================================================================
# Phase 8: Systemd Services
# ==============================================================================
if [ "$CURRENT_PHASE" -le 8 ]; then
    phase "Phase 8: Systemd Services"

    OLLAMA_AFTER=""
    if systemctl list-unit-files ollama.service &>/dev/null 2>&1; then
        OLLAMA_AFTER=" ollama.service"
    fi

    # EnvironmentFile=-  (the dash means "don't fail if file is empty/missing")
    cat > /etc/systemd/system/claude-agentapi.service << EOF
[Unit]
Description=Claude Code AgentAPI Server
After=network-online.target tailscaled.service${OLLAMA_AFTER}
Wants=network-online.target

[Service]
Type=simple
User=claude-agent
WorkingDirectory=/home/claude-agent
EnvironmentFile=-/etc/claude/api-key
ExecStart=/usr/local/bin/agentapi server --type claude -- /usr/local/bin/claude \
  --dangerously-skip-permissions \
  --max-budget-usd 10.00
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=claude-agentapi

[Install]
WantedBy=multi-user.target
EOF

    # Orchestrator — runs Deno directly (not 'deno task dev' which uses --watch)
    cat > /etc/systemd/system/claude-orchestrator.service << 'EOF'
[Unit]
Description=Claude Code Orchestrator (claude-code-by-agents)
After=network-online.target claude-agentapi.service tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=claude-agent
WorkingDirectory=/opt/claude-code-by-agents/backend
EnvironmentFile=-/etc/claude/api-key
Environment="HOME=/home/claude-agent"
Environment="DENO_DIR=/home/claude-agent/.cache/deno"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/deno run \
  --allow-net --allow-run --allow-read --allow-write --allow-env \
  cli/deno.ts \
  --host 0.0.0.0 \
  --port 8080 \
  --claude-path /usr/local/bin/claude
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=claude-orchestrator

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable --now claude-agentapi.service
    systemctl enable --now claude-orchestrator.service

    ok "Services installed and started"
    save_state 9
fi


# ==============================================================================
# Phase 9: Firewalld
# ==============================================================================
if [ "$CURRENT_PHASE" -le 9 ]; then
    phase "Phase 9: Firewall"

    systemctl enable --now firewalld

    # SSH
    firewall-cmd --permanent --add-service=ssh

    # Trust the Tailscale interface fully
    firewall-cmd --permanent --zone=trusted --add-interface=tailscale0 2>/dev/null || true

    # Icecream
    firewall-cmd --permanent --add-port=8765/tcp   # scheduler
    firewall-cmd --permanent --add-port=8766/tcp   # telnet monitor
    firewall-cmd --permanent --add-port=10245/tcp  # worker

    # Ollama (only if running locally)
    if systemctl list-unit-files ollama.service &>/dev/null 2>&1; then
        firewall-cmd --permanent --add-port=11434/tcp
    fi

    # AgentAPI + OpenClaw + Orchestrator
    firewall-cmd --permanent --add-port=3284/tcp
    firewall-cmd --permanent --add-port=18789/tcp
    firewall-cmd --permanent --add-port=8080/tcp

    firewall-cmd --reload
    ok "Firewalld configured"
    save_state 10
fi


# ==============================================================================
# Phase 10: Verification + Cleanup
# ==============================================================================
phase "Phase 10: Verification"

# Remove auto-resume service — bootstrap complete
systemctl disable cnc-bootstrap-resume.service 2>/dev/null || true
rm -f /etc/systemd/system/cnc-bootstrap-resume.service
systemctl daemon-reload

echo ""
echo -e "${BOLD}Service Status:${NC}"

check_svc() {
    local name=$1 st
    st=$(systemctl is-active "$name" 2>/dev/null || echo "not found")
    if [ "$st" = "active" ]; then
        echo -e "  ${GREEN}●${NC} ${name}: active"
    else
        echo -e "  ${RED}●${NC} ${name}: ${st}"
    fi
}

check_svc "tailscaled"
check_svc "icecc-scheduler"
check_svc "iceccd"
systemctl list-unit-files ollama.service &>/dev/null 2>&1 && check_svc "ollama" || \
    echo -e "  ${YELLOW}○${NC} ollama: LAN (${LAN_OLLAMA_PRIMARY})"
check_svc "claude-agentapi"
check_svc "claude-orchestrator"
check_svc "firewalld"

echo ""
echo -e "${BOLD}Network:${NC}"
TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")
echo "  Tailscale IP: ${TS_IP}"
echo "  Hostname:     ${TS_HOSTNAME}"

echo ""
echo -e "${BOLD}Ollama:${NC}"
if [ "${OLLAMA_INSTALLED:-0}" = "1" ]; then
    echo "  Local:    localhost:11434 (${OLLAMA_MODEL:-qwen2.5-coder:7b})"
fi
echo "  Primary:  ${LAN_OLLAMA_PRIMARY} (satibook)"
echo "  Fallback: ${LAN_OLLAMA_FALLBACK} (kokonoe)"

echo ""
echo -e "${BOLD}GPU:${NC}"
if [ -n "${GPU_VENDOR:-}" ]; then
    echo "  ${GPU_VENDOR} ${GPU_NAME} — ${GPU_VRAM_GB} GB VRAM"
else
    echo "  No discrete GPU — inference via LAN Ollama"
fi

echo ""
echo -e "${BOLD}API Key:${NC}"
if [ -n "${ANTHROPIC_API_KEY}" ]; then
    echo "  Configured"
else
    echo "  Not set (Ollama only) — add later if needed:"
    echo "    echo 'ANTHROPIC_API_KEY=sk-ant-...' > /etc/claude/api-key"
fi

# Clean state file — bootstrap complete
rm -f "$STATE_FILE"


# ==============================================================================
# Summary
# ==============================================================================
echo ""
echo -e "${BOLD}${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║     C&C Server is ONLINE                              ║"
echo "║     openSUSE MicroOS · Atomic · Unattended            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BOLD}Endpoints:${NC}"
echo "  Orchestrator UI:  http://${TS_HOSTNAME}:8080"
echo "  OpenClaw:         http://${TS_HOSTNAME}:18789"
echo "  AgentAPI:         http://${TS_HOSTNAME}:3284"
if [ "${OLLAMA_INSTALLED:-0}" = "1" ]; then
    echo "  Ollama (local):   http://${TS_HOSTNAME}:11434"
fi
echo "  Ollama (LAN):     ${LAN_OLLAMA_PRIMARY}"
echo "  Icecream Monitor: telnet ${TS_HOSTNAME} 8766"
echo ""

echo -e "${BOLD}Deploy agents on fleet machines:${NC}"
echo "  Windows: irm https://raw.githubusercontent.com/suhteevah/claw-setup/main/swoop-windows-bootstrap.ps1 | iex"
echo "  Mac:     bash <(curl -sL https://raw.githubusercontent.com/suhteevah/claw-setup/main/fcp-mac-bootstrap.sh)"
echo "  Pi:      bash <(curl -sL https://raw.githubusercontent.com/suhteevah/claw-setup/main/fcp-pi-bootstrap.sh)"
echo "  Linux:   bash <(curl -sL https://raw.githubusercontent.com/suhteevah/claw-setup/main/dr-paper-bootstrap.sh)"
echo ""

echo -e "${BOLD}MicroOS management:${NC}"
echo "  transactional-update               # Apply updates (needs reboot)"
echo "  transactional-update rollback       # Rollback last update"
echo "  snapper list                        # List snapshots"
echo "  snapper rollback <N>               # Rollback to snapshot N"
echo ""

echo -e "${BOLD}Service management:${NC}"
echo "  journalctl -u claude-agentapi -f     # Agent logs"
echo "  journalctl -u claude-orchestrator -f  # Orchestrator logs"
if [ "${OLLAMA_INSTALLED:-0}" = "1" ]; then
    echo "  journalctl -u ollama -f               # Ollama logs"
    echo "  ollama list                            # Show pulled models"
fi
echo "  systemctl restart claude-agentapi     # Restart agent"
echo "  tailscale status                       # Mesh status"
echo ""
