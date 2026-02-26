#!/usr/bin/env python3
"""Install exo on cnc-server for distributed inference (CPU-only, 32GB RAM)."""

import paramiko
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected to cnc-server")

def run(cmd, timeout=600, label=None):
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
            lines = result.strip().split('\n')
            # Show first 10 and last 20 lines if long
            if len(lines) > 40:
                for line in lines[:10]:
                    print(f"  {line}")
                print(f"  ... ({len(lines) - 30} lines omitted) ...")
                for line in lines[-20:]:
                    print(f"  {line}")
            else:
                for line in lines:
                    print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# 1. Check prerequisites
run("""
echo "=== Python ==="
python3 --version 2>&1
echo ""
echo "=== Node ==="
node --version 2>&1 || echo "no node"
echo ""
echo "=== Rust ==="
rustc --version 2>&1 || echo "no rust"
echo ""
echo "=== uv ==="
uv --version 2>&1 || echo "no uv"
echo ""
echo "=== git ==="
git --version 2>&1
echo ""
echo "=== RAM ==="
free -h | head -2
echo ""
echo "=== Disk ==="
df -h / | tail -1
""", label="1. Check prerequisites")

# 2. Install uv if missing
run("""
if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh 2>&1
    export PATH="/root/.local/bin:$PATH"
    uv --version
else
    echo "uv already installed: $(uv --version)"
fi
""", label="2. Install uv")

# 3. Install Rust if missing
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
if ! command -v rustc &>/dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y 2>&1 | tail -5
    source /root/.cargo/env
    rustup toolchain install nightly 2>&1 | tail -3
    rustc --version
else
    echo "Rust already installed: $(rustc --version)"
    rustup toolchain install nightly 2>&1 | tail -3
fi
""", label="3. Install Rust", timeout=300)

# 4. Install Node if missing
run("""
if ! command -v node &>/dev/null; then
    echo "Installing Node.js..."
    # openSUSE Leap Micro - try zypper or manual
    if command -v zypper &>/dev/null; then
        zypper --non-interactive install -y nodejs20 npm20 2>&1 | tail -5
    fi
    node --version 2>&1 || echo "node not available, trying manual..."
fi
node --version 2>&1 || echo "WARN: node not available - dashboard won't build but exo still works"
""", label="4. Install Node.js")

# 5. Clone exo
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
if [ -d /opt/exo ]; then
    echo "exo already cloned, pulling latest..."
    cd /opt/exo && git pull 2>&1
else
    echo "Cloning exo..."
    git clone https://github.com/exo-explore/exo.git /opt/exo 2>&1
fi
echo ""
ls -la /opt/exo/ | head -10
""", label="5. Clone exo")

# 6. Build dashboard (if node available)
run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
if command -v node &>/dev/null && command -v npm &>/dev/null; then
    echo "Building dashboard..."
    cd /opt/exo/dashboard && npm install 2>&1 | tail -3 && npm run build 2>&1 | tail -3
    echo "Dashboard built"
else
    echo "Skipping dashboard (no node/npm) - exo will still work for inference"
fi
""", label="6. Build dashboard", timeout=300)

# 7. Build exo (uv run will compile Rust + install Python deps)
print("\n" + "="*60)
print("  7. Building exo (Rust compile + Python deps)")
print("  This may take 5-10 minutes...")
print("="*60)

run("""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
uv run exo --help 2>&1
""", label="7. Build exo", timeout=900)

client.close()
print("\nDone!")
