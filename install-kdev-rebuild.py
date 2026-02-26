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

# Step 1: Install kernel-default-devel via transactional-update
print("=== Step 1: Install kernel-default-devel ===")
result = run("""
echo "Current kernel: $(uname -r)"
echo ""

# Check if already installed
rpm -q kernel-default-devel 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Already installed!"
else
    echo "Installing via transactional-update..."
    transactional-update -n pkg install kernel-default-devel 2>&1
fi
""", timeout=600)
print(result)

# Step 2: Reboot to activate new snapshot
print("\n=== Step 2: Rebooting ===")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent")
client.close()

# Wait for reboot
print("Waiting for reboot...")
time.sleep(40)

for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}/20...")
    try:
        client2 = paramiko.SSHClient()
        client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client2.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

        def run2(cmd, timeout=120):
            stdin, stdout, stderr = client2.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err

        print("  CONNECTED!")
        break
    except Exception as e:
        print(f"  {e}")
else:
    print("FAILED to reconnect after reboot!")
    exit(1)

# Step 3: Verify kernel-devel is available
print("\n=== Step 3: Verify kernel-devel ===")
print(run2(r"""
KVER=$(uname -r)
echo "Kernel: $KVER"
echo ""

echo "=== kernel-default-devel package ==="
rpm -q kernel-default-devel 2>/dev/null

echo ""
echo "=== Build directory ==="
BUILD="/usr/lib/modules/$KVER/build"
ls -la "$BUILD" 2>/dev/null || echo "NOT FOUND at $BUILD"

# Try alternate locations
for dir in "/usr/src/linux-$KVER" "/usr/src/linux" "/lib/modules/$KVER/build"; do
    if [ -d "$dir" ]; then
        echo "Found: $dir"
        ls "$dir/Module.symvers" 2>/dev/null && echo "  Has Module.symvers" || echo "  NO Module.symvers"
    fi
done

echo ""
echo "=== Module.symvers check ==="
find /usr/lib/modules/$KVER/ /usr/src/ -name 'Module.symvers' 2>/dev/null | head -5

echo ""
echo "=== Verify ieee80211 symbols ==="
for f in $(find /usr/lib/modules/$KVER/ /usr/src/ -name 'Module.symvers' 2>/dev/null | head -3); do
    COUNT=$(grep -c ieee80211 "$f" 2>/dev/null)
    echo "$f: $COUNT ieee80211 symbols"
done
"""))

# Step 4: Rebuild rtw88 against proper kernel
print("\n=== Step 4: Rebuild rtw88 ===")
print(run2(r"""
KVER=$(uname -r)

# Find the correct build directory
BUILD=""
for dir in "/usr/lib/modules/$KVER/build" "/usr/src/linux-$KVER-obj/x86_64/default" "/usr/src/linux" "/lib/modules/$KVER/build"; do
    if [ -d "$dir" ] && [ -f "$dir/Module.symvers" ]; then
        BUILD="$dir"
        break
    fi
done

if [ -z "$BUILD" ]; then
    echo "ERROR: No kernel build directory with Module.symvers found!"
    echo "Falling back to custom source with SUSE Module.symvers..."

    # Copy SUSE Module.symvers to our build tree
    if [ -f "/usr/lib/modules/$KVER/Module.symvers" ]; then
        cp "/usr/lib/modules/$KVER/Module.symvers" /root/wifi-build/linux-6.12/Module.symvers
        BUILD="/root/wifi-build/linux-6.12"
        echo "Copied SUSE Module.symvers to $BUILD"
    fi
fi

if [ -n "$BUILD" ]; then
    echo "Building against: $BUILD"
    echo ""

    cd /root/wifi-build/rtw88
    make clean 2>/dev/null
    make KSRC="$BUILD" 2>&1 | tail -40

    echo ""
    echo "=== Built modules ==="
    find . -name '*.ko' -type f | sort
else
    echo "FATAL: No usable kernel build directory!"
fi
""", timeout=300))

# Step 5: Load modules
print("\n=== Step 5: Load modules ===")
print(run2(r"""
cd /root/wifi-build/rtw88
KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)
echo "Built $KO_COUNT modules"

if [ "$KO_COUNT" -gt 0 ]; then
    # Load dependencies
    modprobe cfg80211 2>/dev/null
    modprobe mac80211 2>/dev/null
    sleep 1

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
    lsmod | grep rtw
    echo ""
    dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipes\|probe' | tail -20
    echo ""
    ip link show
    iw dev 2>/dev/null
fi
""", timeout=60))

# Step 6: Connect WiFi
print("\n=== Step 6: Connect WiFi ===")
print(run2(r"""
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
    dmesg | grep -i 'rtw\|pipes\|probe\|error' | tail -15
fi
""", timeout=120))

client2.close()
print("\n=== DONE ===")
