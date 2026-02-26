import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Check what SUSE exports for the problem symbols
print("=== Check SUSE kernel symbol exports ===")
print(run("""
KVER=$(uname -r)
# Check debugfs
grep debugfs_create_file /usr/lib/modules/$KVER/Module.symvers | head -5
echo "---"
# Check NAPI
grep napi_add /usr/lib/modules/$KVER/Module.symvers | head -5
echo "---"
grep napi_del /usr/lib/modules/$KVER/Module.symvers | head -5
"""))

# Fix 1: Disable debugfs in the build (not needed for WiFi)
# Fix 2: Disable NAPI in PCI driver (we don't need PCI anyway)
print("\n=== Applying fixes ===")
print(run("""
cd /root/wifi-build/rtw88

# Check Makefile for debugfs and NAPI options
grep -n 'DEBUG\|NAPI\|PCI\|SDIO' Makefile | head -20

# Check if there are config options we can disable
grep -rn 'CONFIG_RTW88_DEBUG' Makefile 2>/dev/null
"""))

# Modify build to skip PCI/SDIO modules and fix debugfs
print("\n=== Modifying Makefile ===")
print(run("""
cd /root/wifi-build/rtw88

# Check current Makefile structure
head -60 Makefile
"""))

print("\n=== Building only USB modules ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null

# Method: Build with debugfs disabled and skip PCI/SDIO modules
# First, let's check if we can just build specific modules
# The Makefile should have CONFIG options

# Disable debugfs to fix the debugfs_create_file error
# Disable PCI to skip NAPI errors (we only need USB)
# Add EXTRA_CFLAGS to handle missing symbols

cat > /root/wifi-build/rtw88/compat_napi.h << 'NAPI_EOF'
#ifndef __RTW88_COMPAT_NAPI_H
#define __RTW88_COMPAT_NAPI_H

/* SUSE kernel 6.12 exports _locked variants of NAPI functions */
#include <linux/netdevice.h>

#ifndef netif_napi_add_weight
/* If the symbol isn't available, try the _locked variant */
#define netif_napi_add_weight(dev, napi, poll, weight) \
    netif_napi_add_weight_locked(dev, napi, poll, weight)
#endif

#ifndef __netif_napi_del
#define __netif_napi_del(napi) napi_disable(napi)
#endif

#endif
NAPI_EOF

# Build with DEBUG disabled and only USB-relevant modules
make KSRC="/root/wifi-build/linux-6.12" \
     CONFIG_RTW88_DEBUG=n \
     CONFIG_RTW88_DEBUGFS=n \
     EXTRA_CFLAGS="-DCONFIG_RTW88_DEBUGFS= -include /root/wifi-build/rtw88/compat_napi.h" \
     2>&1 | tail -60
""", timeout=300)
print(result)

# Check results
print("\n=== Check for built modules ===")
print(run("""
cd /root/wifi-build/rtw88
echo "All .ko files:"
find . -name '*.ko' -type f 2>/dev/null
echo ""
echo "8821au specifically:"
ls -la rtw_8821au.ko 2>/dev/null || echo "NOT FOUND"
ls -la rtw_8821a.ko 2>/dev/null || echo "NOT FOUND"
"""))

# Check sizes
print("\n=== Module sizes ===")
print(run("""
cd /root/wifi-build/rtw88
for ko in $(find . -name '*.ko' -type f 2>/dev/null); do
    SIZE=$(objdump -h "$ko" | grep this_module | awk '{print $3}')
    echo "$ko: this_module=$SIZE"
done
echo "Required: 00000580"
"""))

client.close()
print("\n=== DONE ===")
