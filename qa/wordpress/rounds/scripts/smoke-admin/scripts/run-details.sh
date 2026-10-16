#!/usr/bin/env bash
# run-details.sh <71|65> <run>: Creator details checks (fixer's and tester's scripts) on a fresh base
V=$1; R=$2; S=/tmp/claude-0/wptest/work/smoke-admin/scripts; L=/tmp/claude-0/wptest/work/smoke-admin/logs
I=sa$V; P=$( [ "$V" = 71 ] && echo 8952 || echo 8962 ); export GMB=http://127.0.0.1:$P GMI=$I GMW=$L
cd $S; $S/snap.sh load $I base >/dev/null
timeout 2400 node dirty4.mjs $R$V 17 > $L/dirty4-$R$V.out 2>&1; echo "dirty4 $?"
timeout 300 node ctrlz.mjs 17 2>&1 | tail -8 > $L/ctrlz-$R$V.txt; echo "ctrlz $?"
timeout 300 node undoshot2.mjs 17 $R$V 2>&1 | tail -2 > $L/undoshot-$R$V.txt; echo "undoshot2 $?"
timeout 400 node undomix.mjs 17 2>&1 | tail -16 > $L/undomix-$R$V.txt; echo "undomix $?"
$S/snap.sh load $I base >/dev/null
timeout 900 node dirty.mjs d$R$V 20 > $L/dirty-d$R$V.out 2>&1; echo "dirty $?"
wpt wp $I post delete 25 --force 2>&1 | tail -1
timeout 600 node goneclip.mjs g$R$V 23 > $L/goneclip-g$R$V.out 2>&1; echo "goneclip $?"
timeout 600 node contribctrls.mjs c$R$V > $L/contribctrls-c$R$V.out 2>&1; echo "contribctrls $?"
$S/snap.sh load $I base >/dev/null
echo DONE
