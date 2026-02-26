#!/usr/bin/env python3
"""Monitor cache growth on cnc-server to see download progress."""
import paramiko, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)

for i in range(5):
    stdin, stdout, stderr = c.exec_command("""
du -s /root/.cache/uv/ 2>&1 | cut -f1
ps aux | grep 'uv pip' | grep -v grep | wc -l
ls -la /root/.cache/uv/.tmp*/ 2>&1 | grep -E 'total|^d' | head -5
ss -tnp 2>&1 | grep -E 'uv|ESTAB.*443' | head -5
""", timeout=10)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    lines = out.split('\n')
    cache_kb = lines[0] if lines else "?"
    uv_running = lines[1] if len(lines) > 1 else "?"
    print(f"[{i}] cache={cache_kb}KB, uv_procs={uv_running}, {' '.join(lines[2:5])}")
    if i < 4:
        time.sleep(15)

c.close()
