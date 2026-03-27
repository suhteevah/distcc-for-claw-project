#!/bin/bash
set -euo pipefail

# =============================================================================
# FCP (First Choice Plastics) -- Apple TV 4K (1st Gen) Bootstrap
# For jailbroken Apple TV running tvOS via palera1n
#
# Prerequisites:
#   1. Jailbreak with palera1n (https://palera.in)
#   2. Install Sileo package manager from jailbreak
#   3. SSH into the Apple TV: ssh root@<apple-tv-ip> (default pw: alpine)
#   4. Copy this script and run it
#
# Usage: bash appletv-bootstrap.sh [hostname]
#
# Role: Fleet node + monitoring (visible on life dashboard)
# =============================================================================

HOSTNAME="${1:-fcp-appletv}"
HEALTH_PORT=3284

echo "============================================"
echo "  First Choice Plastics -- Apple TV Bootstrap"
echo "  Model: Apple TV 4K (1st Gen, A10X)"
echo "  Setting up: ${HOSTNAME}"
echo "============================================"

# === Sanity Checks ===
if [ "$(uname -s)" != "Darwin" ]; then
  echo "ERROR: This script must run on tvOS/Darwin (the Apple TV itself)."
  exit 1
fi

ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ] && [ "$ARCH" != "arm64e" ]; then
  echo "ERROR: Expected arm64, got ${ARCH}."
  exit 1
fi

echo ""
echo "System: $(uname -s) $(uname -r) (${ARCH})"
echo "RAM: $(sysctl -n hw.memsize | awk '{printf "%.0f MB", $1/1048576}')"

# === Phase 1: Change Root Password ===
echo ""
echo "=== Phase 1: Security ==="
echo ">>> IMPORTANT: Change the default root password (alpine)."
echo ">>> Run: passwd"
read -p "Press Enter after changing the root password..."

# === Phase 2: Package Manager Setup ===
echo "=== Phase 2: Package Manager ==="

# palera1n provides procursus bootstrap with apt
if command -v apt-get &>/dev/null; then
  echo "  apt-get found (procursus)"
  apt-get update
  apt-get install -y bash curl git nano jq
elif command -v dpkg &>/dev/null; then
  echo "  dpkg found but no apt — install Sileo or add procursus repos"
  echo "  See: https://apt.procurs.us"
  read -p "Press Enter after setting up package manager..."
  apt-get update
  apt-get install -y bash curl git nano jq
else
  echo "  ERROR: No package manager found. Ensure jailbreak installed Sileo/procursus."
  exit 1
fi

# === Phase 3: Node.js ===
echo "=== Phase 3: Node.js ==="
if ! command -v node &>/dev/null; then
  echo "  Installing Node.js from procursus..."
  apt-get install -y nodejs || {
    echo "  procursus Node.js not available. Trying manual install..."
    # Fallback: download prebuilt arm64 Darwin binary
    NODE_VER="v20.18.0"
    curl -fsSL "https://nodejs.org/dist/${NODE_VER}/node-${NODE_VER}-darwin-arm64.tar.gz" \
      -o /tmp/node.tar.gz
    tar -xzf /tmp/node.tar.gz -C /usr/local --strip-components=1
    rm /tmp/node.tar.gz
  }
fi
echo "  Node.js: $(node --version 2>/dev/null || echo 'not installed')"

# === Phase 4: Tailscale ===
echo "=== Phase 4: Tailscale ==="
if ! command -v tailscale &>/dev/null; then
  echo "  Installing Tailscale..."
  # Try procursus package first
  if apt-get install -y tailscale 2>/dev/null; then
    echo "  Installed via procursus"
  else
    echo "  Downloading Tailscale for Darwin arm64..."
    # Download the macOS tailscale CLI (works on tvOS/Darwin)
    TS_VER=$(curl -fsSL "https://pkgs.tailscale.com/stable/?mode=json" | jq -r '.Tarballs["darwin_arm64"] // empty' | head -1)
    if [ -n "$TS_VER" ]; then
      curl -fsSL "https://pkgs.tailscale.com/stable/${TS_VER}" -o /tmp/tailscale.tar.gz
      mkdir -p /tmp/ts-extract
      tar -xzf /tmp/tailscale.tar.gz -C /tmp/ts-extract
      find /tmp/ts-extract -name 'tailscale' -type f -exec cp {} /usr/local/bin/tailscale \;
      find /tmp/ts-extract -name 'tailscaled' -type f -exec cp {} /usr/local/bin/tailscaled \;
      chmod +x /usr/local/bin/tailscale /usr/local/bin/tailscaled
      rm -rf /tmp/tailscale.tar.gz /tmp/ts-extract
      echo "  Tailscale binaries installed"
    else
      echo "  WARNING: Could not determine Tailscale download URL."
      echo "  Manually place tailscale + tailscaled in /usr/local/bin/"
      read -p "Press Enter after installing Tailscale..."
    fi
  fi
fi

# Create tailscaled launchd plist
echo "  Creating tailscaled launchd service..."
mkdir -p /Library/LaunchDaemons
cat > /Library/LaunchDaemons/com.tailscale.tailscaled.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.tailscale.tailscaled</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/tailscaled</string>
    <string>--state=/var/lib/tailscale/tailscaled.state</string>
    <string>--socket=/var/run/tailscale/tailscaled.sock</string>
    <string>--tun=utun</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/var/log/tailscaled.log</string>
  <key>StandardErrorPath</key>
  <string>/var/log/tailscaled.err</string>
</dict>
</plist>
PLIST

mkdir -p /var/lib/tailscale /var/run/tailscale
launchctl load /Library/LaunchDaemons/com.tailscale.tailscaled.plist 2>/dev/null || true
sleep 2

echo ">>> Run: tailscale up --hostname ${HOSTNAME}"
read -p "Press Enter after Tailscale is authenticated..."

# === Phase 5: Fleet Health Agent ===
echo "=== Phase 5: Fleet Health Agent ==="

# Lightweight HTTP health endpoint (Node.js based, no dependencies)
# This is what the dashboard polls to show the Apple TV as "up"
AGENT_DIR="/var/lib/fleet-agent"
mkdir -p "$AGENT_DIR"

cat > "$AGENT_DIR/agent.js" << 'AGENT'
const http = require("http");
const os = require("os");
const { execSync } = require("child_process");

const PORT = parseInt(process.env.HEALTH_PORT || "3284");

function getMetrics() {
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const loadavg = os.loadavg();
  const uptime = os.uptime();
  const days = Math.floor(uptime / 86400);
  const hours = Math.floor((uptime % 86400) / 3600);

  let diskInfo = {};
  try {
    const df = execSync("df -h /", { encoding: "utf-8" }).trim().split("\n");
    const parts = df[1]?.split(/\s+/) || [];
    diskInfo = { size: parts[1], used: parts[2], avail: parts[3], usePercent: parts[4] };
  } catch {}

  let thermal = null;
  try {
    // tvOS thermal state (0=nominal, 1=fair, 2=serious, 3=critical)
    const state = parseInt(execSync(
      "sysctl -n machdep.xcpm.cpu_thermal_level 2>/dev/null || echo -1",
      { encoding: "utf-8" }
    ).trim());
    const labels = ["nominal", "fair", "serious", "critical"];
    thermal = labels[state] || "unknown";
  } catch {}

  return {
    hostname: os.hostname(),
    platform: "tvos",
    device: "Apple TV 4K (1st Gen)",
    chip: "A10X Fusion",
    arch: os.arch(),
    memory: {
      totalMB: Math.round(totalMem / 1048576),
      usedMB: Math.round(usedMem / 1048576),
      usedPercent: Math.round((usedMem / totalMem) * 100),
    },
    load: { "1m": loadavg[0], "5m": loadavg[1], "15m": loadavg[2] },
    uptime: `${days}d ${hours}h`,
    disk: diskInfo,
    thermal,
    timestamp: new Date().toISOString(),
  };
}

const server = http.createServer((req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");

  if (req.url === "/status") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", agent: "fleet-health", version: "1.0.0" }));
  } else if (req.url === "/metrics") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(getMetrics()));
  } else if (req.url === "/health") {
    const m = getMetrics();
    const healthy = m.memory.usedPercent < 95 && m.thermal !== "critical";
    res.writeHead(healthy ? 200 : 503, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ healthy, ...m }));
  } else {
    res.writeHead(404);
    res.end("Not Found");
  }
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Fleet health agent running on port ${PORT}`);
});
AGENT

echo "  Health agent installed at ${AGENT_DIR}/agent.js"

# Create launchd plist for fleet agent
cat > /Library/LaunchDaemons/com.fcp.fleet-agent.plist << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.fcp.fleet-agent</string>
  <key>ProgramArguments</key>
  <array>
    <string>$(which node)</string>
    <string>${AGENT_DIR}/agent.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HEALTH_PORT</key>
    <string>${HEALTH_PORT}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/var/log/fleet-agent.log</string>
  <key>StandardErrorPath</key>
  <string>/var/log/fleet-agent.err</string>
</dict>
</plist>
PLIST

launchctl load /Library/LaunchDaemons/com.fcp.fleet-agent.plist 2>/dev/null || true
echo "  Fleet agent service started"

# === Phase 6: Reboot Persistence (palera1n tethered jailbreak note) ===
echo ""
echo "=== Phase 6: Reboot Persistence ==="
echo "  IMPORTANT: palera1n on A10X is SEMI-TETHERED."
echo "  After a reboot, you must re-jailbreak from a computer:"
echo "    palera1n -f"
echo "  Services (Tailscale, fleet agent) will auto-start after re-jailbreak."
echo ""
echo "  To avoid reboots:"
echo "  - Disable automatic tvOS updates in Settings > System > Software Updates"
echo "  - Keep the Apple TV powered on (no reason to power cycle)"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "============================================"
echo "  FCP Apple TV 4K ONLINE"
echo "  Hostname: ${HOSTNAME}"
echo "  Chip: A10X Fusion (arm64)"
echo "  RAM: $(sysctl -n hw.memsize | awk '{printf "%.0f MB", $1/1048576}')"
echo "  Role: Fleet node + monitoring"
echo "  Health: http://${HOSTNAME}:${HEALTH_PORT}/status"
echo "============================================"
echo ""
echo "Endpoints:"
echo "  /status   - Agent up/down check (for dashboard)"
echo "  /metrics  - Full system metrics (CPU, memory, disk, thermal)"
echo "  /health   - Health check with pass/fail"
echo ""
echo "Verify from any fleet machine:"
echo "  curl http://${HOSTNAME}:${HEALTH_PORT}/status"
echo "  tailscale ping ${HOSTNAME}"
echo ""
echo "Dashboard will auto-detect this node if configured in fleet agents."
