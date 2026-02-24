import paramiko
import sys
import time

host = "10.0.0.6"
username = "root"
password = "cnc-server-2024!"

print("Waiting 35s for reboot...")
time.sleep(35)

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

# Verify headers are in place
stdin, stdout, stderr = client.exec_command("ls /usr/include/gelf.h /usr/include/libelf.h 2>&1", timeout=10)
print("Headers check:", stdout.read().decode().strip())

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
KVER_BASE=6.12
WORKDIR=/root/wifi-build

echo "=== Verify gelf.h is accessible ==="
ls -la /usr/include/gelf.h /usr/include/libelf.h

echo ""
echo "=== Prepare kernel build ==="
cd ${WORKDIR}/linux-${KVER_BASE}
cp "/lib/modules/${KVER}/config" .config
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

echo "make olddefconfig..."
make olddefconfig 2>&1 | tail -3

echo ""
echo "make modules_prepare..."
make modules_prepare 2>&1 | tail -20

echo ""
echo "=== Check critical build artifacts ==="
test -f tools/objtool/objtool && echo "objtool: OK" || echo "objtool: MISSING"
test -f scripts/mod/modpost && echo "modpost: OK" || echo "modpost: MISSING"
test -f scripts/sign-file && echo "sign-file: OK" || echo "sign-file: MISSING"
test -f include/generated/uapi/linux/version.h && echo "version.h: OK" || echo "version.h: MISSING"
test -f include/config/auto.conf && echo "auto.conf: OK" || echo "auto.conf: MISSING"

echo ""
echo "=== Build RTL8821AU WiFi driver ==="
cd ${WORKDIR}/8821au-20210708
make clean 2>/dev/null || true

echo "Compiling 8821au driver (this takes a few minutes)..."
make ARCH=x86_64 KSRC="${WORKDIR}/linux-${KVER_BASE}" 2>&1 | tail -60

echo ""
echo "=== Result ==="
if [ -f 8821au.ko ]; then
    echo "SUCCESS: 8821au.ko built!"
    ls -la 8821au.ko
    modinfo 8821au.ko 2>/dev/null | head -15
else
    find . -name '*.ko' -type f 2>/dev/null
    echo ""
    echo "Build failed. Showing last errors..."
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(900)
chan.exec_command(f"cat > /root/build-final.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/build-final.sh 2>&1")

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
