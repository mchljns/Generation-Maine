#!/bin/bash
# smoke-front editor checks on an instance: posts/pages layout (r4-editor mkpage2 + laymeasure, btnui, layoutui), Site Editor
# (dotprobe, dupparts2/3, styles-survey, fontshidden). usage: ed71.sh <port> <tag> <v65 0|1>
cd /tmp/claude-0/wptest/work/smoke-front/ed/scripts
B=http://127.0.0.1:$1; TAG=$2; V65=$3; R=${R:-r1}
L=/tmp/claude-0/wptest/work/smoke-front/ed/logs
run() { local name=$1; shift; echo "=== $name $(date -u +%T) load $(cut -d' ' -f1 /proc/loadavg)"; timeout ${T:-1500} "$@" > $L/$name.log 2>&1; echo "exit $?"; }
for step in ${STEPS:-lay ui se}; do
case $step in
lay)
  run $TAG-mkpage-page node mkpage2.mjs $B $TAG-layp page "Layout page" /tmp/claude-0/wptest/work/smoke-front/ed/markup/${MARKUP:-layout-71.html}
  run $TAG-mkpage-post node mkpage2.mjs $B $TAG-lay post "Layout post" /tmp/claude-0/wptest/work/smoke-front/ed/markup/${MARKUP:-layout-71.html}
  PID=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-layp-mkpage2.json'))['info']['id'])")
  PURL=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-layp-mkpage2.json'))['info']['link'])")
  QID=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-lay-mkpage2.json'))['info']['id'])")
  QURL=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-lay-mkpage2.json'))['info']['link'])")
  echo "page $PID $PURL post $QID $QURL"
  run $TAG-laymeasure-page-$R node laymeasure.mjs $B $PURL $PID $TAG-page-$R
  run $TAG-laymeasure-post-$R node laymeasure.mjs $B $QURL $QID $TAG-post-$R ;;
ui)
  PID=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-layp-mkpage2.json'))['info']['id'])")
  PURL=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/wptest/work/smoke-front/ed/data/$TAG-layp-mkpage2.json'))['info']['link'])")
  run $TAG-btnui50-$R node btnui.mjs $B $TAG-50-$R 50
  run $TAG-btnui25-$R node btnui.mjs $B $TAG-25-$R 25
  run $TAG-layoutui-$R node layoutui.mjs $B $PID $PURL $TAG-$R ;;
se)
  run $TAG-dotprobe-$R node dotprobe.mjs $B $TAG-$R $V65
  run $TAG-dupparts2-$R node dupparts2.mjs $B $TAG-$R $V65
  run $TAG-dupparts3-$R node dupparts3.mjs $B $TAG-$R $V65
  run $TAG-styles-survey-$R node styles-survey.mjs $B $TAG-$R $V65
  [ "$V65" = 0 ] && run $TAG-fontshidden-$R node fontshidden.mjs $B $TAG-$R ;;
esac
done
echo ED DONE $(date -u +%T)
