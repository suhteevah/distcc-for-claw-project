import paramiko
import sys
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    """Run command and return output"""
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check system state
print("=== System State ===")
print(run("uname -r && uptime"))

# Step 2: Check if rtw88 is already in this kernel (it's 6.12.0-160000.6 now!)
print("=== Check for built-in rtw88 modules ===")
print(run("find /lib/modules/$(uname -r) /usr/lib/modules/$(uname -r) -name '*rtw88*' 2>/dev/null"))

print("=== RTW88 kernel config ===")
print(run("zcat /proc/config.gz 2>/dev/null | grep -i RTW88 || echo 'No RTW88 config'"))

# Step 3: Try modprobe rtw88 modules
print("=== Try modprobe rtw88 ===")
print(run("modprobe rtw88_8821au 2>&1 || echo 'rtw88_8821au: not available'"))
print(run("modprobe rtw88_usb 2>&1 || echo 'rtw88_usb: not available'"))
print(run("modprobe rtw88_core 2>&1 || echo 'rtw88_core: not available'"))

# Step 4: Check if our build tools are still there
print("=== Build environment ===")
print(run("gcc --version 2>&1 | head -1"))
print(run("make --version 2>&1 | head -1"))
print(run("ls -la /root/wifi-build/ 2>/dev/null | head -10"))

# Step 5: Check if kernel source is still patched
print("=== Kernel source check ===")
kver = run("uname -r").strip()
print(f"Running kernel: {kver}")
print(run("ls /root/wifi-build/linux-6.12/include/linux/module.h 2>/dev/null && echo 'Kernel source present' || echo 'Kernel source MISSING'"))
print(run("grep -c 'klp_ipa_clones_padding' /root/wifi-build/linux-6.12/include/linux/module.h 2>/dev/null || echo 'Patch not found'"))

# IMPORTANT: Kernel version changed from .5 to .6 - need to update kernel source config!
print("\n=== CRITICAL: Kernel version changed! ===")
print(f"Running kernel: {kver}")
print(run("ls /root/wifi-build/linux-6.12/.config 2>/dev/null && head -5 /root/wifi-build/linux-6.12/.config || echo 'No .config'"))
# Check if the .config matches current kernel
print(run("grep 'CONFIG_LOCALVERSION=' /root/wifi-build/linux-6.12/.config 2>/dev/null || echo 'No LOCALVERSION in config'"))

# Step 6: Clone and try rtw88 backport
print("\n=== Building rtw88 backport ===")
print(run("""
cd /root/wifi-build

# Clone if not present
if [ ! -d rtw88 ]; then
    git clone https://github.com/lwfinger/rtw88.git 2>&1 | tail -5
else
    echo "rtw88 dir exists, pulling latest..."
    cd rtw88 && git pull 2>&1 | tail -3 && cd ..
fi

ls -la rtw88/ 2>/dev/null | head -10
"""))

# Step 7: First update kernel config for the new kernel version
print("=== Updating kernel config for new kernel ===")
print(run("""
cd /root/wifi-build/linux-6.12

# Copy current running kernel config
zcat /proc/config.gz > .config

# Apply our struct module patch if not already there
if ! grep -q 'klp_ipa_clones_padding' include/linux/module.h; then
    echo "Applying struct module padding patch..."
    sed -i '/struct klp_modinfo \\*klp_info;/a\\
\\n\\t/* SUSE compatibility: CONFIG_LIVEPATCH_IPA_CLONES fields */\\n\\tvoid *klp_ipa_clones_padding[8]; /* 64 bytes to match SUSE struct module size */' include/linux/module.h
else
    echo "Struct module patch already applied"
fi

# Run modules_prepare with correct version
make olddefconfig 2>&1 | tail -5
make modules_prepare 2>&1 | tail -10

echo "modules_prepare done"
""", timeout=300))

# Step 8: Build rtw88
print("=== Building rtw88 against patched kernel source ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -40
echo ""
echo "=== Built modules ==="
find . -name '*.ko' -type f 2>/dev/null
""", timeout=300)
print(result)

# Step 9: Check sizes
print("=== Module size check ===")
print(run("""
cd /root/wifi-build/rtw88
echo "Our rtw88 modules:"
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    echo "$ko:"
    objdump -h "$ko" | grep this_module || echo "  no this_module"
done
echo ""
echo "Reference module:"
REF=$(find /usr/lib/modules/$(uname -r) -name 'r8152.ko*' | head -1)
if [ -n "$REF" ]; then
    if [[ "$REF" == *.zst ]]; then
        zstd -d "$REF" -o /tmp/ref.ko -f 2>/dev/null
        objdump -h /tmp/ref.ko | grep this_module
    else
        objdump -h "$REF" | grep this_module
    fi
fi
"""))

# Step 10: Try loading - CAREFULLY (don't crash the server!)
print("=== Loading rtw88 modules (carefully) ===")
print(run("""
dmesg -C 2>/dev/null

# Load cfg80211 first
modprobe cfg80211 2>&1
echo "cfg80211: $?"

# Load rtw88 modules in order
cd /root/wifi-build/rtw88

if [ -f rtw88_core.ko ]; then
    echo "Loading rtw88_core..."
    insmod rtw88_core.ko 2>&1
    echo "  result: $?"
fi

if [ -f rtw88_usb.ko ]; then
    echo "Loading rtw88_usb..."
    insmod rtw88_usb.ko 2>&1
    echo "  result: $?"
fi

# Find the 8821a module
for ko in rtw88_8821a.ko rtw88_8821au.ko; do
    if [ -f "$ko" ]; then
        echo "Loading $ko..."
        insmod "$ko" 2>&1
        echo "  result: $?"
    fi
done

sleep 3

echo ""
echo "=== dmesg after loading ==="
dmesg 2>/dev/null | tail -40

echo ""
echo "=== Loaded modules ==="
lsmod | grep -i 'rtw88\|cfg80211\|mac80211'

echo ""
echo "=== Network interfaces ==="
ip link show 2>/dev/null

echo ""
echo "=== Wireless devices ==="
iw dev 2>/dev/null || iwconfig 2>/dev/null || echo "No wireless tools"
"""))

client.close()
print("\n=== DONE ===")
