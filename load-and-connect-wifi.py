import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check all available .ko files and their dependencies
print("=== Step 1: Check module dependencies ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== All .ko files ==="
find . -name '*.ko' -type f | sort

echo ""
echo "=== Module dependencies ==="
for ko in $(find . -name '*.ko' -type f | sort); do
    DEPS=$(modinfo "$ko" 2>/dev/null | grep depends | head -1)
    echo "$ko: $DEPS"
done
"""))

# Step 2: Unload everything and reload in correct order
print("\n=== Step 2: Load modules in correct dependency order ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Unload everything first
echo "Unloading all rtw modules..."
for mod in rtw88_8821cu rtw88_8821c rtw88_8821au rtw88_8821a rtw88_usb rtw88_core rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1

echo "Current rtw modules:"
lsmod | grep rtw || echo "(none)"

echo ""
echo "=== Loading modules in dependency order ==="

# Correct order: core -> usb -> 88xxa -> 8821a -> 8821au
LOAD_ORDER="rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au"

for mod in $LOAD_ORDER; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  Loading ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED ($RC): $RESULT"
            # Show dmesg for this failure
            dmesg | tail -5
            echo ""
        fi
    else
        echo "  ${mod}.ko NOT FOUND!"
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

# Step 3: Check for WiFi interface
print("\n=== Step 3: Check for WiFi interface ===")
print(run("""
echo "=== Network interfaces ==="
ip link show

echo ""
echo "=== Wireless devices ==="
iw dev 2>/dev/null

echo ""
echo "=== USB device status ==="
lsusb | grep -i '2357\|realtek\|tp-link'

echo ""
echo "=== Driver binding ==="
for dir in /sys/bus/usb/drivers/rtw*; do
    echo "--- $dir ---"
    ls "$dir" 2>/dev/null
done
"""))

# Step 4: If WiFi interface exists, connect to network
print("\n=== Step 4: Configure WiFi ===")
print(run(r"""
# Find WiFi interface name
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)

if [ -z "$WLAN" ]; then
    echo "No WiFi interface found yet. Checking rfkill..."
    rfkill list 2>/dev/null
    echo ""
    echo "Checking if firmware is needed..."
    dmesg | grep -i 'firmware\|rtw88\|8821' | tail -20
else
    echo "Found WiFi interface: $WLAN"
    ip link set "$WLAN" up 2>&1
    echo ""

    # Check if NetworkManager or wpa_supplicant is available
    echo "=== Available WiFi tools ==="
    which nmcli 2>/dev/null && echo "nmcli available" || echo "nmcli not found"
    which wpa_supplicant 2>/dev/null && echo "wpa_supplicant available" || echo "wpa_supplicant not found"
    which iwctl 2>/dev/null && echo "iwctl available" || echo "iwctl not found"
    systemctl is-active NetworkManager 2>/dev/null && echo "NetworkManager running" || echo "NetworkManager not running"
    systemctl is-active wpa_supplicant 2>/dev/null && echo "wpa_supplicant running" || echo "wpa_supplicant not running"

    echo ""
    echo "=== Scanning for networks ==="
    iw dev "$WLAN" scan 2>&1 | grep -E 'SSID:|signal:' | head -20

    # Try connecting with wpa_supplicant
    if which wpa_supplicant >/dev/null 2>&1; then
        echo ""
        echo "=== Setting up WPA connection ==="

        # Create wpa_supplicant config
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

        echo "Created wpa_supplicant config"

        # Kill existing wpa_supplicant for this interface
        killall wpa_supplicant 2>/dev/null
        sleep 1

        # Start wpa_supplicant
        wpa_supplicant -B -i "$WLAN" -c "/etc/wpa_supplicant/wpa_supplicant-${WLAN}.conf" 2>&1
        echo "wpa_supplicant started"
        sleep 5

        # Check connection status
        wpa_cli -i "$WLAN" status 2>&1

        echo ""
        echo "=== Getting IP via DHCP ==="
        # Try dhclient or dhcpcd
        if which dhclient >/dev/null 2>&1; then
            dhclient "$WLAN" 2>&1
        elif which dhcpcd >/dev/null 2>&1; then
            dhcpcd "$WLAN" 2>&1
        else
            echo "No DHCP client found, trying ip/systemd..."
            # Try systemd-networkd or manual
            cat > /etc/systemd/network/20-wifi.network << 'NETEOF'
[Match]
Name=wl*

[Network]
DHCP=yes
NETEOF
            systemctl restart systemd-networkd 2>&1
        fi

        sleep 5

        echo ""
        echo "=== WiFi connection status ==="
        ip addr show "$WLAN"
        echo ""
        echo "=== Route ==="
        ip route | head -5
        echo ""
        echo "=== DNS ==="
        cat /etc/resolv.conf 2>/dev/null | head -5
        echo ""
        echo "=== Internet test ==="
        ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
    elif which nmcli >/dev/null 2>&1; then
        echo ""
        echo "=== Connecting with NetworkManager ==="
        nmcli dev wifi connect "Home_EXT" password "Dolan1955" 2>&1
        sleep 5
        nmcli connection show --active
        ip addr show "$WLAN"
    fi
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
