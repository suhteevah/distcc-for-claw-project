import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

script = r"""#!/bin/bash
set -e

echo "=== Step 1: Try to add Leap Micro 6.2 SLE update repo ==="
# Try to find the actual repo structure
for subdir in "" "x86_64/" "repo/" "product/" "sle-updates/"; do
    url="http://cdn.opensuse.org/update/leap-micro/6.2/sle/${subdir}"
    status=$(curl -sf -o /dev/null -w "%{http_code}" "${url}repodata/repomd.xml" 2>/dev/null || echo "000")
    echo "  ${status} ${url}repodata/repomd.xml"
done

echo ""
echo "=== Try different update repo patterns ==="
for url in \
    "http://cdn.opensuse.org/update/leap-micro/6.2/sle/" \
    "http://cdn.opensuse.org/update/leap-micro/6.2/main/" \
    "http://cdn.opensuse.org/update/leap-micro/6.2/backports/" \
    ; do
    status=$(curl -sf -o /dev/null -w "%{http_code}" "${url}repodata/repomd.xml" 2>/dev/null || echo "000")
    echo "  ${status} ${url}"
done

echo ""
echo "=== Explore the update directory structure ==="
curl -sL "http://cdn.opensuse.org/update/leap-micro/6.2/" 2>&1 | grep -oP 'href="[^"]*"' | head -30

echo ""
echo "=== Look for repos in /etc/zypp/repos.d/ ==="
cat /etc/zypp/repos.d/*.repo 2>/dev/null || true

echo ""
echo "=== Check the zypp service file ==="
ls -la /etc/zypp/services.d/ 2>/dev/null || true
cat /etc/zypp/services.d/*.service 2>/dev/null || true

echo ""
echo "=== Try the download.opensuse.org patterns for update ==="
for url in \
    "https://download.opensuse.org/update/leap-micro/6.2/sle/" \
    "https://download.opensuse.org/update/leap-micro/6.2/sle/update/" \
    ; do
    status=$(curl -sf -o /dev/null -w "%{http_code}" "${url}repodata/repomd.xml" 2>/dev/null || echo "000")
    echo "  ${status} ${url}"
done
"""

stdin, stdout, stderr = client.exec_command(
    f"cat > /tmp/setup-kb.sh << 'ENDSCRIPT'\n{script}\nENDSCRIPT\nbash /tmp/setup-kb.sh",
    timeout=60
)
out = stdout.read().decode()
err = stderr.read().decode()
print(out, end="")
if err:
    print("STDERR:", err, end="")
client.close()
