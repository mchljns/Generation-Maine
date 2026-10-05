"""Adjusting the two brand marks to live with the Maine Policy family. The parent marks are stripes or type, in two colors,
geometric and bold. Family A (Signature): the lined state recolored, then the lined state cut on the parent's slant, then a
bold uppercase lockup with the second word in the accent, the way The Maine Wire sets its name. Family B (Bark & Sky): the
stacked wordmark inside an open frame, the way Maine Civic Action sets its name; the second word in the accent; a single
accent bar beside the wordmark.

  python3 brand/src/build_family_marks.py   # writes brand/identity/logo-maine/family/*.svg, marks.html and marks.png
"""
import base64
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write
import maine2
from build_logo_maine import maine_lines, simplified

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family")
LOGO_B = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
NAVY, BLUE, MG, PAPER, NAVY_B, BLUE_B = "#0F2E4D", "#0556A5", "#EFB443", "#F4F3EE", "#112337", "#006CB5"
BRIC = Face("BricolageGrotesque-ExtraBold.ttf")


def svg(w, h, body, label="Generation Maine"):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s</svg>' % (w, h, w, h, label, body)


# ---- Family A: the state ----
def state_lined(h, fg, accent, x=0, y=0):
    body, w = maine_lines(x, y, h, fg, accent, cut="full", gold=True)
    return body, w


def state_slanted(h, fg, accent, x=0, y=0, angle=62, n=7, idn="st"):
    """The state as a clip, filled with stripes on the parent's slant. One stripe in the accent, the widest, like the lined state's gold line."""
    ring = simplified(maine2.fit(x, y, h * maine2.ASPECT, h), h * 0.012)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    w = maxx - minx
    import math
    pitch = (w * 1.4) / n
    sw = pitch * 0.56
    stripes = ""
    # stripes are vertical bars rotated about the state's centre; the longest after clipping gets the accent, which for Maine is the one through the middle
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    L = h * 2
    for i in range(n):
        off = (i - (n - 1) / 2) * pitch
        col = accent if i == n // 2 else fg
        stripes += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (cx + off - sw / 2, cy - L / 2, sw, L, col)
    return ('<defs><clipPath id="%s"><path d="%s"/></clipPath></defs><g clip-path="url(#%s)"><g transform="rotate(%s %s %s)">%s</g></g>'
            % (idn, maine2.path(ring), idn, 90 - angle, cx, cy, stripes)), w


def word(text, size, fill, x, y, face=BRIC):
    d, w = face.path(text, size, x, y)
    return '<path fill="%s" d="%s"/>' % (fill, d), w


def a_lockup(fg, accent, slanted=True, upper=True):
    h = 100
    mark, mw = (state_slanted(h, fg, accent, idn="lk") if slanted else state_lined(h, fg, accent))
    size = 64 if upper else 70
    t1, w1 = word("GENERATION " if upper else "Generation ", size, fg, mw + 26, h * 0.80)
    t2, w2 = word("MAINE" if upper else "Maine", size, accent, mw + 26 + w1, h * 0.80)
    return svg(mw + 26 + w1 + w2 + 4, h, mark + t1 + t2)


# ---- Family B: the wordmark ----
def b_paths(fg1, fg2):
    s = open(os.path.join(LOGO_B, "wordmark-stacked.svg")).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    paths = re.findall(r'<path[^>]*d="([^"]+)"', s)
    body = '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg1, paths[0], fg2, paths[1])
    return body, float(vb.group(1)), float(vb.group(2))


def b_framed(fg, accent, pad=46, stroke=7):
    """The stacked wordmark inside an open square, open at the bottom left, the way Civic Action frames its name."""
    body, w, h = b_paths(fg, accent)
    W = w + pad * 2
    H = max(h + pad * 2, W * 0.78)
    oy = (H - h) / 2
    frame = ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>'
             % (stroke / 2, H * 0.62, stroke / 2, stroke / 2, W - stroke / 2, stroke / 2, W - stroke / 2, H - stroke / 2, accent, stroke)
             + '<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (W * 0.42, H - stroke / 2, W - stroke / 2, H - stroke / 2, accent, stroke))
    return svg(W, H, frame + '<g transform="translate(%s %s)">%s</g>' % (pad, oy, body))


def b_two_tone(fg, accent):
    body, w, h = b_paths(fg, accent)
    return svg(w, h, body)


def b_bar(fg, accent):
    body, w, h = b_paths(fg, fg)
    bar = 18
    return svg(w + bar + 28, h, '<rect x="0" y="%s" width="%s" height="%s" fill="%s"/>' % (h * 0.06, bar, h * 0.9, accent) + '<g transform="translate(%s 0)">%s</g>' % (bar + 28, body))


def disc(body_fn, bg, size=240):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><circle cx="%d" cy="%d" r="%d" fill="%s"/>%s</svg>' % (size, size, size / 2, size / 2, size / 2, bg, body_fn())


def img(s, px=None, h=None, cls=""):
    st = ("width:%dpx;" % px if px else "") + ("height:%dpx;" % h if h else "")
    return '<img class="%s" src="data:image/svg+xml;base64,%s" style="%sdisplay:block">' % (cls, base64.b64encode(s.encode()).decode(), st)


def build():
    os.makedirs(OUT, exist_ok=True)
    files = {}
    # A marks
    for suf, fg, bg, acc in (("", NAVY, PAPER, MG), ("-reversed", PAPER, NAVY, MG), ("-blue", NAVY, BLUE, MG)):
        b1, w1 = state_lined(240, fg, acc)
        files["a-lined" + suf] = svg(w1, 240, b1)
        b2, w2 = state_slanted(240, fg, acc, idn="s" + suf.strip("-") or "s0")
        files["a-slanted" + suf] = svg(w2, 240, b2)
        files["a-lockup-upper" + suf] = a_lockup(fg, acc, True, True)
        files["a-lockup-title" + suf] = a_lockup(fg, acc, True, False)
        files["a-lockup-lined-upper" + suf] = a_lockup(fg, acc, False, True)
    # B marks
    for suf, fg, bg, acc in (("", NAVY_B, PAPER, MG), ("-reversed", PAPER, NAVY_B, MG)):
        files["b-framed" + suf] = b_framed(fg, acc)
        files["b-two-tone" + suf] = b_two_tone(fg, acc)
        files["b-bar" + suf] = b_bar(fg, acc)
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)

    # avatars
    def av_a(fg, bg, acc):
        b, w = state_slanted(150, fg, acc, x=(240 - 150 * maine2.ASPECT) / 2, y=45, idn="av" + fg.strip("#"))
        return disc(lambda: b, bg)
    def av_b(fg, bg, acc):
        body, w, h = b_paths(fg, acc)
        s = 170 / w
        return disc(lambda: '<g transform="translate(%s %s) scale(%s)">%s</g>' % ((240 - w * s) / 2, (240 - h * s) / 2, s, body), bg)
    def av_bar(fg, bg, acc):
        return disc(lambda: '<rect x="104" y="52" width="32" height="136" fill="%s"/>' % acc, bg)

    css = """body{margin:0;background:#E9E5DA;color:#0F2E4D;font:15px/1.5 'DM Sans',system-ui;padding:48px 56px}
    h1{font:800 34px/1.05 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 8px}h2{font:800 22px/1.1 'Bricolage Grotesque';letter-spacing:-.01em;margin:40px 0 10px}p.in{max-width:80ch;color:#4B5A68;margin:0 0 18px}
    .row{display:grid;grid-template-columns:260px 1fr 1fr;gap:18px;align-items:center;margin-bottom:16px}.lab b{display:block;font-weight:700;margin-bottom:4px}.lab p{margin:0;font-size:12.5px;color:#4B5A68}
    .t{border-radius:12px;padding:28px;display:flex;align-items:center;justify-content:center;min-height:150px}.t.pa{background:#F4F3EE}.t.nv{background:#0F2E4D}.t.nb{background:#112337}.t.bl{background:#0556A5}
    .sz{display:flex;gap:16px;align-items:flex-end}.sz div{text-align:center;font:11px 'IBM Plex Mono',monospace;color:#4B5A68}.sz img{border-radius:50%;margin:0 auto 4px}
    """
    fonts = ""
    for fam, fn, wt in (("Bricolage Grotesque", "BricolageGrotesque-ExtraBold.ttf", "800"), ("IBM Plex Mono", "alt/IBMPlexMono-Medium.ttf", "500")):
        fonts += "@font-face{font-family:'%s';font-weight:%s;src:url(file://%s)}" % (fam, wt, os.path.join(ROOT, "brand", "fonts", fn))
    fonts += "@font-face{font-family:'DM Sans';font-weight:100 900;src:url(file://%s)}" % os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf")
    h = ['<!doctype html><meta charset="utf-8"><title>family marks</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>The marks, adjusted for the family</h1><p class='in'>The parent marks are stripes or type, two colors, geometric and bold: Maine Policy's slanted stripes, The Maine Wire's two-color name, Civic Action's framed stacked name. Each adjustment below keeps the concept's own mark and borrows one of those moves. Left on Paper, right on the family navy.</p>")
    h.append("<h2>Family A: Signature's lined state</h2>")
    rows = [
        ("Recolored", "The lined state as it is, in navy with the one marigold line. The smallest possible change; already reads as a sibling because the parent's mark is also stripes with one accent.", "a-lined"),
        ("Cut on the parent's slant", "The same state, but the lines run at Maine Policy's angle. Seven stripes, the middle one marigold. Rhymes with the parent mark directly while staying the state.", "a-slanted"),
        ("Uppercase lockup, second word in the accent", "The slanted state beside GENERATION MAINE in Bricolage 800, MAINE in marigold, the way The Maine Wire sets its name. The loudest option and the closest to the family.", "a-lockup-upper"),
        ("Title case lockup", "The same with the name in title case, which keeps more of Signature's voice.", "a-lockup-title"),
        ("Lined state, uppercase lockup", "The original horizontal lines with the uppercase two-color name. A middle path.", "a-lockup-lined-upper"),
    ]
    for title, note, key in rows:
        h.append("<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='t pa'>%s</div><div class='t nv'>%s</div></div>" % (title, note, img(files[key], None, 110 if "lockup" not in key else 64), img(files[key + "-reversed"], None, 110 if "lockup" not in key else 64)))
    h.append("<div class='row'><div class='lab'><b>Avatar, slanted state</b><p>At 110, 40 and 16, on Paper and on navy.</p></div><div class='t pa'><div class='sz'>%s%s%s</div></div><div class='t nv'><div class='sz'>%s%s%s</div></div></div>" % (
        img(av_a(NAVY, "#FFFFFF", MG), 110), img(av_a(NAVY, "#FFFFFF", MG), 40), img(av_a(NAVY, "#FFFFFF", MG), 16), img(av_a(PAPER, NAVY, MG), 110), img(av_a(PAPER, NAVY, MG), 40), img(av_a(PAPER, NAVY, MG), 16)))
    h.append("<h2>Family B: Bark &amp; Sky's wordmark</h2>")
    rows = [
        ("Framed, open at the corner", "The stacked lowercase wordmark inside an open square in marigold, generation in navy, maine in marigold. The same device Maine Civic Action uses, in this concept's serif.", "b-framed"),
        ("Two tone", "The stacked wordmark alone, maine in marigold. Quiet, and still a family move: the second word in the accent.", "b-two-tone"),
        ("The bar", "A single marigold bar beside the wordmark. A blaze on bark, and the thing that can stand alone as a favicon.", "b-bar"),
    ]
    for title, note, key in rows:
        h.append("<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='t pa'>%s</div><div class='t nb'>%s</div></div>" % (title, note, img(files[key], None, 96), img(files[key + "-reversed"], None, 96)))
    h.append("<div class='row'><div class='lab'><b>Avatar</b><p>The two tone wordmark at 110 and 40, which is where it stops reading, and the bar at 110, 40 and 16, which is what carries the small sizes.</p></div><div class='t pa'><div class='sz'>%s%s%s%s%s</div></div><div class='t nb'><div class='sz'>%s%s%s%s%s</div></div></div>" % (
        img(av_b(NAVY_B, "#FFFFFF", MG), 110), img(av_b(NAVY_B, "#FFFFFF", MG), 40), img(av_bar(NAVY_B, "#FFFFFF", MG), 110), img(av_bar(NAVY_B, "#FFFFFF", MG), 40), img(av_bar(NAVY_B, "#FFFFFF", MG), 16),
        img(av_b(PAPER, NAVY_B, MG), 110), img(av_b(PAPER, NAVY_B, MG), 40), img(av_bar(PAPER, NAVY_B, MG), 110), img(av_bar(PAPER, NAVY_B, MG), 40), img(av_bar(PAPER, NAVY_B, MG), 16)))
    out = os.path.join(OUT, "marks.html")
    write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "marks.png"), "1500", "1.4"], check=True)
    print("wrote", len(files), "files,", out)


if __name__ == "__main__":
    build()
