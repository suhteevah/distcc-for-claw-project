import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Adding openSUSE Leap 15.6 OSS repo for build tools ==="
# Leap Micro 6.2 is based on SLE/Leap 15.6 - we can add the full Leap repo
zypper ar -f -G https://download.opensuse.org/distribution/leap/15.6/repo/oss/ leap-oss 2>&1 || echo "repo might already exist"

echo ""
echo "=== Refreshing repos ==="
zypper --non-interactive ref 2>&1 | tail -5

echo ""
echo "=== Searching for gcc ==="
zypper se -s gcc | head -15

echo ""
echo "=== Searching for kernel-default-devel ==="
zypper se -s kernel-default-devel | head -10
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/add-repos.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/add-repos.sh",
    timeout=120
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print(err, end="")
client.close()
