#!/usr/bin/env bash
# cren03.sh <instance>: the round 2 CRE-N03 people-made creators next to a 3.0.0 seed: a hand-made Maya marked Placeholder,
# a Devin copy with the person's own avatar, and a Priya copy not marked Placeholder. All three must stay.
I=$1
J=/home/user/Generation-Maine/generation-maine/bin/creators-placeholder.json
q() { wpt wp "$I" "$@" 2>/dev/null; }
bio() { python3 -c "import json,sys;print(json.load(open('$J'))['creators'][int(sys.argv[1])]['bio'])" "$1"; }
M=$(q post create --post_type=gm_creator --post_status=publish --post_title='Maya' --post_content="$(bio 0)" --menu_order=0 --porcelain)
q post meta update "$M" gm_handle '@maya.skow' >/dev/null; q post meta update "$M" gm_hometown 'Skowhegan' >/dev/null; q post meta update "$M" gm_clip_len "$(python3 -c "import json;print(json.load(open('$J'))['creators'][0].get('len',''))")" >/dev/null; q post meta update "$M" gm_placeholder 1 >/dev/null
D=$(q post create --post_type=gm_creator --post_status=publish --post_title='Devin' --post_content="$(bio 1)" --menu_order=1 --porcelain)
q post meta update "$D" gm_handle '@devinpourscoffee' >/dev/null; q post meta update "$D" gm_hometown 'Presque Isle' >/dev/null; q post meta update "$D" gm_placeholder 1 >/dev/null
A=$(q media import /tmp/claude-0/wptest/media/sample-portrait.jpg --post_id="$D" --featured_image --porcelain)
P=$(q post create --post_type=gm_creator --post_status=publish --post_title='Priya' --post_content="$(bio 2)" --menu_order=2 --porcelain)
q post meta update "$P" gm_handle '@priya.biddo' >/dev/null; q post meta update "$P" gm_hometown 'Biddeford' >/dev/null
echo "made: maya=$M devin=$D (own avatar $A) priya=$P"
