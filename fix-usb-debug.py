import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Upload a Python patcher to add debug prints to rtw_usb_parse
run(r"""cat > /tmp/patch_usb_debug.py << 'PYEOF'
import re

path = "/root/wifi-build/rtw88/usb.c"
with open(path, "r") as f:
    content = f.read()

# 1. Add debug print at the start of the for loop in rtw_usb_parse
# Find: "for (i = 0; i < interface_desc->bNumEndpoints; i++) {"
# Add before it: a debug print showing initial state
old = '\tfor (i = 0; i < interface_desc->bNumEndpoints; i++) {\n\t\tendpoint = &host_interface->endpoint[i].desc;\n\t\tnum = usb_endpoint_num(endpoint);'
new = '''	rtw_info(rtwdev, "rtw_usb_parse: bNumEndpoints=%d pipe_in=%u pipe_interrupt=%u\\n",
		interface_desc->bNumEndpoints, rtwusb->pipe_in, rtwusb->pipe_interrupt);

	for (i = 0; i < interface_desc->bNumEndpoints; i++) {
		endpoint = &host_interface->endpoint[i].desc;
		num = usb_endpoint_num(endpoint);

		rtw_info(rtwdev, "  EP[%d]: addr=0x%02x num=%u dir_in=%d xfer_bulk=%d xfer_int=%d\\n",
			i, endpoint->bEndpointAddress, num,
			usb_endpoint_dir_in(endpoint),
			usb_endpoint_xfer_bulk(endpoint),
			usb_endpoint_xfer_int(endpoint));'''

if old in content:
    content = content.replace(old, new)
    print("PATCH 1: Added debug prints to rtw_usb_parse loop")
else:
    print("PATCH 1 FAILED: Could not find for loop pattern")
    # Try to find what's there
    import re
    m = re.search(r'for \(i = 0.*?bNumEndpoints.*?\n.*?endpoint.*?\n.*?num = usb_endpoint_num', content, re.DOTALL)
    if m:
        print(f"Found similar at: ...{m.group()[:100]}...")
    else:
        print("Could not find similar pattern either")

# 2. Add debug print after pipe_in assignment
old2 = '\t\t\trtwusb->pipe_in = num;\n\t\t}'
new2 = '''\t\t\trtwusb->pipe_in = num;
\t\t\trtw_info(rtwdev, "  -> pipe_in set to %u\\n", num);
\t\t}'''

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("PATCH 2: Added pipe_in assignment debug print")
else:
    print("PATCH 2 FAILED")

# 3. Add debug print after pipe_interrupt assignment
old3 = '\t\t\trtwusb->pipe_interrupt = num;\n\t\t}'
new3 = '''\t\t\trtwusb->pipe_interrupt = num;
\t\t\trtw_info(rtwdev, "  -> pipe_interrupt set to %u\\n", num);
\t\t}'''

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("PATCH 3: Added pipe_interrupt assignment debug print")
else:
    print("PATCH 3 FAILED")

# 4. Add debug print for out_ep
old4 = '\t\t\trtwusb->out_ep[num_out_pipes++] = num;\n\t\t}'
new4 = '''\t\t\trtwusb->out_ep[num_out_pipes] = num;
\t\t\trtw_info(rtwdev, "  -> out_ep[%d] set to %u\\n", num_out_pipes, num);
\t\t\tnum_out_pipes++;
\t\t}'''

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("PATCH 4: Added out_ep assignment debug print")
else:
    print("PATCH 4 FAILED")

# 5. Add debug print before the endpoint count check
old5 = '\tif (num_out_pipes < 1 || num_out_pipes > 4) {'
new5 = '''\trtw_info(rtwdev, "rtw_usb_parse done: pipe_in=%u pipe_int=%u out_pipes=%d\\n",
		rtwusb->pipe_in, rtwusb->pipe_interrupt, num_out_pipes);

\tif (num_out_pipes < 1 || num_out_pipes > 4) {'''

if old5 in content:
    content = content.replace(old5, new5, 1)
    print("PATCH 5: Added final state debug print")
else:
    print("PATCH 5 FAILED")

with open(path, "w") as f:
    f.write(content)
print("\nAll patches written to usb.c")
PYEOF
""")

print("=== Applying debug patches ===")
print(run("python3 /tmp/patch_usb_debug.py"))

# Verify patches
print("\n=== Verify debug prints in code ===")
print(run(r"grep -n 'rtw_info.*parse\|rtw_info.*EP\|rtw_info.*pipe_in\|rtw_info.*pipe_int\|rtw_info.*out_ep\|rtw_info.*out_pipes' /root/wifi-build/rtw88/usb.c"))

# Rebuild
print("\n=== Rebuilding ===")
result = run(r"""
cd /root/wifi-build/rtw88
make clean 2>/dev/null
make KSRC="/root/wifi-build/linux-6.12" 2>&1 | tail -20
""", timeout=300)
print(result)

# Check .ko files
print("\n=== Check .ko files ===")
print(run(r"""
cd /root/wifi-build/rtw88
for ko in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do
    [ -f "./${ko}.ko" ] && echo "  ${ko}.ko: $(stat -c%s ./${ko}.ko) bytes"
done
"""))

# Unload old modules and reload
print("\n=== Unload and reload modules ===")
print(run(r"""
# Unload in reverse dependency order
for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do
    echo -n "rmmod $mod... "
    rmmod $mod 2>&1 && echo "OK" || echo "FAIL"
done
sleep 1

echo ""
echo "=== Loading fresh modules ==="
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
""", timeout=60))

# Check results
print("\n=== dmesg debug output ===")
print(run(r"dmesg | grep -i 'rtw_usb_parse\|EP\[.\]\|pipe_in\|pipe_int\|out_ep\|out_pipes\|overflow\|endpoints\|failed.*USB\|probe.*error\|Firmware' | tail -40"))

print("\n=== Interfaces ===")
print(run(r"ip link show | grep -A1 wl"))

client.close()
print("\n=== DONE ===")
