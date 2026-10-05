"""Color rules for the slanted state lockup. Marigold fails on light fields as text (1.7:1), so: on Paper and white the second
word is blue and marigold lives only in the mark's stripe; on navy and blue the second word is marigold. A mark stripe is a
graphic beside navy stripes, so it reads on any field.

  python3 brand/src/build_slant_color.py
"""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import maine2
from build_slant16 import slant16
from build_family_marks import word, svg

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family")
NAVY, BLUE, MG, PAPER, WHITE = "#0F2E4D", "#0556A5", "#EFB443", "#F4F3EE", "#FFFFFF"
KW = dict(angle=62, fill=0.62, accent_at=10)


def lockup(fg, second, accent, idn, upper=False):
    mk, mw, _ = slant16(100, fg, accent, idn=idn, **KW)
    size = 64 if upper else 70
    t1, w1 = word("GENERATION " if upper else "Generation ", size, fg, mw + 26, 80)
    t2, w2 = word("MAINE" if upper else "Maine", size, second, mw + 26 + w1, 80)
    return svg(mw + 26 + w1 + w2 + 4, 100, mk + t1 + t2)


def img(s, h):
    return '<img src="data:image/svg+xml;base64,%s" style="height:%dpx;display:block">' % (base64.b64encode(s.encode()).decode(), h)


ROWS = [
    ("On Paper", PAPER, NAVY, BLUE, MG, "Navy name, Maine in blue (6.6:1), marigold only in the stripe."),
    ("On white", WHITE, NAVY, BLUE, MG, "Same rule."),
    ("On navy", NAVY, WHITE, MG, MG, "White name, Maine in marigold (7.4:1)."),
    ("On blue", BLUE, WHITE, MG, MG, "White name, Maine in marigold (3.9:1, passes for large type; the lockup is always large)."),
    ("On Paper, one color", PAPER, NAVY, NAVY, NAVY, "No accent at all. Print, embroidery, anywhere one color is all there is."),
    ("On Paper, marigold text (rejected)", PAPER, NAVY, MG, MG, "What was on the last sheet: 1.7:1. Shown for comparison only."),
]


def build():
    files = {}
    css = """body{margin:0;background:#E9E5DA;color:#0F2E4D;font:15px/1.5 'DM Sans',system-ui;padding:48px 56px}
    h1{font:800 34px/1.05 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 8px}p.in{max-width:80ch;color:#4B5A68;margin:0 0 22px}
    .row{display:grid;grid-template-columns:300px 1fr 1fr;gap:18px;align-items:center;margin-bottom:14px}.lab b{display:block;font-weight:700;margin-bottom:3px}.lab p{margin:0;font-size:12.5px;color:#4B5A68}
    .t{border-radius:12px;padding:26px 30px;display:flex;align-items:center;justify-content:center;min-height:120px}
    """
    fonts = "@font-face{font-family:'Bricolage Grotesque';font-weight:800;src:url(file://%s)}@font-face{font-family:'DM Sans';font-weight:100 900;src:url(file://%s)}" % (
        os.path.join(ROOT, "brand", "fonts", "BricolageGrotesque-ExtraBold.ttf"), os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"))
    h = ['<!doctype html><meta charset="utf-8"><title>color rules</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>Where the marigold goes</h1><p class='in'>Marigold on a light field is 1.7:1 as text, and no yellow reaches 4.5:1 on Paper. So the rule: on light fields the second word is blue and marigold appears only as the mark's stripe; on navy and blue the second word is marigold. Title case left, uppercase right.</p>")
    for i, (name, bg, fg, second, accent, note) in enumerate(ROWS):
        a = lockup(fg, second, accent, "t%d" % i); b = lockup(fg, second, accent, "u%d" % i, upper=True)
        key = name.lower().replace(" ", "-").replace(",", "").replace("(", "").replace(")", "")
        if "rejected" not in name:
            files["lockup-%s" % key] = a; files["lockup-%s-upper" % key] = b
        h.append("<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='t' style='background:%s'>%s</div><div class='t' style='background:%s'>%s</div></div>" % (name, note, bg, img(a, 56), bg, img(b, 52)))
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)
    out = os.path.join(OUT, "color-rules.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "color-rules.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
