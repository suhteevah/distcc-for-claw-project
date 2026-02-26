#!/usr/bin/env python3
"""Check rsync progress on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
echo "=== rsync running? ==="
ps aux | grep rsync | grep -v grep

echo ""
echo "=== sshd connections ==="
ss -tnp 2>&1 | grep ':22 ' | head -10

echo ""
echo "=== uv cache size ==="
du -sh /root/.cache/uv/ 2>&1

echo ""
echo "=== uv pip running? ==="
ps aux | grep 'uv pip' | grep -v grep | head -5
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
