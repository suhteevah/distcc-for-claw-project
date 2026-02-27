#!/usr/bin/env python3
"""Download a small model via exo API and test inference."""
import subprocess, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Step 1: Check what API endpoints exist for download
print("=" * 60)
print("  Step 1: Find download API endpoints")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

# Check API routes
echo "=== API routes for download ==="
grep -n 'download\|@app\.\|router\.\|add_api_route' src/exo/master/api.py 2>&1 | head -40

echo ""
echo "=== Check for /download endpoint ==="
grep -n 'download' src/exo/master/api.py | head -30

echo ""
echo "=== Available models in the /v1/models list (filtered for small ones) ==="
curl -s http://localhost:52415/v1/models 2>&1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = data.get('data', [])
# Sort by storage size and show small ones
for m in sorted(models, key=lambda x: x.get('storage_size_megabytes', 9999999)):
    size_mb = m.get('storage_size_megabytes', 0)
    if size_mb < 5000:  # Under 5GB
        print(f'  {size_mb:>6} MB  {m[\"id\"]}')
" 2>&1

echo ""
echo "=== Try the download API ==="
# Try to initiate a download for the small Qwen3-0.6B model
curl -s -X POST http://localhost:52415/v1/download \
  -H "Content-Type: application/json" \
  -d '{"model": "mlx-community/Qwen3-0.6B-4bit"}' 2>&1 | python3 -m json.tool 2>&1

echo ""
echo "=== Check other download endpoints ==="
curl -s http://localhost:52415/v1/downloads 2>&1 | python3 -m json.tool 2>&1 | head -20
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
