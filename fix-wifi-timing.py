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
print("  Fix WiFi timing - add driver warmup delay")
print("=" * 60)

# Check current WiFi state
print("\n=== Current WiFi state ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "Interface: $WLAN"
echo "State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
echo "SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
echo "IP: $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}')"
"""))

# Check wpa journal for more detail
print("\n=== Full wpa-wifi boot journal ===")
print(run("journalctl -u wpa-wifi -b --no-pager 2>&1 | tail -20"))

# Check dhcpcd journal
print("\n=== Full dhcpcd-wifi boot journal ===")
print(run("journalctl -u dhcpcd-wifi -b --no-pager 2>&1 | tail -15"))

# Fix: Update wpa-wifi-start.sh to add a 5 second warmup delay after
# finding the interface, before starting wpa_supplicant.
# Also update dhcpcd to wait for wpa association before requesting DHCP.
print("\n=== Updating wpa-wifi-start.sh ===")

sftp = client.open_sftp()

wpa_start_script = '''#!/bin/bash
# WPA Supplicant starter - waits for WiFi interface dynamically
# Added 5s warmup delay to let driver fully initialize

echo "Waiting for WiFi interface..."
for i in $(seq 1 30); do
    WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\\w+' | head -1)
    if [ -n "$WLAN" ]; then
        echo "WiFi interface found: $WLAN after ${i}s"
        break
    fi
    sleep 1
done

if [ -z "$WLAN" ]; then
    echo "ERROR: No WiFi interface found after 30s"
    exit 1
fi

# Wait for driver to fully initialize (prevents EBUSY scan failures)
echo "Waiting 5s for driver warmup..."
sleep 5

ip link set "$WLAN" up
sleep 2

echo "Starting wpa_supplicant on $WLAN..."
exec /usr/sbin/wpa_supplicant -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf
'''

dhcp_start_script = '''#!/bin/bash
# DHCP client starter - waits for WPA association before requesting lease

echo "Waiting for WiFi interface..."
WLAN=""
for i in $(seq 1 30); do
    WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\\w+' | head -1)
    [ -n "$WLAN" ] && break
    sleep 1
done

if [ -z "$WLAN" ]; then
    echo "ERROR: No WiFi interface found"
    exit 1
fi

# Wait for WPA association (up to 30 seconds)
echo "Waiting for WPA association on $WLAN..."
for i in $(seq 1 30); do
    STATE=$(wpa_cli -i "$WLAN" status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)
    if [ "$STATE" = "COMPLETED" ]; then
        SSID=$(wpa_cli -i "$WLAN" status 2>/dev/null | grep '^ssid=' | cut -d= -f2)
        echo "WPA associated to $SSID after ${i}s"
        break
    fi
    sleep 1
done

if [ "$STATE" != "COMPLETED" ]; then
    echo "WARNING: WPA not completed (state=$STATE), trying DHCP anyway..."
fi

echo "Starting dhcpcd on $WLAN..."
exec /usr/sbin/dhcpcd "$WLAN"
'''

with sftp.open('/usr/local/bin/wpa-wifi-start.sh', 'w') as f:
    f.write(wpa_start_script)
print("  Written wpa-wifi-start.sh (with 5s warmup)")

with sftp.open('/usr/local/bin/dhcpcd-wifi-start.sh', 'w') as f:
    f.write(dhcp_start_script)
print("  Written dhcpcd-wifi-start.sh (waits for WPA)")

sftp.close()

print(run("chmod +x /usr/local/bin/wpa-wifi-start.sh /usr/local/bin/dhcpcd-wifi-start.sh"))

# Quick test: restart WiFi services
print("\n=== Quick test: restart WiFi services ===")
print(run(r"""
systemctl stop dhcpcd-wifi 2>/dev/null
systemctl stop wpa-wifi 2>/dev/null
sleep 2
killall dhcpcd wpa_supplicant 2>/dev/null
sleep 2

systemctl restart wpa-wifi 2>&1
""", timeout=45))

time.sleep(15)

print(run("systemctl restart dhcpcd-wifi 2>&1", timeout=45))

time.sleep(15)

print("\n=== WiFi status after restart ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "Interface: $WLAN"
echo "State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
echo "SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
echo "IP: $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)"
echo ""
for svc in rtw88-wifi wpa-wifi dhcpcd-wifi; do
    echo "  $svc: $(systemctl is-active $svc)"
done
echo ""
ping -c 2 -W 3 8.8.8.8 2>&1 | tail -3
"""))

client.close()
print("\n=== TIMING FIX APPLIED ===")
