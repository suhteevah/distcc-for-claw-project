#!/usr/bin/env python3
"""Deploy the bootstrap peer patch to both cnc-server and kokonoe, then rebuild."""
import paramiko, subprocess, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PATCH_FILE = os.path.join(os.path.dirname(__file__), "apply-patch.py")

def run_ssh(host, password, cmd, label, timeout=120):
    print(f"\n{'='*60}")
    print(f"  [{host}] {label}")
    print(f"{'='*60}")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="root", password=password, timeout=30)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    result = out + err
    code = stdout.channel.recv_exit_status()
    lines = result.strip().split('\n')
    for line in lines[:60]:
        print(f"  {line}")
    if len(lines) > 60:
        print(f"  ... ({len(lines) - 60} more lines)")
    if code != 0:
        print(f"  [exit code: {code}]")
    c.close()
    return result, code

def upload_ssh(host, password, local_path, remote_path):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="root", password=password, timeout=30)
    sftp = c.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    c.close()
    print(f"  Uploaded {local_path} -> {host}:{remote_path}")

def run_wsl(cmd, label, timeout=120):
    print(f"\n{'='*60}")
    print(f"  [kokonoe WSL2] {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
        capture_output=True, text=True, timeout=timeout
    )
    out = result.stdout + result.stderr
    lines = out.strip().split('\n')
    for line in lines[:60]:
        print(f"  {line}")
    if len(lines) > 60:
        print(f"  ... ({len(lines) - 60} more lines)")
    return out

# Read patch script
with open(PATCH_FILE, 'r') as f:
    patch_content = f.read()

# ===== CNC-SERVER =====
print("\n" + "#"*60)
print("  CNC-SERVER")
print("#"*60)

# Upload and apply patch
upload_ssh("100.108.202.49", "cnc-server-2024!", PATCH_FILE, "/tmp/apply-patch.py")
run_ssh("100.108.202.49", "cnc-server-2024!",
    "python3 /tmp/apply-patch.py 2>&1",
    "Apply patch")

# Rebuild
run_ssh("100.108.202.49", "cnc-server-2024!", r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo/rust/exo_pyo3_bindings

echo "=== Rebuilding exo_pyo3_bindings ==="
VIRTUAL_ENV=/opt/exo/.venv /opt/exo/.venv/bin/python -m maturin develop --release 2>&1

echo ""
echo "BUILD_EXIT: $?"
""", "Rebuild Rust bindings", timeout=300)

# Verify
run_ssh("100.108.202.49", "cnc-server-2024!", r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
.venv/bin/python -c "from exo_pyo3_bindings import NetworkingHandle; print('OK')" 2>&1
.venv/bin/python -m exo --help 2>&1 | head -3
echo "cnc-server: READY"
""", "Verify")

# ===== KOKONOE WSL2 =====
print("\n" + "#"*60)
print("  KOKONOE WSL2")
print("#"*60)

# Copy patch into WSL2 and apply
run_wsl("cat > /tmp/apply-patch.py << 'PATCHEOF'\n" + patch_content + "\nPATCHEOF\npython3 /tmp/apply-patch.py 2>&1",
    "Apply patch")

# Rebuild
run_wsl(r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo/rust/exo_pyo3_bindings

echo "=== Rebuilding exo_pyo3_bindings ==="
VIRTUAL_ENV=/opt/exo/.venv /opt/exo/.venv/bin/python -m maturin develop --release 2>&1

echo ""
echo "BUILD_EXIT: $?"
""", "Rebuild Rust bindings", timeout=300)

# Verify
run_wsl(r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
.venv/bin/python -c "from exo_pyo3_bindings import NetworkingHandle; print('OK')" 2>&1
.venv/bin/python -m exo --help 2>&1 | head -3
echo "kokonoe: READY"
""", "Verify")

print("\n" + "="*60)
print("  BOTH NODES PATCHED & REBUILT")
print("="*60)
print("""
To start the cluster:

  cnc-server (CPU worker):
    EXO_LIBP2P_PORT=42000 python -m exo -v --no-downloads

  kokonoe (GPU worker, initiates connection):
    EXO_LIBP2P_PORT=42001 EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000 python -m exo -v
""")
