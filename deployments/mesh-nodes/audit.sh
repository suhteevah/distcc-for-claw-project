#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"; source lib/common.sh
node="${1:?usage: audit.sh <node>|all}"

audit_one() {
  local node="$1" role; role="$(node_role "$node")"
  echo "=== $node (role=$role) ==="
  # role-conditional expectations
  local want_watchcat=no want_rsyncd=no
  [ "$role" = relay ] && want_watchcat=yes
  [ "$role" = anchor ] && want_rsyncd=yes
  node_ssh "$node" '
    miss=""
    for p in tailscale prometheus-node-exporter-lua collectd banip dawn umdns; do
      apk info -e "$p" >/dev/null 2>&1 || miss="$miss $p"
    done
    chk(){ /etc/init.d/"$1" enabled 2>/dev/null && echo yes || echo no; }
    echo "pkgs_missing:${miss:- none}"
    echo "dnsmasq_enabled:$(chk dnsmasq)"
    echo "firewall_enabled:$(chk firewall)"
    echo "odhcpd_enabled:$(chk odhcpd)"
    echo "dawn_enabled:$(chk dawn)"
    echo "watchcat_enabled:$(chk watchcat)"
    echo "rsyncd_enabled:$(chk rsyncd)"
    echo "node_exporter_enabled:$(chk prometheus-node-exporter-lua)"
    echo "collectd_enabled:$(chk collectd)"
    echo "banip_enabled:$(chk banip)"
    echo "dhcp_ignore:$(uci -q get dhcp.lan.ignore || echo 0)"
    echo "log_ip:$(uci -q get system.@system[0].log_ip || echo none)"
    echo "mesh_id:$(uci -q get wireless.mesh1.mesh_id || echo none)"
  ' | awk -v ww="$want_watchcat" -v wr="$want_rsyncd" '
    {print "  "$0; split($0,a,":"); v[a[1]]=a[2]}
    END{
      bad=0
      if(v["pkgs_missing"]!=" none" && v["pkgs_missing"]!="none"){print "  DRIFT: missing pkgs"v["pkgs_missing"]; bad=1}
      if(v["dnsmasq_enabled"]=="yes"){print "  DRIFT: dnsmasq still enabled"; bad=1}
      if(v["firewall_enabled"]=="yes"){print "  DRIFT: firewall enabled (want dumb-AP off)"; bad=1}
      if(v["odhcpd_enabled"]=="yes"){print "  DRIFT: odhcpd enabled"; bad=1}
      if(v["dawn_enabled"]!="yes"){print "  DRIFT: dawn not enabled"; bad=1}
      if(v["dhcp_ignore"]!="1"){print "  DRIFT: dhcp.lan.ignore!=1"; bad=1}
      if(v["log_ip"]=="none"){print "  DRIFT: no remote log_ip"; bad=1}
      if(ww=="yes" && v["watchcat_enabled"]!="yes"){print "  DRIFT: watchcat expected on relay"; bad=1}
      if(wr=="yes" && v["rsyncd_enabled"]!="yes"){print "  DRIFT: rsyncd expected on anchor"; bad=1}
      print (bad?"  RESULT: DRIFT":"  RESULT: COMPLIANT")
    }'
}

if [ "$node" = all ]; then for n in $(all_nodes); do audit_one "$n"; done
else audit_one "$node"; fi
