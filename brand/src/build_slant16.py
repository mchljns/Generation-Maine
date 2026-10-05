"""The slanted state with sixteen stripes, one per county, like the horizontal lined state. Variants by angle and weight,
at 240, 110, 40 and 16, and in the title case lockup.

  python3 brand/src/build_slant16.py   # writes brand/identity/logo-maine/family/slant16*.svg, slant16.html and slant16.png
"""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import maine2
from build_logo_maine import simplified
from build_family_marks import word, svg, NAVY, MG, PAPER, BLUE

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family")


def slant16(h, fg, accent, x=0, y=0, angle=62, fill=0.6, accent_at=8, idn="s16", n=16):
    """Sixteen stripes that all cross the state. The state's extent is measured along the stripe normal, in the rotated frame,
    and the sixteen pitches are fitted to exactly that extent, so none is clipped away. Returns (body, width, visible count)."""
    import math
    ring = simplified(maine2.fit(x, y, h * maine2.ASPECT, h), h * 0.01)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    w = maxx - minx
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    rot = 90 - angle  # the bars are drawn vertical, then rotated by this
    r = math.radians(-rot)
    # the ring in the bars' frame
    px = [cx + (X - cx) * math.cos(r) - (Y - cy) * math.sin(r) for X, Y in ring]
    py = [cy + (X - cx) * math.sin(r) + (Y - cy) * math.cos(r) for X, Y in ring]
    lo, hi = min(px), max(px)
    pitch = (hi - lo) / n
    sw = pitch * fill
    L = h * 2.4
    stripes = ""
    # a stripe is visible if the ring crosses its band; check with the polygon edges in the rotated frame
    def crosses(a, b):
        for i in range(len(px)):
            x0, x1 = px[i], px[(i + 1) % len(px)]
            if max(x0, x1) >= a and min(x0, x1) <= b:
                return True
        return False
    visible = 0
    for i in range(n):
        c = lo + (i + 0.5) * pitch
        col = accent if i == accent_at else fg
        if crosses(c - sw / 2, c + sw / 2):
            visible += 1
        stripes += '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (c - sw / 2, cy - L / 2, sw, L, col)
    body = ('<defs><clipPath id="%s"><path d="%s"/></clipPath></defs><g clip-path="url(#%s)"><g transform="rotate(%s %s %s)">%s</g></g>'
            % (idn, maine2.path(ring), idn, rot, cx, cy, stripes))
    return body, w, visible


def disc(body, bg):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240"><circle cx="120" cy="120" r="120" fill="%s"/>%s</svg>' % (bg, body)


def img(s, px=None, h=None):
    st = ("width:%dpx;" % px if px else "") + ("height:%dpx;" % h if h else "")
    return '<img src="data:image/svg+xml;base64,%s" style="%sdisplay:block">' % (base64.b64encode(s.encode()).decode(), st)


VARIANTS = [
    ("62°, even", "Maine Policy's angle. Stripe and gap equal.", dict(angle=62, fill=0.5)),
    ("62°, heavier", "The same angle, stripes at 62 percent of the pitch. Holds the silhouette better when small.", dict(angle=62, fill=0.62)),
    ("55°", "A little more upright, so the stripes read as the state's own lines rather than the parent's exact mark.", dict(angle=55, fill=0.58)),
    ("45°", "A plain diagonal. Furthest from the parent, closest to a hatch.", dict(angle=45, fill=0.58)),
    ("62°, accent low", "The marigold stripe set one further down, through the widest part of the state.", dict(angle=62, fill=0.6, accent_at=10)),
    ("62°, no accent", "One color, for the favicon and anywhere one color is all there is.", dict(angle=62, fill=0.6, accent_at=-1)),
]


def build():
    css = """body{margin:0;background:#E9E5DA;color:#0F2E4D;font:15px/1.5 'DM Sans',system-ui;padding:48px 56px}
    h1{font:800 34px/1.05 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 8px}p.in{max-width:80ch;color:#4B5A68;margin:0 0 22px}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.c{background:#fff;border-radius:12px;padding:18px}.c h3{margin:10px 0 2px;font-weight:700;font-size:16px}.c p{margin:0 0 10px;font-size:12.5px;color:#4B5A68;min-height:40px}
    .two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.two div{border-radius:10px;display:flex;align-items:center;justify-content:center;padding:18px}.pa{background:#F4F3EE}.nv{background:#0F2E4D}
    .sz{display:flex;gap:14px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}.lk{margin-top:14px;background:#F4F3EE;border-radius:10px;padding:14px;display:flex;justify-content:center}
    """
    fonts = "@font-face{font-family:'Bricolage Grotesque';font-weight:800;src:url(file://%s)}@font-face{font-family:'DM Sans';font-weight:100 900;src:url(file://%s)}" % (
        os.path.join(ROOT, "brand", "fonts", "BricolageGrotesque-ExtraBold.ttf"), os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"))
    h = ['<!doctype html><meta charset="utf-8"><title>sixteen stripes</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>The slanted state, sixteen stripes</h1><p class='in'>One stripe per county, like the horizontal lined state. Six cuts, each on Paper and on navy, as the avatar at 110, 40 and 16, and in the title case lockup.</p><div class='grid'>")
    for i, (name, note, kw) in enumerate(VARIANTS):
        body, w, vis = slant16(240, NAVY, MG, idn="v%d" % i, **kw)
        body_r, _, _ = slant16(240, PAPER, MG, idn="r%d" % i, **kw)
        print(name, "visible stripes:", vis)
        write(os.path.join(OUT, "slant16-%d.svg" % (i + 1)), svg(w, 240, body))
        write(os.path.join(OUT, "slant16-%d-reversed.svg" % (i + 1)), svg(w, 240, body_r))
        av = lambda fg, bg, j: disc(slant16(156, fg, MG, x=(240 - 156 * maine2.ASPECT) / 2, y=42, idn="a%d%s" % (i, j), **kw)[0], bg)
        mk, mw, _ = slant16(100, NAVY, MG, idn="l%d" % i, **kw)
        t1, w1 = word("Generation ", 70, NAVY, mw + 26, 80)
        t2, w2 = word("Maine", 70, MG, mw + 26 + w1, 80)
        lk = svg(mw + 26 + w1 + w2 + 4, 100, mk + t1 + t2)
        h.append("<div class='c'><div class='two'><div class='pa'>%s</div><div class='nv'>%s</div></div><h3>%s</h3><p>%s</p><div class='sz'>%s%s%s%s%s%s</div><div class='lk'>%s</div></div>" % (
            img(svg(w, 240, body), None, 170), img(svg(w, 240, body_r), None, 170), name, note,
            img(av(NAVY, "#FFFFFF", "a"), 110), img(av(NAVY, "#FFFFFF", "b"), 40), img(av(NAVY, "#FFFFFF", "c"), 16), img(av(PAPER, NAVY, "d"), 110), img(av(PAPER, NAVY, "e"), 40), img(av(PAPER, NAVY, "f"), 16), img(lk, None, 52)))
    h.append("</div>")
    out = os.path.join(OUT, "slant16.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "slant16.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
