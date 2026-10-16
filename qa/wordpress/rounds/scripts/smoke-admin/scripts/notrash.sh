#!/usr/bin/env bash
# notrash.sh <instance>: on a site with the Trash off, 3.0.0 seeds are left in place; current seeds follow the untouched rule
I=$1
P=/tmp/claude-0/wptest/inst/$I/core/wp-content/themes/generation-maine/bin/seed-creators.php
D=/tmp/claude-0/wptest/work/smoke-admin/scripts/dump.sh
s() { wpt wp "$I" eval-file "$@" 2>&1 | grep -v Deprecated; }
C=/tmp/claude-0/wptest/inst/$I/core/wp-config.php
python3 -c "import sys;p=sys.argv[1];s=open(p).read();open(p,'w').write(s.replace(\"if ( ! defined( 'ABSPATH' ) )\",\"define( 'EMPTY_TRASH_DAYS', 0 );\\nif ( ! defined( 'ABSPATH' ) )\",1))" "$C"
echo "EMPTY_TRASH_DAYS=$(wpt wp "$I" eval 'echo EMPTY_TRASH_DAYS;' 2>/dev/null)"
echo '## a current sample changed (Jess gets an Instagram link), Trash off, seed 0'
wpt wp "$I" post meta update 17 gm_instagram 'https://www.instagram.com/jess.real/' 2>&1 | grep -v Deprecated
s "$P" 0; "$D" "$I"
echo '## real 3.0.0 seed 9 no media, then seed 0 with no Trash'
s /tmp/claude-0/wptest/work/smoke-admin/seed300/seed-creators.php 9
s "$P" 0; "$D" "$I" | tail -4
echo '## seed 9 with no Trash'; s "$P" 9
python3 -c "import sys;p=sys.argv[1];s=open(p).read();open(p,'w').write(s.replace(\"define( 'EMPTY_TRASH_DAYS', 0 );\\n\",''))" "$C"
"$D" "$I" | tail -12
