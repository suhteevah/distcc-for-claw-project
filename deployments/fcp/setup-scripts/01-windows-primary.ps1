# =============================================================================
# First Choice Plastics -- Primary Windows Gaming Laptop Setup
# Role: Primary workstation, future orchestrator when fleet expands
# Run as Administrator
# =============================================================================

$ErrorActionPreference = "Stop"

$Hostname = "fcp-laptop"

Write-Host @"
============================================
  First Choice Plastics
  Setting up: $Hostname (Gaming Laptop)
============================================
"@ -ForegroundColor Cyan

# --- Admin check ---
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: Right-click PowerShell > Run as Administrator" -ForegroundColor Red
    exit 1
}

# --- Chocolatey ---
Write-Host "`n=== Installing package manager ===" -ForegroundColor Yellow
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# --- Dependencies ---
Write-Host "`n=== Installing dependencies ===" -ForegroundColor Yellow
choco install -y nodejs-lts git ripgrep

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "Node.js: $(node --version)"

# --- Tailscale (pre-positioned for future fleet expansion) ---
Write-Host "`n=== Installing Tailscale ===" -ForegroundColor Yellow
if (-not (Get-Command tailscale -ErrorAction SilentlyContinue)) {
    choco install -y tailscale
}
Write-Host @"

Tailscale provides secure networking between your machines.
It's free for up to 100 devices.

>>> Open the Tailscale app and sign in.
>>> Then run: tailscale up --hostname $Hostname

"@ -ForegroundColor White
Read-Host "Press Enter after Tailscale is set up"

# --- Claude Code ---
Write-Host "`n=== Installing Claude Code ===" -ForegroundColor Yellow
npm install -g @anthropic-ai/claude-code

Write-Host @"

============================================
  ANTHROPIC API KEY REQUIRED
============================================

You need an API key to use Claude Code.

1. Go to: https://console.anthropic.com/
2. Create an account (or sign in)
3. Go to API Keys
4. Create a new key (name it "fcp")
5. Copy the key

Then run: claude auth login
   OR set: $env:ANTHROPIC_API_KEY = "your-key-here"

"@ -ForegroundColor Yellow

# --- Authenticate ---
Write-Host ">>> Run 'claude auth login' now to authenticate." -ForegroundColor White
Read-Host "Press Enter after you've authenticated Claude Code"

# --- Verify ---
Write-Host "`n=== Verifying installation ===" -ForegroundColor Yellow
try {
    $version = claude --version 2>&1
    Write-Host "Claude Code: $version" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not verify Claude Code. Run 'claude --version' manually." -ForegroundColor Yellow
}

# --- GPU Detection + Ollama ---
Write-Host "`n=== GPU Detection + Ollama ===" -ForegroundColor Yellow

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SharedModule = Join-Path (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))) "shared\ollama-gpu-detect.ps1"

if (Test-Path $SharedModule) {
    . $SharedModule
    Install-OllamaWithModel
} else {
    Write-Host "  WARNING: ollama-gpu-detect.ps1 not found." -ForegroundColor Yellow
    Write-Host "  Copy shared/ollama-gpu-detect.ps1 from the project root and re-run." -ForegroundColor Yellow
}

Write-Host @"

============================================
  First Choice Plastics - READY
  Machine: $Hostname (Gaming Laptop)
============================================

You're set up! Here's how to use it:

  claude                Open Claude Code (interactive)
  claude -p "task"      Run a one-shot task
  tailscale status      Check network status
"@

if ($script:OllamaInstalled) {
    Write-Host "  Ollama model:   $($script:OllamaModel)" -ForegroundColor Green
    Write-Host "  Test it:        ollama run $($script:OllamaModel) 'Hello world in C'" -ForegroundColor Gray
} else {
    Write-Host "  Ollama:         not installed (no discrete GPU)" -ForegroundColor Gray
}

Write-Host @"

NEXT STEPS (when you get a Raspberry Pi):
  1. Flash 64-bit Raspberry Pi OS
  2. Copy the 'fcp' deployment folder to the Pi
  3. Run: ./setup-scripts/02-raspberry-pi.sh fcp-rpi
  4. Then run: .\setup-scripts\01b-enable-orchestrator.ps1
     on this laptop to start coordinating both machines

"@
