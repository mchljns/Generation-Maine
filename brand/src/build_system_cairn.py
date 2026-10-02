"""The Bark & Sky system around the cairn (wedges ii): the mark, lockups in every arrangement and colorway, avatar, favicon,
app icon and bug, and a sheet to judge them together.

  python3 brand/src/build_system_cairn.py   # writes brand/identity/logo-maine/bark-sky-cairn/*.svg and lockups.html/.png
"""
import base64
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write
from build_cairn5 import round_stone

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky-cairn")
SRC = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
BK, SK, PA, CL = "#26201C", "#B9C9D3", "#F4F3EE", "#5B544C"
SANS = Face("d/HedvigLettersSans-Regular.ttf")
MPI = "an initiative of Maine Policy Institute"  # [CONFIRM: funder line]

# ---- the mark: wedges ii, final pass. The wide flat narrowed so it no longer reads as a brim. Ground at y = 206, 240 square. ----
FLATS = [
    [(40, 206), (44, 188), (90, 185), (140, 186), (196, 180), (202, 206)],   # base: long, thick at the right
    [(70, 185), (66, 162), (108, 156), (150, 162), (152, 182)],              # second: thick at the left, set left
    [(64, 161), (68, 148), (120, 142), (170, 150), (172, 160)],              # third: a little wider than the second
    [(96, 148), (94, 122), (116, 114), (142, 120), (146, 146)],             # fourth: a block with a dip
]
ROUND = (121, 96, 26, 20, -6)
# the mark's ink bounds, for fitting: x 40..202, y 76..206
MX0, MX1, MY0, MY1 = 40, 202, 74, 206
MW, MH = MX1 - MX0, MY1 - MY0


def stone(pts, fg, bg):
    d = "M" + " L".join("%s %s" % p for p in pts) + " Z"
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="9" stroke-linejoin="round"/>' % (d, bg)
            + '<path d="%s" fill="%s" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (d, fg, fg))


def mark(fg, bg, top=None, x=0, y=0, h=MH):
    """The cairn with its base line at y + h, left edge at x, height h. bg is the field it sits on, for the shadow lines."""
    s = h / MH
    cx, cy, rx, ry, tilt = ROUND
    body = "".join(stone(p, fg, bg) for p in FLATS) + round_stone(cx, cy, rx + 3, ry + 3, bg, tilt) + round_stone(cx, cy, rx, ry, top or fg, tilt)
    return '<g transform="translate(%s %s) scale(%s) translate(%s %s)">%s</g>' % (x, y, s, -MX0, -MY0, body)


def wordmark(kind, fg):
    """The one line or stacked wordmark path, recolored. Returns (body, w, h)."""
    s = open(os.path.join(SRC, "wordmark.svg" if kind == "one" else "wordmark-stacked.svg")).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    paths = re.findall(r'<path[^>]*d="([^"]+)"', s)
    return "".join('<path fill="%s" d="%s"/>' % (fg, d) for d in paths), float(vb.group(1)), float(vb.group(2))


def text(t, size, fg, x, y):
    d, w = SANS.path(t, size, x, y)
    return '<path fill="%s" d="%s"/>' % (fg, d), w


def svg(w, h, body, label, bg=None):
    rect = '<rect width="%s" height="%s" fill="%s"/>' % (w, h, bg) if bg else ""
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s%s</svg>' % (w, h, w, h, label, rect, body)


COLORWAYS = {
    "": (BK, PA, SK),          # Bark on Paper, round stone Sky
    "-reversed": (SK, BK, PA),  # Sky on Bark, round stone Paper
    "-black": ("#000000", "#FFFFFF", "#000000"),
    "-white": ("#FFFFFF", "#000000", "#FFFFFF"),
}


def build():
    os.makedirs(OUT, exist_ok=True)
    files = {}
    for suf, (fg, bg, top) in COLORWAYS.items():
        # the mark alone
        files["mark" + suf] = svg(MW, MH, mark(fg, bg, top), "Generation Maine")
        one, ow, oh = wordmark("one", fg)
        stk, sw, sh = wordmark("stacked", fg)
        # horizontal: mark the height of the one line wordmark plus a little, baseline aligned with the x height band
        mh = 118; gap = 30
        files["lockup-horizontal" + suf] = svg(mh * MW / MH + gap + ow, mh, mark(fg, bg, top, 0, 0, mh) + '<g transform="translate(%s %s)">%s</g>' % (mh * MW / MH + gap, mh - oh - 4, one), "Generation Maine")
        # horizontal large: a bigger mark, for title cards
        mh2 = 170
        files["lockup-horizontal-large" + suf] = svg(mh2 * MW / MH + 40 + ow, mh2, mark(fg, bg, top, 0, 0, mh2) + '<g transform="translate(%s %s)">%s</g>' % (mh2 * MW / MH + 40, mh2 - oh - 10, one), "Generation Maine")
        # two line: mark beside the stacked wordmark, the mark the height of both lines
        files["lockup-two-line" + suf] = svg(sh * MW / MH + 34 + sw, sh, mark(fg, bg, top, 0, 0, sh) + '<g transform="translate(%s 0)">%s</g>' % (sh * MW / MH + 34, stk), "Generation Maine")
        # stacked left: mark over the stacked wordmark, left aligned
        mh3 = 150
        files["lockup-stacked" + suf] = svg(max(sw, mh3 * MW / MH), mh3 + 36 + sh, mark(fg, bg, top, 0, 0, mh3) + '<g transform="translate(0 %s)">%s</g>' % (mh3 + 36, stk), "Generation Maine")
        # stacked centered: mark centered over the one line wordmark
        mh4 = 160
        files["lockup-stacked-centered" + suf] = svg(ow, mh4 + 40 + oh, mark(fg, bg, top, (ow - mh4 * MW / MH) / 2, 0, mh4) + '<g transform="translate(0 %s)">%s</g>' % (mh4 + 40, one), "Generation Maine")
        # endorsed: stacked centered with the funder line under it
        t, tw = text(MPI, 30, CL if suf == "" else fg, 0, 0)
        t, tw = text(MPI, 30, CL if suf == "" else fg, (ow - tw) / 2, mh4 + 40 + oh + 54)
        files["lockup-endorsed" + suf] = svg(ow, mh4 + 40 + oh + 66, mark(fg, bg, top, (ow - mh4 * MW / MH) / 2, 0, mh4) + '<g transform="translate(0 %s)">%s</g>' % (mh4 + 40, one) + t, "Generation Maine, " + MPI)
        # compact: the mark at the height of the stacked wordmark's first line, for the bar
        files["lockup-compact" + suf] = svg(sh * 0.55 * MW / MH + 20 + sw * 0.55, sh * 0.55, mark(fg, bg, top, 0, 0, sh * 0.55) + '<g transform="translate(%s 0) scale(.55)">%s</g>' % (sh * 0.55 * MW / MH + 20, stk), "Generation Maine")
    # avatar, favicon, app icon, bug
    for suf, (field, ink, top) in {"": (SK, BK, BK), "-reversed": (BK, SK, PA), "-sky-top": (SK, BK, PA)}.items():
        m = mark(ink, field, top, 120 - MW * 0.68 / 2, 120 - MH * 0.68 / 2 + 2, MH * 0.68)
        files["avatar" + suf] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % field + m, "Generation Maine")
        files["app-icon" + suf] = svg(240, 240, '<rect width="240" height="240" rx="54" fill="%s"/>' % field + m, "Generation Maine")
    # favicon: the silhouette only, no shadow lines, so it stays solid at 16 px
    sil = "".join('<path d="M%s Z" fill="%s"/>' % (" L".join("%s %s" % p for p in pts), BK) for pts in FLATS) + round_stone(*ROUND[:4], BK, ROUND[4])
    files["favicon"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/><g transform="translate(%s %s) scale(.72) translate(%s %s)">%s</g>' % (SK, 120 - MW * 0.72 / 2, 120 - MH * 0.72 / 2 + 2, -MX0, -MY0, sil), "Generation Maine")
    files["bug"] = svg(MW, MH, mark(BK, PA, SK), "Generation Maine")
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)

    # ---- the sheet ----
    def im(k, w=None, h=None):
        s = files[k]
        style = ("width:%spx;" % w if w else "") + ("height:%spx;" % h if h else "")
        return '<img src="data:image/svg+xml;base64,%s" style="%sdisplay:block">' % (base64.b64encode(s.encode()).decode(), style)
    css = """body{margin:0;background:#E9E5DA;color:#26201C;font:15px/1.5 'Hedvig Letters Sans',system-ui;padding:48px 56px}
    h1{font:400 38px/1.05 'Hedvig Letters Serif';margin:0 0 8px}h2{font:400 24px/1.1 'Hedvig Letters Serif';margin:44px 0 12px}p.in{max-width:76ch;color:#5B544C;margin:0 0 20px}
    .g{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.g3{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
    .t{border-radius:14px;padding:34px;display:flex;align-items:center;justify-content:center;min-height:150px}.t.pa{background:#F4F3EE}.t.bk{background:#26201C}.t.wh{background:#fff}.t.bl{background:#000}
    .lab{font:11px 'IBM Plex Mono',monospace;color:#5B544C;margin:8px 0 0 4px}
    .bar{display:flex;align-items:center;justify-content:space-between;background:#F4F3EE;border-radius:999px;padding:12px 22px 12px 16px;gap:20px}.bar span{font-size:13px;color:#5B544C}
    .row{display:flex;gap:18px;align-items:flex-end}.row > div{text-align:center}
    """
    fonts = ""
    for fam, fn in (("Hedvig Letters Serif", "d/HedvigLettersSerif-24.ttf"), ("Hedvig Letters Sans", "d/HedvigLettersSans-Regular.ttf"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf")):
        fonts += "@font-face{font-family:'%s';src:url(file://%s)}" % (fam, os.path.join(ROOT, "brand", "fonts", fn))
    h = ['<!doctype html><meta charset="utf-8"><title>cairn system</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>the system, around the cairn</h1><p class='in'>Wedges ii as the mark, the wide flat narrowed. Lockups in every arrangement, in Bark on Paper with the round stone in Sky, and in Sky on Bark with the round stone in Paper. Then the avatar, app icon, favicon, and the mark at working sizes.</p>")
    for name, k in (("horizontal", "lockup-horizontal"), ("horizontal, large", "lockup-horizontal-large"), ("two line", "lockup-two-line"), ("stacked, left", "lockup-stacked"), ("stacked, centered", "lockup-stacked-centered"), ("endorsed", "lockup-endorsed"), ("compact, for the bar", "lockup-compact")):
        wpx = 520 if "large" in k or "horizontal" in k or "endorsed" in k or "centered" in k else 300
        h.append("<h2>%s</h2><div class='g'><div><div class='t pa'>%s</div><div class='lab'>%s.svg</div></div><div><div class='t bk'>%s</div><div class='lab'>%s-reversed.svg</div></div></div>" % (name, im(k, wpx), k, im(k + "-reversed", wpx), k))
    h.append("<h2>one color</h2><div class='g'><div class='t wh'>%s</div><div class='t bl'>%s</div></div>" % (im("lockup-horizontal-black", 520), im("lockup-horizontal-white", 520)))
    h.append("<h2>avatar, app icon, favicon</h2><div class='row'>" + "".join("<div>%s<div class='lab'>%s</div></div>" % (im(k, px), "%s %d" % (k, px)) for k, px in (("avatar", 110), ("avatar", 40), ("avatar-reversed", 110), ("avatar-reversed", 40), ("avatar-sky-top", 110), ("app-icon", 110), ("app-icon-reversed", 110), ("favicon", 32), ("favicon", 16))) + "</div>")
    h.append("<h2>in the bar</h2><div class='bar'>%s<span>about &nbsp; creators &nbsp; in their words &nbsp; follow</span><span>get the newsletter</span></div>" % im("lockup-compact", None, 30))
    out = os.path.join(OUT, "lockups.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "lockups.png"), "1400", "1.4"], check=True)
    print("wrote", len(files), "files and", out)


if __name__ == "__main__":
    build()
