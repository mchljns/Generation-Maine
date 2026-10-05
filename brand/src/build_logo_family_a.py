"""Family A's logo set: the slanted state (62 degrees, sixteen stripes, the accent through the state's widest part) drawn as
stroked lines inside a clip of the state, so the mark can draw itself in like the lined state did, in the hero mural and the
footer. Lockups are uppercase GENERATION MAINE in Bricolage 800, the second word in the accent on dark fields and in blue on
light ones. Also writes the hero mural data for the splash template.

  python3 brand/src/build_logo_family_a.py   # writes brand/identity/logo-maine/family-a/*.svg and mural.json
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import maine2
from build_logo_maine import simplified
from build_family_marks import word

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family-a")
NAVY, BLUE, MG, WHITE, PAPER = "#0F2E4D", "#0556A5", "#EFB443", "#FFFFFF", "#F4F3EE"
ANGLE, N, FILL, ACCENT_AT = 62, 16, 0.62, 10


def segments(h, x=0, y=0, angle=ANGLE, n=N, fill=FILL, tol=0.003, speck=2.0, samples=7):
    """Sixteen stripes crossing the state, as the pieces each stripe makes with the accurate outline. A piece is found by
    sampling several lines across the stripe's width and merging the intervals where they cross the polygon; its extent along
    the stripe is the farthest crossing on any sample line, so the clip (the exact outline) cuts every piece exactly at the
    coast. Pieces are dropped only if they are specks (shorter along the stripe than `speck` stripe widths) or slivers (the
    stripe's center line never crosses them). Returns (ring, [[(x0,y0,x1,y1), ...] per stripe], stroke width, state width)."""
    ring = simplified(maine2.fit(x, y, h * maine2.ASPECT, h), h * tol)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    rot = math.radians(90 - angle)
    def to(px, py):
        return (cx + (px - cx) * math.cos(-rot) - (py - cy) * math.sin(-rot), cy + (px - cx) * math.sin(-rot) + (py - cy) * math.cos(-rot))
    def back(px, py):
        return (cx + (px - cx) * math.cos(rot) - (py - cy) * math.sin(rot), cy + (px - cx) * math.sin(rot) + (py - cy) * math.cos(rot))
    r2 = [to(*p) for p in ring]
    m = len(r2)
    def cross(xc):
        ys = []
        for k in range(m):
            (x0, y0), (x1, y1) = r2[k], r2[(k + 1) % m]
            if (x0 <= xc < x1) or (x1 <= xc < x0):
                ys.append(y0 + (xc - x0) / (x1 - x0) * (y1 - y0))
        ys.sort()
        return list(zip(ys[0::2], ys[1::2]))
    lo, hi = min(p[0] for p in r2), max(p[0] for p in r2)
    pitch = (hi - lo) / n
    sw = pitch * fill
    stripes = []
    for i in range(n):
        c = lo + (i + 0.5) * pitch
        # intervals on each sample line across the stripe, tagged with whether they come from the center line
        ivs = []
        for k in range(samples):
            xc = c - sw / 2 + sw * (k + 0.5) / samples
            for a, b in cross(xc):
                ivs.append([a, b, k == samples // 2, {k}])
        # merge overlapping intervals into pieces
        ivs.sort()
        pieces = []
        for a, b, mid, ks in ivs:
            if pieces and a <= pieces[-1][1]:
                pieces[-1][1] = max(pieces[-1][1], b); pieces[-1][2] = pieces[-1][2] or mid; pieces[-1][3] |= ks
            else:
                pieces.append([a, b, mid, set(ks)])
        segs = []
        for a, b, mid, ks in pieces:
            # drop a sliver along the coast (the center line misses it), a piece narrower than most of the stripe (fewer than
            # 70 percent of the sample lines cross it: a peninsula thinner than a stripe), or a speck shorter than `speck` widths
            if not mid or len(ks) < math.ceil(samples * 0.7) or b - a < sw * speck:
                continue
            p0, p1 = back(c, a - sw * 0.1), back(c, b + sw * 0.1)
            segs.append((round(p0[0], 2), round(p0[1], 2), round(p1[0], 2), round(p1[1], 2)))
        stripes.append(segs)
    return ring, stripes, sw, maxx - minx


def mark_body(h, fg, accent, x=0, y=0, idn="fa", draw=False):
    ring, stripes, sw, w = segments(h, x, y)
    out = ['<defs><clipPath id="%s"><path d="%s"/></clipPath></defs><g clip-path="url(#%s)">' % (idn, maine2.path(ring), idn)]
    k = 0
    for i, segs in enumerate(stripes):
        col = accent if i == ACCENT_AT else fg
        for x0, y0, x1, y1 in segs:
            extra = ' pathLength="1" style="transition-delay:%dms"' % (k * 40) if draw else ""
            out.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="%.2f" fill="none"%s/>' % (x0, y0, x1, y1, col, sw, extra))
            k += 1
    out.append("</g>")
    return "".join(out), w


def svg(w, h, body, label="Generation Maine"):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s</svg>' % (w, h, w, h, label, body)


def lockup(fg, second, accent, idn, upper=True, mh=100):
    mk, mw = mark_body(mh, fg, accent, idn=idn)
    size = mh * 0.64 if upper else mh * 0.70
    t1, w1 = word("GENERATION " if upper else "Generation ", size, fg, mw + mh * 0.26, mh * 0.80)
    t2, w2 = word("MAINE" if upper else "Maine", size, second, mw + mh * 0.26 + w1, mh * 0.80)
    return svg(round(mw + mh * 0.26 + w1 + w2 + 4, 1), mh, mk + t1 + t2)


def two_line(fg, second, accent, idn):
    mh = 160
    mk, mw = mark_body(mh, fg, accent, idn=idn)
    size = 74
    t1, w1 = word("GENERATION", size, fg, mw + 36, 72)
    t2, w2 = word("MAINE", size, second, mw + 36, 150)
    return svg(round(mw + 36 + max(w1, w2) + 4, 1), mh, mk + t1 + t2)


def build():
    os.makedirs(OUT, exist_ok=True)
    files = {}
    # marks
    for suf, fg, acc in (("", NAVY, BLUE), ("-reversed", WHITE, MG), ("-marigold", NAVY, NAVY), ("-black", "#000000", "#000000"), ("-white", WHITE, WHITE)):
        b, w = mark_body(240, fg, acc, idn="m" + (suf.strip("-") or "0"))
        files["mark" + suf] = svg(round(w, 1), 240, b)
    # lockups: on light (navy + blue), on dark (white + marigold), on marigold (navy only), one color
    for suf, fg, second, acc in (("", NAVY, BLUE, BLUE), ("-reversed", WHITE, MG, MG), ("-marigold", NAVY, NAVY, NAVY), ("-black", "#000000", "#000000", "#000000"), ("-white", WHITE, WHITE, WHITE)):
        files["lockup-compact" + suf] = lockup(fg, second, acc, "c" + (suf.strip("-") or "0"))
        files["lockup-horizontal" + suf] = lockup(fg, second, acc, "h" + (suf.strip("-") or "0"), mh=140)
        files["lockup-title" + suf] = lockup(fg, second, acc, "t" + (suf.strip("-") or "0"), upper=False)
        files["lockup-two-line" + suf] = two_line(fg, second, acc, "l" + (suf.strip("-") or "0"))
    # avatar, app icon, favicon
    def disc(fg, bg, acc, idn, rx=None):
        b, w = mark_body(156, fg, acc, x=(240 - 156 * maine2.ASPECT) / 2, y=42, idn=idn)
        shape = '<rect width="240" height="240" rx="%s" fill="%s"/>' % (rx, bg) if rx is not None else '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg
        return svg(240, 240, shape + b)
    files["avatar"] = disc(NAVY, MG, NAVY, "a1")
    files["avatar-navy"] = disc(WHITE, NAVY, MG, "a2")
    files["avatar-blue"] = disc(WHITE, BLUE, MG, "a3")
    files["app-icon"] = disc(NAVY, MG, NAVY, "a4", rx=54)
    files["favicon"] = disc(NAVY, MG, NAVY, "a5")
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)
    # the hero mural: the state at 720, centered in a 720 square, white stripes, the accent in marigold, as lines for the draw-in
    ring, stripes, sw, w = segments(720, (720 - 720 * maine2.ASPECT) / 2, 0, tol=0.0015)
    lines = []
    for i, segs in enumerate(stripes):
        for x0, y0, x1, y1 in segs:
            lines.append([x0, y0, x1, y1, round(sw, 2), MG if i == ACCENT_AT else WHITE])
    json.dump({"clip": maine2.path(ring), "lines": lines}, open(os.path.join(OUT, "mural.json"), "w"), separators=(",", ":"))
    print("wrote", len(files), "files and mural.json with", len(lines), "lines")


if __name__ == "__main__":
    build()
