# 05 — Module Installation on Leap Micro

## The Immutable Filesystem Challenge

On Leap Micro, `/usr/lib/modules/` is part of the read-only root filesystem. You cannot simply `cp` a module file there. All filesystem modifications go through `transactional-update`.

## Install the Module

```bash
# Use transactional-update shell to modify the filesystem in a new snapshot
transactional-update shell <<'INSTALL_EOF'
# Copy the compiled driver
mkdir -p /usr/lib/modules/$(uname -r)/updates/
cp /root/wifi-build/8821au-20210708/8821au.ko /usr/lib/modules/$(uname -r)/updates/

# Auto-load on boot
echo '8821au' > /etc/modules-load.d/8821au.conf

# Auto-load when USB device is plugged in (udev rule)
cat > /etc/udev/rules.d/99-wifi-8821au.rules << 'UDEV'
# TP-Link Archer T2U PLUS (RTL8821AU)
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="2357", ATTR{idProduct}=="0120", RUN+="/sbin/modprobe 8821au"
UDEV

# Update module dependencies
depmod -a
INSTALL_EOF

# Reboot to activate the new snapshot
reboot
```

## Load the Module (Without Reboot)

If you want to test before committing to a reboot, you can load from the build directory:

```bash
# Load cfg80211 first (wireless subsystem)
modprobe cfg80211

# Load the driver
insmod /root/wifi-build/8821au-20210708/8821au.ko
```

## Verify

```bash
# Check module is loaded
lsmod | grep 8821au

# Check for WiFi interface
ip link show | grep wlan

# Check USB device detection
lsusb | grep "2357:0120"

# Check dmesg for driver messages
dmesg | grep -i "rtl\|8821\|wlan"
```

## Module Path on Leap Micro

On Leap Micro (and MicroOS), the module path is:
- `/usr/lib/modules/$(uname -r)/` — the real path
- `/lib/modules/$(uname -r)/` — symlink to the above

The `updates/` subdirectory takes priority over `kernel/` modules, ensuring our driver is preferred even if a conflicting one exists.
