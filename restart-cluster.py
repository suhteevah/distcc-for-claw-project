#!/usr/bin/env python3
"""Restart both exo nodes in proper order for stable P2P connection.

Strategy:
1. Kill exo on BOTH nodes
2. Start cnc-server first WITHOUT bootstrap (anchor node)
3. Wait for cnc-server to be listening
4. Start kokonoe WITH bootstrap pointing to cnc-server
5. Monitor P2P connection establishment
"""
import paramiko, subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def ssh_run(host, password, cmd, timeout=15):
    """Run a command on remote host via SSH and return output.
    For fire-and-forget commands, set timeout low and ignore errors."""
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username='root', password=password, timeout=10)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
    except Exception:
        out, err = "", ""
    c.close()
    return out, err

def ssh_fire_and_forget(host, password, cmd):
    """Start a command on remote host and immediately disconnect.
    Used for launching background daemons."""
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username='root', password=password, timeout=10)
    # Use invoke_shell for clean backgrounding
    chan = c.get_transport().open_session()
    chan.exec_command(cmd)
    time.sleep(1)  # Give it a moment to start
    c.close()

CNC_IP = '100.108.202.49'
CNC_PW = 'cnc-server-2024!'

# ============================================================
# Step 1: Kill exo on BOTH nodes
# ============================================================
print("=" * 60)
print("STEP 1: Killing exo on both nodes")
print("=" * 60)

# Kill on kokonoe (WSL)
print("\n--- Killing exo on kokonoe ---")
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'pkill -9 -f "python.*exo" 2>&1; sleep 1; ps aux | grep exo | grep -v grep || echo "Clean"'],
    capture_output=True, text=True, timeout=15
)
print(result.stdout.strip())

# Kill on cnc-server
print("--- Killing exo on cnc-server ---")
out, _ = ssh_run(CNC_IP, CNC_PW,
    'pkill -9 -f "python.*exo" 2>&1; sleep 1; ps aux | grep exo | grep -v grep || echo "Clean"')
print(out.strip())

# Clear logs
print("\n--- Clearing logs ---")
ssh_run(CNC_IP, CNC_PW, 'rm -f /tmp/exo-stdout.log')
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'rm', '-f', '/tmp/exo-stdout.log'],
    capture_output=True, timeout=5
)
print("Logs cleared on both nodes")

time.sleep(3)

# ============================================================
# Step 2: Start cnc-server (anchor, no bootstrap)
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Starting cnc-server (anchor node, no bootstrap)")
print("=" * 60)

# Write the startup script via SFTP
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(CNC_IP, username='root', password=CNC_PW, timeout=10)

start_cnc = "#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42000\nexec .venv/bin/python -m exo -v\n"
sftp = c.open_sftp()
with sftp.open('/tmp/start-exo.sh', 'w') as f:
    f.write(start_cnc)
sftp.close()

# Write a launcher that properly backgrounds
launcher = "#!/bin/bash\nchmod +x /tmp/start-exo.sh\nnohup /tmp/start-exo.sh </dev/null >/tmp/exo-stdout.log 2>&1 &\necho $!\n"
sftp = c.open_sftp()
with sftp.open('/tmp/launch-exo.sh', 'w') as f:
    f.write(launcher)
sftp.close()
c.close()

# Run the launcher - this should return quickly because of proper backgrounding
out, _ = ssh_run(CNC_IP, CNC_PW, 'chmod +x /tmp/launch-exo.sh && bash /tmp/launch-exo.sh', timeout=10)
print(f"cnc-server launcher output: {out.strip()}")

# Wait for it to come up
print("Waiting 8s for cnc-server to initialize...")
time.sleep(8)

# Check if running
out, _ = ssh_run(CNC_IP, CNC_PW,
    'ps aux | grep "python -m exo" | grep -v grep | head -2; echo ---; ss -tlnp | grep 42000')
print(out)

if '42000' not in out:
    print("ERROR: cnc-server not listening on port 42000!")
    sys.exit(1)
print("cnc-server UP on port 42000")

# ============================================================
# Step 3: Start kokonoe (with bootstrap to cnc-server)
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Starting kokonoe (bootstrap -> cnc-server:42000)")
print("=" * 60)

# Write startup script via tee (avoids $@ escaping issues)
script = '#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42001\nexport EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000\nexec .venv/bin/python -m exo -v\n'
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'tee', '/tmp/start-exo-kokonoe.sh'],
    input=script.encode(), capture_output=True, timeout=5
)
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'chmod', '755', '/tmp/start-exo-kokonoe.sh'],
    capture_output=True, timeout=5
)

# Launch with nohup
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'nohup /tmp/start-exo-kokonoe.sh </dev/null >/tmp/exo-stdout.log 2>&1 & echo $!'],
    capture_output=True, text=True, timeout=10
)
print(f"kokonoe launcher output: {result.stdout.strip()}")

# Wait for it to come up
print("Waiting 10s for kokonoe to initialize...")
time.sleep(10)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'ps aux | grep "python -m exo" | grep -v grep | head -2; echo ---; ss -tlnp | grep -E "42001|52415"'],
    capture_output=True, text=True, timeout=10
)
print(result.stdout)

# ============================================================
# Step 4: Check P2P connection
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Checking P2P connection (15s)...")
print("=" * 60)
time.sleep(15)

# kokonoe connection log
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'grep -E "pong|Connected|Dialing bootstrap" /tmp/exo-stdout.log | tail -15'],
    capture_output=True, text=True, timeout=10
)
print("\n--- kokonoe P2P log ---")
print(result.stdout if result.stdout.strip() else "No connection messages")

# P2P TCP connections
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'ss -tnp | grep -E "ESTAB.*(42000|42001)"'],
    capture_output=True, text=True, timeout=10
)
print("\n--- Active P2P TCP ---")
print(result.stdout if result.stdout.strip() else "No P2P connections")

# cnc-server connection log
out, _ = ssh_run(CNC_IP, CNC_PW,
    'grep -E "pong|Connected|connection" /tmp/exo-stdout.log | tail -10')
print("\n--- cnc-server P2P log ---")
print(out if out.strip() else "No connection messages")

# ============================================================
# Step 5: P2P stability monitor (90s with checks every 30s)
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: P2P stability monitor (90s)...")
print("=" * 60)

connected = False
for i in range(3):
    time.sleep(30)
    elapsed = (i + 1) * 30

    # Recent pongs
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
         'grep "pong" /tmp/exo-stdout.log | wc -l'],
        capture_output=True, text=True, timeout=10
    )
    pong_count = result.stdout.strip()

    # Disconnections
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
         'grep -cE "Disconnect|reset|error 104" /tmp/exo-stdout.log 2>/dev/null || echo 0'],
        capture_output=True, text=True, timeout=10
    )
    disconnect_count = result.stdout.strip()

    # TCP connections
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
         'ss -tnp | grep -cE "ESTAB.*(42000|42001)" 2>/dev/null || echo 0'],
        capture_output=True, text=True, timeout=10
    )
    tcp_count = result.stdout.strip()

    status = "CONNECTED" if int(pong_count or 0) > 0 and int(disconnect_count or 0) == 0 else "DISCONNECTED" if int(disconnect_count or 0) > 0 else "UNKNOWN"
    if int(pong_count or 0) > 0:
        connected = True
    print(f"  [{elapsed}s] pongs={pong_count} disconnects={disconnect_count} tcp={tcp_count} => {status}")

# ============================================================
# Final summary
# ============================================================
print("\n" + "=" * 60)
print("FINAL STATUS")
print("=" * 60)

# kokonoe recent log
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'tail -5 /tmp/exo-stdout.log'],
    capture_output=True, text=True, timeout=10
)
print("\nkokonoe recent:")
print(result.stdout)

# cnc-server recent log
out, _ = ssh_run(CNC_IP, CNC_PW, 'tail -5 /tmp/exo-stdout.log')
print("cnc-server recent:")
print(out)

# API models
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'curl -s http://localhost:52415/v1/models 2>/dev/null | python3 -m json.tool 2>/dev/null | head -20 || echo "API not available"'],
    capture_output=True, text=True, timeout=10
)
print("Models:")
print(result.stdout)

print("=" * 60)
if connected:
    print("CLUSTER CONNECTED - Ready for instance placement")
else:
    print("CLUSTER NOT CONNECTED - P2P issue persists")
print("=" * 60)
