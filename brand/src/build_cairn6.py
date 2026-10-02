"""Wedges, with more variation in every stone and a stack that is physically possible: each stone's underside rests on the
stone below at two points, its center of mass sits inside the bearing surface under it, and the round stone sits in the dip
of the top wedge. Four builds, with a numeric balance check printed for each.

  python3 brand/src/build_cairn6.py   # writes brand/identity/marks-bark-sky/cairn/wedges.html and wedges.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_cairn import BK, SK, PA, CL, tile, img
from build_cairn4 import stone
from build_cairn5 import round_stone

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")

# Each flat stone: a polygon listed clockwise from the bottom left. Its bottom edge is the first and last point. The round
# stone: (cx, cy, rx, ry, tilt). Coordinates are in a 240 square with the ground at y = 206.
BUILDS = {
    "wedges ii": {
        "flats": [
            [(36, 206), (40, 186), (74, 183), (122, 184), (170, 178), (204, 176), (208, 206)],        # base: long, thick at the right, a dip in the middle
            [(64, 183), (60, 160), (92, 152), (146, 158), (178, 165), (178, 178)],                    # second: thick at the left, a broken top corner
            [(80, 155), (82, 146), (118, 141), (156, 147), (160, 160)],                                # third: a thin flat, slightly crowned
            [(96, 145), (92, 120), (112, 110), (140, 114), (154, 124), (152, 146)],                   # fourth: a chunky wedge with a saddle on top
        ],
        "round": (124, 92, 27, 21, -6),
        "note": "Four flats, no two alike: a long base thick at one end, a second stone thick at the other, a thin crowned flat, a chunky wedge with a saddle. The round stone sits in the saddle.",
    },
    "wedges iii, leaning": {
        "flats": [
            [(44, 206), (46, 190), (100, 186), (150, 188), (200, 182), (206, 206)],
            [(50, 187), (48, 166), (84, 158), (128, 162), (174, 170), (176, 184)],
            [(44, 162), (46, 142), (96, 136), (140, 142), (146, 158)],
            [(56, 141), (60, 120), (84, 110), (118, 114), (124, 128), (126, 142)],
        ],
        "round": (92, 92, 25, 20, -10),
        "note": "The same rules with every top face sloping left, so the stack leans left as it rises and the round stone sits near the edge, still over the stone below.",
    },
    "wedges iv, five": {
        "flats": [
            [(34, 206), (38, 190), (120, 188), (200, 184), (206, 206)],
            [(52, 189), (50, 176), (116, 172), (184, 178), (186, 186)],
            [(70, 174), (66, 150), (104, 142), (148, 148), (172, 158), (170, 176)],
            [(84, 150), (86, 140), (130, 136), (158, 142), (160, 156)],
            [(100, 139), (98, 118), (122, 108), (144, 116), (146, 140)],
        ],
        "round": (124, 90, 24, 19, 4),
        "note": "Five flats: a long thin base, a thin second, a thick wedge, a thin flat, a small block. Thin and thick alternate, which is how real stacks settle.",
    },
    "wedges v, boulder base": {
        "flats": [
            [(40, 206), (36, 176), (62, 160), (120, 154), (176, 160), (200, 178), (204, 206)],        # a rounded boulder as the base
            [(70, 159), (68, 146), (116, 140), (168, 146), (170, 160)],                                # a flat across the boulder
            [(90, 144), (86, 122), (112, 112), (146, 118), (152, 144)],                                # a wedge
        ],
        "round": (118, 92, 26, 20, -4),
        "note": "A rounded boulder as the base, one flat across it, one wedge, the round stone. Three shapes in three stones, and the heaviest thing is at the bottom.",
    },
}


def centroid(pts):
    a = cx = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c; cx += (x0 + x1) * c
    a *= 0.5
    return cx / (6 * a) if a else sum(p[0] for p in pts) / len(pts)


def check(build):
    """Does every stone's center of mass sit over the bearing surface of the stone below? Returns a list of (ok, cx, lo, hi)."""
    out = []
    flats = build["flats"]
    for i, pts in enumerate(flats):
        cx = centroid(pts)
        if i == 0:
            out.append((True, cx, pts[0][0], pts[-1][0])); continue
        below = flats[i - 1]
        lo, hi = max(pts[0][0], min(p[0] for p in below)), min(pts[-1][0], max(p[0] for p in below))
        out.append((lo <= cx <= hi, cx, lo, hi))
    rcx = build["round"][0]; top = flats[-1]
    out.append((top[0][0] <= rcx <= top[-1][0], rcx, top[0][0], top[-1][0]))
    return out


def draw(key, fg, bg, top=None):
    b = BUILDS[key]
    cx, cy, rx, ry, tilt = b["round"]
    return "".join(stone(p, fg, 3) for p in b["flats"]) + round_stone(cx, cy, rx, ry, top or fg, tilt)


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:76ch;color:#5B544C;margin:0 0 28px}
    .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}.c{background:#fff;border-radius:14px;padding:18px}
    .c h3{font:400 22px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:13.5px;color:#5B544C;margin:0 0 10px}
    .c img{display:block;border-radius:10px;max-width:100%}.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .sz{display:flex;gap:14px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}.lk{display:flex;align-items:center;gap:10px;margin-top:14px;font:400 22px 'Hedvig Letters Serif'}.lk img{border-radius:50%}
    .ok{font:11px 'IBM Plex Mono',monospace;color:#5B544C;margin-top:8px}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>wedges</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>wedges, varied and standing up</h1><p class='in'>Every stone its own shape, and a stack that obeys gravity: each stone rests on the one below at two points, its center of mass sits over the bearing surface under it, and the round stone sits in the dip of the top wedge. The balance line under each build is the numeric check: the center of each stone against the span it rests on.</p><div class='grid'>")
    for key, b in BUILDS.items():
        a = tile(draw(key, BK, PA), PA); d = tile(draw(key, SK, BK, PA), BK)
        av = lambda fg, bg, top: tile('<g transform="translate(120 118) scale(.84) translate(-120 -120)">%s</g>' % draw(key, fg, bg, top), bg, True)
        write(os.path.join(OUT, "wedges-%s.svg" % key.split(",")[0].replace(" ", "-")), tile(draw(key, BK, PA), "none"))
        chk = check(b)
        line = " ".join("%s%d[%d-%d]" % ("ok " if ok else "OFF ", cx, lo, hi) for ok, cx, lo, hi in chk)
        print(key, "balanced" if all(c[0] for c in chk) else "UNBALANCED", line)
        h.append("<div class='c'><div class='two'>%s%s</div><h3>%s</h3><p>%s</p><div class='ok'>balance: %s</div><div class='sz'>%s%s%s%s%s%s</div><div class='lk'>%s generation maine</div></div>" % (
            img(a, 300), img(d, 300), key, b["note"], line, img(av(BK, SK, BK), 110), img(av(BK, SK, BK), 40), img(av(BK, SK, BK), 16), img(av(SK, BK, PA), 110), img(av(SK, BK, PA), 40), img(av(SK, BK, PA), 16), img(av(BK, SK, BK), 44)))
    h.append("</div>")
    out = os.path.join(OUT, "wedges.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "wedges.png"), "1400", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
