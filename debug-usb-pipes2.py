import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Check the probe function call chain - where does rtw_usb_parse get called?
print("=== 1. Where rtw_usb_parse is called from ===")
print(run(r"grep -n 'rtw_usb_parse' /root/wifi-build/rtw88/usb.c"))

# 2. Get the full rtw_usb_probe function
print("\n=== 2. rtw_usb_probe function ===")
print(run(r"sed -n '/^static int rtw_usb_probe/,/^}/p' /root/wifi-build/rtw88/usb.c"))

# 3. Check if anything sets pipe_in before parse
print("\n=== 3. All references to pipe_in ===")
print(run(r"grep -n 'pipe_in[^t]' /root/wifi-build/rtw88/usb.c | head -20"))
print(run(r"grep -n 'pipe_in[^t]' /root/wifi-build/rtw88/usb.h | head -10"))

# 4. Check if parse is called multiple times
print("\n=== 4. Count of rtw_usb_parse calls ===")
print(run(r"grep -rn 'rtw_usb_parse' /root/wifi-build/rtw88/*.c"))

# 5. Check RTW_USB_EP_MAX
print("\n=== 5. RTW_USB_EP_MAX ===")
print(run(r"grep -n 'RTW_USB_EP_MAX\|EP_MAX' /root/wifi-build/rtw88/usb.h"))

# 6. Check ieee80211_alloc_hw in probe - how memory is allocated
print("\n=== 6. Memory allocation ===")
print(run(r"grep -n 'alloc_hw\|kzalloc\|kcalloc' /root/wifi-build/rtw88/usb.c | head -10"))

# 7. Check the actual USB endpoint descriptor order from the kernel
print("\n=== 7. USB descriptor details ===")
print(run(r"""
# Check USB descriptors
for ep in /sys/bus/usb/devices/3-9/3-9:1.0/ep_*; do
    EPNAME=$(basename $ep)
    ADDR=$(cat $ep/bEndpointAddress 2>/dev/null)
    TYPE=$(cat $ep/type 2>/dev/null)
    ATTR=$(cat $ep/bmAttributes 2>/dev/null)
    DIR=$(cat $ep/direction 2>/dev/null)
    echo "$EPNAME: addr=$ADDR attr=$ATTR type=$TYPE dir=$DIR"
done
"""))

# 8. Check lsusb details for endpoint order
print("\n=== 8. lsusb endpoint order ===")
print(run(r"lsusb -v -d 2357:0120 2>/dev/null | grep -A2 'Endpoint\|bNumEndpoints'"))
# lsusb might not be available on Micro
print(run(r"cat /sys/kernel/debug/usb/devices 2>/dev/null | grep -A30 'Vendor=2357 ProdID=0120' | head -40"))

# 9. Check if there's an rtw_usb_interface_configure or similar
print("\n=== 9. interface init functions ===")
print(run(r"grep -n 'interface\|rtw_usb_init\b' /root/wifi-build/rtw88/usb.c | head -20"))

# 10. Get the code around line 250 with precise context to see if there are additional blocks
print("\n=== 10. Lines 230-300 of usb.c ===")
print(run(r"sed -n '230,300p' /root/wifi-build/rtw88/usb.c"))

client.close()
print("\n=== DONE ===")
