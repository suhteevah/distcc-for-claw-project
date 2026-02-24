import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== Check what happened to LIVEPATCH in our build ==="
grep -i LIVEPATCH ${WORKDIR}/linux-6.12/.config

echo ""
echo "=== Check what LIVEPATCH looks like in the running kernel config ==="
zcat /proc/config.gz | grep -i LIVEPATCH

echo ""
echo "=== Check MODULE_STATS and other SUSE-specific options ==="
zcat /proc/config.gz | grep -E 'MODULE_STATS|MODULE_DEBUG_AUTOLOAD|MODULE_DECOMPRESS|MODULE_ALLOW_BTF'
echo "---"
grep -E 'MODULE_STATS|MODULE_DEBUG_AUTOLOAD|MODULE_DECOMPRESS|MODULE_ALLOW_BTF' ${WORKDIR}/linux-6.12/.config || echo "Not found in our config"

echo ""
echo "=== The LIVEPATCH_IPA_CLONES is SUSE-specific ==="
echo "Our source probably doesn't have it, causing LIVEPATCH deps to fail"
echo "Let's check if setting the right configs fixes struct module size"

echo ""
echo "=== Fix: Apply correct EXTRAVERSION and rebuild ==="
cd ${WORKDIR}/linux-6.12

# Set EXTRAVERSION in Makefile to match running kernel
sed -i 's/^EXTRAVERSION =.*/EXTRAVERSION = -160000.5-default/' Makefile
echo "Set EXTRAVERSION to -160000.5-default"
grep '^EXTRAVERSION' Makefile

# Check the actual auto.conf for LIVEPATCH
echo ""
echo "=== Check auto.conf for LIVEPATCH ==="
grep LIVEPATCH include/config/auto.conf 2>/dev/null || echo "LIVEPATCH not in auto.conf"

echo ""
echo "=== Force LIVEPATCH options in .config ==="
# Copy fresh config
cp "/lib/modules/${KVER}/config" .config

# Make sure LIVEPATCH is set - even if we don't have IPA_CLONES source
# The key thing is that include/linux/module.h uses #ifdef CONFIG_LIVEPATCH
# to add fields to struct module
make olddefconfig 2>&1 | tail -3

echo ""
echo "=== Check LIVEPATCH after olddefconfig ==="
grep LIVEPATCH .config
grep LIVEPATCH include/config/auto.conf 2>/dev/null || echo "Not in auto.conf yet"

echo ""
echo "=== Full modules_prepare ==="
# Clean and rebuild
make clean 2>&1 | tail -3
make modules_prepare 2>&1 | tail -10

echo ""
echo "=== Rebuild WiFi driver ==="
cd ${WORKDIR}/8821au-20210708
make clean 2>/dev/null || true
make ARCH=x86_64 KSRC="${WORKDIR}/linux-6.12" 2>&1 | tail -20

echo ""
echo "=== Check new module struct size ==="
if [ -f 8821au.ko ]; then
    echo "Our module:"
    objdump -h 8821au.ko | grep this_module
    echo ""
    echo "Reference (r8152):"
    zstd -d /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f 2>/dev/null
    objdump -h /tmp/r8152.ko | grep this_module

    echo ""
    echo "=== Try loading ==="
    insmod 8821au.ko 2>&1 || echo "Load failed"
    dmesg | tail -5
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /root/fix-lp.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-lp.sh 2>&1")

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
