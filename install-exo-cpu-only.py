#!/usr/bin/env python3
"""Install exo on cnc-server with CPU-only PyTorch (skip 2GB of NVIDIA downloads)."""

import paramiko
import sys
import io

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
            if len(lines) > 60:
                for line in lines[:15]:
                    print(f"  {line}")
                print(f"  ... ({len(lines) - 35} lines omitted) ...")
                for line in lines[-20:]:
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

# Strategy: Install CPU-only torch first in the venv, then let uv fill in the rest
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Create venv if it doesn't exist
if [ ! -d .venv ]; then
    uv venv --python 3.13 2>&1
fi

# Install CPU-only torch first (from PyTorch CPU index, ~200MB vs ~2GB)
echo "=== Installing CPU-only PyTorch ==="
uv pip install --python .venv/bin/python \
    torch --index-url https://download.pytorch.org/whl/cpu 2>&1

echo ""
echo "=== Verifying torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, '- CUDA:', torch.cuda.is_available())" 2>&1
""", label="1. Install CPU-only PyTorch")

# Now run uv to install everything else (torch already satisfied)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Building exo with pre-installed CPU torch ==="
UV_TORCH_BACKEND=cpu uv run --reinstall-package exo exo --help 2>&1
""", label="2. Build exo (rest of deps)")

client.close()
print("\nDone!")
