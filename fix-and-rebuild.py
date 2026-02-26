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

# Step 1: Fix Module.symvers - restore from SUSE kernel
print("=== Step 1: Fix Module.symvers ===")
print(run(r"""
KVER=$(uname -r)

# Check what's currently there
echo "Current Module.symvers:"
head -3 /root/wifi-build/linux-6.12/Module.symvers
echo "..."
wc -l /root/wifi-build/linux-6.12/Module.symvers

echo ""
echo "SUSE Module.symvers:"
if [ -f "/usr/lib/modules/$KVER/Module.symvers" ]; then
    head -3 "/usr/lib/modules/$KVER/Module.symvers"
    echo "..."
    wc -l "/usr/lib/modules/$KVER/Module.symvers"

    # Copy it
    cp "/usr/lib/modules/$KVER/Module.symvers" /root/wifi-build/linux-6.12/Module.symvers
    echo ""
    echo "Copied SUSE Module.symvers to build tree"
    echo "New file:"
    head -2 /root/wifi-build/linux-6.12/Module.symvers
    echo "..."
    wc -l /root/wifi-build/linux-6.12/Module.symvers
else
    echo "SUSE Module.symvers not found!"

    # Try to regenerate from modules_prepare
    echo "Regenerating from modules_prepare..."
    cd /root/wifi-build/linux-6.12
    make modules_prepare 2>&1 | tail -5
fi
"""))

# Step 2: Rebuild
print("\n=== Step 2: Rebuild ===")
result = run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -40
""", timeout=300)
print(result)

if "Error" in result and "error:" in result.lower():
    # If MODPOST still fails, try with KBUILD_MODPOST_WARN=1
    print("\n--- Trying with MODPOST warnings only ---")
    result2 = run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" KBUILD_MODPOST_WARN=1 2>&1 | tail -40
""", timeout=300)
    print(result2)
    result = result2

# Step 3: Check build
print("\n=== Step 3: Check build ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f | sort | head -10
echo ""
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(stat -c%s "./${ko}.ko")
        echo "  ${ko}.ko: ${SIZE} bytes"
    fi
done
"""))

# Step 4: Verify the mac.c patch is still there
print("\n=== Step 4: Verify patch in built module ===")
print(run(r"""
cd /root/wifi-build/rtw88
# Check mac.c still has our patch
grep -n 'RTW_CHIP_TYPE_8821A' mac.c | head -10
"""))

# Step 5: Test loading without reboot first (unload old, load new)
print("\n=== Step 5: Load modules ===")
print(run(r"""
# Unload if any loaded
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1

# Ensure dependencies
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null
sleep 1

cd /root/wifi-build/rtw88
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  insmod ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED: $RESULT"
        fi
    fi
done

sleep 3

echo ""
echo "=== lsmod ==="
lsmod | grep -E 'rtw|mac80211'

echo ""
echo "=== dmesg (last 30 rtw lines) ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|mac.*power\|probe' | tail -30

echo ""
echo "=== Interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
""", timeout=60))

# Step 6: WiFi
print("\n=== Step 6: WiFi ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 2
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10
    echo ""
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8
    wpa_cli -i "$WLAN" status 2>&1
    echo ""
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1
    sleep 5
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    dmesg | grep -i 'rtw\|probe\|error\|mac.*power' | tail -20
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
