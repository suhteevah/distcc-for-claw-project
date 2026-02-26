#!/usr/bin/env python3
"""Fix iceccd override to use correct binary path with -N flag."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=10)

def run(cmd, timeout=60, label=None):
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
            for line in result.strip().split('\n')[:60]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# 1. Find the actual iceccd binary/wrapper
run("""
echo "=== Wrapper script ==="
cat /usr/lib/icecc/iceccd-wrapper
echo ""
echo "=== Which iceccd ==="
which iceccd 2>&1
find / -name "iceccd" -type f 2>/dev/null | head -5
echo ""
echo "=== icecc binaries ==="
ls -la /usr/lib/icecc/ 2>/dev/null
ls -la /usr/sbin/iceccd 2>/dev/null
ls -la /usr/bin/icecc* 2>/dev/null
""", label="1. Find iceccd binary")

# 2. Fix the override to use the wrapper with added -N flag
run(r"""
cat > /etc/systemd/system/iceccd.service.d/override.conf << 'OVERRIDE'
[Service]
# Clear the original ExecStart
ExecStart=
# Use the wrapper but add -N to advertise Tailscale IP to remote nodes
ExecStart=/usr/lib/icecc/iceccd-wrapper -u icecream -vv -b /var/cache/icecream/ -N 100.108.202.49
OVERRIDE

echo "=== Override ==="
cat /etc/systemd/system/iceccd.service.d/override.conf
""", label="2. Fix override")

# 3. Restart
run("""
systemctl daemon-reload
systemctl restart iceccd
sleep 5

echo "=== Status ==="
systemctl is-active iceccd
echo ""

echo "=== Daemon logs ==="
journalctl -u iceccd --no-pager -n 15 2>&1
echo ""

echo "=== Ports ==="
ss -tlnp | grep -E "icecc|10245"
""", label="3. Restart iceccd")

client.close()
print("\nDone!")
