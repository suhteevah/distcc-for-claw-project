import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Try installing just the basics that should work, skip cmake/libtool/kernel-devel
script = r"""#!/bin/bash
set -e

echo "=== Step 1: Check for Leap Micro update repos that might have kernel-devel ==="
# The Leap Micro 6.2 update repo might have matching kernel-default-devel
zypper lr -u 2>&1 | grep -i update || echo "No update repos found"

echo ""
echo "=== Step 2: Search SLE/Leap Micro repos for kernel-default-devel matching 6.12 ==="
# Check the source repo
zypper search -s kernel-default-devel --repo openSUSE:repo-main 2>&1 || true

echo ""
echo "=== Step 3: Check the installed kernel packages ==="
rpm -qa | grep kernel | sort

echo ""
echo "=== Step 4: Check what's in /usr/src/ already ==="
ls -la /usr/src/ 2>&1 || true

echo ""
echo "=== Step 5: Try to add Leap Micro 6.2 update repos ==="
# There should be an update repo for Leap Micro with the correct kernel-devel
zypper ar -f -c 'http://cdn.opensuse.org/update/leap-micro/6.2/sle/' 'sle-update' 2>&1 || true
zypper ar -f -c 'http://cdn.opensuse.org/update/leap-micro/6.2/backports/' 'backports-update' 2>&1 || true
zypper --gpg-auto-import-keys ref 2>&1 || true

echo ""
echo "=== Step 6: Now search kernel-default-devel in all repos ==="
zypper search -s kernel-default-devel 2>&1 || true

echo ""
echo "=== Step 7: Try to install minimal build toolchain ==="
echo "Installing: gcc gcc-c++ make git wget curl unzip htop tmux..."
transactional-update --non-interactive --continue pkg install \
    gcc gcc-c++ make \
    git wget curl \
    unzip tar gzip bzip2 xz \
    htop tmux \
    2>&1

echo ""
echo "=== Done ==="
echo "Exit code: $?"
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/install-toolchain2.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/install-toolchain2.sh",
    timeout=600
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print("STDERR:", err, end="")
client.close()
