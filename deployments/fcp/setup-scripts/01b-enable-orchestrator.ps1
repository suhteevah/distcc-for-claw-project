# =============================================================================
# First Choice Plastics -- Enable Orchestrator Mode
# Run this AFTER adding a Raspberry Pi or Mac Mini to the fleet.
# This turns the gaming laptop into the fleet coordinator.
# Run as Administrator
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host @"
============================================
  FCP: Enabling Orchestrator Mode
  This laptop will coordinate your fleet.
============================================
"@ -ForegroundColor Cyan

if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: Run as Administrator." -ForegroundColor Red
    exit 1
}

# --- Install AgentAPI ---
Write-Host "`n=== Installing AgentAPI ===" -ForegroundColor Yellow

$agentapiUrl = "https://github.com/coder/agentapi/releases/latest/download/agentapi-windows-amd64.exe"
$agentapiPath = "C:\Program Files\agentapi\agentapi.exe"

if (-not (Test-Path "C:\Program Files\agentapi")) {
    New-Item -ItemType Directory -Path "C:\Program Files\agentapi" -Force | Out-Null
}

Write-Host "Downloading AgentAPI..."
Invoke-WebRequest -Uri $agentapiUrl -OutFile $agentapiPath -UseBasicParsing

# Add to PATH if not already there
$machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
if ($machinePath -notlike "*agentapi*") {
    [System.Environment]::SetEnvironmentVariable("Path", "$machinePath;C:\Program Files\agentapi", "Machine")
    $env:Path += ";C:\Program Files\agentapi"
}

Write-Host "AgentAPI installed." -ForegroundColor Green

# --- Check for connected agents ---
Write-Host "`n=== Checking for fleet members ===" -ForegroundColor Yellow

$agents = @("fcp-rpi", "fcp-mac-mini")
foreach ($agent in $agents) {
    try {
        $result = tailscale ping --timeout 3s $agent 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[FOUND] $agent is reachable" -ForegroundColor Green
        } else {
            Write-Host "[----]  $agent not found (that's OK if not set up yet)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "[----]  $agent not found" -ForegroundColor Gray
    }
}

Write-Host @"

============================================
  Orchestrator Mode Ready
============================================

To start coordinating agents, run:

  agentapi server --type claude --allowed-hosts '*' -- claude `
    --allowedTools "Read,Edit,Write,Bash(*)" `
    --max-budget-usd 10.00

Then from another terminal, send tasks:

  curl -X POST http://localhost:3284/message `
    -H 'Content-Type: application/json' `
    -d '{"content": "Check status of all fleet machines"}'

Check agent status:
  curl http://fcp-rpi:3284/status
  curl http://fcp-mac-mini:3284/status

"@
