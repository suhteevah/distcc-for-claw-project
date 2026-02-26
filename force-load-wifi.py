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

# Step 1: Reboot to get clean module state
print("=== Step 1: Reboot for clean state ===")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting...")
client.close()

time.sleep(40)
for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        print("  CONNECTED!")

        def run(cmd, timeout=120):
            stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err
        break
    except:
        pass
else:
    print("Failed to reconnect!")
    exit(1)

print(run("uname -r && uptime"))

# Step 2: Check clean state and find the kernel's own rtw88 modules
print("\n=== Step 2: Check kernel's built-in rtw88 modules ===")
print(run(r"""
KVER=$(uname -r)
echo "=== Kernel rtw88 modules ==="
find /usr/lib/modules/$KVER/ -name 'rtw88*' 2>/dev/null

echo ""
echo "=== Currently loaded rtw ==="
lsmod | grep rtw || echo "None"

echo ""
echo "=== What symbols does kernel rtw88_core export? ==="
# Try to find Module.symvers
for f in /usr/lib/modules/$KVER/Module.symvers /boot/Module.symvers-$KVER /usr/src/linux-*/Module.symvers; do
    if [ -f "$f" ]; then
        echo "Found: $f ($(wc -l < "$f") lines)"
        grep rtw88 "$f" | head -10
        echo "..."
        break
    fi
done
"""))

# Step 3: Try approach: use kernel's rtw88_core/rtw88_usb + our chip modules
print("\n=== Step 3: Hybrid approach - kernel core + our chip modules ===")
print(run(r"""
KVER=$(uname -r)

# Load the kernel's own rtw88 modules first
echo "Loading kernel rtw88_core..."
modprobe rtw88_core 2>&1
echo "rc=$?"

echo "Loading kernel rtw88_usb..."
modprobe rtw88_usb 2>&1
echo "rc=$?"

echo ""
lsmod | grep rtw88

echo ""
echo "=== Kernel rtw88_core exported symbols ==="
# Check what symbols are now available from loaded rtw88_core
cat /proc/kallsyms | grep ' rtw88\| rtw_' | grep ' T \| t ' | head -20
"""))

# Step 4: Now strip __versions from our chip-specific modules and load
print("\n=== Step 4: Strip versions and load chip modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Create stripped copies
mkdir -p /tmp/rtw88_stripped

for mod in rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo "Stripping __versions from ${mod}.ko..."
        objcopy --remove-section=__versions "./${mod}.ko" "/tmp/rtw88_stripped/${mod}.ko" 2>&1
        echo "  Original: $(stat -c%s "./${mod}.ko") bytes"
        echo "  Stripped: $(stat -c%s "/tmp/rtw88_stripped/${mod}.ko") bytes"
    fi
done

echo ""
echo "=== Try loading stripped chip modules ==="

# The kernel's rtw88_core and rtw88_usb are already loaded
# We need rtw_88xxa, rtw_8821a, rtw_8821au from our build
# But wait - the symbol names might differ (rtw88_ vs rtw_)

echo ""
echo "=== Check our module's expected symbols ==="
for mod in rtw_88xxa rtw_8821a rtw_8821au; do
    echo "--- ${mod}.ko needs: ---"
    modprobe --dump-modversions "./${mod}.ko" 2>/dev/null | grep 'rtw\|ieee80211' | head -10
    echo ""
done
"""))

# Step 5: Check if symbol names match between kernel's rtw88 and our rtw88
print("\n=== Step 5: Symbol name comparison ===")
print(run(r"""
echo "=== Our rtw_core exports (from module) ==="
cd /root/wifi-build/rtw88
nm rtw_core.ko 2>/dev/null | grep ' T ' | head -20

echo ""
echo "=== Kernel's rtw88_core exports (from kallsyms) ==="
cat /proc/kallsyms | grep ' T .*rtw' | head -20

echo ""
echo "=== Key function name check ==="
echo "Our module expects:"
modprobe --dump-modversions ./rtw_8821a.ko 2>/dev/null | head -10
echo ""
echo "Kernel provides:"
cat /proc/kallsyms | grep rtw88xxa | head -10
cat /proc/kallsyms | grep rtw_read | head -5
"""))

# Step 6: Alternative - strip ALL our modules and force-load the full set
print("\n=== Step 6: Force-load full set (stripped) ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Unload kernel modules
rmmod rtw88_usb 2>/dev/null
rmmod rtw88_core 2>/dev/null
sleep 1

# Load cfg80211 and mac80211
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null

# Strip and load ALL our modules
echo "Stripping and loading..."
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        # Strip version CRCs
        objcopy --remove-section=__versions "./${mod}.ko" "/tmp/${mod}_stripped.ko" 2>&1

        echo -n "  insmod /tmp/${mod}_stripped.ko... "
        RESULT=$(insmod "/tmp/${mod}_stripped.ko" 2>&1)
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
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipes\|probe\|endpoint' | tail -30

echo ""
echo "=== Interfaces ==="
ip link show
iw dev 2>/dev/null
""", timeout=60))

# Step 7: WiFi connect
print("\n=== Step 7: WiFi ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 1
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8
    wpa_cli -i "$WLAN" status 2>&1
    echo ""
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1
    sleep 5
    ip addr show "$WLAN"
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    dmesg | grep -i 'rtw\|probe\|pipes\|endpoint\|error' | tail -15
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
