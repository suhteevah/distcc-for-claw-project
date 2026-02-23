import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Write a script to the remote machine and execute it
script = """#!/bin/bash
KVER=$(uname -r)
echo "Kernel: $KVER"
echo ""
echo "=== Wireless driver modules ==="
ls /lib/modules/$KVER/kernel/drivers/net/wireless/ 2>&1
echo ""
echo "=== Searching for rtw/rtl88/8821 modules ==="
find /lib/modules/$KVER -name '*8821*' -o -name '*rtw88*' -o -name '*rtl88*' -o -name '*rtw89*' -o -name '*rtw_usb*' -o -name '*rtw_core*' 2>/dev/null
echo ""
echo "=== All wireless-related modules ==="
find /lib/modules/$KVER/kernel/drivers/net/wireless/ -name '*.ko*' 2>/dev/null | head -30
echo ""
echo "=== Trying modprobe rtw88_8821au ==="
modprobe rtw88_8821au 2>&1 || echo "not found"
echo ""
echo "=== Trying modprobe rtw88_usb ==="
modprobe rtw88_usb 2>&1 || echo "not found"
echo ""
echo "=== Trying modprobe 8821au ==="
modprobe 8821au 2>&1 || echo "not found"
echo ""
echo "=== Current wlan interfaces ==="
ip link show | grep -i wlan
echo ""
echo "=== USB WiFi in dmesg ==="
dmesg | grep -i '2357\|8821\|rtw\|wlan' | tail -10
"""

stdin, stdout, stderr = client.exec_command(f"cat > /tmp/check-wifi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/check-wifi.sh", timeout=30)
out = stdout.read().decode()
err = stderr.read().decode()
print(out, end="")
if err:
    print(err, end="", file=sys.stderr)
client.close()
