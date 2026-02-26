import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Check if usb.c pipe overflow patch is still present
print("=== 1. usb.c pipe overflow handling ===")
print(run(r"grep -n 'pipes overflow\|IN_PIPES\|INT_PIPES\|OUT_PIPES\|num_in_pipes\|num_int_pipes\|num_out_pipes\|endpoints.*invalid\|continue.*overflow' /root/wifi-build/rtw88/usb.c | head -30"))

# 2. Get the full rtw_usb_parse function (where pipe counting happens)
print("\n=== 2. rtw_usb_parse function ===")
print(run(r"sed -n '/^static int rtw_usb_parse/,/^}/p' /root/wifi-build/rtw88/usb.c"))

# 3. Get the pipe overflow check sections specifically
print("\n=== 3. Pipe overflow check area ===")
print(run(r"grep -n -B3 -A5 'overflow' /root/wifi-build/rtw88/usb.c"))

# 4. Check rtw_usb_setup (where endpoints get validated)
print("\n=== 4. rtw_usb_setup function ===")
print(run(r"sed -n '/^static int rtw_usb_setup/,/^}/p' /root/wifi-build/rtw88/usb.c"))

# 5. Check RTW_USB_MAX_IN/INT/OUT_PIPES definitions
print("\n=== 5. Pipe max definitions ===")
print(run(r"grep -n 'RTW_USB_MAX\|MAX_IN_PIPES\|MAX_INT_PIPES\|MAX_OUT_PIPES\|RTW_USB_PIPE' /root/wifi-build/rtw88/usb.h"))
print(run(r"grep -n 'RTW_USB_MAX\|MAX_IN_PIPES\|MAX_INT_PIPES\|MAX_OUT_PIPES\|RTW_USB_PIPE' /root/wifi-build/rtw88/usb.c"))

# 6. Check the actual USB device endpoints from kernel
print("\n=== 6. USB device endpoints ===")
print(run(r"cat /sys/bus/usb/devices/3-9/3-9:1.0/bNumEndpoints 2>/dev/null || echo 'No endpoint file'"))
print(run(r"ls /sys/bus/usb/devices/3-9/ep_* 2>/dev/null || echo 'No ep files'"))
print(run(r"for ep in /sys/bus/usb/devices/3-9/3-9:1.0/ep_*; do echo -n \"$(basename $ep): \"; cat $ep/bEndpointAddress $ep/bmAttributes 2>/dev/null | tr '\n' ' '; echo; done"))

# 7. Current dmesg errors
print("\n=== 7. Current dmesg rtw ===")
print(run(r"dmesg | grep -i 'rtw\|8821\|pipe\|endpoint\|firmware\|probe' | tail -30"))

# 8. Current module state
print("\n=== 8. Module state ===")
print(run(r"lsmod | grep rtw"))

# 9. Check the rtwusb struct to see pipe fields
print("\n=== 9. rtwusb struct definition ===")
print(run(r"grep -A30 'struct rtw_usb {' /root/wifi-build/rtw88/usb.h"))

# 10. Check rtw_usb_init function
print("\n=== 10. rtw_usb_init ===")
print(run(r"sed -n '/^static int rtw_usb_init/,/^}/p' /root/wifi-build/rtw88/usb.c"))

client.close()
print("\n=== DONE ===")
