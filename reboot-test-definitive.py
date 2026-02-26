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

# Reboot
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting 75s...")
client.close()

time.sleep(75)
for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}...")
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

# Wait for everything to settle (modules + 5s warmup + wpa + dhcp wait)
print("Waiting 120 seconds for all services to fully settle...")
time.sleep(120)

print("\n" + "=" * 60)
print("  cnc-server DEFINITIVE Post-Reboot Report")
print("=" * 60)

report = run(r"""
echo ""
echo "SYSTEM"
echo "  Hostname: $(hostname)"
echo "  Kernel:   $(uname -r)"
echo "  Uptime:   $(cat /proc/uptime | awk '{printf "%.0f seconds", $1}')"
echo "  SELinux:  $(getenforce)"
echo ""

echo "SERVICES                                   STATUS"
echo "  -------                                   ------"
PASS=0
FAIL=0
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld; do
    STATUS=$(systemctl is-active $svc 2>&1)
    if [ "$STATUS" = "active" ]; then
        printf "  %-40s [OK]\n" "$svc"
        PASS=$((PASS+1))
    else
        printf "  %-40s [FAIL: %s]\n" "$svc" "$STATUS"
        FAIL=$((FAIL+1))
    fi
done
echo "  Score: $PASS/6"
echo ""

echo "RTW88 MODULES"
MODCOUNT=$(lsmod | grep -c rtw 2>/dev/null || echo 0)
lsmod | grep rtw | awk '{printf "  %-20s %6d bytes  refs=%s\n", $1, $2, $3}'
echo "  Total: $MODCOUNT modules"
echo ""

echo "NETWORK"
echo "  Ethernet (enp3s0): $(ip -4 addr show enp3s0 2>/dev/null | grep 'inet ' | awk '{print $2}')"
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    WSTATE=$(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)
    WSSID=$(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)
    WIP=$(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)
    echo "  WiFi ($WLAN):       $WIP"
    echo "    SSID:  $WSSID"
    echo "    State: $WSTATE"
else
    echo "  WiFi: NOT AVAILABLE"
fi
echo "  Tailscale:         $(tailscale ip -4 2>&1)"
echo ""

echo "CONNECTIVITY"
echo -n "  Ping 8.8.8.8:      "
PING=$(ping -c 1 -W 3 8.8.8.8 2>&1 | grep -oP 'time=[\d.]+')
[ -n "$PING" ] && echo "${PING} ms" || echo "FAIL"
echo -n "  DNS google.com:    "
PING2=$(ping -c 1 -W 3 google.com 2>&1 | grep -oP 'time=[\d.]+')
[ -n "$PING2" ] && echo "${PING2} ms" || echo "FAIL"
echo ""

echo "TOOLS"
echo "  node:      $(node --version 2>&1)"
echo "  claude:    $(claude --version 2>&1 | head -1)"
echo "  agentapi:  $(agentapi --version 2>&1)"
echo "  ollama:    $(ollama --version 2>&1)"
echo "  tailscale: $(tailscale --version 2>&1 | head -1)"
echo "  deno:      $(/root/.deno/bin/deno --version 2>&1 | head -1)"
echo ""

echo "OLLAMA MODELS"
MODELS=$(curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>&1)
echo "  $MODELS"
echo ""

echo "FIREWALL"
echo "  Trusted zone: $(firewall-cmd --zone=trusted --list-interfaces 2>&1)"
echo "  Open ports:   $(firewall-cmd --list-ports 2>&1)"
echo ""

# Final verdict
PASS=0
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld; do
    [ "$(systemctl is-active $svc)" = "active" ] && PASS=$((PASS+1))
done
MODCOUNT=$(lsmod | grep -c rtw 2>/dev/null || echo 0)
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
WIFI_IP=$(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)
INET=$(ping -c 1 -W 3 8.8.8.8 2>&1 | grep -c '1 received')
WSTATE=$(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)

echo "============================================"
if [ "$PASS" -eq 6 ] && [ "$MODCOUNT" -gt 0 ] && [ -n "$WIFI_IP" ] && [ "$INET" -eq 1 ] && [ "$WSTATE" = "COMPLETED" ]; then
    echo "  VERDICT: ALL SYSTEMS GO !!!"
    echo "  6/6 services | $MODCOUNT modules | WiFi: $WIFI_IP | Internet: OK"
else
    echo "  VERDICT: PARTIAL"
    echo "  Services: $PASS/6 | Modules: $MODCOUNT | WiFi IP: ${WIFI_IP:-none} | WPA: ${WSTATE:-unknown}"
    [ "$INET" -ne 1 ] && echo "  Internet: FAIL"
fi
echo "============================================"
""")

print(report)

client.close()
print("\n=== DEFINITIVE REBOOT TEST COMPLETE ===")
