import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Strategy: Download kernel-default-devel from SUSE OBS (openSUSE Build Service)
# The source RPM is kernel-default-6.12.0-160000.5.1.nosrc.rpm from SUSE
# We need to find the actual devel RPM on OBS or SCC
script = r"""#!/bin/bash
set -e

echo "=== Strategy: Find kernel-default-devel from SUSE OBS ==="
echo "Source RPM: kernel-default-6.12.0-160000.5.1.nosrc.rpm"
echo "VCS: https://src.suse.de/pool/kernel-source (slfo-1.2 branch)"

WORKDIR=/root/wifi-build
cd $WORKDIR

echo ""
echo "=== Try OBS repos for SUSE:SLFO:1.2 ==="
# The SLFO 1.2 project on OBS should have kernel-default-devel
URLS=(
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/1.2:/GA/standard/x86_64/"
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/1.2:/Update/standard/x86_64/"
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/Products:/Leap-Micro:/6.2:/Update/standard/x86_64/"
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/Products:/Leap-Micro:/6.2/standard/x86_64/"
    "https://download.opensuse.org/repositories/SUSE:/SLFO:/1.2:/GA/pool_sle/x86_64/"
    "https://download.opensuse.org/repositories/Kernel:/SLE16-SP0/standard/x86_64/"
    "https://download.opensuse.org/repositories/Kernel:/SLE16-SP0-LTSS/standard/x86_64/"
)

for url in "${URLS[@]}"; do
    echo ""
    echo "Trying: ${url}"
    result=$(curl -sL "${url}" 2>/dev/null | grep -o 'kernel-default-devel[^"]*\.rpm' | sort -u | head -5)
    if [ -n "$result" ]; then
        echo "  FOUND:"
        echo "$result" | sed 's/^/    /'
        # Try to download the matching version
        for rpm in $result; do
            if echo "$rpm" | grep -q "160000"; then
                echo "  >>> DOWNLOADING: ${rpm}"
                curl -sSL "${url}${rpm}" -o "${WORKDIR}/${rpm}" 2>/dev/null && echo "  >>> Downloaded!" || echo "  >>> Download failed"
            fi
        done
    else
        result2=$(curl -sL "${url}" 2>/dev/null | grep -o 'kernel[^"]*devel[^"]*\.rpm' | sort -u | head -5)
        if [ -n "$result2" ]; then
            echo "  Found kernel devel packages:"
            echo "$result2" | sed 's/^/    /'
        else
            echo "  (nothing kernel-related found)"
        fi
    fi
done

echo ""
echo "=== Check for downloaded RPMs ==="
ls -la ${WORKDIR}/kernel-default-devel*.rpm 2>/dev/null || echo "No kernel-default-devel RPMs downloaded"

echo ""
echo "=== Alternative: Try adding OBS repo and using zypper ==="
zypper ar -f -c 'https://download.opensuse.org/repositories/SUSE:/SLFO:/1.2:/GA/standard/' 'slfo-ga' 2>&1 || true
zypper --gpg-auto-import-keys ref 'slfo-ga' 2>&1 || true
zypper search -s -r 'slfo-ga' kernel-default-devel 2>&1 || true

echo ""
echo "=== Try another approach: download the kernel-syms RPM from OBS ==="
for url in "${URLS[@]}"; do
    result=$(curl -sL "${url}" 2>/dev/null | grep -o 'kernel-syms[^"]*\.rpm' | sort -u | head -5)
    if [ -n "$result" ]; then
        echo "kernel-syms at ${url}:"
        echo "$result" | sed 's/^/    /'
    fi
done
"""

chan = client.get_transport().open_session()
chan.settimeout(600)
chan.exec_command(f"cat > /root/fix-module-v4.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /root/fix-module-v4.sh 2>&1")

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
