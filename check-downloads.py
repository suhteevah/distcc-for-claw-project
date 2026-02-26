#!/usr/bin/env python3
"""Check download progress on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
echo "=== uv cache size ==="
du -sh /root/.cache/uv/ 2>&1

echo ""
echo "=== Temp download dirs ==="
for d in /root/.cache/uv/.tmp*/; do
    size=$(du -sh "$d" 2>/dev/null | cut -f1)
    echo "  $d  $size"
done 2>&1 | tail -20

echo ""
echo "=== Disk space ==="
df -h /opt /root 2>&1

echo ""
echo "=== uv sync still running? ==="
ps aux | grep 'uv sync' | grep -v grep

echo ""
echo "=== Network connections to PyPI/torch ==="
ss -tnp 2>&1 | grep -E 'pypi|pytorch|files.python' | head -10
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
