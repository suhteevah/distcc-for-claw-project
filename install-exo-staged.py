#!/usr/bin/env python3
"""Install exo on cnc-server - staged approach, manually control deps."""
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
                for line in lines[:30]:
                    print(f"  {line}")
                print(f"  ... ({len(lines) - 60} lines omitted) ...")
                for line in lines[-30:]:
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

# Step 1: Fresh venv + CPU torch (already done but just make sure)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Check current state
echo "torch:"
.venv/bin/python -c "import torch; print(torch.__version__)" 2>&1

echo "packages: $(uv pip list --python .venv/bin/python 2>&1 | wc -l)"
""", label="0. Current state")

# Step 2: Install mlx[cpu] explicitly (NOT mlx[cuda13])
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing mlx[cpu] ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python 'mlx[cpu]==0.30.6' 2>&1
echo "EXIT: $?"
""", label="1. Install mlx[cpu]", timeout=600)

# Step 3: Install mflux with CPU torch constraint
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing mflux (torch already satisfied) ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python 'mflux==0.15.5' 2>&1
echo "EXIT: $?"
""", label="2. Install mflux", timeout=600)

# Step 4: Install mlx-lm
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing mlx-lm ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python 'mlx-lm==0.30.7' 2>&1
echo "EXIT: $?"
""", label="3. Install mlx-lm", timeout=600)

# Step 5: Install remaining exo deps (no torch/mlx conflicts)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing other exo deps ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python \
    'aiofiles>=24.1.0' \
    'aiohttp>=3.12.14' \
    'types-aiofiles>=24.1.0.20250708' \
    'pydantic>=2.11.7' \
    'fastapi>=0.116.1' \
    'filelock>=3.18.0' \
    'rustworkx>=0.17.1' \
    'huggingface-hub>=0.33.4' \
    'psutil>=7.0.0' \
    'loguru>=0.7.3' \
    'anyio==4.11.0' \
    'tiktoken>=0.12.0' \
    'hypercorn>=0.18.0' \
    'openai-harmony>=0.0.8' \
    'httpx>=0.28.1' \
    'tomlkit>=0.14.0' \
    'pillow>=11.0,<12.0' \
    'python-multipart>=0.0.21' \
    'msgspec>=0.19.0' \
    'zstandard>=0.23.0' \
    2>&1
echo "EXIT: $?"
""", label="4. Install other deps", timeout=600)

# Step 6: Install exo itself (editable, no deps since we handled them)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing exo (editable, no deps) ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python -e . --no-deps 2>&1
echo "EXIT: $?"
""", label="5. Install exo (no deps)", timeout=600)

# Step 7: Build exo_pyo3_bindings Rust workspace member
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Building exo_pyo3_bindings ==="
uv pip install --python .venv/bin/python maturin 2>&1
cd rust/exo_pyo3_bindings
../../.venv/bin/maturin develop --release --interpreter ../../.venv/bin/python 2>&1
echo "EXIT: $?"
""", label="6. Build Rust bindings", timeout=900)

# Step 8: Verify everything
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Package count ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l

echo ""
echo "=== Key imports ==="
.venv/bin/python -c "
import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())
import mlx; print('mlx OK')
import exo; print('exo OK')
" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="7. Verify", timeout=120)

client.close()
print("\nDone!")
