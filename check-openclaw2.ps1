# Check port 18789 (openclaw)
Write-Host "=== Port 18789 (OpenClaw) ==="
Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue | Format-Table LocalAddress, LocalPort, State, OwningProcess -AutoSize

# Check port 11434 (Ollama)
Write-Host "=== Port 11434 (Ollama) ==="
Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue | Format-Table LocalAddress, LocalPort, State, OwningProcess -AutoSize

# Check for openclaw/deno processes
Write-Host "=== Deno/OpenClaw processes ==="
Get-Process | Where-Object { $_.ProcessName -match "deno|openclaw" } | Format-Table Id, ProcessName, Path -AutoSize

# Check if openclaw is installed
Write-Host "=== OpenClaw install location ==="
$paths = @(
    "$env:USERPROFILE\.openclaw",
    "$env:APPDATA\openclaw",
    "$env:LOCALAPPDATA\openclaw"
)
foreach ($p in $paths) {
    if (Test-Path $p) {
        Write-Host "FOUND: $p"
        Get-ChildItem $p -Force | Format-Table Name, Length -AutoSize
    }
}

# Check for openclaw in npm global
Write-Host "=== npm global packages with openclaw ==="
npm list -g --depth=0 2>$null | Select-String "openclaw|claw"

# Check where deno is
Write-Host "=== Deno location ==="
Get-Command deno -ErrorAction SilentlyContinue | Select-Object Source
