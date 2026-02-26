import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Step 1: Create a systemd service to load WiFi modules on boot
print("=== Step 1: Create WiFi module loader service ===")
print(run(r"""
cat > /etc/systemd/system/rtw88-wifi.service << 'EOF'
[Unit]
Description=Load RTW88 WiFi driver modules (RTL8821AU)
After=network-pre.target
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c '\
    modprobe cfg80211 2>/dev/null; \
    modprobe mac80211 2>/dev/null; \
    sleep 1; \
    cd /root/wifi-build/rtw88 && \
    for mod in rtw_core rtw_usb rtw_88xxa rtw_8821a rtw_8821au; do \
        insmod ./${mod}.ko 2>/dev/null || true; \
    done; \
    sleep 2'
ExecStop=/bin/bash -c '\
    for mod in rtw_8821au rtw_8821a rtw_88xxa rtw_usb rtw_core; do \
        rmmod ${mod} 2>/dev/null || true; \
    done'

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable rtw88-wifi.service 2>&1
echo "rtw88-wifi service created and enabled"
"""))

# Step 2: Create wpa_supplicant service for the WiFi interface
print("\n=== Step 2: Create wpa_supplicant service ===")
print(run(r"""
cat > /etc/systemd/system/wpa-wifi.service << 'EOF'
[Unit]
Description=WPA Supplicant for WiFi (RTL8821AU)
After=rtw88-wifi.service
Wants=rtw88-wifi.service
BindsTo=sys-subsystem-net-devices-wlp0s20u9.device
After=sys-subsystem-net-devices-wlp0s20u9.device

[Service]
Type=simple
ExecStartPre=/bin/bash -c 'ip link set wlp0s20u9 up; sleep 1'
ExecStart=/usr/sbin/wpa_supplicant -i wlp0s20u9 -c /etc/wpa_supplicant/wpa_supplicant.conf
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable wpa-wifi.service 2>&1
echo "wpa-wifi service created and enabled"
"""))

# Step 3: Create dhcpcd service for the WiFi interface
print("\n=== Step 3: Create dhcpcd WiFi service ===")
print(run(r"""
cat > /etc/systemd/system/dhcpcd-wifi.service << 'EOF'
[Unit]
Description=DHCP Client for WiFi interface
After=wpa-wifi.service
Wants=wpa-wifi.service

[Service]
Type=forking
ExecStartPre=/bin/bash -c 'sleep 5'
ExecStart=/usr/sbin/dhcpcd wlp0s20u9
PIDFile=/var/run/dhcpcd/dhcpcd-wlp0s20u9.pid
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable dhcpcd-wifi.service 2>&1
echo "dhcpcd-wifi service created and enabled"
"""))

# Step 4: Verify tailscaled is enabled
print("\n=== Step 4: Verify tailscaled enabled ===")
print(run(r"""
systemctl is-enabled tailscaled 2>&1
"""))

# Step 5: Summary of all services
print("\n=== Step 5: Service summary ===")
print(run(r"""
echo "Boot order:"
echo "  1. rtw88-wifi.service  -> loads kernel modules"
echo "  2. wpa-wifi.service    -> connects to WiFi"
echo "  3. dhcpcd-wifi.service -> gets IP address"
echo "  4. tailscaled.service  -> Tailscale VPN"
echo ""
echo "Service states:"
for svc in rtw88-wifi wpa-wifi dhcpcd-wifi tailscaled; do
    STATUS=$(systemctl is-enabled ${svc} 2>&1)
    ACTIVE=$(systemctl is-active ${svc} 2>&1)
    echo "  ${svc}: enabled=${STATUS}, active=${ACTIVE}"
done
"""))

# Step 6: Current network state
print("\n=== Step 6: Current state ===")
print(run(r"""
echo "=== IP addresses ==="
ip -br addr show
echo ""
echo "=== WiFi status ==="
wpa_cli -i wlp0s20u9 status 2>&1 | grep -E 'ssid|wpa_state|ip_address' || echo "not connected"
echo ""
echo "=== Tailscale ==="
tailscale ip -4 2>&1
echo ""
echo "=== Ping test ==="
ping -c 1 -W 3 8.8.8.8 2>&1 | tail -1
"""))

client.close()
print("\n=== DONE ===")
