#!/usr/bin/env python3
"""Install NVIDIA G06 driver on cnc-server via transactional-update (separate snapshot from icecream)."""

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
# 1. Verify NVIDIA repo is available and packages exist
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== NVIDIA repo check ==="
zypper lr -u 2>&1 | grep -i nvidia
echo ""

echo "=== GPU detected ==="
lspci | grep -i vga
echo ""

echo "=== Available NVIDIA driver packages ==="
zypper se -s nvidia-driver-G06 nvidia-drivers-G06 nvidia-compute-G06 nvidia-common-G06 2>&1 | grep -v "^$" | head -20
echo ""

echo "=== Kernel firmware packages ==="
zypper se -s kernel-firmware-nvidia-gsp 2>&1 | grep -v "^$" | head -10
""", timeout=30, label="1. Verify NVIDIA packages available")

# ═══════════════════════════════════════════════════════════════════════
# 2. Install NVIDIA driver + compute via transactional-update
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Installing NVIDIA driver packages ==="
echo "This will create a new btrfs snapshot..."
echo ""

transactional-update --non-interactive pkg install \
    nvidia-driver-G06-kmp-default \
    nvidia-compute-G06 \
    nvidia-compute-utils-G06 \
    nvidia-common-G06 \
    kernel-firmware-nvidia-gsp-G06 \
    kernel-firmware-nvidia-gspx-G06 \
    2>&1 | tail -40

echo ""
echo "transactional-update exit: $?"
""", timeout=600, label="2. transactional-update NVIDIA driver")

# ═══════════════════════════════════════════════════════════════════════
# 3. Check snapshot status
# ═══════════════════════════════════════════════════════════════════════
run("""
echo "=== Snapshot status ==="
snapper list 2>&1 | tail -8
echo ""

echo "=== Pending changes ==="
PENDING=$(snapper list 2>&1 | grep "+" | tail -1)
if [ -n "$PENDING" ]; then
    echo "New snapshot ready: $PENDING"
    echo ""
    echo "⚠  REBOOT REQUIRED to activate:"
    echo "   - NVIDIA G06 driver (GTX 980 / Maxwell)"
    echo "   - Icecream distributed compiler"
    echo "   - distcc"
    echo ""
    echo "   Run 'reboot' when ready."
else
    echo "No pending snapshot found."
fi
""", label="3. Snapshot status")

client.close()
print("\nDone!")
