#!/usr/bin/env python3
"""Check exo swarm config and networking for cluster setup."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_ssh(host, password, cmd, label, timeout=30):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="root", password=password, timeout=30)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    result = out + err
    lines = result.strip().split('\n')
    for line in lines[:80]:
        print(f"  {line}")
    if len(lines) > 80:
        print(f"  ... ({len(lines) - 80} more lines)")
    c.close()
    return result

def run_wsl(cmd, label, timeout=30):
    print(f"\n{'='*60}")
    print(f"  [kokonoe WSL2] {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
        capture_output=True, text=True, timeout=timeout
    )
    out = result.stdout + result.stderr
    lines = out.strip().split('\n')
    for line in lines[:80]:
        print(f"  {line}")
    if len(lines) > 80:
        print(f"  ... ({len(lines) - 80} more lines)")
    return out

# Check swarm.rs for listen addresses
run_ssh("100.108.202.49", "cnc-server-2024!", r"""
cd /opt/exo
cat rust/networking/src/swarm.rs 2>&1
""", "cnc-server: swarm.rs")

# Check kokonoe WSL2 networking situation
run_wsl(r"""
echo "=== WSL2 IP addresses ==="
ip addr show 2>&1 | grep -E 'inet |^[0-9]'

echo ""
echo "=== Can reach cnc-server WiFi IP? ==="
ping -c 2 -W 2 10.0.0.142 2>&1

echo ""
echo "=== Can reach cnc-server Tailscale IP? ==="
ping -c 2 -W 2 100.108.202.49 2>&1

echo ""
echo "=== Tailscale in WSL2? ==="
which tailscale 2>&1
tailscale status 2>&1

echo ""
echo "=== WSL2 networking mode ==="
cat /proc/sys/net/ipv4/ip_forward 2>&1
cat /etc/resolv.conf 2>&1

echo ""
echo "=== Default route ==="
ip route | head -5
""", "kokonoe WSL2: networking check")

# Check avahi/mDNS availability
run_wsl(r"""
echo "=== avahi-daemon ==="
which avahi-daemon 2>&1
systemctl is-active avahi-daemon 2>&1
avahi-browse -a --no-db-lookup -t 2>&1 | head -20
""", "kokonoe WSL2: mDNS/avahi check")

run_ssh("100.108.202.49", "cnc-server-2024!", r"""
echo "=== avahi status ==="
which avahi-daemon 2>&1
systemctl status avahi-daemon 2>&1 | head -10
rpm -q avahi 2>&1

echo ""
echo "=== Can reach kokonoe? ==="
# Try WiFi subnet
ping -c 2 -W 2 10.0.0.100 2>&1
# Try Tailscale
ping -c 2 -W 2 100.90.71.97 2>&1
""", "cnc-server: mDNS/avahi & connectivity")
