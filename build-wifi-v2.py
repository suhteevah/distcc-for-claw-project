import paramiko
import sys
import time

host = "10.0.0.6"
username = "root"
password = "cnc-server-2024!"

# Wait for reboot
print("Waiting 30s for reboot...")
time.sleep(30)

# Try connecting
for attempt in range(10):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, timeout=10)
        print(f"Connected after attempt {attempt+1}")
        break
    except Exception as e:
        print(f"Attempt {attempt+1}: {e}")
        time.sleep(10)
else:
    print("Failed to connect!")
    sys.exit(1)

# Verify flex is available
stdin, stdout, stderr = client.exec_command("flex --version && bison --version | head -1", timeout=10)
print("Verify:", stdout.read().decode().strip())

# Now do the full build
script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
KVER_BASE=6.12

echo "=== Verify tools ==="
gcc --version | head -1
flex --version
bison --version | head -1

echo ""
echo "=== Step 1: Prepare kernel source (already downloaded) ==="
cd /tmp/linux-${KVER_BASE}

# Ensure config and symvers are in place
cp "/lib/modules/${KVER}/config" .config
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

echo ""
echo "=== Step 2: make olddefconfig ==="
make olddefconfig 2>&1 | tail -3

echo ""
echo "=== Step 3: make modules_prepare ==="
make modules_prepare 2>&1 | tail -20

echo ""
echo "=== Step 4: Create symlinks using transactional-update shell trick ==="
# Since /lib/modules is read-only on the live system, we use a bind mount trick
# Actually, we can just use the KSRC variable to point directly to our source tree
# The WiFi driver Makefile supports KSRC= to override
echo "Kernel build dir ready at /tmp/linux-${KVER_BASE}"
ls -la /tmp/linux-${KVER_BASE}/.config
ls -la /tmp/linux-${KVER_BASE}/Module.symvers

echo ""
echo "=== Step 5: Clone RTL8821AU driver if needed ==="
cd /tmp
if [ ! -d "8821au-20210708" ]; then
    git clone --depth=1 https://github.com/morrownr/8821au-20210708.git
    echo "Cloned driver repo"
else
    echo "Driver repo already exists"
fi

echo ""
echo "=== Step 6: Build the WiFi driver ==="
cd /tmp/8821au-20210708

# Clean any previous build
make clean 2>/dev/null || true

# Build with explicit kernel source path
# The morrownr 8821au driver Makefile uses KSRC
make ARCH=x86_64 KSRC="/tmp/linux-${KVER_BASE}" 2>&1 | tail -40

echo ""
echo "=== Step 7: Check build result ==="
if [ -f 8821au.ko ]; then
    echo "SUCCESS: 8821au.ko built!"
    ls -la 8821au.ko
    modinfo 8821au.ko 2>/dev/null | head -10
else
    echo "Looking for any .ko files..."
    find . -name '*.ko' -type f 2>/dev/null
fi

echo ""
echo "=== Done ==="
"""

chan = client.get_transport().open_session()
chan.settimeout(900)
chan.exec_command(f"cat > /tmp/build-wifi-v2.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/build-wifi-v2.sh 2>&1")

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
