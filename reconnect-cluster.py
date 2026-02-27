#!/usr/bin/env python3
"""Check and reconnect cluster nodes."""
import paramiko, subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Check cnc-server
print("=== cnc-server status ===")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('100.108.202.49', username='root', password='cnc-server-2024!', timeout=10)

stdin, stdout, stderr = c.exec_command('ps aux | grep exo | grep -v grep; echo ---; ss -tlnp | grep 42000; echo ---; tail -20 /tmp/exo-stdout.log', timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))

# Restart cnc-server with bootstrap peer pointing to kokonoe
print("=== Restarting cnc-server with bootstrap to kokonoe ===")
stdin, stdout, stderr = c.exec_command('pkill -f "python.*exo" 2>&1; sleep 2; echo Killed old process', timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))

# Write and start new script with bootstrap peer
start_script = '#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42000\nexport EXO_BOOTSTRAP_PEERS=/ip4/100.90.71.97/tcp/42001\nexec .venv/bin/python -m exo -v --no-api\n'
sftp = c.open_sftp()
with sftp.open('/tmp/start-exo.sh', 'w') as f:
    f.write(start_script)
sftp.close()

stdin, stdout, stderr = c.exec_command('chmod +x /tmp/start-exo.sh && setsid /tmp/start-exo.sh > /tmp/exo-stdout.log 2>&1 &\nsleep 5\nps aux | grep exo | grep -v grep\necho ---\nss -tlnp | grep 42000', timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))

# Wait for connection
time.sleep(10)

# Check cnc-server pong
stdin, stdout, stderr = c.exec_command('grep "pong" /tmp/exo-stdout.log | tail -5', timeout=10)
print("cnc-server pings:", stdout.read().decode('utf-8', errors='replace'))

c.close()

# Check kokonoe side
time.sleep(5)
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'grep "pong" /tmp/exo-stdout.log | tail -5'],
    capture_output=True, text=True, timeout=10
)
print("=== kokonoe pings ===")
print(result.stdout)

# Check P2P connections
result2 = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'ss -tnp | grep -E "ESTAB.*42000|ESTAB.*42001"'],
    capture_output=True, text=True, timeout=10
)
print("=== P2P connections ===")
print(result2.stdout if result2.stdout.strip() else "No P2P connections yet")
