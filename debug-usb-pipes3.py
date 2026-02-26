import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# 1. Get the function that contains line 1087 (calls rtw_usb_parse)
print("=== 1. Function containing rtw_usb_parse call (lines 1070-1110) ===")
print(run(r"sed -n '1070,1110p' /root/wifi-build/rtw88/usb.c"))

# 2. Get full rtw_usb_probe (line 1291+)
print("\n=== 2. rtw_usb_probe (lines 1285-1400) ===")
print(run(r"sed -n '1285,1400p' /root/wifi-build/rtw88/usb.c"))

# 3. Find the function that starts before line 1080
print("\n=== 3. Function starting before line 1080 ===")
print(run(r"sed -n '1060,1100p' /root/wifi-build/rtw88/usb.c"))

# 4. Check if pipe_in is used in a way I'm missing
print("\n=== 4. All pipe_in and pipe_interrupt uses ===")
print(run(r"grep -n 'pipe_in\b\|pipe_interrupt' /root/wifi-build/rtw88/usb.c"))

# 5. Check the full function at around 1080
print("\n=== 5. Function around 1080 (broader) ===")
print(run(r"sed -n '1050,1104p' /root/wifi-build/rtw88/usb.c"))

# 6. Check what's ABOVE line 1291 - specifically the static int function def
print("\n=== 6. Lines 1290-1340 ===")
print(run(r"sed -n '1290,1340p' /root/wifi-build/rtw88/usb.c"))

# 7. Check if there's an rtw88xxau-specific USB init
print("\n=== 7. 8821au USB init ===")
print(run(r"grep -n 'parse\|pipe\|endpoint' /root/wifi-build/rtw88/rtw88xxa.c | grep -iv 'antenna\|tx_power\|rf_\|_path' | head -20"))

client.close()
print("\n=== DONE ===")
