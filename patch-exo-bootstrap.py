#!/usr/bin/env python3
"""Patch exo's swarm.rs to support bootstrap peers via EXO_BOOTSTRAP_PEERS env var.
Apply on both cnc-server and kokonoe WSL2, then rebuild."""
import paramiko, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# The patch: modify create_swarm in swarm.rs to support:
# 1. EXO_LIBP2P_PORT env var for fixed listen port (default: 0 = random)
# 2. EXO_BOOTSTRAP_PEERS env var for manual peer dialing (comma-separated multiaddrs)
PATCH_SCRIPT = r'''
cd /opt/exo

# Backup original
cp rust/networking/src/swarm.rs rust/networking/src/swarm.rs.bak

# Apply the patch using python for precision
python3 -c "
import re

with open('rust/networking/src/swarm.rs', 'r') as f:
    content = f.read()

# 1. Add Multiaddr to imports
old_import = 'use libp2p::{SwarmBuilder, identity};'
new_import = 'use libp2p::{Multiaddr, SwarmBuilder, identity};'
content = content.replace(old_import, new_import)

# 2. Replace the create_swarm function
old_fn = '''/// Create and configure a swarm which listens to all ports on OS
pub fn create_swarm(keypair: identity::Keypair) -> alias::AnyResult<Swarm> {
    let mut swarm = SwarmBuilder::with_existing_identity(keypair)
        .with_tokio()
        .with_other_transport(tcp_transport)?
        .with_behaviour(Behaviour::new)?
        .build();

    // Listen on all interfaces and whatever port the OS assigns
    swarm.listen_on(\"/ip4/0.0.0.0/tcp/0\".parse()?)?;
    Ok(swarm)
}'''

new_fn = '''/// Create and configure a swarm which listens to all ports on OS
pub fn create_swarm(keypair: identity::Keypair) -> alias::AnyResult<Swarm> {
    let mut swarm = SwarmBuilder::with_existing_identity(keypair)
        .with_tokio()
        .with_other_transport(tcp_transport)?
        .with_behaviour(Behaviour::new)?
        .build();

    // Listen on configurable port (EXO_LIBP2P_PORT env var, default: 0 = OS-assigned)
    let port = std::env::var(\"EXO_LIBP2P_PORT\").unwrap_or_else(|_| \"0\".to_string());
    let listen_addr = format!(\"/ip4/0.0.0.0/tcp/{port}\");
    log::info!(\"Listening on {listen_addr}\");
    swarm.listen_on(listen_addr.parse()?)?;

    // Dial bootstrap peers if EXO_BOOTSTRAP_PEERS is set (comma-separated multiaddrs)
    // Example: EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000,/ip4/10.0.0.1/tcp/42000
    if let Ok(peers_str) = std::env::var(\"EXO_BOOTSTRAP_PEERS\") {
        for addr_str in peers_str.split(',') {
            let addr_str = addr_str.trim();
            if !addr_str.is_empty() {
                match addr_str.parse::<Multiaddr>() {
                    Ok(addr) => {
                        log::info!(\"Dialing bootstrap peer: {addr_str}\");
                        if let Err(e) = swarm.dial(addr) {
                            log::error!(\"Failed to dial bootstrap peer {addr_str}: {e}\");
                        }
                    }
                    Err(e) => {
                        log::error!(\"Invalid bootstrap peer multiaddr '{addr_str}': {e}\");
                    }
                }
            }
        }
    }

    Ok(swarm)
}'''

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print('PATCHED: create_swarm function replaced successfully')
else:
    print('ERROR: Could not find exact create_swarm function to replace')
    print('Looking for partial match...')
    if 'create_swarm' in content:
        print('  create_swarm exists but text doesnt match exactly')
    else:
        print('  create_swarm NOT FOUND at all')
    import sys
    sys.exit(1)

if new_import in content:
    print('PATCHED: Multiaddr import added')
else:
    print('WARNING: Multiaddr import may not have been added')

with open('rust/networking/src/swarm.rs', 'w') as f:
    f.write(content)

print('Patch applied successfully')
" 2>&1

echo ""
echo "=== Diff ==="
diff rust/networking/src/swarm.rs.bak rust/networking/src/swarm.rs 2>&1 || true
'''

def run_ssh(host, password, cmd, label, timeout=120):
    print(f"\n{'='*60}")
    print(f"  [{host}] {label}")
    print(f"{'='*60}")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="root", password=password, timeout=30)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    result = out + err
    code = stdout.channel.recv_exit_status()
    lines = result.strip().split('\n')
    for line in lines[:60]:
        print(f"  {line}")
    if len(lines) > 60:
        print(f"  ... ({len(lines) - 60} more lines)")
    if code != 0:
        print(f"  [exit code: {code}]")
    c.close()
    return result, code

def run_wsl(cmd, label, timeout=120):
    print(f"\n{'='*60}")
    print(f"  [kokonoe WSL2] {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', cmd],
        capture_output=True, text=True, timeout=timeout
    )
    out = result.stdout + result.stderr
    lines = out.strip().split('\n')
    for line in lines[:60]:
        print(f"  {line}")
    if len(lines) > 60:
        print(f"  ... ({len(lines) - 60} more lines)")
    return out

# === Apply patch on cnc-server ===
run_ssh("100.108.202.49", "cnc-server-2024!", PATCH_SCRIPT, "Apply bootstrap peer patch")

# === Apply patch on kokonoe WSL2 ===
run_wsl(PATCH_SCRIPT, "Apply bootstrap peer patch")

# === Rebuild on cnc-server ===
run_ssh("100.108.202.49", "cnc-server-2024!", r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo/rust/exo_pyo3_bindings

echo "=== Rebuilding exo_pyo3_bindings ==="
VIRTUAL_ENV=/opt/exo/.venv /opt/exo/.venv/bin/python -m maturin develop --release 2>&1

echo ""
echo "BUILD_EXIT: $?"
""", "Rebuild Rust bindings", timeout=300)

# === Rebuild on kokonoe WSL2 ===
run_wsl(r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo/rust/exo_pyo3_bindings

echo "=== Rebuilding exo_pyo3_bindings ==="
VIRTUAL_ENV=/opt/exo/.venv /opt/exo/.venv/bin/python -m maturin develop --release 2>&1

echo ""
echo "BUILD_EXIT: $?"
""", "Rebuild Rust bindings", timeout=300)

# === Verify on both ===
run_ssh("100.108.202.49", "cnc-server-2024!", r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
.venv/bin/python -c "
from exo_pyo3_bindings import ConnectionUpdate, NetworkingHandle, Keypair
print('exo_pyo3_bindings OK')
" 2>&1

.venv/bin/python -m exo --help 2>&1 | head -5
echo "cnc-server READY"
""", "Verify cnc-server")

run_wsl(r"""
export PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
cd /opt/exo
.venv/bin/python -c "
from exo_pyo3_bindings import ConnectionUpdate, NetworkingHandle, Keypair
print('exo_pyo3_bindings OK')
" 2>&1

.venv/bin/python -m exo --help 2>&1 | head -5
echo "kokonoe READY"
""", "Verify kokonoe")

print("\n" + "="*60)
print("  PATCH COMPLETE")
print("="*60)
print("""
Both nodes now support:
  EXO_LIBP2P_PORT=42000    - Fixed listen port
  EXO_BOOTSTRAP_PEERS=/ip4/IP/tcp/PORT  - Manual peer dial

To connect the cluster:
  cnc-server:  EXO_LIBP2P_PORT=42000 python -m exo -v
  kokonoe:     EXO_LIBP2P_PORT=42001 EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000 python -m exo -v
""")
