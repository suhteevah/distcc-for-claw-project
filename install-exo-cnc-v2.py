#!/usr/bin/env python3
"""Install exo on cnc-server - CPU-only, robust approach."""
import paramiko, sys, io, time

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
                for line in lines[:20]:
                    print(f"  {line}")
                print(f"  ... ({len(lines) - 40} lines omitted) ...")
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

# Step 0: Check prerequisites
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
echo "uv: $(uv --version 2>&1)"
echo "rustc: $(rustc --version 2>&1)"
echo "node: $(node --version 2>&1)"
echo "python3.13: $(python3.13 --version 2>&1)"
echo "disk: $(df -h /opt | tail -1)"
echo "mem: $(free -h | grep Mem)"
""", label="0. Prerequisites")

# Step 1: Clean venv and recreate
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Remove old broken venv
rm -rf .venv

# Create fresh venv with Python 3.13
uv venv --python 3.13 2>&1
echo ""
echo "venv python: $(.venv/bin/python --version)"
""", label="1. Create fresh venv")

# Step 2: Configure pip to avoid CUDA packages, install CPU-only torch
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing CPU-only PyTorch ==="
# Force CPU-only torch from the CPU wheel index
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu 2>&1

echo ""
echo "=== Verify torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, '- CUDA:', torch.cuda.is_available())" 2>&1
""", label="2. Install CPU-only PyTorch", timeout=600)

# Step 3: Install exo with uv, torch already satisfied
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing exo dependencies ==="
# Tell uv to use CPU torch backend and skip CUDA downloads
UV_TORCH_BACKEND=cpu uv sync 2>&1

echo ""
echo "=== Test exo import ==="
.venv/bin/python -c "import exo; print('exo imported successfully')" 2>&1
""", label="3. Install exo deps (uv sync)", timeout=900)

# Step 4: Test exo binary
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Testing exo --help ==="
UV_TORCH_BACKEND=cpu uv run exo --help 2>&1 | head -20
""", label="4. Test exo binary", timeout=300)

client.close()
print("\nDone!")
