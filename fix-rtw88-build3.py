import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check what SUSE exports for debugfs
print("=== Step 1: Check SUSE debugfs exports ===")
print(run("""
KVER=$(uname -r)
echo "Kernel: $KVER"

# Check Module.symvers for debugfs symbols
echo "--- debugfs symbols in Module.symvers ---"
grep debugfs /usr/lib/modules/$KVER/Module.symvers 2>/dev/null | head -20

echo ""
echo "--- debugfs in kallsyms ---"
cat /proc/kallsyms | grep -i 'debugfs_create_file' | head -10
"""))

# Step 2: Check full Makefile to understand structure
print("\n=== Step 2: Current Makefile ===")
print(run("cat -n /root/wifi-build/rtw88/Makefile"))

# Step 3: Fix Makefile - disable debugfs and remove PCI
print("\n=== Step 3: Fixing Makefile ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Backup original
cp Makefile Makefile.bak

# Fix 1: Disable DEBUG and DEBUGFS (lines 41-42)
# Change CONFIG_RTW88_DEBUG=1 to =0
# Change CONFIG_RTW88_DEBUGFS=1 to =0
sed -i 's/ccflags-y += -DCONFIG_RTW88_DEBUG=1/ccflags-y += -DCONFIG_RTW88_DEBUG=0/' Makefile
sed -i 's/ccflags-y += -DCONFIG_RTW88_DEBUGFS=1/ccflags-y += -DCONFIG_RTW88_DEBUGFS=0/' Makefile

# Verify the changes
echo "=== Changed lines ==="
grep -n 'CONFIG_RTW88_DEBUG' Makefile

# Fix 2: Check what modules are in MODLIST and remove PCI/SDIO if possible
echo ""
echo "=== Module list ==="
grep -n 'MODLIST\|obj-m\|rtw_pci\|rtw_sdio' Makefile
"""))

# Step 4: Check if we need to remove PCI from obj-m or MODLIST
print("\n=== Step 4: Examine module build targets ===")
print(run("""
cd /root/wifi-build/rtw88
# Show the full obj-m and related sections
grep -n -A2 'obj-m\|MODLIST\|pci\|sdio' Makefile | head -40
"""))

# Step 5: Remove PCI and SDIO from build targets
print("\n=== Step 5: Remove PCI and SDIO from build ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Comment out PCI and SDIO module entries
# We only need: rtw_core, rtw_usb, rtw_8821a, rtw_8821au (and maybe rtw_8821ae but that's PCI)

# Show what modules reference PCI
echo "=== Files referencing PCI ==="
grep -l 'pci' Makefile

# Let's see the exact obj-m lines
echo ""
echo "=== obj-m lines ==="
grep 'obj-m' Makefile
"""))

# Step 6: Selectively comment out PCI and SDIO modules
print("\n=== Step 6: Comment out PCI/SDIO modules ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Comment out any obj-m line containing pci or sdio
sed -i '/obj-m.*pci/s/^/#DISABLED_/' Makefile
sed -i '/obj-m.*sdio/s/^/#DISABLED_/' Makefile

# Also comment out any *-objs line for pci or sdio
sed -i '/pci.*-objs/s/^/#DISABLED_/' Makefile
sed -i '/sdio.*-objs/s/^/#DISABLED_/' Makefile

# Also check for PCI in MODLIST if it exists
sed -i '/MODLIST.*pci/s/^/#DISABLED_/' Makefile

echo "=== Modified Makefile ==="
cat -n Makefile
"""))

# Step 7: Clean and rebuild
print("\n=== Step 7: Clean build ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null

make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -80
""", timeout=300)
print(result)

# Step 8: Check results
print("\n=== Step 8: Check built modules ===")
print(run("""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f 2>/dev/null
echo ""
echo "=== Module info ==="
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    echo "--- $ko ---"
    modinfo "$ko" 2>/dev/null | head -5
    SIZE=$(objdump -h "$ko" 2>/dev/null | grep this_module | awk '{print $3}')
    echo "this_module size: $SIZE (need 00000580)"
    echo ""
done
"""))

# Step 9: If modules built, try loading them
print("\n=== Step 9: Attempt module loading ===")
print(run("""
cd /root/wifi-build/rtw88

# Check if .ko files exist
KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)
echo "Found $KO_COUNT .ko files"

if [ "$KO_COUNT" -gt 0 ]; then
    # First unload any existing rtw88 modules
    echo "Unloading existing modules..."
    rmmod rtw88_8821cu 2>/dev/null
    rmmod rtw88_8821c 2>/dev/null
    rmmod rtw88_usb 2>/dev/null
    rmmod rtw88_core 2>/dev/null
    sleep 1

    # Check what we have
    echo ""
    echo "Available modules to load:"
    find . -name '*.ko' -type f

    # Try loading core first
    if [ -f ./rtw_core.ko ]; then
        echo ""
        echo "Loading rtw_core.ko..."
        insmod ./rtw_core.ko 2>&1
        echo "Result: $?"
    fi

    # Then USB
    if [ -f ./rtw_usb.ko ]; then
        echo ""
        echo "Loading rtw_usb.ko..."
        insmod ./rtw_usb.ko 2>&1
        echo "Result: $?"
    fi

    # Then 8821a base
    if [ -f ./rtw_8821a.ko ]; then
        echo ""
        echo "Loading rtw_8821a.ko..."
        insmod ./rtw_8821a.ko 2>&1
        echo "Result: $?"
    fi

    # Then 8821au (USB variant)
    if [ -f ./rtw_8821au.ko ]; then
        echo ""
        echo "Loading rtw_8821au.ko..."
        insmod ./rtw_8821au.ko 2>&1
        echo "Result: $?"
    fi

    sleep 2

    echo ""
    echo "=== Loaded rtw modules ==="
    lsmod | grep rtw

    echo ""
    echo "=== USB devices ==="
    lsusb | grep -i 'realtek\|tp-link\|2357'

    echo ""
    echo "=== dmesg (last 30 lines) ==="
    dmesg | tail -30

    echo ""
    echo "=== Network interfaces ==="
    ip link show | grep -A1 'wlan'
else
    echo "No .ko files built - check build errors above"
fi
""", timeout=60))

client.close()
print("\n=== DONE ===")
