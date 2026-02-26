#!/usr/bin/env python3
"""Install exo on cnc-server - force CPU torch by re-locking."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

def run(cmd, timeout=900, label=None):
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        if label:
            lines = result.strip().split('\n')
            if len(lines) > 80:
                for line in lines[:25]:
                    print(f"  {line}")
                print(f"  ... ({len(lines) - 50} lines omitted) ...")
                for line in lines[-25:]:
                    print(f"  {line}")
            else:
                for line in lines:
                    print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# Step 1: Re-lock with CPU torch backend
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Re-locking with CPU torch backend ==="
UV_TORCH_BACKEND=cpu uv lock --upgrade-package torch 2>&1
echo ""
echo "=== Check what torch version is in lock file ==="
grep -A2 'name = "torch"' uv.lock 2>&1 | head -10
""", label="1. Re-lock for CPU torch")

# Step 2: Sync with CPU backend and generous timeout
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Syncing with CPU torch and 10-min timeout ==="
UV_TORCH_BACKEND=cpu UV_HTTP_TIMEOUT=600 uv sync 2>&1
""", label="2. uv sync (CPU torch)", timeout=900)

# Step 3: Verify
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo ==="
.venv/bin/python -c "import exo; print('exo imported')" 2>&1

echo ""
echo "=== exo --help ==="
UV_TORCH_BACKEND=cpu uv run exo --help 2>&1 | head -15
""", label="3. Verify install", timeout=300)

client.close()
print("\nDone!")
