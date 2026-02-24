import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Key insight: repo-main has kernel-default 6.12.0-160000.6.1 (newer)
# But the crucial thing is to check if kernel-default-devel is in repo-main
# Also: modules are at /usr/lib/modules/ not /lib/modules/ on Leap Micro
script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
echo "Running kernel: ${KVER}"

echo "=== Check: Where ARE the kernel modules? ==="
ls -la /lib/modules/ 2>/dev/null || echo "/lib/modules/ not found"
ls -la /usr/lib/modules/ 2>/dev/null || echo "/usr/lib/modules/ not found"
readlink -f /lib/modules 2>/dev/null || true

echo ""
echo "=== Search repo-main for ALL kernel packages ==="
zypper search -s -r 'openSUSE:repo-main' 'kernel*' 2>&1 || true

echo ""
echo "=== Check if kernel-default-devel is available in repo-main ==="
zypper info -r 'openSUSE:repo-main' kernel-default-devel 2>&1 || true

echo ""
echo "=== Try to download kernel-default-devel from repo-main ==="
zypper download kernel-default-devel 2>&1 || echo "Download failed"

echo ""
echo "=== Check the cached RPMs ==="
find /var/cache/zypp/ -name 'kernel*devel*' -type f 2>/dev/null
find /var/cache/zypp/ -name 'kernel-default-devel*' -type f 2>/dev/null

echo ""
echo "=== Alternative: Check direct download from the repo URL ==="
# The repo URL is: http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64
curl -sL "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/x86_64/" 2>/dev/null | grep -o 'kernel-default-devel[^"]*' | head -10
# Also check noarch
curl -sL "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/noarch/" 2>/dev/null | grep -o 'kernel[^"]*' | head -20

echo ""
echo "=== Direct URL check: Look for kernel-default-devel in repodata ==="
# Download the primary.xml.gz and search
cd /tmp
curl -sL "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/repodata/" 2>/dev/null | grep -o '[a-f0-9]*-primary.xml.gz' | head -1 | while read f; do
    echo "Found repodata: $f"
    curl -sL "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/repodata/$f" -o /tmp/primary.xml.gz 2>/dev/null
    if [ -f /tmp/primary.xml.gz ]; then
        zcat /tmp/primary.xml.gz 2>/dev/null | grep -i 'kernel-default-devel' | head -5
    fi
done

echo ""
echo "=== Alternative approach: extract headers from installed kernel RPM ==="
# The kernel-default RPM has been downloaded before
# Check if /boot has the config and System.map
ls -la /boot/ 2>/dev/null | head -20

echo ""
echo "=== Alternative approach: Try updating kernel to 160000.6.1 ==="
echo "If we update kernel and install kernel-default-devel together..."
echo "(just checking, not doing it yet)"
zypper info kernel-default-devel 2>&1 | head -20
"""

chan = client.get_transport().open_session()
chan.settimeout(300)
chan.exec_command(f"cat > /root/fix-module-v3.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-module-v3.sh 2>&1")

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
