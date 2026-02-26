#!/usr/bin/env python3
"""Install exo on cnc-server - constrain torch to CPU-only version."""
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

# Kill any running installs
run("pkill -f 'uv pip' 2>/dev/null; sleep 2; echo 'cleaned'", label="0. Kill old installs")

# Step 1: Recreate venv + CPU torch
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Fresh venv
rm -rf .venv
uv venv --python 3.13 2>&1
echo "venv: $(.venv/bin/python --version)"

# Install CPU torch
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu 2>&1
.venv/bin/python -c "import torch; print('torch', torch.__version__)" 2>&1
""", label="1. Fresh venv + CPU torch", timeout=600)

# Step 2: Install exo and all deps, using --override to force CPU torch
# The override file tells uv to use a specific version for torch
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

# Create override to force CPU torch
cat > /tmp/overrides.txt << 'EOF'
torch==2.10.0+cpu
EOF

echo "=== Installing exo with CPU torch override ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python \
    -e . \
    --override /tmp/overrides.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match \
    2>&1
echo "EXIT: $?"
""", label="2. Install exo (override torch)", timeout=900)

# Step 3: Verify
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Packages ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l
echo "packages installed"

echo ""
echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo ==="
.venv/bin/python -c "import exo; print('exo imported OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="3. Verify", timeout=120)

client.close()
print("\nDone!")
