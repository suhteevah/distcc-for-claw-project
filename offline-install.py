#!/usr/bin/env python3
"""Offline exo install: download all wheels on kokonoe, transfer to cnc-server, install locally."""
import subprocess, paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("  PHASE 1: Download wheels on kokonoe (fast network)")
print("=" * 60)

# Step 1: On kokonoe WSL2, download all exo deps as wheels to a directory
result = subprocess.run([
    'wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
    """
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Clean download dir
rm -rf /tmp/exo-wheels
mkdir -p /tmp/exo-wheels

# Get the list of installed packages (these are the correct resolved deps)
echo "=== Exporting package list ==="
.venv/bin/python -m pip freeze 2>&1 | grep -v '^-e ' > /tmp/exo-wheels/requirements.txt
cat /tmp/exo-wheels/requirements.txt | wc -l
echo "packages exported"

# Download wheels for all packages
echo ""
echo "=== Downloading wheels ==="
uv pip download -p 3.13 --platform manylinux_2_28_x86_64 --python-platform linux \
    -r /tmp/exo-wheels/requirements.txt \
    -d /tmp/exo-wheels/ \
    2>&1 | tail -20

# Also get the CPU torch wheel specifically
echo ""
echo "=== Downloading CPU torch ==="
uv pip download -p 3.13 --platform manylinux_2_28_x86_64 --python-platform linux \
    torch --index-url https://download.pytorch.org/whl/cpu \
    -d /tmp/exo-wheels/ \
    2>&1 | tail -5

echo ""
echo "=== Wheels directory ==="
ls /tmp/exo-wheels/*.whl 2>&1 | wc -l
echo "wheel files"
du -sh /tmp/exo-wheels/

echo ""
echo "=== Requirements (first 20) ==="
head -20 /tmp/exo-wheels/requirements.txt
"""
], capture_output=True, text=True, timeout=600)
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr[:1000])

print("\n" + "=" * 60)
print("  PHASE 2: Transfer wheels to cnc-server via Tailscale")
print("=" * 60)

# Kill old uv processes on cnc-server
cnc = paramiko.SSHClient()
cnc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cnc.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

stdin, stdout, stderr = cnc.exec_command("pkill -f 'uv pip' 2>/dev/null; mkdir -p /tmp/exo-wheels; echo 'ready'", timeout=10)
print(stdout.read().decode('utf-8', errors='replace').strip())
cnc.close()

# rsync wheels from kokonoe to cnc-server
print("\n=== rsyncing wheels ===")
result = subprocess.run([
    'wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
    """
which sshpass >/dev/null 2>&1 || apt-get install -y -qq sshpass 2>&1 | tail -1

echo "Transferring wheels to cnc-server..."
sshpass -p 'cnc-server-2024!' rsync -avz --progress \
    /tmp/exo-wheels/ \
    root@100.108.202.49:/tmp/exo-wheels/ \
    -e 'ssh -o StrictHostKeyChecking=no' \
    2>&1 | tail -10

echo ""
echo "=== Transfer complete ==="
"""
], capture_output=True, text=True, timeout=600)
print(result.stdout)

print("\n" + "=" * 60)
print("  PHASE 3: Install from local wheels on cnc-server")
print("=" * 60)

cnc = paramiko.SSHClient()
cnc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cnc.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

def run(cmd, timeout=900, label=None):
    if label:
        print(f"\n--- {label} ---")
    try:
        stdin, stdout, stderr = cnc.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        lines = result.strip().split('\n')
        if len(lines) > 60:
            for line in lines[:15]:
                print(f"  {line}")
            print(f"  ... ({len(lines) - 30} lines omitted) ...")
            for line in lines[-15:]:
                print(f"  {line}")
        else:
            for line in lines:
                print(f"  {line}")
        if code != 0 and label:
            print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        print(f"  ERROR: {e}")
        return str(e), 1

# Check what we received
run("""
echo "Wheels received:"
ls /tmp/exo-wheels/*.whl 2>&1 | wc -l
echo "files"
du -sh /tmp/exo-wheels/
""", label="Check received wheels")

# Install from local wheels (no internet needed!)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Fresh venv
rm -rf .venv
uv venv --python 3.13 2>&1

# Install CPU torch from local wheel first
echo "=== Installing CPU torch from local wheel ==="
uv pip install --python .venv/bin/python \
    --find-links /tmp/exo-wheels/ \
    --no-index \
    torch 2>&1 || \
uv pip install --python .venv/bin/python \
    torch --index-url https://download.pytorch.org/whl/cpu 2>&1

.venv/bin/python -c "import torch; print('torch', torch.__version__)" 2>&1
""", label="Install CPU torch from local")

# Install all other deps from local wheels
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing deps from local wheels ==="
# Filter out torch and CUDA/NVIDIA packages from requirements
grep -v -iE 'torch|nvidia|cuda|triton' /tmp/exo-wheels/requirements.txt > /tmp/exo-wheels/reqs-filtered.txt
echo "Filtered packages:"
wc -l /tmp/exo-wheels/reqs-filtered.txt

uv pip install --python .venv/bin/python \
    --find-links /tmp/exo-wheels/ \
    -r /tmp/exo-wheels/reqs-filtered.txt \
    2>&1

echo "EXIT: $?"
""", label="Install other deps from local wheels", timeout=600)

# Install exo itself editable
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing exo editable ==="
uv pip install --python .venv/bin/python -e . --no-deps 2>&1
echo "EXIT: $?"
""", label="Install exo editable", timeout=300)

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
    import mlx.core; print('mlx OK')
except: print('mlx FAILED (expected on CPU-only)')
import exo; print('exo OK')
" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="Verify")

cnc.close()
print("\nDone!")
