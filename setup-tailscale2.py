import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Find where tailscaled service file might be, or create one
print("=== Step 1: Find/create tailscaled service ===")
print(run(r"""
# Check if service file exists anywhere
find / -name 'tailscaled.service' 2>/dev/null | head -5

# Check if tailscaled has --help for service options
tailscaled --help 2>&1 | head -5

# Check where it was installed
ls -la /usr/local/bin/tailscale*
"""))

# Step 2: Create systemd service file
print("\n=== Step 2: Create systemd service ===")
print(run(r"""
cat > /etc/systemd/system/tailscaled.service << 'EOF'
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/s/tailscaled
Wants=network-pre.target
After=network-pre.target NetworkManager.service systemd-resolved.service

[Service]
EnvironmentFile=-/etc/default/tailscaled
ExecStartPre=/usr/local/bin/tailscaled --cleanup
ExecStart=/usr/local/bin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock --port=${PORT:-0}
ExecStopPost=/usr/local/bin/tailscaled --cleanup
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

# Create defaults file
mkdir -p /etc/default
echo 'PORT=0' > /etc/default/tailscaled

systemctl daemon-reload
echo "Service file created"
"""))

# Step 3: Start tailscaled
print("\n=== Step 3: Start tailscaled ===")
print(run(r"""
systemctl enable tailscaled
systemctl start tailscaled
sleep 3
systemctl status tailscaled 2>&1 | head -10
"""))

# Step 4: Authenticate
print("\n=== Step 4: Tailscale up ===")
TS_KEY = "***TS_AUTH_KEY_REDACTED***"
print(run(f"tailscale up --authkey={TS_KEY} --hostname=cnc-server 2>&1", timeout=30))
time.sleep(3)

# Step 5: Verify
print("\n=== Step 5: Verify ===")
print(run(r"""
echo "=== Tailscale IP ==="
tailscale ip -4 2>&1
echo ""
echo "=== Tailscale Status ==="
tailscale status 2>&1
echo ""
echo "=== Ping tailscale gateway ==="
# Try pinging the MagicDNS
tailscale ping --timeout=5s 100.100.100.100 2>&1 || echo "No Tailscale peers to ping yet"
"""))

client.close()
print("\n=== DONE ===")
