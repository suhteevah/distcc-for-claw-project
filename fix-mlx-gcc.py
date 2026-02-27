#!/usr/bin/env python3
"""Fix MLX JIT compilation on Linux by creating a g++ wrapper with -fpermissive."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c',
     'echo \'#!/bin/bash\nexec /usr/bin/g++ -fpermissive "$@"\' > /usr/local/bin/g++ '
     '&& chmod +x /usr/local/bin/g++ '
     '&& echo "=== Wrapper ===" '
     '&& cat /usr/local/bin/g++ '
     '&& echo "=== Test ===" '
     '&& /usr/local/bin/g++ --version 2>&1 | head -1 '
     '&& rm -rf /tmp/mlx/ '
     '&& echo "MLX JIT cache cleared"'],
    capture_output=True, text=True, timeout=10
)
print(result.stdout + result.stderr)
