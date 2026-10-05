"""Family B, the horizontal lockup. The framed stacked wordmark loses its frame at bar size. Six horizontal arrangements of
the one line name and the open square, each at bar height (48 px), at 120 px, and the mark alone at 40 and 16.
  python3 brand/src/build_horizontal_b.py
"""
import base64, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family-b")
LOGO_BS = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
NAVY, BLUE, MG, PAPER = "#112337", "#006CB5", "#EFB443", "#F4F3EE"


def one_line(fg1, fg2):
    """The one line wordmark; the two words recolored separately. Returns (body, w, h)."""
    s = open(os.path.join(LOGO_BS, "wordmark.svg")).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s); d = re.findall(r'<path[^>]*d="([^"]+)"', s)[0]
    # split the single path at the gap between the words: subpaths whose min x is past the gap belong to maine
    subs = re.findall(r'M[^M]+', d)
    xs = [min(float(v) for v in re.findall(r'(-?\d+\.?\d*) -?\d+\.?\d*', sp)) for sp in subs]
    gap_i = max(range(1, len(subs)), key=lambda i: xs[i] - max(xs[:i]))  # the biggest jump in x starts the second word
    gen = "".join(subs[:gap_i]); maine = "".join(subs[gap_i:])
    mx = min(xs[gap_i:])
    return '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg1, gen, fg2, maine), float(vb.group(1)), float(vb.group(2)), mx


def svg(w, h, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="Generation Maine">%s</svg>' % (w, h, w, h, body)


def open_square(x, y, size, stroke, col, gap=0.42):
    """An open square: the top, right and bottom right drawn, the bottom left open, as in the framed mark."""
    s = stroke / 2
    return ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>'
            % (x + s, y + size * 0.62, x + s, y + s, x + size - s, y + s, x + size - s, y + size - s, col, stroke)
            + '<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (x + size * gap, y + size - s, x + size - s, y + size - s, col, stroke))


def v1(fg, acc):  # the framed stacked mark, for comparison
    from build_family_marks import b_framed
    return b_framed(fg, acc, pad=30, stroke=8)

def v2(fg, acc):  # one line, maine in the accent, no device
    b, w, h, mx = one_line(fg, acc); return svg(w, h, b)

def v3(fg, acc):  # one line with the open square as a mark beside it, square = cap height, heavy stroke
    b, w, h, mx = one_line(fg, acc); S = 86; st = 16; return svg(S + 30 + w, h, open_square(0, (h - S) / 2 + 4, S, st, acc) + '<g transform="translate(%s 0)">%s</g>' % (S + 30, b))

def v4(fg, acc):  # one line, the frame around maine only
    b, w, h, mx = one_line(fg, acc); pad = 18; x0 = mx - pad; W = w - x0 + pad
    return svg(w + pad, h + pad * 2, '<g transform="translate(0 %s)">%s</g>' % (pad, b) + open_square(x0, 0, max(W, h + pad * 2), 7, acc).replace('L%s' % 'X', ''))

def v4b(fg, acc):  # frame around maine as a rectangle (not square), open at the bottom left
    b, w, h, mx = one_line(fg, acc); pad = 20; x0 = mx - pad; x1 = w + pad; y0 = -pad + 10; y1 = h + pad - 6; st = 7; s = st / 2
    fr = ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (x0 + s, y0 + (y1 - y0) * 0.6, x0 + s, y0 + s, x1 - s, y0 + s, x1 - s, y1 - s, acc, st)
          + '<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (x0 + (x1 - x0) * 0.35, y1 - s, x1 - s, y1 - s, acc, st))
    return svg(x1, y1 - y0, '<g transform="translate(0 %s)">%s</g>' % (-y0, b) + '<g transform="translate(0 %s)">%s</g>' % (-y0, fr))

def v5(fg, acc):  # the open square as a heavy bracket at full x-height, with the name one line, no accent on the type
    b, w, h, mx = one_line(fg, fg); S = 100; st = 22; return svg(S + 34 + w, h, open_square(0, (h - S) / 2 + 4, S, st, acc, gap=0.5) + '<g transform="translate(%s 0)">%s</g>' % (S + 34, b))

def v6(fg, acc):  # the whole one line name in a wide open frame
    b, w, h, mx = one_line(fg, acc); pad = 26; st = 8; W = w + pad * 2; H = h + pad * 2 - 10; s = st / 2
    fr = ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (s, H * 0.66, s, s, W - s, s, W - s, H - s, acc, st)
          + '<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (W * 0.28, H - s, W - s, H - s, acc, st))
    return svg(W, H, fr + '<g transform="translate(%s %s)">%s</g>' % (pad, pad - 6, b))


OPTS = [("framed stacked, as in the bar now", v1, "The frame is a hairline at 48 px and the type inside is 11 px. The device is lost exactly where it is needed."),
        ("one line, maine in marigold", v2, "No device. The family move is only the second word in the accent. Honest, and nothing to lose at any size."),
        ("one line with the square beside it", v3, "The open square at cap height as a mark, heavy enough to read at 16. The frame becomes a device rather than a container."),
        ("one line, the frame around maine", v4b, "The frame holds only the word that matters. Reads at bar size because the frame is as tall as the type."),
        ("heavy bracket", v5, "The square as a thick bracket at full height, the name in one color. The most graphic, and a real avatar."),
        ("the whole name framed", v6, "One line inside a wide frame. Reads, but it is a badge, and wide badges fight the bar.")]


def img(s, h=None, w=None):
    st = ("height:%dpx;" % h if h else "") + ("width:%dpx;" % w if w else "")
    return '<img src="data:image/svg+xml;base64,%s" style="%sdisplay:block">' % (base64.b64encode(s.encode()).decode(), st)


def disc(body_svg_fn, fg, bg, acc, size=240):
    # mark alone: the open square in the accent on the field
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240"><circle cx="120" cy="120" r="120" fill="%s"/>%s</svg>' % (bg, open_square(62, 62, 116, 22, acc, gap=0.5))


def build():
    css = """body{margin:0;background:#E9E5DA;color:#112337;font:15px/1.5 'Hedvig Letters Sans',system-ui;padding:48px 56px}
    h1{font:400 34px/1.05 'Hedvig Letters Serif';margin:0 0 8px}p.in{max-width:80ch;color:#4B5A68;margin:0 0 22px}
    .row{display:grid;grid-template-columns:270px 1fr 1fr;gap:18px;align-items:center;margin-bottom:14px}.lab b{display:block;font-weight:700;margin-bottom:3px;font-family:'Hedvig Letters Serif';font-size:17px;font-weight:400}.lab p{margin:0;font-size:12.5px;color:#4B5A68}
    .bar{background:#112337;height:76px;display:flex;align-items:center;padding:0 26px;gap:40px;border-radius:10px}.bar span{color:#F4F3EE;font:600 11px/1 system-ui;letter-spacing:.12em;text-transform:uppercase;opacity:.9}
    .big{background:#112337;border-radius:10px;padding:28px;display:flex;align-items:center;gap:36px}.big .pa{background:#F4F3EE;border-radius:8px;padding:18px;display:flex;align-items:center}
    """
    fonts = "@font-face{font-family:'Hedvig Letters Serif';src:url(file://%s)}@font-face{font-family:'Hedvig Letters Sans';src:url(file://%s)}" % (os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSerif-24.ttf"), os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSans-Regular.ttf"))
    h = ['<!doctype html><meta charset="utf-8"><title>horizontal b</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>Family B, the horizontal lockup</h1><p class='in'>Left column: each option in the bar at its real size, 48 px tall on navy beside the navigation. Right: at 120 px on navy and on Paper. The frame has to read in the left column or it is not doing its job.</p>")
    files = {}
    for i, (name, fn, note) in enumerate(OPTS):
        dark = fn(PAPER, MG); light = fn(NAVY, BLUE)
        key = "horizontal-%d" % (i + 1)
        files[key + "-reversed"] = dark; files[key] = light
        h.append("<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='bar'>%s<span>about · creators · follow</span></div><div class='big'>%s<div class='pa'>%s</div></div></div>" % (name, note, img(dark, 48), img(dark, 110), img(light, 72)))
    h.append("<div class='row'><div class='lab'><b>the square alone</b><p>As the avatar and favicon: the open square in marigold on navy, and navy on marigold, at 110, 40 and 16.</p></div><div class='bar' style='gap:16px'>%s%s%s%s%s%s</div><div></div></div>" % (
        img(disc(None, PAPER, NAVY, MG), 110), img(disc(None, PAPER, NAVY, MG), 40), img(disc(None, PAPER, NAVY, MG), 16), img(disc(None, NAVY, MG, NAVY), 110), img(disc(None, NAVY, MG, NAVY), 40), img(disc(None, NAVY, MG, NAVY), 16)))
    files["avatar-square"] = disc(None, PAPER, NAVY, MG); files["avatar-square-marigold"] = disc(None, NAVY, MG, NAVY)
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)
    out = os.path.join(OUT, "horizontal.html"); write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "horizontal.png"), "1600", "1.4"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
