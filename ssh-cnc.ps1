param([string]$cmd = "hostname")

# Get the host key fingerprint first
$output = echo "y" | & "C:\Program Files\PuTTY\plink.exe" -ssh -l root -pw "cnc-server-2024!" 10.0.0.6 "exit" 2>&1
Start-Sleep -Seconds 1

# Now run with batch mode
& "C:\Program Files\PuTTY\plink.exe" -ssh -l root -pw "cnc-server-2024!" -batch 10.0.0.6 $cmd
