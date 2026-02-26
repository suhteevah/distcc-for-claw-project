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

# Step 1: Use sed to fix the three broken if-conditions
# The debug cleanup removed usb_endpoint_xfer_bulk/int condition lines
print("=== Step 1: Fix usb.c if-conditions with sed ===")

# Fix 1: First "if (usb_endpoint_dir_in(endpoint) &&" needs "usb_endpoint_xfer_bulk(endpoint)) {"
# Fix 2: Second "if (usb_endpoint_dir_in(endpoint) &&" needs "usb_endpoint_xfer_int(endpoint)) {"
# Fix 3: "if (usb_endpoint_dir_out(endpoint) &&" needs "usb_endpoint_xfer_bulk(endpoint)) {"

# Use Python on the remote to fix it properly
fix_script = r'''
import re

path = "/root/wifi-build/rtw88/usb.c"
with open(path, "r") as f:
    lines = f.readlines()

fixed = []
i = 0
fix_count = 0
in_bulk_done = False
in_int_done = False
out_bulk_done = False

while i < len(lines):
    line = lines[i]

    # Pattern: "if (usb_endpoint_dir_in(endpoint) &&" followed by "if (rtwusb->pipe_in)"
    if (not in_bulk_done and
        'usb_endpoint_dir_in(endpoint) &&' in line and
        i+1 < len(lines) and 'pipe_in' in lines[i+1]):
        fixed.append(line.rstrip() + '\n')
        fixed.append('\t\t    usb_endpoint_xfer_bulk(endpoint)) {\n')
        in_bulk_done = True
        fix_count += 1
        i += 1
        continue

    # Pattern: "if (usb_endpoint_dir_in(endpoint) &&" followed by "if (rtwusb->pipe_interrupt)"
    if (not in_int_done and
        'usb_endpoint_dir_in(endpoint) &&' in line and
        i+1 < len(lines) and 'pipe_interrupt' in lines[i+1]):
        fixed.append(line.rstrip() + '\n')
        fixed.append('\t\t    usb_endpoint_xfer_int(endpoint)) {\n')
        in_int_done = True
        fix_count += 1
        i += 1
        continue

    # Pattern: "if (usb_endpoint_dir_out(endpoint) &&" followed by "if (num_out_pipes"
    if (not out_bulk_done and
        'usb_endpoint_dir_out(endpoint) &&' in line and
        i+1 < len(lines) and 'num_out_pipes' in lines[i+1]):
        fixed.append(line.rstrip() + '\n')
        fixed.append('\t\t    usb_endpoint_xfer_bulk(endpoint)) {\n')
        out_bulk_done = True
        fix_count += 1
        i += 1
        continue

    fixed.append(line)
    i += 1

with open(path, "w") as f:
    f.writelines(fixed)
print(f"Applied {fix_count} fixes")
'''

# Write the fix script to the server
sftp = client.open_sftp()
with sftp.open('/tmp/fix_usb_syntax.py', 'w') as f:
    f.write(fix_script)
sftp.close()

print(run("python3 /tmp/fix_usb_syntax.py"))

# Step 2: Verify the fix looks right
print("\n=== Step 2: Verify rtw_usb_parse function ===")
print(run(r"sed -n '250,300p' /root/wifi-build/rtw88/usb.c"))

# Step 3: Full rebuild
print("\n=== Step 3: Full rebuild ===")
result = run(r"""
cd /root/wifi-build/rtw88
rm -f *.ko *.o *.mod *.mod.c *.mod.o modules.order Module.symvers .*.cmd 2>/dev/null
rm -rf .tmp_versions 2>/dev/null

make KSRC="/root/wifi-build/linux-6.12" KBUILD_MODPOST_WARN=1 2>&1 | tail -15
""", timeout=300)
print(result)

# Check .ko files
print("\n=== Check .ko files ===")
ko_result = run(r"""
cd /root/wifi-build/rtw88
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(stat -c%s "./${ko}.ko")
        echo "  ${ko}.ko: ${SIZE} bytes"
    else
        echo "  ${ko}.ko: NOT FOUND"
    fi
done
""")
print(ko_result)

# Check if build succeeded
if "NOT FOUND" in ko_result and "rtw_usb.ko: NOT FOUND" in ko_result:
    print("\n!!! BUILD FAILED - checking full error output ===")
    print(run(r"""
cd /root/wifi-build/rtw88
rm -f *.ko *.o *.mod *.mod.c *.mod.o modules.order Module.symvers .*.cmd 2>/dev/null
rm -rf .tmp_versions 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" KBUILD_MODPOST_WARN=1 2>&1 | grep -i 'error'
""", timeout=300))
    client.close()
    exit(1)

# Step 4: Reboot
print("\n=== Step 4: Rebooting ===")
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

# Step 5: Load modules fresh
print("\n=== Step 5: Load modules ===")
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

# Step 6: Check results
print("\n=== Step 6: dmesg ===")
print(run(r"dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipe\|endpoint\|probe' | tail -30"))

print("\n=== Interfaces ===")
print(run(r"""
ip link show
echo ""
iw dev 2>/dev/null
"""))

# Step 7: WiFi if interface exists
print("\n=== Step 7: WiFi ===")
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
    dmesg | grep -i 'rtw\|probe\|error\|pipe\|endpoint\|mac.*power\|firmware' | tail -25
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
