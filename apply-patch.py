#!/usr/bin/env python3
"""Apply bootstrap peer patch to exo's swarm.rs. Run this ON the target machine."""
import sys

SWARM_RS = "/opt/exo/rust/networking/src/swarm.rs"

with open(SWARM_RS, "r") as f:
    content = f.read()

# Backup
with open(SWARM_RS + ".bak", "w") as f:
    f.write(content)

# 1. Add Multiaddr to imports
old_import = "use libp2p::{SwarmBuilder, identity};"
new_import = "use libp2p::{Multiaddr, SwarmBuilder, identity};"
content = content.replace(old_import, new_import)

# 2. Replace the listen_on line and add bootstrap peer support
old_listen = '    // Listen on all interfaces and whatever port the OS assigns\n    swarm.listen_on("/ip4/0.0.0.0/tcp/0".parse()?)?;\n    Ok(swarm)'

new_listen = """    // Listen on configurable port (EXO_LIBP2P_PORT env var, default: 0 = OS-assigned)
    let port = std::env::var("EXO_LIBP2P_PORT").unwrap_or_else(|_| "0".to_string());
    let listen_addr = format!("/ip4/0.0.0.0/tcp/{port}");
    log::info!("Listening on {listen_addr}");
    swarm.listen_on(listen_addr.parse()?)?;

    // Dial bootstrap peers if EXO_BOOTSTRAP_PEERS is set (comma-separated multiaddrs)
    // Example: EXO_BOOTSTRAP_PEERS=/ip4/100.108.202.49/tcp/42000
    if let Ok(peers_str) = std::env::var("EXO_BOOTSTRAP_PEERS") {
        for addr_str in peers_str.split(',') {
            let addr_str = addr_str.trim();
            if !addr_str.is_empty() {
                match addr_str.parse::<Multiaddr>() {
                    Ok(addr) => {
                        log::info!("Dialing bootstrap peer: {addr_str}");
                        if let Err(e) = swarm.dial(addr) {
                            log::error!("Failed to dial bootstrap peer {addr_str}: {e}");
                        }
                    }
                    Err(e) => {
                        log::error!("Invalid bootstrap peer multiaddr: {e}");
                    }
                }
            }
        }
    }

    Ok(swarm)"""

if old_listen in content:
    content = content.replace(old_listen, new_listen)
    print("PATCHED: listen_on + bootstrap peers added")
else:
    print("ERROR: Could not find expected code block")
    print("Searching for partial matches...")
    if 'listen_on("/ip4/0.0.0.0/tcp/0"' in content:
        print("  Found listen_on line but surrounding context differs")
    elif "listen_on" in content:
        print("  Found listen_on but format differs")
    else:
        print("  listen_on NOT FOUND")
    sys.exit(1)

if new_import in content:
    print("PATCHED: Multiaddr import added")
else:
    print("WARNING: Import may not have been updated")

with open(SWARM_RS, "w") as f:
    f.write(content)

print("Patch applied to " + SWARM_RS)
