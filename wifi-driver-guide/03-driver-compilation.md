# 03 — RTL8821AU Driver Compilation

## Clone the Driver Source

```bash
cd /root/wifi-build
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
```

## Fix NAPI Symbol Mismatch

The SUSE kernel exports `_locked` variants of NAPI functions that differ from vanilla kernel exports:

| Vanilla Symbol | SUSE Symbol |
|---------------|-------------|
| `netif_napi_add_weight` | `netif_napi_add_weight_locked` |
| `__netif_napi_del` | `__netif_napi_del_locked` |

The simplest fix is to **disable NAPI** in the driver:

```bash
# Disable NAPI and GRO (Generic Receive Offload)
sed -i 's/CONFIG_RTW_NAPI = y/CONFIG_RTW_NAPI = n/' Makefile
sed -i 's/CONFIG_RTW_GRO = y/CONFIG_RTW_GRO = n/' Makefile
```

**Verify:**
```bash
grep 'CONFIG_RTW_NAPI\|CONFIG_RTW_GRO' Makefile
# Should show:
# CONFIG_RTW_NAPI = n
# CONFIG_RTW_GRO = n
```

> **Note:** Disabling NAPI may slightly reduce network performance under heavy load, but the driver will work correctly. For a USB WiFi adapter, this is negligible.

## Build the Driver

```bash
make clean
make ARCH=x86_64 KSRC="/root/wifi-build/linux-6.12"
```

The `KSRC=` parameter is critical — it tells the driver Makefile where to find the kernel source tree, since the normal `/lib/modules/$(uname -r)/build` symlink doesn't exist on Leap Micro.

Expected output (last lines):
```
  LD [M]  /root/wifi-build/8821au-20210708/8821au.o
  MODPOST /root/wifi-build/8821au-20210708/Module.symvers
  CC [M]  /root/wifi-build/8821au-20210708/8821au.mod.o
  CC [M]  /root/wifi-build/8821au-20210708/.module-common.o
  LD [M]  /root/wifi-build/8821au-20210708/8821au.ko
```

## Verify the Module

```bash
ls -la 8821au.ko
# Should be ~7.7 MB

modinfo 8821au.ko | head -15
# Should show USB aliases matching the TP-Link Archer T2U PLUS
```

## What Can Go Wrong

| Error | Cause | Fix |
|-------|-------|-----|
| `flex: not found` during modules_prepare | flex not installed | Install via transactional-update |
| `openssl/opensslv.h: No such file` | openssl headers missing | Install libopenssl-3-devel |
| `gelf.h: No such file` | libelf headers missing | Extract from RPM (see 01-environment-setup.md) |
| `cannot find -lelf` | libelf.so symlink missing | Create: `ln -sf libelf.so.1 /usr/lib64/libelf.so` |
| `undefined symbol: netif_napi_add_weight` | SUSE NAPI symbol names | Disable CONFIG_RTW_NAPI (see above) |
| `.gnu.linkonce.this_module section size must match` | SUSE struct module padding | See [04-struct-module-fix.md](04-struct-module-fix.md) |
