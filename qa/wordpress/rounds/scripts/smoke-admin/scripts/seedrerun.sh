#!/usr/bin/env bash
# seedrerun.sh <instance>: after seedvariants.sh, run the removal again, trash a changed sample, re-seed and remove again
I=$1
P=/tmp/claude-0/wptest/inst/$I/core/wp-content/themes/generation-maine/bin/seed-creators.php
D=/tmp/claude-0/wptest/work/smoke-admin/scripts/dump.sh
s() { wpt wp "$I" eval-file "$P" "$@" 2>&1 | grep -v Deprecated; }
echo '## seed 0 again'; s 0
echo '## trash Noah (changed) then seed 0'; wpt wp "$I" eval 'wp_trash_post( 26 );' 2>&1 | grep -v Deprecated; s 0; "$D" "$I"
echo '## seed 9 no media'; s 9; "$D" "$I"
echo '## seed 0'; s 0; "$D" "$I"
