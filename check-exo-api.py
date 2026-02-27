#!/usr/bin/env python3
"""Check exo API and model capabilities on both nodes."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ===== Check kokonoe (master node, has GPU) =====
print("=" * 60)
print("  kokonoe - exo API and model check")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', """
cd /opt/exo

echo "=== exo CLI flags ==="
.venv/bin/python -m exo --help 2>&1

echo ""
echo "=== Available model configs ==="
find . -path '*/models*' -name '*.py' 2>/dev/null | head -20
find . -path '*/models*' -name '*.json' 2>/dev/null | head -20

echo ""
echo "=== Check exo inference module ==="
find . -name 'inference*' -type f 2>/dev/null | head -20

echo ""
echo "=== Check main.py for API details ==="
grep -n 'api\|API\|port\|52415\|chat\|completions\|model' src/exo/main.py 2>&1 | head -40

echo ""
echo "=== Check for model registry / supported models ==="
grep -rn 'supported\|model_id\|model_name\|MODELS\|model_list\|registry' src/exo/ --include='*.py' 2>/dev/null | head -40

echo ""
echo "=== Current processes ==="
ps aux | grep python | grep exo | grep -v grep

echo ""
echo "=== Is port 52415 listening? ==="
ss -tlnp | grep 52415 2>&1

echo ""
echo "=== All listening ports for python ==="
ss -tlnp | grep python 2>&1
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)

# ===== Check cnc-server =====
print("=" * 60)
print("  cnc-server - exo process check")
print("=" * 60)

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

stdin, stdout, stderr = c.exec_command("""
echo "=== All listening ports for python ==="
ss -tlnp | grep python 2>&1

echo ""
echo "=== exo process ==="
ps aux | grep python | grep exo | grep -v grep
""", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
