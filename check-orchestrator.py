import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print("=" * 60)
print("  cnc-server Orchestrator Status Report")
print("=" * 60)

print("\n=== SYSTEM ===")
print(run('echo "Hostname: $(hostname)"; echo "Kernel: $(uname -r)"; echo "Uptime: $(uptime -p)"'))

print("=== SERVICES ===")
print(run('for svc in tailscaled ollama rtw88-wifi wpa-wifi dhcpcd-wifi firewalld agentapi; do STATUS=$(systemctl is-active $svc 2>&1); ENABLED=$(systemctl is-enabled $svc 2>&1); printf "  %-18s %-10s (%s)\n" "$svc" "$STATUS" "$ENABLED"; done'))

print("=== TOOLS ===")
print(run('for cmd in node claude agentapi ollama tailscale; do VER=$($cmd --version 2>&1 | head -1); printf "  %-12s %s\n" "$cmd:" "$VER"; done'))
print(run('/root/.deno/bin/deno --version 2>&1 | head -1 | xargs -I{} printf "  %-12s %s\n" "deno:" "{}"'))

print("=== NETWORK ===")
print(run('echo "  Ethernet: $(ip -4 addr show enp3s0 2>/dev/null | grep inet | awk \'{print $2}\')"; WLAN=$(ip link show 2>/dev/null | grep -oP "wl\\w+" | head -1); echo "  WiFi ($WLAN): $(ip -4 addr show $WLAN 2>/dev/null | grep "inet " | awk \'{print $2}\' | head -1)"; echo "  Tailscale: $(tailscale ip -4 2>&1)"'))

print("=== OLLAMA ===")
print(run("curl -s --max-time 5 http://localhost:11434/api/tags 2>&1 | python3 -c \"import json,sys; d=json.load(sys.stdin); print('  Models:', ', '.join(m['name'] for m in d.get('models',[])))\" 2>&1 || echo '  Ollama API not responding'"))

print("=== ICECREAM / DISTCC ===")
print(run('for cmd in iceccd icecc icecc-scheduler distcc distccd icecream-sundae; do which $cmd 2>/dev/null && echo "  $cmd: INSTALLED" || echo "  $cmd: not installed"; done'))

print("=== FIREWALL ===")
print(run('echo "  Trusted interfaces: $(firewall-cmd --zone=trusted --list-interfaces 2>&1)"; echo "  Open ports: $(firewall-cmd --list-ports 2>&1)"'))

print("=== GPU ===")
print(run('nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>/dev/null || echo "  No NVIDIA driver (nouveau: $(lspci | grep -i vga | grep -oP "NVIDIA.*" | head -1))"'))

print("=== SELinux ===")
print(run('echo "  Mode: $(getenforce)"'))

print("=== DISK ===")
print(run("df -h / /root | tail -2 | awk '{printf \"  %-20s %s used of %s (%s)\\n\", $6, $3, $2, $5}'"))

client.close()
print("=" * 60)
