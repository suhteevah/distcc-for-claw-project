#!/usr/bin/env python3
"""Trigger model download via exo API and monitor progress."""
import subprocess, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Step 1: Check the start_download function signature
print("=" * 60)
print("  Step 1: Check download API format")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== start_download function ==="
sed -n '1696,1730p' src/exo/master/api.py

echo ""
echo "=== DownloadCommand type ==="
grep -rn 'class DownloadCommand\|class StartDownload\|class ForwarderDownload' src/exo/ --include='*.py' | grep -v __pycache__ | grep -v test | head -10

echo ""
echo "=== Download types ==="
cat src/exo/shared/types/api.py 2>/dev/null | grep -A20 'class.*Download' | head -40
"""],
    capture_output=True, text=True, timeout=15
)
print(result.stdout + result.stderr)

# Step 2: Trigger the download
print("\n" + "=" * 60)
print("  Step 2: Trigger download of Qwen3-0.6B-4bit")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
# Try POST /download/start with model_id
echo "=== Attempt 1: model_id in body ==="
curl -s -X POST http://localhost:52415/download/start \
  -H "Content-Type: application/json" \
  -d '{"model_id": "mlx-community/Qwen3-0.6B-4bit"}' 2>&1

echo ""
echo "=== Attempt 2: model field ==="
curl -s -X POST http://localhost:52415/download/start \
  -H "Content-Type: application/json" \
  -d '{"model": "mlx-community/Qwen3-0.6B-4bit"}' 2>&1

echo ""
echo "=== Attempt 3: with node_id ==="
# Get our node_id from logs
NODE_ID=$(grep 'Node elected' /tmp/exo-stdout.log | head -1)
echo "Master node context: $NODE_ID"

# Try with form data
echo ""
echo "=== Attempt 4: form params ==="
curl -s -X POST "http://localhost:52415/download/start?model_id=mlx-community/Qwen3-0.6B-4bit" 2>&1

echo ""
echo "=== Check log for download events ==="
tail -20 /tmp/exo-stdout.log 2>&1
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
