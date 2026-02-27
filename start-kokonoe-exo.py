#!/usr/bin/env python3
"""Start exo on kokonoe WSL2 with bootstrap peer to cnc-server."""
import subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_wsl(cmd, label, timeout=30):
    print(f"\n--- {label} ---")
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
        capture_output=True, text=True, timeout=timeout
    )
    out = (result.stdout + result.stderr).strip()
    for line in out.split('\n')[:60]:
        print(f"  {line}")
    if len(out.split('\n')) > 60:
        print(f"  ... (more lines)")
    return out

# Kill existing
run_wsl("pkill -f 'python.*exo' 2>/dev/null; sleep 1; echo done", "Kill old exo")

# Write daemon script
run_wsl(r"""cat > /tmp/start-exo.sh << 'EOF'
#!/bin/bash
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
export EXO_LIBP2P_PORT=42001
export EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000
exec .venv/bin/python -m exo -v > /tmp/exo-stdout.log 2>&1
EOF
chmod +x /tmp/start-exo.sh
echo "Script written"
""", "Write daemon script")

# Start
run_wsl("setsid /tmp/start-exo.sh &>/dev/null & echo 'launched'", "Launch exo daemon")

# Wait for startup and connection
print("\nWaiting 12 seconds for exo to start and connect...")
time.sleep(12)

# Check
run_wsl("ps aux | grep 'python.*exo' | grep -v grep", "Check process")
run_wsl("ss -tlnp | grep -E '42001|python'", "Check listening ports")
run_wsl("ss -tnp | grep python | head -10", "Check TCP connections")
run_wsl("tail -50 /tmp/exo-stdout.log 2>&1", "Stdout log (last 50)")
run_wsl("tail -30 /root/.cache/exo/exo_log/exo.log 2>&1", "Exo log")

print("\nkokonoe exo startup complete!")
