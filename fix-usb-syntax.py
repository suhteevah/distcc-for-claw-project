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

# Step 1: Look at the damaged area around line 318
print("=== Step 1: Examine usb.c around the error ===")
print(run(r"sed -n '230,330p' /root/wifi-build/rtw88/usb.c"))

client.close()
print("\n=== DONE ===")
