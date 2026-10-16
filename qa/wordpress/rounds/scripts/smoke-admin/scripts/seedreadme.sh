#!/usr/bin/env bash
# seedreadme.sh <instance>: the README seed rules on an untouched seeded site (round 2 I04 case), then re-seed with media
I=$1
P=/tmp/claude-0/wptest/inst/$I/core/wp-content/themes/generation-maine/bin/seed-creators.php
D=/tmp/claude-0/wptest/work/smoke-admin/scripts/dump.sh
M=/home/user/Generation-Maine/brand/identity/splash-lean-a/media
s() { wpt wp "$I" eval-file "$P" "$@" 2>&1 | grep -v Deprecated; }
echo '## re-seed 9 with media on the untouched seeded site'; s 9 "$M"; "$D" "$I"
echo '## own placeholder creator, and Maya made real by unticking Placeholder'
OWN=$(wpt wp "$I" post create --post_type=gm_creator --post_status=publish --post_title='Pending recruit (mine)' --post_content='Coming soon.' --porcelain 2>/dev/null)
wpt wp "$I" post meta update "$OWN" gm_placeholder 1 2>&1 | grep -v Deprecated
MAYA=$(wpt wp "$I" post list --post_type=gm_creator --title=Maya --field=ID 2>/dev/null | head -1)
wpt wp "$I" post meta update "$MAYA" gm_placeholder '' 2>&1 | grep -v Deprecated
echo '## seed 0'; s 0; "$D" "$I"
echo '## seed 0 again'; s 0
