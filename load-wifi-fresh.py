import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Fresh boot - no old modules in memory
print("=== Server status ===")
print(run("uname -r && uptime"))

print("\n=== Current rtw modules (should be none) ===")
print(run("lsmod | grep rtw || echo 'None loaded - clean slate'"))

print("\n=== USB device ===")
print(run("lsusb | grep -i '2357\\|realtek\\|tp-link'"))

print("\n=== Available .ko files ===")
print(run("ls -la /root/wifi-build/rtw88/*.ko 2>/dev/null | head -10"))

# Load patched modules in dependency order
print("\n=== Loading patched modules ===")
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
            dmesg | tail -5
            echo ""
        fi
    else
        echo "  ${mod}.ko NOT FOUND"
    fi
done

sleep 3

echo ""
echo "=== Loaded modules ==="
lsmod | grep rtw

echo ""
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|pipes\|firmware\|wlan\|8821' | tail -30

echo ""
echo "=== Network interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
"""))

# WiFi connection
print("\n=== WiFi Connection ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "SUCCESS - WiFi interface: $WLAN"
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
    echo "=== RESULT ==="
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -5
    echo ""
    ping -c 2 -W 5 google.com 2>&1 | tail -3
else
    echo "NO WiFi interface"
    echo "Probe failed - checking dmesg..."
    dmesg | grep -i 'rtw_8821au\|pipes\|probe\|error' | tail -15
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
