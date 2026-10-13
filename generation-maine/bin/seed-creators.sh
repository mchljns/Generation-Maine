#!/usr/bin/env bash
# Seeds placeholder creators with WP-CLI. Run from the WordPress root.
#   bash wp-content/themes/generation-maine/bin/seed-creators.sh 9 https://mchljns.github.io/Generation-Maine/v2/media
#   bash wp-content/themes/generation-maine/bin/seed-creators.sh 0   # remove placeholders and the media the script imported
set -euo pipefail
COUNT="${1:-9}"
MEDIA="${2:-}"
DIR="$(cd "$(dirname "$0")" && pwd)"
wp eval-file "$DIR/seed-creators.php" "$COUNT" ${MEDIA:+"$MEDIA"}
