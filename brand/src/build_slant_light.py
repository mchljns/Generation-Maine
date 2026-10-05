"""The mark on light fields: the marigold stripe is hard to read against Paper gaps. Three options at 240, 110, 56 and 40:
marigold stripe (as it was), blue stripe, no accent.
  python3 brand/src/build_slant_light.py
"""
import base64, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_slant16 import slant16
from build_family_marks import word, svg

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family")
NAVY, BLUE, MG, PAPER = "#0F2E4D", "#0556A5", "#EFB443", "#F4F3EE"
KW = dict(angle=62, fill=0.62, accent_at=10)

def mark(acc, idn, h=240):
    body, w, _ = slant16(h, NAVY, acc, idn=idn, **KW) if acc else slant16(h, NAVY, NAVY, idn=idn, **dict(KW, accent_at=-1))
    return svg(w, h, body)

def lockup(acc, idn):
    mk, mw, _ = slant16(100, NAVY, acc or NAVY, idn=idn, **(KW if acc else dict(KW, accent_at=-1)))
    t1, w1 = word("Generation ", 70, NAVY, mw + 26, 80); t2, w2 = word("Maine", 70, BLUE, mw + 26 + w1, 80)
    return svg(mw + 26 + w1 + w2 + 4, 100, mk + t1 + t2)

def img(s, h): return '<img src="data:image/svg+xml;base64,%s" style="height:%dpx;display:block">' % (base64.b64encode(s.encode()).decode(), h)

OPTS = [("Marigold stripe", MG, "As it was. Beside Paper gaps the marigold stripe reads as a gap at lockup size."),
        ("Blue stripe", BLUE, "The accent stripe in the same blue as the second word. 6.6:1 against Paper, so it stays a stripe at any size, and the lockup becomes two colors, navy and blue, like the parent's two-color names."),
        ("No accent", None, "One color. The quietest, and nothing to lose at small sizes.")]

def build():
    css = """body{margin:0;background:#E9E5DA;color:#0F2E4D;font:15px/1.5 'DM Sans',system-ui;padding:48px 56px}
    h1{font:800 34px/1.05 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 8px}p.in{max-width:80ch;color:#4B5A68;margin:0 0 22px}
    .row{display:grid;grid-template-columns:260px 1fr;gap:18px;align-items:center;margin-bottom:14px}.lab b{display:block;font-weight:700;margin-bottom:3px}.lab p{margin:0;font-size:12.5px;color:#4B5A68}
    .t{border-radius:12px;padding:26px 30px;display:flex;align-items:center;gap:40px;background:#F4F3EE;min-height:150px}.t .sz{display:flex;gap:22px;align-items:flex-end}
    """
    fonts = "@font-face{font-family:'Bricolage Grotesque';font-weight:800;src:url(file://%s)}@font-face{font-family:'DM Sans';font-weight:100 900;src:url(file://%s)}" % (
        os.path.join(ROOT, "brand", "fonts", "BricolageGrotesque-ExtraBold.ttf"), os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"))
    h = ['<!doctype html><meta charset="utf-8"><title>mark on light</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>The mark on light fields</h1><p class='in'>Three ways to handle the accent stripe on Paper and white. Each at 240, 110, 56 and 40, then in the lockup with Maine in blue.</p>")
    for i, (name, acc, note) in enumerate(OPTS):
        m = mark(acc, "m%d" % i)
        h.append("<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='t'><div class='sz'>%s%s%s%s</div>%s</div></div>" % (name, note, img(m, 240), img(m, 110), img(m, 56), img(m, 40), img(lockup(acc, "l%d" % i), 56)))
        if acc == BLUE:
            write(os.path.join(OUT, "mark-light-blue-stripe.svg"), m); write(os.path.join(OUT, "lockup-on-paper-blue-stripe.svg"), lockup(acc, "x"))
    out = os.path.join(OUT, "mark-light.html"); write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "mark-light.png"), "1500", "1.4"], check=True)

if __name__ == "__main__":
    build()
