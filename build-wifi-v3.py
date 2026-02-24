import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Use /root instead of /tmp to survive reboots
script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
KVER_BASE=6.12
WORKDIR=/root/wifi-build

mkdir -p ${WORKDIR}
cd ${WORKDIR}

echo "=== Verify tools ==="
gcc --version | head -1
flex --version
bison --version | head -1
make --version | head -1

echo ""
echo "=== Step 1: Download kernel source ==="
if [ ! -f "linux-${KVER_BASE}.tar.xz" ]; then
    echo "Downloading kernel ${KVER_BASE} source..."
    wget -q "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KVER_BASE}.tar.xz" -O "linux-${KVER_BASE}.tar.xz"
    echo "Downloaded: $(ls -lh linux-${KVER_BASE}.tar.xz | awk '{print $5}')"
fi

echo ""
echo "=== Step 2: Extract kernel source ==="
if [ ! -d "linux-${KVER_BASE}" ]; then
    echo "Extracting... (this takes a minute)"
    tar xf "linux-${KVER_BASE}.tar.xz"
    echo "Extracted."
else
    echo "Already extracted."
fi

echo ""
echo "=== Step 3: Prepare kernel build ==="
cd "${WORKDIR}/linux-${KVER_BASE}"

# Copy running kernel config
cp "/lib/modules/${KVER}/config" .config

# Decompress Module.symvers from running kernel
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

echo "Running make olddefconfig..."
make olddefconfig 2>&1 | tail -5

echo ""
echo "Running make modules_prepare..."
make modules_prepare 2>&1 | tail -10

echo ""
echo "=== Step 4: Verify kernel build dir ==="
ls -la "${WORKDIR}/linux-${KVER_BASE}/.config" | awk '{print $NF, $5}'
ls -la "${WORKDIR}/linux-${KVER_BASE}/Module.symvers" | awk '{print $NF, $5}'
test -f "${WORKDIR}/linux-${KVER_BASE}/include/generated/uapi/linux/version.h" && echo "version.h: OK" || echo "version.h: MISSING"
test -f "${WORKDIR}/linux-${KVER_BASE}/include/config/auto.conf" && echo "auto.conf: OK" || echo "auto.conf: MISSING"
test -f "${WORKDIR}/linux-${KVER_BASE}/scripts/mod/modpost" && echo "modpost: OK" || echo "modpost: MISSING"

echo ""
echo "=== Step 5: Clone RTL8821AU driver ==="
cd ${WORKDIR}
if [ ! -d "8821au-20210708" ]; then
    git clone --depth=1 https://github.com/morrownr/8821au-20210708.git
    echo "Cloned."
else
    echo "Already cloned."
fi

echo ""
echo "=== Step 6: Build the WiFi driver ==="
cd ${WORKDIR}/8821au-20210708

# Clean
make clean 2>/dev/null || true

# Build with explicit kernel source path
echo "Building 8821au driver..."
make ARCH=x86_64 KSRC="${WORKDIR}/linux-${KVER_BASE}" 2>&1 | tail -50

echo ""
echo "=== Step 7: Check build result ==="
if [ -f 8821au.ko ]; then
    echo "SUCCESS: 8821au.ko built!"
    ls -la 8821au.ko
    modinfo 8821au.ko 2>/dev/null | head -10
else
    echo "Looking for any .ko files..."
    find . -name '*.ko' -type f 2>/dev/null
    echo ""
    echo "Build may have failed. Checking for errors in full build output..."
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(900)
chan.exec_command(f"cat > /root/build-wifi-v3.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/build-wifi-v3.sh 2>&1")

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
