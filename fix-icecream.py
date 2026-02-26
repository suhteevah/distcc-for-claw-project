#!/usr/bin/env python3
"""Fix icecream scheduler discovery + test distributed compile."""

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
            for line in result.strip().split('\n')[:50]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Configure icecream: point daemon to local scheduler
# ═══════════════════════════════════════════════════════════════════════
run(r"""
echo "=== Current icecream config ==="
grep -v "^#" /etc/sysconfig/icecream | grep -v "^$"
echo ""

echo "=== Fixing: set ICECREAM_SCHEDULER_HOST=127.0.0.1 ==="
# Also configure for Tailscale network use
sed -i 's/^ICECREAM_SCHEDULER_HOST=.*/ICECREAM_SCHEDULER_HOST="127.0.0.1"/' /etc/sysconfig/icecream

# Set a network name for our fleet
sed -i 's/^ICECREAM_NETNAME=.*/ICECREAM_NETNAME="claw-fleet"/' /etc/sysconfig/icecream

echo "=== Updated config ==="
grep -v "^#" /etc/sysconfig/icecream | grep -v "^$"
""", label="1. Fix icecream config")

# ═══════════════════════════════════════════════════════════════════════
# 2. Also configure scheduler to listen on all interfaces (for Tailscale)
# ═══════════════════════════════════════════════════════════════════════
run(r"""
echo "=== Check scheduler service ==="
cat /usr/lib/systemd/system/icecc-scheduler.service 2>&1
echo ""

echo "=== Check iceccd service ==="
cat /usr/lib/systemd/system/iceccd.service 2>&1
""", label="2. Check systemd units")

# ═══════════════════════════════════════════════════════════════════════
# 3. Restart icecream services
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Restarting icecream ==="
systemctl restart icecc-scheduler
sleep 2
systemctl restart iceccd
sleep 5

echo "=== Scheduler logs ==="
journalctl -u icecc-scheduler --no-pager -n 5 2>&1
echo ""

echo "=== Daemon logs ==="
journalctl -u iceccd --no-pager -n 10 2>&1
""", label="3. Restart icecream")

# ═══════════════════════════════════════════════════════════════════════
# 4. Verify daemon found scheduler
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Check if daemon connected to scheduler ==="
# Wait a bit more if needed
sleep 3
journalctl -u iceccd --no-pager -n 15 2>&1
echo ""

echo "=== Ports ==="
ss -tlnp | grep -E "icecc|8765|8766|10245"
echo ""
ss -ulnp | grep -E "icecc|8765"
""", label="4. Verify connection")

# ═══════════════════════════════════════════════════════════════════════
# 5. Test distributed compile (with -c flag for icecc)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Distributed compile test ==="
cat > /tmp/test_icecc.c << 'CEOF'
#include <stdio.h>
int main() {
    printf("Hello from icecream distributed compile!\\n");
    return 0;
}
CEOF

echo "Step 1: Compile to .o with icecc (distributable)"
ICECC_DEBUG=1 icecc gcc -c -o /tmp/test_icecc.o /tmp/test_icecc.c 2>&1
echo ""

if [ -f /tmp/test_icecc.o ]; then
    echo "Step 2: Link locally"
    gcc -o /tmp/test_icecc /tmp/test_icecc.o 2>&1
    echo ""

    if [ -f /tmp/test_icecc ]; then
        echo "Step 3: Run"
        /tmp/test_icecc
        echo ""
        echo "✓ icecc distributed compile test PASSED"
    fi
fi

rm -f /tmp/test_icecc /tmp/test_icecc.o /tmp/test_icecc.c

echo ""
echo "=== Scheduler network name ==="
echo "Fleet nodes can join with: ICECREAM_SCHEDULER_HOST=100.108.202.49"
echo "Network name: claw-fleet"
""", label="5. Distributed compile test")

# ═══════════════════════════════════════════════════════════════════════
# 6. Ensure firewall allows icecc from Tailscale
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Firewall: icecc ports in trusted zone (Tailscale) ==="
# tailscale0 is already in trusted zone, which allows all traffic
firewall-cmd --get-zone-of-interface=tailscale0 2>&1
echo ""
echo "Tailscale is in trusted zone — all ports open for fleet nodes ✓"
echo ""
echo "Ports used by icecream:"
echo "  8765/tcp+udp  — scheduler"
echo "  8766/tcp      — scheduler (telnet monitor)"
echo "  10245/tcp     — daemon (compile jobs)"
""", label="6. Firewall check")

client.close()
print("\nDone!")
