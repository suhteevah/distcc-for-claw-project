import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Try listing the Leap Micro 6.2 repo directory for kernel packages ==="
curl -sL "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64/x86_64/" 2>&1 | grep -i 'kernel-default-devel' || echo "No kernel-default-devel in product repo"

echo ""
echo "=== Check if there's an update repo for Leap Micro 6.2 ==="
# Try common SUSE update repo patterns
for url in \
    "http://cdn.opensuse.org/update/leap-micro/6.2/" \
    "http://cdn.opensuse.org/update/leap-micro/6.2/product/" \
    "http://cdn.opensuse.org/update/leap-micro/6.2/sle/" \
    "http://download.opensuse.org/update/leap-micro/6.2/" \
    "https://download.opensuse.org/update/leap-micro/6.2/x86_64/" \
    "https://download.opensuse.org/update/leap-micro/6.2/product/repo/" \
    "http://cdn.opensuse.org/distribution/leap-micro/6.2/product/repo/openSUSE-Leap-Micro-6.2-x86_64-Source/" \
    ; do
    status=$(curl -sf -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    echo "  $status $url"
done

echo ""
echo "=== Check /lib/modules contents more carefully ==="
ls -la /lib/modules/6.12.0-160000.5-default/ | grep -E 'build|source|Module|symvers'

echo ""
echo "=== Check if Module.symvers exists ==="
find /lib/modules/6.12.0-160000.5-default/ -name 'Module.symvers' -o -name 'Kconfig' -o -name '.config' 2>/dev/null || echo "None found"

echo ""
echo "=== Check if kernel-default-extra has what we need ==="
rpm -ql kernel-default-extra 2>&1 | head -20

echo ""
echo "=== Check kernel-default-optional package contents ==="
rpm -ql kernel-default-optional 2>&1 | head -20

echo ""
echo "=== Alternative: Build module against running kernel using only /lib/modules data ==="
echo "Files we have:"
ls /lib/modules/6.12.0-160000.5-default/config
ls /lib/modules/6.12.0-160000.5-default/System.map
ls /lib/modules/6.12.0-160000.5-default/modules.builtin 2>/dev/null

echo ""
echo "=== Check for Module.symvers in the modules dir ==="
find /lib/modules/6.12.0-160000.5-default/ -maxdepth 1 -name '*.symvers' -o -name 'Module*' 2>/dev/null | head -10

echo ""
echo "=== Full listing of /lib/modules/$(uname -r)/ (top level only) ==="
ls -la /lib/modules/$(uname -r)/
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/get-headers.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/get-headers.sh",
    timeout=60
)
out = stdout.read().decode()
err = stderr.read().decode()
print(out, end="")
if err:
    print("STDERR:", err, end="")
client.close()
