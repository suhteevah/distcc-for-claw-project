#!/usr/bin/env python3
"""Check if exo/libp2p has any bootstrap peer mechanism."""
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
    for line in lines[:100]:
        print(f"  {line}")
    if len(lines) > 100:
        print(f"  ... ({len(lines) - 100} more lines)")
    return result

# Check pyo3 bindings for bootstrap/dial functions
run(r"""
cd /opt/exo
cat rust/exo_pyo3_bindings/src/networking.rs 2>&1
""", "pyo3 networking bindings")

# Check pyo3 stub file for available Python API
run(r"""
cd /opt/exo
cat rust/exo_pyo3_bindings/exo_pyo3_bindings.pyi 2>&1
""", "Python stub file (API)")

# Check the full behaviour code in discovery.rs
run(r"""
cd /opt/exo
wc -l rust/networking/src/discovery.rs
echo "---"
cat rust/networking/src/discovery.rs 2>&1
""", "Full discovery.rs")

# Check full swarm.rs behaviour module
run(r"""
cd /opt/exo
# Look for the behaviour module referenced in swarm.rs
grep -rn 'mod behaviour' rust/networking/src/swarm.rs 2>&1
cat rust/networking/src/swarm.rs 2>&1 | tail -80
""", "swarm.rs behaviour")

# Check main.py for how the networking handle is created
run(r"""
cd /opt/exo
grep -A 20 'NetworkingHandle\|create_swarm\|bootstrap\|dial\|seed\|connect_to' src/exo/main.py 2>&1
""", "main.py networking setup")

c.close()
print("\nDone!")
