import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Running kernel ==="
uname -r

echo ""
echo "=== Kernel package info ==="
rpm -qi kernel-default | head -20

echo ""
echo "=== Check if /lib/modules has build symlink ==="
ls -la /lib/modules/$(uname -r)/ 2>&1 | head -10

echo ""
echo "=== Check for any kernel config ==="
ls -la /boot/config-* 2>/dev/null || echo "No config in /boot"
ls -la /lib/modules/$(uname -r)/config 2>/dev/null || echo "No config in modules"
zcat /proc/config.gz > /dev/null 2>&1 && echo "/proc/config.gz EXISTS" || echo "No /proc/config.gz"

echo ""
echo "=== Check for kernel source ==="
ls -la /lib/modules/$(uname -r)/source 2>/dev/null || echo "No source symlink"
ls -la /lib/modules/$(uname -r)/build 2>/dev/null || echo "No build symlink"

echo ""
echo "=== Package vendor/repo info for kernel ==="
rpm -q --queryformat '%{VENDOR}\n%{DISTRIBUTION}\n%{PACKAGER}\n%{URL}\n' kernel-default

echo ""
echo "=== Try to find the Leap Micro 6.2 update repo URL ==="
# Check if there's an update repo URL embedded in the kernel RPM
rpm -q --queryformat '%{SOURCERPM}\n' kernel-default

echo ""
echo "=== Check SUSEConnect repos if available ==="
SUSEConnect --list 2>&1 | head -30 || echo "SUSEConnect not available"

echo ""
echo "=== Check zypper products ==="
zypper products 2>&1 || true

echo ""
echo "=== Try direct URL for Leap Micro 6.2 product repo ==="
# The Leap Micro product repo might have kernel-default-devel
curl -sf -o /dev/null "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/x86_64/" && echo "Product repo accessible" || echo "Product repo NOT accessible"

echo ""
echo "=== Search in main repo for kernel-default-devel ==="
zypper search -s kernel-default-devel --repo openSUSE:repo-main 2>&1 || true

echo ""
echo "=== Alternatives: Check /proc/config.gz for building headers from source ==="
if [ -f /proc/config.gz ]; then
    echo "CONFIG EXISTS - we can extract it"
    zcat /proc/config.gz | head -5
fi
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/find-headers.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/find-headers.sh",
    timeout=60
)
out = stdout.read().decode()
err = stderr.read().decode()
print(out, end="")
if err:
    print("STDERR:", err, end="")
client.close()
