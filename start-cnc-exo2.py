#!/usr/bin/env python3
"""Start exo on cnc-server using a proper daemon script."""
import paramiko, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

def run(cmd, label, timeout=15):
    print(f"\n--- {label} ---")
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    result = (out + err).strip()
    for line in result.split('\n')[:40]:
        print(f"  {line}")
    return result

# Kill existing
run("pkill -f 'python.*exo' 2>/dev/null; sleep 1; echo done", "Kill old exo")

# Write a daemon script
run("""cat > /tmp/start-exo.sh << 'EOF'
#!/bin/bash
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
export EXO_LIBP2P_PORT=42000
exec .venv/bin/python -m exo -v --no-downloads --no-api > /tmp/exo-stdout.log 2>&1
EOF
chmod +x /tmp/start-exo.sh
echo "Script written"
""", "Write daemon script")

# Start via setsid (fully detached from SSH session)
run("setsid /tmp/start-exo.sh &>/dev/null & echo 'launched'", "Launch exo daemon")

# Wait for startup
print("\nWaiting 8 seconds for exo to initialize...")
time.sleep(8)

# Check
run("ps aux | grep 'python.*exo' | grep -v grep", "Check process")
run("ss -tlnp | grep -E '42000|python'", "Check listening ports")
run("cat /tmp/exo-stdout.log 2>&1 | tail -40", "Stdout log")

log_dir = run("ls /root/.cache/exo/exo_log/ 2>&1", "Log dir")
if "exo.log" in log_dir:
    run("tail -40 /root/.cache/exo/exo_log/exo.log", "Exo log")

c.close()
print("\ncnc-server exo startup complete!")
