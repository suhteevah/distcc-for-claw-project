#!/usr/bin/env bash
# Build a baked OpenWrt 25.12.3 image for AC-1304 (google_wifi) with the Layer-0 baseline packages.
# Runs on a Linux host (cnc). Output: factory.bin + sysupgrade.bin in $OUT.
set -euo pipefail
VER=25.12.3; TARGET=ipq40xx/chromium; PROFILE=google_wifi
WORK="${WORK:-/opt/owrt-ib}"; OUT="${OUT:-/opt/owrt-ib/out}"
PKGS="$(grep -vE '^[[:space:]]*#|^[[:space:]]*$' "$(dirname "$0")/../packages.list" | tr '\n' ' ')"
mkdir -p "$WORK" "$OUT"; cd "$WORK"
IB="openwrt-imagebuilder-${VER}-ipq40xx-chromium.Linux-x86_64"
if [ ! -d "$IB" ]; then
  curl -fSLO "https://downloads.openwrt.org/releases/${VER}/targets/${TARGET}/${IB}.tar.zst"
  tar --use-compress-program=unzstd -xf "${IB}.tar.zst"
fi
cd "$IB"
# cnc (MicroOS) lacks GNU 'patch'; a package-only image assembly never uses it, and FORCE=1 doesn't
# skip the .prereq-build target — so satisfy the stamp directly.
mkdir -p staging_dir/host && touch staging_dir/host/.prereq-build
echo "Building $PROFILE with: $PKGS"
make image PROFILE="$PROFILE" PACKAGES="$PKGS" BIN_DIR="$OUT"
echo "=== built ==="
ls -la "$OUT"/*google_wifi*squashfs-{factory,sysupgrade}.bin
sha256sum "$OUT"/*google_wifi*squashfs-*.bin
