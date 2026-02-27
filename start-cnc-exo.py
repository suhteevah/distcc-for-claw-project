#!/usr/bin/env python3
"""Start exo on cnc-server as background daemon."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

# Kill existing
stdin, stdout, stderr = c.exec_command("pkill -f 'python.*exo' 2>/dev/null; sleep 1; echo killed", timeout=10)
print("Killed old:", stdout.read().decode().strip())

# Start exo as daemon (fully detached, logs to file)
stdin, stdout, stderr = c.exec_command(
    'bash -c \'export PATH="/root/.local/bin:/root/.cargo/bin:$PATH" && '
    'cd /opt/exo && '
    'EXO_LIBP2P_PORT=42000 '
    'nohup .venv/bin/python -m exo -v --no-downloads --no-api '
    '> /tmp/exo-stdout.log 2>&1 & '
    'echo $!\'',
    timeout=10
)
pid = stdout.read().decode().strip()
print(f"Started exo with PID: {pid}")

import time
time.sleep(5)

# Check it's running
stdin, stdout, stderr = c.exec_command("ps aux | grep 'python.*exo' | grep -v grep", timeout=10)
print("\nProcess:", stdout.read().decode().strip())

stdin, stdout, stderr = c.exec_command("ss -tlnp | grep 42000", timeout=10)
print("Listening:", stdout.read().decode().strip())

stdin, stdout, stderr = c.exec_command("tail -30 /tmp/exo-stdout.log 2>&1", timeout=10)
print("\nStdout log:")
print(stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = c.exec_command("tail -30 /root/.cache/exo/exo_log/exo.log 2>&1", timeout=10)
print("Exo log:")
print(stdout.read().decode('utf-8', errors='replace'))

c.close()
