import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print("=== Final Reboot Test ===")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting 75 seconds...")
client.close()

time.sleep(75)
for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        def run(cmd, timeout=120):
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

# Wait for WiFi services to complete (USB wait + wpa + dhcp = ~45 sec)
print("Waiting 45 seconds for all services to settle...")
time.sleep(45)

print("\n" + "="*60)
print("  cnc-server Post-Reboot Status Report")
print("="*60)

print(run(r"""
echo ""
echo "SYSTEM"
echo "  Hostname: $(hostname)"
echo "  Kernel:   $(uname -r)"
echo "  Uptime:   $(uptime -p)"
echo ""

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
echo "  Result: $PASS passed, $FAIL failed"
echo ""

echo "NETWORK"
echo "  Ethernet:  $(ip -4 addr show enp3s0 2>/dev/null | grep inet | awk '{print $2}')"
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "  WiFi ($WLAN): $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)"
    echo "  WiFi SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
    echo "  WiFi State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
else
    echo "  WiFi: NOT AVAILABLE"
fi
echo "  Tailscale: $(tailscale ip -4 2>&1)"
echo ""

echo "CONNECTIVITY"
echo -n "  Internet (8.8.8.8): "
ping -c 1 -W 3 8.8.8.8 2>&1 | grep -oP 'time=\K[\d.]+' && echo " ms" || echo "FAIL"
echo ""

echo "TOOLS"
for cmd in node claude agentapi ollama tailscale; do
    VER=$($cmd --version 2>&1 | head -1)
    echo "  $cmd: $VER"
done
echo "  deno: $(/root/.deno/bin/deno --version 2>&1 | head -1)"
echo ""

echo "OLLAMA"
MODELS=$(curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>&1)
echo "  Models: $MODELS"
echo ""

echo "RTW88 MODULES"
lsmod | grep rtw | awk '{printf "  %-15s %s bytes\n", $1, $2}'
echo ""

echo "FIREWALL"
echo "  Trusted:  $(firewall-cmd --zone=trusted --list-interfaces 2>&1)"
echo "  Ports:    $(firewall-cmd --list-ports 2>&1)"
"""))

client.close()
print("\n=== ALL DONE ===")
