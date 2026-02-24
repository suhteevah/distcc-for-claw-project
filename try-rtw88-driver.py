import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
WORKDIR=/root/wifi-build

echo "=== System status ==="
echo "Kernel: $KVER"
uptime

echo ""
echo "=== Option 1: Check if rtw88 modules already exist in kernel ==="
echo "The SUSE 6.12 kernel may have backported rtw88 USB support..."
find /lib/modules/$KVER -name '*rtw88*' 2>/dev/null
find /usr/lib/modules/$KVER -name '*rtw88*' 2>/dev/null
echo "---"

echo ""
echo "=== Check for rtw88 config options in running kernel ==="
zcat /proc/config.gz | grep -i RTW88 2>/dev/null || echo "No RTW88 config found"

echo ""
echo "=== Try to modprobe rtw88 ==="
modprobe rtw88_8821au 2>&1 || echo "rtw88_8821au not available"
modprobe rtw88_usb 2>&1 || echo "rtw88_usb not available"
modprobe rtw88 2>&1 || echo "rtw88 not available"

echo ""
echo "=== Option 2: Build rtw88 from lwfinger backport repo ==="
echo "If rtw88 is not in kernel, we'll build from https://github.com/lwfinger/rtw88"
cd $WORKDIR

if [ ! -d rtw88 ]; then
    echo "Cloning lwfinger/rtw88..."
    git clone https://github.com/lwfinger/rtw88.git 2>&1 | tail -5
else
    echo "rtw88 repo already exists"
    cd rtw88 && git pull 2>&1 | tail -3 && cd ..
fi

echo ""
echo "=== Check if rtw88 can build against our kernel source ==="
cd $WORKDIR/rtw88
ls -la Makefile 2>/dev/null
head -30 Makefile 2>/dev/null

echo ""
echo "=== Try building rtw88 ==="
make clean 2>/dev/null || true
# Build against our patched kernel source
make KSRC="${WORKDIR}/linux-6.12" 2>&1 | tail -30

echo ""
echo "=== Check built modules ==="
find . -name '*.ko' -type f 2>/dev/null
ls -la rtw88_8821au.ko 2>/dev/null || echo "rtw88_8821au.ko not found"
ls -la rtw88_usb.ko 2>/dev/null || echo "rtw88_usb.ko not found"
ls -la rtw88_core.ko 2>/dev/null || echo "rtw88_core.ko not found"

echo ""
echo "=== Check sizes ==="
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    echo "$ko:"
    objdump -h $ko 2>/dev/null | grep this_module || echo "  no this_module section"
done

echo ""
echo "=== Reference size ==="
zstd -d /lib/modules/${KVER}/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f 2>/dev/null
objdump -h /tmp/r8152.ko | grep this_module

echo ""
echo "=== Try loading rtw88 modules ==="
if [ -f rtw88_core.ko ]; then
    echo "Loading rtw88_core..."
    insmod rtw88_core.ko 2>&1 || true
fi
if [ -f rtw88_usb.ko ]; then
    echo "Loading rtw88_usb..."
    insmod rtw88_usb.ko 2>&1 || true
fi
if [ -f rtw88_8821a.ko ] || [ -f rtw88_8821au.ko ]; then
    ko=$(find . -name 'rtw88_8821a*.ko' -type f | head -1)
    echo "Loading $ko..."
    insmod "$ko" 2>&1 || true
fi

sleep 3

echo ""
echo "=== dmesg after load ==="
dmesg | tail -30

echo ""
echo "=== Loaded modules ==="
lsmod | grep -i 'rtw88\|cfg\|mac80211' || echo "No wifi modules"

echo ""
echo "=== Network interfaces ==="
ip link show 2>/dev/null
iwconfig 2>/dev/null || true
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /root/try-rtw88.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/try-rtw88.sh 2>&1")

output = ""
while True:
    if chan.recv_ready():
        data = chan.recv(4096).decode('utf-8', errors='replace')
        if data:
            output += data
    if chan.exit_status_ready():
        while chan.recv_ready():
            data = chan.recv(4096).decode('utf-8', errors='replace')
            if data:
                output += data
        break

with open("rtw88-output.txt", "w", encoding="utf-8") as f:
    f.write(output)
    f.write(f"\nExit code: {chan.recv_exit_status()}\n")

for line in output.split('\n'):
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'replace').decode('ascii'))

print(f"\nExit code: {chan.recv_exit_status()}")
client.close()
