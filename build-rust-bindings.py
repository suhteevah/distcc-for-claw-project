#!/usr/bin/env python3
"""Build exo_pyo3_bindings on cnc-server using maturin."""
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

# Step 1: Check Rust toolchain
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"

echo "=== Rust toolchain ==="
which rustc 2>&1 && rustc --version 2>&1
which cargo 2>&1 && cargo --version 2>&1

echo ""
echo "=== Python venv ==="
ls -la /opt/exo/.venv/bin/python 2>&1
/opt/exo/.venv/bin/python --version 2>&1

echo ""
echo "=== exo_pyo3_bindings source ==="
ls -la /opt/exo/rust/exo_pyo3_bindings/ 2>&1
cat /opt/exo/rust/exo_pyo3_bindings/Cargo.toml 2>&1

echo ""
echo "=== Workspace Cargo.toml ==="
head -30 /opt/exo/Cargo.toml 2>&1
""", label="1. Check prerequisites")

# Step 2: Install maturin
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing maturin ==="
UV_HTTP_TIMEOUT=120 uv pip install --python .venv/bin/python maturin 2>&1
echo "MATURIN_EXIT: $?"

echo ""
echo "=== Verify maturin ==="
.venv/bin/python -m maturin --version 2>&1
""", label="2. Install maturin")

# Step 3: Build the Rust bindings
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Building exo_pyo3_bindings ==="
cd rust/exo_pyo3_bindings

# Use maturin develop to build and install into the venv
/opt/exo/.venv/bin/python -m maturin develop --release \
    --interpreter /opt/exo/.venv/bin/python \
    2>&1

echo ""
echo "BUILD_EXIT: $?"
""", label="3. Build Rust bindings", timeout=900)

# Step 4: Verify
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Test import ==="
.venv/bin/python -c "
from exo_pyo3_bindings import ConnectionUpdate, ConnectionUpdateType
print('exo_pyo3_bindings OK')
print('ConnectionUpdate:', ConnectionUpdate)
print('ConnectionUpdateType:', ConnectionUpdateType)
" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -30

echo ""
echo "=== Package count ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l
""", label="4. Verify bindings")

client.close()
print("\nDone!")
