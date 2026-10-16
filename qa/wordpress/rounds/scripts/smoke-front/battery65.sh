#!/bin/bash
# smoke-front: front checks against smf65 (8951, WP 6.5.13, theme from dist zip bd9243a) and the repo v2 page (8961). One browser at a time.
cd /tmp/claude-0/wptest/work/smoke-front/s
export WPURL=http://127.0.0.1:8951/ V2URL=http://127.0.0.1:8961/
export PLAYWRIGHT_DIR=/home/user/Generation-Maine/node_modules/playwright PW_CHROMIUM=/opt/pw-browsers/chromium
S=/home/user/Generation-Maine/.claude/skills/website-build/scripts
L=/tmp/claude-0/wptest/work/smoke-front/logs
R=${R:-r1}
SZ=320x568,390x844,430x932,768x1024,844x390
VP4=320x568,390x844,768x1024,1440x900
K25=shipped,url,urlnobr,urlhttps,urllong,quoted,quotedcurly,quotedsingle,guillemet,onebigword,long1,long2,long3,long4,long5,long6,long7,long8,hyphen,twowords,emdashless,apos,paren,period,nbspent
run() { local name=$1; shift; echo "=== $name $(date -u +%T) load $(cut -d' ' -f1 /proc/loadavg)"; timeout ${T:-2400} "$@" > $L/$name.log 2>&1; echo "exit $?"; }
for step in ${STEPS:-dot gest gestx rot r3 audit roster}; do
case $step in
dot)
  TARGET=wp KEYS=$K25 T=3500 run dotsweep-65-$R node dotsweep.mjs 65-$R
  ;;
gest)
  SIZES=$SZ TARGETS=wp T=3500 run gest-65-$R node gest.mjs 65-$R ;;
gestx)
  SIZES=$SZ TARGETS=wp T=4000 run gestx-65-$R node gestx.mjs 65-$R ;;
rot)
  TARGETS=wp run focusjump-65-$R node focusjump.mjs
  run menuscroll3-65-$R node menuscroll3.mjs
  TARGETS=wp T=3000 run rot4-65-$R node rot4.mjs 65-$R ;;
r3)
  for x in pause pausestill pause-ax viewer viewer-trap viewer-sizes keyboard reduced nojs2 menu menukbd menu-open-tab carousel carousel-end2 swipe flingback glide rotate2; do run $x-65-$R node $x.mjs 65-$R; done ;;
audit)
  run measure-65-$R node $S/measure.mjs $WPURL --out /tmp/claude-0/wptest/work/smoke-front/measure/65-$R --viewports $VP4
  run contrast-65-$R node $S/contrast.mjs $WPURL --viewports $VP4
  SIZES=$VP4 TARGETS=wp run axe8-65-$R node axe8.mjs 65-$R ;;
roster)
  URL=${WPURL}roster/ TAG=roster65 run roster4-roster65-$R node roster4.mjs $R
  URL=${WPURL}stepper/ run stepperpage-stepper65-$R node stepperpage.mjs stepper65-$R ;;
esac
done
echo BATTERY65 DONE $(date -u +%T)
