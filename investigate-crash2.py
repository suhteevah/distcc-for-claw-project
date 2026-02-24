import paramiko
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash

KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== Current kernel and uptime ==="
uname -r
uptime

echo ""
echo "=== Check if USB WiFi adapter is plugged in ==="
lsusb 2>/dev/null | grep -i '2357\|rtl\|realtek\|tp-link' || echo "No WiFi USB adapter detected in lsusb!"
echo "Full lsusb:"
lsusb 2>/dev/null || echo "lsusb not available"

echo ""
echo "=== Check dmesg for crash info from previous boot ==="
journalctl -b -1 -k 2>/dev/null | grep -i 'BUG\|panic\|NULL\|oops\|fault\|device_links' | tail -20 || echo "No previous boot journal"

echo ""
echo "=== Current dmesg ==="
dmesg | grep -i 'BUG\|panic\|NULL\|oops\|fault\|device_links\|usb\|8821\|rtl\|wifi\|wlan' | tail -30

echo ""
echo "=== Check if 8821au.ko exists ==="
ls -la ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null || echo "8821au.ko not found"

echo ""
echo "=== Our struct module patch ==="
grep -B1 -A3 'klp_ipa_clones_padding' ${WORKDIR}/linux-6.12/include/linux/module.h 2>/dev/null || echo "Patch not found"

echo ""
echo "=== Check size match ==="
if [ -f ${WORKDIR}/8821au-20210708/8821au.ko ]; then
    echo "Our module this_module:"
    objdump -h ${WORKDIR}/8821au-20210708/8821au.ko | grep this_module
    echo "Reference (r8152):"
    zstd -d /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f 2>/dev/null
    objdump -h /tmp/r8152.ko | grep this_module
fi

echo ""
echo "=== cfg80211 status ==="
lsmod | grep cfg80211 || echo "cfg80211 not loaded"

echo ""
echo "=== Module symbols needed ==="
if [ -f ${WORKDIR}/8821au-20210708/8821au.ko ]; then
    nm ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | grep ' U ' | grep -i 'device\|driver\|usb\|link\|cfg80211\|register\|alloc' | head -30
fi

echo ""
echo "=== Check vermagic ==="
modinfo ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | grep -E 'vermagic|depends|alias'

echo ""
echo "=== Analyze: Is the crash from our padding or from USB device init? ==="
echo "device_links_driver_bound operates on struct device, NOT struct module"
echo "The crash is in the USB subsystem when the driver binds to a device"
echo "This could be because:"
echo "  1. The USB adapter is not plugged in but driver tries to bind"
echo "  2. The driver's probe() function has a bug with this kernel version"
echo "  3. Our module struct offset is wrong causing misaligned field access"
echo ""
echo "=== Let's try a safe test: load cfg80211 only ==="
modprobe cfg80211 2>&1
echo "cfg80211 load result: $?"
lsmod | grep cfg80211

echo ""
echo "=== Now try insmod with dmesg monitoring ==="
echo "IMPORTANT: First check if USB adapter is present"
if lsusb 2>/dev/null | grep -q '2357:0120'; then
    echo "USB adapter IS plugged in"
    echo "Will attempt insmod..."
    dmesg -C 2>/dev/null  # Clear dmesg
    insmod ${WORKDIR}/8821au-20210708/8821au.ko 2>&1 || true
    sleep 2
    echo ""
    echo "=== dmesg after insmod ==="
    dmesg 2>/dev/null | tail -40
    echo ""
    echo "=== Module loaded? ==="
    lsmod | grep 8821 || echo "Module NOT in lsmod"
    echo ""
    echo "=== Network interfaces ==="
    ip link show 2>/dev/null | grep -A1 'wlan' || echo "No wlan interface"
else
    echo "USB adapter is NOT plugged in - skipping insmod test"
    echo "Please plug in the TP-Link Archer T2U PLUS and try again"
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(180)
chan.exec_command(f"cat > /root/investigate2.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/investigate2.sh 2>&1")

output = ""
while True:
    if chan.recv_ready():
        data = chan.recv(4096).decode('utf-8', errors='replace')
        if data:
            output += data
    if chan.exit_status_ready():
        while chan.recv_ready():
            data = chan.recv(4096).decode('utf-8', errors='replace')
            if data:
                output += data
        break

# Write to file to avoid encoding issues
with open("investigate-output.txt", "w", encoding="utf-8") as f:
    f.write(output)
    f.write(f"\nExit code: {chan.recv_exit_status()}\n")

print("Output saved to investigate-output.txt")
client.close()
