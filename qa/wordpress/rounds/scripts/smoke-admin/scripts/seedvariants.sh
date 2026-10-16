#!/usr/bin/env bash
# seedvariants.sh <instance> <ownClipId>: change current (gm_seeded) samples in different ways through WP-CLI, then run seed 0
I=$1; OWN=$2
w() { wpt wp "$I" "$@" 2>&1 | grep -v '^Success\|Deprecated' ; }
# Jess: a real person's handle, their own clip from the Media Library, Instagram and TikTok; Placeholder left ticked
w post meta update 17 gm_handle '@real.person'
w post meta update 17 gm_clip_id "$OWN"
w post meta update 17 gm_instagram 'https://www.instagram.com/real.person/'
w post meta update 17 gm_tiktok 'https://www.tiktok.com/@real.person'
# Devin: only the place changed
w post update 8 --menu_order=12
# Priya: unpublished, nothing else changed
w post update 11 --post_status=draft
# Cole: in the Trash, nothing else changed
w eval "wp_trash_post( 14 );"
# Tyler: avatar removed, nothing else changed
w post meta delete 20 _thumbnail_id
# Amara: given Maya's sample clip
w post meta update 23 gm_clip_id 7
# Noah: story edited
w post update 26 --post_content='I am finishing a nursing license. This is my own story now.'
# Sam: Placeholder unticked (a real creator now)
w post meta update 29 gm_placeholder ''
echo '## before'; /tmp/claude-0/wptest/work/smoke-admin/scripts/dump.sh "$I"
echo '## seed 0'; wpt wp "$I" eval-file /tmp/claude-0/wptest/inst/$I/core/wp-content/themes/generation-maine/bin/seed-creators.php 0 2>&1 | grep -v Deprecated
echo '## after'; /tmp/claude-0/wptest/work/smoke-admin/scripts/dump.sh "$I"
echo '## all seeded media ids'; wpt wp "$I" post list --post_type=attachment --meta_key=gm_seeded --field=ID --format=ids 2>/dev/null; echo
echo '## own media'; wpt wp "$I" post list --post_type=attachment --post__in="$OWN" --fields=ID,post_title 2>/dev/null
