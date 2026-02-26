import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Reboot
print("=== Rebooting for full persistence test ===")
try:
    run("reboot", timeout=5)
except:
    pass
print("Reboot sent, waiting...")
client.close()

time.sleep(60)
for attempt in range(20):
    time.sleep(10)
    print(f"  Attempt {attempt+1}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)
        def run(cmd, timeout=120):
            stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            return out + err
        print("  CONNECTED!")
        break
    except:
        pass
else:
    print("Failed to reconnect!")
    exit(1)

# Wait for services to settle
time.sleep(15)

# Full status check
print("\n=== Post-Reboot Status ===")
print(run(r"""
echo "Hostname: $(hostname)"
echo "Kernel:   $(uname -r)"
echo "Uptime:   $(uptime)"
echo ""

echo "=== Services ==="
for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld; do
    STATUS=$(systemctl is-active $svc 2>&1)
    echo "  $svc: $STATUS"
done

echo ""
echo "=== Network Interfaces ==="
ip -br addr show 2>&1

echo ""
echo "=== WiFi Status ==="
wpa_cli -i wlp0s20u9 status 2>&1 | grep -E 'ssid|wpa_state|ip_address' || echo "WiFi not connected yet"

echo ""
echo "=== Tailscale ==="
tailscale ip -4 2>&1
tailscale status 2>&1 | head -5

echo ""
echo "=== Ollama ==="
curl -s http://localhost:11434/api/tags 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('models',[])), 'models available')" 2>&1

echo ""
echo "=== Ping Tests ==="
echo -n "  8.8.8.8: "
ping -c 1 -W 3 8.8.8.8 2>&1 | grep -oP '\d+\.\d+ ms' || echo "FAIL"
echo -n "  tailscale (self): "
ping -c 1 -W 3 100.108.202.49 2>&1 | grep -oP '\d+\.\d+ ms' || echo "FAIL"

echo ""
echo "=== Loaded rtw88 Modules ==="
lsmod | grep rtw
"""))

client.close()
print("\n=== REBOOT TEST COMPLETE ===")
