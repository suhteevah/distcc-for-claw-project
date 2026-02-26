#!/usr/bin/env python3
"""Full fleet status check - cnc-server services, icecream cluster, orchestrator, Tailscale mesh."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.25", username="root", password="cnc-server-2024!", timeout=10)

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

# ═══════════════════════════════════════════════════════════════════════
# 1. All cnc-server services
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║          cnc-server Fleet Status                     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "=== Services ==="
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator iceccd icecc-scheduler; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  ● %-28s active\n" "$svc"
    else
        printf "  ○ %-28s %s\n" "$svc" "$STATUS"
    fi
done
""", label="1. cnc-server services")

# ═══════════════════════════════════════════════════════════════════════
# 2. Icecream cluster status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Icecream Scheduler ==="
journalctl -u icecc-scheduler --no-pager -n 15 2>&1
echo ""

echo "=== Icecream Daemon (iceccd) ==="
journalctl -u iceccd --no-pager -n 15 2>&1
echo ""

echo "=== icecc config ==="
cat /etc/sysconfig/icecream 2>/dev/null || echo "(no /etc/sysconfig/icecream)"
echo ""
cat /etc/icecream.conf 2>/dev/null || echo "(no /etc/icecream.conf)"
echo ""

echo "=== icecc environment ==="
echo "ICECC_VERSION: ${ICECC_VERSION:-not set}"
echo "ICECC_SCHEDULER_HOST: ${ICECC_SCHEDULER_HOST:-not set}"
icecc --version 2>&1
echo ""

echo "=== Scheduler listening? ==="
ss -tlnp | grep -E "(8765|8766|10245)" || echo "(no scheduler ports found)"
# Default scheduler port is 8765 for TCP, but also check common ones
ss -tlnp | grep icecc || echo "(no icecc-specific ports)"
ss -ulnp | grep icecc || echo "(no icecc UDP ports)"
echo ""
# Check what ports scheduler uses
ss -tlnp | grep -E "$(pgrep -f icecc-scheduler 2>/dev/null || echo NOPID)" 2>/dev/null || echo "(scheduler PID ports not found)"
ss -ulnp | grep -E "$(pgrep -f icecc-scheduler 2>/dev/null || echo NOPID)" 2>/dev/null || echo "(scheduler UDP not found)"
echo ""

echo "=== Processes ==="
ps aux | grep -E "icecc|distcc" | grep -v grep || echo "(no icecc/distcc processes)"
""", label="2. Icecream cluster")

# ═══════════════════════════════════════════════════════════════════════
# 3. Orchestrator + AgentAPI health
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Orchestrator ==="
ORCH=$(curl -s http://localhost:8080/api/health 2>&1)
echo "  Health: $ORCH"
echo ""

echo "=== AgentAPI ==="
AGENT_HTTP=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:3284 2>&1)
echo "  HTTP: $AGENT_HTTP"
echo ""

echo "=== Ollama ==="
OLLAMA=$(curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    models=d.get('models',[])
    for m in models:
        name=m.get('name','?')
        size=m.get('size',0)/(1024**3)
        print(f'    {name} ({size:.1f} GB)')
    print(f'  Total: {len(models)} models')
except:
    print('  (parse error)')
" 2>&1)
echo "$OLLAMA"
""", label="3. Orchestrator + Ollama")

# ═══════════════════════════════════════════════════════════════════════
# 4. Tailscale mesh
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Tailscale Mesh ==="
tailscale status 2>&1
echo ""

echo "=== Reachability from cnc-server ==="
for node in 100.90.71.97 100.93.211.48 100.77.45.99; do
    NAME=$(tailscale status 2>&1 | grep "$node" | awk '{print $2}')
    if ping -c 1 -W 2 $node &>/dev/null; then
        echo "  ✓ $NAME ($node) — reachable"
    else
        echo "  ✗ $NAME ($node) — unreachable"
    fi
done
""", label="4. Tailscale mesh")

# ═══════════════════════════════════════════════════════════════════════
# 5. Compile test with icecc
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Quick compile test with icecc ==="
# Create a simple test file
cat > /tmp/test_icecc.c << 'EOF'
#include <stdio.h>
int main() {
    printf("Hello from icecream!\\n");
    return 0;
}
EOF

# Try compiling with icecc
which gcc &>/dev/null && {
    echo "Compiling with icecc..."
    ICECC_DEBUG=1 icecc gcc -o /tmp/test_icecc /tmp/test_icecc.c 2>&1
    echo ""
    if [ -f /tmp/test_icecc ]; then
        echo "Binary created, running..."
        /tmp/test_icecc
        echo "✓ icecc compile test PASSED"
    else
        echo "✗ Binary not created"
    fi
} || {
    echo "gcc not installed — checking clang..."
    which clang &>/dev/null && {
        ICECC_DEBUG=1 icecc clang -o /tmp/test_icecc /tmp/test_icecc.c 2>&1
        if [ -f /tmp/test_icecc ]; then
            /tmp/test_icecc
            echo "✓ icecc compile test PASSED (clang)"
        fi
    } || echo "No C compiler installed yet (need gcc or clang via transactional-update)"
}

rm -f /tmp/test_icecc /tmp/test_icecc.c
""", label="5. icecc compile test")

client.close()
print("\nDone!")
