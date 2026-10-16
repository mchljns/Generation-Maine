#!/usr/bin/env bash
# run-settings.sh <port> <run>: Settings checks on a fresh base each, as the round 4 tester ran them
P=$1; R=$2; S=/tmp/claude-0/wptest/work/smoke-admin/scripts; L=/tmp/claude-0/wptest/work/smoke-admin/logs
I=$( [ "$P" = 8952 ] && echo sa71 || echo sa65 )
cd $S
$S/snap.sh load $I base >/dev/null; timeout 1500 node settings-matrix.mjs $P m$P > $L/settings-matrix-$P-$R.json 2>&1; echo "matrix $?"
$S/snap.sh load $I base >/dev/null; timeout 1500 node handles-all.mjs $P h$P > $L/handles-all-$P-$R.json 2>&1; echo "handles-all $?"
$S/snap.sh load $I base >/dev/null; timeout 900 node handlespace2.mjs $P > $L/handlespace-$P-$R.json 2>&1; echo "handlespace $?"
$S/snap.sh load $I base >/dev/null
timeout 900 node contact-fresh.mjs $P cf$P "javascript:alert(1)" "data:text/html,hi" "ftp://example.org/x" "mailto:not-an-address" > $L/contact-fresh-$P-$R.json 2>&1; echo "contact $?"
timeout 600 node rest-settings.mjs $P gm_contact_url "javascript:alert(1)" gm_contact_url "data:text/html,x" gm_contact_url "ftp://x.org/" gm_instagram_url "mailto:info@mainepolicy.org" gm_contact_url "http://mainepolicy.org/contact-us/" gm_contact_url "javascript:alert(2)" gm_contact_url "mailto:info@mainepolicy.org" gm_contact_url "mailto:bad" gm_subscribe_url "mailto:info@mainepolicy.org" gm_youtube_url "http://www.youtube.com/@gm" > $L/rest-settings-$P-$R.json 2>&1; echo "rest-settings $?"
$S/snap.sh load $I base >/dev/null
