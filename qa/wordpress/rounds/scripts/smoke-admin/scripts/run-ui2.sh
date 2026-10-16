#!/usr/bin/env bash
# run-ui2.sh <71|65> <run>: clip picker, 10 MB warning and Remove through one session; names; Place and WordPress's Order; author kept
V=$1; R=$2; S=/tmp/claude-0/wptest/work/smoke-admin/scripts; L=/tmp/claude-0/wptest/work/smoke-admin/logs
I=sa$V; P=$( [ "$V" = 71 ] && echo 8952 || echo 8962 ); M=/tmp/claude-0/wptest/work/smoke-admin/media
cd $S; $S/snap.sh load $I base >/dev/null
for f in big-link.gif small-b.gif big-pick.gif small-a.gif big-link.mp4; do echo "$(wpt wp $I media import $M/$f --porcelain 2>/dev/null) $f"; done
U=http://127.0.0.1:$P/wp-content/uploads/2026/10
if [ "$V" = 71 ]; then
  timeout 900 node clip.mjs $P adr1-$V-$R as:admin open:26 remove link:$U/big-link.gif update reload box link:$U/small-b.gif update box shot:adr1-after-update reload box > $L/adr1-$V-$R.txt 2>&1; echo "adr1 $?"
  timeout 1200 node clip.mjs $P adr1v-$V-$R as:admin open:26 link:$U/big-link.gif update reload link: link:$U/big-link.gif pickname:big-pick remove pickname:small-a update reload remove link:$U/small-b.gif savekbd reload > $L/adr1-variants-$V-$R.txt 2>&1; echo "adr1v $?"
  timeout 1200 node clip.mjs $P x12q-$V-$R as:admin open:26 "link:$U/big-link.gif?v=2" update reload "link:$U/big-link.gif#t=1" update reload "link:$U/big-link.mp4?x=1&y=2#z" update reload "link:$U/small-b.gif?v=big-link.gif" update reload shot:x12q-final > $L/x12-query-$V-$R.txt 2>&1; echo "x12q $?"
else
  timeout 1500 node clip.mjs $P adr1-$V-$R as:admin open:26 remove link:$U/big-link.gif update reload link:$U/small-b.gif update reload "link:$U/big-link.gif?v=2" update reload pickname:big-pick update reload remove link: link:$U/big-link.gif?v=2 savekbd reload > $L/adr1-x12-$V-$R.txt 2>&1; echo "adr1-65 $?"
fi
timeout 1500 node names.mjs $P n$V$R > $L/names-n$V$R.out 2>&1; echo "names $?"
$S/snap.sh load $I base >/dev/null
timeout 1200 node handleonce.mjs $P ho$V$R "@4x4.maine|@4x4.maine" "@gen--maine|@ gen--maine" "Kai 2x4|@kai--2x4" "Lena|lena" "Rae|@" > $L/handleonce-$V-$R.txt 2>&1; echo "handleonce $?"
$S/snap.sh load $I base >/dev/null
if [ "$V" = 71 ]; then
  timeout 900 node order.mjs $P o71b-$R open:20 place:12 update actions:2 title:x update arrow:Up3 savekbd reload qe:20:7 open:20 place:1 hometown:Rumford2 update place:5 actions:9 update reload place:5 update reload > $L/order71-long-$R.txt 2>&1; echo "order-long $?"
else
  timeout 900 node order.mjs $P o65a-$R open:20 place:9 update place:5 update reload place:9 update attr:2 update place:7 attr:3 update reload qe:20:6 open:20 arrow:Down2 savekbd reload attr:5 place:5 update reload > $L/order65-$R.txt 2>&1; echo "order65 $?"
fi
timeout 900 node order.mjs $P ob$P-$R open:14 place:20 update place:3 update hometown:Machias2 savekbd place:5 savekbd place:3 savekbd reload > $L/order-back-$P-$R.txt 2>&1; echo "order-back $?"
$S/snap.sh load $I base >/dev/null
timeout 1500 node author.mjs $P sm$V$R > $L/author$V-$R.txt 2>&1; echo "author $?"
$S/snap.sh load $I base >/dev/null
echo DONE
