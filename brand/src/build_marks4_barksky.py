"""Round four for Bark & Sky: a shape that means something. No initials, no numbers, no glyphs.
Rings (a generation is a ring; the concept is called Bark), rings rising from the ground, a cairn (the trail is marked by the
people who walked it before you), and a fieldstone wall (what earlier generations built and left).

  python3 brand/src/build_marks4_barksky.py   # writes brand/identity/marks-bark-sky/round4/*.svg, candidates.html and .png
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_marks_barksky as M

S = 240
OUT = "brand/identity/marks-bark-sky/round4"


def disc(bg):
    return '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg


def rings(fg, bg, n=5, cx=132, cy=108, w=9, gap=19, clip=None):
    """Growth rings, off centre the way real rings are: the tree grew toward the light."""
    out = []
    for i in range(n):
        r = 14 + i * gap
        # each ring is a little more eccentric than the last, drifting back toward the disc's centre as it grows
        t = i / max(1, n - 1)
        x = cx + (120 - cx) * t * 0.55
        y = cy + (120 - cy) * t * 0.55
        out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="%d"/>' % (x, y, r, fg, w))
    body = "".join(out)
    if clip:
        body = '<g clip-path="url(#%s)">%s</g>' % (clip, body)
    return body


def rings_disc(fg, bg):
    return ('<defs><clipPath id="r4d"><circle cx="120" cy="120" r="120"/></clipPath></defs>' + disc(bg) + rings(fg, bg, clip="r4d"))


def rings_square(fg, bg):
    return rings(fg, bg, n=5, cx=120, cy=120, w=10, gap=22)


def rings_rising(fg, bg):
    """Ground and sky: the rings rise out of the ground line like a sun. A generation coming up."""
    hy = 150
    return ('<defs><clipPath id="r4s"><rect x="0" y="0" width="240" height="%d"/></clipPath><clipPath id="r4d2"><circle cx="120" cy="120" r="120"/></clipPath></defs>' % hy
            + disc(bg)
            + '<g clip-path="url(#r4d2)"><rect x="0" y="%d" width="240" height="%d" fill="%s"/>%s</g>' % (hy, 240 - hy, fg, rings(fg, bg, n=5, cx=120, cy=hy, w=9, gap=20, clip="r4s")))


def cairn(fg, bg, scale=1.0, ox=0, oy=0):
    """Three stones, the way a trail is marked above the treeline. The people before you left the way."""
    stones = [(120, 178, 66, 22), (120, 136, 50, 19), (120, 100, 34, 16)]
    out = []
    for i, (cx, cy, rx, ry) in enumerate(stones):
        dx = (-6, 5, -2)[i]
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%d" ry="%d" fill="%s"/>' % (ox + 120 + (cx - 120 + dx) * scale, oy + 120 + (cy - 120) * scale, rx * scale, ry * scale, fg))
    return "".join(out)


def cairn_square(fg, bg):
    return cairn(fg, bg, scale=1.08, oy=-14)


def cairn_disc(fg, bg):
    return disc(bg) + cairn(fg, bg, scale=0.86, oy=-8)


def wall(fg, bg):
    """A fieldstone wall: four courses of stones, no mortar, the way they run through every Maine wood. What was built and left."""
    rows = [[(14, 50), (70, 42), (118, 58), (182, 44)], [(14, 36), (56, 60), (122, 40), (168, 58)], [(14, 54), (74, 38), (118, 50), (174, 52)], [(14, 44), (64, 52), (122, 46), (174, 52)]]
    out = []
    y = 46
    h = 36
    for row in rows:
        for x, w in row:
            out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="%s"/>' % (x, y, w, h, fg))
        y += h + 8
    return "".join(out)


def wall_disc(fg, bg):
    return ('<defs><clipPath id="r4w"><circle cx="120" cy="120" r="120"/></clipPath></defs>' + disc(bg)
            + '<g clip-path="url(#r4w)" transform="translate(0 6)">%s</g>' % wall(fg, bg))


CANDS = [
    ("rings", "growth rings", "A generation is a ring. Five rings, off centre the way real rings are, because a tree grows toward the light. The concept is named for bark; this is what is under it.", rings_square),
    ("rings-disc", "growth rings, as the disc", "The same rings filling the avatar. The outer ring runs off the edge, so the tree is older than what you can see.", rings_disc, "round"),
    ("rings-rising", "rings rising", "Ground and sky, which the client liked, with the rings coming up out of the ground like a sun. A generation coming up.", rings_rising, "round"),
    ("cairn", "the cairn", "Three stones. Above the treeline on Katahdin the trail is marked by the people who walked it before you. The brand marks the way for the next ones.", cairn_square),
    ("cairn-disc", "the cairn, as the disc", "The cairn inside the disc, for the avatar.", cairn_disc, "round"),
    ("wall", "the stone wall", "A fieldstone wall, four courses, no mortar. They run through every Maine wood: what earlier generations built and left. Reads as a texture when small.", wall),
    ("wall-disc", "the stone wall, as the disc", "The wall cropped to the avatar.", wall_disc, "round"),
]

if __name__ == "__main__":
    M.build(CANDS, OUT, "Bark &amp; Sky, round four: a shape that means something",
            "The client's brief: not a number, not a glyph, a shape with meaning. Three ideas. Rings, because a generation is a ring and the concept is called Bark. A cairn, because the trail above the treeline is marked by the people who walked it first. A stone wall, because that is what the generations before built and left in every Maine wood. Each on Paper, on Bark, as the avatar at 110, 40 and 16, and beside the wordmark.")
    print("round four written")


# ---- refinement: granite, not spa stones; rings that lean harder ----
def granite(fg, bg, scale=1.0, oy=0):
    """Three split granite stones, flat tops and broken sides, the way a Katahdin cairn is actually built."""
    stones = [
        "M44 196 L58 160 L120 154 L186 158 L198 194 L172 202 L110 206 L62 204 Z",
        "M70 154 L80 120 L128 114 L166 122 L172 152 L138 158 L96 160 Z",
        "M88 114 L98 86 L132 78 L154 90 L158 112 L128 118 Z",
    ]
    g = '<g transform="translate(120 %s) scale(%s) translate(-120 -120)">' % (120 + oy, scale)
    return g + "".join('<path d="%s" fill="%s"/>' % (d, fg) for d in stones) + "</g>"


def granite_square(fg, bg):
    return granite(fg, bg, 1.06, -12)


def granite_disc(fg, bg):
    return disc(bg) + granite(fg, bg, 0.84, -10)


def rings_rising2(fg, bg):
    """Four rings, thinner, leaning right as they rise. The ground is a third of the disc."""
    hy = 156
    body = []
    for i in range(4):
        r = 18 + i * 24
        body.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="8"/>' % (120 + i * 5, hy, r, fg))
    return ('<defs><clipPath id="r4s2"><rect x="0" y="0" width="240" height="%d"/></clipPath><clipPath id="r4d3"><circle cx="120" cy="120" r="120"/></clipPath></defs>' % hy
            + disc(bg) + '<g clip-path="url(#r4d3)"><rect x="0" y="%d" width="240" height="%d" fill="%s"/><g clip-path="url(#r4s2)">%s</g></g>' % (hy, 240 - hy, fg, "".join(body)))


REFINED = [
    ("granite", "the cairn, granite", "Three split stones, flat tops, broken sides: a real Katahdin cairn, not balanced spa pebbles. Reads at 16 px. Meaning: the people before you marked the way; this brand marks it for the next.", granite_square),
    ("granite-disc", "the cairn, granite, as the disc", "The granite cairn inside the disc.", granite_disc, "round"),
    ("rings-rising-2", "rings rising, leaner", "Four rings, thinner, leaning as they come up over a ground that is a third of the disc. A generation coming up over the ground it grew in.", rings_rising2, "round"),
]

if __name__ == "__main__" and "--refined" in sys.argv:
    M.build(REFINED, OUT + "b", "Bark &amp; Sky, round four, refined", "The cairn drawn as granite, and the rising rings leaner. Each on Paper, on Bark, as the avatar at 110, 40 and 16, and beside the wordmark.")
