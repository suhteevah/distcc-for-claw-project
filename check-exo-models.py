#!/usr/bin/env python3
"""Check exo model registry and API module."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== Model cards / registry ==="
find src/exo -name '*card*' -o -name '*model*' -o -name '*registry*' | grep -v __pycache__ | grep -v test | head -30

echo ""
echo "=== API module ==="
find src/exo -path '*/api*' -type f | grep -v __pycache__ | grep -v test | head -20

echo ""
echo "=== Master module ==="
find src/exo/master -type f | grep -v __pycache__ | head -20

echo ""
echo "=== Worker module ==="
find src/exo/worker -type f -name '*.py' | grep -v __pycache__ | grep -v test | head -20

echo ""
echo "=== Download module ==="
find src/exo/download -type f -name '*.py' | grep -v __pycache__ | grep -v test | head -20

echo ""
echo "=== model_cards.py content (if exists) ==="
cat src/exo/shared/model_cards.py 2>/dev/null | head -100

echo ""
echo "=== Check for model ID definitions ==="
grep -rn 'class ModelCard\|class ModelId\|MODEL_CARDS\|model_cards' src/exo/ --include='*.py' | grep -v __pycache__ | grep -v test | head -20

echo ""
echo "=== main.py spawn_api logic ==="
grep -n -A5 'spawn_api\|no.api\|api_port' src/exo/main.py 2>&1 | head -40

echo ""
echo "=== API class ==="
cat src/exo/master/api.py 2>/dev/null | head -80
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
