#!/usr/bin/env python3
"""Generate SSH keypair for accessing satibook remotely.
Creates a keypair that can be installed on satibook for passwordless SSH."""
import paramiko
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

KEY_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(KEY_DIR, "satibook-key")
PUB_FILE = KEY_FILE + ".pub"

# Generate new RSA keypair
print("=== Generating SSH keypair for satibook ===")
key = paramiko.RSAKey.generate(4096)

# Save private key
key.write_private_key_file(KEY_FILE)
print(f"Private key: {KEY_FILE}")

# Save public key
pub_key_str = f"ssh-rsa {key.get_base64()} claude-code@claw-fleet"
with open(PUB_FILE, 'w') as f:
    f.write(pub_key_str + "\n")
print(f"Public key:  {PUB_FILE}")

print(f"\n=== Public key (copy to satibook) ===")
print(pub_key_str)

print(f"""
=== Setup Instructions ===

On satibook, run these commands:

  1. Open PowerShell as Administrator:
     mkdir C:\\Users\\<username>\\.ssh -Force

  2. Add the public key:
     Add-Content C:\\Users\\<username>\\.ssh\\authorized_keys "{pub_key_str}"

  3. Ensure sshd is running:
     Get-Service sshd
     Start-Service sshd
     Set-Service -Name sshd -StartupType Automatic

  4. For WSL2 SSH access (if needed):
     wsl -d Ubuntu -u root -- bash -c "mkdir -p /root/.ssh && echo '{pub_key_str}' >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys"

Or simpler: just put the public key file on the USB along with join-claw-fleet.ps1
and have the script install it automatically.

=== Testing connection ===
Once installed, test with:
  ssh -i "{KEY_FILE}" <username>@100.77.45.99
""")
