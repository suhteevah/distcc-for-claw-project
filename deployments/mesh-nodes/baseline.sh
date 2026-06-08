#!/bin/sh
# baseline.sh — idempotent fleet baseline, role-agnostic. Runs ON the node (busybox ash).
# Caller (deploy.sh) sets CNC_LOG_IP. Touches NO wireless (that's role overlays + dead-man).
set -e
: "${CNC_LOG_IP:?CNC_LOG_IP not set}"
changed=0
log(){ echo "[baseline] $*"; }
us(){ cur="$(uci -q get "$1" || true)"; [ "$cur" = "$2" ] || { uci set "$1=$2"; changed=1; log "set $1=$2 (was ${cur:-unset})"; }; }
disable_svc(){ if /etc/init.d/"$1" enabled 2>/dev/null; then /etc/init.d/"$1" disable; /etc/init.d/"$1" stop 2>/dev/null || true; changed=1; log "disabled $1"; fi; }
enable_svc(){ ls /etc/rc.d/S??"$1" >/dev/null 2>&1 || { /etc/init.d/"$1" enable; changed=1; log "enabled $1"; }; }  # symlink check (some init 'enabled' fns false-negative, e.g. banip)

# dumb-AP posture
disable_svc firewall
disable_svc odhcpd
disable_svc dnsmasq
us dhcp.lan.ignore 1

# remote syslog to cnc (busybox logd — no extra package)
us system.@system[0].log_ip   "$CNC_LOG_IP"
us system.@system[0].log_port "514"
us system.@system[0].log_proto "udp"

# node-exporter must listen on the LAN, not loopback (else the cnc prometheus can't scrape it;
# the prometheus container reaches nodes via LAN IP, not tailnet).
ne_if="$(uci -q get prometheus-node-exporter-lua.main.listen_interface || true)"
us prometheus-node-exporter-lua.main.listen_interface lan

# NTP: these routers have no RTC and busybox sysntpd won't step a huge boot offset
# (seen up to ~45h). A 15-min one-shot step keeps clocks correct after every reboot.
if ! grep -q 'ntpd -nq' /etc/crontabs/root 2>/dev/null; then
  mkdir -p /etc/crontabs
  echo '*/15 * * * * /usr/sbin/ntpd -nq -p 0.openwrt.pool.ntp.org >/dev/null 2>&1' >> /etc/crontabs/root
  changed=1; log "added ntpd-step cron"
fi

# Layer-0 services
enable_svc dawn
enable_svc collectd
enable_svc prometheus-node-exporter-lua
enable_svc banip
enable_svc umdns
enable_svc cron

uci commit
# restart logd so log_ip takes effect (cheap, non-wifi)
/etc/init.d/log restart 2>/dev/null || true
# (re)load crontab so the ntpd-step entry takes effect (cheap, non-wifi)
/etc/init.d/cron restart 2>/dev/null || true
# restart node-exporter only if its listen interface changed (apply the LAN bind)
[ "$ne_if" = lan ] || /etc/init.d/prometheus-node-exporter-lua restart 2>/dev/null || true
log "baseline complete (changed=$changed)"
echo "BASELINE-OK"
