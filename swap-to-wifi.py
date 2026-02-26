#!/usr/bin/env python3
"""Prepare cnc-server to run WiFi-only: verify WiFi, test connectivity, swap."""

import paramiko
import time
import sys
import io
import socket

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ETH_IP = "10.0.0.6"
USER = "root"
PASS = "cnc-server-2024!"
TAILSCALE_IP = "100.108.202.49"

def ssh_connect(host, timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=USER, password=PASS, timeout=timeout)
    return client

def run(client, cmd, timeout=60, label=None):
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        result = out + err
        if label:
            for line in result.strip().split('\n')[:60]:
                print(f"  {line}")
            if code != 0:
                print(f"  [exit code: {code}]")
        return result, code
    except Exception as e:
        if label:
            print(f"  ERROR: {e}")
        return str(e), 1

# Connect via ethernet first
client = ssh_connect(ETH_IP)

# ═══════════════════════════════════════════════════════════════════════
# 1. Check current WiFi status
# ═══════════════════════════════════════════════════════════════════════
run(client, """
echo "=== Network interfaces ==="
ip -brief addr show
echo ""

echo "=== WiFi interface state ==="
ip link show wlp0s20u9 2>&1 || ip link show wlan0 2>&1
echo ""

echo "=== wpa_supplicant status ==="
systemctl is-active wpa-wifi
wpa_cli -i wlp0s20u9 status 2>&1 || wpa_cli -i wlan0 status 2>&1
echo ""

echo "=== dhcpcd-wifi status ==="
systemctl is-active dhcpcd-wifi
echo ""

echo "=== WiFi driver ==="
dmesg | grep -i "rtw88\|wlan\|wlp0\|802.11" | tail -10
""", label="1. Current WiFi status")

# ═══════════════════════════════════════════════════════════════════════
# 2. Fix WiFi if not connected
# ═══════════════════════════════════════════════════════════════════════
run(client, """
echo "=== Checking if WiFi is associated ==="
WIFI_IF=""
for iface in wlp0s20u9 wlan0; do
    if ip link show $iface &>/dev/null; then
        WIFI_IF=$iface
        break
    fi
done

if [ -z "$WIFI_IF" ]; then
    echo "ERROR: No WiFi interface found!"
    exit 1
fi
echo "WiFi interface: $WIFI_IF"

STATE=$(wpa_cli -i $WIFI_IF status 2>&1 | grep "^wpa_state=" | cut -d= -f2)
echo "WPA state: $STATE"

if [ "$STATE" != "COMPLETED" ]; then
    echo ""
    echo "WiFi not connected. Restarting WiFi services..."

    # Bring interface up
    ip link set $WIFI_IF up
    sleep 1

    # Check if wpa_supplicant config exists
    echo "=== wpa_supplicant config ==="
    ls -la /etc/wpa_supplicant/ 2>&1
    cat /etc/wpa_supplicant/wpa_supplicant-${WIFI_IF}.conf 2>/dev/null | grep -v "psk=" || \
    cat /etc/wpa_supplicant/wpa_supplicant.conf 2>/dev/null | grep -v "psk="

    # Restart services
    systemctl restart wpa-wifi
    sleep 3
    systemctl restart dhcpcd-wifi
    sleep 5

    # Check again
    STATE=$(wpa_cli -i $WIFI_IF status 2>&1 | grep "^wpa_state=" | cut -d= -f2)
    echo ""
    echo "After restart - WPA state: $STATE"

    if [ "$STATE" != "COMPLETED" ]; then
        echo "Trying scan + reconnect..."
        wpa_cli -i $WIFI_IF scan 2>&1
        sleep 3
        wpa_cli -i $WIFI_IF scan_results 2>&1 | head -10
        wpa_cli -i $WIFI_IF reconnect 2>&1
        sleep 5
        STATE=$(wpa_cli -i $WIFI_IF status 2>&1 | grep "^wpa_state=" | cut -d= -f2)
        echo "After reconnect - WPA state: $STATE"
    fi
fi

echo ""
echo "=== WiFi IP address ==="
ip addr show $WIFI_IF | grep "inet "
echo ""
echo "=== Routes ==="
ip route | head -5
""", timeout=60, label="2. Fix WiFi connection")

# ═══════════════════════════════════════════════════════════════════════
# 3. Get the WiFi IP and test connectivity
# ═══════════════════════════════════════════════════════════════════════
wifi_ip_result, _ = run(client, """
for iface in wlp0s20u9 wlan0; do
    IP=$(ip addr show $iface 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
    if [ -n "$IP" ]; then
        echo "$IP"
        break
    fi
done
""")
wifi_ip = wifi_ip_result.strip()
print(f"\n  WiFi IP detected: '{wifi_ip}'")

if wifi_ip:
    # Test that we can reach the WiFi IP from here
    print(f"\n  Testing SSH to WiFi IP {wifi_ip}...")
    try:
        wifi_client = ssh_connect(wifi_ip, timeout=5)
        out, _ = run(wifi_client, "echo 'SSH via WiFi OK'; hostname")
        print(f"  ✓ SSH via WiFi IP works: {out.strip()}")
        wifi_client.close()
    except Exception as e:
        print(f"  ✗ SSH via WiFi IP FAILED: {e}")
        print("  WiFi may need more time or the interface isn't up yet")

# ═══════════════════════════════════════════════════════════════════════
# 4. Ensure firewall allows traffic on WiFi interface
# ═══════════════════════════════════════════════════════════════════════
run(client, """
echo "=== Current firewall zones ==="
firewall-cmd --get-active-zones
echo ""

# Find WiFi interface name
WIFI_IF=""
for iface in wlp0s20u9 wlan0; do
    if ip link show $iface &>/dev/null; then
        WIFI_IF=$iface
        break
    fi
done

echo "=== WiFi interface zone ==="
firewall-cmd --get-zone-of-interface=$WIFI_IF 2>&1

# Make sure WiFi is in the trusted zone (same as ethernet)
ZONE=$(firewall-cmd --get-zone-of-interface=$WIFI_IF 2>&1)
if [ "$ZONE" = "trusted" ]; then
    echo "WiFi already in trusted zone ✓"
else
    echo "Adding WiFi to trusted zone..."
    firewall-cmd --permanent --zone=trusted --add-interface=$WIFI_IF 2>&1
    firewall-cmd --reload 2>&1
    echo "Result: $(firewall-cmd --get-zone-of-interface=$WIFI_IF 2>&1)"
fi

echo ""
echo "=== All open ports in active zones ==="
for zone in $(firewall-cmd --get-active-zones | grep -v "^\s"); do
    echo "Zone: $zone"
    firewall-cmd --zone=$zone --list-all 2>&1 | grep -E "(interfaces|ports|services)" | head -5
    echo ""
done
""", label="4. Firewall config for WiFi")

# ═══════════════════════════════════════════════════════════════════════
# 5. Test all services via WiFi IP
# ═══════════════════════════════════════════════════════════════════════
if wifi_ip:
    run(client, f"""
echo "=== Testing endpoints via WiFi IP ({wifi_ip if wifi_ip else 'N/A'}) ==="
echo "Orchestrator: $(curl -s -o /dev/null -w 'HTTP %{{http_code}}' http://{wifi_ip}:8080/api/health 2>&1)"
echo "AgentAPI:     $(curl -s -o /dev/null -w 'HTTP %{{http_code}}' http://{wifi_ip}:3284 2>&1)"
echo "Ollama:       $(curl -s -o /dev/null -w 'HTTP %{{http_code}}' http://{wifi_ip}:11434 2>&1)"
echo ""
echo "=== Testing via Tailscale IP ({TAILSCALE_IP}) ==="
echo "Orchestrator: $(curl -s -o /dev/null -w 'HTTP %{{http_code}}' http://{TAILSCALE_IP}:8080/api/health 2>&1)"
echo "Ollama:       $(curl -s -o /dev/null -w 'HTTP %{{http_code}}' http://{TAILSCALE_IP}:11434 2>&1)"
echo ""
echo "=== DNS test (critical for WiFi-only) ==="
ping -c 1 -W 3 google.com 2>&1 | head -2
ping -c 1 -W 3 api.anthropic.com 2>&1 | head -2
""", label="5. Test services via WiFi")

# ═══════════════════════════════════════════════════════════════════════
# 6. Configure WiFi as primary (lower metric) for when ethernet is gone
# ═══════════════════════════════════════════════════════════════════════
run(client, """
WIFI_IF=""
for iface in wlp0s20u9 wlan0; do
    if ip link show $iface &>/dev/null; then
        WIFI_IF=$iface
        break
    fi
done

echo "=== Current route metrics ==="
ip route | grep default
echo ""
echo "When ethernet is unplugged, WiFi default route will become primary automatically."
echo ""

echo "=== Tailscale will re-route over WiFi ==="
tailscale status 2>&1 | head -6
""", label="6. Route configuration")

# ═══════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════
run(client, f"""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     WiFi Swap Readiness Check                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Ethernet IP:  $(ip addr show enp3s0 | grep 'inet ' | awk '{{print $2}}')"

WIFI_IF=""
for iface in wlp0s20u9 wlan0; do
    if ip link show $iface &>/dev/null; then
        WIFI_IF=$iface
        break
    fi
done

WIFI_IP=$(ip addr show $WIFI_IF 2>/dev/null | grep 'inet ' | awk '{{print $2}}')
WIFI_STATE=$(wpa_cli -i $WIFI_IF status 2>&1 | grep "^wpa_state=" | cut -d= -f2)
WIFI_SSID=$(wpa_cli -i $WIFI_IF status 2>&1 | grep "^ssid=" | cut -d= -f2)

echo "  WiFi IP:      $WIFI_IP"
echo "  WiFi SSID:    $WIFI_SSID"
echo "  WiFi State:   $WIFI_STATE"
echo "  Tailscale:    $(tailscale ip -4 2>&1)"
echo ""

if [ "$WIFI_STATE" = "COMPLETED" ] && [ -n "$WIFI_IP" ]; then
    echo "  ✅ READY TO SWAP — unplug ethernet when ready"
    echo ""
    echo "  After unplugging:"
    echo "    - SSH via WiFi:     ssh root@$(echo $WIFI_IP | cut -d/ -f1)"
    echo "    - SSH via Tailscale: ssh root@{TAILSCALE_IP}"
    echo "    - Orchestrator:     http://{TAILSCALE_IP}:8080"
    echo "    - Ollama:           http://{TAILSCALE_IP}:11434"
else
    echo "  ⚠️  WiFi NOT READY — do not unplug ethernet yet"
    echo "  WiFi state: $WIFI_STATE"
fi
""", label="SUMMARY")

client.close()
print("\nDone!")
