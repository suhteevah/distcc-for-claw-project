import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Unbind the USB device first, then force unload
print("=== Step 1: Unbind USB device and unload modules ===")
print(run(r"""
echo "=== Current state ==="
lsmod | grep rtw

echo ""
echo "=== Unbinding USB device ==="
# Unbind from rtw_8821au driver
echo "3-9:1.0" > /sys/bus/usb/drivers/rtw_8821au/unbind 2>&1 && echo "Unbound from rtw_8821au" || echo "Not bound to rtw_8821au"
sleep 1

echo ""
echo "=== Now unloading in reverse order ==="
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    echo -n "  rmmod $mod... "
    rmmod "$mod" 2>&1
    if [ $? -eq 0 ]; then
        echo "OK"
    else
        echo "FAILED, trying modprobe -r..."
        modprobe -r "$mod" 2>&1
    fi
done

sleep 1

echo ""
echo "=== Remaining modules ==="
lsmod | grep rtw || echo "(all cleared)"
"""))

# Step 2: Load patched modules
print("\n=== Step 2: Load patched modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Verify no rtw modules loaded
REMAINING=$(lsmod | grep -c rtw)
if [ "$REMAINING" -gt 0 ]; then
    echo "WARNING: $REMAINING rtw modules still loaded!"
    lsmod | grep rtw
    echo ""
    echo "Trying force removal..."
    for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
        rmmod -f "$mod" 2>/dev/null
    done
    sleep 1
fi

echo "Loading patched modules..."
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  insmod ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED ($RC): $RESULT"
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
echo "=== dmesg (last 30) ==="
dmesg | tail -30

echo ""
echo "=== Network interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
"""))

# Step 3: Check for WiFi and connect
print("\n=== Step 3: WiFi connection ===")
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
    wpa_cli -i "$WLAN" status 2>&1

    echo ""
    echo "Getting DHCP..."
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1 || busybox udhcpc -i "$WLAN" 2>&1
    sleep 5

    echo ""
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "NO WiFi interface"
    echo ""
    echo "Checking dmesg for probe issues..."
    dmesg | grep -i 'rtw_8821au\|probe\|pipes\|firmware' | tail -20
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
