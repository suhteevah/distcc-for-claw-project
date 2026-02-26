import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Check if BTF is available
print("=== 1. BTF availability ===")
print(run(r"""
ls -la /sys/kernel/btf/vmlinux 2>/dev/null && echo "BTF available!" || echo "No BTF"
zcat /proc/config.gz 2>/dev/null | grep -i BTF || echo "No /proc/config.gz"
"""))

# 2. Try bpftool
print("\n=== 2. bpftool btf dump ===")
print(run(r"""
which bpftool 2>/dev/null && bpftool btf dump file /sys/kernel/btf/vmlinux format c 2>/dev/null | grep -A30 'struct usb_host_endpoint {' || echo "bpftool not available or BTF not readable"
"""))

# 3. Try pahole
print("\n=== 3. pahole ===")
print(run(r"""
which pahole 2>/dev/null && pahole -C usb_host_endpoint /sys/kernel/btf/vmlinux 2>/dev/null || echo "pahole not available"
"""))

# 4. Write kernel module to dump raw memory of endpoint array
print("\n=== 4. Raw memory dump module ===")
run(r"""cat > /tmp/ep_dump.c << 'EOF'
#include <linux/module.h>
#include <linux/usb.h>
#include <linux/kernel.h>

/* This module finds the 8821au USB device and dumps raw memory
 * around the endpoint array to determine the actual stride */

static int __init ep_dump_init(void)
{
    struct usb_device *udev;
    struct usb_interface *intf;
    struct usb_host_interface *hostif;
    unsigned char *raw;
    int i;

    pr_info("ep_dump: compiled sizeof(usb_host_endpoint) = %zu\n",
            sizeof(struct usb_host_endpoint));

    /* Find the device by iterating USB buses */
    udev = usb_find_device(0x2357, 0x0120);
    if (!udev) {
        pr_info("ep_dump: device 2357:0120 not found\n");
        return -ENODEV;
    }

    pr_info("ep_dump: found device %s\n", dev_name(&udev->dev));

    intf = usb_ifnum_to_if(udev, 0);
    if (!intf) {
        pr_info("ep_dump: no interface 0\n");
        usb_put_dev(udev);
        return -ENODEV;
    }

    hostif = &intf->altsetting[0];
    pr_info("ep_dump: bNumEndpoints = %d\n", hostif->desc.bNumEndpoints);

    /* Dump raw bytes starting from the endpoint array */
    raw = (unsigned char *)hostif->endpoint;

    /* Dump first 1024 bytes of the endpoint array in 16-byte rows */
    for (i = 0; i < 1024; i += 16) {
        pr_info("ep_dump: +%04d: %02x %02x %02x %02x %02x %02x %02x %02x  %02x %02x %02x %02x %02x %02x %02x %02x\n",
                i,
                raw[i+0], raw[i+1], raw[i+2], raw[i+3],
                raw[i+4], raw[i+5], raw[i+6], raw[i+7],
                raw[i+8], raw[i+9], raw[i+10], raw[i+11],
                raw[i+12], raw[i+13], raw[i+14], raw[i+15]);
    }

    usb_put_dev(udev);
    return -EINVAL; /* Don't actually load */
}

module_init(ep_dump_init);
MODULE_LICENSE("GPL");
EOF

cat > /tmp/Makefile << 'EOF'
obj-m := ep_dump.o
EOF
""")

print(run(r"""
cd /tmp
make -C /root/wifi-build/linux-6.12 M=/tmp modules KBUILD_MODPOST_WARN=1 2>&1 | tail -5
if [ -f /tmp/ep_dump.ko ]; then
    echo "Module built OK"
    insmod /tmp/ep_dump.ko 2>/dev/null
    dmesg | grep 'ep_dump' | tail -80
    rmmod ep_dump 2>/dev/null
else
    echo "Build failed"
fi
rm -f /tmp/ep_dump.* /tmp/Makefile /tmp/.ep_dump* /tmp/Module.symvers /tmp/modules.order 2>/dev/null
""", timeout=120))

# 5. Check kernel config for any SUSE-specific USB config
print("\n=== 5. Kernel USB config ===")
print(run(r"zcat /proc/config.gz 2>/dev/null | grep -i 'USB_MON\|USB_DEBUG\|USB_XHCI_HCD_DEBUGGING\|USB_EHCI_HCD\|KASAN\|KCSAN\|KMSAN\|LOCKDEP\|PROVE_LOCKING\|DEBUG_OBJECTS\|SPINLOCK_LOCK' | head -20"))

# 6. Check if there's a vmlinux with debug info
print("\n=== 6. Debug symbols ===")
print(run(r"""
ls -la /boot/vmlinux-$(uname -r) 2>/dev/null | head -1
ls -la /usr/lib/debug/boot/vmlinux-$(uname -r) 2>/dev/null | head -1
echo "No debug vmlinux" 2>/dev/null
"""))

client.close()
print("\n=== DONE ===")
