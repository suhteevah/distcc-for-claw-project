#!/usr/bin/env python3
"""Reboot cnc-server and verify all services come back up with icecream+distcc active."""

import paramiko
import time
import sys
import io
import socket

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = "10.0.0.6"
USER = "root"
PASS = "cnc-server-2024!"

def ssh_connect(timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=timeout)
    return client

def run(client, cmd, timeout=30):
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        return (out + err).strip(), code
    except Exception as e:
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Issue reboot
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  1. Rebooting cnc-server...")
print("=" * 60)

client = ssh_connect()
# Fire and forget - reboot will kill the connection
try:
    client.exec_command("systemctl reboot", timeout=5)
except:
    pass
time.sleep(2)
try:
    client.close()
except:
    pass

print("  Reboot command sent. Waiting for server to go down...")

# ═══════════════════════════════════════════════════════════════════════
# 2. Wait for server to go down
# ═══════════════════════════════════════════════════════════════════════
down = False
for i in range(30):
    try:
        s = socket.create_connection((HOST, 22), timeout=3)
        s.close()
        print(f"  [{i*2}s] Still up...")
        time.sleep(2)
    except:
        print(f"  [{i*2}s] Server is DOWN")
        down = True
        break

if not down:
    print("  WARNING: Server didn't appear to go down. Continuing anyway...")

# ═══════════════════════════════════════════════════════════════════════
# 3. Wait for server to come back
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  2. Waiting for server to come back up...")
print("=" * 60)

up = False
for i in range(90):  # up to 3 minutes
    try:
        s = socket.create_connection((HOST, 22), timeout=3)
        s.close()
        print(f"  [{i*3}s] SSH port is open!")
        up = True
        break
    except:
        if i % 5 == 0:
            print(f"  [{i*3}s] Waiting...")
        time.sleep(3)

if not up:
    print("  ERROR: Server did not come back within 4.5 minutes!")
    sys.exit(1)

# Give services a moment to start
print("  Waiting 15s for services to initialize...")
time.sleep(15)

# ═══════════════════════════════════════════════════════════════════════
# 4. Verify everything
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  3. Verifying services and new packages")
print("=" * 60)

client = ssh_connect(timeout=15)

# Check snapshot
out, _ = run(client, "snapper list 2>&1 | tail -5")
print(f"\n  Snapshots:\n  {out.replace(chr(10), chr(10) + '  ')}")

# Check uptime
out, _ = run(client, "uptime")
print(f"\n  Uptime: {out}")

# Check all services
services = [
    "tailscaled", "ollama", "rtw88-wifi", "wpa-wifi",
    "dhcpcd-wifi", "firewalld", "claude-agentapi", "claude-orchestrator"
]
print("\n  Services:")
for svc in services:
    out, _ = run(client, f"systemctl is-active {svc} 2>&1")
    status = out.strip()
    icon = "●" if status == "active" else "○"
    print(f"    {icon} {svc:30s} {status}")

# Check icecream + distcc
print("\n  New packages:")
out, _ = run(client, "rpm -q icecream distcc 2>&1")
print(f"  {out.replace(chr(10), chr(10) + '  ')}")

out, _ = run(client, "which icecc 2>&1 && icecc --version 2>&1 || echo 'icecc not found'")
print(f"\n  icecc: {out}")

out, _ = run(client, "which distcc 2>&1 && distcc --version 2>&1 | head -1 || echo 'distcc not found'")
print(f"  distcc: {out}")

# Check endpoints
print("\n  Endpoints:")
import subprocess
for name, url in [
    ("Orchestrator", "http://10.0.0.6:8080/api/health"),
    ("AgentAPI", "http://10.0.0.6:8765"),
    ("Ollama", "http://10.0.0.6:11434"),
]:
    out, _ = run(client, f"curl -s -o /dev/null -w '%{{http_code}}' {url} 2>&1", timeout=10)
    print(f"    {name:20s} HTTP {out}")

# DNS still working?
out, _ = run(client, "ping -c 1 -W 3 google.com 2>&1 | head -2")
print(f"\n  DNS: {out}")

# WiFi still connected?
out, _ = run(client, "iw wlan0 link 2>&1 | head -3")
print(f"\n  WiFi: {out}")

# Tailscale
out, _ = run(client, "tailscale status 2>&1 | head -8")
print(f"\n  Tailscale:\n  {out.replace(chr(10), chr(10) + '  ')}")

# Final summary
print("\n" + "=" * 60)
print("  ╔══════════════════════════════════════════════════════╗")
print("  ║     cnc-server Reboot Complete                       ║")
print("  ╚══════════════════════════════════════════════════════╝")

client.close()
print("\nDone!")
