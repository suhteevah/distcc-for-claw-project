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

# Step 1: Check if tailscale is already installed
print("=== Step 1: Check tailscale status ===")
print(run(r"""
which tailscale 2>/dev/null && echo "tailscale binary found" || echo "tailscale not found"
which tailscaled 2>/dev/null && echo "tailscaled binary found" || echo "tailscaled not found"
systemctl status tailscaled 2>/dev/null | head -5 || echo "tailscaled service not found"
"""))

# Step 2: Install tailscale via transactional-update if not present
print("\n=== Step 2: Install tailscale ===")
result = run(r"""
if ! which tailscale &>/dev/null; then
    echo "Installing tailscale..."
    # On MicroOS, use transactional-update for persistent installs
    # But first check if it's available as a package
    zypper -n search tailscale 2>&1 | head -10

    # Try direct zypper install (may work on Leap Micro)
    zypper -n install tailscale 2>&1 | tail -15

    # If zypper fails, try the official install script
    if ! which tailscale &>/dev/null; then
        echo "Trying official install script..."
        curl -fsSL https://tailscale.com/install.sh | sh 2>&1 | tail -15
    fi
else
    echo "tailscale already installed"
    tailscale version
fi
""", timeout=180)
print(result)

# Step 3: Start tailscaled if not running
print("\n=== Step 3: Start tailscaled ===")
print(run(r"""
systemctl enable tailscaled 2>&1
systemctl start tailscaled 2>&1
sleep 2
systemctl status tailscaled 2>&1 | head -8
"""))

# Step 4: Authenticate with auth key
print("\n=== Step 4: Tailscale up ===")
TS_KEY = "***TS_AUTH_KEY_REDACTED***"
result = run(f"""
tailscale status 2>&1
if tailscale status 2>&1 | grep -q "Logged out"; then
    echo "Logging in with auth key..."
    tailscale up --authkey={TS_KEY} --hostname=cnc-server 2>&1
    sleep 3
fi
tailscale status 2>&1
""", timeout=60)
print(result)

# Step 5: Verify connectivity
print("\n=== Step 5: Tailscale info ===")
print(run(r"""
echo "=== Tailscale IP ==="
tailscale ip -4 2>&1
tailscale ip -6 2>&1
echo ""
echo "=== Tailscale Status ==="
tailscale status 2>&1
echo ""
echo "=== Network interfaces ==="
ip addr show tailscale0 2>/dev/null || ip addr show | grep -A3 tailscale
"""))

client.close()
print("\n=== DONE ===")
