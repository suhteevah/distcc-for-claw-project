#!/usr/bin/env python3
"""Start exo cluster: cnc-server as listener, kokonoe dials in."""
import paramiko, subprocess, sys, io, time, threading

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# === Start cnc-server exo (background, fixed port, no downloads) ===
print("="*60)
print("  Starting cnc-server exo (CPU worker, port 42000)")
print("="*60)

cnc = paramiko.SSHClient()
cnc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cnc.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

# Kill any existing exo
cnc.exec_command("pkill -f 'python.*exo' 2>/dev/null", timeout=10)
time.sleep(2)

# Start exo on cnc-server in background
cnc_stdin, cnc_stdout, cnc_stderr = cnc.exec_command(
    """export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
EXO_LIBP2P_PORT=42000 nohup .venv/bin/python -m exo -v --no-downloads --no-api 2>&1 &
sleep 5
echo "=== exo process ==="
ps aux | grep 'python.*exo' | grep -v grep
echo ""
echo "=== Listening ports ==="
ss -tlnp 2>&1 | grep -E '42000|python'
echo ""
echo "=== Last 20 log lines ==="
tail -20 /root/.cache/exo/exo_log/exo.log 2>&1
""",
    timeout=30
)
cnc_out = cnc_stdout.read().decode('utf-8', errors='replace')
cnc_err = cnc_stderr.read().decode('utf-8', errors='replace')
print(cnc_out + cnc_err)

# === Start kokonoe exo (with bootstrap peer to cnc-server) ===
print("\n" + "="*60)
print("  Starting kokonoe exo (GPU worker, bootstrap to cnc-server)")
print("="*60)

# Kill any existing exo on kokonoe
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     "pkill -f 'python.*exo' 2>/dev/null"],
    capture_output=True, timeout=10
)
time.sleep(2)

# Start exo on kokonoe in background, with bootstrap peer
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
EXO_LIBP2P_PORT=42001 EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000 \
    nohup .venv/bin/python -m exo -v 2>&1 &
sleep 8

echo "=== exo process ==="
ps aux | grep 'python.*exo' | grep -v grep

echo ""
echo "=== Listening ports ==="
ss -tlnp 2>&1 | grep -E '42001|python'

echo ""
echo "=== Last 30 log lines ==="
tail -30 /root/.cache/exo/exo_log/exo.log 2>&1
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)

# Wait a bit for connection
print("\n" + "="*60)
print("  Waiting 10s for peer discovery...")
print("="*60)
time.sleep(10)

# Check cluster status on both
print("\n" + "="*60)
print("  Checking cluster status")
print("="*60)

# Check cnc-server logs for connection
cnc2 = paramiko.SSHClient()
cnc2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cnc2.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
stdin, stdout, stderr = cnc2.exec_command(
    r"""
echo "=== cnc-server: last 40 log lines ==="
tail -40 /root/.cache/exo/exo_log/exo.log 2>&1

echo ""
echo "=== cnc-server: connections ==="
ss -tnp 2>&1 | grep python | head -10
""", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
cnc2.close()

# Check kokonoe logs
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     r"""
echo "=== kokonoe: last 40 log lines ==="
tail -40 /root/.cache/exo/exo_log/exo.log 2>&1

echo ""
echo "=== kokonoe: connections ==="
ss -tnp 2>&1 | grep python | head -10
"""],
    capture_output=True, text=True, timeout=15
)
print(result.stdout + result.stderr)

cnc.close()
print("\nCluster startup complete!")
