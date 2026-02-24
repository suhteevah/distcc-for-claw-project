import paramiko
import time
import sys

host = "10.0.0.6"
username = "root"
password = "cnc-server-2024!"

print(f"Waiting for {host} to come back online...")
for attempt in range(30):
    time.sleep(10)
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, timeout=5)

        print(f"\nConnected after {(attempt+1)*10} seconds!")

        # Verify gcc is now available
        commands = [
            "gcc --version | head -1",
            "g++ --version | head -1",
            "make --version | head -1",
            "git --version",
            "uname -r",
            "hostname",
            "hostname -I",
            "snapper list | tail -5",
        ]

        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            print(f"  {cmd}: {out}")
            if err and 'warning' not in err.lower():
                print(f"    stderr: {err}")

        client.close()
        sys.exit(0)
    except Exception as e:
        print(f"  Attempt {attempt+1}: {e}")
        continue

print("Timed out waiting for server to come back!")
sys.exit(1)
