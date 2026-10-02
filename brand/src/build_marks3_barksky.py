"""Bark & Sky, mark round three. The horizon disc did not land. Six more, each still one color and quiet, drawn for a Gen Z
audience in Maine: patch, sticker, grid, heavy outline, the split silhouette, and the name alone as the mark.

  python3 brand/src/build_marks3_barksky.py   # writes brand/identity/marks-bark-sky/round3/
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_v4 import f, rect
import maine2
from build_logo_maine import maine_lines, simplified
import build_marks_barksky as M

S, BK, SK, PA = M.S, "#26201C", "#B9C9D3", "#F4F3EE"
_N = [0]


def uid(p):
    _N[0] += 1
    return "%s%d" % (p, _N[0])


def state_path(x, y, h, tol=0.012):
    ring = simplified(maine2.fit(x, y, h * maine2.ASPECT, h), h * tol)
    return maine2.path(ring), ring


def patch(fg, bg):
    """A sew-on patch: a rounded square with a single-weight border, the solid state inside."""
    d, _ = state_path((S - 150 * maine2.ASPECT) / 2, 45, 150)
    return ('<rect x="14" y="14" width="%s" height="%s" rx="34" fill="none" stroke="%s" stroke-width="9"/><path d="%s" fill="%s"/>'
            % (f(S - 28), f(S - 28), fg, d, fg))


def sticker(fg, bg):
    """A die-cut sticker: the solid state with a thick offset edge in the field's color, then the state again."""
    d, _ = state_path((S - 170 * maine2.ASPECT) / 2, 35, 170)
    edge = PA if fg == BK else BK
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="34" stroke-linejoin="round"/><path d="%s" fill="none" stroke="%s" stroke-width="16" stroke-linejoin="round"/><path d="%s" fill="%s"/>'
            % (d, fg, d, edge, d, fg))


def grid(fg, bg, cols=4, rows=5):
    """Maine as a grid of rounded squares: a cell is filled where the state covers most of it. The social grid, the app icon, the
    sixteen counties, all in one gesture."""
    h = S - 40
    _, ring = state_path((S - h * maine2.ASPECT) / 2, 20, h, tol=0.004)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    cw, ch = (maxx - minx) / cols, (maxy - miny) / rows
    cell = min(cw, ch)
    ox = (S - cols * cell) / 2
    oy = (S - rows * cell) / 2
    out = ""
    for r in range(rows):
        for c in range(cols):
            # sample a 6 by 6 lattice inside the cell, in the state's own box
            hits = 0
            for i in range(6):
                for j in range(6):
                    px = minx + (c + (i + 0.5) / 6) * cw
                    py = miny + (r + (j + 0.5) / 6) * ch
                    xs = maine2.crossings(ring, py)
                    inside = any(a <= px <= b for a, b in zip(xs[0::2], xs[1::2]))
                    hits += inside
            if hits >= 14:
                out += rect(ox + c * cell + cell * 0.08, oy + r * cell + cell * 0.08, cell * 0.84, cell * 0.84, fg, cell * 0.22)
    return out


def outline(fg, bg):
    """The state as one heavy stroke with rounded joins, like a routed sign."""
    d, _ = state_path((S - 160 * maine2.ASPECT) / 2, 40, 160, tol=0.02)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="18" stroke-linejoin="round"/>' % (d, fg)


def split(fg, bg):
    """The solid state cut once by a horizontal gap, two thirds down. The horizon kept as a memory, no disc."""
    d, _ = state_path((S - 180 * maine2.ASPECT) / 2, 30, 180)
    y = 30 + 180 * 0.64
    a, b = uid("a"), uid("b")
    return ('<defs><clipPath id="%s"><rect x="0" y="0" width="%s" height="%s"/></clipPath><clipPath id="%s"><rect x="0" y="%s" width="%s" height="%s"/></clipPath></defs>'
            '<path d="%s" fill="%s" clip-path="url(#%s)"/><path d="%s" fill="%s" clip-path="url(#%s)"/>') % (
        a, f(S), f(y - 5), b, f(y + 5), f(S), f(S), d, fg, a, d, fg, b)


def name_mark(fg, bg):
    """No symbol. The name stacked in the serif, maine set large: the wordmark is the mark."""
    d1, w1 = M.SERIF.path("generation", 38, 0, 0, -6)
    d2, w2 = M.SERIF.path("maine", 84, 0, 0, -10)
    return ('<path fill="%s" d="%s"/><path fill="%s" d="%s"/>'
            % (fg, M.SERIF.path("generation", 38, (S - w1) / 2, 100, -6)[0], fg, M.SERIF.path("maine", 84, (S - w2) / 2, 172, -10)[0]))


def lined(fg, bg):
    body, w = maine_lines(0, 0, S - 24, fg, fg, "full", gold=False)
    return '<g transform="translate(%s 12)">%s</g>' % (f((S - w) / 2), body)


CANDS = [
    ("lined", "The lined state (shared)", "Reference.", lined),
    ("patch", "Patch", "A sew-on patch: a rounded square with one border weight, the solid state inside. Workwear and gear, which is where the audience lives.", patch),
    ("sticker", "Sticker", "The solid state cut like a die-cut sticker, with the thick edge a laptop lid gives it. Loud for this concept, and the most Gen Z thing on the sheet.", sticker),
    ("grid", "Grid, 4 by 5", "Maine as a grid of rounded squares, a cell filled where the state covers it. It is a feed, an app icon and the state at once, and it is abstract enough to pass the on-the-nose test.", grid),
    ("grid6", "Grid, 5 by 6", "The same rule one step finer. More Maine, still blocks.", lambda fg, bg: grid(fg, bg, cols=5, rows=6)),
    ("grid8", "Grid, 6 by 8", "Finer again. The silhouette is clear and the blocks start to read as pixels.", lambda fg, bg: grid(fg, bg, cols=6, rows=8)),
    ("outline", "Heavy outline", "One thick stroke with rounded joins, like a routed trail sign. Honest and plain. Dies at 16 px.", outline),
    ("split", "Split", "The solid state cut once by a horizontal gap two thirds down. The horizon kept as a memory with no disc around it. Quiet, and the gap reads as the line between the Maine you can afford and the one you can find work in.", split),
    ("name", "The name as the mark", "No symbol. The name stacked in the serif with maine set large. Many of the brands this audience trusts have no symbol at all.", name_mark),
]

if __name__ == "__main__":
    # the field palette for this round
    M.BK, M.SK, M.PA = BK, SK, PA
    M.build(CANDS, "brand/identity/marks-bark-sky/round3", "Bark &amp; Sky, mark round three",
            "The horizon disc did not land. Six more, each one color and quiet, drawn for a Gen Z audience in Maine. Each row: on Paper, on Bark, the avatar at 110, 40 and 16 px, and the horizontal lockup.")
    print("round three written")
