# 04 — Fixing the SUSE `struct module` Size Mismatch

## The Problem

After building the driver against vanilla Linux 6.12 source, `insmod` fails with:

```
module 8821au: .gnu.linkonce.this_module section size must match
the kernel's built struct module size at run time
```

Comparing the `.gnu.linkonce.this_module` section sizes:

| Module | Size | Source |
|--------|------|--------|
| Our 8821au.ko | 0x540 (1344 bytes) | Built against vanilla 6.12 |
| Reference r8152.ko | 0x580 (1408 bytes) | Built by SUSE with patched kernel |

**Difference: 64 bytes (0x40)**

## Root Cause

The SUSE kernel has `CONFIG_LIVEPATCH_IPA_CLONES=y` — a SUSE-specific patch that adds fields to `struct module` in `include/linux/module.h`. This config option does not exist in the vanilla kernel source.

```bash
# Running kernel config:
zcat /proc/config.gz | grep LIVEPATCH
# CONFIG_HAVE_LIVEPATCH=y
# CONFIG_LIVEPATCH=y
# CONFIG_LIVEPATCH_IPA_CLONES=y    <-- SUSE-specific!

# Our vanilla .config:
grep LIVEPATCH .config
# CONFIG_HAVE_LIVEPATCH=y
# CONFIG_LIVEPATCH=y
# (CONFIG_LIVEPATCH_IPA_CLONES is absent — vanilla doesn't know about it)
```

## The Fix: Add Padding to `struct module`

We add exactly 64 bytes of padding to `struct module` to match the SUSE kernel's expected size. The padding is placed inside the existing `#ifdef CONFIG_LIVEPATCH` block, right after the `klp_info` pointer.

### Patch

Edit `include/linux/module.h` in the kernel source:

```bash
cd /root/wifi-build/linux-6.12
```

Find the LIVEPATCH section inside `struct module` (around line 558):

```c
#ifdef CONFIG_LIVEPATCH
    bool klp; /* Is this a livepatch module? */
    bool klp_alive;

    /* ELF information */
    struct klp_modinfo *klp_info;
#endif
```

Add the padding after `klp_info`:

```c
#ifdef CONFIG_LIVEPATCH
    bool klp; /* Is this a livepatch module? */
    bool klp_alive;

    /* ELF information */
    struct klp_modinfo *klp_info;

    /* SUSE compatibility: CONFIG_LIVEPATCH_IPA_CLONES fields */
    void *klp_ipa_clones_padding[8]; /* 64 bytes to match SUSE struct module size */
#endif
```

### Automated Patch

```bash
sed -i '/struct klp_modinfo \*klp_info;/a\\n\t/* SUSE compatibility: CONFIG_LIVEPATCH_IPA_CLONES fields */\n\tvoid *klp_ipa_clones_padding[8]; /* 64 bytes to match SUSE struct module size */' \
    include/linux/module.h
```

### Rebuild Everything

After patching, clean and rebuild:

```bash
cd /root/wifi-build/linux-6.12
make clean
zcat /proc/config.gz > .config
make olddefconfig
make modules_prepare

cd /root/wifi-build/8821au-20210708
make clean
make ARCH=x86_64 KSRC="/root/wifi-build/linux-6.12"
```

### Verify Size Match

```bash
# Our module
objdump -h 8821au.ko | grep this_module
# Should show: 00000580

# Reference module
zstd -d /usr/lib/modules/$(uname -r)/kernel/drivers/net/usb/r8152.ko.zst -o /tmp/r8152.ko -f
objdump -h /tmp/r8152.ko | grep this_module
# Should show: 00000580

# Both should be 0x580!
```

## Why This Works

The `struct module` in the Linux kernel uses `__randomize_layout`, but the randomization is deterministic — it's based on a per-build seed derived from the kernel config. Since we use the **same kernel config** (from `/proc/config.gz`), the field randomization produces the same layout. Our padding fields are placed inside the LIVEPATCH block where the SUSE kernel expects its IPA clones fields.

## Important Caveat

The padding fields are initialized to zero (NULL pointers). If the kernel's IPA clones code tries to walk these as linked lists, it will hit NULL pointer dereferences. In practice:

- The module loading code only checks the **size** of `struct module`, not the field contents
- The LIVEPATCH IPA clones feature only activates for modules that are explicitly marked as livepatch modules
- Our WiFi driver module is not a livepatch module, so the IPA clones fields should never be accessed

However, if you encounter a kernel crash during `insmod`, it may be due to other code paths touching these padding fields. See [07-troubleshooting.md](07-troubleshooting.md) for mitigation strategies.

## Alternative Approaches (Not Recommended)

1. **Get the actual SUSE kernel source** — Requires SUSE Customer Center (SCC) subscription to access the SLFO 1.2 kernel source RPM
2. **Downgrade to a kernel with available devel package** — The only available kernel-default-devel is for 6.4.0, incompatible with the 6.12.0 kernel
3. **Use `insmod --force`** — Doesn't work; the kernel hard-rejects struct size mismatches
4. **Build inside a container** — Same problem; containers share the host kernel
