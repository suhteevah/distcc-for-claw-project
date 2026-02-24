import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# First check what openssl-devel packages are available
script = r"""#!/bin/bash
set -e

echo "=== Search for openssl devel ==="
zypper search -s openssl-devel libopenssl-devel 2>&1 | head -20

echo ""
echo "=== Try to install openssl devel ==="
transactional-update --non-interactive --continue pkg install \
    libopenssl-devel \
    2>&1

echo ""
echo "=== Done ==="
"""

chan = client.get_transport().open_session()
chan.settimeout(300)
chan.exec_command(f"cat > /root/inst-ssl.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/inst-ssl.sh 2>&1")

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
