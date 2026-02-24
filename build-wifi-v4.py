import paramiko
import sys
import time

host = "10.0.0.6"
username = "root"
password = "cnc-server-2024!"

print("Waiting 30s for reboot...")
time.sleep(30)

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

# Verify openssl headers
stdin, stdout, stderr = client.exec_command("ls /usr/include/openssl/opensslv.h 2>&1", timeout=10)
print("OpenSSL headers:", stdout.read().decode().strip())

# Now do the full build
script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
KVER_BASE=6.12
WORKDIR=/root/wifi-build

cd ${WORKDIR}/linux-${KVER_BASE}

echo "=== Re-prepare kernel build (with openssl now available) ==="
# Config and symvers should still be there
cp "/lib/modules/${KVER}/config" .config
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

echo "make olddefconfig..."
make olddefconfig 2>&1 | tail -3

echo ""
echo "make modules_prepare..."
make modules_prepare 2>&1 | tail -15

echo ""
echo "=== Verify build artifacts ==="
test -f include/generated/uapi/linux/version.h && echo "version.h: OK" || echo "version.h: MISSING"
test -f include/config/auto.conf && echo "auto.conf: OK" || echo "auto.conf: MISSING"
test -f scripts/mod/modpost && echo "modpost: OK" || echo "modpost: MISSING"
test -f scripts/sign-file && echo "sign-file: OK" || echo "sign-file: MISSING"

echo ""
echo "=== Build RTL8821AU driver ==="
cd ${WORKDIR}/8821au-20210708
make clean 2>/dev/null || true

echo "Compiling..."
make ARCH=x86_64 KSRC="${WORKDIR}/linux-${KVER_BASE}" 2>&1 | tail -50

echo ""
echo "=== Result ==="
if [ -f 8821au.ko ]; then
    echo "SUCCESS: 8821au.ko built!"
    ls -la 8821au.ko
    modinfo 8821au.ko 2>/dev/null | head -15
else
    echo "Checking for .ko files..."
    find . -name '*.ko' -type f 2>/dev/null
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(900)
chan.exec_command(f"cat > /root/build-v4.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/build-v4.sh 2>&1")

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
