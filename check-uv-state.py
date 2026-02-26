#!/usr/bin/env python3
"""Check what uv is actually doing."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
echo "=== uv + child processes ==="
ps auxf | grep -A5 'uv pip' | grep -v grep

echo ""
echo "=== Top CPU consumers ==="
top -bn1 -o %CPU | head -20

echo ""
echo "=== /proc/PID info for uv ==="
UV_PID=$(pgrep -f 'uv pip install --python' | head -1)
if [ -n "$UV_PID" ]; then
    echo "uv PID: $UV_PID"
    echo "  status: $(cat /proc/$UV_PID/status 2>&1 | grep -E 'State|VmRSS|Threads')"
    echo "  fds: $(ls /proc/$UV_PID/fd 2>&1 | wc -l)"
    echo "  open files:"
    ls -la /proc/$UV_PID/fd 2>&1 | grep -v 'pipe\|socket\|anon_inode' | tail -10
fi

echo ""
echo "=== Any cargo/rustc running? ==="
pgrep -la 'cargo\|rustc\|cc1plus\|maturin' 2>&1 || echo "none"

echo ""
echo "=== Network connections for PID tree ==="
ss -tnp 2>&1 | grep -E "uv|45|46|47" | head -10
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
