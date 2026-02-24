import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

print("Rebooting cnc-server...")
stdin, stdout, stderr = client.exec_command("reboot", timeout=5)
try:
    print(stdout.read().decode(), end="")
except:
    pass
try:
    client.close()
except:
    pass
print("Reboot command sent. Waiting for machine to come back...")
