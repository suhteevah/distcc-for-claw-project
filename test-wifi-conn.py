#!/usr/bin/env python3
"""Test connectivity to cnc-server after ethernet unplug."""

import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PASS = "cnc-server-2024!"

for host, label in [("10.0.0.25", "WiFi LAN"), ("100.108.202.49", "Tailscale")]:
    print(f"Trying {label} ({host})...")
    try:
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host, username="root", password=PASS, timeout=8)
        stdin, stdout, stderr = c.exec_command(
            "echo OK; hostname; uptime;"
            " ip -brief addr show | grep -v lo;"
            " echo '---';"
            " for svc in claude-orchestrator claude-agentapi ollama iceccd icecc-scheduler tailscaled; do"
            "   echo \"$svc: $(systemctl is-active $svc)\";"
            " done;"
            " echo '---';"
            " curl -s -o /dev/null -w 'Orchestrator: HTTP %{http_code}' http://localhost:8080/api/health;"
            " echo;"
            " curl -s -o /dev/null -w 'Ollama: HTTP %{http_code}' http://localhost:11434;"
            " echo",
            timeout=15
        )
        out = stdout.read().decode("utf-8", "replace")
        err = stderr.read().decode("utf-8", "replace")
        print(out)
        if err.strip():
            print(err)
        c.close()
        print(f"\n✅ {label} connection SUCCESS")
        break
    except Exception as e:
        print(f"  ✗ {label} failed: {e}\n")
else:
    print("\n❌ Could not reach cnc-server on either WiFi or Tailscale")
