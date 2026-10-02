"""The cairn drawn from the references, not from memory. Real cairns are one of two things: a rough heap of many stones
(Katahdin's summit, the Scottish and Norwegian summits) or a built structure of a few big stones (Acadia's Bates cairns:
two rounded granite boulders, a flat lintel, a pointer stone). Three neat stones is the clipart version.

  python3 brand/src/build_cairn4.py   # writes brand/identity/marks-bark-sky/cairn/studied.html and studied.png
"""
import base64
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_cairn import BK, SK, PA, CL, tile, img

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")
REF = os.path.join(ROOT, "brand", "content", "photos", "cairns")


def stone(pts, fill, r=5):
    """An irregular stone: a polygon with its corners softened by a same color stroke, which is how granite reads at a distance."""
    d = "M" + " L".join("%s %s" % p for p in pts) + " Z"
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (d, fill, fill, r * 2)


# ---- the Bates cairn, from refs 19 and 20: two rounded boulders, a lintel that is a split slab, a pointer stone set toward the way ----
def bates(fg, bg, top=None, pointer_right=True):
    top = top or fg
    left = [(46, 206), (42, 182), (50, 160), (66, 150), (88, 152), (100, 168), (102, 190), (96, 206)]
    right = [(140, 206), (138, 186), (146, 164), (164, 152), (186, 154), (198, 170), (200, 192), (192, 206)]
    lintel = [(36, 146), (44, 130), (120, 124), (204, 128), (208, 144), (196, 150), (120, 148), (48, 150)]
    pointer = [(104, 118), (112, 92), (136, 84), (160, 96), (152, 118)] if pointer_right else [(90, 118), (98, 96), (122, 84), (146, 92), (138, 118)]
    return stone(left, fg, 6) + stone(right, fg, 6) + stone(lintel, fg, 4) + stone(pointer, top, 4)


def bates_simple(fg, bg, top=None):
    """The same structure with fewer vertices, for small sizes."""
    top = top or fg
    return (stone([(46, 206), (46, 166), (70, 152), (98, 166), (98, 206)], fg, 7) + stone([(142, 206), (142, 168), (170, 152), (196, 168), (196, 206)], fg, 7)
            + stone([(38, 144), (44, 128), (204, 128), (206, 144)], fg, 4) + stone([(106, 118), (116, 92), (148, 86), (156, 118)], top, 4))


# ---- the heap, from ref 01 and 03: a rough cone of many stones, slightly asymmetric, a flat-ish top with a pointer ----
def heap(fg, bg, n_rows=6, top=None, seed=7):
    rnd = random.Random(seed)
    top = top or fg
    out = []
    base_y = 206
    row_h = 23
    for r in range(n_rows):
        y1 = base_y - r * row_h
        y0 = y1 - row_h + 4
        half = 84 - r * 12 + rnd.randint(-4, 4)
        cx = 120 + (r * 3)  # the heap leans a little to the right as it rises
        x = cx - half
        while x < cx + half - 6:
            w = rnd.randint(16, 34)
            w = min(w, cx + half - x)
            if w < 10:
                break
            pts = [(x + rnd.randint(0, 4), y1), (x, y0 + rnd.randint(0, 5)), (x + w * 0.5, y0 - rnd.randint(0, 4)), (x + w, y0 + rnd.randint(0, 5)), (x + w - rnd.randint(0, 4), y1)]
            out.append(stone(pts, fg, 2))
            x += w + 4
    # the pointer on top
    ty = base_y - n_rows * row_h + 2
    out.append(stone([(118, ty), (124, ty - 26), (142, ty - 32), (154, ty - 18), (150, ty)], top, 3))
    return "".join(out)


# ---- the flat stack, from ref 12 and 22: seven flat stones of seven sizes, the way they balance ----
def flat_stack(fg, bg, top=None, seed=3):
    rnd = random.Random(seed)
    top = top or fg
    out = []
    y = 206
    widths = [150, 128, 104, 118, 88, 70, 48]
    for i, w in enumerate(widths):
        h = rnd.randint(13, 20)
        cx = 120 + rnd.randint(-10, 10)
        tilt = rnd.randint(-3, 3)
        pts = [(cx - w / 2, y), (cx - w / 2 + rnd.randint(2, 8), y - h + tilt), (cx + w / 2 - rnd.randint(2, 8), y - h - tilt), (cx + w / 2, y)]
        out.append(stone(pts, top if i == len(widths) - 1 else fg, 3))
        y -= h + 3
    return "".join(out)


FORMS = [
    ("the Bates cairn", "ref-20.jpg", "Acadia's own design, drawn from the Gorham Mountain photographs: two rounded granite boulders, a split slab across them, a pointer stone set toward the way. A structure, not a pile. Only Maine builds these, and the park maintains them.", bates),
    ("the Bates cairn, simplified", "ref-19.jpg", "The same structure with fewer corners, for the avatar and favicon.", bates_simple),
    ("the heap", "ref-01.jpg", "Katahdin's summit cairn: a rough cone of many stones, leaning a little, a pointer on top. The texture is the drawing. Reads as a mountain at 16 px.", heap),
    ("the flat stack", "ref-12.jpg", "Seven flat stones of seven sizes balanced the way they are in the Zion and Texter Mountain photographs. Honest, and still a stack.", flat_stack),
]


def refimg(name, w=150, h=112):
    p = os.path.join(REF, name)
    return '<img src="file://%s" style="width:%dpx;height:%dpx;object-fit:cover;border-radius:10px">' % (p, w, h)


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:76ch;color:#5B544C;margin:0 0 28px}
    .row{display:grid;grid-template-columns:150px 1fr;gap:22px;align-items:start;margin-bottom:26px;background:#fff;border-radius:14px;padding:18px}
    .row h3{font:400 22px 'Hedvig Letters Serif';margin:0 0 4px}.row p{font-size:13.5px;color:#5B544C;margin:0 0 14px;max-width:70ch}
    .tiles{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap}.tiles img{display:block;border-radius:10px}.tiles .av img{border-radius:50%}
    .lab{font:11px 'IBM Plex Mono',monospace;color:#5B544C;text-align:center;margin-top:4px}.cred{font-size:11px;color:#5B544C;margin-top:6px}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>studied</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>the cairn, drawn from the photographs</h1><p class='in'>What the references say: a real cairn is either a rough heap of many stones, or a built structure of a few big ones. Each form below is drawn from a named photograph, shown in Bark on Paper, with the top stone in Sky on Bark, and as the avatar at 110, 40 and 16 px. Reference photographs are study material only and are credited in REFERENCES.md.</p>")
    for name, ref, note, fn in FORMS:
        a = tile(fn(BK, PA), PA)
        b = tile(fn(SK, BK, top=PA), BK)
        av = lambda fg, bg, top: tile('<g transform="translate(120 116) scale(.84) translate(-120 -120)">%s</g>' % fn(fg, bg, top=top), bg, True)
        write(os.path.join(OUT, "studied-%s.svg" % name.replace(" ", "-").replace(",", "")), tile(fn(BK, PA), "none"))
        h.append("<div class='row'><div>%s<div class='cred'>%s</div></div><div><h3>%s</h3><p>%s</p><div class='tiles'>%s%s<div class='av'>%s<div class='lab'>110</div></div><div class='av'>%s<div class='lab'>40</div></div><div class='av'>%s<div class='lab'>16</div></div><div class='av'>%s<div class='lab'>40</div></div><div class='av'>%s<div class='lab'>16</div></div></div></div></div>" % (
            refimg(ref), ref, name, note, img(a, 200), img(b, 200), img(av(BK, SK, BK), 110), img(av(BK, SK, BK), 40), img(av(BK, SK, BK), 16), img(av(SK, BK, PA), 40), img(av(SK, BK, PA), 16)))
    out = os.path.join(OUT, "studied.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "studied.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
