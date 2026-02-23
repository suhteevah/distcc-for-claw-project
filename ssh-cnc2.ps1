# Accept the host key by writing to PuTTY's registry directly
$keyData = "0x" + "00000023" # placeholder - we'll use a different approach

# Use plink with -no-antispoof and pipe y for host key
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "C:\Program Files\PuTTY\plink.exe"
$psi.Arguments = "-ssh -l root -pw cnc-server-2024! 10.0.0.6 `"hostname; uname -r`""
$psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true

$proc = [System.Diagnostics.Process]::Start($psi)
Start-Sleep -Milliseconds 500
$proc.StandardInput.WriteLine("y")
$proc.StandardInput.Flush()
Start-Sleep -Milliseconds 500

$output = $proc.StandardOutput.ReadToEnd()
$errors = $proc.StandardError.ReadToEnd()
$proc.WaitForExit(10000)

Write-Host "STDOUT: $output"
Write-Host "STDERR: $errors"
Write-Host "EXIT: $($proc.ExitCode)"
