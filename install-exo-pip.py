#!/usr/bin/env python3
"""Install exo on cnc-server using uv pip install (bypasses lockfile).
This avoids the lockfile which forces CUDA torch downloads."""
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
            if len(lines) > 100:
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

# Step 0: Kill any existing uv sync
run("""
pkill -f 'uv sync' 2>/dev/null
sleep 2
echo "Killed old uv sync"
""", label="0. Kill old process")

# Step 1: Recreate venv with CPU torch already installed
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
rm -rf .venv
uv venv --python 3.13 2>&1
echo "venv: $(.venv/bin/python --version)"
echo ""
echo "=== Installing CPU-only PyTorch ==="
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu 2>&1
echo ""
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())"
""", label="1. Fresh venv + CPU torch", timeout=600)

# Step 2: Install exo editable with CPU torch index override
# Using uv pip install -e . which doesn't use the lockfile
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing exo + deps (CPU torch index) ==="
# Install editable with CPU torch already present, use CPU index as extra
UV_HTTP_TIMEOUT=600 uv pip install --python .venv/bin/python -e ".[all]" \
    --extra-index-url https://download.pytorch.org/whl/cpu 2>&1
""", label="2. Install exo (pip, no lockfile)", timeout=900)

# Step 3: Build Rust bindings if needed
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Check if exo_pyo3 needs building ==="
.venv/bin/python -c "import exo; print('exo imports ok')" 2>&1
if [ $? -ne 0 ]; then
    echo "Trying maturin build..."
    cd rust/exo_pyo3_bindings
    ../../.venv/bin/pip install maturin 2>&1 | tail -3
    maturin develop --release 2>&1 | tail -10
fi
""", label="3. Build Rust bindings", timeout=600)

# Step 4: Test
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo ==="
.venv/bin/python -c "import exo; print('exo imported ok')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="4. Verify", timeout=120)

client.close()
print("\nDone!")
