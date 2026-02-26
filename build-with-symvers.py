import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Build a complete Module.symvers from running system
print("=== Step 1: Build Module.symvers from running system ===")
print(run(r"""
KVER=$(uname -r)
echo "Kernel: $KVER"

# Start with the base Module.symvers (vmlinux symbols)
SUSE_SYMVERS="/usr/lib/modules/$KVER/Module.symvers"
if [ -f "$SUSE_SYMVERS" ]; then
    cp "$SUSE_SYMVERS" /tmp/combined_symvers.txt
    BASE_COUNT=$(wc -l < /tmp/combined_symvers.txt)
    echo "Base Module.symvers: $BASE_COUNT symbols"
else
    echo "No base Module.symvers!"
    > /tmp/combined_symvers.txt
fi

# Load mac80211 and cfg80211 first
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null
sleep 1

# Now extract symvers from mac80211 and cfg80211 modules
echo ""
echo "Extracting module symvers..."
for mod_path in $(find /usr/lib/modules/$KVER/kernel/net/ -name '*.ko*' 2>/dev/null); do
    # Decompress if needed
    REAL_PATH="$mod_path"
    if echo "$mod_path" | grep -q '\.zst$'; then
        TEMP="/tmp/$(basename ${mod_path%.zst})"
        zstd -d -f "$mod_path" -o "$TEMP" 2>/dev/null
        REAL_PATH="$TEMP"
    elif echo "$mod_path" | grep -q '\.xz$'; then
        TEMP="/tmp/$(basename ${mod_path%.xz})"
        xz -d -f -k "$mod_path" 2>/dev/null
        cp "${mod_path%.xz}" "$TEMP" 2>/dev/null || xz -d -c "$mod_path" > "$TEMP" 2>/dev/null
        REAL_PATH="$TEMP"
    fi

    if [ -f "$REAL_PATH" ]; then
        # Extract symvers using modprobe --dump-modversions
        SYMS=$(modprobe --dump-modversions "$REAL_PATH" 2>/dev/null)
        if [ -n "$SYMS" ]; then
            MOD_NAME=$(basename "$mod_path" | sed 's/\.ko.*$//')
            SYM_COUNT=$(echo "$SYMS" | wc -l)
            # Convert to Module.symvers format: CRC symbol module EXPORT_TYPE
            echo "$SYMS" | while read crc sym; do
                echo -e "0x${crc}\t${sym}\t${mod_path}\tEXPORT_SYMBOL"
            done >> /tmp/combined_symvers.txt
        fi
    fi
done

TOTAL=$(wc -l < /tmp/combined_symvers.txt)
echo "Total combined symvers: $TOTAL symbols"

# Check for key ieee80211 symbols
echo ""
echo "Key ieee80211 symbols:"
grep 'ieee80211_probereq_get\|ieee80211_channel_to_freq\|ieee80211_cqm_rssi' /tmp/combined_symvers.txt | head -5
"""))

# Step 2: Copy combined symvers to our build tree and rebuild
print("\n=== Step 2: Rebuild with correct symvers ===")
print(run(r"""
# Copy the combined Module.symvers
cp /tmp/combined_symvers.txt /root/wifi-build/linux-6.12/Module.symvers
echo "Copied combined Module.symvers"

# Verify key symbols present
KEY_SYMS="ieee80211_probereq_get ieee80211_channel_to_freq_khz cfg80211_rx_mgmt"
for sym in $KEY_SYMS; do
    if grep -q "$sym" /root/wifi-build/linux-6.12/Module.symvers; then
        echo "  $sym: FOUND"
    else
        echo "  $sym: MISSING"
    fi
done

echo ""
echo "Rebuilding..."
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -30
""", timeout=300))

# Step 3: Verify modules
print("\n=== Step 3: Verify modules ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== Built .ko files ==="
find . -name '*.ko' -type f | sort

echo ""
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(objdump -h "./${ko}.ko" 2>/dev/null | grep this_module | awk '{print $3}')
        echo "${ko}.ko: this_module=$SIZE"
    fi
done

echo ""
echo "=== Check symbol resolution ==="
# Verify rtw_core's dependencies resolve
modprobe --dump-modversions ./rtw_core.ko 2>/dev/null | grep ieee80211 | head -5
"""))

# Step 4: Unload old, load new
print("\n=== Step 4: Load modules ===")
print(run(r"""
# Unload everything
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1

echo "Cleared:"
lsmod | grep rtw || echo "  (none)"

# Ensure mac80211 loaded
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null

echo ""
echo "Loading patched modules..."
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
lsmod | grep -E 'rtw|mac80211|cfg80211'

echo ""
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipes\|probe\|endpoint' | tail -25

echo ""
echo "=== Interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
""", timeout=60))

# Step 5: Connect if interface exists
print("\n=== Step 5: WiFi ===")
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
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    dmesg | grep -i 'rtw\|probe\|pipes\|endpoint\|error' | tail -15
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
