import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Install patched modules to proper kernel module directory
print("=== Step 1: Install patched modules ===")
print(run(r"""
KVER=$(uname -r)
echo "Kernel: $KVER"

cd /root/wifi-build/rtw88

# Create updates directory (takes priority over built-in modules)
DEST="/usr/lib/modules/$KVER/updates/rtw88"
mkdir -p "$DEST"

echo "Installing modules to $DEST..."
# Only install the modules we need (USB chain)
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        cp -v "./${mod}.ko" "$DEST/"
    else
        echo "WARNING: ${mod}.ko not found!"
    fi
done

echo ""
echo "Installed modules:"
ls -la "$DEST/"

echo ""
echo "Running depmod..."
depmod -a
echo "depmod done (rc=$?)"

echo ""
echo "Verify module resolution:"
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    FOUND=$(modinfo "$mod" 2>/dev/null | grep filename | head -1)
    echo "  $mod: $FOUND"
done
"""))

# Step 2: Set up auto-load config
print("\n=== Step 2: Configure auto-load ===")
print(run(r"""
# Create module load config
cat > /etc/modules-load.d/rtw88-wifi.conf << 'EOF'
# RTL8821AU WiFi driver (TP-Link Archer T2U PLUS)
rtw_core
rtw_usb
rtw_88xxa
rtw_8821a
rtw_8821au
EOF

echo "Created /etc/modules-load.d/rtw88-wifi.conf"
cat /etc/modules-load.d/rtw88-wifi.conf

echo ""
echo "=== Set up WiFi config for after reboot ==="

# Pre-create wpa_supplicant config
mkdir -p /etc/wpa_supplicant

# Create a generic wpa config that will work with any interface name
cat > /etc/wpa_supplicant/wpa_supplicant.conf << 'WPAEOF'
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

echo "Created /etc/wpa_supplicant/wpa_supplicant.conf"

# Check what network management is available
echo ""
echo "=== Network tools ==="
which wpa_supplicant 2>/dev/null && echo "wpa_supplicant: available" || echo "wpa_supplicant: NOT found"
which nmcli 2>/dev/null && echo "nmcli: available" || echo "nmcli: NOT found"
which dhclient 2>/dev/null && echo "dhclient: available" || echo "dhclient: NOT found"
which dhcpcd 2>/dev/null && echo "dhcpcd: available" || echo "dhcpcd: NOT found"
systemctl is-enabled NetworkManager 2>/dev/null && echo "NetworkManager: enabled" || echo "NetworkManager: not enabled"
systemctl is-enabled wpa_supplicant 2>/dev/null && echo "wpa_supplicant service: enabled" || echo "wpa_supplicant service: not enabled"
systemctl is-enabled systemd-networkd 2>/dev/null && echo "systemd-networkd: enabled" || echo "systemd-networkd: not enabled"

# Set up systemd-networkd config for WiFi DHCP
mkdir -p /etc/systemd/network
cat > /etc/systemd/network/25-wifi.network << 'NETEOF'
[Match]
Name=wl*

[Network]
DHCP=yes
DNS=8.8.8.8
DNS=8.8.4.4
NETEOF
echo "Created /etc/systemd/network/25-wifi.network"

# Create a startup script to connect WiFi after boot
cat > /root/connect-wifi.sh << 'SHEOF'
#!/bin/bash
# Auto-connect WiFi after boot
sleep 5
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "Found WiFi interface: $WLAN"
    ip link set "$WLAN" up
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf
    sleep 8
    if which dhclient >/dev/null 2>&1; then
        dhclient "$WLAN"
    elif which dhcpcd >/dev/null 2>&1; then
        dhcpcd "$WLAN"
    fi
    sleep 3
    ip addr show "$WLAN"
    echo "WiFi connection attempted"
else
    echo "No WiFi interface found"
fi
SHEOF
chmod +x /root/connect-wifi.sh
echo "Created /root/connect-wifi.sh"
"""))

# Step 3: Reboot
print("\n=== Step 3: Rebooting server ===")
print("Sending reboot command...")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot command sent")

client.close()

# Step 4: Wait for server to come back
print("\n=== Step 4: Waiting for server to reboot ===")
time.sleep(30)  # Initial wait

for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}/20 - trying SSH...")
    try:
        client2 = paramiko.SSHClient()
        client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client2.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

        def run2(cmd, timeout=60):
            stdin, stdout, stderr = client2.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err

        print("  CONNECTED!")

        # Step 5: Check post-reboot status
        print("\n=== Step 5: Post-reboot status ===")
        print(run2("uname -r"))
        print(run2("uptime"))

        print("\n=== Loaded rtw modules ===")
        print(run2("lsmod | grep rtw"))

        print("\n=== dmesg WiFi ===")
        print(run2("dmesg | grep -i 'rtw\\|wifi\\|wlan\\|8821\\|firmware\\|pipes' | tail -30"))

        print("\n=== Network interfaces ===")
        print(run2("ip link show"))
        print(run2("iw dev 2>/dev/null"))

        # Step 6: Try connecting WiFi
        print("\n=== Step 6: Connect WiFi ===")
        result = run2(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi interface: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 1

    echo "Scanning..."
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10

    echo ""
    echo "Connecting..."
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8

    echo ""
    echo "WPA status:"
    wpa_cli -i "$WLAN" status 2>&1

    echo ""
    echo "Getting DHCP..."
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1

    sleep 5
    echo ""
    echo "Connection:"
    ip addr show "$WLAN"
    echo ""
    echo "Internet test:"
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "NO WiFi interface found after reboot"
    echo ""
    echo "Module load status:"
    dmesg | grep -i 'rtw\|pipes\|probe\|firmware' | tail -20
fi
""", timeout=120)
        print(result)

        client2.close()
        break
    except Exception as e:
        print(f"  Not ready yet: {e}")

print("\n=== DONE ===")
