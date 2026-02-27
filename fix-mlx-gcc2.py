#!/usr/bin/env python3
"""Fix MLX JIT compilation on Linux by creating a g++ wrapper with -fpermissive."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Use Python inside WSL to write the file properly
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'python3', '-c', """
import os, stat

# Write the g++ wrapper
wrapper = '#!/bin/bash\\nexec /usr/bin/g++ -fpermissive "$@"\\n'
with open('/usr/local/bin/g++', 'w') as f:
    f.write(wrapper)
os.chmod('/usr/local/bin/g++', 0o755)

# Verify
with open('/usr/local/bin/g++', 'r') as f:
    print("=== Wrapper contents ===")
    print(repr(f.read()))

# Clear MLX JIT cache
import shutil
if os.path.exists('/tmp/mlx/'):
    shutil.rmtree('/tmp/mlx/')
    print("MLX JIT cache cleared")

print("Done!")
"""],
    capture_output=True, text=True, timeout=10
)
print(result.stdout + result.stderr)

# Test the wrapper works
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     '/usr/local/bin/g++ --version 2>&1 | head -1'],
    capture_output=True, text=True, timeout=10
)
print("g++ wrapper test:", result.stdout.strip())
