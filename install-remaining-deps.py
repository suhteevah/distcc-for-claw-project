#!/usr/bin/env python3
"""Install remaining exo dependencies on cnc-server (small packages only)."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

def run(cmd, timeout=600, label=None):
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

# Install core deps (these are all small, <10MB each)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing core deps (batch 1) ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python \
    'anyio==4.11.0' \
    'aiofiles>=24.1.0' \
    'aiohttp>=3.12.14' \
    'types-aiofiles>=24.1.0.20250708' \
    'pydantic>=2.11.7' \
    'fastapi>=0.116.1' \
    'filelock>=3.18.0' \
    'numpy' \
    2>&1
echo "EXIT1: $?"
""", label="1. Core deps batch 1")

run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing core deps (batch 2) ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python \
    'rustworkx>=0.17.1' \
    'huggingface-hub>=0.33.4' \
    'psutil>=7.0.0' \
    'loguru>=0.7.3' \
    'tiktoken>=0.12.0' \
    'hypercorn>=0.18.0' \
    'openai-harmony>=0.0.8' \
    2>&1
echo "EXIT2: $?"
""", label="2. Core deps batch 2")

run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing core deps (batch 3) ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python \
    'httpx>=0.28.1' \
    'tomlkit>=0.14.0' \
    'pillow>=11.0,<12.0' \
    'python-multipart>=0.0.21' \
    'msgspec>=0.19.0' \
    'zstandard>=0.23.0' \
    2>&1
echo "EXIT3: $?"
""", label="3. Core deps batch 3")

# Install mlx[cpu] and mflux (without pulling CUDA deps)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing mlx[cpu] ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python 'mlx[cpu]==0.30.6' 2>&1
echo "MLX_EXIT: $?"

echo ""
echo "=== Installing mlx-lm ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python 'mlx-lm==0.30.7' --no-deps 2>&1
echo "MLXLM_EXIT: $?"
""", label="4. MLX packages")

# Install mflux without letting it pull CUDA torch
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing mflux (no-deps to prevent CUDA torch) ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python 'mflux==0.15.5' --no-deps 2>&1
echo "MFLUX_EXIT: $?"

echo ""
echo "=== Installing mflux's other deps ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python \
    'safetensors' 'sentencepiece' 'transformers' 'tqdm' 'regex' \
    'tokenizers' 'protobuf' 'requests' 2>&1
echo "MFLUX_DEPS_EXIT: $?"
""", label="5. mflux + deps")

# Verify
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Package count ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l

echo ""
echo "=== Key imports ==="
.venv/bin/python -c "
import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())
try:
    import mlx.core as mx; print('mlx', mx.__version__ if hasattr(mx, '__version__') else 'OK')
except Exception as e: print('mlx:', e)
try:
    import mflux; print('mflux OK')
except Exception as e: print('mflux:', e)
import exo; print('exo OK')
" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -20
""", label="6. Final verify")

client.close()
print("\nDone!")
