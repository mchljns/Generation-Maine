#!/usr/bin/env bash
# run-seedui.sh <71|65> <run>: the seed checks that go through the editor (N3 edited sample, seedrec4 on current and on 3.0.0 seeds)
V=$1; R=$2; S=/tmp/claude-0/wptest/work/smoke-admin/scripts; L=/tmp/claude-0/wptest/work/smoke-admin/logs
I=sa$V; P=$( [ "$V" = 71 ] && echo 8952 || echo 8962 ); export GMB=http://127.0.0.1:$P GMI=$I GMW=$L
T=/tmp/claude-0/wptest/inst/$I/core/wp-content/themes/generation-maine/bin/seed-creators.php; D=$S/dump.sh
s() { wpt wp $I eval-file "$@" 2>&1 | grep -v Deprecated; }
mkdir -p $L/shots; cd $S
# N3: a sample given its own clip and links, Placeholder left ticked
$S/snap.sh load $I base >/dev/null; wpt wp $I media import /tmp/claude-0/wptest/media/sample-clip.gif --title=small-a --porcelain 2>/dev/null
timeout 300 node editsample.mjs 17 2>&1 | tail -1 > $L/editsample-$V-$R.txt
(echo "## seed 0"; s $T 0; $D $I; echo "## re-seed 9 (no media)"; s $T 9; $D $I; wpt wp $I post meta list 17 --format=csv 2>/dev/null | grep gm_) > $L/seed$V-T1-sample-edited-$R.txt 2>&1; echo "T1 done"
# current seeds changed through the editor
$S/snap.sh load $I base >/dev/null
timeout 900 node seedrec4.mjs cur$V$R 4 26 8 20 5 23 29 2>&1 | tail -1 > $L/seedrec-cur$V-$R.out
(echo "## before"; $D $I; echo "## seed 0"; s $T 0; $D $I) > $L/seedrec-cur$V-$R-seed0.txt 2>&1; echo "cur done"
# PL-R1: a real 3.0.0 seed of 12 with media, changed through the editor
$S/snap.sh load $I base >/dev/null
(echo "## theme seed 0"; s $T 0; echo "## real 3.0.0 seed 12 with media"; s $S/../seed300/seed-creators.php 12 /home/user/Generation-Maine/brand/identity/splash-lean-a/media; $D $I) > $L/seedrec-$V-$R-setup.txt 2>&1
id() { grep "|$1|publish|" $L/seedrec-$V-$R-setup.txt | head -1 | cut -d'|' -f1; }
ARGS="$(id Noah) $(id Devin) $(id Tyler) $(id Maya) $(id Amara) $(id Sam)"; echo "seedrec4 ids: $ARGS"
timeout 1500 node seedrec4.mjs $V-$R 2 $ARGS 2>&1 | tail -1 > $L/seedrec-$V-$R.out
[ "$V" = 65 ] && $S/cren03.sh $I
(echo "## README removal: seed 0"; s $T 0; $D $I; echo "## seed 0 again"; s $T 0) > $L/seedrec-$V-$R-seed0.txt 2>&1; echo "plr1 done"
(echo "## empty the Trash"; TR=$(wpt wp $I post list --post_type=gm_creator --post_status=trash --format=ids 2>/dev/null); [ -n "$TR" ] && wpt wp $I post delete $TR --force 2>&1 | grep -v Deprecated; echo "## seed 0"; s $T 0; $D $I; echo "attachments: $(wpt wp $I post list --post_type=attachment --format=count 2>/dev/null)") > $L/seedrec-$V-$R-empty.txt 2>&1; echo "empty done"
$S/snap.sh load $I base >/dev/null
echo DONE
