"""Can 207 be drawn so it belongs to this brand alone? Five constructions, each at 110, 40 and 16 px, both colorways.

  python3 brand/src/build_207.py   # writes brand/identity/marks-bark-sky/207.html and 207.png
"""
import base64
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky")
BK, SK, PA, CL = "#26201C", "#B9C9D3", "#F4F3EE", "#5B544C"
SERIF = Face("d/HedvigLettersSerif-24.ttf")
MONO = Face("alt/IBMPlexMono-Medium.ttf")
S = 240


def bbox(d):
    xs, ys = [], []
    for m in re.finditer(r"(-?\d+\.?\d*) (-?\d+\.?\d*)", d):
        xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    return min(xs), min(ys), max(xs), max(ys)


def glyph(text, size, cx, cy, face=SERIF):
    d, _ = face.path(text, size, 0, 0)
    x0, y0, x1, y1 = bbox(d)
    d, _ = face.path(text, size, cx - (x0 + x1) / 2, cy - (y0 + y1) / 2)
    return d


def disc(bg, body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><defs><clipPath id="disc"><circle cx="%d" cy="%d" r="%d"/></clipPath>%s</defs>'
            '<circle cx="%d" cy="%d" r="%d" fill="%s"/><g clip-path="url(#disc)">%s</g></svg>') % (S, S, S / 2, S / 2, S / 2, defs, S / 2, S / 2, S / 2, bg, body)


# A. one line: the three digits written in a single unbroken stroke that shares one baseline, the way a hand would write
# them without lifting. The 0 is a loop the line makes on its way to the 7.
def one_line(fg, bg):
    d = ("M40 98 A21 21 0 0 1 82 98 C82 122 56 148 40 170 L118 170 "
         "A21 44 0 0 1 118 82 A21 44 0 0 1 118 170 L166 170 L200 72 L146 72")
    return disc(bg, '<path d="%s" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>' % (d, fg))


# B. horizon: the serif digits stand on a low horizon. Above it Bark on Sky, below it the colors swap, like ground and sky.
def horizon(fg, bg):
    d = glyph("207", 112, S / 2, 128)
    hy = 152
    defs = '<clipPath id="up"><rect x="0" y="0" width="%d" height="%d"/></clipPath><clipPath id="dn"><rect x="0" y="%d" width="%d" height="%d"/></clipPath>' % (S, hy, hy, S, S - hy)
    body = ('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (hy, S, S - hy, fg) +
            '<path d="%s" fill="%s" clip-path="url(#up)"/><path d="%s" fill="%s" clip-path="url(#dn)"/>' % (d, fg, d, bg))
    return disc(bg, body, defs)


# C. the disc is the zero: 2 and 7 in the serif, and between them a ring that is the only drawn shape
def ring_zero(fg, bg):
    return disc(bg, '<path d="%s" fill="%s"/><path d="%s" fill="%s"/><circle cx="%d" cy="%d" r="26" fill="none" stroke="%s" stroke-width="12"/>' %
                (glyph("2", 110, 66, 122), fg, glyph("7", 110, 176, 122), fg, S / 2, 122, fg))


# D. the stack: 2 over 0 over 7 in the numbers face, like a mile marker
def stack(fg, bg):
    return disc(bg, "".join('<path d="%s" fill="%s"/>' % (glyph(c, 64, S / 2, y, MONO), fg) for c, y in (("2", 66), ("0", 120), ("7", 174))))


# E. said out loud: two oh seven, the way the voice would write it
def words(fg, bg):
    return disc(bg, "".join('<path d="%s" fill="%s"/>' % (glyph(w, 46, S / 2, y), fg) for w, y in (("two", 76), ("oh", 120), ("seven", 164))))


OPTIONS = [("one line", "The three digits written without lifting the pen, on one shared baseline. The 0 is a loop the line makes on its way to the 7. Nobody else's 207 is drawn like this.", one_line),
           ("the horizon", "The serif digits stand on a low horizon and the colors swap below it. Ground and sky, which the client liked in an earlier round, with the number standing in it.", horizon),
           ("the disc is the zero", "Only the 2 and the 7 are set; the zero is a ring, the same shape as the avatar itself. Reads as a device, not a number, until you know.", ring_zero),
           ("the stack", "2 over 0 over 7 in the numbers face, like a mile marker on Route 1. Reads at 16 px because each digit gets the width.", stack),
           ("said out loud", "two oh seven, in words, the way the voice would say it. Plain, and unlike every 207 shirt. Fails below 40 px.", words)]


def img(svgtxt, px):
    return '<img src="data:image/svg+xml;base64,%s" width="%d" height="%d">' % (base64.b64encode(svgtxt.encode()).decode(), px, px)


def build():
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px;letter-spacing:-.01em}p.in{max-width:70ch;color:#5B544C;margin:0 0 28px}
    .row{display:grid;grid-template-columns:repeat(5,1fr);gap:22px;align-items:start;margin-bottom:22px}
    .card{background:#fff;border-radius:14px;padding:22px}.card h3{font:400 20px 'Hedvig Letters Serif';margin:0 0 4px}
    .card p{font-size:13px;color:#5B544C;margin:0 0 16px;min-height:120px}
    .sizes{display:flex;gap:18px;align-items:flex-end}.sizes div{text-align:center;font:12px 'IBM Plex Mono',monospace;color:#5B544C}.sizes img{display:block;margin:0 auto 6px}
    .big{display:grid;grid-template-columns:repeat(5,1fr);gap:22px}.big img{width:100%;height:auto;display:block}
    .ctx{display:flex;gap:28px;margin-top:40px;align-items:center}.bar{display:flex;align-items:center;gap:14px;border-radius:999px;padding:12px 22px 12px 12px;background:#fff}
    .bar b{font:400 22px 'Hedvig Letters Serif'}.chrome{display:flex;align-items:center;gap:8px;background:#E4E8E6;border-radius:8px;padding:8px 12px;font-size:13px}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>207</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>207, if it has to be ours alone</h1><p class='in'>The client's bar: 207 is everywhere in Maine, so a plain 207 in a disc does not get in. Five constructions that could belong to this brand only. Each at 110, 40 and 16 px, Bark on Sky, then Sky on Bark.</p>")
    h.append('<div class="big">%s</div>' % "".join(img(fn(BK, SK), 260) for _, _, fn in OPTIONS))
    for fg, bg in ((BK, SK), (SK, BK)):
        h.append('<div class="row">')
        for name, note, fn in OPTIONS:
            s = fn(fg, bg)
            h.append('<div class="card"><h3>%s</h3><p>%s</p><div class="sizes">%s</div></div>' % (name, note, "".join('<div>%s%d</div>' % (img(s, px), px) for px in (110, 40, 16))))
        h.append('</div>')
    h.append('<div class="ctx">%s</div>' % "".join('<div class="bar">%s<b>generation maine</b></div><div class="chrome">%s generation maine</div>' % (img(fn(BK, SK), 44), img(fn(BK, SK), 16)) for _, _, fn in OPTIONS[:2]))
    out = os.path.join(OUT, "207.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "207.png"), "1600", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
