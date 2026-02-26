#!/usr/bin/env python3
"""Full fleet status check via Tailscale IP."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Try Tailscale first, then WiFi fallback
HOSTS = [("100.108.202.49", "Tailscale"), ("10.0.0.25", "WiFi"), ("10.0.0.24", "WiFi-alt")]
client = None

for host, label in HOSTS:
    try:
        print(f"Trying {label} ({host})...")
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host, username="root", password="cnc-server-2024!", timeout=8)
        print(f"  Connected via {label}!\n")
        client = c
        break
    except Exception as e:
        print(f"  Failed: {e}")

if not client:
    print("\nERROR: Cannot reach cnc-server on any IP")
    sys.exit(1)

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

# 1. Services
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║          cnc-server Fleet Status                     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Uptime: $(uptime)"
echo "WiFi:   $(ip addr show wlp0s20u9 2>/dev/null | grep 'inet ' | awk '{print $2}' || echo 'no WiFi IP')"
echo ""
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator iceccd icecc-scheduler; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  ● %-28s active\\n" "$svc"
    else
        printf "  ○ %-28s %s\\n" "$svc" "$STATUS"
    fi
done
""", label="1. Services")

# 2. Icecream
run("""
echo "=== Icecream Scheduler Logs ==="
journalctl -u icecc-scheduler --no-pager -n 10 2>&1
echo ""
echo "=== Icecream Daemon Logs ==="
journalctl -u iceccd --no-pager -n 10 2>&1
echo ""
echo "=== icecc processes ==="
ps aux | grep -E "icecc" | grep -v grep
echo ""
echo "=== Network listeners (icecc) ==="
ss -tlnp 2>/dev/null | head -1
ss -tlnp 2>/dev/null | grep -E "icecc|8765|8766"
ss -ulnp 2>/dev/null | grep -E "icecc|8765|8766"
echo ""
echo "=== icecc config files ==="
for f in /etc/sysconfig/icecream /etc/default/icecc /etc/icecc/icecc.conf; do
    [ -f "$f" ] && echo "--- $f ---" && cat "$f" && echo ""
done
""", label="2. Icecream Cluster")

# 3. Endpoints
run("""
echo "=== Endpoints ==="
echo "Orchestrator: $(curl -s http://localhost:8080/api/health 2>&1)"
echo "AgentAPI:     HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3284 2>&1)"
echo "Ollama:       HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:11434 2>&1)"
echo ""
echo "=== Ollama models ==="
curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    for m in d.get('models',[]):
        size=m.get('size',0)/(1024**3)
        print(f'  {m[\"name\"]:40s} {size:.1f} GB')
    print(f'  Total: {len(d.get(\"models\",[]))} models')
except: print('  (error)')
" 2>&1
""", label="3. Endpoints & Ollama")

# 4. Tailscale
run("""
echo "=== Tailscale Mesh ==="
tailscale status 2>&1
echo ""
echo "=== Reachability ==="
for node in 100.90.71.97 100.93.211.48 100.77.45.99; do
    NAME=$(tailscale status 2>&1 | grep "$node" | awk '{print $2}')
    if ping -c 1 -W 2 $node &>/dev/null; then
        echo "  ✓ $NAME ($node)"
    else
        echo "  ✗ $NAME ($node) — unreachable"
    fi
done
""", label="4. Tailscale Mesh")

# 5. Compile test
run("""
echo "=== Compile test ==="
cat > /tmp/test_icecc.c << 'EOF'
#include <stdio.h>
int main() { printf("Hello from icecream!\\n"); return 0; }
EOF

if which gcc &>/dev/null; then
    COMPILER=gcc
elif which clang &>/dev/null; then
    COMPILER=clang
elif which cc &>/dev/null; then
    COMPILER=cc
else
    echo "No C compiler found — need to install gcc or clang"
    echo "Run: transactional-update pkg install gcc"
    exit 0
fi

echo "Using compiler: $COMPILER"
ICECC_DEBUG=1 icecc $COMPILER -o /tmp/test_icecc /tmp/test_icecc.c 2>&1
echo ""
if [ -f /tmp/test_icecc ]; then
    /tmp/test_icecc
    echo "✓ icecc compile PASSED"
else
    echo "✗ compile failed"
fi
rm -f /tmp/test_icecc /tmp/test_icecc.c
""", label="5. Compile Test")

client.close()
print("\nDone!")
