import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Search for libelf / gelf packages ==="
zypper search -s libelf 2>&1 | head -20
echo ""
zypper search -s elfutils 2>&1 | head -20

echo ""
echo "=== Try install ==="
transactional-update --non-interactive --continue pkg install \
    libelf-devel \
    2>&1
"""

chan = client.get_transport().open_session()
chan.settimeout(300)
chan.exec_command(f"cat > /root/inst-elf.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/inst-elf.sh 2>&1")

while True:
    if chan.recv_ready():
        data = chan.recv(4096).decode('utf-8', errors='replace')
        if data:
            print(data, end="")
            sys.stdout.flush()
    if chan.exit_status_ready():
        while chan.recv_ready():
            data = chan.recv(4096).decode('utf-8', errors='replace')
            if data:
                print(data, end="")
        break

print(f"\nExit code: {chan.recv_exit_status()}")
client.close()
