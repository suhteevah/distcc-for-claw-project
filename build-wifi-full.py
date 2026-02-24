import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# We need to:
# 1. Download kernel 6.12 source to get the headers
# 2. Set up the build directory with our running config
# 3. Clone the 8821au driver
# 4. Build it
script = r"""#!/bin/bash
set -ex

KVER=$(uname -r)
KVER_BASE=6.12

echo "=== Step 1: Download kernel source headers ==="
cd /tmp

# Download kernel 6.12 source
if [ ! -f "linux-${KVER_BASE}.tar.xz" ]; then
    echo "Downloading kernel ${KVER_BASE} source..."
    wget -q "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KVER_BASE}.tar.xz" -O "linux-${KVER_BASE}.tar.xz"
    echo "Downloaded."
fi

echo "=== Step 2: Extract kernel source ==="
if [ ! -d "linux-${KVER_BASE}" ]; then
    echo "Extracting..."
    tar xf "linux-${KVER_BASE}.tar.xz"
    echo "Extracted."
fi

echo "=== Step 3: Set up kernel build directory ==="
cd "/tmp/linux-${KVER_BASE}"

# Copy the running kernel's config
cp "/lib/modules/${KVER}/config" .config

# Decompress Module.symvers
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

# Prepare the kernel headers for module building
make olddefconfig 2>&1 | tail -5
make modules_prepare 2>&1 | tail -10

echo "=== Step 4: Create build/source symlinks ==="
# Create the build symlink that the driver Makefile expects
ln -sf "/tmp/linux-${KVER_BASE}" "/lib/modules/${KVER}/build"
ln -sf "/tmp/linux-${KVER_BASE}" "/lib/modules/${KVER}/source"

echo "=== Step 5: Verify build directory ==="
ls -la "/lib/modules/${KVER}/build/.config"
ls -la "/lib/modules/${KVER}/build/Module.symvers"
ls -la "/lib/modules/${KVER}/build/include/generated/uapi/linux/version.h" 2>/dev/null || echo "version.h generated path check needed"

echo ""
echo "=== Step 6: Clone RTL8821AU WiFi driver ==="
cd /tmp
if [ ! -d "8821au-20210708" ]; then
    git clone --depth=1 https://github.com/morrownr/8821au-20210708.git
fi
cd 8821au-20210708

echo ""
echo "=== Step 7: Build the driver ==="
# The morrownr driver uses KSRC for the kernel source path
make KSRC="/tmp/linux-${KVER_BASE}" 2>&1 | tail -30

echo ""
echo "=== Step 8: Check if module was built ==="
ls -la *.ko 2>/dev/null || echo "No .ko file found - build may have failed"

echo ""
echo "=== Done ==="
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /tmp/build-wifi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/build-wifi.sh 2>&1")

# Stream output
while True:
    if chan.recv_ready():
        data = chan.recv(4096).decode('utf-8', errors='replace')
        if data:
            print(data, end="")
            sys.stdout.flush()
    if chan.exit_status_ready():
        # Drain remaining
        while chan.recv_ready():
            data = chan.recv(4096).decode('utf-8', errors='replace')
            if data:
                print(data, end="")
        break

print(f"\nExit code: {chan.recv_exit_status()}")
client.close()
