Start-Process -FilePath "C:\Users\Matt\.openclaw\gateway.cmd" -WindowStyle Hidden
Start-Sleep -Seconds 8

$conn = Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "OpenClaw is UP on port 18789" -ForegroundColor Green
    $conn | Format-Table LocalAddress, LocalPort, State, OwningProcess -AutoSize
} else {
    Write-Host "OpenClaw NOT listening on 18789 yet" -ForegroundColor Yellow
    # Check if the process started
    $p = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
        $_.MainModule.FileName -eq "C:\Program Files\nodejs\node.exe"
    }
    Write-Host "Node processes: $($p.Count)"
}
