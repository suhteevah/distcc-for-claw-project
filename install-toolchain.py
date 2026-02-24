import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# First, let's check what repos we have and what's available
script = r"""#!/bin/bash
set -e

echo "=== Current repos ==="
zypper lr -u 2>&1 || true

echo ""
echo "=== Currently installed gcc/make/build? ==="
rpm -q gcc gcc-c++ make git 2>&1 || true

echo ""
echo "=== Check what zypper can resolve for just gcc gcc-c++ make ==="
zypper --non-interactive info gcc gcc-c++ make 2>&1 | head -80 || true

echo ""
echo "=== Kernel running ==="
uname -r

echo ""
echo "=== Search for kernel-devel packages ==="
zypper search -s kernel-devel 2>&1 || true
zypper search -s kernel-default-devel 2>&1 || true

echo ""
echo "=== Available kernel source/headers ==="
zypper search -s 'kernel*devel*' 2>&1 || true
zypper search -s 'kernel*source*' 2>&1 || true
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/check-toolchain.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/check-toolchain.sh",
    timeout=120
)
print(stdout.read().decode(), end="")
err = stderr.read().decode()
if err:
    print("STDERR:", err, end="")
client.close()
