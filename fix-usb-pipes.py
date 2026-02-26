import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Find the "IN pipes overflow" code
print("=== Step 1: Find USB pipe overflow code ===")
print(run(r"""
cd /root/wifi-build/rtw88
grep -rn 'pipes overflow\|IN pipes\|OUT pipes' *.c *.h 2>/dev/null
"""))

# Step 2: Check the USB interface init code
print("\n=== Step 2: USB interface init code ===")
print(run(r"""
cd /root/wifi-build/rtw88
grep -rn 'failed to init USB\|init_usb\|parse.*endpoint\|bulk.*pipe\|num_bulk' usb.c 2>/dev/null | head -30
"""))

# Step 3: Get the full USB endpoint parsing function
print("\n=== Step 3: Full USB endpoint parsing ===")
print(run(r"""
cd /root/wifi-build/rtw88
# Find the function that checks pipes
grep -n 'pipes overflow' usb.c
"""))

# Step 4: Show context around the overflow check
print("\n=== Step 4: Context around overflow check ===")
print(run(r"""
cd /root/wifi-build/rtw88
# Get line number of overflow
LINE=$(grep -n 'IN pipes overflow' usb.c | cut -d: -f1)
if [ -n "$LINE" ]; then
    START=$((LINE - 40))
    END=$((LINE + 10))
    [ $START -lt 1 ] && START=1
    sed -n "${START},${END}p" usb.c
fi
"""))

# Step 5: Check the USB endpoint limit definitions
print("\n=== Step 5: USB endpoint limits ===")
print(run(r"""
cd /root/wifi-build/rtw88
grep -rn 'RTW_USB_MAX\|MAX_BULKIN\|MAX_BULKOUT\|RTW_USB_EP\|num_in\|num_out\|RTW_USB_PIPE' usb.h usb.c 2>/dev/null | head -30
"""))

# Step 6: Check what USB endpoints the actual device has
print("\n=== Step 6: Actual USB device endpoints ===")
print(run(r"""
# Show USB descriptor for the device
cat /sys/bus/usb/devices/3-9/bNumInterfaces 2>/dev/null
echo "---"
# List endpoints
for ep in /sys/bus/usb/devices/3-9/3-9:1.0/ep_*; do
    if [ -d "$ep" ]; then
        DIR=$(cat "$ep/direction" 2>/dev/null)
        TYPE=$(cat "$ep/type" 2>/dev/null)
        ADDR=$(cat "$ep/bEndpointAddress" 2>/dev/null)
        echo "Endpoint: addr=$ADDR dir=$DIR type=$TYPE"
    fi
done

echo ""
echo "=== Full USB device info ==="
cat /sys/kernel/debug/usb/devices 2>/dev/null | grep -A30 '2357' | head -40

echo ""
echo "=== lsusb verbose ==="
lsusb -v -d 2357:0120 2>/dev/null | grep -E 'Endpoint|bNumEndpoints|Interface|bulk' | head -20
"""))

# Step 7: Check the full rtw_usb_init function
print("\n=== Step 7: rtw_usb_init function ===")
print(run(r"""
cd /root/wifi-build/rtw88
# Find rtw_usb_init or similar
grep -n 'static.*rtw_usb_setup\|rtw_usb_init\|rtw_usb_intf_init\|static.*setup.*usb' usb.c | head -10
"""))

# Step 8: Show the full function that handles endpoint parsing
print("\n=== Step 8: Full endpoint parsing function ===")
print(run(r"""
cd /root/wifi-build/rtw88
# Get the function containing 'pipes overflow'
LINE=$(grep -n 'IN pipes overflow' usb.c | cut -d: -f1)
# Find function start (search backward for opening brace pattern)
FUNC_START=$(head -n $LINE usb.c | grep -n '^static\|^int\|^void' | tail -1 | cut -d: -f1)
FUNC_END=$((LINE + 30))
echo "Function from line $FUNC_START to $FUNC_END:"
sed -n "${FUNC_START},${FUNC_END}p" usb.c
"""))

# Step 9: Check what RTW_USB_MAX_BULKIN_NUM is
print("\n=== Step 9: Max bulk-in definition ===")
print(run(r"""
cd /root/wifi-build/rtw88
grep -rn 'BULKIN_NUM\|BULKOUT_NUM\|MAX_BULK\|RTW_USB_MAX' *.h *.c 2>/dev/null | head -20
echo ""
echo "=== usb.h contents ==="
cat usb.h
"""))

client.close()
print("\n=== DONE ===")
