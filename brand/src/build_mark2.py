"""Improving the brandmark. The room becomes the shape the system already uses: a headline block,
low left. Lines that would cross it stop at it, the nearest lines bow and turn gold.

  python3 brand/src/build_mark2.py     # writes brand/identity/mark2/<key>/*.svg
"""
from gmlib import write
from build_v4 import svg, rect
from build_v6 import C
from build_push import field
from build_abstract import mark_gold_flat

OUT = "brand/identity/mark2"
SP, BI, MG = C["spruce"], C["birch"], C["marigold"]


def room(x, y, s, fg, mark, small=False, open_left=True, n=None, ry=(0.50, 0.80), rx=(0.12, 0.60), clear_k=0.075, wt=(0.012, 0.046), mode="gap", gold="below", rr=0, pad_k=0.06):
    n = n or (6 if small else 13)
    w_lo, w_hi = (s * 0.03, s * 0.075) if small else (s * wt[0], s * wt[1])
    x0 = x - s if open_left else x + s * rx[0]
    ob = [("rect", x0, y + s * ry[0], x + s * rx[1], y + s * ry[1], gold, s * rr)]
    return field(x, y, s, s, n, ob, s * (clear_k * (1.35 if small else 1)), fg, mark, w_lo, w_hi, steps=160, pad=s * pad_k, mode=mode)


def room_circle_two(x, y, s, fg, mark, small=False):
    """The circle room kept, but only the two lines that hug it turn gold."""
    n = 6 if small else 13
    w_lo, w_hi = (s * 0.03, s * 0.075) if small else (s * 0.012, s * 0.046)
    cx, cy = x + s * 0.32, y + s * 0.68
    r = s * (0.13 if small else 0.11)
    ob = [("circle", cx, cy, r, True)]
    return field(x, y, s, s, n, ob, s * 0.05, fg, mark, w_lo, w_hi, steps=160, pad=s * 0.06, mode="gap")


def half_room(x, y, s, fg, mark, small=False, where="left", mode="wrap", n=None, gold=True, wide=False, r_k=0.2, wt=(0.012, 0.046)):
    """A round room that opens to an edge. where = left (the margin) or corner (low left)."""
    n = n or (6 if small else 13)
    w_lo, w_hi = (s * 0.03, s * 0.075) if small else (s * wt[0], s * wt[1])
    pad = s * 0.06
    W = s * 1.4 if wide else s
    r = s * (r_k * 1.25 if small else r_k)
    if where == "left":
        cx, cy = x + pad, y + s * 0.6
    else:
        cx, cy = x + pad, y + s - pad
    ob = [("circle", cx, cy, r, gold)]
    return field(x, y, W, s, n, ob, s * (0.06 if small else 0.045), fg, mark, w_lo, w_hi, steps=180, pad=pad, mode=mode)


CANDIDATES = [
    ("margin-wrap", "Room at the margin, lines wrap, gold where they bend", lambda *a, **k: half_room(*a, **k, where="left")),
    ("margin-gap", "Room at the margin, lines stop, gold on the hugging lines", lambda *a, **k: half_room(*a, **k, where="left", mode="gap")),
    ("corner-wrap", "Room at the corner, lines wrap", lambda *a, **k: half_room(*a, **k, where="corner", r_k=0.3)),
    ("corner-gap", "Room at the corner, lines stop", lambda *a, **k: half_room(*a, **k, where="corner", mode="gap", r_k=0.3)),
    ("margin-wrap-9", "Room at the margin, nine heavier lines", lambda *a, **k: half_room(*a, **k, where="left", n=(6 if k.get("small") else 9), wt=(0.016, 0.06), r_k=0.22)),
    ("control", "Control: the circle room", lambda *a, **k: mark_gold_flat(*a, **k)),
]


def build():
    out = {}
    for key, name, fn in CANDIDATES:
        m = {}
        m["mark"] = svg(240, 240, fn(0, 0, 240, SP, MG), "Generation Maine")
        m["mark-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + fn(0, 0, 240, BI, MG), "Generation Maine")
        m["mark-mono"] = svg(240, 240, fn(0, 0, 240, SP, SP), "Generation Maine")
        m["mark-small"] = svg(240, 240, fn(0, 0, 240, SP, MG, small=True), "Generation Maine")
        m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + fn(44, 44, 152, BI, MG, small=True), "Generation Maine")
        for k, v in m.items():
            write("%s/%s/%s.svg" % (OUT, key, k), v)
        out[key] = (name, m)
    return out


if __name__ == "__main__":
    print("mark2:", list(build()))
