import paramiko
import sys
import io

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
print("  Diagnose insmod Permission Denied during boot")
print("=" * 60)

# 1. Secure Boot status
print("\n=== 1. Secure Boot status ===")
print(run(r"""
# Check EFI secure boot variable
mokutil --sb-state 2>&1 || echo "mokutil not available"
# Alternative check
cat /sys/firmware/efi/efivars/SecureBoot-* 2>/dev/null | xxd | head -3
# Or simpler
dmesg | grep -i 'secure boot\|secureboot' | head -5
"""))

# 2. Kernel lockdown
print("\n=== 2. Kernel lockdown ===")
print(run(r"""
cat /sys/kernel/security/lockdown 2>/dev/null || echo "lockdown file not found"
dmesg | grep -i 'lockdown' | head -5
"""))

# 3. SELinux/AppArmor
print("\n=== 3. Security modules ===")
print(run(r"""
getenforce 2>&1 || echo "SELinux not available"
cat /sys/kernel/security/lsm 2>/dev/null || echo "no LSM info"
apparmor_status 2>&1 | head -5 || echo "AppArmor not available"
"""))

# 4. Module signing config
print("\n=== 4. Module signing kernel config ===")
print(run(r"""
# Check compiled-in kernel config
for opt in MODULE_SIG MODULE_SIG_FORCE MODULE_SIG_ALL LOCK_DOWN_KERNEL LOCK_DOWN_KERNEL_FORCE_INTEGRITY LOCK_DOWN_KERNEL_FORCE_CONFIDENTIALITY; do
    VAL=$(cat /boot/config-$(uname -r) 2>/dev/null | grep "CONFIG_${opt}=" || zcat /proc/config.gz 2>/dev/null | grep "CONFIG_${opt}=")
    echo "  $opt: ${VAL:-not found}"
done
"""))

# 5. dmesg around boot for module loading
print("\n=== 5. dmesg for module/insmod/lockdown ===")
print(run("dmesg | grep -iE 'lockdown|module.*sig|insmod|unsigned|verification|PKCS' | head -15"))

# 6. Test insmod NOW (post-boot, should work)
print("\n=== 6. Manual insmod test (post-boot) ===")
print(run(r"""
# First verify modules aren't loaded
lsmod | grep rtw && echo "Already loaded" || echo "Not loaded, testing insmod..."
cd /root/wifi-build/rtw88
insmod ./rtw_core.ko 2>&1
echo "Exit code: $?"
lsmod | grep rtw_core && echo "rtw_core loaded OK" || echo "rtw_core FAILED to load"
# Clean up
rmmod rtw_core 2>/dev/null
"""))

# 7. Check if insmod works with absolute path
print("\n=== 7. Absolute path insmod test ===")
print(run(r"""
insmod /root/wifi-build/rtw88/rtw_core.ko 2>&1
echo "Exit code: $?"
lsmod | grep rtw_core && echo "rtw_core loaded OK" || echo "rtw_core FAILED"
rmmod rtw_core 2>/dev/null
"""))

# 8. Check service execution context
print("\n=== 8. rtw88-wifi service full journal ===")
print(run("journalctl -u rtw88-wifi -b --no-pager 2>&1"))

# 9. Check if modprobe would work for our modules
print("\n=== 9. Can we use modprobe instead? ===")
print(run(r"""
echo "Kernel module path:"
ls -la /usr/lib/modules/$(uname -r)/ 2>/dev/null | head -5
echo ""
echo "Is it read-only?"
touch /usr/lib/modules/$(uname -r)/test_write 2>&1 || echo "YES - read-only filesystem"
rm -f /usr/lib/modules/$(uname -r)/test_write 2>/dev/null
echo ""
echo "depmod location:"
which depmod
echo ""
# Check for overlayfs or writable paths
mount | grep modules
echo ""
echo "Module search path:"
modprobe -vn rtw_core 2>&1 | head -5 || echo "rtw_core not found by modprobe"
"""))

client.close()
print("\n=== DIAGNOSTIC COMPLETE ===")
