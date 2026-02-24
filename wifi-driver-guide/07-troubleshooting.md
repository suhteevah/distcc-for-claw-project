# 07 — Troubleshooting Guide

## Common Errors and Solutions

### "Invalid module format" / struct module size mismatch

**Error:**
```
module 8821au: .gnu.linkonce.this_module section size must match
the kernel's built struct module size at run time
```

**Cause:** The compiled module's `struct module` size doesn't match the running kernel.

**Diagnosis:**
```bash
# Check our module's this_module section size
objdump -h 8821au.ko | grep this_module

# Check a reference kernel module
zstd -d /usr/lib/modules/$(uname -r)/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f
objdump -h /tmp/r8152.ko | grep this_module
```

**Fix:** Apply the struct module padding patch. See [04-struct-module-fix.md](04-struct-module-fix.md).

---

### "Unknown symbol cfg80211_*"

**Error:**
```
8821au: Unknown symbol cfg80211_unlink_bss (err -2)
8821au: Unknown symbol wiphy_register (err -2)
```

**Cause:** The `cfg80211` wireless subsystem module isn't loaded.

**Fix:**
```bash
modprobe cfg80211
# Then retry insmod
insmod 8821au.ko
```

---

### "Unknown symbol netif_napi_add_weight"

**Error during MODPOST:**
```
ERROR: modpost: "netif_napi_add_weight" undefined!
ERROR: modpost: "__netif_napi_del" undefined!
```

**Cause:** SUSE kernel exports `_locked` variants of NAPI functions.

**Fix:** Disable NAPI in the driver Makefile:
```bash
sed -i 's/CONFIG_RTW_NAPI = y/CONFIG_RTW_NAPI = n/' Makefile
sed -i 's/CONFIG_RTW_GRO = y/CONFIG_RTW_GRO = n/' Makefile
```

---

### Kernel BUG/NULL pointer dereference during insmod

**Error in dmesg:**
```
BUG: unable to handle page fault for address: 000000000001448a
RIP: 0010:device_links_driver_bound+0x163/0x2d0
```

**Cause:** This crash occurs in the kernel's device link management subsystem when the
driver binds to a USB device. The faulting address `0x1448a` is NOT zero — it's a misaligned
offset deep in a structure, suggesting the out-of-tree morrownr driver's `probe()` function
creates a `struct device` with incompatible or uninitialized fields for kernel 6.12.

The `device_links_driver_bound()` function walks `dev->links.consumers` and
`dev->links.suppliers` list_heads. If these aren't properly initialized by the driver's
USB subsystem interaction, a NULL pointer dereference occurs.

**IMPORTANT:** This crash kills sshd and makes the server unreachable remotely. A physical
reboot is required after each crash.

**This is NOT caused by our struct module padding.** The padding correctly matches the
0x580 size and the module loads (appears in lsmod). The crash happens during device binding,
not module initialization.

**Potential fixes:**
1. Try loading the module **without** the USB adapter plugged in, then hot-plug after
2. Use the **lwfinger/rtw88** backport (see "Alternative: In-Kernel rtw88 Driver" below)
3. Check if a newer commit on the morrownr repo fixes the device_links issue
4. Try with `CONFIG_RTW_USB_AUTOSUSPEND = n` in the driver Makefile

### Alternative: In-Kernel rtw88 Driver (Recommended for 6.12+)

Starting with Linux kernel 6.13, an in-kernel mac80211-compliant driver for RTL8821AU
was merged into mainline. For kernel 6.12, a backport is available from
[lwfinger/rtw88](https://github.com/lwfinger/rtw88).

**Why use rtw88 instead of morrownr/8821au:**
- Standards compliant (mac80211) — better integration with Linux WiFi stack
- Actively maintained and heading into mainline
- No NAPI symbol issues (uses standard kernel APIs)
- No `device_links_driver_bound` crash

**Building rtw88 backport:**
```bash
cd /root/wifi-build
git clone https://github.com/lwfinger/rtw88.git
cd rtw88
make KSRC="/root/wifi-build/linux-6.12"

# Load modules in order
insmod rtw88_core.ko
insmod rtw88_usb.ko
insmod rtw88_8821a.ko   # or rtw88_8821au.ko
```

**Note:** The rtw88 modules still need to be built against our patched kernel source
(with the struct module padding fix) to match the SUSE kernel's struct module size.

---

### Build fails: "flex: not found"

```bash
transactional-update --non-interactive pkg install flex bison m4
reboot
```

---

### Build fails: "gelf.h: No such file or directory"

See the libelf-devel manual extraction in [01-environment-setup.md](01-environment-setup.md).

---

### Build fails: "cannot find -lelf"

```bash
# Create the linker symlink
transactional-update shell
ln -sf libelf.so.1 /usr/lib64/libelf.so
exit
reboot
```

---

### `/lib/modules/` is read-only

**Cause:** Leap Micro's immutable root filesystem.

**Fix:** Use `transactional-update shell` for filesystem modifications, or specify `KSRC=` when building:
```bash
make ARCH=x86_64 KSRC="/root/wifi-build/linux-6.12"
```

---

### modprobe says "Module not found in directory"

**Cause:** modprobe looks in `/usr/lib/modules/` (the real path), not `/lib/modules/` (the symlink). Also, `depmod -a` must be run after installing the module.

**Fix:**
```bash
# Install module to the correct path
cp 8821au.ko /usr/lib/modules/$(uname -r)/updates/

# Rebuild module dependencies
depmod -a

# Now modprobe should find it
modprobe 8821au
```

---

### No WiFi interface after module loads

1. Check if USB adapter is connected: `lsusb | grep "2357:0120"`
2. Check dmesg for errors: `dmesg | tail -30`
3. Check if interface was created with different name: `ip link show`
4. Try unloading and reloading: `rmmod 8821au && insmod 8821au.ko`

## Useful Diagnostic Commands

```bash
# Kernel and module info
uname -r
lsmod | grep -E '8821au|cfg80211|rfkill'
modinfo 8821au.ko

# USB info
lsusb -v -d 2357:0120

# Wireless info
iw dev
iw phy
iwconfig

# NetworkManager
nmcli dev status
nmcli connection show
nmcli dev wifi list

# System logs
dmesg | grep -i "8821\|rtl\|wlan\|wifi"
journalctl -k | grep -i "8821\|rtl\|wlan"
```
