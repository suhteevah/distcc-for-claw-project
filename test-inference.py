#!/usr/bin/env python3
"""Test exo inference via the OpenAI-compatible API."""
import subprocess, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Step 1: Check the API endpoints
print("=" * 60)
print("  Step 1: Check API - list models")
print("=" * 60)

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', """
# List available models
echo "=== GET /v1/models ==="
curl -s http://localhost:52415/v1/models 2>&1 | python3 -m json.tool 2>&1 | head -100

echo ""
echo "=== GET /v1/topology ==="
curl -s http://localhost:52415/v1/topology 2>&1 | python3 -m json.tool 2>&1 | head -50

echo ""
echo "=== GET / (root) ==="
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:52415/ 2>&1
echo ""
"""],
    capture_output=True, text=True, timeout=30
)
print(result.stdout + result.stderr)

# Step 2: Try a chat completion with the smallest model
print("=" * 60)
print("  Step 2: Try inference with Qwen3-0.6B-4bit (~340MB)")
print("=" * 60)
print("  (This will trigger model download + inference)")
print("  Sending request...")

result = subprocess.run(
    ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', 'bash', '-c', r"""
# Send a chat completion request with small model
curl -s --max-time 300 http://localhost:52415/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Qwen3-0.6B-4bit",
    "messages": [
      {"role": "user", "content": "Say hello in exactly 5 words."}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }' 2>&1

echo ""
echo "=== Check log after request ==="
tail -30 /tmp/exo-stdout.log 2>&1
"""],
    capture_output=True, text=True, timeout=360
)
print(result.stdout + result.stderr)
