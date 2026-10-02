"""The client's pick: a flat stack with a round rock on top, the flat stones varied in size and shape, air between them.
Six builds. Shown in Bark on Paper, with the round stone in Sky on Bark, and as the avatar at 110, 40 and 16.

  python3 brand/src/build_cairn5.py   # writes brand/identity/marks-bark-sky/cairn/flat-round.html and .png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_cairn import BK, SK, PA, CL, tile, img
from build_cairn4 import stone

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")


def round_stone(cx, cy, rx, ry, fill, tilt=0):
    """A rounded stone that is not a perfect ellipse: an egg, a little flatter on the bottom where it sits."""
    return ('<g transform="rotate(%s %s %s)"><path d="M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z" fill="%s"/></g>'
            % (tilt, cx, cy, cx - rx, cy + ry * 0.35, cx - rx * 1.05, cy - ry * 0.9, cx + rx * 0.2, cy - ry * 1.08, cx + rx, cy - ry * 0.1,
               cx + rx * 1.02, cy + ry * 0.7, cx + rx * 0.3, cy + ry * 1.0, cx - rx, cy + ry * 0.35, fill))


# each build: list of flat stones as polygons (base first), then the round stone (cx, cy, rx, ry, tilt)
BUILDS = {
    "five and a round": (
        [[(40, 206), (44, 190), (196, 186), (202, 206)],
         [(62, 180), (66, 160), (166, 158), (170, 180)],
         [(52, 150), (58, 140), (182, 136), (184, 150)],
         [(80, 128), (86, 108), (150, 106), (156, 128)],
         [(72, 98), (78, 88), (160, 86), (162, 98)]],
        (118, 62, 30, 24, -8)),
    "wedges": (
        [[(36, 206), (40, 186), (200, 192), (204, 206)],
         [(58, 178), (62, 152), (174, 160), (176, 178)],
         [(48, 144), (56, 132), (168, 126), (170, 144)],
         [(84, 118), (90, 96), (150, 102), (152, 118)]],
        (122, 68, 34, 26, 6)),
    "thick and thin": (
        [[(44, 206), (48, 174), (192, 172), (196, 206)],
         [(60, 164), (62, 156), (178, 154), (180, 164)],
         [(74, 146), (80, 118), (156, 116), (160, 146)],
         [(66, 108), (70, 100), (166, 98), (168, 108)]],
        (120, 72, 30, 25, -4)),
    "leaning left": (
        [[(50, 206), (54, 188), (200, 184), (204, 206)],
         [(44, 176), (50, 158), (180, 154), (182, 176)],
         [(38, 146), (46, 128), (154, 124), (158, 146)],
         [(48, 116), (54, 102), (134, 100), (136, 116)]],
        (90, 76, 28, 22, -10)),
    "big slab base": (
        [[(28, 206), (34, 176), (206, 172), (212, 206)],
         [(70, 164), (76, 148), (158, 146), (162, 164)],
         [(62, 138), (68, 128), (176, 124), (178, 138)],
         [(96, 116), (100, 102), (142, 100), (146, 116)]],
        (120, 76, 24, 20, 4)),
    "seven thin": (
        [[(42, 206), (46, 194), (198, 192), (200, 206)],
         [(60, 186), (64, 174), (176, 172), (180, 186)],
         [(50, 166), (56, 154), (186, 150), (188, 166)],
         [(76, 146), (80, 134), (160, 132), (164, 146)],
         [(68, 126), (74, 114), (150, 112), (154, 126)],
         [(90, 106), (94, 96), (140, 94), (144, 106)],
         [(82, 88), (86, 80), (156, 78), (158, 88)]],
        (120, 56, 24, 20, -6)),
}
NOTES = {
    "five and a round": "Five flat stones, no two alike, alternating wide and narrow. The round stone sits a little left.",
    "wedges": "The flats are wedges, thicker at one end, as split stone is. The round stone leans the other way.",
    "thick and thin": "Two thick slabs with two thin ones between. The rhythm reads at small size.",
    "leaning left": "The stack steps left as it rises and the round stone sits near the edge. The most handmade.",
    "big slab base": "One heavy base slab, three smaller flats, a small round stone. The most stable silhouette.",
    "seven thin": "Seven thin flats, the way slate stacks. A texture at 16 px, a stripe pattern at 40.",
}


def draw(key, fg, bg, top=None):
    flats, (cx, cy, rx, ry, tilt) = BUILDS[key]
    return "".join(stone(p, fg, 3) for p in flats) + round_stone(cx, cy, rx, ry, top or fg, tilt)


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:76ch;color:#5B544C;margin:0 0 28px}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.c{background:#fff;border-radius:14px;padding:18px}
    .c h3{font:400 20px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:13px;color:#5B544C;margin:0 0 10px;min-height:40px}
    .c img{display:block;border-radius:10px;max-width:100%}.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .sz{display:flex;gap:14px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}.lk{display:flex;align-items:center;gap:10px;margin-top:14px;font:400 20px 'Hedvig Letters Serif'}.lk img{border-radius:50%}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>flat stack, round top</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>flat stack, round stone on top</h1><p class='in'>The client's pick. Flat stones of different sizes and shapes with air between them, and one rounded stone on top. Six builds. Left: Bark on Paper. Right: Sky stones on Bark with the round stone in Paper. Then the avatar at 110, 40 and 16 in both colorways, and the mark beside the wordmark.</p><div class='grid'>")
    for key in BUILDS:
        a = tile(draw(key, BK, PA), PA)
        b = tile(draw(key, SK, BK, PA), BK)
        av = lambda fg, bg, top: tile('<g transform="translate(120 118) scale(.84) translate(-120 -120)">%s</g>' % draw(key, fg, bg, top), bg, True)
        write(os.path.join(OUT, "flat-round-%s.svg" % key.replace(" ", "-")), tile(draw(key, BK, PA), "none"))
        h.append("<div class='c'><div class='two'>%s%s</div><h3>%s</h3><p>%s</p><div class='sz'>%s%s%s%s%s%s</div><div class='lk'>%s generation maine</div></div>" % (
            img(a, 230), img(b, 230), key, NOTES[key], img(av(BK, SK, BK), 110), img(av(BK, SK, BK), 40), img(av(BK, SK, BK), 16), img(av(SK, BK, PA), 110), img(av(SK, BK, PA), 40), img(av(SK, BK, PA), 16), img(av(BK, SK, BK), 40)))
    h.append("</div>")
    out = os.path.join(OUT, "flat-round.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "flat-round.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
