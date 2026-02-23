import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Step 1: Install build dependencies via transactional-update ==="
# MicroOS needs transactional-update for package installs
transactional-update --non-interactive --continue pkg install git make gcc kernel-default-devel 2>&1

echo ""
echo "=== Step 2: Check if packages are available in the new snapshot ==="
# After transactional-update, packages are in a new snapshot
# We need to check /var/lib/overlay or reboot, OR use --continue to chain
echo "Packages will be available after reboot, but let's try chroot approach..."

# Actually, on MicroOS we can use transactional-update shell to build inside the snapshot
echo ""
echo "=== Step 3: Build the driver inside transactional-update shell ==="
transactional-update --non-interactive --continue run bash -c '
set -ex
echo "Inside transactional-update snapshot..."

# Check if gcc is available
which gcc && gcc --version | head -1

# Check kernel headers
ls /usr/src/linux-*/ 2>/dev/null | head -5 || echo "No kernel source found"
ls /lib/modules/$(uname -r)/build/ 2>/dev/null | head -5 || echo "No kernel build dir"

# Clone the driver
cd /tmp
if [ ! -d rtl8821au ]; then
    git clone https://github.com/morrownr/8821au-20210708.git rtl8821au
fi
cd rtl8821au

# Build
make -j$(nproc) 2>&1 | tail -20

# Install
make install 2>&1 | tail -10

echo "=== Driver built and installed ==="
'

echo ""
echo "=== DONE: Reboot needed to activate new snapshot ==="
echo "After reboot, run: modprobe 8821au"
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/build-wifi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/build-wifi.sh",
    timeout=300
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print(err, end="", file=sys.stderr)
client.close()
