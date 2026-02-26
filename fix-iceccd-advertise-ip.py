#!/usr/bin/env python3
"""Fix iceccd on cnc-server to advertise its Tailscale IP instead of 127.0.0.1."""

import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Connect via Tailscale
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

# 1. Check current iceccd service and how daemon advertises itself
run("""
echo "=== Current iceccd service ==="
cat /usr/lib/systemd/system/iceccd.service 2>&1
echo ""

echo "=== Current override (if any) ==="
cat /etc/systemd/system/iceccd.service.d/override.conf 2>/dev/null || echo "(no override)"
echo ""

echo "=== iceccd help (look for hostname/IP options) ==="
iceccd --help 2>&1 | head -30
""", label="1. Check iceccd config")

# 2. Create systemd override to make iceccd advertise Tailscale IP
run(r"""
mkdir -p /etc/systemd/system/iceccd.service.d

# Check what ExecStart the base unit uses
BASE_EXEC=$(grep "^ExecStart=" /usr/lib/systemd/system/iceccd.service)
echo "Base ExecStart: $BASE_EXEC"

# Create override that clears ExecStart and adds -N for hostname
cat > /etc/systemd/system/iceccd.service.d/override.conf << 'OVERRIDE'
[Service]
# Clear the original ExecStart
ExecStart=
# Re-add with -N to set the hostname that gets advertised to the scheduler
ExecStart=/usr/bin/iceccd -N 100.108.202.49
OVERRIDE

echo ""
echo "=== Override created ==="
cat /etc/systemd/system/iceccd.service.d/override.conf
""", label="2. Create iceccd override")

# 3. Also update the config to keep scheduler host pointing to localhost
# but allow remote connections
run(r"""
echo "=== Current icecc config ==="
grep -v "^#" /etc/sysconfig/icecream | grep -v "^$"
echo ""

# Make sure ALLOW_REMOTE is yes
sed -i 's/^ICECREAM_ALLOW_REMOTE=.*/ICECREAM_ALLOW_REMOTE="yes"/' /etc/sysconfig/icecream

echo "=== Updated config ==="
grep -v "^#" /etc/sysconfig/icecream | grep -v "^$"
""", label="3. Verify icecc config")

# 4. Restart both services
run("""
systemctl daemon-reload
systemctl restart icecc-scheduler
sleep 2
systemctl restart iceccd
sleep 5

echo "=== Scheduler status ==="
systemctl is-active icecc-scheduler

echo "=== Daemon status ==="
systemctl is-active iceccd

echo ""
echo "=== Daemon logs (check advertised IP) ==="
journalctl -u iceccd --no-pager -n 15 2>&1

echo ""
echo "=== Scheduler logs ==="
journalctl -u icecc-scheduler --no-pager -n 10 2>&1

echo ""
echo "=== Listening ports ==="
ss -tlnp | grep -E "icecc|8765|8766|10245"
ss -ulnp | grep -E "icecc|8765"
""", label="4. Restart and verify")

client.close()
print("\nDone!")
