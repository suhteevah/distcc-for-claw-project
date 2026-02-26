#!/usr/bin/env python3
"""Try alternative approaches for NVIDIA driver on Leap Micro 6.2 (immutable OS)."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120, label=None):
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        if label:
            for line in result.strip().split('\n')[:80]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# ═══════════════════════════════════════════════════════════════════════
# 1. Check kernel version and availability of kernel-default-devel
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Running kernel ==="
uname -r
echo ""

echo "=== Installed kernel packages ==="
rpm -qa | grep kernel | sort
echo ""

echo "=== kernel-default-devel availability ==="
zypper se -s kernel-default-devel 2>&1 | head -20
echo ""

echo "=== Check if we're on Leap Micro ==="
cat /etc/os-release | head -5
""", timeout=30, label="1. Kernel & OS info")

# ═══════════════════════════════════════════════════════════════════════
# 2. Try installing just nvidia-drivers-G06 meta package (solver picks deps)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Trying nvidia-drivers-G06 meta package ==="
echo "This lets the solver figure out compatible versions..."
echo ""

# First, see what the solver would do (dry run)
zypper --non-interactive install --dry-run nvidia-drivers-G06 2>&1 | tail -30
""", timeout=60, label="2. Dry-run nvidia-drivers-G06")

# ═══════════════════════════════════════════════════════════════════════
# 3. Try nvidia-drivers-minimal-G06 (compute only, may skip kernel module)
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Trying nvidia-drivers-minimal-G06 (compute only) ==="
zypper --non-interactive install --dry-run nvidia-drivers-minimal-G06 2>&1 | tail -30
""", timeout=60, label="3. Dry-run nvidia-drivers-minimal-G06")

# ═══════════════════════════════════════════════════════════════════════
# 4. Check NVIDIA container toolkit as alternative
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== NVIDIA Container Toolkit packages ==="
zypper se nvidia-container 2>&1 | grep -v "^$" | head -15
echo ""

echo "=== Check if podman/docker is available ==="
which podman 2>/dev/null && podman --version || echo "podman not found"
which docker 2>/dev/null && docker --version || echo "docker not found"
echo ""

echo "=== openSUSE-repos-Leap-NVIDIA package ==="
echo "This may configure the proper NVIDIA repo for Leap Micro:"
zypper info openSUSE-repos-Leap-NVIDIA 2>&1 | head -20
""", timeout=30, label="4. Container toolkit & alternatives")

# ═══════════════════════════════════════════════════════════════════════
# 5. Try installing kernel-default-devel first, then driver
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Attempt: install kernel-default-devel ==="
KVER=$(uname -r | sed 's/-default//')
echo "Need kernel-default-devel for kernel $KVER"
echo ""

# Check exact version available
zypper se -s kernel-default-devel 2>&1 | grep "$KVER" || echo "Exact kernel version not found in repos"
echo ""

# Try anyway
zypper --non-interactive install --dry-run kernel-default-devel 2>&1 | tail -20
""", timeout=30, label="5. Attempt kernel-default-devel")

# ═══════════════════════════════════════════════════════════════════════
# 6. Summary and recommendation
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     NVIDIA Driver Status Summary                     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "GPU:     $(lspci | grep -i vga | cut -d: -f3)"
echo "Kernel:  $(uname -r)"
echo "OS:      $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')"
echo ""
echo "Current NVIDIA status:"
lsmod | grep -i nvidia && echo "  NVIDIA module LOADED" || echo "  No NVIDIA kernel module loaded"
echo ""
nvidia-smi 2>&1 | head -5 || echo "  nvidia-smi not available"
echo ""
echo "Icecream + distcc: READY (in snapshot #11, awaiting reboot)"
""", label="6. NVIDIA status summary")

client.close()
print("\nDone!")
