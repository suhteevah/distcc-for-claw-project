import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Load mac80211 subsystem first
print("=== Step 1: Load mac80211 dependencies ===")
print(run(r"""
echo "Loading cfg80211..."
modprobe cfg80211 2>&1
echo "rc=$?"

echo "Loading mac80211..."
modprobe mac80211 2>&1
echo "rc=$?"

echo ""
echo "Loaded wireless modules:"
lsmod | grep -E 'cfg80211|mac80211'
"""))

# Step 2: Load rtw88 modules in order
print("\n=== Step 2: Load rtw88 modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  insmod ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED ($RC): $RESULT"
            dmesg | tail -3
            echo ""
        fi
    fi
done

sleep 3

echo ""
echo "=== Loaded modules ==="
lsmod | grep rtw

echo ""
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|pipes\|firmware\|wlan\|8821\|probe' | tail -30

echo ""
echo "=== Network interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
"""))

# Step 3: Connect WiFi if interface exists
print("\n=== Step 3: Connect WiFi ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi interface: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 1

    echo "Scanning..."
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10

    echo ""
    echo "Connecting to Home_EXT..."
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8

    echo "WPA status:"
    wpa_cli -i "$WLAN" status 2>&1

    echo ""
    echo "Getting DHCP..."
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1 || busybox udhcpc -i "$WLAN" 2>&1
    sleep 5

    echo ""
    echo "=== CONNECTION RESULT ==="
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -5
    echo ""
    ping -c 2 -W 5 google.com 2>&1 | tail -3
else
    echo "NO WiFi interface - probe failed"
    dmesg | grep -i 'rtw_8821au\|pipes\|probe\|error' | tail -15
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
