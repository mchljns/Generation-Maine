"""Family B, one frame drawn by one set of rules. The horizontal lockup and the framed stacked lockup were drawn separately:
stroke 16 against stroke 9, a square sitting 11 units below the baseline against a 1.28:1 rectangle. This rebuilds both,
and the avatar, from the same rules.

  rules: the frame is open at the bottom left; the left leg stops at 62 percent of the height and the bottom returns from
  42 percent of the width. The stroke is a quarter of the x-height of the type it sits with. Beside one line of type the
  frame runs from the ascender to the baseline. Around two lines of type the frame keeps one pad, a stroke and a half,
  on each side. The frame and the word maine take the accent; generation takes the text color. The gap between frame
  and type is twice the stroke.

  python3 brand/src/build_b_consistent.py          # writes consistent.html/png and the candidate SVGs
  python3 brand/src/build_b_consistent.py apply    # also overwrites lockup-compact*, lockup-two-line*, lockup-framed*, avatar-square*
"""
import base64, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_horizontal_b import one_line, svg
from build_family_marks import b_paths

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family-b")
NAVY, BLUE, MG, PAPER, BLACK, WHITE = "#112337", "#006CB5", "#EFB443", "#F4F3EE", "#000000", "#FFFFFF"
ASC, BASE, XTOP = 6.0, 78.0, 25.0          # measured from the glyph boxes of the one line wordmark
XH = BASE - XTOP                            # 53
STROKE = round(XH * 0.25)                   # 13
LEG, RET = 0.62, 0.42                       # the opening


def frame(x, y, W, H, st, col):
    s = st / 2
    # the long leg runs through the bottom right corner to the outer edge, so the two paths meet without a notch
    return ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (x + s, y + H * LEG, x + s, y + s, x + W - s, y + s, x + W - s, y + H, col, st)
            + '<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (x + W * RET, y + H - s, x + W - s, y + H - s, col, st))


def horizontal(fg, acc, ratio=1.0, st=STROKE):
    """One line of type with the frame beside it. The frame runs from the ascender to the baseline."""
    b, w, h, mx = one_line(fg, acc)
    H = BASE - ASC; W = H * ratio; gap = st * 2
    return svg(W + gap + w, h + 4, frame(0, ASC, W, H, st, acc) + '<g transform="translate(%s 0)">%s</g>' % (W + gap, b))


def stacked(fg, acc, square=False, low=False, st=STROKE):
    """Two lines of type inside the frame."""
    body, w, h = b_paths(fg, acc)
    pad = st * 1.5 + st          # a stroke and a half of air past the stroke itself
    W = w + pad * 2
    H = W if square else max(h + pad * 2, W * 0.78)
    oy = (H - h - pad) if low else (H - h) / 2
    return svg(W, H, frame(0, 0, W, H, st, acc) + '<g transform="translate(%s %s)">%s</g>' % (pad, oy, body))


def avatar(bg, acc, ratio=1.0):
    """The frame alone on a disc, at the stroke to side ratio of the horizontal device."""
    H = 116; W = H * ratio; st = STROKE / (BASE - ASC) * H
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="Generation Maine"><circle cx="120" cy="120" r="120" fill="%s"/>%s</svg>' % (bg, frame((240 - W) / 2, (240 - H) / 2, W, H, st, acc))


def img(s, h=None, w=None):
    st = ("height:%dpx;" % h if h else "") + ("width:%dpx;" % w if w else "")
    return '<img src="data:image/svg+xml;base64,%s" style="%sdisplay:block">' % (base64.b64encode(s.encode()).decode(), st)


def build(apply=False):
    from build_family_marks import b_framed
    from build_horizontal_b import v3
    fonts = "@font-face{font-family:'Hedvig Letters Serif';src:url(file://%s)}@font-face{font-family:'Hedvig Letters Sans';src:url(file://%s)}" % (os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSerif-24.ttf"), os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSans-Regular.ttf"))
    css = """body{margin:0;background:#E9E5DA;color:#112337;font:15px/1.5 'Hedvig Letters Sans',system-ui;padding:48px 56px}
    h1{font:400 34px/1.05 'Hedvig Letters Serif';margin:0 0 8px}h2{font:400 22px/1.1 'Hedvig Letters Serif';margin:34px 0 10px}p.in{max-width:84ch;color:#4B5A68;margin:0 0 22px}
    .row{display:grid;grid-template-columns:250px 1fr 1fr;gap:18px;align-items:center;margin-bottom:14px}.lab b{display:block;margin-bottom:3px;font-family:'Hedvig Letters Serif';font-size:17px;font-weight:400}.lab p{margin:0;font-size:12.5px;color:#4B5A68}
    .bar{background:#112337;height:68px;display:flex;align-items:center;padding:0 24px;gap:40px}.bar span{color:#F4F3EE;font:600 11px/1 system-ui;letter-spacing:.12em;text-transform:uppercase;opacity:.9}
    .big{background:#112337;padding:26px;display:flex;align-items:center;gap:30px}.big .pa{background:#F4F3EE;padding:16px;display:flex;align-items:center}
    .pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}.cell{background:#112337;padding:28px;display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap}.cell .pa{background:#F4F3EE;padding:14px}
    .av{display:flex;gap:14px;align-items:center}
    """
    h = ['<!doctype html><meta charset="utf-8"><title>family b, one frame</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>Family B, one frame drawn by one set of rules</h1><p class='in'>Top rows: how the two lockups are drawn now. The horizontal square is stroke 16 and sits 11 units below the baseline. The stacked frame is stroke 9, nearly half the weight, and a 1.28 to 1 rectangle. Below: both rebuilt from one rule. The stroke is a quarter of the x-height in both. Beside one line the frame runs from the ascender to the baseline. The opening is the same in every drawing. The gap is twice the stroke.</p>")

    def row(name, note, dark, light, bar_h=None):
        return "<div class='row'><div class='lab'><b>%s</b><p>%s</p></div><div class='bar'>%s<span>about · creators · follow</span></div><div class='big'>%s<div class='pa'>%s</div></div></div>" % (name, note, img(dark, bar_h or 44), img(dark, 96), img(light, 64))

    h.append("<h2>Now</h2>")
    h.append(row("horizontal, as built", "stroke 16, square 70, bottom 11 below the baseline", v3(PAPER, MG), v3(NAVY, BLUE)))
    h.append(row("framed stacked, as built", "stroke 9, pad 40, 1.28 to 1", b_framed(PAPER, MG), b_framed(NAVY, BLUE), 68))

    h.append("<h2>One rule</h2>")
    h.append(row("horizontal, square device", "stroke 13, ascender to baseline, gap 26", horizontal(PAPER, MG), horizontal(NAVY, BLUE)))
    h.append(row("stacked, same stroke, same pad", "stroke 13, pad 32, proportion kept at 1.28 to 1", stacked(PAPER, MG), stacked(NAVY, BLUE), 68))
    h.append(row("stacked, square frame, name centered", "the frame is the same square as the device, the name sits in the middle", stacked(PAPER, MG, square=True), stacked(NAVY, BLUE, square=True), 68))
    h.append(row("stacked, square frame, name low", "the same square, the name set at the foot where the frame opens", stacked(PAPER, MG, square=True, low=True), stacked(NAVY, BLUE, square=True, low=True), 68))
    h.append(row("horizontal, device at the frame's proportion", "if the stacked frame stays 1.28 to 1, the device beside the one line name can match it", horizontal(PAPER, MG, ratio=1.28), horizontal(NAVY, BLUE, ratio=1.28)))

    h.append("<h2>The pair, side by side at the sizes they live at</h2>")
    for title, hz, stk, av in (("square device, stacked kept at 1.28 to 1", horizontal(PAPER, MG), stacked(PAPER, MG), avatar(NAVY, MG)),
                                ("square device, square frame, name low", horizontal(PAPER, MG), stacked(PAPER, MG, square=True, low=True), avatar(NAVY, MG)),
                                ("device and frame both 1.28 to 1", horizontal(PAPER, MG, ratio=1.28), stacked(PAPER, MG), avatar(NAVY, MG, ratio=1.28))):
        h.append("<div class='row' style='grid-template-columns:250px 1fr'><div class='lab'><b>%s</b></div><div class='cell'>%s%s<div class='av'>%s%s%s</div></div></div>" % (title, img(hz, 44), img(stk, 150), img(av, 72), img(av, 40), img(av, 16)))

    out = os.path.join(OUT, "consistent.html"); write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "consistent.png"), "1600", "1.4"], check=True)
    print("wrote", out)
    if apply:
        for suf, fg, acc in (("", NAVY, BLUE), ("-reversed", PAPER, MG), ("-black", BLACK, BLACK), ("-white", WHITE, WHITE)):
            write(os.path.join(OUT, "lockup-compact%s.svg" % suf), horizontal(fg, acc))
            write(os.path.join(OUT, "lockup-two-line%s.svg" % suf), stacked(fg, acc))
            write(os.path.join(OUT, "lockup-framed%s.svg" % suf), stacked(fg, acc))
        write(os.path.join(OUT, "avatar-square.svg"), avatar(NAVY, MG)); write(os.path.join(OUT, "avatar-square-marigold.svg"), avatar(MG, NAVY))
        print("applied")


if __name__ == "__main__":
    build(apply="apply" in sys.argv)
