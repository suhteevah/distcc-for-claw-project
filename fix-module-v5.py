import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Strategy: Directly patch struct module in the vanilla source to add
# the missing 64 bytes (padding or SUSE-specific fields).
# We know:
#   - Our module: this_module = 0x540 (1344 bytes)
#   - Running kernel: this_module = 0x580 (1408 bytes)
#   - Difference: 64 bytes (0x40)
#   - CONFIG_LIVEPATCH_IPA_CLONES=y adds fields to struct module
#
# Approach: Add dummy padding fields to struct module that match
# what the SUSE kernel expects. We can figure out what fields
# LIVEPATCH_IPA_CLONES adds by looking at the SUSE kernel source.
script = r"""#!/bin/bash
set -e

WORKDIR=/root/wifi-build
KSRC=${WORKDIR}/linux-6.12

echo "=== Analyzing struct module size difference ==="
echo "Need to add 64 bytes (0x40) to struct module"
echo ""

echo "=== Check what CONFIG_LIVEPATCH_IPA_CLONES controls ==="
# In SUSE kernels, LIVEPATCH_IPA_CLONES adds:
# - struct list_head klp_ipa_list  (16 bytes on x86_64 - list_head is 2 pointers)
# - Other SUSE-specific livepatch fields
# Plus there may be other SUSE patches adding fields

echo ""
echo "=== Check current struct module in our source ==="
grep -n 'CONFIG_LIVEPATCH' ${KSRC}/include/linux/module.h | head -20

echo ""
echo "=== Check what LIVEPATCH adds to struct module ==="
sed -n '/#ifdef CONFIG_LIVEPATCH/,/#endif/p' ${KSRC}/include/linux/module.h | head -30

echo ""
echo "=== Count lines and check end of struct module ==="
grep -n 'struct module {' ${KSRC}/include/linux/module.h
grep -n '^} ____cacheline_aligned' ${KSRC}/include/linux/module.h || \
    grep -n '} __randomize_layout' ${KSRC}/include/linux/module.h || \
    grep -n '^};' ${KSRC}/include/linux/module.h | tail -5

echo ""
echo "=== Show the LIVEPATCH section and a few lines around it ==="
LINE=$(grep -n 'CONFIG_LIVEPATCH' ${KSRC}/include/linux/module.h | head -1 | cut -d: -f1)
if [ -n "$LINE" ]; then
    START=$((LINE - 5))
    END=$((LINE + 20))
    sed -n "${START},${END}p" ${KSRC}/include/linux/module.h
fi

echo ""
echo "=== Show the end of struct module ==="
# Get line number of the struct closing
ENDLINE=$(grep -n '__randomize_layout\|____cacheline_aligned' ${KSRC}/include/linux/module.h | tail -1 | cut -d: -f1)
if [ -n "$ENDLINE" ]; then
    START=$((ENDLINE - 30))
    sed -n "${START},${ENDLINE}p" ${KSRC}/include/linux/module.h
fi

echo ""
echo "=== Approach: Add padding to match SUSE struct module size ==="
echo "We need exactly 64 extra bytes. Adding padding fields before the end of struct module."
echo ""
echo "=== Check what the SUSE kernel config says about these fields ==="
zcat /proc/config.gz | grep -E 'LIVEPATCH|MODULE_STATS|IPA_CLONES' || true

echo ""
echo "=== Our .config ==="
grep -E 'LIVEPATCH|MODULE_STATS|IPA_CLONES' ${KSRC}/.config || true

echo ""
echo "=== Check MODULE_STATS ==="
grep -n 'CONFIG_MODULE_STATS' ${KSRC}/include/linux/module.h | head -10
# MODULE_STATS can also add fields to struct module
sed -n '/#ifdef CONFIG_MODULE_STATS/,/#endif/p' ${KSRC}/include/linux/module.h | head -20
"""

chan = client.get_transport().open_session()
chan.settimeout(300)
chan.exec_command(f"cat > /root/fix-module-v5.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-module-v5.sh 2>&1")

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
