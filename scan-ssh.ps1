$ips = @("10.0.0.2","10.0.0.18","10.0.0.55","10.0.0.84","10.0.0.173","10.0.0.176","10.0.0.206")
foreach ($ip in $ips) {
    try {
        $t = New-Object Net.Sockets.TcpClient
        $r = $t.BeginConnect($ip, 22, $null, $null)
        $w = $r.AsyncWaitHandle.WaitOne(500)
        if ($w -and $t.Connected) {
            Write-Host "$ip - SSH OPEN"
        }
        $t.Close()
    } catch {}
}
