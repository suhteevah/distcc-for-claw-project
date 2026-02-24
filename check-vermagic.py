import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
echo "=== Running kernel version ==="
uname -r

echo ""
echo "=== Running kernel vermagic ==="
cat /proc/version

echo ""
echo "=== Module vermagic ==="
modinfo /root/wifi-build/8821au-20210708/8821au.ko | grep -i 'vermagic\|version\|depends'

echo ""
echo "=== Compare with an existing loaded module ==="
modinfo /lib/modules/$(uname -r)/kernel/drivers/net/usb/r8152.ko.zst 2>/dev/null | grep -i 'vermagic\|version' || \
modinfo /lib/modules/$(uname -r)/kernel/drivers/usb/core/usbcore.ko.zst 2>/dev/null | grep -i 'vermagic\|version' || \
echo "Can't find a reference module"

echo ""
echo "=== Check insmod error more carefully ==="
insmod /root/wifi-build/8821au-20210708/8821au.ko 2>&1
dmesg | tail -10
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /root/check-vm.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/check-vm.sh",
    timeout=30
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print("STDERR:", err, end="")
client.close()
