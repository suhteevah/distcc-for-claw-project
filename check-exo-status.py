#!/usr/bin/env python3
"""Check exo install status on cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

def run(cmd, timeout=120, label=None):
    if label:
        print(f"\n--- {label} ---")
    try:
        stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = (out + err).strip()
        if result:
            print(result)
        if code != 0 and label:
            print(f"[exit code: {code}]")
        return result, code
    except Exception as e:
        print(f"ERROR: {e}")
        return str(e), 1

run("free -h | head -3", label="Memory")
run("ls -la /opt/exo/pyproject.toml /opt/exo/.venv/bin/python 2>&1", label="Exo files")
run("cd /opt/exo && .venv/bin/python -c 'import torch; print(\"torch\", torch.__version__, \"CUDA:\", torch.cuda.is_available())' 2>&1", label="PyTorch check")
run("export PATH='/root/.local/bin:/root/.cargo/bin:$PATH' && cd /opt/exo && uv run exo --help 2>&1 | head -10", label="Exo binary", timeout=300)

c.close()
print("\nDone!")
