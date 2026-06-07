#!/bin/sh
# roles/anchor.sh — wired anchor overlay. Runs ON node. Idempotent.
set -e
: "${FLEET_PSK:?FLEET_PSK not set}"
changed=0; log(){ echo "[anchor] $*"; }
us(){ cur="$(uci -q get "$1" || true)"; [ "$cur" = "$2" ] || { uci set "$1=$2"; changed=1; log "set $1"; }; }

us wireless.radio0.channel 11
us wireless.radio0.htmode HT20
us wireless.radio0.country US
us wireless.radio0.disabled 0
us wireless.default_radio0.mode ap
us wireless.default_radio0.network lan
us wireless.default_radio0.ssid Home_EXT
us wireless.default_radio0.encryption psk2
us wireless.default_radio0.key "$FLEET_PSK"
us wireless.radio1.channel 149
us wireless.radio1.htmode VHT40
us wireless.radio1.country US
us wireless.radio1.disabled 0
[ "$(uci -q get wireless.mesh1)" = wifi-iface ] || { uci set wireless.mesh1=wifi-iface; changed=1; }
us wireless.mesh1.device radio1
us wireless.mesh1.network lan
us wireless.mesh1.mode mesh
us wireless.mesh1.mesh_id homemesh
us wireless.mesh1.encryption none
us network.lan.proto dhcp
# rsyncd on, watchcat OFF (anchor is wired/stable; watchcat reboot-loop risk)
/etc/init.d/rsyncd enabled 2>/dev/null || { apk add rsyncd 2>/dev/null || apk add rsync 2>/dev/null || true; /etc/init.d/rsyncd enable 2>/dev/null || true; changed=1; log "rsyncd on"; }
if /etc/init.d/watchcat enabled 2>/dev/null; then /etc/init.d/watchcat disable; changed=1; log "watchcat off"; fi

uci commit
[ "$changed" = 1 ] && { wifi reload; /etc/init.d/network reload; }
log "anchor overlay done (changed=$changed)"; echo "ROLE-OK"
