#!/usr/bin/env python3
"""Quick restart and immediate model placement within the P2P window.

We know the P2P connection lasts ~4 minutes before dropping.
So we need to: restart both → wait for connection → place instance → FAST.
"""
import paramiko, subprocess, sys, io, time, json, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CNC_IP = '100.108.202.49'
CNC_PW = 'cnc-server-2024!'

def ssh_run(cmd, timeout=15):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(CNC_IP, username='root', password=CNC_PW, timeout=10)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace')
    except Exception:
        out = ""
    c.close()
    return out

def wsl_run(cmd, timeout=15):
    r = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
        capture_output=True, text=True, timeout=timeout
    )
    return r.stdout

def api_call(path, method='GET', data=None):
    url = f'http://localhost:52415{path}'
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                     headers={'Content-Type': 'application/json'},
                                     method=method)
    else:
        req = urllib.request.Request(url, method=method)
    # Route through WSL since the API is inside WSL
    cmd = f'curl -s -X {method} http://localhost:52415{path}'
    if data:
        cmd = f"curl -s -X {method} http://localhost:52415{path} -H 'Content-Type: application/json' -d '{json.dumps(data)}'"
    return wsl_run(cmd, timeout=30)

# ============================================================
# Step 1: Kill both
# ============================================================
print("STEP 1: Killing both nodes...")
wsl_run('pkill -9 -f "python.*exo" 2>/dev/null; pkill -9 -f "python.*multiprocessing" 2>/dev/null')
ssh_run('pkill -9 -f "python.*exo" 2>/dev/null')
time.sleep(3)
wsl_run('rm -f /tmp/exo-stdout.log')
ssh_run('rm -f /tmp/exo-stdout.log')
print("Both killed and logs cleared")

# ============================================================
# Step 2: Start cnc-server (anchor)
# ============================================================
print("\nSTEP 2: Starting cnc-server...")

# Upload start script
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(CNC_IP, username='root', password=CNC_PW, timeout=10)
sftp = c.open_sftp()
with sftp.open('/tmp/start-exo.sh', 'w') as f:
    f.write("#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42000\nexec .venv/bin/python -m exo -v --no-api\n")
sftp.close()
c.close()

# Launch via launcher
ssh_run('chmod +x /tmp/start-exo.sh && bash -c "nohup /tmp/start-exo.sh </dev/null >/tmp/exo-stdout.log 2>&1 &"')
time.sleep(7)

out = ssh_run('ss -tlnp | grep 42000')
if '42000' not in out:
    print("FAIL: cnc-server not listening!")
    sys.exit(1)
print("cnc-server UP on port 42000")

# ============================================================
# Step 3: Start kokonoe (with bootstrap)
# ============================================================
print("\nSTEP 3: Starting kokonoe...")
wsl_run('rm -f /tmp/exo-stdout.log')
script = '#!/bin/bash\ncd /opt/exo\nexport EXO_LIBP2P_PORT=42001\nexport EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000\nexec .venv/bin/python -m exo -v\n'
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'tee', '/tmp/start-exo-kokonoe.sh'],
    input=script.encode(), capture_output=True, timeout=5
)
subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'chmod', '755', '/tmp/start-exo-kokonoe.sh'],
    capture_output=True, timeout=5
)
wsl_run('setsid /tmp/start-exo-kokonoe.sh > /tmp/exo-stdout.log 2>&1 &')
time.sleep(10)

ports = wsl_run('ss -tlnp | grep -E "42001|52415"')
if '42001' not in ports:
    print("FAIL: kokonoe not listening!")
    sys.exit(1)
print(f"kokonoe UP: {ports.strip()}")

# ============================================================
# Step 4: Wait for P2P connection
# ============================================================
print("\nSTEP 4: Waiting for P2P connection...")
for i in range(12):
    time.sleep(5)
    pongs = wsl_run('grep -c "pong" /tmp/exo-stdout.log 2>/dev/null || echo 0').strip()
    if int(pongs) > 0:
        print(f"  P2P CONNECTED! ({pongs} pongs after {(i+1)*5}s)")
        break
    print(f"  {(i+1)*5}s - no pongs yet...")
else:
    print("FAIL: P2P never connected!")
    sys.exit(1)

# Wait a bit more for election to settle
time.sleep(5)
election = wsl_run('grep "Election queue" /tmp/exo-stdout.log | tail -1')
print(f"  Election: {election.strip()[:100]}...")

# ============================================================
# Step 5: IMMEDIATELY place instance (we have ~4 min window)
# ============================================================
print("\nSTEP 5: Placing model instance (min_nodes=2)...")
start_time = time.time()

result = api_call('/place_instance', 'POST', {
    'model_id': 'mlx-community/Qwen3-0.6B-4bit',
    'min_nodes': 2
})
print(f"  Placement response: {result[:200]}...")

# Check for the "No cycles" error
if 'error' in result.lower() or 'No cycles' in result:
    print("\n  min_nodes=2 FAILED! Trying min_nodes=1...")
    result = api_call('/place_instance', 'POST', {
        'model_id': 'mlx-community/Qwen3-0.6B-4bit',
        'min_nodes': 1
    })
    print(f"  min_nodes=1 response: {result[:200]}...")

# ============================================================
# Step 6: Monitor warmup
# ============================================================
print("\nSTEP 6: Monitoring warmup (this takes ~220s on CPU)...")
for i in range(50):
    time.sleep(10)
    elapsed = (i + 1) * 10

    # Check for runner ready
    ready = wsl_run('grep "runner ready" /tmp/exo-stdout.log 2>/dev/null').strip()
    if ready:
        print(f"\n  RUNNER READY after {elapsed}s!")
        break

    # Check warmup progress
    warmup = wsl_run('grep -c "Generated" /tmp/exo-stdout.log 2>/dev/null || echo 0').strip()
    loading = wsl_run('grep "LoadModel" /tmp/exo-stdout.log 2>/dev/null | tail -1').strip()

    # Check P2P still alive
    pongs = wsl_run('grep -c "pong" /tmp/exo-stdout.log 2>/dev/null || echo 0').strip()
    disconnects = wsl_run('grep -c "Disconnected" /tmp/exo-stdout.log 2>/dev/null || echo 0').strip()

    status = f"  [{elapsed}s] warmup_tokens={warmup} pongs={pongs} disconnects={disconnects}"
    if loading:
        status += f" loading=YES"
    print(status)

    # Check for errors
    errors = wsl_run('grep -E "Error|ERROR|No instance" /tmp/exo-stdout.log 2>/dev/null | tail -3').strip()
    if errors and 'Error in command processor' in errors:
        print(f"\n  ERROR detected: {errors[:200]}")
        break
else:
    print(f"\n  Warmup still running after 500s - checking status...")

# ============================================================
# Step 7: Test inference
# ============================================================
print("\nSTEP 7: Testing inference...")
result = api_call('/v1/chat/completions', 'POST', {
    'model': 'mlx-community/Qwen3-0.6B-4bit',
    'messages': [{'role': 'user', 'content': 'What is 2+2? Answer in one word.'}],
    'max_tokens': 100,
    'temperature': 0.1
})
print(f"  Inference result: {result[:500]}")

print("\nDONE!")
