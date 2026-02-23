param([string]$cmd = "hostname")
# Cache the host key first
echo "y" | & "C:\Program Files\PuTTY\plink.exe" -ssh -l root -pw "cnc-server-2024!" 10.0.0.55 "exit" 2>$null
# Now run the actual command
& "C:\Program Files\PuTTY\plink.exe" -ssh -l root -pw "cnc-server-2024!" -batch 10.0.0.55 $cmd
