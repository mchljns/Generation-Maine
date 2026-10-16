#!/bin/bash
# smoke-front: front checks against smf71 (8951, WP 7.1.3, theme from dist zip bd9243a) and the repo v2 page (8961). One browser at a time.
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
  TARGET=wp KEYS=$K25 T=3500 run dotsweep-71-$R node dotsweep.mjs 71-$R
  TARGET=v2 KEYS=$K25 T=3500 run dotsweep-v2-$R node dotsweep.mjs v2-$R ;;
gest)
  SIZES=$SZ TARGETS=wp,v2 T=3500 run gest-71v2-$R node gest.mjs 71v2-$R ;;
gestx)
  SIZES=$SZ TARGETS=wp,v2 T=4000 run gestx-71v2-$R node gestx.mjs 71v2-$R ;;
rot)
  run focusjump-71v2-$R node focusjump.mjs
  run menuscroll3-71v2-$R node menuscroll3.mjs
  T=3000 run rot4-71v2-$R node rot4.mjs 71v2-$R ;;
r3)
  for x in pause pausestill pause-ax viewer viewer-trap viewer-sizes keyboard reduced nojs2 menu menukbd menu-open-tab carousel carousel-end2 swipe flingback glide rotate2; do run $x-71v2-$R node $x.mjs 71v2-$R; done ;;
audit)
  run measure-71-$R node $S/measure.mjs $WPURL --out /tmp/claude-0/wptest/work/smoke-front/measure/71-$R --viewports $VP4
  run measure-v2-$R node $S/measure.mjs $V2URL --out /tmp/claude-0/wptest/work/smoke-front/measure/v2-$R --viewports $VP4
  run contrast-71-$R node $S/contrast.mjs $WPURL --viewports $VP4
  run contrast-v2-$R node $S/contrast.mjs $V2URL --viewports $VP4
  SIZES=$VP4 TARGETS=wp,v2 run axe8-71v2-$R node axe8.mjs 71v2-$R ;;
roster)
  URL=${WPURL}roster/ TAG=roster71 run roster4-roster71-$R node roster4.mjs $R
  URL=${WPURL}stepper/ run stepperpage-stepper71-$R node stepperpage.mjs stepper71-$R ;;
esac
done
echo BATTERY71 DONE $(date -u +%T)
