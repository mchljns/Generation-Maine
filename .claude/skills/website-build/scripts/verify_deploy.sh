#!/usr/bin/env bash
# Verify that a static host is serving the file you just built, then wait out the CDN cache window
# and verify again, so "it's live" is only said when every address form returns the new build.
#
#   verify_deploy.sh <local-file> <public-url> [cache-seconds] [max-wait-seconds]
#
# Example: verify_deploy.sh dist/index.html https://user.github.io/site/v2/ 600 480
# Exit 0 only when the served sha1 matches the local sha1 after the cache window has passed.
set -u
LOCAL="${1:?local file}"; URL="${2:?public url}"; CACHE="${3:-600}"; MAXWAIT="${4:-480}"
L=$(sha1sum "$LOCAL" | cut -c1-8)
base="${URL%/}"
served() { curl -sL --max-time 20 "$1" | sha1sum | cut -c1-8; }
echo "local  $L  $LOCAL"
t=0
until [ "$(served "$base/index.html?n=$RANDOM")" = "$L" ]; do
  [ $t -ge $MAXWAIT ] && { echo "origin never matched within ${MAXWAIT}s"; exit 1; }
  sleep 15; t=$((t+15))
done
echo "origin matched after ${t}s; waiting out the ${CACHE}s cache window before calling it live"
sleep "$CACHE"
ok=1
for u in "$base/" "$base/index.html" "$base/?r=$RANDOM"; do
  h=$(served "$u"); age=$(curl -sIL --max-time 20 "$u" | tr -d '\r' | grep -i '^age:' | tail -1)
  printf '%-60s %s %s %s\n' "$u" "$h" "$([ "$h" = "$L" ] && echo match || echo STALE)" "$age"
  [ "$h" = "$L" ] || ok=0
done
[ $ok = 1 ] && echo "LIVE: all address forms serve $L at $(date -u +%H:%M) UTC" || { echo "NOT live yet"; exit 2; }
