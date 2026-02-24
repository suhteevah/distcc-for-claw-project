import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

WORKDIR=/root/wifi-build

echo "=== Check NAPI config in driver ==="
grep -r 'CONFIG_RTW_NAPI\|NAPI' ${WORKDIR}/8821au-20210708/Makefile | head -10
grep -r 'CONFIG_RTW_NAPI\|NAPI' ${WORKDIR}/8821au-20210708/include/autoconf.h 2>/dev/null | head -10

echo ""
echo "=== Check what NAPI symbols the running kernel exports ==="
zcat /lib/modules/$(uname -r)/symvers.gz | grep -i napi | head -20

echo ""
echo "=== Check the NAPI functions in the vanilla source ==="
grep -r 'netif_napi_add_weight\|__netif_napi_del' ${WORKDIR}/linux-6.12/include/linux/netdevice.h | head -5

echo ""
echo "=== Check if driver has a NAPI disable option ==="
grep -n 'NAPI' ${WORKDIR}/8821au-20210708/Makefile | head -10

echo ""
echo "=== Try disabling NAPI in the driver and rebuilding ==="
cd ${WORKDIR}/8821au-20210708

# Check the Makefile for NAPI toggle
grep -n 'CONFIG_RTW_NAPI' Makefile | head -5

# Disable NAPI
sed -i 's/CONFIG_RTW_NAPI = y/CONFIG_RTW_NAPI = n/' Makefile
sed -i 's/CONFIG_RTW_GRO = y/CONFIG_RTW_GRO = n/' Makefile

echo "After sed:"
grep 'CONFIG_RTW_NAPI\|CONFIG_RTW_GRO' Makefile | head -5

echo ""
echo "=== Rebuild with NAPI disabled ==="
make clean 2>/dev/null || true
make ARCH=x86_64 KSRC="${WORKDIR}/linux-6.12" 2>&1 | tail -20

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
chan.settimeout(600)
chan.exec_command(f"cat > /root/fix-napi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-napi.sh 2>&1")

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
