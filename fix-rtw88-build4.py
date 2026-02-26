import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check how debug.c uses debugfs_create_file
print("=== Step 1: Check debug.c for debugfs guards ===")
print(run("""
cd /root/wifi-build/rtw88
echo "--- #ifdef guards in debug.c ---"
grep -n 'CONFIG_RTW88_DEBUGFS\|debugfs_create\|#ifdef\|#ifndef\|#endif\|#if ' debug.c | head -30
echo ""
echo "--- debug.h guards ---"
grep -n 'CONFIG_RTW88_DEBUGFS\|debugfs_create\|#ifdef\|#ifndef\|#endif' debug.h | head -30
"""))

# Step 2: Check if the code properly guards debugfs behind ifdefs
print("\n=== Step 2: Full debug.c content (first 80 lines) ===")
print(run("head -80 /root/wifi-build/rtw88/debug.c"))

# Step 3: Check the Makefile for how debug.o is included
print("\n=== Step 3: Check if debug.o is conditionally compiled ===")
print(run("""
cd /root/wifi-build/rtw88
grep -n 'debug' Makefile
"""))

# Step 4: The real fix - we need to:
# A) Remove debug.o from rtw_core-objs if DEBUGFS is disabled
# B) Remove ALL PCI chip modules from the build
# C) Remove ALL SDIO chip modules from the build
print("\n=== Step 4: Apply comprehensive Makefile fix ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Restore from original (undo previous changes)
git checkout Makefile 2>/dev/null || cp Makefile.bak Makefile 2>/dev/null

# Show current Makefile
echo "=== Current Makefile ==="
cat -n Makefile
"""))

# Step 5: Create a completely fixed Makefile
print("\n=== Step 5: Creating fixed Makefile ===")
print(run(r"""
cd /root/wifi-build/rtw88

# Read the original Makefile first
cat Makefile > /tmp/orig_makefile.txt

# Now create fixed version using Python for precise control
python3 << 'PYEOF'
with open('/root/wifi-build/rtw88/Makefile', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    lineno = i + 1
    stripped = line.strip()

    # Fix 1: Disable DEBUG and DEBUGFS
    if 'DCONFIG_RTW88_DEBUG=1' in line:
        new_lines.append(line.replace('DCONFIG_RTW88_DEBUG=1', 'DCONFIG_RTW88_DEBUG=0'))
        continue
    if 'DCONFIG_RTW88_DEBUGFS=1' in line:
        new_lines.append(line.replace('DCONFIG_RTW88_DEBUGFS=1', 'DCONFIG_RTW88_DEBUGFS=0'))
        continue

    # Fix 2: Remove debug.o from rtw_core-objs
    # The line looks like: rtw_core-objs += debug.o
    if 'debug.o' in stripped and 'rtw_core-objs' in stripped:
        new_lines.append('# DISABLED (debugfs not exported by SUSE): ' + line)
        continue

    # Fix 3: Comment out ALL PCI-related obj-m and objs lines
    # This includes rtw_pci and all PCI chip variant modules
    if any(pci in stripped for pci in ['rtw_pci', 'rtw_8723de', 'rtw_8812ae', 'rtw_8821ae', 'rtw_8821ce', 'rtw_8822be', 'rtw_8822ce', 'rtw_8814ae']):
        if 'obj-m' in stripped or '-objs' in stripped:
            new_lines.append('# DISABLED (PCI not needed for USB): ' + line)
            continue

    # Fix 4: Comment out ALL SDIO-related obj-m and objs lines
    if any(sdio in stripped for sdio in ['rtw_sdio', 'rtw_8723ds', 'rtw_8821cs', 'rtw_8822bs', 'rtw_8822cs']):
        if 'obj-m' in stripped or '-objs' in stripped:
            new_lines.append('# DISABLED (SDIO not needed for USB): ' + line)
            continue

    new_lines.append(line)

with open('/root/wifi-build/rtw88/Makefile', 'w') as f:
    f.writelines(new_lines)

print("Makefile patched successfully")
PYEOF

echo ""
echo "=== Fixed Makefile ==="
cat -n /root/wifi-build/rtw88/Makefile
"""))

# Step 6: Also need to check if debug.c compiles even without being in objs
# The issue might be that debug.c has functions called from other files
print("\n=== Step 6: Check if debug functions are called from other files ===")
print(run("""
cd /root/wifi-build/rtw88
echo "--- Functions exported from debug.c ---"
grep -n '^void\|^int\|^static' debug.c | head -20

echo ""
echo "--- Calls to debug functions from other files ---"
grep -rn 'rtw_debugfs_init\|rtw_debugfs' *.c *.h 2>/dev/null | grep -v debug.c | grep -v debug.h
"""))

# Step 7: Check debug.h for the stub/noop definitions when DEBUGFS is disabled
print("\n=== Step 7: Check debug.h stubs ===")
print(run("cat /root/wifi-build/rtw88/debug.h"))

# Step 8: Clean and rebuild
print("\n=== Step 8: Clean rebuild ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null

# Build only what we need
make KSRC="/root/wifi-build/linux-6.12" 2>&1
""", timeout=300)
print(result)

# Step 9: Check results
print("\n=== Step 9: Check built modules ===")
print(run("""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f 2>/dev/null

echo ""
echo "=== Module sizes ==="
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    SIZE=$(objdump -h "$ko" 2>/dev/null | grep this_module | awk '{print $3}')
    echo "$ko: this_module=$SIZE (need 00000580)"
done
"""))

# Step 10: If modules built, try loading
print("\n=== Step 10: Try loading modules ===")
print(run("""
cd /root/wifi-build/rtw88

KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)
echo "Found $KO_COUNT .ko files"

if [ "$KO_COUNT" -gt 0 ]; then
    # Unload existing
    rmmod rtw88_8821cu 2>/dev/null
    rmmod rtw88_8821c 2>/dev/null
    rmmod rtw88_usb 2>/dev/null
    rmmod rtw88_core 2>/dev/null
    sleep 1

    echo "Available modules:"
    find . -name '*.ko' -type f

    # Load in order
    for mod in rtw_core rtw_usb rtw_8821a rtw_8821au; do
        if [ -f "./${mod}.ko" ]; then
            echo ""
            echo "Loading ${mod}.ko..."
            insmod "./${mod}.ko" 2>&1
            echo "Exit code: $?"
        fi
    done

    sleep 2
    echo ""
    echo "=== Loaded rtw modules ==="
    lsmod | grep rtw

    echo ""
    echo "=== dmesg (last 40) ==="
    dmesg | tail -40

    echo ""
    echo "=== WiFi interfaces ==="
    ip link show 2>/dev/null | grep -A2 'wlan\|wlp'
    iw dev 2>/dev/null
else
    echo "No .ko files - build failed"
fi
""", timeout=60))

client.close()
print("\n=== DONE ===")
