import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

KVER=$(uname -r)
WORKDIR=/root/wifi-build
MODDIR="/lib/modules/${KVER}/updates"

echo "=== Step 1: Install the 8821au.ko module ==="
# Use transactional-update shell to install to the immutable filesystem
transactional-update --non-interactive --continue shell <<'TUEOF'
KVER=$(uname -r)
MODDIR="/lib/modules/${KVER}/updates"

# Create the updates directory for extra modules
mkdir -p "${MODDIR}"

# Copy the module
cp /root/wifi-build/8821au-20210708/8821au.ko "${MODDIR}/"
echo "Module copied to ${MODDIR}/"

# Run depmod to update module dependency database
depmod -a "${KVER}"
echo "depmod complete"

# Create modprobe config to auto-load on boot
mkdir -p /etc/modules-load.d/
echo "8821au" > /etc/modules-load.d/8821au.conf
echo "Auto-load config created"

# Also create udev rule for automatic loading when USB device is plugged in
mkdir -p /etc/udev/rules.d/
cat > /etc/udev/rules.d/99-wifi-8821au.rules <<'UDEV'
# TP-Link Archer T2U PLUS (RTL8821AU)
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="2357", ATTR{idProduct}=="0120", RUN+="/sbin/modprobe 8821au"
UDEV
echo "udev rule created"

# Verify
ls -la "${MODDIR}/8821au.ko"
cat /etc/modules-load.d/8821au.conf
cat /etc/udev/rules.d/99-wifi-8821au.rules
exit
TUEOF

echo ""
echo "=== Step 2: Now try loading module directly (before reboot) ==="
# The module might work with insmod even on the current snapshot
# since it's being loaded from the build dir
insmod /root/wifi-build/8821au-20210708/8821au.ko 2>&1 || echo "insmod failed - will work after reboot"

echo ""
echo "=== Step 3: Check if WiFi interface appeared ==="
sleep 3
ip link show 2>&1
echo ""
iwconfig 2>&1 || ip link show | grep -i wlan

echo ""
echo "=== Step 4: Check dmesg for WiFi driver ==="
dmesg | grep -i '8821\|rtl\|wlan\|wifi' | tail -20

echo ""
echo "=== Step 5: Check NetworkManager connections ==="
nmcli device status 2>&1 || true
nmcli connection show 2>&1 || true
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/install-wifi.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/install-wifi.sh 2>&1")

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
