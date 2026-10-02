"""Mixed stones: every stone a different shape and size, with air between them, the way a real trail cairn is built from whatever
was at hand. Six builds, with the top stone in Sky as the second colorway.

  python3 brand/src/build_cairn3.py   # writes brand/identity/marks-bark-sky/cairn/mixed.html and mixed.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_cairn import BK, SK, PA, CL, tile, img
from build_cairn2 import poly, solid

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")

BUILDS = [
    ("boulder and cap", "One big boulder, a flat slab across it, a small wedge on top. Three stones, three shapes.",
     [[(44, 206), (40, 160), (74, 128), (150, 124), (196, 156), (200, 206)],
      [(56, 118), (62, 100), (176, 96), (182, 118)],
      [(122, 90), (132, 64), (158, 60), (166, 86)]]),
    ("four at hand", "A wide slab, a chunky block set left, a thin flat stone, and a chip on top. Whatever was there.",
     [[(36, 206), (40, 182), (204, 180), (206, 206)],
      [(54, 172), (60, 126), (128, 120), (134, 172)],
      [(70, 112), (74, 98), (178, 94), (184, 112)],
      [(118, 86), (128, 68), (152, 66), (156, 86)]]),
    ("leaning", "Five stones, each set a little further left as they rise, the way a cairn settles over years. Reads as handmade.",
     [[(50, 206), (56, 180), (196, 178), (198, 206)],
      [(62, 170), (66, 146), (176, 142), (178, 170)],
      [(58, 134), (64, 112), (154, 108), (156, 134)],
      [(54, 100), (62, 80), (128, 78), (126, 100)],
      [(64, 70), (72, 52), (104, 50), (102, 70)]]),
    ("big top", "Small base stones and a wide flat stone across them, then a chip. The top-heavy silhouette is unlike any pile.",
     [[(56, 206), (60, 176), (108, 174), (110, 206)],
      [(136, 206), (140, 180), (184, 178), (190, 206)],
      [(36, 166), (42, 136), (200, 130), (206, 166)],
      [(104, 122), (112, 100), (146, 98), (150, 122)]]),
    ("wedge and block", "A tall block on a flat base, with a wedge leaned against the side and a stone balanced on top. Asymmetric.",
     [[(40, 206), (44, 184), (200, 182), (204, 206)],
      [(92, 174), (96, 104), (158, 100), (164, 174)],
      [(50, 174), (60, 140), (86, 134), (84, 174)],
      [(100, 92), (112, 72), (150, 68), (156, 92)]]),
    ("six small", "Six small stones of six sizes. More like the real thing above the treeline; a texture at 16 px.",
     [[(44, 206), (48, 186), (122, 184), (126, 206)], [(134, 206), (140, 182), (198, 180), (200, 206)],
      [(66, 176), (70, 152), (150, 148), (156, 176)], [(160, 172), (166, 152), (190, 150), (192, 172)],
      [(84, 140), (90, 116), (142, 112), (146, 140)], [(104, 104), (112, 84), (140, 82), (142, 104)]]),
]


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:72ch;color:#5B544C;margin:0 0 28px}
    .grid{display:grid;grid-template-columns:repeat(6,1fr);gap:18px}.c{background:#fff;border-radius:14px;padding:16px}
    .c h3{font:400 18px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:12.5px;color:#5B544C;margin:0 0 10px;min-height:80px}
    .c img{display:block;border-radius:10px;max-width:100%}.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sz{display:flex;gap:12px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}
    .lk{display:flex;align-items:center;gap:10px;margin-top:14px;font:400 19px 'Hedvig Letters Serif'}.lk img{border-radius:50%}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>mixed stones</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>mixed stones</h1><p class='in'>Every stone a different shape and size, with air between them, the way a trail cairn is built from what was at hand. Left: Bark on Paper. Right: the top stone in Sky, on Bark. Then the avatar at 40 and 16 in both, and the mark beside the wordmark.</p><div class='grid'>")
    for name, note, stones in BUILDS:
        n = len(stones)
        a = tile(solid(stones, BK, PA), PA)
        b = tile(solid(stones, [SK] * (n - 1) + [PA], BK), BK)
        def av(fg, bg, top):
            return tile('<g transform="translate(120 114) scale(.86) translate(-120 -120)">%s</g>' % solid(stones, [fg] * (n - 1) + [top], bg), bg, True)
        write(os.path.join(OUT, "mixed-%s.svg" % name.replace(" ", "-")), tile(solid(stones, BK, "none"), "none"))
        h.append("<div class='c'><div class='two'>%s%s</div><h3>%s</h3><p>%s</p><div class='sz'>%s%s%s%s</div><div class='lk'>%s generation maine</div></div>" % (
            img(a, 110), img(b, 110), name, note, img(av(BK, SK, BK), 40), img(av(BK, SK, BK), 16), img(av(SK, BK, PA), 40), img(av(SK, BK, PA), 16), img(av(BK, SK, BK), 36)))
    h.append("</div>")
    out = os.path.join(OUT, "mixed.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "mixed.png"), "1600", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
