#!/usr/bin/env python3
"""Compare two dotsweep JSON files: per headline, the widths whose lines changed, split into the widths where the old
dot sat alone (expected to change) and any other width (must not change). usage: dotcmp.py old.json new.json"""
import json, sys

old, new = (json.load(open(p)) for p in sys.argv[1:3])


def expand(pats):
    out = {}
    for t in pats:
        for w in range(t["a"], t["z"] + 1, 2):
            out[w] = t["k"]
    return out


bad = 0
for key in new:
    if key not in old:
        print("%-12s not in old" % key)
        continue
    o, n = expand(old[key]["pats"]), expand(new[key]["pats"])
    alone_old = set(old[key]["alone"])
    changed = [w for w in n if w in o and o[w] != n[w]]
    other = [w for w in changed if w not in alone_old]
    fixed = [w for w in changed if w in alone_old]
    # where the old dot was alone, the new lines should be the old lines with the lone dot moved up to the line before it,
    # or the last letter moved down with it
    print("%-12s alone before %3d, now %3d | changed widths %3d (at old lone-dot widths %3d, elsewhere %d) | overflow %d past %d | word split %d -> %d"
          % (key, len(alone_old), len(new[key]["alone"]), len(changed), len(fixed), len(other), len(new[key]["over"]), len(new[key]["past"]),
             len(old[key]["split"]), len(new[key]["split"])))
    for w in other[:6]:
        print("     %d: %s\n          -> %s" % (w, o[w], n[w]))
    for w in fixed[:2]:
        print("     e.g. %d: %s\n          -> %s" % (w, o[w], n[w]))
    if other or new[key]["alone"] or new[key]["over"] or new[key]["past"]:
        bad += 1
print("headlines with a problem: %d of %d" % (bad, len(new)))
