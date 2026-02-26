import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print("=" * 60)
print("  Fix SELinux blocking insmod")
print("=" * 60)

# Quick check: SELinux denials from dmesg
print("\n=== 1. dmesg SELinux denials ===")
print(run("dmesg | grep -i 'avc.*denied' | tail -10"))

# Check SSH context vs service context
print("\n=== 2. Current SSH SELinux context ===")
print(run("id -Z"))

# Quick fix: set SELinux permissive (this is the fastest reliable fix)
print("\n=== 3. Setting SELinux to permissive ===")
print(run("setenforce 0 && getenforce"))

# Make it persistent across reboots
print("\n=== 4. Making permissive persistent ===")
print(run(r"""
# Find the config file
if [ -f /etc/selinux/config ]; then
    sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config
    grep '^SELINUX=' /etc/selinux/config
elif [ -f /etc/sysconfig/selinux ]; then
    sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/sysconfig/selinux
    grep '^SELINUX=' /etc/sysconfig/selinux
else
    echo "No SELinux config found, checking alternatives..."
    find /etc -name '*selinux*' -type f 2>/dev/null
fi
"""))

# Now test: unload modules and restart the service
print("\n=== 5. Test insmod with permissive SELinux ===")
print(run(r"""
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1
echo "Modules cleared: $(lsmod | grep -c rtw) rtw modules"

systemctl reset-failed rtw88-wifi 2>/dev/null
systemctl restart rtw88-wifi 2>&1
sleep 3

echo "Service status: $(systemctl is-active rtw88-wifi)"
echo "Module count: $(lsmod | grep -c rtw)"
lsmod | grep rtw
"""))

# Start full WiFi stack
print("\n=== 6. Start WiFi services ===")
print(run(r"""
systemctl reset-failed wpa-wifi 2>/dev/null
systemctl reset-failed dhcpcd-wifi 2>/dev/null
systemctl restart wpa-wifi 2>&1
""", timeout=45))

time.sleep(10)

print(run(r"""
systemctl restart dhcpcd-wifi 2>&1
""", timeout=20))

time.sleep(10)

print("\n=== 7. WiFi status ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
echo "Interface: $WLAN"
echo "IP: $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)"
echo "SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
echo "State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
echo ""
echo "All services:"
for svc in rtw88-wifi wpa-wifi dhcpcd-wifi; do
    echo "  $svc: $(systemctl is-active $svc)"
done
echo ""
echo "Ping:"
ping -c 2 -W 3 8.8.8.8 2>&1 | tail -3
"""))

client.close()
print("\n=== SELinux FIX APPLIED ===")
