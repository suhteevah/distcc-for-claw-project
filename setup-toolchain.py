import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Installing full build toolchain via transactional-update ==="
echo "This installs gcc, make, git, and dev tools from Leap 15.6 repo..."
echo "(kernel-default-devel will be wrong version, we'll handle that separately)"

transactional-update --non-interactive --continue pkg install \
    gcc gcc-c++ make cmake autoconf automake libtool \
    git wget curl tar unzip gzip bzip2 xz \
    kernel-default-devel \
    htop tmux screen \
    2>&1

echo ""
echo "=== transactional-update done ==="
echo "NOTE: A reboot is needed to activate the new snapshot."
echo "After reboot, gcc and build tools will be available."
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/setup-toolchain.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/setup-toolchain.sh",
    timeout=300
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print(err, end="")
client.close()
