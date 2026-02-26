#!/usr/bin/env python3
"""Fix iceccd on cnc-server to connect to scheduler via Tailscale IP."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server via Tailscale")

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

# 1. Change scheduler host from 127.0.0.1 to Tailscale IP
run(r"""
sed -i 's/^ICECREAM_SCHEDULER_HOST=.*/ICECREAM_SCHEDULER_HOST="100.108.202.49"/' /etc/sysconfig/icecream
echo "=== Updated config ==="
grep -v "^#" /etc/sysconfig/icecream | grep -v "^$"
""", label="1. Fix scheduler host to Tailscale IP")

# 2. Restart both services
run("""
systemctl restart icecc-scheduler
sleep 2
systemctl restart iceccd
sleep 8

echo "=== Daemon logs ==="
journalctl -u iceccd --no-pager -n 10 2>&1
echo ""

echo "=== Scheduler monitor ==="
echo "listcs" | nc -w 2 127.0.0.1 8766 2>&1
""", label="2. Restart and check")

# 3. Compile test to verify remote routing
run("""
cat > /tmp/test_route.c << 'EOF'
#include <stdio.h>
int main() {
    printf("Routing test OK\\n");
    return 0;
}
EOF

ICECC_DEBUG=1 icecc gcc -c -o /tmp/test_route.o /tmp/test_route.c 2>&1
echo ""
if [ -f /tmp/test_route.o ]; then
    gcc -o /tmp/test_route /tmp/test_route.o
    /tmp/test_route
fi
rm -f /tmp/test_route /tmp/test_route.o /tmp/test_route.c
""", label="3. Compile test (check routing)")

client.close()
print("\nDone!")
