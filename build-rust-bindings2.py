#!/usr/bin/env python3
"""Build exo_pyo3_bindings on cnc-server - fix maturin syntax."""
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

# Check maturin develop help
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
.venv/bin/python -m maturin develop --help 2>&1
""", label="1. maturin develop --help")

# Build with correct syntax - maturin 1.12+ uses --uv flag and auto-detects venv
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo/rust/exo_pyo3_bindings

echo "=== Building exo_pyo3_bindings ==="
# maturin develop builds and installs into the active venv
VIRTUAL_ENV=/opt/exo/.venv /opt/exo/.venv/bin/python -m maturin develop --release 2>&1

echo ""
echo "BUILD_EXIT: $?"
""", label="2. Build Rust bindings", timeout=900)

# Verify
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
""", label="3. Verify bindings")

client.close()
print("\nDone!")
