import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# The kernel crashed with NULL pointer in device_links_driver_bound.
# The padding we added as void* was all zeros, and some code tries to
# walk these fields as list_heads. We need to understand exactly what
# fields SUSE adds and use the correct types.
#
# Looking at SUSE kernel source (CONFIG_LIVEPATCH_IPA_CLONES):
# - struct list_head klp_ipa_list; (used for IPA clone tracking)
# Plus there may be additional livepatch-related fields
#
# But actually, the crash might not be from our padding - it could be
# from the driver itself. Let me check more carefully.
# The crash is in device_links_driver_bound which is in driver core,
# suggesting a list corruption issue.
#
# A better approach: Instead of padding with void*, use proper list_head
# structures and other typed fields that match what SUSE expects.
#
# Actually - let me reconsider. The crash happens during module insertion
# and the NULL deref is at address 0x000000000001448a which suggests
# it's walking through the struct module at an offset and hitting garbage.
# With __randomize_layout, the field order IS randomized, so our padding
# fields are getting mixed in with real fields!
#
# Solution: We need to either:
# 1. Disable __randomize_layout for struct module (not practical)
# 2. Use the exact same field names and types as SUSE kernel
# 3. Or: Find the exact randomization seed (from the kernel build)
#
# Actually wait - __randomize_layout is based on a per-build random seed.
# The seed is part of the kernel config. Our modules_prepare uses the
# SAME config as the running kernel, so the randomization should be
# THE SAME. The problem is that our new fields are included in the
# randomization with different slot positions than what the running
# kernel expects.
#
# Real solution: Use EXACT field names and types from the SUSE patch.
# The field names influence the randomization (they're hashed).

script = r"""#!/bin/bash
set -e

WORKDIR=/root/wifi-build
KSRC=${WORKDIR}/linux-6.12

echo "=== Analysis: The struct is __randomize_layout ==="
echo "Field names affect randomization. We need exact SUSE field names."
echo ""

echo "=== Check the running kernel's randstruct seed ==="
# The randomization is determined at build time and baked into the kernel.
# Without the exact seed, we can't predict the layout.
# But the seed is in scripts/gcc-plugins/randomize_layout_seed.h
ls -la ${KSRC}/scripts/gcc-plugins/randomize_layout_seed.h 2>/dev/null || echo "No seed file"
cat ${KSRC}/scripts/gcc-plugins/randomize_layout_seed.h 2>/dev/null || echo "Can't read seed"

echo ""
echo "=== Check if randstruct is even enabled ==="
zcat /proc/config.gz | grep -i RANDSTRUCT || echo "RANDSTRUCT not found"
grep RANDSTRUCT ${KSRC}/.config || echo "RANDSTRUCT not in .config"

echo ""
echo "=== Check GCC plugins ==="
zcat /proc/config.gz | grep -i GCC_PLUGIN || echo "No GCC_PLUGINS"
grep GCC_PLUGIN ${KSRC}/.config || echo "No GCC_PLUGINS in .config"

echo ""
echo "=== The real question: is __randomize_layout active? ==="
# If no randstruct plugin/feature is enabled, __randomize_layout is a no-op
# and field order is deterministic. In that case, our padding should work
# IF placed in the right position.

echo ""
echo "=== Check if the crash was from our padding or something else ==="
echo "The crash was at device_links_driver_bound+0x163"
echo "Let's check if the USB device is even detected..."
lsusb 2>/dev/null | grep -i "tp-link\|realtek\|2357\|0bda" || echo "No TP-Link/Realtek USB device found!"

echo ""
echo "=== Check USB devices ==="
lsusb 2>/dev/null || true

echo ""
echo "=== Is the WiFi adapter plugged in? ==="
echo "The driver needs the USB WiFi adapter to be physically connected."
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/fix7.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix7.sh 2>&1")

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
