import paramiko
import time
import sys

# Try multiple times with delays
for attempt in range(3):
    try:
        print(f"Attempt {attempt+1}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)
        stdin, stdout, stderr = client.exec_command("echo OK && uname -r && uptime", timeout=10)
        print(stdout.read().decode())
        client.close()
        print("SSH is working!")
        sys.exit(0)
    except Exception as e:
        print(f"  Failed: {e}")
        if attempt < 2:
            print("  Waiting 10 seconds...")
            time.sleep(10)

print("SSH is down. The kernel bug may have disrupted sshd.")
print("Attempting reboot via alternative method...")

# Try one more SSH to send reboot
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=30)
    client.exec_command("reboot", timeout=5)
    client.close()
    print("Reboot command sent")
except:
    print("Could not reboot via SSH. Machine may need physical reboot.")
