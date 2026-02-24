import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# The SUSE kernel source RPM should be available from the source repo
# Or we can try to download kernel-default-devel from SUSE's repos
script = r"""#!/bin/bash
set -e

echo "=== Check the actual struct module size difference ==="
# The kernel was compiled with gcc-13, we're using gcc-7 - this might also affect struct layout

echo ""
echo "=== Try finding kernel-default-devel from SUSE Leap Micro 6.2 repos ==="
# Enable the source repo to find the kernel source RPM
# The Leap Micro main repo doesn't carry -devel packages
# But maybe there's a separate development repo

# Try the SLE development tools channel
# Leap Micro 6.2 is based on SLE Micro 6.2 which is based on SLFO 1.2
for url in \
    "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/" \
    ; do
    echo "Checking $url for kernel-default-devel..."
    curl -sL "$url/x86_64/" 2>/dev/null | grep -i 'kernel-default-devel' | head -5 || echo "  Not found"
done

echo ""
echo "=== Try getting nosrc RPM from source repo ==="
# The source repo is enabled but disabled by default
zypper mr -e openSUSE:repo-source 2>&1 || true
zypper ref 2>&1 | tail -5
zypper search -s kernel-default-devel --all-repos 2>&1 | head -20

echo ""
echo "=== Alternative: Search OBS for Leap Micro kernel-default-devel ==="
# Try direct download from OBS
curl -sfL "https://download.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/x86_64/" 2>/dev/null | grep -oP 'kernel[^"]*devel[^"]*' | head -10 || echo "Not in product repo"

echo ""
echo "=== Check if we can get kernel-devel from the Tumbleweed/Factory repo ==="
# The kernel 6.12.0-160000.5 is specific to Leap Micro 6.2 / SLFO
# Let's try a different approach: force load the module

echo ""
echo "=== Try forcing the module load ==="
modprobe --force 8821au 2>&1 || echo "modprobe force failed"
insmod --force /root/wifi-build/8821au-20210708/8821au.ko 2>&1 || echo "insmod force failed"

# insmod doesn't have --force, but modprobe does with the module in the right path
# But the module isn't in the right path yet (needs reboot for snapshot 9)

echo ""
echo "=== Workaround: Copy module to a location and use modprobe ==="
# Copy to /var which is writable
mkdir -p /var/lib/modules
cp /root/wifi-build/8821au-20210708/8821au.ko /var/lib/modules/

# Try insmod with force via kernel param
echo "Trying insmod..."
insmod /var/lib/modules/8821au.ko 2>&1
dmesg | tail -5
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/find-kdev.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/find-kdev.sh 2>&1")

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
