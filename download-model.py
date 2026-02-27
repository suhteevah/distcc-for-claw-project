#!/usr/bin/env python3
"""Download Qwen3-0.6B-4bit model on kokonoe using exo's own downloader."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("  Downloading mlx-community/Qwen3-0.6B-4bit (~327MB)")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

# Use huggingface_hub to download to the exact path exo expects
.venv/bin/python << 'PYEOF'
import os
from pathlib import Path
from huggingface_hub import snapshot_download

model_id = "mlx-community/Qwen3-0.6B-4bit"
models_dir = Path("/root/.local/share/exo/models")
normalized = model_id.replace("/", "--")
target_dir = models_dir / normalized

print(f"Downloading {model_id} to {target_dir}")
os.makedirs(target_dir, exist_ok=True)

# Download using snapshot_download with local_dir to place files directly
result = snapshot_download(
    repo_id=model_id,
    local_dir=str(target_dir),
    local_dir_use_symlinks=False,
)
print(f"Downloaded to: {result}")

# Verify contents
print("\n=== Downloaded files ===")
for f in sorted(target_dir.iterdir()):
    if f.is_file():
        size_mb = f.stat().st_size / (1024*1024)
        print(f"  {size_mb:>8.1f} MB  {f.name}")
    elif f.is_dir():
        print(f"  [DIR]      {f.name}")
PYEOF
"""],
    capture_output=True, text=True, timeout=300
)
print(result.stdout + result.stderr)
