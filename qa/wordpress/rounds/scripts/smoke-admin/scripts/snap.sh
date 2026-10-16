#!/usr/bin/env bash
# snap.sh save|load <instance> [label]: keep or bring back the instance's database, uploads and wp-config.php
set -e
I=/tmp/claude-0/wptest/inst/$2/core
S=/tmp/claude-0/wptest/work/smoke-admin/snap-$2-${3:-base}
wpt stop "$2" >/dev/null
if [ "$1" = save ]; then
  rm -rf "$S"; mkdir -p "$S"; cp -a "$I/wp-content/database" "$I/wp-content/uploads" "$I/wp-config.php" "$S/"
else
  rm -rf "$I/wp-content/database" "$I/wp-content/uploads"; cp -a "$S/database" "$S/uploads" "$I/wp-content/"; cp -a "$S/wp-config.php" "$I/"
fi
wpt start "$2"
