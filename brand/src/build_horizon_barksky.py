"""Ground and sky, with Maine in it. The client liked the split disc and asked whether the state can be worked in.
Six ways, each keeping the horizon: Sky above, ground below, a thin line of light between.

  python3 brand/src/build_horizon_barksky.py   # writes brand/identity/marks-bark-sky/horizon/
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_v4 import f, rect
import maine2
from build_logo_maine import maine_lines, simplified
import build_marks_barksky as M

S, BK, SK, PA = M.S, M.BK, M.SK, M.PA
_N = [0]


def uid(p):
    _N[0] += 1
    return "%s%d" % (p, _N[0])


def ground_of(fg):
    return BK if fg == BK else PA


def state(x, y, h, tol=0.012):
    w_box = h * maine2.ASPECT
    ring = simplified(maine2.fit(x, y, w_box, h), h * tol)
    return maine2.path(ring), w_box


def disc(fg, inner, y=S * 0.6):
    """The disc: Sky above the horizon, ground below, the light line, then whatever sits inside."""
    cid = uid("d")
    line = PA if fg == BK else BK
    return ('<defs><clipPath id="%s"><circle cx="%s" cy="%s" r="%s"/></clipPath></defs><g clip-path="url(#%s)">%s%s%s'
            '<rect x="0" y="%s" width="%s" height="3" fill="%s"/></g>') % (
        cid, f(S / 2), f(S / 2), f(S / 2), cid, rect(0, 0, S, y, SK), rect(0, y, S, S - y, ground_of(fg)), inner, f(y - 1.5), f(S), line)


def counterchange(fg, bg):
    """The state centred on the horizon, Bark where it crosses the sky, Sky where it crosses the ground."""
    y = S * 0.6
    h = 150
    d, w = state((S - h * maine2.ASPECT) / 2, S / 2 - h / 2 + 6, h)
    a, b = uid("a"), uid("b")
    inner = ('<defs><clipPath id="%s"><rect x="0" y="0" width="%s" height="%s"/></clipPath><clipPath id="%s"><rect x="0" y="%s" width="%s" height="%s"/></clipPath></defs>'
             '<path d="%s" fill="%s" clip-path="url(#%s)"/><path d="%s" fill="%s" clip-path="url(#%s)"/>') % (
        a, f(S), f(y), b, f(y), f(S), f(S), d, ground_of(fg), a, d, SK, b)
    return disc(fg, inner)


def rising(fg, bg):
    """The state stands on the ground and rises into the sky, like a landform. Its base is lost in the ground."""
    y = S * 0.6
    h = 170
    d, w = state((S - h * maine2.ASPECT) / 2, y - h * 0.72, h)
    return disc(fg, '<path d="%s" fill="%s"/>' % (d, ground_of(fg)))


def standing(fg, bg):
    """A small state on the horizon, the one place on the line."""
    y = S * 0.6
    h = 64
    d, w = state((S - h * maine2.ASPECT) / 2, y - h + 2, h, tol=0.02)
    return disc(fg, '<path d="%s" fill="%s"/>' % (d, ground_of(fg)))


def knockout(fg, bg):
    """The state cut out of the ground, so the sky shows through it below the horizon."""
    y = S * 0.6
    h = 120
    d, w = state((S - h * maine2.ASPECT) / 2, y - h * 0.3, h)
    cid = uid("k")
    inner = ('<defs><clipPath id="%s"><rect x="0" y="%s" width="%s" height="%s"/></clipPath></defs><path d="%s" fill="%s" clip-path="url(#%s)"/>') % (
        cid, f(y), f(S), f(S), d, SK, cid)
    return disc(fg, inner)


def shaped(fg, bg):
    """No disc: the state itself holds the sky and the ground. Maine, with a horizon through it."""
    h = S - 20
    d, w = state((S - h * maine2.ASPECT) / 2, 10, h)
    y = S * 0.6
    cid = uid("s")
    line = PA if fg == BK else BK
    return ('<defs><clipPath id="%s"><path d="%s"/></clipPath></defs><g clip-path="url(#%s)">%s%s<rect x="0" y="%s" width="%s" height="3" fill="%s"/></g>') % (
        cid, d, cid, rect(0, 0, S, y, SK), rect(0, y, S, S - y, ground_of(fg)), f(y - 1.5), f(S), line)


def lined_horizon(fg, bg):
    """The shared lined state inside the disc, counterchanged: Bark lines on the sky, Sky lines on the ground."""
    y = S * 0.6
    h = 160
    body, w = maine_lines((S - h * maine2.ASPECT) / 2, S / 2 - h / 2 + 6, h, "X", "X", "full", gold=False)
    a, b = uid("la"), uid("lb")
    inner = ('<defs><clipPath id="%s"><rect x="0" y="0" width="%s" height="%s"/></clipPath><clipPath id="%s"><rect x="0" y="%s" width="%s" height="%s"/></clipPath></defs>'
             '<g clip-path="url(#%s)">%s</g><g clip-path="url(#%s)">%s</g>') % (
        a, f(S), f(y), b, f(y), f(S), f(S), a, body.replace('"X"', '"%s"' % ground_of(fg)), b, body.replace('"X"', '"%s"' % SK))
    return disc(fg, inner)


CANDS = [
    ("horizon", "Ground and sky, as drawn", "The disc split at the horizon, the thin line of light between. The reference.", lambda fg, bg: M.horizon(fg, bg, PA if fg == BK else BK), "round"),
    ("counterchange", "Counterchange", "The state centred on the horizon, dark where it crosses the sky, light where it crosses the ground. An old heraldic move: one shape, two fields.", counterchange, "round"),
    ("rising", "Rising from the ground", "The state stands on the horizon and rises into the sky, its base lost in the ground. It reads as a landform first and a map second.", rising, "round"),
    ("standing", "A place on the line", "A small state on the horizon, the one thing on it. The place you are from, seen from a distance.", standing, "round"),
    ("knockout", "Cut from the ground", "The state cut out of the ground so the sky shows through. The quietest of the set.", knockout, "round"),
    ("shaped", "Maine holds the horizon", "No disc. The state itself is the field, sky above and ground below, the line of light through it.", shaped),
    ("lined", "The lined state on the horizon", "The shared sixteen lines inside the disc, counterchanged. The system mark and the horizon in one.", lined_horizon, "round"),
]

if __name__ == "__main__":
    M.build(CANDS, "brand/identity/marks-bark-sky/horizon", "Ground and sky, with Maine in it",
            "The split disc the client liked, with the state worked in six ways. Every version keeps the horizon: Sky above, ground below, a thin line of light between. Each row: on Paper, on Bark, the avatar at 110, 40 and 16 px, and the horizontal lockup.")
    print("horizon candidates written")
