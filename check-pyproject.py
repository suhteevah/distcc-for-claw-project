#!/usr/bin/env python3
"""Check exo pyproject.toml on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

# Kill any running uv installs first
stdin, stdout, stderr = c.exec_command("pkill -f 'uv pip install' 2>&1; echo killed", timeout=10)
stdout.read()

stdin, stdout, stderr = c.exec_command("cat /opt/exo/pyproject.toml", timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
