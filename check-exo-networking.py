#!/usr/bin/env python3
"""Deeper investigation of exo's peer discovery and networking."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

def run(cmd, label, timeout=30):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    result = out + err
    lines = result.strip().split('\n')
    for line in lines[:80]:
        print(f"  {line}")
    if len(lines) > 80:
        print(f"  ... ({len(lines) - 80} more lines)")
    return result

# Find where router/networking lives
run("""
cd /opt/exo
find src/exo/routing -type f -name '*.py' 2>&1
find src/exo -type f -name '*.py' | xargs grep -l 'libp2p\|mDNS\|mdns\|swarm\|listen\|multiaddr' 2>&1 | head -20
""", "Find networking files")

# Check router code
run("""
cd /opt/exo
cat src/exo/routing/router.py 2>&1 | head -120
""", "Router code (head)")

# Check for libp2p config
run("""
cd /opt/exo
grep -rn 'EXO_LIBP2P\|libp2p\|NAMESPACE\|listen_addr\|multiaddr\|bootstrap\|peer_id\|dial\|mDNS\|mdns' src/exo/ --include='*.py' 2>&1 | head -40
""", "libp2p config references")

# Check Rust networking code (the actual libp2p implementation is in Rust)
run("""
cd /opt/exo
find rust/ -name '*.rs' 2>&1 | head -20
echo ""
echo "=== networking crate ==="
ls rust/networking/src/ 2>&1
""", "Rust networking files")

# Check the networking Rust code for mDNS and peer config
run("""
cd /opt/exo
grep -rn 'mdns\|mDNS\|bootstrap\|listen\|addr\|NAMESPACE\|peer\|dial\|swarm' rust/networking/src/ --include='*.rs' 2>&1 | head -50
""", "Rust networking config")

# Check Rust main for listen address config
run("""
cd /opt/exo
cat rust/networking/src/lib.rs 2>&1 | head -100
""", "Networking lib.rs (head)")

# Check constants/env vars
run("""
cd /opt/exo
cat src/exo/shared/constants.py 2>&1
""", "Constants/env vars")

# Check if there's a config file or environment approach
run("""
cd /opt/exo
grep -rn 'LISTEN\|ADDR\|PORT\|INTERFACE\|BIND' src/exo/ rust/ --include='*.py' --include='*.rs' 2>&1 | grep -iv 'api_port\|http\|import' | head -30
""", "Listen/bind config")

c.close()
print("\nDone!")
