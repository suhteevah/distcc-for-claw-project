# 06 — WiFi Configuration with NetworkManager

## Prerequisites

- The 8821au module is loaded (`lsmod | grep 8821au`)
- A wireless interface exists (`ip link show | grep wlan`)
- The TP-Link Archer T2U PLUS is plugged in via USB

## Configure WiFi via NetworkManager

Leap Micro uses NetworkManager by default.

### Option 1: nmcli (Command Line)

```bash
# List available networks
nmcli dev wifi list

# Connect to your network
nmcli dev wifi connect "YourSSID" password "YourPassword"

# Verify connection
nmcli connection show --active
ip addr show wlan0
```

### Option 2: Connection File (Persistent)

Create a NetworkManager connection profile:

```bash
cat > /etc/NetworkManager/system-connections/home-wifi.nmconnection << 'EOF'
[connection]
id=home-wifi
type=wifi
autoconnect=true

[wifi]
ssid=YourSSID
mode=infrastructure

[wifi-security]
key-mgmt=wpa-psk
psk=YourPassword

[ipv4]
method=auto
EOF

chmod 600 /etc/NetworkManager/system-connections/home-wifi.nmconnection
nmcli connection reload
nmcli connection up home-wifi
```

### Option 3: Combustion (First Boot)

If you're setting up via combustion (USB installer first-boot), add WiFi config to the combustion `script`:

```bash
# In combustion/script:
mkdir -p /etc/NetworkManager/system-connections/
cat > /etc/NetworkManager/system-connections/home-wifi.nmconnection << WIFIEOF
[connection]
id=home-wifi
type=wifi
autoconnect=true

[wifi]
ssid=${WIFI_SSID}
mode=infrastructure

[wifi-security]
key-mgmt=wpa-psk
psk=${WIFI_PASSWORD}

[ipv4]
method=auto
WIFIEOF
chmod 600 /etc/NetworkManager/system-connections/home-wifi.nmconnection
```

## Verify WiFi is Working

```bash
# Check interface status
ip addr show wlan0

# Check route
ip route | grep wlan0

# Test connectivity
ping -c 3 8.8.8.8

# Check signal strength
iw dev wlan0 link
```

## Troubleshooting

- **No wlan0 interface:** Check `lsmod | grep 8821au` and `dmesg | grep 8821au`
- **Interface exists but no IP:** Run `nmcli dev wifi list` to scan, then connect
- **Connected but no internet:** Check DNS (`cat /etc/resolv.conf`) and routing (`ip route`)
- **Disconnects frequently:** USB power management may be interfering — disable USB autosuspend for the device
