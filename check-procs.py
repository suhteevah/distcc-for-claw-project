#!/usr/bin/env python3
"""Check running processes on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
echo "=== All uv/python/pip/cargo/rustc processes ==="
ps aux | grep -E 'uv |pip|cargo|rustc|maturin' | grep -v grep

echo ""
echo "=== SSH sessions ==="
who 2>&1

echo ""
echo "=== bash commands running ==="
ps aux | grep 'bash -c' | grep -v grep

echo ""
echo "=== venv status ==="
ls -la /opt/exo/.venv/bin/python 2>&1
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
uv pip list --python .venv/bin/python 2>&1 | wc -l
echo "packages"

echo ""
echo "=== Can exo import? ==="
/opt/exo/.venv/bin/python -c "import exo; print('YES')" 2>&1 || echo "NO"
""", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
