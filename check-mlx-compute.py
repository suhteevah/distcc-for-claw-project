#!/usr/bin/env python3
"""Check if MLX can actually compute on our Linux nodes."""
import subprocess, paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MLX_TEST = r"""
cd /opt/exo
.venv/bin/python -c "
import sys
print(f'Python: {sys.version}')

# Check MLX
try:
    import mlx
    print(f'mlx module: {dir(mlx)}')
except Exception as e:
    print(f'mlx import error: {e}')

try:
    import mlx.core as mx
    print(f'mlx.core: OK')
    print(f'mx default device: {mx.default_device()}')

    # Try basic operations
    a = mx.array([1.0, 2.0, 3.0])
    b = mx.array([4.0, 5.0, 6.0])
    c = a + b
    mx.eval(c)
    print(f'Basic compute: {c.tolist()}')

    # Matrix multiply
    x = mx.ones((2, 3))
    y = mx.ones((3, 2))
    z = x @ y
    mx.eval(z)
    print(f'Matmul: {z.tolist()}')

    print('MLX COMPUTE: WORKING')
except Exception as e:
    print(f'MLX compute error: {e}')
    import traceback
    traceback.print_exc()

# Check mlx_lm
try:
    import mlx_lm
    print(f'mlx_lm version: {mlx_lm.__version__}')
except Exception as e:
    print(f'mlx_lm error: {e}')

# Check installed mlx package details
import importlib.metadata
try:
    dist = importlib.metadata.distribution('mlx')
    print(f'mlx package version: {dist.version}')
    print(f'mlx package location: {dist._path}')
except Exception as e:
    print(f'mlx metadata: {e}')
" 2>&1
"""

# Check kokonoe
print("=" * 60)
print("  kokonoe - MLX compute test")
print("=" * 60)
result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', MLX_TEST],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)

# Check cnc-server
print("=" * 60)
print("  cnc-server - MLX compute test")
print("=" * 60)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
stdin, stdout, stderr = c.exec_command(MLX_TEST, timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))
c.close()
