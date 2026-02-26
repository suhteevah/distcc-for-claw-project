#!/usr/bin/env python3
"""Quick check what's happening on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

# Check running processes and disk usage
stdin, stdout, stderr = c.exec_command("""
echo "=== Running uv/python processes ==="
ps aux | grep -E 'uv|pip|python' | grep -v grep
echo ""
echo "=== /opt/exo disk usage ==="
du -sh /opt/exo/.venv 2>&1
echo ""
echo "=== /opt/exo/.venv/lib size ==="
du -sh /opt/exo/.venv/lib/python3.13/site-packages/ 2>&1
echo ""
echo "=== Recent files in cache ==="
ls -latr /root/.cache/uv/ 2>&1 | tail -5
echo ""
echo "=== Network activity ==="
ss -s 2>&1 | head -5
echo ""
echo "=== uv.lock torch entry ==="
grep -A3 'name = "torch"' /opt/exo/uv.lock 2>&1 | head -10
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
