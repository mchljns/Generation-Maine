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
            [(40, 206), (44, 188), (90, 185), (140, 186), (196, 180), (202, 206)],                 # base: long, thick at the right
            [(70, 185), (66, 162), (108, 156), (150, 162), (152, 182)],                            # second: shorter, thick at the left, set left
            [(58, 161), (62, 148), (120, 142), (176, 150), (178, 160)],                            # third: wider than the second, overhangs both sides
            [(96, 148), (94, 122), (116, 114), (142, 120), (146, 146)],                           # fourth: a chunky block with a dip
        ],
        "round": (121, 96, 26, 20, -6),
        "note": "A long base, a shorter wedge set left, a wider flat that overhangs it on both sides, a block with a dip, the round stone. The silhouette steps in and out instead of tapering.",
    },
    "wedges iii, leaning": {
        "flats": [
            [(46, 206), (50, 190), (120, 187), (198, 184), (204, 206)],
            [(56, 188), (54, 168), (98, 160), (168, 168), (170, 186)],
            [(40, 166), (44, 150), (100, 144), (150, 150), (152, 164)],
            [(58, 148), (60, 126), (84, 116), (118, 120), (120, 146)],
        ],
        "round": (90, 96, 24, 19, -10),
        "note": "Every top face slopes left so the stack leans as it rises, the third stone overhangs to the left, and the round stone sits near the edge, still over the block below.",
    },
    "wedges iv, five": {
        "flats": [
            [(36, 206), (40, 192), (124, 190), (198, 186), (204, 206)],
            [(60, 190), (58, 178), (120, 174), (182, 180), (184, 188)],
            [(74, 177), (70, 152), (112, 144), (160, 152), (162, 176)],
            [(52, 151), (56, 140), (120, 134), (170, 142), (172, 150)],
            [(100, 140), (98, 120), (120, 112), (142, 118), (144, 138)],
        ],
        "round": (122, 92, 24, 19, 4),
        "note": "Five flats: long thin base, thin second, thick wedge, a wide thin flat that overhangs, a small block. Thin and thick alternate, as real stacks settle.",
    },
    "wedges v, boulder base": {
        "flats": [
            [(44, 206), (40, 178), (64, 162), (120, 156), (176, 162), (198, 180), (202, 206)],
            [(60, 160), (62, 148), (120, 142), (180, 148), (182, 158)],
            [(92, 147), (90, 122), (112, 112), (144, 118), (148, 146)],
        ],
        "round": (118, 94, 26, 20, -4),
        "note": "A rounded boulder as the base, one long flat across it that overhangs the boulder, one wedge, the round stone. The heaviest thing is at the bottom.",
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


def sep(pts, fg, bg):
    """A stone with a hairline of background around it: the shadow line between stones in a real stack."""
    d = "M" + " L".join("%s %s" % p for p in pts) + " Z"
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="9" stroke-linejoin="round"/>' % (d, bg)
            + '<path d="%s" fill="%s" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (d, fg, fg))


def draw(key, fg, bg, top=None):
    b = BUILDS[key]
    cx, cy, rx, ry, tilt = b["round"]
    body = "".join(sep(p, fg, bg) for p in b["flats"])
    rs = round_stone(cx, cy, rx, ry, top or fg, tilt)
    halo = round_stone(cx, cy, rx + 3, ry + 3, bg, tilt)
    return body + halo + rs


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
