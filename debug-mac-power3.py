import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Find rtw_chip_efuse_enable - this is the function that calls power on for efuse read
print("=== rtw_chip_efuse_enable ===")
print(run(r"grep -n 'rtw_chip_efuse_enable\|efuse_enable\|power_on.*mac\|failed to power on' /root/wifi-build/rtw88/main.c | head -20"))

# 2. Get the full function
print("\n=== rtw_chip_efuse_enable implementation ===")
print(run(r"sed -n '/^static.*rtw_chip_efuse_enable/,/^}/p' /root/wifi-build/rtw88/main.c"))

# 3. Also check if there's an 8821a-specific efuse enable
print("\n=== 8821a efuse functions ===")
print(run(r"grep -n 'efuse_enable\|efuse_disable\|power_on' /root/wifi-build/rtw88/rtw88xxa.c | head -20"))

# 4. Check rtw88xxa_power_on - specifically the "failed to power on mac" message
print("\n=== 'failed to power on mac' message source ===")
print(run(r"grep -rn 'failed to power on mac\|power on mac' /root/wifi-build/rtw88/*.c | head -10"))

# 5. Check if rtw88xxa.c has an efuse-specific power on
print("\n=== rtw88xxa efuse power on ===")
print(run(r"sed -n '/efuse_enable\|efuse_grant/,/^}/p' /root/wifi-build/rtw88/rtw88xxa.c | head -40"))

# 6. Check the chip_ops structure for 8821a to see what ops->power_on points to
print("\n=== 8821a chip_ops structure ===")
print(run(r"sed -n '/static.*const.*struct.*rtw_chip_info.*rtw8821a/,/^};/p' /root/wifi-build/rtw88/rtw8821a.c | head -60"))

# 7. Check ops->power_on assignment
print("\n=== rtw88xxa_common_chip_ops ===")
print(run(r"grep -n 'power_on\|efuse' /root/wifi-build/rtw88/rtw88xxa.c | grep -i 'ops\|assign\|\.power' | head -20"))

# 8. Let me also check where "failed to power on mac" comes from
print("\n=== Searching all 'failed to power on' messages ===")
print(run(r"grep -rn 'failed to power on' /root/wifi-build/rtw88/*.c"))

# 9. Check rtw_chip_efuse_disable
print("\n=== rtw_chip_efuse_disable ===")
print(run(r"sed -n '/^static.*rtw_chip_efuse_disable/,/^}/p' /root/wifi-build/rtw88/main.c"))

# 10. Current dmesg with full rtw trace
print("\n=== Full current dmesg rtw trace ===")
print(run(r"dmesg | grep -i rtw | tail -30"))

# 11. Check REG_CR and REG_SYS_STATUS1 current values (if modules still loaded)
print("\n=== Current module state ===")
print(run(r"lsmod | grep rtw"))

# 12. Check the rtw88xxau_hw_reset function
print("\n=== rtw88xxau_hw_reset ===")
print(run(r"sed -n '/^static.*rtw88xxau_hw_reset/,/^}/p' /root/wifi-build/rtw88/rtw88xxa.c"))

# 13. Check rtw_mac_pre_system_cfg
print("\n=== rtw_mac_pre_system_cfg ===")
print(run(r"sed -n '/^static int rtw_mac_pre_system_cfg/,/^}/p' /root/wifi-build/rtw88/mac.c"))

client.close()
print("\n=== DONE ===")
