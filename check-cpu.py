#!/usr/bin/env python3
"""Check what uv is doing on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
echo "=== CPU usage (uv/rustc/cargo/cc) ==="
top -bn1 | grep -E 'uv|rustc|cargo|cc1|pip|python' | head -15

echo ""
echo "=== strace on uv pid ==="
UV_PID=$(pgrep -f 'uv sync' | head -1)
if [ -n "$UV_PID" ]; then
    echo "uv PID: $UV_PID"
    ls -la /proc/$UV_PID/fd 2>&1 | tail -10
    echo ""
    echo "=== uv cwd ==="
    readlink /proc/$UV_PID/cwd 2>&1
    echo ""
    echo "=== Open files ==="
    ls -la /proc/$UV_PID/fd 2>&1 | grep -v pipe | grep -v socket | tail -10
else
    echo "uv sync not running!"
fi

echo ""
echo "=== Active network connections ==="
ss -tnp 2>&1 | grep -E 'ESTAB' | head -10

echo ""
echo "=== IO wait ==="
iostat -x 1 1 2>&1 | tail -5
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
