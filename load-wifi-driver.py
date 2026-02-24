import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# The struct module size now matches! But cfg80211 symbols are missing.
# We need to load cfg80211 before loading 8821au.
script = r"""#!/bin/bash
set -e

echo "=== Load cfg80211 wireless subsystem first ==="
modprobe cfg80211 2>&1 || echo "cfg80211 modprobe failed"
lsmod | grep cfg80211 || echo "cfg80211 not loaded"

echo ""
echo "=== Check if cfg80211 is available ==="
find /usr/lib/modules/$(uname -r) -name 'cfg80211*' 2>/dev/null
find /lib/modules/$(uname -r) -name 'cfg80211*' 2>/dev/null

echo ""
echo "=== Try loading cfg80211 explicitly ==="
if [ -f /usr/lib/modules/$(uname -r)/kernel/net/wireless/cfg80211.ko.zst ]; then
    echo "Found cfg80211.ko.zst - loading..."
    modprobe cfg80211 2>&1 || insmod /usr/lib/modules/$(uname -r)/kernel/net/wireless/cfg80211.ko 2>&1 || {
        # Maybe it needs decompression
        zstd -d /usr/lib/modules/$(uname -r)/kernel/net/wireless/cfg80211.ko.zst -o /tmp/cfg80211.ko -f 2>/dev/null
        insmod /tmp/cfg80211.ko 2>&1 || echo "Even manual insmod failed"
    }
elif [ -f /usr/lib/modules/$(uname -r)/kernel/net/wireless/cfg80211.ko ]; then
    echo "Found cfg80211.ko - loading..."
    modprobe cfg80211 2>&1 || insmod /usr/lib/modules/$(uname -r)/kernel/net/wireless/cfg80211.ko 2>&1
fi

echo ""
echo "=== Verify cfg80211 loaded ==="
lsmod | grep cfg80211

echo ""
echo "=== Now load 8821au driver ==="
cd /root/wifi-build/8821au-20210708
insmod 8821au.ko 2>&1 || echo "insmod 8821au failed"

echo ""
echo "=== Check dmesg ==="
dmesg | tail -20

echo ""
echo "=== Check for WiFi interface ==="
ip link show 2>/dev/null
echo ""
iw dev 2>/dev/null || true
echo ""
iwconfig 2>/dev/null || true

echo ""
echo "=== Check USB devices ==="
lsusb | grep -i "tp-link\|realtek\|2357\|0bda" || echo "No matching USB devices"
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/load-wifi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/load-wifi.sh 2>&1")

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
