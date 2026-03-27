# 09 -- Monitor Mode & Packet Injection Patches

Adding monitor mode and packet injection support to the lwfinger/rtw88 driver for use with aircrack-ng.

## Background

The stock lwfinger/rtw88 driver registers only `STATION`, `AP`, `ADHOC`, `P2P_CLIENT`, and `P2P_GO` interface types. Monitor mode is not enabled by default, but the driver already uses the mac80211 subsystem which handles radiotap headers automatically. This means adding monitor mode requires only minimal changes.

**What mac80211 gives us for free:**
- RX radiotap headers (added automatically when interface is in monitor mode)
- TX injection (mac80211 strips radiotap header before calling `rtw_ops_tx`)
- Frame type filtering via `configure_filter` callback

**What we need to add:**
1. Register `NL80211_IFTYPE_MONITOR` as a supported interface type
2. Handle monitor interfaces in `add_interface`
3. Accept control frames and all-BSS traffic in `configure_filter`

## Prerequisites

- Driver source at `/root/wifi-build/rtw88/` (see [04-rtw88-driver-build.md](04-rtw88-driver-build.md))
- All SUSE ABI fixes applied (see [03-suse-abi-fixes.md](03-suse-abi-fixes.md))
- Valid `Module.symvers` from running kernel (see Patch Notes below)

---

## Patch 1: Register Monitor Mode (`main.c`)

### The Change

In `main.c`, find the `interface_modes` assignment (around line 2398) and add `NL80211_IFTYPE_MONITOR`:

```c
// BEFORE:
hw->wiphy->interface_modes = BIT(NL80211_IFTYPE_STATION) |
                             BIT(NL80211_IFTYPE_AP) |
                             BIT(NL80211_IFTYPE_ADHOC) |
                             BIT(NL80211_IFTYPE_P2P_CLIENT) |
                             BIT(NL80211_IFTYPE_P2P_GO);

// AFTER:
hw->wiphy->interface_modes = BIT(NL80211_IFTYPE_STATION) |
                             BIT(NL80211_IFTYPE_AP) |
                             BIT(NL80211_IFTYPE_ADHOC) |
                             BIT(NL80211_IFTYPE_MONITOR) |
                             BIT(NL80211_IFTYPE_P2P_CLIENT) |
                             BIT(NL80211_IFTYPE_P2P_GO);
```

This tells cfg80211/nl80211 that monitor mode is a supported interface type, which enables `iw dev <iface> set type monitor`.

---

## Patch 2: Handle Monitor Interface (`mac80211.c`)

### The Change

In `mac80211.c`, find the `rtw_ops_add_interface()` function's switch statement (around line 209). Add a `MONITOR` case before the `STATION` case:

```c
// BEFORE:
    case NL80211_IFTYPE_STATION:
        rtw_add_rsvd_page_sta(rtwdev, rtwvif);
        net_type = RTW_NET_NO_LINK;
        bcn_ctrl = BIT_EN_BCN_FUNCTION;
        break;

// AFTER:
    case NL80211_IFTYPE_MONITOR:
        net_type = RTW_NET_NO_LINK;
        bcn_ctrl = 0;
        break;
    case NL80211_IFTYPE_STATION:
        rtw_add_rsvd_page_sta(rtwdev, rtwvif);
        net_type = RTW_NET_NO_LINK;
        bcn_ctrl = BIT_EN_BCN_FUNCTION;
        break;
```

**Why `RTW_NET_NO_LINK`:** Monitor mode doesn't associate to any AP, so it uses the "no link" network type — same as an unassociated station.

**Why `bcn_ctrl = 0`:** Monitor mode doesn't need beacon functions. Setting it to 0 disables beacon filtering so all beacons are passed through.

---

## Patch 3: Accept All Frame Types in Monitor Mode (`mac80211.c`)

### The Change

In `mac80211.c`, find the `rtw_ops_configure_filter()` function (around line 290). Two modifications:

**3a: Add `FIF_CONTROL` and `FIF_PSPOLL` to the accepted filter flags:**

```c
// BEFORE:
*new_flags &= FIF_ALLMULTI | FIF_OTHER_BSS | FIF_FCSFAIL |
              FIF_BCN_PRBRESP_PROMISC;

// AFTER:
*new_flags &= FIF_ALLMULTI | FIF_OTHER_BSS | FIF_FCSFAIL |
              FIF_BCN_PRBRESP_PROMISC | FIF_CONTROL | FIF_PSPOLL;
```

**3b: Add a new filter block after the `FIF_BCN_PRBRESP_PROMISC` handler:**

```c
    // ... existing FIF_BCN_PRBRESP_PROMISC block ...
        else
            rtwdev->hal.rcr |= BIT_CBSSID_BCN;
    }
    // ADD THIS BLOCK:
    if (changed_flags & (FIF_CONTROL | FIF_PSPOLL)) {
        if (*new_flags & (FIF_CONTROL | FIF_PSPOLL))
            rtwdev->hal.rcr |= BIT_AAP | BIT_AB | BIT_APM;
        else
            rtwdev->hal.rcr &= ~(BIT_AB | BIT_APM);
    }

    rtw_dbg(rtwdev, RTW_DBG_RX,
    // ... rest of function ...
```

### RCR Bit Definitions (from `reg.h`)

| Bit | Name | Effect |
|-----|------|--------|
| `BIT_AAP` (bit 0) | Accept All Packets | Receive frames destined to any address |
| `BIT_APM` (bit 1) | Accept Physical Match | Accept frames matching our MAC |
| `BIT_AB` (bit 3) | Accept Broadcast | Accept broadcast frames |
| `BIT_AM` (bit 2) | Accept Multicast | Accept multicast frames |
| `BIT_ACRC32` (bit 8) | Accept CRC32 Error | Accept frames with bad FCS (useful for analysis) |
| `BIT_APP_FCS` (bit 31) | Append FCS | Include FCS in received frames |
| `BIT_CBSSID_BCN` (bit 7) | Check BSSID Beacon | Filter beacons by BSSID (disabled in promisc) |
| `BIT_CBSSID_DATA` (bit 6) | Check BSSID Data | Filter data by BSSID (disabled in promisc) |

When `FIF_CONTROL | FIF_PSPOLL` is set by mac80211 (which it does automatically for monitor interfaces), we enable `BIT_AAP`, `BIT_AB`, and `BIT_APM` to receive all traffic regardless of destination address.

---

## Applying Patches (Automated)

SSH into CNC-Server and run:

```bash
cd /root/wifi-build/rtw88
cp main.c main.c.bak
cp mac80211.c mac80211.c.bak

python3 -c "
# Patch main.c
with open('main.c', 'r') as f:
    src = f.read()
src = src.replace(
    'BIT(NL80211_IFTYPE_ADHOC) |\n\t\t\t\t     BIT(NL80211_IFTYPE_P2P_CLIENT)',
    'BIT(NL80211_IFTYPE_ADHOC) |\n\t\t\t\t     BIT(NL80211_IFTYPE_MONITOR) |\n\t\t\t\t     BIT(NL80211_IFTYPE_P2P_CLIENT)',
    1)
with open('main.c', 'w') as f:
    f.write(src)

# Patch mac80211.c
with open('mac80211.c', 'r') as f:
    src = f.read()
# Patch 2: Add MONITOR case
src = src.replace(
    '\tcase NL80211_IFTYPE_STATION:\n\t\trtw_add_rsvd_page_sta(rtwdev, rtwvif);',
    '\tcase NL80211_IFTYPE_MONITOR:\n\t\tnet_type = RTW_NET_NO_LINK;\n\t\tbcn_ctrl = 0;\n\t\tbreak;\n\tcase NL80211_IFTYPE_STATION:\n\t\trtw_add_rsvd_page_sta(rtwdev, rtwvif);',
    1)
# Patch 3a: Add FIF_CONTROL | FIF_PSPOLL
src = src.replace(
    'FIF_BCN_PRBRESP_PROMISC;',
    'FIF_BCN_PRBRESP_PROMISC | FIF_CONTROL | FIF_PSPOLL;',
    1)
# Patch 3b: Add control frame RCR handler
src = src.replace(
    '\t\telse\n\t\t\trtwdev->hal.rcr |= BIT_CBSSID_BCN;\n\t}\n\n\trtw_dbg(rtwdev, RTW_DBG_RX,',
    '\t\telse\n\t\t\trtwdev->hal.rcr |= BIT_CBSSID_BCN;\n\t}\n\tif (changed_flags & (FIF_CONTROL | FIF_PSPOLL)) {\n\t\tif (*new_flags & (FIF_CONTROL | FIF_PSPOLL))\n\t\t\trtwdev->hal.rcr |= BIT_AAP | BIT_AB | BIT_APM;\n\t\telse\n\t\t\trtwdev->hal.rcr &= ~(BIT_AB | BIT_APM);\n\t}\n\n\trtw_dbg(rtwdev, RTW_DBG_RX,',
    1)
with open('mac80211.c', 'w') as f:
    f.write(src)
print('All patches applied.')
"
```

---

## Building

```bash
# Ensure Module.symvers is populated (empty = modpost fails with 300+ unresolved symbols)
cp /usr/src/linux-6.12.0-160000.26-obj/x86_64/default/Module.symvers /root/wifi-build/linux-6.12/Module.symvers

cd /root/wifi-build/rtw88
make clean
make KSRC="/root/wifi-build/linux-6.12"
```

Verify the struct module size matches:
```bash
objdump -h rtw_core.ko | grep this_module
# Should show 00000580
```

---

## Installation

The boot script (`/usr/local/bin/rtw88-wifi-start.sh`) loads modules from `/root/wifi-build/rtw88/` via `insmod`, so no file copying is needed — just reboot:

```bash
reboot
```

### Preventing Duplicate Module Loading

Create a blacklist for in-tree rtw88 modules to prevent conflicts:

```bash
cat > /etc/modprobe.d/rtw88-blacklist.conf << EOF
# Blacklist in-tree rtw88 modules to prevent conflict with custom out-of-tree build
blacklist rtw88_8821cu
blacklist rtw88_8821ce
blacklist rtw88_8821cs
blacklist rtw88_8821c
blacklist rtw88_core
blacklist rtw88_usb
EOF
```

> **WARNING:** Duplicate WiFi modules loading simultaneously has previously caused bootloops on this system. Always verify only one set of rtw88 modules is loaded after reboot.

---

## Installing aircrack-ng

`iw` can be installed via transactional-update:
```bash
transactional-update -n pkg install iw
reboot
```

`aircrack-ng` must be built from source (repo version has dependency conflicts on Leap Micro):
```bash
cd /root
git clone --depth 1 https://github.com/aircrack-ng/aircrack-ng.git

# Install build deps first
transactional-update -n -c pkg install autoconf automake libtool libnl3-devel libpcap-devel
reboot

# Build
cd /root/aircrack-ng
autoreconf -i
./configure --prefix=/usr/local --with-experimental
make -j$(nproc)
make install
ldconfig
```

---

## Usage

### Enable Monitor Mode

```bash
# Stop WiFi services
systemctl stop dhcpcd-wifi wpa-wifi

# Switch to monitor mode
ip link set wlp0s20u9 down
iw dev wlp0s20u9 set type monitor
ip link set wlp0s20u9 up

# Verify
iw dev wlp0s20u9 info
# Should show: type monitor

# Run airodump-ng
airodump-ng wlp0s20u9

# Capture to file
airodump-ng wlp0s20u9 --write /tmp/capture --output-format pcap,csv

# Target specific channel
airodump-ng wlp0s20u9 --channel 6

# Deauth test (your own network only)
aireplay-ng --deauth 5 -a <BSSID> wlp0s20u9
```

### Return to Managed Mode

```bash
ip link set wlp0s20u9 down
iw dev wlp0s20u9 set type managed
systemctl restart rtw88-wifi wpa-wifi dhcpcd-wifi
```

---

## Verification

After patching and rebooting, confirm monitor mode works:

```bash
# 1. Check new modules loaded (rtw_core size should be ~266KB vs ~262KB stock)
lsmod | grep rtw

# 2. iw confirms monitor mode is supported
iw phy phy0 info | grep monitor
# Should show: * monitor

# 3. Switch to monitor and back
ip link set wlp0s20u9 down
iw dev wlp0s20u9 set type monitor
iw dev wlp0s20u9 info | grep "type monitor"
# Should show: type monitor

ip link set wlp0s20u9 down
iw dev wlp0s20u9 set type managed
ip link set wlp0s20u9 up

# 4. Quick airodump-ng test (5 seconds)
ip link set wlp0s20u9 down
iw dev wlp0s20u9 set type monitor
ip link set wlp0s20u9 up
timeout 5 airodump-ng wlp0s20u9 --write /tmp/test --output-format csv
cat /tmp/test-01.csv | head -10
# Should show detected APs and stations
```

---

## How It Works (Technical Details)

### Why mac80211 Makes This Easy

The lwfinger/rtw88 driver is a proper mac80211 driver, meaning it delegates most WiFi stack functionality to the kernel's mac80211 subsystem. When an interface is set to monitor mode:

1. **mac80211** tells cfg80211 to set the interface type
2. **cfg80211** calls `rtw_ops_add_interface` with `NL80211_IFTYPE_MONITOR`
3. **mac80211** calls `rtw_ops_configure_filter` with `FIF_CONTROL`, `FIF_PSPOLL`, `FIF_OTHER_BSS`, etc.
4. **On RX:** mac80211 automatically prepends radiotap headers to all frames before delivering to userspace
5. **On TX (injection):** mac80211 strips the radiotap header from injected frames before calling `rtw_ops_tx`

We never had to write radiotap code — mac80211 handles it all. Our patches just:
- Tell the kernel "yes, we support monitor mode" (Patch 1)
- Don't crash when a monitor interface is created (Patch 2)
- Configure the hardware to actually receive all frames (Patch 3)

### RX Flow in Monitor Mode

```
Air → RTL8821AU hardware → USB bulk transfer → rtw_usb_rx()
  → rtw_rx_query_rx_desc() → rtw_rx_fill_rx_status()
  → ieee80211_rx() [mac80211 adds radiotap header]
  → /dev/wlp0s20u9 [userspace: airodump-ng reads raw frames]
```

### Packet Injection Flow

```
aireplay-ng → raw socket write with radiotap header
  → mac80211 strips radiotap → rtw_ops_tx()
  → rtw_tx_fill_tx_desc() → rtw_usb_tx()
  → USB bulk transfer → RTL8821AU hardware → Air
```
