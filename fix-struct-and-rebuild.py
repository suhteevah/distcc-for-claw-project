import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Patch usb.h to add the missing eusb2_isoc_ep_comp field
print("=== Step 1: Patch usb.h ===")
run(r"""cat > /tmp/fix_usb_struct.py << 'PYEOF'
path = "/root/wifi-build/linux-6.12/include/linux/usb.h"
with open(path, "r") as f:
    content = f.read()

# Find the usb_host_endpoint struct and add the missing field
# The SUSE kernel has 'eusb2_isoc_ep_comp' between ssp_isoc_ep_comp and urb_list
# This adds 8 bytes to the struct (sizeof goes from 80 to 88)

old = '\tstruct usb_ssp_isoc_ep_comp_descriptor\tssp_isoc_ep_comp;\n\tstruct list_head\t\turb_list;'
new = '''\tstruct usb_ssp_isoc_ep_comp_descriptor\tssp_isoc_ep_comp;
\t/* SUSE 6.12.0-160000.6-default kernel backports eusb2 isochronous
\t * endpoint companion descriptor from 6.13. Must match kernel ABI
\t * or struct usb_host_endpoint array indexing breaks (sizeof 80 vs 88).
\t */
\tu8\t\t\t\t\t__eusb2_isoc_ep_comp[8];
\tstruct list_head\t\turb_list;'''

if old in content:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("PATCHED: Added 8-byte eusb2_isoc_ep_comp padding to usb_host_endpoint")
else:
    print("FAILED: Could not find struct pattern in usb.h")
    # Check what's there
    import re
    m = re.search(r'ssp_isoc_ep_comp.*?urb_list', content, re.DOTALL)
    if m:
        print(f"Found: ...{m.group()[:200]}...")
PYEOF
""")
print(run("python3 /tmp/fix_usb_struct.py"))

# Verify the patch
print("\n=== Verify usb.h patch ===")
print(run(r"grep -A12 'struct usb_host_endpoint {' /root/wifi-build/linux-6.12/include/linux/usb.h"))

# Step 2: Quick sizeof check
print("\n=== Step 2: Verify sizeof ===")
run(r"""cat > /tmp/check_size2.c << 'EOF'
#include <linux/module.h>
#include <linux/usb.h>

static int __init check_init(void)
{
    pr_info("sizeof(usb_host_endpoint) = %zu (should be 88)\n",
            sizeof(struct usb_host_endpoint));
    return -EINVAL;
}
module_init(check_init);
MODULE_LICENSE("GPL");
EOF
cat > /tmp/Makefile << 'EOF'
obj-m := check_size2.o
EOF
""")
print(run(r"""
cd /tmp
make -C /root/wifi-build/linux-6.12 M=/tmp modules KBUILD_MODPOST_WARN=1 2>&1 | grep -v WARNING | tail -5
if [ -f /tmp/check_size2.ko ]; then
    insmod /tmp/check_size2.ko 2>/dev/null
    dmesg | grep 'sizeof' | tail -3
    rmmod check_size2 2>/dev/null
fi
rm -f /tmp/check_size2.* /tmp/Makefile /tmp/.check_size2* /tmp/Module.symvers /tmp/modules.order 2>/dev/null
""", timeout=120))

# Step 3: Also remove debug prints from usb.c (keep it clean)
print("\n=== Step 3: Clean up debug prints from usb.c ===")
run(r"""cat > /tmp/clean_usb_debug.py << 'PYEOF'
path = "/root/wifi-build/rtw88/usb.c"
with open(path, "r") as f:
    lines = f.readlines()

# Remove lines containing our debug prints
cleaned = []
skip_count = 0
for line in lines:
    if 'rtw_info(rtwdev, "rtw_usb_parse' in line:
        skip_count += 1
        # Skip this line and the next line (continuation)
        continue
    if 'rtw_info(rtwdev, "  EP[' in line:
        skip_count += 1
        continue
    if 'rtw_info(rtwdev, "  -> pipe_in' in line:
        skip_count += 1
        continue
    if 'rtw_info(rtwdev, "  -> pipe_interrupt' in line:
        skip_count += 1
        continue
    if 'rtw_info(rtwdev, "  -> out_ep' in line:
        skip_count += 1
        continue
    if 'rtw_info(rtwdev, "rtw_usb_parse done' in line:
        skip_count += 1
        continue
    # Also check for multi-line continuations of the debug prints
    stripped = line.strip()
    if stripped.startswith('interface_desc->bNumEndpoints'):
        skip_count += 1
        continue
    if stripped.startswith('i, endpoint->bEndpointAddress'):
        skip_count += 1
        continue
    if stripped.startswith('usb_endpoint_dir_in(endpoint)'):
        skip_count += 1
        continue
    if stripped.startswith('usb_endpoint_xfer_bulk(endpoint)'):
        skip_count += 1
        continue
    if stripped.startswith('usb_endpoint_xfer_int(endpoint)'):
        skip_count += 1
        continue
    if stripped.startswith('rtwusb->pipe_in, rtwusb->pipe_interrupt'):
        skip_count += 1
        continue
    cleaned.append(line)

with open(path, "w") as f:
    f.writelines(cleaned)
print(f"Removed {skip_count} debug print lines from usb.c")
PYEOF
""")
print(run("python3 /tmp/clean_usb_debug.py"))

# Step 4: Rebuild everything
print("\n=== Step 4: Full rebuild ===")
result = run(r"""
cd /root/wifi-build/rtw88
# Clean everything
rm -f *.ko *.o *.mod *.mod.c *.mod.o modules.order Module.symvers .*.cmd 2>/dev/null
rm -rf .tmp_versions 2>/dev/null

# Full rebuild
make KSRC="/root/wifi-build/linux-6.12" KBUILD_MODPOST_WARN=1 2>&1 | tail -15
""", timeout=300)
print(result)

# Check .ko files
print("\n=== Check .ko files ===")
print(run(r"""
cd /root/wifi-build/rtw88
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(stat -c%s "./${ko}.ko")
        echo "  ${ko}.ko: ${SIZE} bytes"
    else
        echo "  ${ko}.ko: NOT FOUND"
    fi
done
"""))

# Step 5: Reboot
print("\n=== Step 5: Rebooting ===")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting...")
client.close()

time.sleep(40)
for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        def run(cmd, timeout=120):
            stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err
        print("  CONNECTED!")
        break
    except:
        pass
else:
    print("Failed to reconnect!")
    exit(1)

print(run("uname -r && uptime"))

# Step 6: Load modules fresh
print("\n=== Step 6: Load modules ===")
print(run(r"""
modprobe cfg80211 2>/dev/null
modprobe mac80211 2>/dev/null
sleep 1

cd /root/wifi-build/rtw88
for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${mod}.ko" ]; then
        echo -n "  insmod ${mod}.ko... "
        RESULT=$(insmod "./${mod}.ko" 2>&1)
        RC=$?
        if [ $RC -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED: $RESULT"
        fi
    fi
done

sleep 5
""", timeout=60))

# Step 7: Check results
print("\n=== Step 7: dmesg ===")
print(run(r"dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipe\|endpoint\|probe' | tail -30"))

print("\n=== Interfaces ===")
print(run(r"""
ip link show
echo ""
iw dev 2>/dev/null
"""))

# Step 8: WiFi if interface exists
print("\n=== Step 8: WiFi ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 2
    echo "=== Scanning ==="
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10
    echo ""
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8
    echo "=== WPA Status ==="
    wpa_cli -i "$WLAN" status 2>&1
    echo ""
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1
    sleep 5
    echo "=== IP ==="
    ip addr show "$WLAN"
    echo ""
    echo "=== Ping ==="
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    echo ""
    dmesg | grep -i 'rtw\|probe\|error\|pipe\|endpoint\|mac.*power' | tail -25
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
