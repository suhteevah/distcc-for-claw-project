import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Find the correct kernel build directory
print("=== Step 1: Find correct kernel build/devel path ===")
print(run(r"""
KVER=$(uname -r)
echo "Running kernel: $KVER"

echo ""
echo "=== Check kernel-devel locations ==="
ls -la /usr/src/linux-* 2>/dev/null | head -10
ls -la /lib/modules/$KVER/build 2>/dev/null
ls -la /lib/modules/$KVER/source 2>/dev/null
ls -la /usr/lib/modules/$KVER/build 2>/dev/null
ls -la /usr/lib/modules/$KVER/source 2>/dev/null

echo ""
echo "=== Module.symvers locations ==="
find /usr/lib/modules/$KVER/ -name 'Module.symvers' 2>/dev/null
find /usr/src/ -name 'Module.symvers' 2>/dev/null | head -5
find /lib/modules/$KVER/ -name 'Module.symvers' 2>/dev/null

echo ""
echo "=== Our custom source ==="
ls /root/wifi-build/linux-6.12/Module.symvers 2>/dev/null && echo "exists" || echo "missing"

echo ""
echo "=== Compare symbol CRCs ==="
echo "--- ieee80211_probereq_get CRC in running kernel ---"
grep ieee80211_probereq_get /usr/lib/modules/$KVER/Module.symvers 2>/dev/null || echo "not in SUSE Module.symvers"

echo "--- ieee80211_probereq_get CRC in our build ---"
grep ieee80211_probereq_get /root/wifi-build/linux-6.12/Module.symvers 2>/dev/null || echo "not in custom Module.symvers"
"""))

# Step 2: Check what's different
print("\n=== Step 2: Diagnose symbol mismatch ===")
print(run(r"""
KVER=$(uname -r)

# Check if the SUSE kernel-devel package provides build infrastructure
echo "=== Kernel build dir ==="
BUILD=$(ls -d /usr/lib/modules/$KVER/build 2>/dev/null || ls -d /lib/modules/$KVER/build 2>/dev/null)
echo "Build dir: $BUILD"

if [ -d "$BUILD" ]; then
    echo "Contents:"
    ls "$BUILD/" 2>/dev/null | head -20
    echo ""
    echo "Has Module.symvers:"
    ls -la "$BUILD/Module.symvers" 2>/dev/null || echo "NO"
    echo ""
    echo "Has Makefile:"
    ls -la "$BUILD/Makefile" 2>/dev/null || echo "NO"
fi

echo ""
echo "=== Installed kernel packages ==="
rpm -qa 2>/dev/null | grep -i 'kernel.*devel\|kernel.*source\|kernel.*headers' | head -10
zypper se -i 2>/dev/null | grep -i 'kernel.*devel\|kernel.*source' | head -10

echo ""
echo "=== Can we use SUSE build dir directly? ==="
SUSE_BUILD="/usr/lib/modules/$KVER/build"
if [ -f "$SUSE_BUILD/Module.symvers" ]; then
    echo "YES - SUSE build dir has Module.symvers"
    echo "CRC count: $(wc -l < "$SUSE_BUILD/Module.symvers")"
    echo ""
    echo "Sample ieee80211 symbols:"
    grep 'ieee80211_probereq\|ieee80211_channel_to_freq' "$SUSE_BUILD/Module.symvers" | head -5
else
    echo "NO - need to install kernel-devel or copy Module.symvers"
fi
"""))

# Step 3: Try rebuilding against SUSE kernel build dir
print("\n=== Step 3: Rebuild against correct kernel ===")
print(run(r"""
KVER=$(uname -r)
SUSE_BUILD="/usr/lib/modules/$KVER/build"

if [ -d "$SUSE_BUILD" ] && [ -f "$SUSE_BUILD/Module.symvers" ]; then
    echo "Using SUSE kernel build dir: $SUSE_BUILD"

    cd /root/wifi-build/rtw88

    # Need to copy our struct module fix to the SUSE build dir too
    # Check if SUSE build dir has the same module padding issue
    echo ""
    echo "=== Check if SUSE build dir needs module padding ==="
    grep 'klp_ipa_clones_padding\|CONFIG_LIVEPATCH_IPA_CLONES' "$SUSE_BUILD/.config" 2>/dev/null | head -5

    echo ""
    echo "Check struct module in SUSE headers:"
    grep -A5 'klp_ipa_clones\|ipa_clones' "$SUSE_BUILD/include/linux/module.h" 2>/dev/null | head -10

    echo ""
    echo "=== Cleaning and rebuilding ==="
    make clean 2>/dev/null
    make KSRC="$SUSE_BUILD" 2>&1 | tail -40
else
    echo "SUSE build dir not found at $SUSE_BUILD"
    echo ""
    echo "Alternative: Copy SUSE Module.symvers to our build tree"
    SUSE_SYMVERS="/usr/lib/modules/$KVER/Module.symvers"
    if [ -f "$SUSE_SYMVERS" ]; then
        echo "Found Module.symvers at $SUSE_SYMVERS"
        echo "Copying to our build tree..."
        cp "$SUSE_SYMVERS" /root/wifi-build/linux-6.12/Module.symvers
        echo "Done. Rebuilding..."
        cd /root/wifi-build/rtw88
        make clean 2>/dev/null
        make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -40
    else
        echo "No Module.symvers found anywhere!"
        echo ""
        echo "Need to install kernel-devel:"
        echo "  transactional-update pkg install kernel-default-devel"
    fi
fi
""", timeout=300))

# Step 4: Check build results
print("\n=== Step 4: Check modules ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f | sort

echo ""
echo "=== Module sizes ==="
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(objdump -h "./${ko}.ko" 2>/dev/null | grep this_module | awk '{print $3}')
        echo "  ${ko}.ko: this_module=$SIZE"
    fi
done
"""))

# Step 5: Load if built successfully
print("\n=== Step 5: Load modules ===")
print(run(r"""
cd /root/wifi-build/rtw88
KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)

if [ "$KO_COUNT" -gt 0 ]; then
    # Unload old ones first
    for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
        rmmod $mod 2>/dev/null
    done
    sleep 1

    # Ensure mac80211 is loaded
    modprobe cfg80211 2>/dev/null
    modprobe mac80211 2>/dev/null

    # Load new ones
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
    lsmod | grep rtw

    echo ""
    echo "=== dmesg ==="
    dmesg | grep -i 'rtw\|pipes\|firmware\|wlan\|8821\|probe' | tail -20

    echo ""
    echo "=== Interfaces ==="
    ip link show
    iw dev 2>/dev/null
fi
""", timeout=60))

# Step 6: Connect WiFi if interface exists
print("\n=== Step 6: WiFi Connection ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 1
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
    echo ""
    ip addr show "$WLAN"
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
