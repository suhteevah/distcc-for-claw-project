import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
KVER_BASE=6.12
WORKDIR=/root/wifi-build
EXTRACT=/root/wifi-build/libelf-extract

echo "=== Copy libelf headers using transactional-update shell ==="
# Use transactional-update to install files into the next snapshot
transactional-update --non-interactive --continue shell <<'TUEOF'
# Copy libelf headers into the snapshot
cp /root/wifi-build/libelf-extract/usr/include/gelf.h /usr/include/
cp /root/wifi-build/libelf-extract/usr/include/libelf.h /usr/include/
cp /root/wifi-build/libelf-extract/usr/include/nlist.h /usr/include/
mkdir -p /usr/include/elfutils/
cp /root/wifi-build/libelf-extract/usr/include/elfutils/*.h /usr/include/elfutils/
echo "Headers copied"
ls -la /usr/include/gelf.h /usr/include/libelf.h /usr/include/elfutils/
exit
TUEOF

echo ""
echo "=== Wait, we can't reboot again. Let's try a bind mount or CFLAGS trick ==="
echo "Actually let's just rebuild objtool with custom CFLAGS pointing to our headers"

cd ${WORKDIR}/linux-${KVER_BASE}

# Make sure config is set
cp "/lib/modules/${KVER}/config" .config
zcat "/lib/modules/${KVER}/symvers.gz" > Module.symvers

# Set up include paths for the objtool build
export C_INCLUDE_PATH="${EXTRACT}/usr/include:${C_INCLUDE_PATH}"
export CPLUS_INCLUDE_PATH="${EXTRACT}/usr/include:${CPLUS_INCLUDE_PATH}"

echo "C_INCLUDE_PATH=$C_INCLUDE_PATH"

echo ""
echo "=== Rebuild modules_prepare with custom include path ==="
# Clean objtool and rebuild
rm -rf tools/objtool/objtool tools/objtool/*.o tools/objtool/arch/x86/*.o 2>/dev/null || true

make modules_prepare 2>&1 | tail -20

echo ""
echo "=== Check objtool ==="
ls -la tools/objtool/objtool 2>/dev/null || echo "objtool still not built"

echo ""
echo "=== Build WiFi driver ==="
cd ${WORKDIR}/8821au-20210708
make clean 2>/dev/null || true

echo "Compiling with custom include path..."
make ARCH=x86_64 KSRC="${WORKDIR}/linux-${KVER_BASE}" 2>&1 | tail -50

echo ""
echo "=== Result ==="
if [ -f 8821au.ko ]; then
    echo "SUCCESS: 8821au.ko built!"
    ls -la 8821au.ko
    modinfo 8821au.ko 2>/dev/null | head -15
else
    find . -name '*.ko' -type f 2>/dev/null
    echo "Build failed."
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(900)
chan.exec_command(f"cat > /root/build-v5.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/build-v5.sh 2>&1")

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
