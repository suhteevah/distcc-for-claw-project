import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# The system has libelf.so already (from libelf1 package), we just need the symlink
# that -devel packages provide
script = r"""#!/bin/bash
set -e

echo "=== Check existing libelf files ==="
find / -name 'libelf*' -type f 2>/dev/null | grep -v snapshot

echo ""
echo "=== Create the missing -lelf symlink ==="
# libelf1 provides libelf.so.1, we need libelf.so for the linker
# The system has libelf.so.1 but not the unversioned symlink
ls -la /usr/lib64/libelf* 2>/dev/null || true

# Create the symlink - need transactional-update for read-only fs
transactional-update --non-interactive --continue shell <<'TUEOF'
# Create the linker symlink
if [ -f /usr/lib64/libelf.so.1 ]; then
    ln -sf libelf.so.1 /usr/lib64/libelf.so
    echo "Created /usr/lib64/libelf.so -> libelf.so.1"
elif [ -f /usr/lib64/libelf.so.0 ]; then
    ln -sf libelf.so.0 /usr/lib64/libelf.so
    echo "Created /usr/lib64/libelf.so -> libelf.so.0"
fi

# Also copy the static lib from extracted RPM if available
if [ -f /root/wifi-build/libelf-extract/usr/lib64/libelf.a ]; then
    cp /root/wifi-build/libelf-extract/usr/lib64/libelf.a /usr/lib64/
    echo "Copied libelf.a"
fi

ls -la /usr/lib64/libelf*
exit
TUEOF

echo ""
echo "=== Done - need reboot ==="
"""

chan = client.get_transport().open_session()
chan.settimeout(120)
chan.exec_command(f"cat > /root/fix-elf.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-elf.sh 2>&1")

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
