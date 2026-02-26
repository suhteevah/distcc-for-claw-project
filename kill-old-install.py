#!/usr/bin/env python3
"""Kill old duplicate install process on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
# Kill the older duplicate process (PID 45274 bash + 45287 uv)
kill 45274 45287 2>&1
echo "Killed old install process"
sleep 2

# Verify only one remains
echo ""
echo "=== Remaining uv processes ==="
ps aux | grep 'uv pip' | grep -v grep
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
