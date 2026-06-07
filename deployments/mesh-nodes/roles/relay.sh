#!/bin/sh
# roles/relay.sh — wireless relay overlay. Runs ON node. Idempotent. Wireless changes (dead-man armed by caller).
# watchcat files are PUSHED by deploy.sh (apk fetch for watchcat is unreliable on this fleet); we only enable here.
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
uci -q delete network.lan.ipaddr 2>/dev/null || true
uci -q delete network.lan.netmask 2>/dev/null || true

# commit wireless FIRST — never gated by later (watchcat) steps
uci commit
[ "$changed" = 1 ] && { wifi reload; /etc/init.d/network reload; log "wifi+net reloaded"; }

# watchcat (safety net) — files pushed by deploy.sh; enable non-fatally
if [ -x /etc/init.d/watchcat ]; then
  if ! ls /etc/rc.d/S??watchcat >/dev/null 2>&1; then
    /etc/init.d/watchcat enable 2>/dev/null && log "watchcat enabled" || log "watchcat enable failed (non-fatal)"
  fi
else
  log "WARN: watchcat not present (deploy.sh asset push missing) — skipping"
fi
log "relay overlay done (changed=$changed)"; echo "ROLE-OK"
