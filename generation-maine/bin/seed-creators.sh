#!/usr/bin/env bash
# Seeds placeholder creators with WP-CLI. Run from the WordPress root.
#   bash wp-content/themes/generation-maine/bin/seed-creators.sh 12
#   bash wp-content/themes/generation-maine/bin/seed-creators.sh 0   # remove placeholders
set -euo pipefail
COUNT="${1:-12}"
DIR="$(cd "$(dirname "$0")" && pwd)"
wp eval-file "$DIR/seed-creators.php" "$COUNT"
