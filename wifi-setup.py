import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -x

echo "=== Loading rtw88 modules ==="
modprobe rtw88_core 2>&1
modprobe rtw88_usb 2>&1
modprobe rtw88_8821c 2>&1
modprobe rtw88_8821cu 2>&1

sleep 2

echo "=== Check if wlan interface appeared ==="
ip link show | grep -i wlan

echo "=== Check dmesg for rtw88 ==="
dmesg | grep -i rtw88 | tail -10

echo "=== Try connecting WiFi ==="
nmcli dev wifi list 2>&1
echo "=== nmcli device status ==="
nmcli device status 2>&1
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/wifi-setup.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/wifi-setup.sh",
    timeout=30
)
print(stdout.read().decode(), end="")
print(stderr.read().decode(), end="", file=sys.stderr)
client.close()
