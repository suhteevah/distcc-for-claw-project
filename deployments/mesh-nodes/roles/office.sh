#!/bin/sh
# roles/office.sh — wired 5GHz-only office AP overlay. Runs ON node. Idempotent.
set -e
: "${FLEET_PSK:?FLEET_PSK not set}"
changed=0; log(){ echo "[office] $*"; }
us(){ cur="$(uci -q get "$1" || true)"; [ "$cur" = "$2" ] || { uci set "$1=$2"; changed=1; log "set $1"; }; }

us wireless.radio0.disabled 1
us wireless.radio1.channel 36
us wireless.radio1.htmode VHT80
us wireless.radio1.country US
us wireless.radio1.disabled 0
us wireless.default_radio1.mode ap
us wireless.default_radio1.network lan
us wireless.default_radio1.ssid Home_EXT
us wireless.default_radio1.encryption psk2
us wireless.default_radio1.key "$FLEET_PSK"
# no mesh on the office node
if [ "$(uci -q get wireless.mesh1)" = wifi-iface ]; then uci delete wireless.mesh1; changed=1; log "mesh removed"; fi
us network.lan.proto dhcp
if /etc/init.d/watchcat enabled 2>/dev/null; then /etc/init.d/watchcat disable; changed=1; fi

uci commit
[ "$changed" = 1 ] && { wifi reload; /etc/init.d/network reload; }
log "office overlay done (changed=$changed)"; echo "ROLE-OK"
