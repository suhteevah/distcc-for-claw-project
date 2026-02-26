import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Key insight: -DCONFIG_RTW88_DEBUGFS=0 still DEFINES the macro!
# #ifdef sees it as defined. Must REMOVE the define entirely.

# Step 1: Check ifdef style
print("=== Step 1: Check ifdef style ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "--- debug.h guards ---"
grep -n '#if\|#ifdef\|#ifndef\|#else\|#endif' debug.h
echo ""
echo "--- coex.c calls ---"
grep -n 'rtw_debugfs_get_simple_phy_info' coex.c debug.h debug.c 2>/dev/null
echo ""
echo "--- debug.h #else stubs ---"
awk '/#else/,/#endif/' debug.h
"""))

# Step 2: Fix Makefile - REMOVE debugfs/debug defines, disable PCI/SDIO
print("\n=== Step 2: Fix Makefile ===")
# Upload a Python fixer script to the server
fixer_script = r"""
import re

with open('/root/wifi-build/rtw88/Makefile', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    stripped = line.strip()

    # REMOVE (comment out) the DEBUG and DEBUGFS defines entirely
    if 'DCONFIG_RTW88_DEBUG=' in stripped and 'DEBUGFS' not in stripped:
        new_lines.append('# REMOVED: ' + line)
        continue
    if 'DCONFIG_RTW88_DEBUGFS=' in stripped:
        new_lines.append('# REMOVED: ' + line)
        continue

    # Comment out ALL PCI module targets
    pci_mods = ['rtw_pci', 'rtw_8723de', 'rtw_8812ae', 'rtw_8821ae',
                'rtw_8821ce', 'rtw_8822be', 'rtw_8822ce', 'rtw_8814ae']
    skip = False
    for m in pci_mods:
        if m in stripped and ('obj-m' in stripped or '-objs' in stripped):
            new_lines.append('# DISABLED_PCI: ' + line)
            skip = True
            break
    if skip:
        continue

    # Comment out ALL SDIO module targets
    sdio_mods = ['rtw_sdio', 'rtw_8723ds', 'rtw_8821cs', 'rtw_8822bs', 'rtw_8822cs']
    skip2 = False
    for m in sdio_mods:
        if m in stripped and ('obj-m' in stripped or '-objs' in stripped):
            new_lines.append('# DISABLED_SDIO: ' + line)
            skip2 = True
            break
    if skip2:
        continue

    new_lines.append(line)

with open('/root/wifi-build/rtw88/Makefile', 'w') as f:
    f.writelines(new_lines)

print("Makefile patched:")
print("- Removed CONFIG_RTW88_DEBUG define (not set to 0, fully removed)")
print("- Removed CONFIG_RTW88_DEBUGFS define (not set to 0, fully removed)")
print("- Disabled PCI modules")
print("- Disabled SDIO modules")
"""

# Write fixer script to server
run("cat > /tmp/fix_makefile.py << 'PYEOF'\n" + fixer_script + "\nPYEOF")

# Restore original and apply fix
print(run(r"""
cd /root/wifi-build/rtw88
git checkout Makefile 2>&1
python3 /tmp/fix_makefile.py
echo ""
echo "=== Verify ==="
grep -n 'REMOVED\|DISABLED\|CONFIG_RTW88_DEBUG' Makefile
"""))

# Step 3: Fix debug.h - add missing stub
print("\n=== Step 3: Fix debug.h stubs ===")
debug_h_fixer = r"""
with open('/root/wifi-build/rtw88/debug.h', 'r') as f:
    content = f.read()

# Check if stub already exists in the #else block
lines = content.split('\n')
in_else = False
has_stub = False
else_line_idx = -1

for i, line in enumerate(lines):
    if '#else' in line and 'CONFIG_RTW88_DEBUGFS' not in line:
        # This is the generic #else (for DEBUGFS stubs)
        pass
    if '#else' in line:
        in_else = True
        else_line_idx = i
    if in_else and 'rtw_debugfs_get_simple_phy_info' in line:
        has_stub = True
    if in_else and '#endif' in line:
        break

if has_stub:
    print("Stub already exists")
else:
    print("Adding missing stub for rtw_debugfs_get_simple_phy_info")
    # Find the function signature
    import re
    match = re.search(r'(void\s+rtw_debugfs_get_simple_phy_info\s*\([^)]*\))', content)
    if match:
        sig = match.group(1)
        print(f"Found: {sig}")
        # Add stub before the last #endif in the file
        last_endif = content.rfind('#endif')
        stub = "\nstatic inline " + sig + "\n{\n}\n\n"
        content = content[:last_endif] + stub + content[last_endif:]
        with open('/root/wifi-build/rtw88/debug.h', 'w') as f:
            f.write(content)
        print("Stub added")
    else:
        print("Could not find function signature, checking alternatives...")
        for line in content.split('\n'):
            if 'simple_phy' in line:
                print(f"  Found: {line.strip()}")
"""
run("cat > /tmp/fix_debug_h.py << 'PYEOF'\n" + debug_h_fixer + "\nPYEOF")
print(run("cd /root/wifi-build/rtw88 && git checkout debug.h 2>&1 && python3 /tmp/fix_debug_h.py"))

# Show the fixed #else block
print("\n=== debug.h #else block now ===")
print(run("awk '/#else/,/#endif/' /root/wifi-build/rtw88/debug.h"))

# Step 4: Check if rtw_dbg is also guarded
print("\n=== Step 4: Check rtw_dbg guards ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "--- rtw_dbg in debug.h ---"
grep -n 'rtw_dbg' debug.h | head -10
echo ""
echo "--- CONFIG_RTW88_DEBUG (not DEBUGFS) guards ---"
grep -n 'CONFIG_RTW88_DEBUG[^F]' debug.h
grep -n 'CONFIG_RTW88_DEBUG[^F]' debug.c | head -5
"""))

# Step 5: Clean rebuild
print("\n=== Step 5: Clean rebuild ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1
""", timeout=300)
print(result)

# Step 6: Check results
print("\n=== Step 6: Check built modules ===")
print(run("""
cd /root/wifi-build/rtw88
echo "=== .ko files ==="
find . -name '*.ko' -type f 2>/dev/null
echo ""
echo "=== Module details ==="
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    echo "--- $ko ---"
    SIZE=$(objdump -h "$ko" 2>/dev/null | grep this_module | awk '{print $3}')
    echo "this_module size: $SIZE (need 00000580)"
done
"""))

# Step 7: Load modules if built
print("\n=== Step 7: Load modules ===")
print(run("""
cd /root/wifi-build/rtw88
KO_COUNT=$(find . -name '*.ko' -type f 2>/dev/null | wc -l)
echo "Found $KO_COUNT .ko files"

if [ "$KO_COUNT" -gt 0 ]; then
    echo "Unloading existing..."
    for mod in rtw88_8821cu rtw88_8821c rtw88_8821au rtw88_8821a rtw88_usb rtw88_core; do
        rmmod $mod 2>/dev/null
    done
    sleep 1

    echo ""
    for mod in rtw_core rtw_usb rtw_8821a rtw_8821au; do
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
    echo "=== dmesg (last 50) ==="
    dmesg | tail -50
    echo ""
    echo "=== WiFi interfaces ==="
    ip link show 2>/dev/null
    echo ""
    iw dev 2>/dev/null
else
    echo "No .ko files - build failed"
fi
""", timeout=60))

client.close()
print("\n=== DONE ===")
