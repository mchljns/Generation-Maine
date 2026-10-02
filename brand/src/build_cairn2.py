"""The cairn without the emoji read. What makes the poop emoji: a brown mound, smoothly tapering, no gaps, rounded.
So: gaps between courses, straight edges, an uneven silhouette, a line drawing, Sky stones, or a structure (the Bates cairn).

  python3 brand/src/build_cairn2.py   # writes brand/identity/marks-bark-sky/cairn/fixes.html and fixes.png
"""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_cairn import BK, SK, PA, CL, tile, img

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")


def poly(pts, fill="none", stroke=None, sw=0):
    d = "M" + " L".join("%s %s" % p for p in pts) + " Z"
    if stroke:
        return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (d, fill, stroke, sw)
    return '<path d="%s" fill="%s"/>' % (d, fill)


# the stones, drawn with air between them and straight broken edges. Base wide and flat, middle offset left, a small top stone offset right.
GAP_STONES = [
    [(40, 206), (46, 176), (118, 170), (196, 176), (200, 206)],            # base slab
    [(62, 164), (70, 134), (132, 128), (160, 138), (156, 164)],            # middle, sits left
    [(112, 122), (120, 96), (150, 90), (166, 104), (162, 122)],            # top, sits right, small
]
SLAB_STONES = [
    [(36, 206), (40, 184), (204, 184), (204, 206)],                        # a long flat slab
    [(56, 176), (60, 150), (170, 148), (176, 176)],
    [(80, 140), (86, 118), (144, 116), (148, 140)],
    [(100, 108), (104, 92), (134, 92), (136, 108)],
]
BATES = [
    [(52, 206), (56, 160), (92, 160), (96, 206)], [(144, 206), (148, 160), (184, 160), (188, 206)],
    [(44, 150), (46, 132), (194, 132), (196, 150)],
    [(98, 124), (110, 90), (146, 96), (138, 124)],
]


def solid(stones, cols, fill_bg):
    if isinstance(cols, str):
        cols = [cols] * len(stones)
    return "".join(poly(p, c) for p, c in zip(stones, cols))


def outline(stones, color, sw=9):
    return "".join(poly(p, "none", color, sw) for p in stones)


FIXES = [
    ("as drawn", "The granite as it was: three stones touching, a smooth taper. This is where the emoji read comes from.",
     lambda fg, bg: '<path d="M44 196 L58 160 L120 154 L186 158 L198 194 L172 202 L110 206 L62 204 Z" fill="%s"/><path d="M70 154 L80 120 L128 114 L166 122 L172 152 L138 158 L96 160 Z" fill="%s"/><path d="M88 114 L98 86 L132 78 L154 90 L158 112 L128 118 Z" fill="%s"/>' % (fg, fg, fg)),
    ("air between", "Gaps between the courses, straight broken edges, the middle stone set left and the small top stone set right. A stack, not a mound.",
     lambda fg, bg: solid(GAP_STONES, fg, bg)),
    ("the one you add, with air", "The same stack with the top stone in Sky. The color break on top kills the mound read on its own.",
     lambda fg, bg: solid(GAP_STONES, [fg, fg, SK if fg == BK else PA], bg)),
    ("slabs", "Flat slabs, long base, horizontal emphasis. Nothing about it is a swirl.",
     lambda fg, bg: solid(SLAB_STONES, fg, bg)),
    ("one line", "The stack as an outline in one weight, like the serif. A line drawing cannot be a mound. Fails at 16 px.",
     lambda fg, bg: outline(GAP_STONES, fg, 9)),
    ("bates", "Acadia's cairn: two legs, a lintel, a pointer. A structure, not a pile. Zero emoji risk, and only Maine builds them.",
     lambda fg, bg: solid(BATES, fg, bg)),
]


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:72ch;color:#5B544C;margin:0 0 28px}
    .grid{display:grid;grid-template-columns:repeat(6,1fr);gap:18px}.c{background:#fff;border-radius:14px;padding:16px}
    .c h3{font:400 18px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:12.5px;color:#5B544C;margin:0 0 10px;min-height:92px}
    .c img{display:block;border-radius:10px;max-width:100%}.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sz{display:flex;gap:12px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>cairn fixes</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>the cairn, not the emoji</h1><p class='in'>The emoji is a brown mound that tapers smoothly with no gaps and rounded edges. Every fix below removes one of those: air between the courses, straight edges, an uneven silhouette, a color break on top, a line drawing, or a structure instead of a pile. Each in Bark on Paper and Sky on Bark, and as the avatar at 40 and 16.</p><div class='grid'>")
    for name, note, fn in FIXES:
        a = tile(fn(BK, PA), PA); b = tile(fn(SK, BK), BK)
        av = tile('<g transform="translate(120 112) scale(.84) translate(-120 -120)">%s</g>' % fn(BK, SK), SK, True)
        avd = tile('<g transform="translate(120 112) scale(.84) translate(-120 -120)">%s</g>' % fn(SK, BK), BK, True)
        write(os.path.join(OUT, "fix-%s.svg" % name.replace(" ", "-").replace(",", "")), tile(fn(BK, PA), "none"))
        h.append("<div class='c'><div class='two'>%s%s</div><h3>%s</h3><p>%s</p><div class='sz'>%s%s%s%s</div></div>" % (img(a, 110), img(b, 110), name, note, img(av, 40), img(av, 16), img(avd, 40), img(avd, 16)))
    h.append("</div>")
    out = os.path.join(OUT, "fixes.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "fixes.png"), "1600", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
