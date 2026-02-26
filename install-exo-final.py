#!/usr/bin/env python3
"""Install exo on cnc-server - final attempt with proper pip + index strategy."""
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

# Check what we have
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
echo "=== Current venv packages ==="
uv pip list --python .venv/bin/python 2>&1
""", label="0. Current state")

# Install exo with correct flags
result, code = run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Installing exo with all deps ==="
UV_HTTP_TIMEOUT=600 uv pip install --python .venv/bin/python \
    -e ".[all]" \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match \
    2>&1
echo "EXIT: $?"
""", label="1. Install exo + deps", timeout=900)

if "EXIT: 0" in result:
    # Verify
    run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Package count ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l

echo ""
echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo import ==="
.venv/bin/python -c "import exo; print('exo imported OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="2. Verify", timeout=120)
else:
    print("\n  Install failed - checking what went wrong...")

client.close()
print("\nDone!")
