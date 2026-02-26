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

# Step 1: Upload and run the Python patcher for mac.c
print("=== Step 1: Patch mac.c ===")

# Upload patcher via heredoc (avoiding tab issues)
run(r"""cat > /tmp/fix_mac_power.py << 'PYEOF'
import re

path = "/root/wifi-build/rtw88/mac.c"
with open(path, "r") as f:
    lines = f.readlines()

patched = False
output = []
i = 0
while i < len(lines):
    line = lines[i]

    # FIX 1: After "cur_pwr = true;" and before "if (pwr_on == cur_pwr)"
    # Insert force-false for 8821A/8812A USB
    if 'cur_pwr = true;' in line and not patched:
        output.append(line)
        # Check if next non-blank line is "if (pwr_on == cur_pwr)"
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            output.append(lines[j])
            j += 1
        if j < len(lines) and 'pwr_on == cur_pwr' in lines[j]:
            # Insert our fix before the check
            output.append('\n')
            output.append('\t/* RTL8821A and RTL8812A USB: chip appears powered on after\n')
            output.append('\t * USB enumeration but is not properly initialized. Force the\n')
            output.append('\t * power-on sequence to run regardless of apparent state.\n')
            output.append('\t */\n')
            output.append('\tif (pwr_on && rtw_hci_type(rtwdev) == RTW_HCI_TYPE_USB &&\n')
            output.append('\t    (chip->id == RTW_CHIP_TYPE_8821A ||\n')
            output.append('\t     chip->id == RTW_CHIP_TYPE_8812A))\n')
            output.append('\t\tcur_pwr = false;\n')
            output.append('\n')
            output.append(lines[j])  # the "if (pwr_on == cur_pwr)" line
            i = j + 1
            patched = True
            print("FIX 1: Inserted 8821A/8812A USB power state override")
            continue

    # FIX 2: Add 8821A/8812A to SYS_STATUS1 clearing list
    if 'RTW_CHIP_TYPE_8821C)' in line and i+1 < len(lines) and 'REG_SYS_STATUS1' in lines[i+1]:
        # Replace the line to add 8821A and 8812A
        new_line = line.replace(
            'chip->id == RTW_CHIP_TYPE_8821C)',
            'chip->id == RTW_CHIP_TYPE_8821C ||\n\t\t    chip->id == RTW_CHIP_TYPE_8821A ||\n\t\t    chip->id == RTW_CHIP_TYPE_8812A)'
        )
        output.append(new_line)
        print("FIX 2: Added 8821A/8812A to SYS_STATUS1 clearing list")
        i += 1
        continue

    output.append(line)
    i += 1

if patched:
    with open(path, "w") as f:
        f.writelines(output)
    print("mac.c patched successfully!")
else:
    print("WARNING: FIX 1 pattern not found!")
    # Debug: show the area around cur_pwr
    for idx, line in enumerate(lines):
        if 'cur_pwr' in line:
            print(f"  Line {idx+1}: {line.rstrip()}")
PYEOF
""")
print(run("python3 /tmp/fix_mac_power.py"))

# Step 2: Verify patches
print("\n=== Step 2: Verify patches ===")
print("--- Power state override ---")
print(run(r"grep -n -B2 -A2 'RTW_CHIP_TYPE_8821A' /root/wifi-build/rtw88/mac.c"))
print("\n--- SYS_STATUS1 clearing ---")
print(run(r"grep -n -A1 'RTW_CHIP_TYPE_8812A' /root/wifi-build/rtw88/mac.c"))

# Step 3: Rebuild
print("\n=== Step 3: Rebuild ===")
result = run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -30
""", timeout=300)
print(result)

if "Error" in result or "error:" in result.lower():
    print("BUILD FAILED! Checking errors...")
    print(run(r"cd /root/wifi-build/rtw88 && make KSRC='/root/wifi-build/linux-6.12' 2>&1 | grep -i error"))
    client.close()
    exit(1)

# Step 4: Check built modules
print("\n=== Step 4: Check build ===")
print(run(r"""
cd /root/wifi-build/rtw88
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    if [ -f "./${ko}.ko" ]; then
        SIZE=$(stat -c%s "./${ko}.ko")
        echo "  ${ko}.ko: ${SIZE} bytes"
    fi
done
"""))

# Step 5: Reboot for clean state
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
print("\n=== Step 6: Load patched modules ===")
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

sleep 3

echo ""
echo "=== lsmod ==="
lsmod | grep -E 'rtw|mac80211|cfg80211'

echo ""
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|pipes\|probe\|mac.*power\|endpoint' | tail -30

echo ""
echo "=== Interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
""", timeout=60))

# Step 7: WiFi
print("\n=== Step 7: WiFi ===")
print(run(r"""
WLAN=$(ip link show 2>/dev/null | grep -oP 'wl\w+' | head -1)
if [ -n "$WLAN" ]; then
    echo "WiFi: $WLAN"
    ip link set "$WLAN" up 2>&1
    sleep 2
    iw dev "$WLAN" scan 2>&1 | grep 'SSID:' | head -10
    echo ""
    killall wpa_supplicant 2>/dev/null
    sleep 1
    wpa_supplicant -B -i "$WLAN" -c /etc/wpa_supplicant/wpa_supplicant.conf 2>&1
    sleep 8
    wpa_cli -i "$WLAN" status 2>&1
    echo ""
    dhclient "$WLAN" 2>&1 || dhcpcd "$WLAN" 2>&1
    sleep 5
    ip addr show "$WLAN"
    echo ""
    ping -c 3 -W 5 8.8.8.8 2>&1 | tail -3
else
    echo "No WiFi interface"
    dmesg | grep -i 'rtw\|probe\|error\|pipes\|endpoint\|mac.*power' | tail -20
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
