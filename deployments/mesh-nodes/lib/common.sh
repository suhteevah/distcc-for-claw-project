#!/usr/bin/env bash
# Shared helpers — sourced by audit.sh / deploy.sh on kokonoe (git-bash).
MESH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$MESH_DIR/manifest.tsv"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=8"
SSH_NOISE='post-quantum\|store now\|openssh.com/pq\|may need to be upgraded\|This session may be vulnerable\|Permanently added\|^Warning: '

# manifest lookups (skip comment lines)
node_field() { awk -v n="$1" -v c="$2" '$1!~/^#/ && $1==n{print $c}' "$MANIFEST"; }
node_ip()   { node_field "$1" 3; }
node_role() { node_field "$1" 2; }
all_nodes() { awk '$1!~/^#/ && $2!="spare"{print $1}' "$MANIFEST"; }

node_ssh() { # node, remote-command-string
  local node="$1"; shift
  local ip; ip="$(node_ip "$node")"
  [ -n "$ip" ] || { echo "ERR: $node not in manifest" >&2; return 2; }
  ssh-keygen -f ~/.ssh/known_hosts -R "$ip" >/dev/null 2>&1
  ssh $SSH_OPTS "root@$ip" "$@" 2>&1 | grep -v "$SSH_NOISE"
}

push_file() { # node, localpath, remotepath
  local ip; ip="$(node_ip "$1")"
  cat "$2" | ssh $SSH_OPTS "root@$ip" "cat > $3"
}
