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

# Diagnose why WiFi modules didn't load
print("=== Diagnose WiFi boot failure ===")
print(run(r"""
echo "=== rtw88-wifi service log ==="
journalctl -u rtw88-wifi --no-pager -n 30 2>&1

echo ""
echo "=== lsmod | grep rtw ==="
lsmod | grep rtw || echo "No rtw modules loaded"

echo ""
echo "=== Check if .ko files exist ==="
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    [ -f "/root/wifi-build/rtw88/${ko}.ko" ] && echo "  $ko.ko: exists" || echo "  $ko.ko: MISSING"
done

echo ""
echo "=== USB device present? ==="
lsusb | grep -i 2357 || echo "USB WiFi adapter NOT DETECTED"

echo ""
echo "=== dmesg for USB and rtw ==="
dmesg | grep -i 'rtw\|8821\|2357\|wlan\|cfg80211\|mac80211' | tail -20
"""))

# Try loading modules manually now
print("\n=== Try manual module load ===")
print(run(r"""
modprobe cfg80211 2>&1
modprobe mac80211 2>&1
sleep 1

cd /root/wifi-build/rtw88
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    echo -n "insmod ${mod}.ko... "
    RESULT=$(insmod ./${mod}.ko 2>&1)
    RC=$?
    if [ $RC -eq 0 ]; then
        echo "OK"
    else
        echo "FAILED($RC): $RESULT"
    fi
done
sleep 3

echo ""
echo "=== After manual load ==="
lsmod | grep rtw
echo ""
ip link show | grep wl
"""))

# Check dmesg after loading
print("\n=== dmesg after load ===")
print(run(r"dmesg | grep -i 'rtw\|firmware\|wlan\|8821' | tail -15"))

# Fix the service - it may need a delay for USB enumeration
print("\n=== Fix service with USB wait ===")
print(run(r"""
cat > /etc/systemd/system/rtw88-wifi.service << 'EOF'
[Unit]
Description=Load RTW88 WiFi driver modules (RTL8821AU)
After=network-pre.target systemd-modules-load.service
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
# Wait for USB enumeration to complete
ExecStartPre=/bin/bash -c 'for i in $(seq 1 30); do lsusb 2>/dev/null | grep -q 2357 && exit 0; sleep 1; done; echo "USB device not found after 30s"'
ExecStart=/bin/bash -c '\
    modprobe cfg80211 2>/dev/null; \
    modprobe mac80211 2>/dev/null; \
    sleep 1; \
    cd /root/wifi-build/rtw88 && \
    for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do \
        insmod ./${mod}.ko 2>/dev/null || true; \
    done; \
    sleep 3'
ExecStop=/bin/bash -c '\
    for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do \
        rmmod ${mod} 2>/dev/null || true; \
    done'

[Install]
WantedBy=multi-user.target
EOF

# Fix wpa service - use a more flexible approach that doesn't require exact interface name
cat > /etc/systemd/system/wpa-wifi.service << 'EOF'
[Unit]
Description=WPA Supplicant for WiFi (RTL8821AU)
After=rtw88-wifi.service
Wants=rtw88-wifi.service

[Service]
Type=simple
ExecStartPre=/bin/bash -c '\
    for i in $(seq 1 30); do \
        WLAN=$(ip link show 2>/dev/null | grep -oP "wl\w+" | head -1); \
        [ -n "$WLAN" ] && exit 0; \
        sleep 1; \
    done; \
    echo "No WiFi interface found after 30s"; exit 1'
ExecStart=/bin/bash -c '\
    WLAN=$(ip link show | grep -oP "wl\w+" | head -1); \
    ip link set "$WLAN" up; \
    sleep 1; \
    exec /usr/sbin/wpa_supplicant -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Fix dhcpcd service similarly
cat > /etc/systemd/system/dhcpcd-wifi.service << 'EOF'
[Unit]
Description=DHCP Client for WiFi interface
After=wpa-wifi.service
Wants=wpa-wifi.service

[Service]
Type=forking
ExecStartPre=/bin/bash -c 'sleep 8'
ExecStart=/bin/bash -c '\
    WLAN=$(ip link show | grep -oP "wl\w+" | head -1); \
    exec /usr/sbin/dhcpcd "$WLAN"'
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo "Services updated with USB wait and dynamic interface detection"
"""))

# Now start the WiFi services
print("\n=== Start WiFi services ===")
print(run(r"""
# WiFi modules should already be loaded from manual load above
systemctl start wpa-wifi 2>&1
sleep 8
systemctl start dhcpcd-wifi 2>&1
sleep 8

echo "=== WiFi Status ==="
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "Interface: $WLAN"
    wpa_cli -i "$WLAN" status 2>&1 | grep -E 'ssid|wpa_state|ip_address'
    echo ""
    ip addr show "$WLAN" | grep inet
fi
"""))

client.close()
print("\n=== DONE ===")
