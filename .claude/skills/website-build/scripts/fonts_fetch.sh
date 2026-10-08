#!/usr/bin/env bash
# Fetch one or more Open Font License families from the google/fonts repository into fonts/<family>/
# with the OFL.txt beside each, using a sparse, blobless clone so only those folders download.
#
#   fonts_fetch.sh <family-dir> [family-dir ...] [--dest fonts] [--clone /tmp/google-fonts]
#
# <family-dir> is the folder name under ofl/ in google/fonts: lowercase, no spaces (michroma, jura,
# bricolagegrotesque, dmsans). Check https://github.com/google/fonts/tree/main/ofl for the name.
# Variable fonts have [wght] in the filename; the script copies them as they are.
set -eu
DEST=fonts; CLONE=/tmp/google-fonts; FAMS=()
while [ $# -gt 0 ]; do case "$1" in --dest) DEST="$2"; shift;; --clone) CLONE="$2"; shift;; *) FAMS+=("$1");; esac; shift; done
[ ${#FAMS[@]} -gt 0 ] || { echo "usage: fonts_fetch.sh <family-dir> ... [--dest fonts]"; exit 2; }
if [ ! -d "$CLONE/.git" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git "$CLONE"
fi
paths=(); for f in "${FAMS[@]}"; do paths+=("ofl/$f"); done
git -C "$CLONE" sparse-checkout set "${paths[@]}"
for f in "${FAMS[@]}"; do
  src="$CLONE/ofl/$f"
  [ -d "$src" ] || { echo "not found: ofl/$f (check the folder name in google/fonts)"; exit 1; }
  mkdir -p "$DEST/$f"
  cp "$src"/*.ttf "$DEST/$f/" 2>/dev/null || true
  cp "$src"/OFL.txt "$DEST/$f/" 2>/dev/null || cp "$src"/LICENSE* "$DEST/$f/" 2>/dev/null || true
  echo "== $f"; ls -la "$DEST/$f"
  [ -f "$DEST/$f/OFL.txt" ] || echo "  WARNING: no OFL.txt copied; check the license before use"
  grep -m1 -E '^(name|license|category)' "$src/METADATA.pb" 2>/dev/null || true
done
