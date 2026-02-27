#!/usr/bin/env python3
"""Check if MLX can actually run on our Linux nodes."""
import subprocess, paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Check kokonoe
print("=" * 60)
print("  kokonoe - MLX compatibility check")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== Try importing mlx ==="
.venv/bin/python -c "
try:
    import mlx
    import mlx.core as mx
    print(f'MLX version: {mlx.__version__}')
    print(f'MLX available: True')
    # Try basic operation
    a = mx.array([1.0, 2.0, 3.0])
    print(f'Basic op: {a}')
except Exception as e:
    print(f'MLX import error: {e}')
" 2>&1

echo ""
echo "=== Platform info ==="
uname -a
python3 -c "import platform; print(platform.machine(), platform.system())"

echo ""
echo "=== Check mlx_lm ==="
.venv/bin/python -c "
try:
    import mlx_lm
    print(f'mlx_lm available: {mlx_lm.__version__}')
except Exception as e:
    print(f'mlx_lm error: {e}')
" 2>&1

echo ""
echo "=== Check if exo worker can start ==="
.venv/bin/python -c "
try:
    from exo.worker.runner.llm_inference.runner import LLMInferenceRunner
    print('LLMInferenceRunner imported OK')
except Exception as e:
    print(f'LLM runner import error: {e}')

try:
    from exo.worker.engines.mlx import Model
    print('MLX Model imported OK')
except Exception as e:
    print(f'MLX Model import error: {e}')
" 2>&1

echo ""
echo "=== Check old exo versions for other engines ==="
git log --all --oneline --grep='tinygrad\|pytorch\|torch\|cuda' 2>&1 | head -10
git tag | head -10 2>&1

echo ""
echo "=== Check branches ==="
git branch -a 2>&1 | head -20
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)

# Check cnc-server too
print("\n" + "=" * 60)
print("  cnc-server - MLX compatibility check")
print("=" * 60)

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

stdin, stdout, stderr = c.exec_command("""
cd /opt/exo

echo "=== Try importing mlx ==="
.venv/bin/python -c "
try:
    import mlx
    import mlx.core as mx
    print(f'MLX version: {mlx.__version__}')
except Exception as e:
    print(f'MLX import error: {e}')
" 2>&1

echo ""
echo "=== Platform info ==="
uname -a
""", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
