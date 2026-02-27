#!/usr/bin/env python3
"""Download model directly using huggingface_hub on kokonoe."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Step 1: Check where exo stores/looks for models
print("=" * 60)
print("  Step 1: Find model storage path")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== EXO model/data paths ==="
grep -n 'EXO_DATA_HOME\|models_dir\|MODELS_DIR\|model_path\|cache_dir\|HF_HOME' src/exo/shared/constants.py 2>&1 | head -20

echo ""
echo "=== Full constants.py ==="
cat src/exo/shared/constants.py 2>&1

echo ""
echo "=== Download utils - where models go ==="
grep -n 'ensure_models_dir\|models_dir\|snapshot_download\|hf_hub_download' src/exo/download/*.py 2>&1 | head -20

echo ""
echo "=== Check huggingface cache ==="
ls -la ~/.cache/huggingface/ 2>/dev/null
echo "---"
ls -la /root/.local/share/exo/ 2>/dev/null
echo "---"
ls -la /root/.cache/exo/ 2>/dev/null
"""],
    capture_output=True, text=True, timeout=15
)
print(result.stdout + result.stderr)
