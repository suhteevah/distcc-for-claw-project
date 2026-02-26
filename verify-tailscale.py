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

# Check status
print("=== Tailscale Status ===")
print(run("tailscale status 2>&1"))

print("\n=== Tailscale IP ===")
print(run("tailscale ip -4 2>&1"))

print("\n=== Tailscale interface ===")
print(run("ip addr show tailscale0 2>&1"))

# If not logged in, authenticate
print("\n=== Check if auth needed ===")
status = run("tailscale status 2>&1")
if "Logged out" in status or "NeedsLogin" in status:
    TS_KEY = "***TS_AUTH_KEY_REDACTED***"
    print("Authenticating...")
    print(run(f"tailscale up --authkey={TS_KEY} --hostname=cnc-server 2>&1", timeout=30))
else:
    print("Already authenticated")

# Set hostname if needed
print("\n=== Set hostname ===")
print(run("tailscale set --hostname=cnc-server 2>&1"))

# Final status
print("\n=== Final Status ===")
print(run("tailscale status 2>&1"))

# Test connectivity
print("\n=== Test connectivity ===")
print(run(r"""
echo "Tailscale IPs:"
tailscale ip 2>&1
echo ""
echo "Ping test (Tailscale DERP):"
ping -c 2 -W 3 100.100.100.100 2>&1 | tail -3
"""))

client.close()
print("\n=== DONE ===")
