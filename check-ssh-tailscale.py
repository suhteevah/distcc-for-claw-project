import paramiko
import time
import sys

# Try both IPs
for ip, name in [("100.108.202.49", "Tailscale"), ("10.0.0.6", "LAN")]:
    print(f"Trying {name} ({ip})...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username="root", password="cnc-server-2024!", timeout=15)
        stdin, stdout, stderr = client.exec_command("echo OK && uname -r && uptime", timeout=10)
        print(stdout.read().decode())
        client.close()
        print(f"SSH via {name} is working!")
        sys.exit(0)
    except Exception as e:
        print(f"  Failed: {type(e).__name__}: {e}")

print("\nBoth SSH connections failed. The kernel BUG likely killed sshd.")
print("The machine needs a physical reboot (power cycle).")
print("Please power cycle the cnc-server machine.")
