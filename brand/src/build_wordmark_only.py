"""Can Bark & Sky live on the wordmark alone? The stacked wordmark at working sizes, and avatar and favicon options that use
no brand mark and no initials: the name itself, the word maine, the quotation mark, the period, and the colors as the mark.

  python3 brand/src/build_wordmark_only.py   # writes brand/identity/marks-bark-sky/wordmark-only-2.html and .png
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write

OUT = os.path.join(ROOT, "brand", "identity", "marks-bark-sky")
LOGO = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
BK, SK, PA, CL = "#26201C", "#B9C9D3", "#F4F3EE", "#5B544C"
SERIF = Face("d/HedvigLettersSerif-24.ttf")
MONO = Face("alt/IBMPlexMono-Medium.ttf")
S = 240


def bbox(d):
    xs, ys = [], []
    for m in re.finditer(r"(-?\d+\.?\d*) (-?\d+\.?\d*)", d):
        xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    return min(xs), min(ys), max(xs), max(ys)


def word(text, fg, size, dy=0, dx=0, face=None):
    face = face or SERIF
    d, _ = face.path(text, size, 0, 0)
    x0, y0, x1, y1 = bbox(d)
    d, _ = face.path(text, size, S / 2 - (x0 + x1) / 2 + dx, S / 2 - (y0 + y1) / 2 + dy)
    return '<path fill="%s" d="%s"/>' % (fg, d)


def disc(bg, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><circle cx="%d" cy="%d" r="%d" fill="%s"/>%s</svg>' % (S, S, S / 2, S / 2, S / 2, bg, body)


def disc_clip(bg, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><defs><clipPath id="c"><circle cx="%d" cy="%d" r="%d"/></clipPath></defs>'
            '<circle cx="%d" cy="%d" r="%d" fill="%s"/><g clip-path="url(#c)">%s</g></svg>') % (S, S, S / 2, S / 2, S / 2, S / 2, S / 2, S / 2, bg, body)


def stacked_name(fg, size):
    """generation over maine, left aligned, as the stacked wordmark sets it."""
    a, wa = SERIF.path("generation", size, 0, 0)
    b, wb = SERIF.path("maine", size, 0, 0)
    x0, y0, x1, y1 = bbox(a)
    lead = size * 0.98
    tot_h = (y1 - y0) + lead
    ox = S / 2 - (x0 + x1) / 2
    oy = S / 2 - (y0 + y1 + lead) / 2
    a, _ = SERIF.path("generation", size, ox, oy)
    b, _ = SERIF.path("maine", size, ox, oy + lead)
    return '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg, a, fg, b)


def options():
    o = []
    o.append(("207", "The area code. Every Mainer's number, already on shirts and in handles. Set in Plex Mono, the brand's numbers face. Digits read at 16 px.",
              lambda fg, bg: disc(bg, word("207", fg, 96, face=MONO))))
    o.append(("207, serif", "The same number in the wordmark's face, so it matches the name rather than the counters.",
              lambda fg, bg: disc(bg, word("207", fg, 104))))
    o.append(("me", "The postal abbreviation, lowercase, which is also the word. Two letters that are not the brand's initials. Reads at 16 px.",
              lambda fg, bg: disc(bg, word("me", fg, 120, dy=-6))))
    o.append(("me.", "The abbreviation with the voice's full stop. A sentence about whose story it is.",
              lambda fg, bg: disc(bg, word("me.", fg, 112, dy=-6, dx=6))))
    o.append(("maine", "The whole word. Reads at 40 px, a bar at 16.",
              lambda fg, bg: disc(bg, word("maine", fg, 76, dy=-4))))
    o.append(("sky over bark", "No letters. The two colors at a low horizon. A sticker more than an avatar.",
              lambda fg, bg: disc_clip(bg, '<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (S * 0.62, S, S * 0.38, fg))))
    return o


def img(svgtxt, px, extra=""):
    import base64
    return '<img src="data:image/svg+xml;base64,%s" width="%d" height="%d" %s>' % (base64.b64encode(svgtxt.encode()).decode(), px, px, extra)


def file_img(name, w, cls=""):
    p = os.path.join(LOGO, name + ".svg")
    return '<img class="%s" src="file://%s" style="width:%dpx;height:auto">' % (cls, p, w)


def build():
    os.makedirs(OUT, exist_ok=True)
    css = """body{margin:0;background:#F4F3EE;color:#26201C;font:16px/1.5 'Hedvig Letters Sans',system-ui;padding:56px 64px}
    h1{font:400 40px/1.05 'Hedvig Letters Serif';margin:0 0 10px;letter-spacing:-.01em}h2{font:400 26px/1.1 'Hedvig Letters Serif';margin:56px 0 6px}
    p.in{max-width:70ch;color:#5B544C;margin:0 0 24px}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;align-items:start}
    .card{background:#fff;border-radius:14px;padding:26px}.card.dark{background:#26201C;color:#B9C9D3}.card h3{font:400 20px 'Hedvig Letters Serif';margin:0 0 4px}
    .card p{font-size:14px;color:#5B544C;margin:0 0 16px;min-height:63px}.card.dark p{color:rgba(185,201,211,.8)}
    .sizes{display:flex;gap:22px;align-items:flex-end}.sizes div{text-align:center;font:12px 'IBM Plex Mono',monospace;color:#5B544C}.sizes img{display:block;margin:0 auto 6px}
    .stack{display:grid;grid-template-columns:1fr 1fr;gap:28px}.pane{border-radius:14px;padding:40px;display:flex;flex-direction:column;gap:40px;align-items:flex-start}
    .pane.light{background:#fff}.pane.dark{background:#26201C}.pane.sky{background:#B9C9D3}.lab{font:12px 'IBM Plex Mono',monospace;color:#5B544C;margin-top:8px}.pane.dark .lab{color:rgba(185,201,211,.7)}
    .bar{display:flex;justify-content:space-between;align-items:center;border-radius:999px;padding:14px 22px;background:#fff;width:600px}.bar span{font-size:14px;color:#5B544C}
    .chrome{display:flex;align-items:center;gap:8px;background:#E4E8E6;border-radius:8px;padding:8px 12px;font-size:13px;color:#26201C;width:260px}
    """
    h = ['<!doctype html><meta charset="utf-8"><title>Wordmark alone</title><style>%s</style>' % css]
    h.append("<h1>Bark &amp; Sky on the wordmark alone</h1><p class='in'>Two questions from the client: does this identity need a brand mark, and if not, what is the avatar and the favicon? Also: how does the wordmark look stacked. No initials anywhere on this sheet.</p>")
    # stacked wordmark
    h.append("<h2>the stacked wordmark</h2><p class='in'>As built: generation over maine, left aligned, one weight. Shown at 320, 160 and 72 px wide, in Bark on Paper, in Paper on Bark, and in Bark on Sky.</p>")
    h.append('<div class="stack">')
    for pane, name in (("light", "wordmark-stacked"), ("dark", "wordmark-stacked-reversed"), ("sky", "wordmark-stacked")):
        h.append('<div class="pane %s">' % pane)
        for w in (320, 160, 72):
            h.append('<div>%s<div class="lab">%d px wide</div></div>' % (file_img(name, w), w))
        h.append('</div>')
    h.append('<div class="pane light"><div>%s<div class="lab">one line, 320 px, for comparison</div></div><div>%s<div class="lab">stacked centered lockup, as built, with the lined state</div></div><div>%s<div class="lab">two-line lockup, as built</div></div></div>' % (file_img("wordmark", 320), file_img("lockup-stacked-centered", 220), file_img("lockup-two-line", 300)))
    h.append('</div>')
    # avatars
    h.append("<h2>avatar and favicon without a mark, without initials, round two</h2><p class='in'>The quotation mark is out. Each option at 110, 40 and 16 px, which is the profile, the comment thread, and the browser tab. Bark on Sky, then Sky on Bark.</p>")
    for fg, bg, cls in ((BK, SK, ""), (SK, BK, "")):
        h.append('<div class="row">')
        for name, note, fn in options():
            s = fn(fg, bg)
            h.append('<div class="card %s"><h3>%s</h3><p>%s</p><div class="sizes">%s</div></div>' % (cls, name, note, "".join('<div>%s%d</div>' % (img(s, px), px) for px in (110, 40, 16))))
        h.append('</div>')
    # in context: a browser tab and a social bar
    h.append("<h2>in place</h2><p class='in'>207 and me where they would live: a browser tab, and a profile row beside the handle.</p>")
    q = options()[0][2](BK, SK); m = options()[2][2](BK, SK)
    h.append('<div class="row"><div class="chrome">%s generation maine</div><div class="chrome">%s generation maine</div></div>' % (img(q, 16), img(m, 16)))
    h.append('<div class="row" style="margin-top:18px"><div class="bar">%s<span>@generationmaine</span></div><div class="bar">%s<span>@generationmaine</span></div></div>' % (img(q, 44), img(m, 44)))
    # fonts
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf")):
        p = os.path.join(ROOT, "brand", "fonts", fn)
        if os.path.exists(p):
            fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, p)
    h.append("<style>%s</style>" % fonts)
    out = os.path.join(OUT, "wordmark-only-2.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "wordmark-only-2.png"), "1500", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
