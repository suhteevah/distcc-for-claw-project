import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Strategy: Find the SUSE kernel-default-devel RPM from OBS/download.opensuse.org
# The SUSE kernel 6.12.0-160000.5 comes from SLFO (SUSE Linux Framework One)
# which is the base for Leap Micro 6.2
script = r"""#!/bin/bash
set -e

echo "=== Strategy: Find SUSE kernel-default-devel RPM ==="

KVER=$(uname -r)
echo "Running kernel: ${KVER}"

echo ""
echo "=== Check what repos are configured ==="
zypper lr -u 2>&1 | head -30

echo ""
echo "=== Search ALL repos for kernel-default-devel ==="
zypper search -s kernel-default-devel 2>&1 || true

echo ""
echo "=== Try to find the SUSE kernel source RPM ==="
zypper search -s kernel-source 2>&1 || true
zypper search -s kernel-syms 2>&1 || true

echo ""
echo "=== Check if we can add the SLE 16 / SLFO repo ==="
# The kernel version 6.12.0-160000 suggests SLFO 1.2 (SUSE Linux Framework One)
# which is used by SLE 16 and Leap Micro 6.2

echo ""
echo "=== Try downloading kernel-default-devel from download.opensuse.org ==="
# Try multiple potential locations
URLS=(
    "https://download.opensuse.org/distribution/leap-micro/6.2/repo/oss/x86_64/"
    "https://download.opensuse.org/update/leap-micro/6.2/sle/x86_64/"
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/Products:/Leap-Micro:/6.2/standard/x86_64/"
    "https://download.opensuse.org/repositories/Kernel:/stable/standard/x86_64/"
)

for url in "${URLS[@]}"; do
    echo "Trying: ${url}"
    result=$(curl -sL "${url}" 2>/dev/null | grep -o 'kernel-default-devel[^"]*rpm' | head -3)
    if [ -n "$result" ]; then
        echo "  FOUND: $result"
    else
        echo "  (nothing found)"
    fi
done

echo ""
echo "=== Alternative: Try to find it via zypper ==="
# Try adding a repo that might have it
zypper ar -f -c 'https://download.opensuse.org/distribution/leap-micro/6.2/repo/oss/' 'leap-micro-oss' 2>&1 || true
zypper --gpg-auto-import-keys ref 'leap-micro-oss' 2>&1 || true
zypper search -s -r 'leap-micro-oss' kernel-default-devel 2>&1 || true

echo ""
echo "=== Check the exact kernel package info ==="
rpm -qi kernel-default 2>&1 | head -20

echo ""
echo "=== Check repo of kernel-default ==="
zypper info kernel-default 2>&1 | head -30

echo ""
echo "=== Try: Can we just force-insert the module? ==="
echo "Checking modprobe --force option..."
cd /root/wifi-build/8821au-20210708
if [ -f 8821au.ko ]; then
    echo "Module exists. Trying insmod --force..."
    insmod --force 8821au.ko 2>&1 || echo "insmod --force failed"

    echo ""
    echo "Trying modprobe --force..."
    cp 8821au.ko /lib/modules/${KVER}/updates/ 2>/dev/null || true
    depmod -a 2>/dev/null || true
    modprobe --force 8821au 2>&1 || echo "modprobe --force failed"

    echo ""
    dmesg | tail -10
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /root/fix-module-v2.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-module-v2.sh 2>&1")

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
