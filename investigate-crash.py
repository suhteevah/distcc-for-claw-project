import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== Current kernel and uptime ==="
uname -r
uptime
snapper list | tail -5

echo ""
echo "=== Check if USB WiFi adapter is plugged in ==="
lsusb 2>/dev/null | grep -i '2357\|rtl\|realtek\|tp-link\|wifi\|wireless' || echo "No WiFi USB adapter detected!"
lsusb 2>/dev/null || echo "lsusb not available"

echo ""
echo "=== Check dmesg for last crash info ==="
dmesg | grep -i 'BUG\|panic\|NULL\|oops\|fault\|device_links' | tail -20

echo ""
echo "=== Check if 8821au.ko exists ==="
ls -la ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null || echo "8821au.ko not found"

echo ""
echo "=== Check our struct module patch ==="
grep -A3 'klp_ipa_clones_padding' ${WORKDIR}/linux-6.12/include/linux/module.h 2>/dev/null || echo "Patch not found"

echo ""
echo "=== Check if cfg80211 is loaded ==="
lsmod | grep cfg80211 || echo "cfg80211 not loaded"

echo ""
echo "=== Analyze the crash more carefully ==="
echo "The crash was in device_links_driver_bound+0x163"
echo "This function walks dev->links.consumers and dev->links.suppliers"
echo "These are list_head structures that must be properly initialized"
echo ""
echo "The issue is NOT our padding - it's the USB device registration"
echo "Let's check if the adapter is plugged in first"

echo ""
echo "=== Full lsusb ==="
lsusb 2>/dev/null

echo ""
echo "=== Check what the running kernel's struct module looks like ==="
echo "Our padding approach: void *klp_ipa_clones_padding[8] = all NULL"
echo "But device_links_driver_bound operates on struct device, not struct module"
echo "The crash might be from the driver's probe() function creating a device"
echo "with uninitialized list_head members"
echo ""
echo "Let's check if there's a better approach - maybe we need to look at"
echo "what SUSE actually adds to struct module for IPA_CLONES"

echo ""
echo "=== Check the SUSE kernel source for CONFIG_LIVEPATCH_IPA_CLONES ==="
echo "The 64-byte difference = 8 pointers = could be:"
echo "  - A list_head (2 ptrs) + other fields"
echo "  - An array of function pointers"
echo "  - A struct with mixed types"
echo ""
echo "=== Let's try a different approach: look at the actual binary ==="
echo "Compare our module's __this_module section byte-by-byte"

if [ -f ${WORKDIR}/8821au-20210708/8821au.ko ]; then
    echo ""
    echo "=== Module exists, checking sections ==="
    objdump -h ${WORKDIR}/8821au-20210708/8821au.ko | grep -E 'this_module|\.gnu'

    echo ""
    echo "=== Module info ==="
    modinfo ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | head -20

    echo ""
    echo "=== Check vermagic ==="
    modinfo ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | grep vermagic

    echo ""
    echo "=== Let's look at what symbols our module needs ==="
    nm ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | grep ' U ' | grep -i 'device\|driver\|usb\|link' | head -20
fi

echo ""
echo "=== Check kernel config for device_links related options ==="
zcat /proc/config.gz | grep -i 'DEVICE_LINK\|DL_' 2>/dev/null || echo "No device_link config found"

echo ""
echo "=== IMPORTANT: Check if the crash was actually from device_links ==="
echo "device_links_driver_bound walks list_heads on struct device"
echo "If the USB subsystem creates a device with uninitialized link lists,"
echo "the crash happens regardless of our module padding"
echo ""
echo "Let's try loading cfg80211 first, then loading our module WITHOUT"
echo "the USB adapter plugged in to see if the crash is USB-related"
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/investigate.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/investigate.sh 2>&1")

while True:
    if chan.recv_ready():
        data = chan.recv(4096).decode('utf-8', errors='replace')
        if data:
            print(data, end="")
            sys.stdout.flush()
    if chan.exit_status_ready():
        while chan.recv_ready():
            data = chan.recv(4096).decode('utf-8', errors='replace')
            if data:
                print(data, end="")
        break

print(f"\nExit code: {chan.recv_exit_status()}")
client.close()
