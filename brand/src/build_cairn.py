"""The cairn, decided. Two explorations: the stones (granite, fieldstone, slate, Acadia's Bates cairn, a tall pile) and color with the
mark fixed (the palette as it stands, the top stone picked out, stones graded, and two new accents tried: lichen and granite pink).

  python3 brand/src/build_cairn.py   # writes brand/identity/marks-bark-sky/cairn/*.svg, cairn.html and cairn.png
"""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "cairn")
BK, SK, PA, MIST, CL, BLUE = "#26201C", "#B9C9D3", "#F4F3EE", "#E4E8E6", "#5B544C", "#2B4760"
LICHEN, PINK, RUST = "#8E9B86", "#C8AFA3", "#A4553A"
S = 240

# ---- stone sets: each is a list of (path, label) from the base up, drawn in a 240 square, base at y≈206 ----
STONES = {
    "granite": ["M44 196 L58 160 L120 154 L186 158 L198 194 L172 202 L110 206 L62 204 Z",
                "M70 154 L80 120 L128 114 L166 122 L172 152 L138 158 L96 160 Z",
                "M88 114 L98 86 L132 78 L154 90 L158 112 L128 118 Z"],
    "fieldstone": ["M46 192 C50 164 84 150 124 152 C166 154 198 168 196 194 C194 210 160 208 120 208 C80 208 44 210 46 192 Z",
                   "M72 152 C70 128 92 112 126 112 C160 112 176 126 172 152 C170 162 148 160 124 160 C100 160 74 164 72 152 Z",
                   "M92 112 C92 90 110 76 132 78 C152 80 160 94 156 112 C150 118 134 118 124 118 C112 118 92 120 92 112 Z"],
    "slate": ["M40 196 L200 190 L202 206 L44 210 Z", "M56 178 L190 174 L190 190 L56 194 Z", "M66 160 L178 158 L180 174 L66 177 Z",
              "M78 142 L164 142 L166 158 L80 160 Z", "M92 122 L150 124 L150 142 L92 142 Z", "M106 102 L138 104 L140 122 L104 122 Z"],
    "bates": ["M52 206 L58 160 L94 160 L98 206 Z", "M142 206 L146 160 L182 160 L188 206 Z",  # two legs
              "M44 160 L48 140 L192 140 L196 160 Z",  # the lintel
              "M100 140 L112 100 L148 108 L140 140 Z"],  # the pointer stone, set toward the way
    "tall": ["M48 206 L58 176 L182 176 L192 206 Z", "M66 176 L74 150 L170 150 L176 176 Z", "M82 150 L88 126 L154 126 L160 150 Z",
             "M96 126 L100 106 L144 106 L146 126 Z", "M108 106 L112 90 L134 90 L136 106 Z", "M116 90 L118 78 L130 78 L130 90 Z"],
    "three-rough": ["M40 198 L52 170 L96 158 L150 162 L198 172 L196 200 L150 208 L84 208 Z",
                    "M86 158 L92 128 L132 118 L168 134 L164 160 L124 164 Z",
                    "M118 118 L126 92 L146 84 L158 94 L156 116 L132 120 Z"],
}
NOTES = {
    "granite": "split granite, flat tops, broken sides. The Katahdin cairn.",
    "fieldstone": "rounded fieldstone, the stones a farmer pulls from a field. Softer; watch for the spa reading.",
    "slate": "slate slabs, six thin courses. Reads as a stack of paper, which suits a brand about fine print.",
    "bates": "the Bates cairn. Acadia's own design, two legs, a lintel, and a pointer stone set toward the way. Only Maine builds these.",
    "tall": "a tall pile, six courses, the way summit cairns grow as each hiker adds one.",
    "three-rough": "three rough stones, each set off axis, as they fall.",
}


def cairn(stones, colors, scale=1.0, oy=0):
    if isinstance(colors, str):
        colors = [colors] * len(stones)
    g = '<g transform="translate(120 %s) scale(%s) translate(-120 -120)">' % (120 + oy, scale)
    return g + "".join('<path d="%s" fill="%s"/>' % (d, c) for d, c in zip(stones, colors)) + "</g>"


def tile(body, bg, round_=False, size=S):
    shape = '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg if round_ else '<rect width="240" height="240" rx="28" fill="%s"/>' % bg
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">%s%s</svg>' % (shape, body)


def img(svg, px, h=None):
    return '<img src="data:image/svg+xml;base64,%s" width="%d" height="%d" style="width:%dpx;height:%dpx">' % (base64.b64encode(svg.encode()).decode(), px, h or px, px, h or px)


def build():
    os.makedirs(OUT, exist_ok=True)
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}h2{font:400 26px/1.1 'Hedvig Letters Serif';margin:52px 0 6px}
    p.in{max-width:72ch;color:#5B544C;margin:0 0 24px}
    .grid{display:grid;grid-template-columns:repeat(6,1fr);gap:18px}.grid3{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
    .c{background:#fff;border-radius:14px;padding:16px}.c h3{font:400 18px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:12.5px;color:#5B544C;margin:0;min-height:56px}
    .c img{display:block;width:100%;height:auto;border-radius:10px}.sz{display:flex;gap:12px;align-items:flex-end;margin-top:10px}.sz img{width:auto;border-radius:50%}
    .sw{display:flex;gap:6px;margin-top:8px}.sw i{display:block;width:22px;height:22px;border-radius:6px;border:1px solid rgba(0,0,0,.08)}
    .pal{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.pal .c{padding:0;overflow:hidden}.pal .c .top{padding:16px 16px 0}
    .page{padding:22px;display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:center}.page b{font:400 24px/1 'Hedvig Letters Serif';display:block}.page span{font-size:12px;color:#5B544C}
    .page img{border-radius:50%}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>The cairn</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>the cairn, decided</h1><p class='in'>Two questions from the client: should the stones vary, and what does color theory look like with the mark fixed. Stones first, then color.</p>")

    # ---- stones ----
    h.append("<h2>the stones</h2><p class='in'>Six builds, each in Bark on Sky and as the avatar at 110, 40 and 16 px.</p><div class='grid'>")
    for key, stones in STONES.items():
        big = tile(cairn(stones, BK, 1.0, -8), SK)
        av = tile(cairn(stones, BK, 0.84, -8), SK, True)
        write(os.path.join(OUT, "stones-%s.svg" % key), tile(cairn(stones, BK, 1.0, -8), "none"))
        h.append("<div class='c'>%s<h3>%s</h3><p>%s</p><div class='sz'>%s%s%s</div></div>" % (img(big, 200), key.replace("-", " "), NOTES[key], img(av, 110), img(av, 40), img(av, 16)))
    h.append("</div>")

    # ---- color ----
    G = STONES["granite"]
    h.append("<h2>color, with the mark fixed</h2><p class='in'>The palette as it stands, then the top stone picked out (the one you add), then the stones graded from ground to sky, then two new accents tried against the mark: lichen and granite pink. Each shows the mark in a field, and the swatches it needs.</p>")
    schemes = [
        ("as it stands", "Bark stones on Sky. Quiet, one color, the identity as built.", [BK] * 3, SK, [BK, SK, PA, CL]),
        ("reversed", "Sky stones on Bark. The dark mode and the end card.", [SK] * 3, BK, [BK, SK, PA, CL]),
        ("on paper", "Bark on Paper, for print and the page body.", [BK] * 3, PA, [BK, PA, CL]),
        ("the one you add", "Two Bark stones and the top one in Sky. The people before you built the base; the sky stone is the one this generation adds. The mark gains a story at a glance.", [BK, BK, SK], PA, [BK, SK, PA]),
        ("the one you add, on bark", "The same idea on the dark field: the top stone is Paper, the base is Clay.", [CL, CL, PA], BK, [BK, CL, PA]),
        ("graded", "Base in Bark, middle in Clay, top in Sky. Ground to sky in three steps, which is the whole palette in one object.", [BK, CL, SK], PA, [BK, CL, SK, PA]),
        ("lichen", "A new accent: the grey green of lichen on granite. Natural beside Bark and Sky, and the first color in the system that is not grey, brown or blue. Risk: it reads eco.", [BK, BK, LICHEN], PA, [BK, SK, PA, LICHEN]),
        ("granite pink", "A new accent: the warm pink of Maine granite in low sun. Warms the whole palette, pairs with Sky as a near complement, and no Maine brand owns it. Risk: it softens a direction that was asked to skew masculine.", [BK, BK, PINK], PA, [BK, SK, PA, PINK]),
        ("rust", "A new accent: iron rust, the color of a Katahdin trail sign bracket. The strongest contrast with Sky. Risk: it reads as a warning color at small sizes.", [BK, BK, RUST], PA, [BK, SK, PA, RUST]),
    ]
    h.append("<div class='pal'>")
    for name, note, cols, bg, sw in schemes:
        big = tile(cairn(G, cols, 1.0, -8), bg)
        av = tile(cairn(G, cols, 0.84, -8), bg if bg != PA else SK, True)
        write(os.path.join(OUT, "color-%s.svg" % name.replace(" ", "-").replace(",", "")), big)
        h.append("<div class='c'><div class='top'>%s<h3>%s</h3><p>%s</p><div class='sw'>%s</div><div class='sz'>%s%s%s</div></div><div class='page'>%s<div><b>generation maine</b><span>the mark beside the stacked wordmark, 56 px</span></div></div></div>"
                 % (img(big, 300), name, note, "".join('<i style="background:%s"></i>' % c for c in sw), img(av, 110), img(av, 40), img(av, 16), img(tile(cairn(G, cols, 0.84, -8), bg if bg != PA else SK, True), 56)))
    h.append("</div>")

    out = os.path.join(OUT, "cairn.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "cairn.png"), "1600", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
