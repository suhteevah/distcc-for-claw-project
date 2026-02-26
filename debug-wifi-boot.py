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
print("  WiFi Boot Persistence - Root Cause Investigation")
print("=" * 60)

# Phase 1: Check rtw88-wifi service journal
print("\n=== 1. rtw88-wifi service journal ===")
print(run("journalctl -u rtw88-wifi --no-pager -n 40 2>&1"))

# Phase 2: Check wpa-wifi service journal
print("\n=== 2. wpa-wifi service journal ===")
print(run("journalctl -u wpa-wifi --no-pager -n 30 2>&1"))

# Phase 3: Check dhcpcd-wifi service journal
print("\n=== 3. dhcpcd-wifi service journal ===")
print(run("journalctl -u dhcpcd-wifi --no-pager -n 20 2>&1"))

# Phase 4: Check current state
print("\n=== 4. Current service status ===")
print(run(r"""
for svc in rtw88-wifi wpa-wifi dhcpcd-wifi; do
    echo "--- $svc ---"
    systemctl status $svc 2>&1 | head -15
    echo ""
done
"""))

# Phase 5: Check if modules are loaded NOW
print("\n=== 5. Current module state ===")
print(run("lsmod | grep -E 'rtw|cfg80211|mac80211' || echo 'NO rtw/wifi modules loaded'"))

# Phase 6: Check if USB device is present
print("\n=== 6. USB device present? ===")
print(run("lsusb | grep -i 2357 || echo 'USB WiFi NOT detected'"))

# Phase 7: Check dmesg for any clues
print("\n=== 7. dmesg for rtw/usb/wifi ===")
print(run("dmesg | grep -i 'rtw\\|8821\\|2357\\|wlan\\|cfg80211\\|mac80211\\|firmware' | tail -25"))

# Phase 8: Check the actual service files for correctness
print("\n=== 8. Current rtw88-wifi.service content ===")
print(run("cat /etc/systemd/system/rtw88-wifi.service"))

# Phase 9: Check if .ko files exist
print("\n=== 9. .ko files present? ===")
print(run(r"""
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "/root/wifi-build/rtw88/${ko}.ko" ]; then
        echo "  $ko.ko: $(ls -la /root/wifi-build/rtw88/${ko}.ko | awk '{print $5}') bytes"
    else
        echo "  $ko.ko: MISSING!"
    fi
done
"""))

# Phase 10: Try manual load NOW to see what happens
print("\n=== 10. Manual module load test ===")
print(run(r"""
echo "Loading cfg80211..."
modprobe cfg80211 2>&1
echo "Loading mac80211..."
modprobe mac80211 2>&1
sleep 1

cd /root/wifi-build/rtw88
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    echo -n "insmod ${mod}.ko... "
    RESULT=$(insmod ./${mod}.ko 2>&1)
    RC=$?
    if [ $RC -eq 0 ]; then
        echo "OK"
    elif echo "$RESULT" | grep -q "File exists"; then
        echo "ALREADY LOADED"
    else
        echo "FAILED($RC): $RESULT"
    fi
done

sleep 3
echo ""
echo "Modules after manual load:"
lsmod | grep rtw
echo ""
echo "WiFi interface:"
ip link show | grep wl
"""))

client.close()
print("\n=== DIAGNOSTIC COMPLETE ===")
