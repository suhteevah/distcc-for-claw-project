import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Extract Module.symvers from kernel's own modules
print("=== Step 1: Extract proper Module.symvers ===")
print(run(r"""
KVER=$(uname -r)
MODDIR="/usr/lib/modules/$KVER/kernel"

# Make sure rtw88_core and rtw88_usb are loaded so their symbols are in the kernel
modprobe rtw88_core 2>/dev/null
modprobe rtw88_usb 2>/dev/null

echo "Building Module.symvers from kernel modules..."

# Create a Python script to properly extract and format symvers
python3 << 'PYEOF'
import subprocess
import os
import glob

kver = subprocess.check_output(["uname", "-r"]).decode().strip()
moddir = f"/usr/lib/modules/{kver}/kernel"

# Find all relevant .ko.zst module files
modules_to_extract = []

# We need: vmlinux symbols + cfg80211 + mac80211 + rtw88_core + rtw88_usb
patterns = [
    f"{moddir}/net/wireless/cfg80211.ko*",
    f"{moddir}/net/mac80211/mac80211.ko*",
    f"{moddir}/drivers/net/wireless/realtek/rtw88/rtw88_core.ko*",
    f"{moddir}/drivers/net/wireless/realtek/rtw88/rtw88_usb.ko*",
]

for pattern in patterns:
    for f in glob.glob(pattern):
        modules_to_extract.append(f)

print(f"Found {len(modules_to_extract)} modules to extract symvers from")

symvers_lines = []

# Also check if there's a base Module.symvers for vmlinux symbols
base_symvers = f"/usr/lib/modules/{kver}/Module.symvers"
if os.path.exists(base_symvers):
    with open(base_symvers) as f:
        for line in f:
            line = line.strip()
            if line:
                symvers_lines.append(line)
    print(f"Base Module.symvers: {len(symvers_lines)} symbols")
else:
    print("No base Module.symvers found")
    # Try to find it elsewhere
    for alt in [f"/boot/symvers-{kver}.gz", f"/boot/Module.symvers-{kver}"]:
        if os.path.exists(alt):
            print(f"Found alternative: {alt}")
            break

# Extract symvers from each module
for mod_path in modules_to_extract:
    # Decompress if needed
    real_path = mod_path
    if mod_path.endswith('.zst'):
        tmp = f"/tmp/{os.path.basename(mod_path).replace('.zst', '')}"
        ret = os.system(f"zstd -d -f '{mod_path}' -o '{tmp}' 2>/dev/null")
        if ret == 0:
            real_path = tmp
        else:
            print(f"Failed to decompress {mod_path}")
            continue
    elif mod_path.endswith('.xz'):
        tmp = f"/tmp/{os.path.basename(mod_path).replace('.xz', '')}"
        ret = os.system(f"xz -d -f -c '{mod_path}' > '{tmp}' 2>/dev/null")
        if ret == 0:
            real_path = tmp
        else:
            continue

    # Use modprobe --dump-modversions to get CRCs
    try:
        result = subprocess.check_output(
            ["modprobe", "--dump-modversions", real_path],
            stderr=subprocess.DEVNULL
        ).decode()

        mod_name = os.path.basename(mod_path).split('.ko')[0]
        count = 0
        for line in result.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                crc = parts[0]
                sym = parts[1]
                # Module.symvers format: CRC\tsymbol\tmodule\tEXPORT_TYPE
                if not crc.startswith('0x'):
                    crc = f"0x{crc}"
                symvers_lines.append(f"{crc}\t{sym}\t{mod_path}\tEXPORT_SYMBOL")
                count += 1
        print(f"  {mod_name}: {count} symbols")
    except Exception as e:
        print(f"  Failed for {mod_path}: {e}")

# Write combined Module.symvers
output = "/root/wifi-build/linux-6.12/Module.symvers"
with open(output, 'w') as f:
    for line in symvers_lines:
        f.write(line + '\n')

print(f"\nTotal symbols: {len(symvers_lines)}")

# Verify key symbols
key_syms = ['rtw_phy_config_swing_table', 'rtw_phy_init', 'rtw_usb_probe',
            'rtw_usb_disconnect', 'ieee80211_probereq_get', 'cfg80211_rx_mgmt']
for sym in key_syms:
    found = any(sym in line for line in symvers_lines)
    print(f"  {sym}: {'FOUND' if found else 'MISSING'}")
PYEOF
""", timeout=60))

# Step 2: Rebuild - only need rtw88 chip modules
print("\n=== Step 2: Rebuild rtw88 ===")
print(run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null

# Build against our kernel source (which now has correct Module.symvers)
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -30
""", timeout=300))

# Step 3: Check build
print("\n=== Step 3: Check built modules ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f | sort | head -10

echo ""
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(objdump -h "./${ko}.ko" 2>/dev/null | grep this_module | awk '{print $3}')
        echo "${ko}.ko: this_module=$SIZE"
    fi
done
"""))

# Step 4: Load - use kernel's core, but also try our full set
print("\n=== Step 4: Load modules ===")
print(run(r"""
# Make sure kernel modules are clean
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core rtw88_usb rtw88_core; do
    rmmod $mod 2>/dev/null
done
sleep 1

# Load dependencies
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null

cd /root/wifi-build/rtw88

# Load our full module set
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
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipes\|probe\|endpoint' | tail -25

echo ""
echo "=== Interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
""", timeout=60))

# Step 5: WiFi
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
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    dmesg | grep -i 'rtw\|probe\|pipes\|endpoint\|error' | tail -15
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
