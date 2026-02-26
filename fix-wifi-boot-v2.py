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

print("=" * 60)
print("  Fix WiFi Boot - Use Standalone Scripts")
print("  Root cause: systemd expands ${mod} before bash sees it")
print("  Fix: move all logic to standalone .sh scripts")
print("=" * 60)

# First, unload the modules we just manually loaded (from diagnostic)
print("\n=== Unload manually-loaded modules ===")
print(run(r"""
systemctl stop wpa-wifi 2>/dev/null
systemctl stop dhcpcd-wifi 2>/dev/null
killall wpa_supplicant 2>/dev/null
killall dhcpcd 2>/dev/null
sleep 2
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
echo "Modules cleared"
lsmod | grep rtw || echo "No rtw modules - clean"
"""))

# Write the WiFi start script
print("\n=== Creating /usr/local/bin/rtw88-wifi-start.sh ===")

# Use SFTP to write files to avoid all quoting issues
sftp = client.open_sftp()

start_script = '''#!/bin/bash
# RTW88 WiFi Driver Loader for RTL8821AU
# Loads kernel modules for TP-Link Archer T2U PLUS

set -e

# Wait for USB device enumeration
echo "Waiting for USB WiFi adapter (2357:0120)..."
for i in $(seq 1 30); do
    if lsusb 2>/dev/null | grep -q 2357; then
        echo "USB WiFi adapter found after ${i}s"
        break
    fi
    sleep 1
done

if ! lsusb 2>/dev/null | grep -q 2357; then
    echo "ERROR: USB WiFi adapter not found after 30s"
    exit 1
fi

# Load prerequisite modules
modprobe cfg80211 2>/dev/null || true
modprobe mac80211 2>/dev/null || true
sleep 1

# Load rtw88 modules in order
cd /root/wifi-build/rtw88
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    echo "Loading ${mod}..."
    if ! insmod ./${mod}.ko 2>&1; then
        echo "WARNING: Failed to load ${mod}"
    fi
done

sleep 2

# Verify
if lsmod | grep -q rtw_8821au; then
    echo "SUCCESS: RTW88 modules loaded"
    lsmod | grep rtw
else
    echo "ERROR: rtw_8821au not in lsmod"
    exit 1
fi
'''

stop_script = '''#!/bin/bash
# RTW88 WiFi Driver Unloader
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null || true
done
echo "RTW88 modules unloaded"
'''

wpa_start_script = '''#!/bin/bash
# WPA Supplicant starter - waits for WiFi interface dynamically

echo "Waiting for WiFi interface..."
for i in $(seq 1 30); do
    WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
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

ip link set "$WLAN" up
sleep 1

echo "Starting wpa_supplicant on $WLAN..."
exec /usr/sbin/wpa_supplicant -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf
'''

dhcp_start_script = '''#!/bin/bash
# DHCP client starter - waits for WiFi interface dynamically

sleep 5

WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -z "$WLAN" ]; then
    echo "ERROR: No WiFi interface found"
    exit 1
fi

echo "Starting dhcpcd on $WLAN..."
exec /usr/sbin/dhcpcd "$WLAN"
'''

# Write scripts via SFTP
for path, content in [
    ('/usr/local/bin/rtw88-wifi-start.sh', start_script),
    ('/usr/local/bin/rtw88-wifi-stop.sh', stop_script),
    ('/usr/local/bin/wpa-wifi-start.sh', wpa_start_script),
    ('/usr/local/bin/dhcpcd-wifi-start.sh', dhcp_start_script),
]:
    with sftp.open(path, 'w') as f:
        f.write(content)
    print(f"  Written: {path}")

sftp.close()

# Make executable
print(run("""
chmod +x /usr/local/bin/rtw88-wifi-start.sh
chmod +x /usr/local/bin/rtw88-wifi-stop.sh
chmod +x /usr/local/bin/wpa-wifi-start.sh
chmod +x /usr/local/bin/dhcpcd-wifi-start.sh
echo "Scripts made executable"
"""))

# Now rewrite the systemd service files to use the scripts
print("\n=== Rewriting systemd services ===")

rtw88_service = '''[Unit]
Description=Load RTW88 WiFi driver modules (RTL8821AU)
After=network-pre.target systemd-modules-load.service
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/rtw88-wifi-start.sh
ExecStop=/usr/local/bin/rtw88-wifi-stop.sh

[Install]
WantedBy=multi-user.target
'''

wpa_service = '''[Unit]
Description=WPA Supplicant for WiFi (RTL8821AU)
After=rtw88-wifi.service
Wants=rtw88-wifi.service

[Service]
Type=simple
ExecStart=/usr/local/bin/wpa-wifi-start.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
'''

dhcpcd_service = '''[Unit]
Description=DHCP Client for WiFi interface
After=wpa-wifi.service
Wants=wpa-wifi.service

[Service]
Type=forking
ExecStart=/usr/local/bin/dhcpcd-wifi-start.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
'''

sftp = client.open_sftp()
for path, content in [
    ('/etc/systemd/system/rtw88-wifi.service', rtw88_service),
    ('/etc/systemd/system/wpa-wifi.service', wpa_service),
    ('/etc/systemd/system/dhcpcd-wifi.service', dhcpcd_service),
]:
    with sftp.open(path, 'w') as f:
        f.write(content)
    print(f"  Written: {path}")
sftp.close()

print(run("systemctl daemon-reload && echo 'daemon-reload done'"))

# Test: start the services now
print("\n=== Testing: start rtw88-wifi service ===")
print(run("systemctl start rtw88-wifi 2>&1 && echo 'rtw88-wifi started' || echo 'rtw88-wifi FAILED'"))
print(run("systemctl status rtw88-wifi 2>&1 | head -15"))

print("\n=== Module check ===")
print(run("lsmod | grep rtw"))

print("\n=== WiFi interface? ===")
print(run("ip link show | grep wl"))

# Start wpa
print("\n=== Testing: start wpa-wifi service ===")
print(run("systemctl start wpa-wifi 2>&1 && echo 'wpa-wifi started' || echo 'wpa-wifi FAILED'", timeout=45))
time.sleep(8)
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "Interface: $WLAN"
wpa_cli -i "$WLAN" status 2>&1 | grep -E 'ssid|wpa_state|ip_address'
"""))

# Start dhcpcd
print("\n=== Testing: start dhcpcd-wifi service ===")
print(run("systemctl start dhcpcd-wifi 2>&1 && echo 'dhcpcd-wifi started' || echo 'dhcpcd-wifi FAILED'", timeout=30))
time.sleep(10)

# Final status
print("\n=== Final WiFi Status ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "Interface: $WLAN"
echo "IP: $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}')"
echo "SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
echo "State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
echo ""
echo "Ping test:"
ping -c 2 -W 3 8.8.8.8 2>&1 | tail -3
"""))

print("\n=== All services ===")
print(run(r"""
for svc in rtw88-wifi wpa-wifi dhcpcd-wifi; do
    STATUS=$(systemctl is-active $svc 2>&1)
    echo "  $svc: $STATUS"
done
"""))

client.close()
print("\n=== FIX APPLIED - Ready for reboot test ===")
