#!/usr/bin/env python3
"""Download Qwen3-0.6B-4bit model on kokonoe for exo inference."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("  Downloading mlx-community/Qwen3-0.6B-4bit on kokonoe")
print("  Size: ~327 MB")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

# Check how exo normalizes model IDs
echo "=== Check model ID normalization ==="
.venv/bin/python -c "
from exo.shared.types.common import ModelId
mid = ModelId('mlx-community/Qwen3-0.6B-4bit')
print(f'Model ID: {mid}')
print(f'Normalized: {mid.normalize() if hasattr(mid, \"normalize\") else \"no normalize method\"}')
" 2>&1

echo ""
echo "=== Download model using huggingface_hub ==="
.venv/bin/python -c "
import os
from pathlib import Path
from huggingface_hub import snapshot_download

model_id = 'mlx-community/Qwen3-0.6B-4bit'
models_dir = Path.home() / '.local/share/exo/models'
model_dir = models_dir / model_id.replace('/', '--')

# Also check with the slash-based path
model_dir_slash = models_dir / model_id

print(f'Models dir: {models_dir}')
print(f'Model dir (--): {model_dir}')
print(f'Model dir (/): {model_dir_slash}')
print(f'Exists (--): {model_dir.exists()}')
print(f'Exists (/): {model_dir_slash.exists()}')

# Check what normalize does
from exo.shared.types.common import ModelId
mid = ModelId(model_id)
norm = str(mid).replace('/', '--')
print(f'Normalized path would be: {models_dir / norm}')
" 2>&1

echo ""
echo "=== Download using exo's own download utils ==="
.venv/bin/python -c "
import asyncio
from exo.download.download_utils import ensure_models_dir

async def main():
    models_dir = await ensure_models_dir()
    print(f'exo models dir: {models_dir}')

asyncio.run(main())
" 2>&1

echo ""
echo "=== List existing model dirs ==="
find /root/.local/share/exo/models/ -maxdepth 2 -type d 2>/dev/null
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
