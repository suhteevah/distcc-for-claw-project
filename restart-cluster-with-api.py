#!/usr/bin/env python3
"""Restart exo cluster with API enabled on kokonoe (master)."""
import paramiko, subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ===== Step 1: Kill existing exo on both nodes =====
print("=" * 60)
print("  Step 1: Kill existing exo processes")
print("=" * 60)

# Kill on cnc-server
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
stdin, stdout, stderr = c.exec_command("pkill -f 'python.*exo' 2>/dev/null; sleep 1; echo 'cnc-server: killed'", timeout=10)
print(stdout.read().decode().strip())
c.close()

# Kill on kokonoe
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     "pkill -f 'python.*exo' 2>/dev/null; sleep 1; echo 'kokonoe: killed'"],
    capture_output=True, text=True, timeout=10
)
print(result.stdout.strip())

time.sleep(2)

# ===== Step 2: Start cnc-server (worker, no downloads, no api) =====
print("\n" + "=" * 60)
print("  Step 2: Start cnc-server (CPU worker)")
print("=" * 60)

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

# Write startup script
stdin, stdout, stderr = c.exec_command("""
cat > /tmp/start-exo.sh << 'SCRIPT'
#!/bin/bash
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
EXO_LIBP2P_PORT=42000 .venv/bin/python -m exo -v --no-downloads --no-api > /tmp/exo-stdout.log 2>&1
SCRIPT
chmod +x /tmp/start-exo.sh
echo 'script written'
""", timeout=10)
print(stdout.read().decode().strip())

# Launch daemon
stdin, stdout, stderr = c.exec_command(
    "setsid /tmp/start-exo.sh &>/dev/null & echo $!",
    timeout=10
)
pid = stdout.read().decode().strip()
print(f"cnc-server started with PID: {pid}")
c.close()

time.sleep(5)

# Verify cnc-server
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
stdin, stdout, stderr = c.exec_command("""
echo "=== Process ==="
ps aux | grep 'python.*exo' | grep -v grep
echo ""
echo "=== Listening ==="
ss -tlnp | grep python
echo ""
echo "=== Log ==="
tail -10 /tmp/exo-stdout.log 2>&1
""", timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()

# ===== Step 3: Start kokonoe (master, WITH API) =====
print("=" * 60)
print("  Step 3: Start kokonoe (master, WITH API)")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', """
cd /opt/exo
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"

# Start exo WITH API (no --no-api flag), bootstrap to cnc-server
EXO_LIBP2P_PORT=42001 EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000 \
    nohup .venv/bin/python -m exo -v > /tmp/exo-stdout.log 2>&1 &
echo "PID=$!"

sleep 8

echo ""
echo "=== Process ==="
ps aux | grep 'python.*exo' | grep -v grep

echo ""
echo "=== Listening ports ==="
ss -tlnp | grep python

echo ""
echo "=== TCP connections ==="
ss -tnp | grep python | head -5

echo ""
echo "=== Log (last 30 lines) ==="
tail -30 /tmp/exo-stdout.log 2>&1
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
