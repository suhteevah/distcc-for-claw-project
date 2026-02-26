import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Check current dmesg for the full error trace
print("=== DMESG ERROR TRACE ===")
print(run("dmesg | grep -i 'rtw\|8821\|mac.*power\|firmware\|probe\|efuse' | tail -40"))

# 2. Look at the power_on function in rtw88xxa.c
print("\n=== rtw88xxa_power_on function ===")
print(run("grep -n 'power_on' /root/wifi-build/rtw88/rtw88xxa.c | head -20"))

# 3. Get the full power_on function
print("\n=== Full power_on implementation ===")
print(run("sed -n '/^.*rtw88xxa_power_on/,/^}/p' /root/wifi-build/rtw88/rtw88xxa.c | head -80"))

# 4. Check mac.c for rtw_mac_power_on
print("\n=== rtw_mac_power_on in mac.c ===")
print(run("grep -n 'mac_power_on\|power_on\|mac_power_switch' /root/wifi-build/rtw88/mac.c | head -20"))

# 5. Get the mac power on function
print("\n=== rtw_mac_power_on implementation ===")
print(run("sed -n '/^.*rtw_mac_power_on/,/^}/p' /root/wifi-build/rtw88/mac.c | head -80"))

# 6. Check what EALREADY (114) means in context - search for -114 or EALREADY
print("\n=== EALREADY references ===")
print(run("grep -rn 'EALREADY\|-114' /root/wifi-build/rtw88/*.c /root/wifi-build/rtw88/*.h 2>/dev/null | head -20"))

# 7. Check mac_power_switch function (this is often where EALREADY comes from)
print("\n=== mac_power_switch ===")
print(run("grep -n 'mac_power_switch\|pwr_seq' /root/wifi-build/rtw88/mac.c | head -20"))

# 8. Look at rtw_pwr_seq_parser or power sequence
print("\n=== Power sequence parser ===")
print(run("grep -n 'pwr_seq\|power_seq\|rtw_pwr' /root/wifi-build/rtw88/mac.c | head -30"))

# 9. Get the mac_power_switch function
print("\n=== mac_power_switch implementation ===")
print(run("sed -n '/static.*mac_power_switch/,/^}/p' /root/wifi-build/rtw88/mac.c | head -100"))

# 10. Check if there's a chip_ops power_on for 8821a
print("\n=== 8821a chip_ops ===")
print(run("grep -n 'power_on\|chip_ops' /root/wifi-build/rtw88/rtw8821a.c | head -20"))

# 11. Check the main probe path
print("\n=== Probe path in main.c ===")
print(run("grep -n 'power_on\|setup_chip\|efuse' /root/wifi-build/rtw88/main.c | head -20"))

# 12. Get the chip setup function
print("\n=== rtw_chip_info_setup ===")
print(run("sed -n '/rtw_chip_info_setup/,/^}/p' /root/wifi-build/rtw88/main.c | head -40"))

# 13. USB-specific register access 
print("\n=== USB read/write functions ===")
print(run("grep -n 'rtw_usb_read\|rtw_usb_write\|rtw_read8\|rtw_write8' /root/wifi-build/rtw88/usb.c | head -20"))

# 14. Check errno.h for EALREADY definition
print("\n=== EALREADY value ===")
print(run("grep EALREADY /usr/include/asm-generic/errno.h 2>/dev/null || grep EALREADY /usr/include/linux/errno.h 2>/dev/null || echo 'EALREADY = 114 (Operation already in progress)'"))

# 15. Check for USB-specific power issues
print("\n=== USB power/init ===")
print(run("grep -n 'power\|init.*chip\|pre_init' /root/wifi-build/rtw88/usb.c | head -20"))

client.close()
