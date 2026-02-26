#!/usr/bin/env python3
import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("100.108.202.49", username="root", password="cnc-server-2024!", timeout=30)
stdin, stdout, stderr = c.exec_command("free -h; echo '---'; cat /proc/meminfo | head -5; echo '---'; lscpu | head -15; echo '---'; lspci | grep -i 'vga\|nvidia\|3d'", timeout=30)
print(stdout.read().decode('utf-8', errors='replace'))
c.close()
