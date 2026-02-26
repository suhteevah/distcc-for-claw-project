import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# First unload the 8821cu we loaded (wrong chip)
print("=== Unloading wrong 8821cu driver ===")
print(run("rmmod rtw88_8821cu rtw88_8821c 2>&1"))

# Check the actual source code
print("=== Checking devm_kmemdup_array usage ===")
print(run("cd /root/wifi-build/rtw88 && grep -n 'devm_kmemdup_array' main.c"))

print("\n=== Context around the calls ===")
print(run("cd /root/wifi-build/rtw88 && sed -n '1765,1790p' main.c"))

# Apply fix - replace devm_kmemdup_array with a compat version
print("\n=== Applying compat fix ===")
patch = run("""
cd /root/wifi-build/rtw88

# First reset the file to original
git checkout main.c 2>&1

# Now look at the function signature we need to replace
grep -n 'devm_kmemdup_array' main.c

# Create a compat header
cat > compat.h << 'COMPAT_EOF'
#ifndef __RTW88_COMPAT_H
#define __RTW88_COMPAT_H

#include <linux/version.h>

#if LINUX_VERSION_CODE < KERNEL_VERSION(6, 13, 0)
/* devm_kmemdup_array was added in 6.13 */
#include <linux/device.h>
#include <linux/slab.h>

static inline void *devm_kmemdup_array(struct device *dev, const void *src,
                                        size_t n, size_t size, gfp_t flags)
{
    return devm_kmemdup(dev, src, n * size, flags);
}
#endif

#endif /* __RTW88_COMPAT_H */
COMPAT_EOF

echo "Created compat.h"

# Add include to main.c after the last #include
# Find the last include line number
LAST_INCLUDE=$(grep -n '^#include' main.c | tail -1 | cut -d: -f1)
echo "Last #include at line $LAST_INCLUDE"

# Insert our compat include after it
sed -i "${LAST_INCLUDE}a\\#include \\"compat.h\\"" main.c

echo "Patched main.c"
grep -n 'compat.h' main.c
""")
print(patch)

# Rebuild
print("\n=== Rebuilding rtw88 ===")
result = run("""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -50
""", timeout=300)
print(result)

# Check built modules
print("\n=== Built modules ===")
print(run("cd /root/wifi-build/rtw88 && find . -name '*.ko' -type f"))

# Check for 8821au specifically
print("\n=== Check for 8821au module ===")
print(run("cd /root/wifi-build/rtw88 && ls -la rtw88_8821a*.ko 2>/dev/null || echo 'No 8821a modules found'"))
print(run("cd /root/wifi-build/rtw88 && ls -la *.ko 2>/dev/null"))

# Check sizes
print("\n=== Size check ===")
print(run("""
cd /root/wifi-build/rtw88
for ko in $(find . -name '*.ko' -type f); do
    SIZE=$(objdump -h "$ko" | grep this_module | awk '{print $3}')
    echo "$ko: this_module=$SIZE"
done
echo ""
echo "Reference: 00000580"
"""))

client.close()
print("\n=== DONE ===")
