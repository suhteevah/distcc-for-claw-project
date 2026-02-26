import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. The EXACT rtw_chip_efuse_info_setup function
print("=== rtw_chip_efuse_info_setup ===")
print(run(r"sed -n '/^.*rtw_chip_efuse_info_setup/,/^}/p' /root/wifi-build/rtw88/main.c"))

# 2. The EXACT rtw_mac_power_on function
print("\n=== rtw_mac_power_on (full) ===")
print(run(r"sed -n '/^int rtw_mac_power_on/,/^}/p' /root/wifi-build/rtw88/mac.c"))

# 3. The EXACT rtw_mac_power_switch function
print("\n=== rtw_mac_power_switch (full) ===")
print(run(r"sed -n '/^static int rtw_mac_power_switch/,/^}/p' /root/wifi-build/rtw88/mac.c"))

# 4. The EXACT rtw88xxa_power_on function
print("\n=== rtw88xxa_power_on (full) ===")
print(run(r"sed -n '/^int rtw88xxa_power_on/,/^}/p' /root/wifi-build/rtw88/rtw88xxa.c"))

# 5. The EXACT rtw88xxau_init_power_on function
print("\n=== rtw88xxau_init_power_on (full) ===")
print(run(r"sed -n '/^.*rtw88xxau_init_power_on/,/^}/p' /root/wifi-build/rtw88/rtw88xxa.c"))

# 6. Check the power sequence for 8821a
print("\n=== 8821a power sequences ===")
print(run(r"grep -n 'pwr_on_seq\|pwr_off_seq\|pwr_track_tbl' /root/wifi-build/rtw88/rtw8821a.c | head -20"))
print(run(r"grep -n 'pwr_on_seq\|pwr_off_seq' /root/wifi-build/rtw88/rtw8821a_table.c 2>/dev/null | head -10"))
print(run(r"grep -n 'pwr_on_seq\|pwr_off_seq' /root/wifi-build/rtw88/rtw8821a_table.h 2>/dev/null | head -10"))

# 7. Check the probe function in main.c to understand call order
print("\n=== Probe / chip_info_setup call order ===")
print(run(r"sed -n '/^int rtw_chip_info_setup/,/^}/p' /root/wifi-build/rtw88/main.c"))

# 8. Check rtw_pwr_seq_parser - where the actual hardware power sequence runs
print("\n=== rtw_pwr_seq_parser ===")
print(run(r"sed -n '/^static int rtw_pwr_seq_parser/,/^}/p' /root/wifi-build/rtw88/mac.c"))

# 9. Check rtw_pwr_cmd_polling  - where the actual polling happens
print("\n=== rtw_pwr_cmd_polling ===")
print(run(r"sed -n '/^static int rtw_pwr_cmd_polling/,/^}/p' /root/wifi-build/rtw88/mac.c"))

# 10. Check the REG_SYS_STATUS1 check for USB
print("\n=== REG_SYS_STATUS1 and REG_CR reads ===")
print(run(r"grep -n 'SYS_STATUS1\|REG_CR\|0xea' /root/wifi-build/rtw88/mac.c | head -20"))
print(run(r"grep -n 'REG_SYS_STATUS1\|0xf0' /root/wifi-build/rtw88/reg.h 2>/dev/null | head -10"))

# 11. Check if there's a USB-specific pre_init or chip detection
print("\n=== USB chip detection ===")
print(run(r"grep -n 'rtw_usb_probe\|chip_id\|lte_coex\|pre_init' /root/wifi-build/rtw88/usb.c | head -20"))

# 12. Full rtw_usb_probe
print("\n=== rtw_usb_probe function ===")
print(run(r"sed -n '/^static int rtw_usb_probe/,/^}/p' /root/wifi-build/rtw88/usb.c"))

# 13. Check what rtw_core_init does
print("\n=== rtw_core_init ===")
print(run(r"sed -n '/^int rtw_core_init/,/^}/p' /root/wifi-build/rtw88/main.c | head -60"))

# 14. Check if the register access returns errors via USB
print("\n=== rtw_usb_read/write implementation ===")
print(run(r"sed -n '/^static u8 rtw_usb_read8/,/^}/p' /root/wifi-build/rtw88/usb.c"))
print(run(r"sed -n '/^static int rtw_usb_read/,/^}/p' /root/wifi-build/rtw88/usb.c | head -30"))

client.close()
print("\n=== DONE ===")
