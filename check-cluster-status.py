#!/usr/bin/env python3
"""Check cluster status from both nodes."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Check cnc-server
print("="*60)
print("  cnc-server cluster view")
print("="*60)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

stdin, stdout, stderr = c.exec_command("""
echo "=== TCP connections ==="
ss -tnp 2>&1 | grep python | head -10

echo ""
echo "=== Last 30 log lines ==="
tail -30 /tmp/exo-stdout.log 2>&1

echo ""
echo "=== Memory ==="
free -h
""", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()

# Check kokonoe
print("="*60)
print("  kokonoe cluster view")
print("="*60)
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     """
echo "=== TCP connections ==="
ss -tnp 2>&1 | grep python | head -10

echo ""
echo "=== Grep for connection/election events ==="
grep -E 'Connected|Disconnected|elected|Election|connection.*established|peer' /tmp/exo-stdout.log 2>&1 | tail -20
"""],
    capture_output=True, text=True, timeout=15
)
print(result.stdout + result.stderr)
