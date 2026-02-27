#!/usr/bin/env python3
"""Read full networking.rs from cnc-server."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
print("Connected")

stdin, stdout, stderr = c.exec_command("wc -l /opt/exo/rust/exo_pyo3_bindings/src/networking.rs", timeout=10)
print(stdout.read().decode())

stdin, stdout, stderr = c.exec_command("cat /opt/exo/rust/exo_pyo3_bindings/src/networking.rs", timeout=30)
content = stdout.read().decode('utf-8', errors='replace')
print(content)

c.close()
