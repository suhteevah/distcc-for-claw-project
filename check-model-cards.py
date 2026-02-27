#!/usr/bin/env python3
"""Check exo model cards and figure out what models we can run."""
import subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
cd /opt/exo

echo "=== Inference model cards directory ==="
ls -la resources/inference_model_cards/ 2>&1 | head -40

echo ""
echo "=== Image model cards directory ==="
ls -la resources/image_model_cards/ 2>&1 | head -40

echo ""
echo "=== Sample model card (smallest first) ==="
# Get the smallest model cards by file size
ls -lS resources/inference_model_cards/*.json 2>/dev/null | tail -5
echo "---"
# Show one model card to understand the format
cat resources/inference_model_cards/*.json 2>/dev/null | python3 -c "
import sys, json
cards = []
for line in sys.stdin:
    try:
        cards.append(json.loads(line))
    except:
        pass
# Try reading each file individually
import os, glob
for f in sorted(glob.glob('resources/inference_model_cards/*.json')):
    with open(f) as fh:
        try:
            card = json.loads(fh.read())
            cards.append((f, card))
        except:
            pass
# Print sorted by size
for path, card in sorted(cards, key=lambda x: x[1].get('display_size_gb', 999)):
    name = card.get('display_name', card.get('model_id', 'unknown'))
    size_gb = card.get('display_size_gb', '?')
    model_id = card.get('model_id', '?')
    task = card.get('task', '?')
    print(f'  {size_gb:>6} GB  {name:40s}  {model_id}  ({task})')
" 2>&1

echo ""
echo "=== model_cards.py get_model_cards logic ==="
head -80 src/exo/shared/models/model_cards.py 2>&1

echo ""
echo "=== Check for PyTorch/CUDA inference engine ==="
find src/exo/worker/engines -name '*.py' -type f | grep -v __pycache__ | grep -v test | head -20
grep -rn 'torch\|cuda\|pytorch\|tinygrad' src/exo/worker/engines/ --include='*.py' | grep -v __pycache__ | grep -v test | head -20
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)
