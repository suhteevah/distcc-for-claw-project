import paramiko
import sys
import os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== System status ==="
echo "Kernel: $KVER"
uptime

echo ""
echo "=== USB devices ==="
lsusb 2>/dev/null || echo "lsusb not found"

echo ""
echo "=== Previous crash info ==="
journalctl -b -1 -k --no-pager 2>/dev/null | grep -i 'BUG\|panic\|NULL\|oops\|fault\|device_links' | tail -20 || echo "No prev boot journal"

echo ""
echo "=== Current dmesg for USB/WiFi ==="
dmesg | grep -i 'usb\|wifi\|wlan\|8821\|rtl\|2357' | tail -20

echo ""
echo "=== Check driver exists ==="
ls -la ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null || echo "NO 8821au.ko"

echo ""
echo "=== Our struct module patch ==="
grep -A3 'klp_ipa_clones_padding' ${WORKDIR}/linux-6.12/include/linux/module.h 2>/dev/null || echo "Patch not found"

echo ""
echo "=== Size comparison ==="
if [ -f ${WORKDIR}/8821au-20210708/8821au.ko ]; then
    echo "Our module:"
    objdump -h ${WORKDIR}/8821au-20210708/8821au.ko | grep this_module
    echo "Reference:"
    zstd -d /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f 2>/dev/null
    objdump -h /tmp/r8152.ko | grep this_module
fi

echo ""
echo "=== Loaded modules ==="
lsmod | grep -i 'cfg\|8821\|mac80211' || echo "No wifi modules loaded"

echo ""
echo "=== CRITICAL: Analyze the crash ==="
echo "The crash was: device_links_driver_bound+0x163/0x2d0"
echo "Address: 000000000001448a - NOT zero, not our NULL padding"
echo "This is 0x1448a which is in the middle of some structure"
echo "This suggests the USB driver has a real bug, not our padding issue"
echo ""
echo "=== Let's try a SAFE approach ==="
echo "1. Load cfg80211"
modprobe cfg80211 2>&1
echo "cfg80211 result: $?"

echo ""
echo "2. Check if USB adapter is plugged in"
if lsusb 2>/dev/null | grep -q '2357:0120'; then
    echo "YES - USB adapter is present (2357:0120)"

    echo ""
    echo "3. Clear dmesg and try insmod"
    dmesg -C 2>/dev/null

    echo "Loading 8821au.ko..."
    insmod ${WORKDIR}/8821au-20210708/8821au.ko 2>&1
    RESULT=$?
    echo "insmod exit code: $RESULT"

    sleep 3

    echo ""
    echo "4. Check dmesg after load"
    dmesg 2>/dev/null | tail -50

    echo ""
    echo "5. Check if module is loaded"
    lsmod | grep 8821 || echo "NOT loaded"

    echo ""
    echo "6. Check interfaces"
    ip link show 2>/dev/null

    echo ""
    echo "7. Check for wlan"
    iwconfig 2>/dev/null || ip link | grep wlan
else
    echo "NO - USB adapter NOT plugged in"
    echo ""
    echo "=== Testing without adapter ==="
    echo "Loading module without USB device present..."
    dmesg -C 2>/dev/null
    insmod ${WORKDIR}/8821au-20210708/8821au.ko 2>&1
    RESULT=$?
    echo "insmod exit code: $RESULT"
    sleep 2
    echo ""
    echo "dmesg after load:"
    dmesg 2>/dev/null | tail -30
    echo ""
    lsmod | grep 8821 || echo "NOT loaded"
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/inv2.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/inv2.sh 2>&1")

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

with open("investigate-v2-output.txt", "w", encoding="utf-8") as f:
    f.write(output)
    f.write(f"\nExit code: {chan.recv_exit_status()}\n")

# Print with safe encoding
for line in output.split('\n'):
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'replace').decode('ascii'))

print(f"\nExit code: {chan.recv_exit_status()}")
client.close()
