#!/usr/bin/env python3
"""Transfer uv cache/wheels from kokonoe to cnc-server via Tailscale.
Kokonoe already has all exo deps downloaded. Copy them over."""
import paramiko, sys, io, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# First, kill any existing uv installs on cnc-server
cnc = paramiko.SSHClient()
cnc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cnc.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

stdin, stdout, stderr = cnc.exec_command("pkill -f 'uv pip' 2>/dev/null; echo 'killed uv'", timeout=10)
print(stdout.read().decode('utf-8', errors='replace').strip())

# Set up SSH access from kokonoe WSL2 to cnc-server using sshpass
# Then rsync the uv cache
print("\n=== Transferring uv cache from kokonoe to cnc-server ===")
print("This uses Tailscale (100.90.71.97 -> 100.108.202.49)")

# Run from kokonoe WSL2 to rsync the cache
result = subprocess.run([
    'wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
    """
# Install sshpass if not present
which sshpass >/dev/null 2>&1 || apt-get install -y -qq sshpass 2>&1 | tail -1

echo "=== Source cache size ==="
du -sh /root/.cache/uv/ 2>&1

echo ""
echo "=== Syncing uv cache to cnc-server ==="
# Use rsync over ssh with password
sshpass -p 'cnc-server-2024!' rsync -avz --progress \
    /root/.cache/uv/ \
    root@100.108.202.49:/root/.cache/uv/ \
    -e 'ssh -o StrictHostKeyChecking=no' \
    2>&1 | tail -30

echo ""
echo "=== Done ==="
"""
], capture_output=True, text=True, timeout=1800)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])

# Now try the install again on cnc-server with the cached wheels
print("\n=== Now installing exo from cached wheels ===")
stdin, stdout, stderr = cnc.exec_command("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Cache size ==="
du -sh /root/.cache/uv/ 2>&1

echo ""
echo "=== Installing exo (wheels should be cached) ==="
UV_HTTP_TIMEOUT=300 uv pip install --python .venv/bin/python -e . \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match \
    2>&1

echo ""
echo "=== Verify ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1
.venv/bin/python -c "import exo; print('exo imported OK')" 2>&1
.venv/bin/python -m exo --help 2>&1 | head -10
""", timeout=900)
print(stdout.read().decode('utf-8', errors='replace'))

cnc.close()
print("\nDone!")
