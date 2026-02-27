#!/usr/bin/env python3
"""Apply g++ -fpermissive fix and download model on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('100.108.202.49', username='root', password='cnc-server-2024!', timeout=10)

# Step 1: Create g++ wrapper with -fpermissive
print("=== Creating g++ wrapper ===")
stdin, stdout, stderr = c.exec_command(r"""
python3 -c "
import os
wrapper = '#!/bin/bash\nexec /usr/bin/g++ -fpermissive \"\$@\"\n'
with open('/usr/local/bin/g++', 'w') as f:
    f.write(wrapper)
os.chmod('/usr/local/bin/g++', 0o755)
with open('/usr/local/bin/g++', 'r') as f:
    print('Wrapper:', repr(f.read()))
"
""", timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

# Step 2: Test wrapper
print("=== Testing g++ wrapper ===")
stdin, stdout, stderr = c.exec_command(
    '/usr/local/bin/g++ --version 2>&1 | head -1', timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))

# Step 3: Clear MLX JIT cache
print("=== Clearing MLX JIT cache ===")
stdin, stdout, stderr = c.exec_command(
    'rm -rf /tmp/mlx/ && echo "MLX cache cleared"', timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))

# Step 4: Download model if not already present
print("=== Checking/downloading model ===")
stdin, stdout, stderr = c.exec_command(r"""
cd /opt/exo
MODEL_DIR="/root/.local/share/exo/models/mlx-community--Qwen3-0.6B-4bit"
if [ -f "$MODEL_DIR/model.safetensors" ]; then
    echo "Model already downloaded"
    ls -la "$MODEL_DIR/"
else
    echo "Downloading model..."
    HF_HUB_DISABLE_PROGRESS_BARS=1 .venv/bin/python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='mlx-community/Qwen3-0.6B-4bit',
    local_dir='/root/.local/share/exo/models/mlx-community--Qwen3-0.6B-4bit',
    local_dir_use_symlinks=False
)
print('Download complete!')
"
    ls -la "$MODEL_DIR/"
fi
""", timeout=300)
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

# Step 5: Restart exo on cnc-server (without --no-downloads but still --no-api)
print("=== Restarting exo on cnc-server ===")
stdin, stdout, stderr = c.exec_command(
    'pkill -f "python.*exo" 2>&1; sleep 2; echo "Killed old process"', timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = c.exec_command(r"""
cat > /tmp/start-exo.sh << 'SCRIPT'
#!/bin/bash
cd /opt/exo
export EXO_LIBP2P_PORT=42000
exec .venv/bin/python -m exo -v --no-api
SCRIPT
chmod +x /tmp/start-exo.sh
setsid /tmp/start-exo.sh &>/tmp/exo-stdout.log &
sleep 3
ps aux | grep exo | grep -v grep
echo "---"
ss -tlnp | grep 42000
""", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

c.close()
print("\nDone!")
