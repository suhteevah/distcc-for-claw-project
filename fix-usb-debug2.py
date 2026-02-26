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

# Step 1: Force rebuild with MODPOST warnings only
print("=== Step 1: Rebuild with KBUILD_MODPOST_WARN=1 ===")
result = run(r"""
cd /root/wifi-build/rtw88
# Remove old .ko files explicitly
rm -f *.ko *.o *.mod *.mod.c *.mod.o modules.order Module.symvers .*.cmd 2>/dev/null
rm -rf .tmp_versions 2>/dev/null

# Full rebuild
make KSRC="/root/wifi-build/linux-6.12" KBUILD_MODPOST_WARN=1 2>&1 | tail -25
""", timeout=300)
print(result)

# Check if .ko files were generated
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

# Verify debug prints are in the built module
print("\n=== Verify debug strings in rtw_usb.ko ===")
print(run(r"strings /root/wifi-build/rtw88/rtw_usb.ko | grep -i 'rtw_usb_parse\|pipe_in\|out_pipes' | head -10"))

# Step 2: Reboot
print("\n=== Step 2: Rebooting ===")
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

# Step 3: Load modules fresh
print("\n=== Step 3: Load debug modules ===")
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
""", timeout=60))

# Step 4: Get the debug output
print("\n=== Step 4: Debug output from dmesg ===")
print(run(r"dmesg | grep -i 'rtw_usb_parse\|EP\[.\]\|pipe_in\|pipe_int\|out_ep\|out_pipes\|overflow\|endpoints\|failed.*USB\|probe.*error\|Firmware' | tail -50"))

print("\n=== Step 4b: Full rtw dmesg ===")
print(run(r"dmesg | grep -i rtw | tail -30"))

print("\n=== Interfaces ===")
print(run(r"ip link show"))

client.close()
print("\n=== DONE ===")
