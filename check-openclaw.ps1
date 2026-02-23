try {
    $r = Invoke-WebRequest -Uri "http://localhost:8080" -TimeoutSec 3 -UseBasicParsing
    Write-Host "Status: $($r.StatusCode)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Check what's listening on 8080
Write-Host ""
Write-Host "Port 8080 listeners:"
Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Format-Table LocalAddress, LocalPort, State, OwningProcess -AutoSize

# Check for any openclaw/claude processes
Write-Host ""
Write-Host "Related processes:"
Get-Process | Where-Object { $_.ProcessName -match "node|deno|claude|openclaw" } | Format-Table Id, ProcessName, CPU, WorkingSet -AutoSize
