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

# Step 1: Fix Module.symvers - create empty file
print("=== Step 1: Fix Module.symvers ===")
print(run(r"""
# The corrupted Module.symvers has wrong format from modprobe --dump-modversions
# Create an empty one - MODPOST will succeed without CRC validation
> /root/wifi-build/linux-6.12/Module.symvers
echo "Created empty Module.symvers"
ls -la /root/wifi-build/linux-6.12/Module.symvers
"""))

# Step 2: Verify mac.c patch is still in place
print("\n=== Step 2: Verify mac.c patch ===")
print(run(r"""
echo "=== Power state override ==="
grep -n 'RTW_CHIP_TYPE_8821A' /root/wifi-build/rtw88/mac.c
echo ""
echo "=== Full context ==="
grep -n -B2 -A2 'cur_pwr = false' /root/wifi-build/rtw88/mac.c | head -20
"""))

# Step 3: Rebuild
print("\n=== Step 3: Rebuild ===")
result = run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -40
""", timeout=300)
print(result)

# Check for .ko files
print("\n=== Step 3b: Check build ===")
print(run(r"""
cd /root/wifi-build/rtw88
echo "=== Built modules ==="
find . -name '*.ko' -type f | sort | head -10
echo ""
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    [ -f "./${ko}.ko" ] && echo "  ${ko}.ko: $(stat -c%s ./${ko}.ko) bytes"
done
"""))

# Step 4: Reboot to get clean module state
print("\n=== Step 4: Rebooting for clean state ===")
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

# Step 5: Load patched modules fresh
print("\n=== Step 5: Load patched modules ===")
print(run(r"""
# Ensure no old rtw modules
lsmod | grep rtw && echo "WARNING: old modules loaded!" || echo "Clean state"

# Load dependencies
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
    else
        echo "  ${mod}.ko NOT FOUND!"
    fi
done

sleep 3

echo ""
echo "=== lsmod ==="
lsmod | grep -E 'rtw|mac80211|cfg80211'

echo ""
echo "=== dmesg ==="
dmesg | grep -i 'rtw\|firmware\|wlan\|8821\|mac.*power\|probe\|endpoint' | tail -25

echo ""
echo "=== Interfaces ==="
ip link show
echo ""
iw dev 2>/dev/null
""", timeout=60))

# Step 6: WiFi
print("\n=== Step 6: WiFi ===")
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
    dmesg | grep -i 'rtw\|probe\|error\|mac.*power\|endpoint' | tail -20
fi
""", timeout=120))

client.close()
print("\n=== DONE ===")
