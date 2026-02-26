import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print("=" * 60)
print("  DEFINITIVE REBOOT TEST")
print("  SELinux permissive + standalone scripts")
print("=" * 60)

# Reboot
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting 75 seconds...")
client.close()

time.sleep(75)
for attempt in range(20):
    time.sleep(10)
    print(f"  Reconnect attempt {attempt+1}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        def run(cmd, timeout=30):
            stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err
        print("  CONNECTED!")
        break
    except:
        pass
else:
    print("Failed to reconnect!")
    exit(1)

# Wait for all WiFi services to complete
# USB wait (30s) + module load (5s) + wpa wait (30s) + dhcp (15s) = ~80s
print("Waiting 90 seconds for WiFi services to complete...")
time.sleep(90)

print("\n" + "=" * 60)
print("  cnc-server Post-Reboot Status Report")
print("=" * 60)

# System info
print(run(r"""
echo ""
echo "SYSTEM"
echo "  Hostname: $(hostname)"
echo "  Kernel:   $(uname -r)"
echo "  Uptime:   $(cat /proc/uptime | awk '{printf "%.0f seconds", $1}')"
echo "  SELinux:  $(getenforce)"
"""))

# Services
print(run(r"""
echo "SERVICES"
PASS=0
FAIL=0
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        echo "  [OK] $svc"
        PASS=$((PASS+1))
    else
        echo "  [!!] $svc: $STATUS"
        FAIL=$((FAIL+1))
    fi
done
echo "  Score: $PASS/6 passed"
"""))

# Modules
print(run(r"""
echo ""
echo "RTW88 MODULES"
MODCOUNT=$(lsmod | grep -c rtw)
lsmod | grep rtw | awk '{printf "  %-15s %s bytes\n", $1, $2}'
echo "  Total: $MODCOUNT modules"
"""))

# Network
print(run(r"""
echo ""
echo "NETWORK"
echo "  Ethernet:  $(ip -4 addr show enp3s0 2>/dev/null | grep 'inet ' | awk '{print $2}')"
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "  WiFi ($WLAN):"
    echo "    IP:    $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)"
    echo "    SSID:  $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
    echo "    State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
    echo "    BSSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^bssid=' | cut -d= -f2)"
else
    echo "  WiFi: NOT AVAILABLE"
fi
echo "  Tailscale: $(tailscale ip -4 2>&1)"
"""))

# Connectivity
print(run(r"""
echo ""
echo "CONNECTIVITY"
echo -n "  Internet (8.8.8.8): "
PING=$(ping -c 1 -W 3 8.8.8.8 2>&1 | grep -oP 'time=[\d.]+')
[ -n "$PING" ] && echo "$PING ms" || echo "FAIL"
echo -n "  DNS (google.com):   "
PING2=$(ping -c 1 -W 3 google.com 2>&1 | grep -oP 'time=[\d.]+')
[ -n "$PING2" ] && echo "$PING2 ms" || echo "FAIL"
echo -n "  Tailscale self:     "
PING3=$(ping -c 1 -W 3 100.108.202.49 2>&1 | grep -oP 'time=[\d.]+')
[ -n "$PING3" ] && echo "$PING3 ms" || echo "FAIL"
"""))

# Tools
print(run(r"""
echo ""
echo "TOOLS"
for cmd in node claude agentapi ollama tailscale; do
    VER=$($cmd --version 2>&1 | head -1)
    echo "  $cmd: $VER"
done
echo "  deno: $(/root/.deno/bin/deno --version 2>&1 | head -1)"
"""))

# Ollama
print(run(r"""
echo ""
echo "OLLAMA"
MODELS=$(curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>&1)
echo "  Models: $MODELS"
"""))

# Firewall
print(run(r"""
echo ""
echo "FIREWALL"
echo "  Trusted:  $(firewall-cmd --zone=trusted --list-interfaces 2>&1)"
echo "  Ports:    $(firewall-cmd --list-ports 2>&1)"
"""))

# Service journals (key lines only)
print(run(r"""
echo ""
echo "SERVICE BOOT LOGS"
echo "  rtw88-wifi:"
journalctl -u rtw88-wifi -b --no-pager 2>&1 | grep -E 'found|loaded|SUCCESS|ERROR|FAIL|Finished' | head -3
echo "  wpa-wifi:"
journalctl -u wpa-wifi -b --no-pager 2>&1 | grep -E 'found|Starting|connected|FAIL' | head -3
echo "  dhcpcd-wifi:"
journalctl -u dhcpcd-wifi -b --no-pager 2>&1 | grep -E 'leased|bound|offered|FAIL|Starting' | head -3
"""))

# Verdict
print(run(r"""
echo ""
echo "============================================"
# Count passing services
PASS=0
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld; do
    [ "$(systemctl is-active $svc)" = "active" ] && PASS=$((PASS+1))
done
MODCOUNT=$(lsmod | grep -c rtw)
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
WIFI_IP=$(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)
INET=$(ping -c 1 -W 3 8.8.8.8 2>&1 | grep -c '1 received')

if [ "$PASS" -eq 6 ] && [ "$MODCOUNT" -gt 0 ] && [ -n "$WIFI_IP" ] && [ "$INET" -eq 1 ]; then
    echo "  VERDICT: ALL SYSTEMS GO"
else
    echo "  VERDICT: ISSUES DETECTED"
    [ "$PASS" -lt 6 ] && echo "    - Services: $PASS/6"
    [ "$MODCOUNT" -eq 0 ] && echo "    - No WiFi modules loaded"
    [ -z "$WIFI_IP" ] && echo "    - No WiFi IP"
    [ "$INET" -ne 1 ] && echo "    - No internet connectivity"
fi
echo "============================================"
"""))

client.close()
print("\n=== REBOOT TEST COMPLETE ===")
