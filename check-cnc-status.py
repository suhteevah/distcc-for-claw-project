#!/usr/bin/env python3
"""Check cnc-server status."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('100.108.202.49', username='root', password='cnc-server-2024!', timeout=10)
stdin, stdout, stderr = c.exec_command('ps aux | grep exo | grep -v grep; echo ---; ss -tlnp | grep 42000', timeout=10)
print('cnc-server processes:')
print(stdout.read().decode('utf-8', errors='replace'))

# Error/warning log
stdin, stdout, stderr = c.exec_command('grep -nE "ERROR|error|Error|WARNING|Broken|Disconnect|reset|OOM|killed|timeout|close" /tmp/exo-stdout.log | tail -20', timeout=10)
print('cnc-server errors/warnings:')
print(stdout.read().decode('utf-8', errors='replace'))

# Connection logs
stdin, stdout, stderr = c.exec_command('grep -nE "pong|Connected|Disconnected" /tmp/exo-stdout.log | tail -20', timeout=10)
print('cnc-server connection logs:')
print(stdout.read().decode('utf-8', errors='replace'))

# Recent logs
stdin, stdout, stderr = c.exec_command('tail -20 /tmp/exo-stdout.log', timeout=10)
print('cnc-server recent logs:')
print(stdout.read().decode('utf-8', errors='replace'))

# Memory info
stdin, stdout, stderr = c.exec_command('free -h; echo ---; uptime', timeout=5)
print('cnc-server memory/load:')
print(stdout.read().decode('utf-8', errors='replace'))

c.close()
