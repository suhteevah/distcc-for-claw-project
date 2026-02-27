#!/usr/bin/env python3
"""Check what inference engines/backends exo supports."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== All engine directories ==="
find src/exo/worker/engines -type d | grep -v __pycache__

echo ""
echo "=== Worker runner module ==="
find src/exo/worker/runner -type f -name '*.py' | grep -v __pycache__ | grep -v test

echo ""
echo "=== LLM inference runner ==="
cat src/exo/worker/runner/llm_inference/runner.py 2>&1 | head -80

echo ""
echo "=== Worker main - engine selection logic ==="
grep -n 'engine\|backend\|mlx\|torch\|cuda\|tinygrad\|pytorch' src/exo/worker/main.py 2>&1 | head -30

echo ""
echo "=== Check for tinygrad references ==="
grep -rn 'tinygrad' src/exo/ --include='*.py' | grep -v __pycache__ | head -10

echo ""
echo "=== Check for torch/cuda references in engines ==="
grep -rn 'torch\|cuda\|pytorch' src/exo/worker/engines/ --include='*.py' | grep -v __pycache__ | head -20

echo ""
echo "=== One sample model card (smallest model) ==="
cat resources/inference_model_cards/mlx-community--Qwen3-0.6B-4bit.toml

echo ""
echo "=== Llama 3.2 1B card ==="
cat resources/inference_model_cards/mlx-community--Llama-3.2-1B-Instruct-4bit.toml

echo ""
echo "=== Check git log for engine changes ==="
cd /opt/exo && git log --oneline -20 2>&1

echo ""
echo "=== exo version ==="
.venv/bin/python -c "import exo; print(exo.__version__)" 2>&1 || true
.venv/bin/pip show exo 2>&1 | head -5 || true
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
