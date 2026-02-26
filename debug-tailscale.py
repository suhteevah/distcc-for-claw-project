import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Check why tailscaled fails
print("=== Journal logs for tailscaled ===")
print(run("journalctl -u tailscaled --no-pager -n 30 2>&1"))

print("\n=== Try running tailscaled directly ===")
print(run(r"""
# Try starting manually to see the error
mkdir -p /var/lib/tailscale /var/run/tailscale
/usr/local/bin/tailscaled --cleanup 2>&1
echo "Cleanup exit: $?"
"""))

print("\n=== Check TUN device ===")
print(run(r"""
ls -la /dev/net/tun 2>/dev/null && echo "TUN device exists" || echo "No TUN device"
modprobe tun 2>/dev/null
ls -la /dev/net/tun 2>/dev/null && echo "TUN device exists after modprobe" || echo "Still no TUN"
"""))

print("\n=== Check iptables/nftables ===")
print(run(r"""
which iptables 2>/dev/null && echo "iptables found" || echo "no iptables"
which nft 2>/dev/null && echo "nft found" || echo "no nft"
"""))

# Try starting without ExecStartPre
print("\n=== Try direct start (foreground, 5 sec) ===")
print(run(r"""
# Remove cleanup from service
cat > /etc/systemd/system/tailscaled.service << 'EOF'
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/s/tailscaled
Wants=network-pre.target
After=network-pre.target

[Service]
ExecStart=/usr/local/bin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock --port=0
Restart=on-failure
RuntimeDirectory=tailscale
RuntimeDirectoryMode=0755
StateDirectory=tailscale
StateDirectoryMode=0700
CacheDirectory=tailscale
CacheDirectoryMode=0750
Type=notify

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start tailscaled 2>&1
sleep 3
systemctl is-active tailscaled 2>&1
journalctl -u tailscaled --no-pager -n 15 2>&1
"""))

client.close()
print("\n=== DONE ===")
