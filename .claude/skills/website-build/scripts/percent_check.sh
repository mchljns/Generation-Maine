#!/usr/bin/env bash
# Catch the two ways %-formatted page builders break: a bare % inside the formatted template
# (crashes the build or formats the wrong thing) and a %% that leaked into the built output because
# that block was never formatted (ships "100%%" into the stylesheet and silently kills the rule).
#
#   percent_check.sh <builder.py> [built.html] [--marker 'HTML = '] [--end 'def ']
#
# A template region runs from a line matching --marker (default: a triple-quoted assignment named
# HTML, CSS or TEMPLATE) to the next line matching --end. Only blocks that actually go through
# %-formatting belong in the region; pass --marker for the builder's own names, and keep blocks that
# are concatenated after formatting (overrides, phone CSS) out of it, since there a %% is the bug.
# Exit 1 on any finding.
set -u
BUILDER="${1:?builder file}"; BUILT="${2:-}"
MARKER='^(HTML|CSS|TEMPLATE)[A-Z_]* *= *r?"""'; END='^(def |class |[A-Z_]+ *= *)'
while [ $# -gt 0 ]; do case "$1" in --marker) MARKER="$2"; shift;; --end) END="$2"; shift;; esac; shift; done
status=0
# bare % : a % not followed by ( or % , inside template regions
awk -v marker="$MARKER" -v end="$END" '
  BEGIN{inreg=0}
  { if (!inreg && $0 ~ marker) { inreg=1; start=NR; next }
    if (inreg && $0 ~ end && $0 !~ marker) { inreg=0 }
    if (inreg) { line=$0; gsub(/%\(/, "", line); gsub(/%%/, "", line); if (line ~ /%/) printf("  bare %% at %s:%d: %s\n", FILENAME, NR, substr($0,1,110)) }
  }' "$BUILDER" > /tmp/pc_bare.$$
if [ -s /tmp/pc_bare.$$ ]; then echo "FAIL bare % inside a %-formatted template region (write %% or move the block out of the formatted string):"; cat /tmp/pc_bare.$$; status=1; else echo "ok: no bare % in template regions of $BUILDER"; fi
rm -f /tmp/pc_bare.$$
if [ -n "$BUILT" ]; then
  n=$(grep -c '%%' "$BUILT" || true)
  if [ "$n" != "0" ]; then echo "FAIL $n line(s) with %% leaked into $BUILT:"; grep -n '%%' "$BUILT" | head -5 | cut -c1-140; status=1; else echo "ok: no %% in $BUILT"; fi
fi
exit $status
