"""Round five: the cairn is out (it reads as the emoji at small sizes). Shapes with meaning that are built for 16 px:
the blaze, first light, Katahdin's profile, the lit window, the fine print, the threshold.

  python3 brand/src/build_marks5_barksky.py   # writes brand/identity/marks-bark-sky/round5/*.svg, candidates.html and .png
"""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky", "round5")
BK, SK, PA, CL = "#26201C", "#B9C9D3", "#F4F3EE", "#5B544C"
S = 240


def disc(bg):
    return '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg


def clipdisc(body, idn="d"):
    return '<defs><clipPath id="%s"><circle cx="120" cy="120" r="120"/></clipPath></defs><g clip-path="url(#%s)">%s</g>' % (idn, idn, body)


# 1 the blaze: one painted rectangle on a tree, the way a trail is marked in Maine. Sky on Bark is literally the name.
def blaze(fg, bg):
    # a hand-painted edge: a rectangle with slightly uneven corners
    return '<path d="M96 56 L146 54 L148 182 L94 186 Z" fill="%s"/>' % fg


def blaze_double(fg, bg):
    # two blazes, offset: on the trail this means a turn is coming
    return '<path d="M84 44 L134 42 L136 106 L82 109 Z" fill="%s"/><path d="M106 130 L156 128 L158 194 L104 198 Z" fill="%s"/>' % (fg, fg)


def blaze_disc(fg, bg):
    return disc(bg) + '<path d="M96 56 L146 54 L148 182 L94 186 Z" fill="%s"/>' % fg


# 2 first light: the sun's first edge over the horizon. The first sunrise in the United States lands on Maine.
def first_light(fg, bg):
    hy = 142
    return (clipdisc('<rect width="240" height="%d" fill="%s"/><rect y="%d" width="240" height="%d" fill="%s"/>' % (hy, bg, hy, 240 - hy, fg)
                     + '<circle cx="120" cy="%d" r="46" fill="%s"/>' % (hy + 6, fg), "fl")
            + '<rect y="%d" width="240" height="%d" fill="%s" clip-path="url(#fl)"/>' % (hy, 240 - hy, fg))


def first_light_thin(fg, bg):
    """Only the sun's edge: a thin arc of light sitting on the ground line."""
    hy = 146
    return clipdisc('<rect width="240" height="240" fill="%s"/><rect y="%d" width="240" height="%d" fill="%s"/>' % (bg, hy, 240 - hy, fg)
                    + '<path d="M66 %d A54 54 0 0 1 174 %d" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % (hy - 2, hy - 2, fg), "flt")


# 3 Katahdin: the flat top and the Knife Edge as the line between ground and sky
def katahdin(fg, bg):
    ridge = "M0 170 L40 160 L70 118 L96 96 L128 92 L160 104 L182 124 L200 134 L240 156 L240 240 L0 240 Z"
    return clipdisc('<rect width="240" height="240" fill="%s"/><path d="%s" fill="%s"/>' % (bg, ridge, fg), "kt")


def katahdin_line(fg, bg):
    ridge = "M0 170 L40 160 L70 118 L96 96 L128 92 L160 104 L182 124 L200 134 L240 156"
    return disc(bg) + '<g clip-path="url(#kl)"><path d="%s" fill="none" stroke="%s" stroke-width="12" stroke-linejoin="round"/></g><defs><clipPath id="kl"><circle cx="120" cy="120" r="120"/></clipPath></defs>' % (ridge, fg)


# 4 the lit window: one window in a small town with a light on. Somebody stayed.
def window(fg, bg):
    return ('<rect x="62" y="40" width="116" height="160" rx="6" fill="%s"/>' % fg
            + '<rect x="74" y="52" width="44" height="64" fill="%s"/><rect x="122" y="52" width="44" height="64" fill="%s"/>'
              '<rect x="74" y="124" width="44" height="64" fill="%s"/><rect x="122" y="124" width="44" height="64" fill="%s"/>' % (bg, bg, SK if fg == BK else PA, bg))


# 5 the fine print: a sheet with three short lines, one of them long. The rules nobody reads until they cost them.
def fine_print(fg, bg):
    return ('<path d="M66 40 L174 40 L174 196 L160 206 L148 196 L136 206 L124 196 L112 206 L100 196 L88 206 L76 196 L66 206 Z" fill="%s"/>' % fg
            + '<rect x="86" y="72" width="68" height="10" rx="5" fill="%s"/><rect x="86" y="98" width="40" height="10" rx="5" fill="%s"/><rect x="86" y="124" width="56" height="10" rx="5" fill="%s"/>' % (bg, bg, bg))


# 6 the threshold: a doorway, open, with the sky through it. Building a life here starts with a door.
def threshold(fg, bg):
    return ('<path d="M56 206 L56 60 Q56 36 80 36 L160 36 Q184 36 184 60 L184 206 Z" fill="%s"/>' % fg
            + '<path d="M78 206 L78 66 Q78 56 88 56 L152 56 Q162 56 162 66 L162 206 Z" fill="%s"/>' % (SK if fg == BK else PA)
            + '<path d="M78 206 L78 66 Q78 56 88 56 L120 54 L120 206 Z" fill="%s"/>' % bg)


CANDS = [
    ("blaze", "the blaze", "One painted rectangle on a tree, the way a trail is marked in Maine. Sky on Bark is the name of the direction, literally. Means: you are on the path, keep going. Reads at any size.", blaze),
    ("blaze-double", "the double blaze", "Two blazes offset. On the trail it means a turn ahead. A second form for free.", blaze_double),
    ("first-light", "first light", "The sun's edge over the ground line. The first sunrise in the United States lands on Maine, on Cadillac and at West Quoddy. A new generation and a new day, in the ground and sky disc.", first_light),
    ("first-light-thin", "first light, as a line", "Only the sun's edge, a thin arc on the ground. Quieter, closer to the serif.", first_light_thin),
    ("katahdin", "Katahdin", "The flat top and the Knife Edge as the line between ground and sky. Every Mainer knows the profile. The hero loop opens on it.", katahdin),
    ("katahdin-line", "Katahdin, as a line", "The same profile drawn as one line, in the disc.", katahdin_line),
    ("window", "the lit window", "One window in a small town with one light on. Somebody stayed. Risk: a two by two grid is a software logo.", window),
    ("fine-print", "the fine print", "A sheet with a torn edge and three short lines. The rules nobody reads until they cost them. Risk: it is an icon more than a mark.", fine_print),
    ("threshold", "the threshold", "A doorway, half open, with the sky through it. Building a life here starts with a door and a lease. Risk: real estate.", threshold),
]


def tile(body, bg, round_=False):
    base = '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg if round_ else '<rect width="240" height="240" rx="28" fill="%s"/>' % bg
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">%s%s</svg>' % (base, body)


def img(svg, px):
    return '<img src="data:image/svg+xml;base64,%s" style="width:%dpx;height:%dpx;display:block">' % (base64.b64encode(svg.encode()).decode(), px, px)


def build():
    os.makedirs(OUT, exist_ok=True)
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px}p.in{max-width:76ch;color:#5B544C;margin:0 0 28px}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.c{background:#fff;border-radius:14px;padding:18px}
    .c h3{font:400 21px 'Hedvig Letters Serif';margin:10px 0 2px}.c p{font-size:13px;color:#5B544C;margin:0 0 10px;min-height:78px}
    .c img{border-radius:10px}.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.two img{width:100%!important;height:auto!important}
    .sz{display:flex;gap:14px;align-items:flex-end;margin-top:12px}.sz img{border-radius:50%}.lk{display:flex;align-items:center;gap:10px;margin-top:14px;font:400 20px 'Hedvig Letters Serif'}.lk img{border-radius:50%}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>round five</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>round five: shapes with meaning, built for 16 px</h1><p class='in'>The cairn is out. Each idea here is one or two shapes with a reason to exist, shown in Bark on Paper and Sky on Bark, then as the avatar at 110, 40 and 16 in both, and beside the wordmark.</p><div class='grid'>")
    for key, name, note, fn in CANDS:
        is_disc = key in ("first-light", "first-light-thin", "katahdin", "katahdin-line")
        a = tile(fn(BK, PA), PA); b = tile(fn(SK, BK), BK)
        def av(fg, bg):
            if is_disc:
                return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">%s</svg>' % fn(fg, bg)
            return tile('<g transform="translate(120 120) scale(.72) translate(-120 -120)">%s</g>' % fn(fg, bg), bg, True)
        write(os.path.join(OUT, key + ".svg"), tile(fn(BK, PA), "none"))
        h.append("<div class='c'><div class='two'>%s%s</div><h3>%s</h3><p>%s</p><div class='sz'>%s%s%s%s%s%s</div><div class='lk'>%s generation maine</div></div>" % (
            img(a, 200), img(b, 200), name, note, img(av(BK, SK), 110), img(av(BK, SK), 40), img(av(BK, SK), 16), img(av(SK, BK), 110), img(av(SK, BK), 40), img(av(SK, BK), 16), img(av(BK, SK), 40)))
    h.append("</div>")
    out = os.path.join(OUT, "candidates.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "candidates.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
