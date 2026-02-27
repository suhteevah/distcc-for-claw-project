#!/usr/bin/env python3
"""Restart exo on kokonoe with API and bootstrap peer."""
import subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Write the startup script
script = '#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42001\nexport EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000\nexec .venv/bin/python -m exo -v\n'
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'tee', '/tmp/start-exo-kokonoe.sh'],
    input=script.encode(), capture_output=True, timeout=5
)
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'chmod', '755', '/tmp/start-exo-kokonoe.sh'],
    capture_output=True, timeout=5
)

# Start as daemon
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'setsid /tmp/start-exo-kokonoe.sh > /tmp/exo-stdout.log 2>&1 &\necho Started\nsleep 5\nps aux | grep exo | grep -v grep | head -3\necho ---\nss -tlnp | grep python'],
    capture_output=True, text=True, timeout=20
)
print(result.stdout)
print(result.stderr[:500] if result.stderr else '')
