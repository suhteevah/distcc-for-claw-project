import paramiko
import time
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Check if service started from previous attempt
print("=== Step 1: Check tailscaled ===")
print(run(r"""
systemctl is-active tailscaled 2>&1
ls -la /var/run/tailscale/tailscaled.sock 2>/dev/null && echo "Socket exists" || echo "No socket"
"""))

# Step 2: If not running, start it
print("\n=== Step 2: Ensure tailscaled is running ===")
print(run(r"""
if ! systemctl is-active tailscaled &>/dev/null; then
    echo "Starting tailscaled..."
    systemctl start tailscaled 2>&1
    sleep 3
fi
systemctl is-active tailscaled 2>&1
# Check socket
ls -la /var/run/tailscale/tailscaled.sock 2>&1
"""))

# Step 3: Authenticate with auth key
print("\n=== Step 3: Tailscale up ===")
TS_KEY = "***TS_AUTH_KEY_REDACTED***"
print(run(f"tailscale up --authkey={TS_KEY} --hostname=cnc-server 2>&1", timeout=30))
time.sleep(3)

# Step 4: Verify
print("\n=== Step 4: Verify ===")
print(run(r"""
echo "=== Tailscale IP ==="
tailscale ip -4 2>&1
echo ""
echo "=== Tailscale Status ==="
tailscale status 2>&1
echo ""
echo "=== Tailscale interface ==="
ip addr show tailscale0 2>/dev/null || echo "No tailscale0 interface"
"""))

client.close()
print("\n=== DONE ===")
