# RTL8821AU WiFi Driver on openSUSE Leap Micro 6.2

Building out-of-tree WiFi drivers on an immutable Linux distribution with a SUSE-patched kernel — the hard way, fully documented.

## The Problem

openSUSE Leap Micro 6.2 (and SLE Micro) ships a SUSE-patched kernel `6.12.0-160000.x-default` but **does not include `kernel-default-devel`** in its repositories. This means you cannot build kernel modules the normal way.

The TP-Link Archer T2U PLUS (RTL8821AU chipset, USB ID `2357:0120`) has no in-tree driver, requiring an out-of-tree build from [morrownr/8821au-20210708](https://github.com/morrownr/8821au-20210708).

## What Makes This Hard

1. **Immutable root filesystem** — packages install via `transactional-update` into btrfs snapshots, requiring reboots
2. **No kernel-default-devel** — the Leap Micro 6.2 repos don't ship it for the 6.12.0 kernel
3. **SUSE-patched kernel** — the kernel has `CONFIG_LIVEPATCH_IPA_CLONES=y` which adds 64 bytes to `struct module`, making modules built against vanilla kernel sources incompatible
4. **Dependency hell** — build tools (flex, bison, libelf-devel, openssl-devel) have version conflicts between Leap Micro and Leap 15.6 repos
5. **NAPI symbol mismatch** — SUSE exports `_locked` variants of NAPI functions (`netif_napi_add_weight_locked` instead of `netif_napi_add_weight`)

## Documentation

| Document | Description |
|----------|-------------|
| [01-environment-setup.md](01-environment-setup.md) | Setting up the build toolchain on Leap Micro |
| [02-kernel-source-preparation.md](02-kernel-source-preparation.md) | Preparing vanilla kernel source for module building |
| [03-driver-compilation.md](03-driver-compilation.md) | Compiling the RTL8821AU driver |
| [04-struct-module-fix.md](04-struct-module-fix.md) | Fixing the SUSE `struct module` size mismatch |
| [05-module-installation.md](05-module-installation.md) | Installing and loading the driver on Leap Micro |
| [06-wifi-configuration.md](06-wifi-configuration.md) | Configuring WiFi with NetworkManager |
| [07-troubleshooting.md](07-troubleshooting.md) | Common issues and solutions |

## Hardware

- **WiFi Adapter:** TP-Link Archer T2U PLUS (RTL8821AU)
- **USB ID:** `2357:0120`
- **Driver Source:** https://github.com/morrownr/8821au-20210708
- **Host OS:** openSUSE Leap Micro 6.2
- **Kernel:** 6.12.0-160000.5-default (SUSE-patched, built with gcc-13)
- **Build GCC:** 7.5.0 (from Leap 15.6 OSS repo)

## Quick Start

If you just want the working commands (and understand what they do), see the [quick-build.sh](quick-build.sh) script.

## License

This guide is released under MIT. The RTL8821AU driver is GPL-2.0.
