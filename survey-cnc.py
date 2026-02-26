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

# Survey what's available
print("=== System Info ===")
print(run("uname -a && cat /etc/os-release | head -5"))

print("\n=== CPU/GPU/RAM ===")
print(run(r"""
echo "CPU: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
echo "Cores: $(nproc)"
echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
echo "GPU:"
lspci | grep -i vga
nvidia-smi 2>/dev/null | head -10 || echo "  no nvidia-smi"
"""))

print("\n=== Package Manager ===")
print(run(r"""
which zypper && echo "zypper available"
which transactional-update && echo "transactional-update available"
which podman && echo "podman available"
which docker && echo "docker available" || echo "docker NOT available"
"""))

print("\n=== Development Tools ===")
print(run(r"""
for cmd in node npm git curl gcc g++ make clang python3 pip3 deno; do
    if which $cmd &>/dev/null; then
        VER=$($cmd --version 2>&1 | head -1)
        echo "  $cmd: $VER"
    else
        echo "  $cmd: NOT FOUND"
    fi
done
"""))

print("\n=== Claude/Agent Tools ===")
print(run(r"""
for cmd in claude agentapi ollama; do
    if which $cmd &>/dev/null; then
        VER=$($cmd --version 2>&1 | head -1)
        echo "  $cmd: $VER"
    else
        echo "  $cmd: NOT FOUND"
    fi
done
"""))

print("\n=== Icecream ===")
print(run(r"""
for cmd in iceccd icecc icecc-scheduler icecream-sundae; do
    which $cmd 2>/dev/null && echo "  $cmd: found" || echo "  $cmd: NOT FOUND"
done
"""))

print("\n=== Disk Space ===")
print(run("df -h / /root /var /tmp 2>/dev/null | head -10"))

print("\n=== Running Services ===")
print(run("systemctl list-units --type=service --state=running --no-pager --no-legend | head -20"))

print("\n=== Available Packages (quick search) ===")
print(run(r"""
for pkg in nodejs npm gcc clang icecream; do
    RESULT=$(zypper search $pkg 2>/dev/null | grep "^i\|^v\|^$pkg" | head -3)
    echo "  $pkg: $RESULT"
done
""", timeout=60))

print("\n=== Podman/Container Status ===")
print(run(r"""
podman version 2>&1 | head -3
podman ps -a 2>&1 | head -5
"""))

client.close()
print("\n=== DONE ===")
