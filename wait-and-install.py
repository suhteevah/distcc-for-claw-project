#!/usr/bin/env python3
"""Wait for rsync to finish, then install exo from cached wheels."""
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

# Wait for rsync to finish
print("Waiting for rsync to complete...")
for i in range(60):  # max 10 minutes
    result, _ = run("pgrep rsync | wc -l")
    count = result.strip()
    cache_result, _ = run("du -sh /root/.cache/uv/ 2>&1 | cut -f1")
    cache_size = cache_result.strip()
    print(f"  [{i}] rsync procs: {count}, cache: {cache_size}")
    if count == "0":
        print("  rsync finished!")
        break
    time.sleep(10)

# Now install exo from cached wheels
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Cache size ==="
du -sh /root/.cache/uv/ 2>&1

echo ""
echo "=== Installing exo from cached wheels ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python -e . \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match \
    2>&1
echo "EXIT: $?"
""", label="Install exo", timeout=900)

# Verify
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Packages ==="
uv pip list --python .venv/bin/python 2>&1 | wc -l
echo "packages"

echo ""
echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo ==="
.venv/bin/python -c "import exo; print('exo imported OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", label="Verify", timeout=120)

client.close()
print("\nDone!")
