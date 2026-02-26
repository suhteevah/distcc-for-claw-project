import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check what's actually loaded
print("=== Step 1: Currently loaded rtw modules ===")
print(run("lsmod | grep rtw"))

# Step 2: Force unload in reverse dependency order
print("\n=== Step 2: Unloading all rtw modules ===")
print(run(r"""
# Show loaded modules with use counts
echo "Current state:"
lsmod | grep rtw

echo ""
echo "Removing in reverse dependency order..."

# Try all possible module names - both underscore and dash variants
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core \
           rtw88_8821au rtw88_8821a rtw88_88xxa rtw88_usb rtw88_core; do
    if lsmod | grep -q "^${mod}"; then
        echo -n "  rmmod $mod... "
        rmmod "$mod" 2>&1
        echo "done (rc=$?)"
    fi
done

# Also try module names with dashes
for mod in rtw-8821au rtw-8821a rtw-88xxa rtw-usb rtw-core; do
    if lsmod | grep -q "${mod}"; then
        echo -n "  rmmod $mod... "
        rmmod "$mod" 2>&1
        echo "done (rc=$?)"
    fi
done

sleep 1

echo ""
echo "Remaining rtw modules:"
lsmod | grep rtw || echo "(none - all cleared)"
"""))

# Step 3: Load patched modules
print("\n=== Step 3: Loading patched modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

echo "Available .ko files:"
find . -name '*.ko' -type f | sort

echo ""
echo "Loading in dependency order..."

for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  insmod ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED ($RC): $RESULT"
            # Check dmesg for details
            dmesg | tail -3
        fi
    else
        echo "  WARNING: ${mod}.ko not found!"
    fi
done

sleep 3

echo ""
echo "=== Loaded modules ==="
lsmod | grep rtw

echo ""
echo "=== dmesg (last 40) ==="
dmesg | tail -40
"""))

# Step 4: Check for WiFi interface
print("\n=== Step 4: Check WiFi interface ===")
print(run(r"""
echo "=== Network interfaces ==="
ip link show

echo ""
echo "=== Wireless devices ==="
iw dev 2>/dev/null

echo ""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "FOUND WiFi interface: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 1

    echo ""
    echo "=== Scanning ==="
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10

    echo ""
    echo "=== Connecting to Home_EXT ==="
    mkdir -p /etc/wpa_supplicant
    cat > /etc/wpa_supplicant/wpa_supplicant-${WLAN}.conf << 'WPAEOF'
ctrl_interface=/run/wpa_supplicant
update_config=1
country=US

network={
    ssid="Home_EXT"
    psk="Dolan1955"
    key_mgmt=WPA-PSK
    priority=1
}
WPAEOF

    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c "/etc/wpa_supplicant/wpa_supplicant-${WLAN}.conf" 2>&1
    sleep 8

    echo ""
    echo "=== WPA status ==="
    wpa_cli -i "$WLAN" status 2>&1

    echo ""
    echo "=== Getting DHCP ==="
    if which dhclient >/dev/null 2>&1; then
        dhclient "$WLAN" 2>&1
    elif which dhcpcd >/dev/null 2>&1; then
        dhcpcd "$WLAN" 2>&1
    elif which busybox >/dev/null 2>&1; then
        busybox udhcpc -i "$WLAN" 2>&1
    else
        echo "No DHCP client - trying systemd-networkd"
        mkdir -p /etc/systemd/network
        cat > /etc/systemd/network/25-wifi.network << 'NETEOF'
[Match]
Name=wl*

[Network]
DHCP=yes
NETEOF
        systemctl restart systemd-networkd 2>&1
    fi

    sleep 5

    echo ""
    echo "=== Connection result ==="
    ip addr show "$WLAN"
    echo ""
    echo "=== Internet test ==="
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -5
    echo ""
    ping -c 2 -W 5 google.com 2>&1 | tail -3
else
    echo "NO WiFi interface found"
    echo ""
    echo "=== Check firmware ==="
    dmesg | grep -i 'firmware\|rtw' | tail -20
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
