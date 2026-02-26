import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check for alternate USB interface settings
print("=== Step 1: Check USB alternate settings ===")
print(run(r"""
echo "=== All USB interfaces for device 3-9 ==="
ls -la /sys/bus/usb/devices/3-9/3-9:*/

echo ""
echo "=== lsusb full descriptor ==="
lsusb -v -d 2357:0120 2>/dev/null | head -80
"""))

# Step 2: Show the exact rtw_usb_parse function
print("\n=== Step 2: Exact rtw_usb_parse function ===")
print(run(r"""
cd /root/wifi-build/rtw88
sed -n '230,300p' usb.c
"""))

# Step 3: Patch usb.c - make IN overflow non-fatal (just use first pipe)
print("\n=== Step 3: Patching usb.c ===")

patch_script = r"""
with open('/root/wifi-build/rtw88/usb.c', 'r') as f:
    content = f.read()

import re

# Replace the "IN pipes overflow" fatal error with a warning + continue
# Original pattern:
#   if (rtwusb->pipe_in) {
#       rtw_err(rtwdev, "IN pipes overflow\n");
#       return -EINVAL;
#   }
# Replace with:
#   if (rtwusb->pipe_in) {
#       rtw_warn(rtwdev, "IN pipes overflow, using first pipe\n");
#       continue;
#   }

old_in = '''if (rtwusb->pipe_in) {
\t\t\trtw_err(rtwdev, "IN pipes overflow\\n");
\t\t\treturn -EINVAL;
\t\t}'''

new_in = '''if (rtwusb->pipe_in) {
\t\t\tdev_warn(&usb_dev->dev, "IN pipes overflow, ignoring extra\\n");
\t\t\tcontinue;
\t\t}'''

if old_in in content:
    content = content.replace(old_in, new_in)
    print("Patched IN pipes overflow -> non-fatal warning")
else:
    print("Exact pattern not found for IN overflow, trying alternatives...")
    # Try with different whitespace
    lines = content.split('\n')
    patched = False
    for i, line in enumerate(lines):
        if 'IN pipes overflow' in line:
            # Replace the return -EINVAL with continue
            for j in range(i, min(i+3, len(lines))):
                if 'return -EINVAL' in lines[j]:
                    lines[j] = lines[j].replace('return -EINVAL', 'continue')
                    print(f"Patched line {j+1}: return -EINVAL -> continue")
                    patched = True
                    break
            if not patched:
                print(f"Found 'IN pipes overflow' at line {i+1} but no return -EINVAL nearby")
            break
    if patched:
        content = '\n'.join(lines)

# Do the same for INT pipes overflow - make non-fatal
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'INT pipes overflow' in line:
        for j in range(i, min(i+3, len(lines))):
            if 'return -EINVAL' in lines[j]:
                lines[j] = lines[j].replace('return -EINVAL', 'continue')
                print(f"Patched INT pipes overflow at line {j+1}: return -EINVAL -> continue")
                break
        break
content = '\n'.join(lines)

with open('/root/wifi-build/rtw88/usb.c', 'w') as f:
    f.write(content)

print("usb.c patched")
"""

run("cat > /tmp/fix_usb.py << 'PYEOF'\n" + patch_script + "\nPYEOF")
print(run("cd /root/wifi-build/rtw88 && git checkout usb.c 2>&1 && python3 /tmp/fix_usb.py"))

# Show the patched function
print("\n=== Patched rtw_usb_parse ===")
print(run("sed -n '230,300p' /root/wifi-build/rtw88/usb.c"))

# Step 4: Rebuild
print("\n=== Step 4: Rebuild ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -30
""", timeout=300)
print(result)

# Step 5: Reload and test
print("\n=== Step 5: Reload modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Check .ko files
KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)
echo "Built $KO_COUNT .ko files"

if [ "$KO_COUNT" -gt 0 ]; then
    # Unload all
    for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
        rmmod $mod 2>/dev/null
    done
    sleep 1

    # Load in order
    for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
        if [ -f "./${mod}.ko" ]; then
            echo -n "Loading ${mod}.ko... "
            RESULT=$(insmod "./${mod}.ko" 2>&1)
            RC=$?
            if [ $RC -eq 0 ]; then
                echo "OK"
            else
                echo "FAILED ($RC): $RESULT"
            fi
        fi
    done

    sleep 3

    echo ""
    echo "=== lsmod ==="
    lsmod | grep rtw

    echo ""
    echo "=== dmesg (last 30) ==="
    dmesg | tail -30

    echo ""
    echo "=== Network interfaces ==="
    ip link show
    echo ""
    iw dev 2>/dev/null

    # If WiFi interface exists, try connecting
    WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
    if [ -n "$WLAN" ]; then
        echo ""
        echo "=== WiFi interface found: $WLAN ==="
        ip link set "$WLAN" up 2>&1

        echo "Scanning..."
        iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10

        # Set up WPA connection
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
        sleep 5
        wpa_cli -i "$WLAN" status 2>&1

        echo ""
        echo "=== Getting DHCP ==="
        if which dhclient >/dev/null 2>&1; then
            dhclient "$WLAN" 2>&1
        elif which dhcpcd >/dev/null 2>&1; then
            dhcpcd "$WLAN" 2>&1
        fi
        sleep 5

        echo ""
        echo "=== Connection status ==="
        ip addr show "$WLAN"
        echo ""
        ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
    else
        echo "No WiFi interface yet"
    fi
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
