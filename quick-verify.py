#!/usr/bin/env python3
"""Quick verify exo status on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Venv packages ==="
.venv/bin/pip list 2>&1 | wc -l
echo "packages installed"
echo ""

echo "=== torch ==="
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())" 2>&1

echo ""
echo "=== exo import ==="
.venv/bin/python -c "import exo; print('exo imported OK')" 2>&1

echo ""
echo "=== exo --help ==="
.venv/bin/python -m exo --help 2>&1 | head -15
""", timeout=120)
print(stdout.read().decode('utf-8', errors='replace'))
err = stderr.read().decode('utf-8', errors='replace')
if err.strip():
    print("STDERR:", err[:500])
c.close()
