#!/bin/sh
# roles/relay.sh — wireless relay overlay. Runs ON node. Idempotent. Touches wireless (dead-man armed by caller).
set -e
: "${FLEET_PSK:?FLEET_PSK not set}"
changed=0; log(){ echo "[relay] $*"; }
us(){ cur="$(uci -q get "$1" || true)"; [ "$cur" = "$2" ] || { uci set "$1=$2"; changed=1; log "set $1"; }; }

# radio0 = 2.4GHz Home_EXT ch6
us wireless.radio0.channel 6
us wireless.radio0.htmode HT20
us wireless.radio0.country US
us wireless.radio0.disabled 0
us wireless.default_radio0.mode ap
us wireless.default_radio0.network lan
us wireless.default_radio0.ssid Home_EXT
us wireless.default_radio0.encryption psk2
us wireless.default_radio0.key "$FLEET_PSK"
# radio1 = 5GHz Home_EXT ch149 AP
us wireless.radio1.channel 149
us wireless.radio1.htmode VHT40
us wireless.radio1.country US
us wireless.radio1.disabled 0
us wireless.default_radio1.mode ap
us wireless.default_radio1.network lan
us wireless.default_radio1.ssid Home_EXT
us wireless.default_radio1.encryption psk2
us wireless.default_radio1.key "$FLEET_PSK"
# mesh1 = 802.11s homemesh on radio1 ch149
[ "$(uci -q get wireless.mesh1)" = wifi-iface ] || { uci set wireless.mesh1=wifi-iface; changed=1; }
us wireless.mesh1.device radio1
us wireless.mesh1.network lan
us wireless.mesh1.mode mesh
us wireless.mesh1.mesh_id homemesh
us wireless.mesh1.encryption none
us wireless.mesh1.rts 256
us wireless.mesh1.frag 1024
# br-lan dhcp client
us network.lan.proto dhcp
uci -q delete network.lan.ipaddr || true
uci -q delete network.lan.netmask || true
# watchcat on (relay safety net)
/etc/init.d/watchcat enabled 2>/dev/null || { apk add watchcat 2>/dev/null || true; /etc/init.d/watchcat enable; changed=1; log "watchcat on"; }

uci commit
[ "$changed" = 1 ] && { wifi reload; /etc/init.d/network reload; }
log "relay overlay done (changed=$changed)"; echo "ROLE-OK"
