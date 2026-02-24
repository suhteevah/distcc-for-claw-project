import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Strategy: Add padding to struct module to match the SUSE kernel's 0x580 size.
# The SUSE kernel has CONFIG_LIVEPATCH_IPA_CLONES=y which adds fields.
# We need to add exactly 64 bytes of padding (0x580 - 0x540 = 0x40 = 64).
# We'll add this right before the end of struct module, after the LIVEPATCH section.
# Since __randomize_layout randomizes field order, padding at any position should work.
# But to be safe, we add it at a known position.
script = r"""#!/bin/bash
set -e

WORKDIR=/root/wifi-build
KSRC=${WORKDIR}/linux-6.12

echo "=== Adding padding to struct module ==="

# First, let's see the exact LIVEPATCH section in struct module
echo "=== Current LIVEPATCH fields in struct module ==="
sed -n '/^#ifdef CONFIG_LIVEPATCH$/,/#endif/p' ${KSRC}/include/linux/module.h | grep -v 'struct klp_modinfo' | grep -v 'Elf_' | grep -v '@' | grep -v '\*\*' | grep -v '/\*\*' | grep -v '\*/' | head -20

# The SUSE CONFIG_LIVEPATCH_IPA_CLONES typically adds:
# - struct list_head klp_ipa_list; (16 bytes - 2 pointers)
# - Other IPA clone tracking fields
# Total likely: 64 bytes additional
#
# We'll add padding as "SUSE compatibility" fields inside the LIVEPATCH block

echo ""
echo "=== Patching include/linux/module.h ==="

# Find the LIVEPATCH section in struct module (inside struct module, not the klp_modinfo struct)
# We need to add padding AFTER the existing LIVEPATCH fields
# The section looks like:
# #ifdef CONFIG_LIVEPATCH
#     bool klp;
#     bool klp_alive;
#     struct klp_modinfo *klp_info;
# #endif

# We'll add our padding after klp_info but before the #endif
# Using sed to insert after "struct klp_modinfo *klp_info;"

cd ${KSRC}

# Backup
cp include/linux/module.h include/linux/module.h.bak

# Add 64 bytes of padding after klp_info line
# 64 bytes = 8 pointers on x86_64
sed -i '/struct klp_modinfo \*klp_info;/a\\n\t/* SUSE compatibility: CONFIG_LIVEPATCH_IPA_CLONES fields */\n\tvoid *klp_ipa_clones_padding[8]; /* 64 bytes to match SUSE struct module size */' include/linux/module.h

echo "Patch applied. Checking..."
grep -A 10 'CONFIG_LIVEPATCH' include/linux/module.h | grep -A 10 'bool klp;'

echo ""
echo "=== Verify: Rebuild modules_prepare ==="
make clean 2>&1 | tail -3
cp /usr/lib/modules/$(uname -r)/config .config
zcat /proc/config.gz > .config  # Use running kernel's config
make olddefconfig 2>&1 | tail -3
make modules_prepare 2>&1 | tail -10

echo ""
echo "=== Rebuild WiFi driver ==="
cd ${WORKDIR}/8821au-20210708
make clean 2>/dev/null || true
make ARCH=x86_64 KSRC="${KSRC}" 2>&1 | tail -20

echo ""
echo "=== Check new module struct size ==="
if [ -f 8821au.ko ]; then
    echo "Our module:"
    objdump -h 8821au.ko | grep this_module

    echo ""
    echo "Reference (r8152):"
    if [ ! -f /tmp/r8152.ko ]; then
        zstd -d /usr/lib/modules/$(uname -r)/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f 2>/dev/null
    fi
    objdump -h /tmp/r8152.ko | grep this_module

    echo ""
    OUR_SIZE=$(objdump -h 8821au.ko | grep this_module | awk '{print $3}')
    REF_SIZE=$(objdump -h /tmp/r8152.ko | grep this_module | awk '{print $3}')
    echo "Our size: 0x${OUR_SIZE}"
    echo "Ref size: 0x${REF_SIZE}"

    if [ "$OUR_SIZE" = "$REF_SIZE" ]; then
        echo ""
        echo "*** SIZE MATCHES! Attempting insmod... ***"
        insmod 8821au.ko 2>&1 || echo "insmod failed"
        dmesg | tail -10

        echo ""
        echo "=== Check for WiFi interface ==="
        ip link show 2>/dev/null | grep -A 2 'wlan'
        iw dev 2>/dev/null || true
    else
        echo ""
        echo "Size still doesn't match. Difference: $((0x${REF_SIZE} - 0x${OUR_SIZE})) bytes"
        echo "Need to adjust padding."
    fi
else
    echo "Build failed!"
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /root/fix-module-v6.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-module-v6.sh 2>&1")

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
