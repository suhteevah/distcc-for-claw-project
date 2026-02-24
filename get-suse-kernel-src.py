import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# The SUSE kernel has a different struct module due to CONFIG options
# Let's check what's different and try to fix it
script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== Check kernel module struct size from a loaded module ==="
# Get the section info from an existing kernel module to compare struct sizes
objdump -h /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst 2>/dev/null | grep this_module || true

# Try decompressing a kernel module first
cd /tmp
cp /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst . 2>/dev/null
zstd -d r8152.ko.zst -o r8152.ko 2>/dev/null || true
if [ -f r8152.ko ]; then
    echo "Reference module section sizes:"
    objdump -h r8152.ko 2>/dev/null | grep this_module
    echo ""
    echo "Our module section sizes:"
    objdump -h ${WORKDIR}/8821au-20210708/8821au.ko 2>/dev/null | grep this_module
fi

echo ""
echo "=== Check CONFIG options that affect struct module ==="
zcat /proc/config.gz | grep -E 'MODULE_SIG|MODULE_COMPRESS|MODULE_UNLOAD|MODVERSIONS|MODULE_ALLOW|MODULE_FORCE|MODULE_SRCVERSION|MODULE_DEBUG_AUTOLOAD_DUPS|TRIM_UNUSED_KSYMS|UNUSED_KSYMS_WHITELIST|MODULE_DECOMPRESS'

echo ""
echo "=== Check if there's a mismatch in the kernel .config we used ==="
grep -E 'MODULE_SIG|MODULE_COMPRESS|MODULE_UNLOAD|MODVERSIONS|MODULE_ALLOW|MODULE_FORCE|MODULE_SRCVERSION|MODULE_DEBUG_AUTOLOAD_DUPS|TRIM_UNUSED_KSYMS|UNUSED_KSYMS_WHITELIST|MODULE_DECOMPRESS' ${WORKDIR}/linux-6.12/.config

echo ""
echo "=== Try to find SUSE kernel source RPM ==="
# Check if we can download the nosrc.rpm and extract the patches
zypper search -s kernel-source --all-repos 2>&1 | head -10

echo ""
echo "=== Check the source repo for kernel-default ==="
zypper search --repo openSUSE:repo-source kernel-default 2>&1 | head -10

echo ""
echo "=== Alternative: Download kernel-default-devel from SUSE ==="
# Try to find the RPM directly - the package name for Leap Micro uses -160000 versioning
# Search the OBS for SLFO kernel
echo "Searching for kernel RPMs in source repo..."
zypper download kernel-default 2>&1 | head -5 || true

echo ""
echo "=== Check Module LIVEPATCH config ==="
zcat /proc/config.gz | grep -i 'LIVEPATCH\|MODULE_STATS'
grep -i 'LIVEPATCH\|MODULE_STATS' ${WORKDIR}/linux-6.12/.config 2>/dev/null || echo "Not in .config"
"""

chan = client.get_transport().open_session()
chan.settimeout(60)
chan.exec_command(f"cat > /root/check-src.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/check-src.sh 2>&1")

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
