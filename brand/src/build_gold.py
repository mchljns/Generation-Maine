"""Where does the yellow go? Four answers, shown on the lockup, the avatar on light, and the end card.

  A  stripe   : the widest line of the state is Marigold (current)
  B  dot      : the state is one color, Marigold is the dot on the i, as in every headline
  C  thread   : the widest line runs out of the state and reaches the name
  D  baseline : the state has no gold, and a Marigold rule under the wordmark is the line the state sits on

  python3 brand/src/build_gold.py && python3 brand/src/sheet_gold.py
"""
from gmlib import write
from build_v4 import svg, rect, f, wordmark_one_line
from build_v6 import C
from build_logo_maine import maine_lines
import maine2

OUT = "brand/identity/gold"
SP, BI, MG, MOSS = C["spruce"], C["birch"], C["marigold"], C["moss"]


def widest_y(x, y, h):
    """The y of the widest line, so other elements can meet it."""
    ring = maine2.fit(x, y, h * maine2.ASPECT, h)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    best, by = 0, 0
    for i in range(21):
        t = i / 20
        y0 = miny + (maxy - miny) * (0.035 + 0.93 * t)
        xs = maine2.crossings(ring, y0)
        L = sum(b - a for a, b in zip(xs[0::2], xs[1::2]))
        if L > best:
            best, by = L, y0
    return by, maxx


def lockup(variant, fg, mk, bg=None, W=None):
    b, w, h = wordmark_one_line(fg, mk if variant == "B" else fg, "circle", 100)
    mh, gap = 96, 26
    gold = variant in ("A", "C")
    mb, mw = maine_lines(0, 74 - mh + 6, mh, fg, mk, "full", gold=gold)
    tw = w + mw + gap
    body = (rect(-20, -30, tw + 40, h + 60, bg) if bg else "")
    body += mb + '<g transform="translate(%s 0)">%s</g>' % (f(mw + gap), b)
    if variant == "C":
        yw, east = widest_y(0, 74 - mh + 6, mh)
        lw = mh * (0.015 + (0.034 - 0.015) * ((yw - (74 - mh + 6)) / mh))
        body += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(east - lw), f(yw), f(mw + gap - 6), f(yw), mk, f(lw))
    if variant == "D":
        body += rect(0, h + 14, tw, 3, mk)
    return svg(tw, h, body, "Generation Maine")


def avatar_light(variant):
    fg, mk = SP, MG
    gold = variant in ("A", "C")
    mb, mw = maine_lines(0, 0, 164, fg, mk, "full", gold=gold)
    extra = ""
    if variant == "C":
        yw, east = widest_y(0, 0, 164)
        extra = '<path d="M%s %s L%s %s" stroke="%s" stroke-width="3.4" stroke-linecap="round" fill="none"/>' % (f(east - 3), f(yw), f(east + 34), f(yw), mk)
    if variant == "D":
        extra = rect(38, 214, 164, 4, mk)
    # B: the mark alone carries no Marigold. A floating dot beside the state read as a badge, so it is gone.
    return svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % BI + '<g transform="translate(%s 38)">%s</g>' % (f((240 - mw) / 2), mb) + extra, "Generation Maine")


def build():
    m = {}
    for v in "ABCD":
        m["lockup-" + v] = lockup(v, SP, MG)
        m["lockup-%s-reversed" % v] = lockup(v, BI, MG, bg=SP)
        m["avatar-light-" + v] = avatar_light(v)
    for k, s in m.items():
        write("%s/%s.svg" % (OUT, k), s)
    return m


if __name__ == "__main__":
    print("gold:", list(build()))
