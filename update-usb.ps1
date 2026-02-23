# Clean and copy new combustion files to USB
$src = "J:\distcc for claw project"
$dst = "H:\combustion"

Write-Host "Cleaning old combustion files..."
Remove-Item "$dst\*" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Copying new files..."
Copy-Item "$src\combustion\script" "$dst\script" -Force
Copy-Item "$src\cnc-server-bootstrap.sh" "$dst\cnc-server-bootstrap.sh" -Force
Copy-Item "$src\.secrets" "$dst\.secrets" -Force

# Fix CRLF -> LF on all files
Write-Host "Fixing line endings to Unix LF..."
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
foreach ($f in Get-ChildItem $dst -Force) {
    $content = [System.IO.File]::ReadAllText($f.FullName)
    $content = $content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($f.FullName, $content, $utf8NoBom)
    Write-Host "  Fixed: $($f.Name)"
}

# Verify
Write-Host ""
Write-Host "USB combustion contents:"
Get-ChildItem $dst -Force | Format-Table Name, Length -AutoSize

# Verify no CR bytes
Write-Host "Line ending check:"
foreach ($f in Get-ChildItem $dst -Force) {
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $cr = ($bytes | Where-Object { $_ -eq 13 }).Count
    if ($cr -gt 0) {
        Write-Host "  $($f.Name): STILL HAS $cr CR BYTES - PROBLEM" -ForegroundColor Red
    } else {
        Write-Host "  $($f.Name): LF only - OK" -ForegroundColor Green
    }
}

# Verify shebang
$first15 = [System.Text.Encoding]::ASCII.GetString(
    [System.IO.File]::ReadAllBytes("$dst\script"), 0, 15
)
Write-Host ""
Write-Host "Shebang check: $first15"
