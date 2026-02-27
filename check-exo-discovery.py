#!/usr/bin/env python3
"""Check exo's peer discovery mechanism and config options."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_ssh(host, password, cmd, label, timeout=60):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    try:
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host, username="root", password=password, timeout=30)
        stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        lines = result.strip().split('\n')
        for line in lines[:80]:
            print(f"  {line}")
        if len(lines) > 80:
            print(f"  ... ({len(lines) - 80} more lines)")
        c.close()
        return result, code
    except Exception as e:
        print(f"  ERROR: {e}")
        return str(e), 1

# Check exo's full help and environment vars
run_ssh("100.108.202.49", "cnc-server-2024!", """
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo

echo "=== Full exo help ==="
.venv/bin/python -m exo --help 2>&1

echo ""
echo "=== Check for peer/discovery config ==="
grep -rn 'peer\|discovery\|mdns\|mDNS\|bootstrap\|connect\|seed\|LISTEN\|listen_addr\|advertise\|EXO_' src/exo/main.py 2>&1 | head -30

echo ""
echo "=== Check networking module ==="
ls src/exo/networking/ 2>&1

echo ""
echo "=== Main.py imports and setup ==="
head -100 src/exo/main.py 2>&1

echo ""
echo "=== Discovery code ==="
grep -rn 'discovery\|mDNS\|mdns\|peer\|bootstrap' src/exo/networking/ 2>&1 | head -30

echo ""
echo "=== Environment vars used by exo ==="
grep -rn 'environ\|getenv\|EXO_' src/exo/ 2>&1 | grep -v '.pyc' | head -40

echo ""
echo "=== Config / settings ==="
ls src/exo/config* src/exo/settings* 2>&1
cat src/exo/config.py 2>&1 | head -60 || echo "no config.py"
""", "Check exo peer discovery mechanisms")
