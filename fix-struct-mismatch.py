import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Check what's at the default kernel build path
print("=== 1. Default kernel build path ===")
print(run(r"""
ls -la /lib/modules/$(uname -r)/build
echo ""
ls -la /lib/modules/$(uname -r)/source 2>/dev/null || echo "No source symlink"
"""))

# 2. Check if the SUSE headers have Module.symvers
print("\n=== 2. SUSE Module.symvers ===")
print(run(r"""
KBUILD=/lib/modules/$(uname -r)/build
if [ -f "$KBUILD/Module.symvers" ]; then
    echo "Module.symvers found at $KBUILD/Module.symvers"
    wc -l "$KBUILD/Module.symvers"
    head -3 "$KBUILD/Module.symvers"
else
    echo "No Module.symvers at $KBUILD"
fi
"""))

# 3. Compare usb_host_endpoint struct between build trees
print("\n=== 3. usb_host_endpoint struct comparison ===")
print("--- Custom build tree ---")
print(run(r"grep -A20 'struct usb_host_endpoint {' /root/wifi-build/linux-6.12/include/linux/usb.h"))
print("\n--- SUSE kernel headers ---")
print(run(r"""
KBUILD=/lib/modules/$(uname -r)/build
grep -A20 'struct usb_host_endpoint {' $KBUILD/include/linux/usb.h 2>/dev/null || echo "Not found in build headers"
"""))

# 4. Check if SUSE has additional fields
print("\n=== 4. usb_host_interface struct ===")
print("--- Custom ---")
print(run(r"grep -A15 'struct usb_host_interface {' /root/wifi-build/linux-6.12/include/linux/usb.h"))
print("\n--- SUSE ---")
print(run(r"""
KBUILD=/lib/modules/$(uname -r)/build
grep -A15 'struct usb_host_interface {' $KBUILD/include/linux/usb.h 2>/dev/null
"""))

# 5. Check SUSE build dir contents
print("\n=== 5. SUSE build dir contents ===")
print(run(r"""
KBUILD=/lib/modules/$(uname -r)/build
echo "Build dir type:"
file $KBUILD 2>/dev/null
echo ""
echo "Key files present:"
for f in .config Makefile Module.symvers Kconfig include/generated/autoconf.h include/config/auto.conf; do
    [ -f "$KBUILD/$f" ] && echo "  $f: YES" || echo "  $f: NO"
done
echo ""
echo "Includes:"
ls $KBUILD/include/ 2>/dev/null
echo ""
echo "Scripts:"
ls $KBUILD/scripts/ 2>/dev/null | head -20
"""))

# 6. Try a test build against SUSE headers
print("\n=== 6. Quick sizeof comparison ===")
print(run(r"""
# Check sizeof in custom tree
cat > /tmp/check_sizes.c << 'EOF'
#include <linux/module.h>
#include <linux/usb.h>

static int __init check_init(void)
{
    pr_info("sizeof(usb_host_endpoint) = %zu\n", sizeof(struct usb_host_endpoint));
    pr_info("sizeof(usb_endpoint_descriptor) = %zu\n", sizeof(struct usb_endpoint_descriptor));
    pr_info("sizeof(usb_host_interface) = %zu\n", sizeof(struct usb_host_interface));
    pr_info("sizeof(usb_interface_descriptor) = %zu\n", sizeof(struct usb_interface_descriptor));
    return -EINVAL;
}
module_init(check_init);
MODULE_LICENSE("GPL");
EOF

cat > /tmp/check_sizes_Makefile << 'EOF'
obj-m := check_sizes.o
EOF

# Build against custom tree
cd /tmp
cp check_sizes_Makefile Makefile
echo "=== Custom tree sizes ==="
make -C /root/wifi-build/linux-6.12 M=/tmp modules KBUILD_MODPOST_WARN=1 2>&1 | grep -v Warning | tail -5
if [ -f /tmp/check_sizes.ko ]; then
    insmod /tmp/check_sizes.ko 2>/dev/null
    dmesg | grep 'sizeof' | tail -10
    rmmod check_sizes 2>/dev/null
    rm -f /tmp/check_sizes.ko
fi

# Build against SUSE tree
echo ""
echo "=== SUSE tree sizes ==="
rm -f /tmp/check_sizes.o /tmp/check_sizes.ko /tmp/check_sizes.mod* /tmp/.check_sizes* /tmp/Module.symvers /tmp/modules.order 2>/dev/null
make -C /lib/modules/$(uname -r)/build M=/tmp modules 2>&1 | grep -v Warning | tail -5
if [ -f /tmp/check_sizes.ko ]; then
    insmod /tmp/check_sizes.ko 2>/dev/null
    dmesg | grep 'sizeof' | tail -10
    rmmod check_sizes 2>/dev/null
    rm -f /tmp/check_sizes.ko
fi
rm -f /tmp/check_sizes.* /tmp/Makefile /tmp/.check_sizes* /tmp/Module.symvers /tmp/modules.order 2>/dev/null
""", timeout=120))

client.close()
print("\n=== DONE ===")
