import paramiko
import time
import sys

print("Waiting for cnc-server to come back online...")
for i in range(30):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        stdin, stdout, stderr = client.exec_command("echo OK && uname -r && uptime && snapper list | tail -5", timeout=15)
        output = stdout.read().decode()
        print(f"\n{output}")
        client.close()
        print("Server is back online!")
        sys.exit(0)
    except Exception as e:
        print(f"  Attempt {i+1}: {type(e).__name__}")
        time.sleep(5)

print("Server did not come back after 2.5 minutes")
sys.exit(1)
