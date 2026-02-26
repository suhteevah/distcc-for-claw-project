#!/usr/bin/env pwsh
# join-claw-fleet.ps1 — Run on any Windows machine to join the claw-fleet cluster
# Sets up: icecream (distributed compilation) + exo (distributed AI inference)
# Requires: WSL2 with Ubuntu already installed, Tailscale connected
# Scheduler: cnc-server at 100.108.202.49

$ErrorActionPreference = "Continue"
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  claw-fleet Cluster Join Tool" -ForegroundColor Cyan
Write-Host "  icecream + exo distributed inference" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# --- 1. Check WSL2 ---
Write-Host "[1/9] Checking WSL2..." -ForegroundColor Yellow
$wslList = wsl --list --quiet 2>&1 | Out-String
if ($wslList -match "Ubuntu") {
    Write-Host "  OK: Ubuntu found in WSL2" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Ubuntu not found in WSL2. Install it first:" -ForegroundColor Red
    Write-Host "    wsl --install -d Ubuntu" -ForegroundColor White
    Write-Host "  Then re-run this script." -ForegroundColor White
    exit 1
}

# --- 2. Check Tailscale connectivity ---
Write-Host "`n[2/9] Testing connectivity to cnc-server (100.108.202.49)..." -ForegroundColor Yellow
$ping = Test-Connection -ComputerName 100.108.202.49 -Count 1 -TimeoutSeconds 5 -ErrorAction SilentlyContinue
if ($ping) {
    Write-Host "  OK: cnc-server reachable ($($ping.Latency)ms)" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Cannot reach cnc-server at 100.108.202.49" -ForegroundColor Red
    Write-Host "  Make sure Tailscale is connected and cnc-server is online." -ForegroundColor White
    $continue = Read-Host "  Continue anyway? (y/N)"
    if ($continue -ne "y") { exit 1 }
}

# ===== ICECREAM SETUP =====
Write-Host "`n--- ICECREAM (Distributed Compilation) ---" -ForegroundColor Magenta

# --- 3. Install icecc + gcc ---
Write-Host "`n[3/9] Installing icecc and gcc in WSL2..." -ForegroundColor Yellow
wsl -d Ubuntu -u root -- bash -c "
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq 2>&1 | tail -1
apt-get install -y -qq icecc gcc g++ 2>&1 | tail -5
echo ''
echo 'Installed:'
dpkg -l icecc gcc 2>/dev/null | grep '^ii' | awk '{printf ""  %-20s %s\n"", \$2, \$3}'
"
Write-Host "  Done" -ForegroundColor Green

# --- 4. Configure & start icecc ---
Write-Host "`n[4/9] Configuring icecc for claw-fleet..." -ForegroundColor Yellow
wsl -d Ubuntu -u root -- bash -c "
sed -i 's/^ICECC_SCHEDULER_HOST=.*/ICECC_SCHEDULER_HOST=""100.108.202.49""/' /etc/icecc/icecc.conf
sed -i 's/^ICECC_NETNAME=.*/ICECC_NETNAME=""claw-fleet""/' /etc/icecc/icecc.conf
sed -i 's/^ICECC_ALLOW_REMOTE=.*/ICECC_ALLOW_REMOTE=""yes""/' /etc/icecc/icecc.conf
pkill iceccd 2>/dev/null; sleep 1
iceccd -s 100.108.202.49 -n claw-fleet -d 2>&1
sleep 5
PID=\$(pgrep iceccd)
if [ -n ""\$PID"" ]; then
    echo ""iceccd running (PID \$PID) - joined claw-fleet""
else
    echo ""WARNING: iceccd failed to start (non-critical)""
fi
"
Write-Host "  Done" -ForegroundColor Green

# ===== EXO SETUP =====
Write-Host "`n--- EXO (Distributed AI Inference) ---" -ForegroundColor Magenta

# --- 5. Install exo prerequisites (uv, Rust, Node) ---
Write-Host "`n[5/9] Installing exo prerequisites (uv, Rust nightly, Node.js)..." -ForegroundColor Yellow
wsl -d Ubuntu -u root -- bash -c "
export PATH=""/root/.local/bin:/root/.cargo/bin:\$PATH""

# uv
if ! command -v uv &>/dev/null; then
    echo 'Installing uv...'
    curl -LsSf https://astral.sh/uv/install.sh | sh 2>&1 | tail -3
    export PATH=""/root/.local/bin:\$PATH""
fi
echo ""uv: \$(uv --version 2>&1)""

# Rust
if ! command -v rustc &>/dev/null; then
    echo 'Installing Rust...'
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y 2>&1 | tail -3
    source /root/.cargo/env
fi
rustup toolchain install nightly 2>&1 | tail -2
echo ""rustc: \$(rustc --version 2>&1)""

# Node.js
if ! command -v node &>/dev/null; then
    echo 'Installing Node.js...'
    apt-get install -y -qq nodejs npm 2>&1 | tail -3
fi
echo ""node: \$(node --version 2>&1)""
"
Write-Host "  Done" -ForegroundColor Green

# --- 6. Clone exo ---
Write-Host "`n[6/9] Cloning exo repository..." -ForegroundColor Yellow
wsl -d Ubuntu -u root -- bash -c "
if [ -d /opt/exo ]; then
    echo 'exo already cloned, pulling latest...'
    cd /opt/exo && git pull 2>&1
else
    echo 'Cloning exo...'
    git clone https://github.com/exo-explore/exo.git /opt/exo 2>&1 | tail -3
fi
echo ""exo dir: \$(ls /opt/exo/pyproject.toml 2>&1)""
"
Write-Host "  Done" -ForegroundColor Green

# --- 7. Build exo dashboard ---
Write-Host "`n[7/9] Building exo dashboard..." -ForegroundColor Yellow
wsl -d Ubuntu -u root -- bash -c "
export PATH=""/root/.local/bin:/root/.cargo/bin:\$PATH""
cd /opt/exo/dashboard && npm install 2>&1 | tail -3 && npm run build 2>&1 | tail -3
echo 'Dashboard built'
"
Write-Host "  Done" -ForegroundColor Green

# --- 8. Build exo (Rust + Python deps) ---
Write-Host "`n[8/9] Building exo (compiling Rust bindings + installing Python deps)..." -ForegroundColor Yellow
Write-Host "  This may take 5-15 minutes on first run..." -ForegroundColor White
wsl -d Ubuntu -u root -- bash -c "
export PATH=""/root/.local/bin:/root/.cargo/bin:\$PATH""
cd /opt/exo
uv run exo --help 2>&1 | head -5
if [ \$? -eq 0 ]; then
    echo 'exo build SUCCESS'
else
    echo 'exo build FAILED - you may need to retry'
fi
"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Done" -ForegroundColor Green
} else {
    Write-Host "  Build had issues - try running again" -ForegroundColor Yellow
}

# --- 9. Test exo startup ---
Write-Host "`n[9/9] Quick exo startup test (10s)..." -ForegroundColor Yellow
$exoOutput = wsl -d Ubuntu -u root -- bash -c "
export PATH=""/root/.local/bin:/root/.cargo/bin:\$PATH""
cd /opt/exo
timeout 10 uv run exo --quiet --api-port 52415 2>&1 | head -20
echo 'EXO_TEST_OK'
" 2>&1 | Out-String

if ($exoOutput -match "EXO_TEST_OK|Starting EXO|Dashboard") {
    Write-Host "  exo starts successfully" -ForegroundColor Green
} else {
    Write-Host "  exo startup test inconclusive - check manually" -ForegroundColor Yellow
}

# --- Install SSH key for remote management ---
Write-Host "`nInstalling SSH key for remote management..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pubKeyFile = Join-Path $scriptDir "satibook-key.pub"
if (Test-Path $pubKeyFile) {
    $pubKey = Get-Content $pubKeyFile -Raw
    $pubKey = $pubKey.Trim()

    # Install in Windows SSH
    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshDir)) { mkdir $sshDir -Force | Out-Null }
    $authKeys = Join-Path $sshDir "authorized_keys"
    if (-not (Test-Path $authKeys) -or -not (Select-String -Path $authKeys -Pattern "claude-code@claw-fleet" -Quiet)) {
        Add-Content -Path $authKeys -Value $pubKey
        Write-Host "  SSH key installed for Windows SSH" -ForegroundColor Green
    } else {
        Write-Host "  SSH key already present in Windows" -ForegroundColor Green
    }

    # Install in WSL2
    wsl -d Ubuntu -u root -- bash -c "mkdir -p /root/.ssh && chmod 700 /root/.ssh && if ! grep -q 'claude-code@claw-fleet' /root/.ssh/authorized_keys 2>/dev/null; then echo '$pubKey' >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys && echo 'SSH key installed in WSL2'; else echo 'SSH key already in WSL2'; fi"

    # Ensure Windows OpenSSH server is running
    $sshd = Get-Service sshd -ErrorAction SilentlyContinue
    if ($sshd) {
        if ($sshd.Status -ne "Running") {
            Start-Service sshd
            Set-Service -Name sshd -StartupType Automatic
            Write-Host "  Started OpenSSH server" -ForegroundColor Green
        } else {
            Write-Host "  OpenSSH server already running" -ForegroundColor Green
        }
    } else {
        Write-Host "  WARNING: OpenSSH Server not installed." -ForegroundColor Yellow
        Write-Host "  Install it: Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0" -ForegroundColor White
    }
} else {
    Write-Host "  No satibook-key.pub found on USB, skipping SSH key setup" -ForegroundColor Yellow
}

# --- Create helper scripts ---
Write-Host "`nCreating helper scripts..." -ForegroundColor Yellow

# start-iceccd.bat
$iceScript = @'
@echo off
REM Start icecream daemon to join claw-fleet distributed compilation cluster
wsl -d Ubuntu -u root -- bash -c "pkill iceccd 2>/dev/null; sleep 1; iceccd -s 100.108.202.49 -n claw-fleet -d 2>&1; sleep 3; pgrep iceccd && echo 'iceccd started - joined claw-fleet' || echo 'FAILED to start iceccd'"
pause
'@
Set-Content -Path (Join-Path $scriptDir "start-iceccd.bat") -Value $iceScript -Encoding ASCII

# start-exo.bat
$exoScript = @'
@echo off
REM Start exo distributed inference node
REM Nodes auto-discover each other via mDNS on the same network
echo Starting exo node...
wsl -d Ubuntu -u root -- bash -c "export PATH='/root/.local/bin:/root/.cargo/bin:$PATH'; cd /opt/exo && uv run exo --api-port 52415"
'@
Set-Content -Path (Join-Path $scriptDir "start-exo.bat") -Value $exoScript -Encoding ASCII

# start-all.bat
$allScript = @'
@echo off
REM Start both icecream and exo for full claw-fleet participation
echo === Starting icecream daemon ===
start /b wsl -d Ubuntu -u root -- bash -c "pkill iceccd 2>/dev/null; sleep 1; iceccd -s 100.108.202.49 -n claw-fleet -d 2>&1; sleep 3; pgrep iceccd && echo 'iceccd OK' || echo 'iceccd FAILED'"
timeout /t 5 /nobreak > nul
echo === Starting exo inference node ===
wsl -d Ubuntu -u root -- bash -c "export PATH='/root/.local/bin:/root/.cargo/bin:$PATH'; cd /opt/exo && uv run exo --api-port 52415"
'@
Set-Content -Path (Join-Path $scriptDir "start-all.bat") -Value $allScript -Encoding ASCII

Write-Host "  Created: start-iceccd.bat" -ForegroundColor Green
Write-Host "  Created: start-exo.bat" -ForegroundColor Green
Write-Host "  Created: start-all.bat" -ForegroundColor Green

# --- Summary ---
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  claw-fleet Cluster Join Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  This node:    $(hostname)" -ForegroundColor White
Write-Host "  Cluster:      claw-fleet" -ForegroundColor White
Write-Host "  Scheduler:    100.108.202.49 (cnc-server)" -ForegroundColor White
Write-Host ""
Write-Host "  Helper scripts (run after reboot):" -ForegroundColor Yellow
Write-Host "    start-iceccd.bat  - Join distributed compilation cluster" -ForegroundColor White
Write-Host "    start-exo.bat     - Join distributed AI inference cluster" -ForegroundColor White
Write-Host "    start-all.bat     - Start both services" -ForegroundColor White
Write-Host ""
Write-Host "  exo dashboard: http://localhost:52415" -ForegroundColor White
Write-Host "  exo nodes auto-discover via mDNS on the same network." -ForegroundColor White
Write-Host ""
