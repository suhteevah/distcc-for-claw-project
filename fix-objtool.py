import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Option 1: Download the RPM and extract just the headers (no install)
# Option 2: Force install with dependency break
# Option 3: Disable objtool in the kernel config
# Let's try option 1 first - extract headers from the RPM without installing
script = r"""#!/bin/bash
set -e

echo "=== Option 1: Download libelf-devel RPM and extract headers manually ==="
cd /root/wifi-build

# Download the RPM
zypper --non-interactive download libelf-devel 2>&1 || true

# Find the downloaded RPM
RPM=$(find /var/cache/zypp/packages -name 'libelf-devel*.rpm' 2>/dev/null | head -1)
if [ -z "$RPM" ]; then
    echo "Download via zypper didn't work, trying wget..."
    wget -q "https://download.opensuse.org/distribution/leap/15.6/repo/oss/x86_64/libelf-devel-0.185-150400.5.3.1.x86_64.rpm" \
        -O libelf-devel.rpm 2>&1
    RPM="/root/wifi-build/libelf-devel.rpm"
fi

if [ -f "$RPM" ]; then
    echo "Found RPM: $RPM"
    # Extract to a temp location
    mkdir -p /root/wifi-build/libelf-extract
    cd /root/wifi-build/libelf-extract
    rpm2cpio "$RPM" | cpio -idm 2>/dev/null
    echo "Extracted files:"
    find . -type f | head -20

    echo ""
    echo "=== Copy headers to system include dir ==="
    # Check if gelf.h is in the extract
    find . -name 'gelf.h' -o -name 'libelf.h' -o -name 'elf.h' | head -5

    # We need to copy to a location gcc can find
    # Use transactional-update shell for this
    echo ""
    echo "Headers from extracted RPM:"
    ls -la ./usr/include/*.h 2>/dev/null || echo "No headers in usr/include"
    ls -la ./usr/include/elfutils/*.h 2>/dev/null || echo "No elfutils headers"
else
    echo "Could not get RPM!"
fi
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/fix-obj.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-obj.sh 2>&1")

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
