#!/usr/bin/env python3
"""Check exo status on both nodes and prepare for cluster connection."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_ssh(host, password, cmd, label, timeout=60):
    print(f"\n{'='*60}")
    print(f"  [{host}] {label}")
    print(f"{'='*60}")
    try:
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host, username="root", password=password, timeout=30)
        stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        lines = result.strip().split('\n')
        for line in lines[:50]:
            print(f"  {line}")
        if len(lines) > 50:
            print(f"  ... ({len(lines) - 50} more lines)")
        if code != 0:
            print(f"  [exit code: {code}]")
        c.close()
        return result, code
    except Exception as e:
        print(f"  ERROR: {e}")
        return str(e), 1

def run_wsl(cmd, label, timeout=60):
    print(f"\n{'='*60}")
    print(f"  [kokonoe WSL2] {label}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
            capture_output=True, text=True, timeout=timeout
        )
        out = result.stdout + result.stderr
        lines = out.strip().split('\n')
        for line in lines[:50]:
            print(f"  {line}")
        if len(lines) > 50:
            print(f"  ... ({len(lines) - 50} more lines)")
        return out, result.returncode
    except Exception as e:
        print(f"  ERROR: {e}")
        return str(e), 1

# === Check kokonoe (local WSL2) ===
run_wsl("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== exo version ==="
.venv/bin/python -c "import exo; print('exo OK')" 2>&1

echo ""
echo "=== torch/CUDA ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available(), 'GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')" 2>&1

echo ""
echo "=== exo_pyo3_bindings ==="
.venv/bin/python -c "from exo_pyo3_bindings import ConnectionUpdate; print('bindings OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -20

echo ""
echo "=== exo already running? ==="
ps aux | grep -E 'exo' | grep -v grep

echo ""
echo "=== Network (Tailscale) ==="
ip addr show tailscale0 2>&1 | grep inet
hostname -I 2>&1
""", "Check exo readiness")

# === Check cnc-server ===
run_ssh("100.108.202.49", "cnc-server-2024!", """
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== exo version ==="
.venv/bin/python -c "import exo; print('exo OK')" 2>&1

echo ""
echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo_pyo3_bindings ==="
.venv/bin/python -c "from exo_pyo3_bindings import ConnectionUpdate; print('bindings OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -20

echo ""
echo "=== exo already running? ==="
ps aux | grep -E 'exo' | grep -v grep

echo ""
echo "=== Network (Tailscale) ==="
ip addr show tailscale0 2>&1 | grep inet
hostname -I 2>&1

echo ""
echo "=== Memory ==="
free -h 2>&1

echo ""
echo "=== mDNS/avahi ==="
which avahi-browse 2>&1
systemctl is-active avahi-daemon 2>&1
""", "Check exo readiness")

print("\n" + "="*60)
print("  SUMMARY")
print("="*60)
print("Both nodes need exo running simultaneously for mDNS auto-discovery.")
print("exo uses libp2p with mDNS to find peers on the same network.")
print("Tailscale provides the network layer (same virtual subnet).")
