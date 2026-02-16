# =============================================================================
# Dr Paper -- Windows Human Workstation Setup
# Run this on: Swoop's Windows Desktop or Windows Laptop
# Role: Interactive Claude Code + icecream build worker (via WSL)
# Run as Administrator
#
# Usage: .\05-windows-workstation.ps1 -Hostname <name>
#   e.g.: .\05-windows-workstation.ps1 -Hostname swoop-windows-desktop
#   e.g.: .\05-windows-workstation.ps1 -Hostname swoop-windows-laptop
# =============================================================================

param(
    [string]$Hostname = ""
)

$ErrorActionPreference = "Stop"

if (-not $Hostname) {
    $Hostname = Read-Host "Enter Tailscale hostname (e.g., swoop-windows-desktop or swoop-windows-laptop)"
}

Write-Host "=== Setting up $Hostname for Dr Paper ===" -ForegroundColor Cyan

if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: Run as Administrator." -ForegroundColor Red
    exit 1
}

# Chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

choco install -y nodejs-lts git ripgrep ccache

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Tailscale
if (-not (Get-Command tailscale -ErrorAction SilentlyContinue)) {
    choco install -y tailscale
}
Write-Host ">>> Open Tailscale, authenticate, then: tailscale up --hostname $Hostname"
Read-Host "Press Enter after authenticated"

# Icecream
Write-Host @"

Icecream has no native Windows build. Options:
  A) Install WSL2 with Ubuntu, then: sudo apt install -y icecc
     Edit /etc/default/icecc: ICECC_SCHEDULER_HOST="dr-paper"
  B) Skip icecream, use this machine for Claude Code only.
"@

# Claude Code
npm install -g @anthropic-ai/claude-code

Write-Host @"

You need an Anthropic API key.
Get one at: https://console.anthropic.com/

"@

claude --version

# GPU Detection + Ollama
Write-Host "`n=== GPU Detection + Ollama ===" -ForegroundColor Yellow

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Walk up to project root and find shared module
$SharedModule = Join-Path (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))) "shared\ollama-gpu-detect.ps1"

if (Test-Path $SharedModule) {
    . $SharedModule
    Install-OllamaWithModel
} else {
    Write-Host "  WARNING: ollama-gpu-detect.ps1 not found." -ForegroundColor Yellow
    Write-Host "  Copy shared/ollama-gpu-detect.ps1 from the project root and re-run." -ForegroundColor Yellow
}

# LAN Ollama discovery
Write-Host "`n=== LAN Ollama Discovery ===" -ForegroundColor Yellow
Write-Host "  Dr Paper's network has an existing Ollama server." -ForegroundColor White
$LanOllamaReachable = $false

Write-Host "  Default: 192.168.10.242 (press Enter to accept)" -ForegroundColor Gray
$lanHost = Read-Host "Ollama server hostname/IP [192.168.10.242]"
if (-not $lanHost) { $lanHost = "192.168.10.242" }
if ($lanHost -and $lanHost -ne "skip") {
    $lanUrl = "http://${lanHost}:11434"
    Write-Host "  Testing ${lanUrl}..." -ForegroundColor Gray
    try {
        $response = Invoke-WebRequest -Uri "${lanUrl}/api/tags" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Write-Host "  [OK] LAN Ollama reachable!" -ForegroundColor Green
        $LanOllamaReachable = $true
    } catch {
        Write-Host "  [FAIL] Could not connect to ${lanUrl}" -ForegroundColor Yellow
        Write-Host @"

  To fix this on the Ollama server:
    1. Set: export OLLAMA_HOST=0.0.0.0
    2. Restart Ollama: sudo systemctl restart ollama
    3. Or use Tailscale for secure cross-network access
"@ -ForegroundColor Gray
    }
}

Write-Host @"

============================================
  $Hostname connected to Dr Paper
============================================

Usage:
  claude                  (interactive Claude Code)
  tailscale status        (verify network)
"@

if ($script:OllamaInstalled) {
    Write-Host "  Ollama (local): $($script:OllamaModel)" -ForegroundColor Green
    Write-Host "  Test: ollama run $($script:OllamaModel) 'Hello world in C'" -ForegroundColor Gray
}
if ($LanOllamaReachable) {
    Write-Host "  Ollama (LAN):   ${lanUrl}" -ForegroundColor Green
    Write-Host "  Use: `$env:OLLAMA_HOST='${lanHost}:11434'; ollama run <model>" -ForegroundColor Gray
}
