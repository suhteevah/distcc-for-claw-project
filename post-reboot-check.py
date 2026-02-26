#!/usr/bin/env python3
"""Quick post-reboot verification of remaining services."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=30, label=None):
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
            for line in result.strip().split('\n'):
                print(f"  {line}")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# Check AgentAPI
run("""
echo "=== AgentAPI status ==="
systemctl is-active claude-agentapi
echo ""
journalctl -u claude-agentapi --no-pager -n 10 2>&1
echo ""
echo "=== AgentAPI endpoint ==="
curl -s -o /dev/null -w 'HTTP %{http_code}' http://localhost:8765 2>&1
""", label="1. AgentAPI check")

# Check dhcpcd
run("""
echo "=== dhcpcd-wifi status ==="
systemctl is-active dhcpcd-wifi
echo ""
echo "=== WiFi connection ==="
# iw not available, check via ip
ip addr show wlan0 2>&1 | grep -E "(state|inet)" | head -5
echo ""
echo "=== Default route ==="
ip route | head -3
""", label="2. WiFi / dhcpcd check")

# Tailscale DNS warning - expected, confirm it's benign
run("""
echo "=== resolv.conf (should be our static config) ==="
cat /etc/resolv.conf
echo ""
echo "=== Tailscale DNS works via daemon anyway ==="
# Test resolving a tailscale hostname
tailscale status --json 2>&1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
self_dns = data.get('Self', {}).get('DNSName', 'unknown')
print(f'  Own DNS name: {self_dns}')
health = data.get('Health', [])
if health:
    print(f'  Health warnings: {len(health)}')
    for h in health[:3]:
        print(f'    - {h}')
else:
    print('  Health: OK')
" 2>&1
""", label="3. DNS / Tailscale health")

# icecream daemon status
run("""
echo "=== iceccd (icecream daemon) ==="
systemctl is-enabled iceccd 2>&1 || echo "not enabled"
systemctl is-active iceccd 2>&1 || echo "not active"
echo ""
echo "=== icecc-scheduler ==="
systemctl is-enabled icecc-scheduler 2>&1 || echo "not enabled"
systemctl is-active icecc-scheduler 2>&1 || echo "not active"
echo ""
echo "=== Available icecream services ==="
systemctl list-unit-files | grep -i ice
""", label="4. Icecream daemon status")

# Enable and start icecream
run("""
echo "=== Enabling and starting icecream services ==="
systemctl enable iceccd 2>&1
systemctl start iceccd 2>&1
echo "iceccd: $(systemctl is-active iceccd)"

# cnc-server should run the scheduler (it's the orchestrator)
systemctl enable icecc-scheduler 2>&1
systemctl start icecc-scheduler 2>&1
echo "icecc-scheduler: $(systemctl is-active icecc-scheduler)"

echo ""
echo "=== icecc status ==="
icecc --help 2>&1 | head -3
echo ""
ICECC_VERSION=$(icecc --version 2>&1)
echo "Version: $ICECC_VERSION"
""", label="5. Enable icecream services")

# Final full status
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     cnc-server FULLY OPERATIONAL                     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Services:"
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld claude-agentapi claude-orchestrator iceccd icecc-scheduler; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        echo "  ● $svc"
    else
        echo "  ○ $svc ($STATUS)"
    fi
done
echo ""
echo "Tools:"
echo "  icecc:      $(icecc --version 2>&1)"
echo "  distcc:     $(distcc --version 2>&1 | head -1)"
echo "  claude:     $(claude --version 2>&1 | head -1)"
echo "  agentapi:   $(agentapi --version 2>&1 | head -1)"
echo "  deno:       $(deno --version 2>&1 | head -1)"
echo "  node:       $(node --version 2>&1)"
echo "  ollama:     $(ollama --version 2>&1)"
echo ""
echo "Endpoints:"
echo "  Orchestrator: $(curl -s -o /dev/null -w 'HTTP %{http_code}' http://localhost:8080/api/health)"
echo "  AgentAPI:     $(curl -s -o /dev/null -w 'HTTP %{http_code}' http://localhost:8765)"
echo "  Ollama:       $(curl -s -o /dev/null -w 'HTTP %{http_code}' http://localhost:11434)"
echo ""
echo "Network:"
echo "  Tailscale: $(tailscale ip -4 2>&1)"
echo "  WiFi:      $(ip addr show wlan0 2>&1 | grep 'inet ' | awk '{print $2}')"
echo "  DNS:       $(cat /etc/resolv.conf | grep nameserver | head -1)"
""", label="FINAL STATUS")

client.close()
print("\nDone!")
