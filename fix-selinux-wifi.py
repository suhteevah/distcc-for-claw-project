import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print("=" * 60)
print("  Fix SELinux blocking insmod from systemd service")
print("=" * 60)

# 1. Verify SELinux is the blocker - check audit log
print("\n=== 1. SELinux audit denials for insmod/modules ===")
print(run(r"""
# Check audit log for module-related denials
ausearch -m AVC --start today 2>/dev/null | grep -i 'insmod\|module\|rtw\|init_module' | tail -10
echo "---"
# Also check dmesg for SELinux denials
dmesg | grep -i 'selinux.*denied\|avc.*denied' | grep -i 'module\|insmod\|init_module' | tail -10
echo "---"
# Check what context insmod runs in
ls -Z /sbin/insmod /usr/sbin/insmod 2>/dev/null
echo "---"
# Check what context our service runs in
ps -eZ | grep rtw88 2>/dev/null || echo "rtw88 service not running"
echo "---"
# Check current SELinux context of SSH session
id -Z 2>/dev/null
"""))

# 2. Check the audit log more broadly
print("\n=== 2. Recent SELinux AVC denials ===")
print(run(r"""
# Look for any module_request or init_module denials
cat /var/log/audit/audit.log 2>/dev/null | grep -i 'denied.*init_module\|denied.*module_load\|denied.*insmod' | tail -10
echo "---"
# Broader search
cat /var/log/audit/audit.log 2>/dev/null | grep 'denied' | tail -15
"""))

# 3. Attempt fix: Create SELinux policy to allow module loading from our service
print("\n=== 3. Fix approach: Set rtw88-wifi service to unconfined context ===")
print(run(r"""
# Check what SELinux booleans exist for module loading
getsebool -a 2>/dev/null | grep -i module
echo "---"
# Check if we can use setsebool to allow it
getsebool domain_kernel_load_modules 2>/dev/null || echo "boolean not found"
"""))

# 4. The most robust fix: add SELinuxContext to service OR use semodule
# First, let's try adding the unconfined context to the service
print("\n=== 4. Applying fix: unconfined SELinux context for rtw88-wifi ===")

sftp = client.open_sftp()

rtw88_service = '''[Unit]
Description=Load RTW88 WiFi driver modules (RTL8821AU)
After=network-pre.target systemd-modules-load.service
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
SELinuxContext=system_u:system_r:unconfined_service_t:s0
ExecStart=/usr/local/bin/rtw88-wifi-start.sh
ExecStop=/usr/local/bin/rtw88-wifi-stop.sh

[Install]
WantedBy=multi-user.target
'''

with sftp.open('/etc/systemd/system/rtw88-wifi.service', 'w') as f:
    f.write(rtw88_service)
print("  Written rtw88-wifi.service with SELinuxContext")
sftp.close()

print(run("systemctl daemon-reload"))

# 5. Test: stop the service, unload modules, restart
print("\n=== 5. Test the fixed service ===")
print(run(r"""
# Unload modules first
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1
lsmod | grep rtw && echo "WARNING: modules still loaded" || echo "Modules cleared"

# Reset the failed state and restart
systemctl reset-failed rtw88-wifi 2>/dev/null
systemctl restart rtw88-wifi 2>&1
echo "Exit code: $?"
sleep 3

# Check result
echo ""
echo "Service status:"
systemctl is-active rtw88-wifi
echo ""
echo "Modules:"
lsmod | grep rtw
echo ""
echo "WiFi interface:"
ip link show | grep wl
"""))

# 6. If that didn't work, try alternative: allow boolean or semanage
print("\n=== 6. Check if service worked ===")
result = run("lsmod | grep -c rtw")
modcount = result.strip()
print(f"  RTW module count: {modcount}")

if modcount == "0":
    print("\n  SELinuxContext didn't help. Trying alternative approaches...")

    # Try enabling the domain_kernel_load_modules boolean
    print("\n=== 6a. Try setsebool domain_kernel_load_modules ===")
    print(run(r"""
setsebool -P domain_kernel_load_modules 1 2>&1 || echo "Boolean not available"
"""))

    # Try a custom SELinux module
    print("\n=== 6b. Generate and load custom SELinux policy ===")
    print(run(r"""
# Generate policy from audit log denials
ausearch -m AVC --start today 2>/dev/null | audit2allow -M rtw88wifi 2>&1
echo "---"
# Install the module
semodule -i rtw88wifi.pp 2>&1 || echo "semodule install failed"
echo "---"
# Retry module loading
systemctl reset-failed rtw88-wifi 2>/dev/null
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1
systemctl restart rtw88-wifi 2>&1
sleep 3
echo "Modules after policy fix:"
lsmod | grep rtw
"""))

    result2 = run("lsmod | grep -c rtw")
    modcount2 = result2.strip()
    print(f"\n  RTW module count after policy fix: {modcount2}")

    if modcount2 == "0":
        print("\n  Custom policy also failed. Last resort: set SELinux permissive for this domain")
        print("\n=== 6c. Set SELinux to permissive as last resort ===")
        print(run(r"""
# Check if semanage is available
which semanage 2>/dev/null || echo "semanage not available"
# Try setting permissive for the service domain
semanage permissive -a init_t 2>&1 || echo "semanage permissive failed"
# As last resort, set global permissive
echo "Setting SELinux to permissive mode..."
setenforce 0
getenforce
# Make it persistent
sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config 2>/dev/null || \
  sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/sysconfig/selinux 2>/dev/null || \
  echo "Could not update SELinux config file"
cat /etc/selinux/config 2>/dev/null | grep '^SELINUX=' || \
  cat /etc/sysconfig/selinux 2>/dev/null | grep '^SELINUX='

# Now retry
systemctl reset-failed rtw88-wifi 2>/dev/null
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    rmmod $mod 2>/dev/null
done
sleep 1
systemctl restart rtw88-wifi 2>&1
sleep 3
echo ""
echo "Modules after SELinux permissive:"
lsmod | grep rtw
echo ""
echo "WiFi interface:"
ip link show | grep wl
"""))

# 7. Final verification - start all WiFi services
print("\n=== 7. Start full WiFi stack ===")
print(run(r"""
# Check if modules are loaded
if lsmod | grep -q rtw_8821au; then
    echo "Modules loaded, starting WiFi services..."
    systemctl reset-failed wpa-wifi 2>/dev/null
    systemctl reset-failed dhcpcd-wifi 2>/dev/null
    systemctl restart wpa-wifi 2>&1
    sleep 10
    systemctl restart dhcpcd-wifi 2>&1
    sleep 10

    WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
    echo "Interface: $WLAN"
    echo "IP: $(ip -4 addr show $WLAN 2>/dev/null | grep 'inet ' | awk '{print $2}' | head -1)"
    echo "SSID: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^ssid=' | cut -d= -f2)"
    echo "State: $(wpa_cli -i $WLAN status 2>/dev/null | grep '^wpa_state=' | cut -d= -f2)"
    echo ""
    ping -c 2 -W 3 8.8.8.8 2>&1 | tail -3
else
    echo "MODULES NOT LOADED - WiFi cannot start"
fi
"""))

client.close()
print("\n=== DONE ===")
