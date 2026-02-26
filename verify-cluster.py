#!/usr/bin/env python3
"""Verify icecream cluster status and test remote compilation from kokonoe."""

import paramiko
import sys
import io
import time

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

# Check daemon connection status
run("""
echo "=== Daemon logs (latest) ==="
journalctl -u iceccd --no-pager -n 20 2>&1
echo ""

echo "=== Scheduler monitor (telnet port 8766) ==="
echo "listcs" | nc -w 2 127.0.0.1 8766 2>&1 || echo "(nc failed)"
echo ""

echo "=== All icecc processes ==="
ps aux | grep icecc | grep -v grep
echo ""

echo "=== Ports ==="
ss -tlnp | grep -E "8765|8766|10245"
ss -ulnp | grep -E "8765"
""", label="1. Cluster status")

# Test distributed compile on cnc-server itself
run("""
echo "=== Self-compile test ==="
cat > /tmp/test_remote.c << 'EOF'
#include <stdio.h>
int main() {
    printf("Hello from cnc-server cluster!\\n");
    return 0;
}
EOF

ICECC_DEBUG=1 icecc gcc -c -o /tmp/test_remote.o /tmp/test_remote.c 2>&1
echo ""

if [ -f /tmp/test_remote.o ]; then
    gcc -o /tmp/test_remote /tmp/test_remote.o
    /tmp/test_remote
    echo "PASSED"
fi
rm -f /tmp/test_remote /tmp/test_remote.o /tmp/test_remote.c
""", label="2. cnc-server compile test")

client.close()
print("\nDone!")
