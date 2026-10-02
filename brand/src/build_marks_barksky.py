"""Brand mark candidates that Bark & Sky's voice allows and Signature's did not: quiet, one weight, serif, paper-like.
Each is drawn by hand as SVG and shown in Bark on Paper, in Sky on Bark, as the avatar at 110, 40 and 16 px, and in the horizontal
lockup beside the lowercase wordmark. The lined state from the shared system is the first row, for comparison.

  python3 brand/src/build_marks_barksky.py   # writes brand/identity/marks-bark-sky/*.svg, candidates.html and candidates.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write
from build_v4 import svg, f, rect
import maine2
from build_logo_maine import maine_lines, simplified

OUT = "brand/identity/marks-bark-sky"
BK, SK, PA, MIST, CL = "#2B211C", "#CFE3F0", "#FFFFFF", "#EEF4F8", "#6B5A4E"
SERIF = Face("d/HedvigLettersSerif-24.ttf")
S = 240  # every mark is drawn in a 240 unit square


def glyph_mark(text, fg, size, tracking=0, dy=0):
    """A serif glyph or two, centred in the square by its ink bounds."""
    d, w = SERIF.path(text, size, 0, 0, tracking)
    # centre by the path's bounding box
    import re
    xs, ys = [], []
    for m in re.finditer(r"(-?\d+\.?\d*) (-?\d+\.?\d*)", d):
        xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    d, _ = SERIF.path(text, size, S / 2 - cx, S / 2 - cy + dy, tracking)
    return '<path fill="%s" d="%s"/>' % (fg, d)


def quote(fg):
    return glyph_mark("“", fg, 300, dy=0)


def gm(fg):
    return glyph_mark("gm", fg, 150, tracking=-30, dy=-6)


def ruled(fg, n=13, pad=18):
    """Ruled paper with the state left blank: lines of one weight stop at the state's edge. The inverse of the lined state."""
    h = S - pad * 2
    w_box = h * maine2.ASPECT
    ring = simplified(maine2.fit((S - w_box) / 2, pad, w_box, h), h * 0.006)
    body = ""
    w = 4.6
    for i in range(n):
        y = pad + h * (i + 0.5) / n
        xs = maine2.crossings(ring, y)
        segs = [(pad, S - pad)]
        for a, b in zip(xs[0::2], xs[1::2]):
            new = []
            for s0, s1 in segs:
                if b < s0 or a > s1:
                    new.append((s0, s1))
                else:
                    if a - 10 > s0: new.append((s0, a - 10))
                    if b + 10 < s1: new.append((b + 10, s1))
            segs = new
        for s0, s1 in segs:
            if s1 - s0 > w * 2:
                body += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(s0), f(y), f(s1), f(y), fg, f(w))
    return body


def outline(fg):
    """The state as one hairline, a pen drawing. Allowed here because the whole concept is one thin weight."""
    pad = 20
    h = S - pad * 2
    w_box = h * maine2.ASPECT
    ring = simplified(maine2.fit((S - w_box) / 2, pad, w_box, h), h * 0.009)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="4.5" stroke-linejoin="round"/>' % (maine2.path(ring), fg)


_HID = [0]
def horizon(fg, bg, line):
    """Ground and sky: a disc, Sky above, ground below, a thin line of light between. Abstract, calm, no state."""
    _HID[0] += 1
    cid = "hz%d" % _HID[0]
    y = S * 0.6
    ground = BK if fg == BK else PA
    return ('<defs><clipPath id="%s"><circle cx="%s" cy="%s" r="%s"/></clipPath></defs>'
            '<g clip-path="url(#%s)">%s%s<rect x="0" y="%s" width="%s" height="3" fill="%s"/></g>') % (
        cid, f(S / 2), f(S / 2), f(S / 2), cid, rect(0, 0, S, y, SK), rect(0, y, S, S - y, ground), f(y - 1.5), f(S), line)


def lined(fg):
    body, w = maine_lines(0, 0, S - 24, fg, fg, "full", gold=False)
    return '<g transform="translate(%s 12)">%s</g>' % (f((S - w) / 2), body)


CANDS = [
    ("lined", "The lined state (the shared system)", "Sixteen lines, one for each county. Kept here as the reference the others are judged against.", lambda fg, bg: lined(fg)),
    ("quote", "The opening quote", "The project is young people in their own words. Hedvig's opening quotation mark, nothing else. Literary, immediate, and it says what the brand does rather than where it is.", lambda fg, bg: quote(fg)),
    ("gm", "The gm monogram", "The two initials in the serif, set tight. The original Bark & Sky avatar, brought back as a mark. Reads as a byline or a bookplate.", lambda fg, bg: gm(fg)),
    ("ruled", "Ruled paper, Maine left blank", "Lines of one weight, like a notebook page, stopping at the edge of the state. The state is the gap. The inverse of the shared mark, in this concept's thinness.", lambda fg, bg: ruled(fg)),
    ("outline", "The state as one line", "The coast drawn as a single hairline, a pen drawing. Signature could not carry a stroke this thin; this concept is built from them.", lambda fg, bg: outline(fg)),
    ("horizon", "Ground and sky", "A disc split at the horizon, a thin line of light between. Bark below, Sky above: building a life here. No state at all.", lambda fg, bg: horizon(fg, bg, PA if fg == BK else BK)),
]


def wordmark(fg):
    d, w = SERIF.path("generation maine", 100, 0, 78, -8)
    return '<path fill="%s" d="%s"/>' % (fg, d), w


def build():
    files = {}
    rows = ""
    for key, title, note, draw in CANDS:
        on_paper = svg(S, S, draw(BK, PA), title)
        on_bark = svg(S, S, rect(0, 0, S, S, BK, 28) + draw(SK, BK), title)
        files["%s" % key] = on_paper
        files["%s-reversed" % key] = on_bark
        # avatar: the mark at 70 percent inside a Bark disc
        av = svg(S, S, '<circle cx="120" cy="120" r="120" fill="%s"/>' % BK + '<g transform="translate(36 36) scale(.7)">%s</g>' % draw(SK, BK), title)
        files["%s-avatar" % key] = av
        wm, w = wordmark(BK)
        lk = svg(w + S * 0.46 + 28, 114, '<g transform="translate(0 2) scale(.4583)">%s</g>' % draw(BK, PA) + '<g transform="translate(%s 14)">%s</g>' % (f(S * 0.46 + 28), wm), "Generation Maine")
        files["%s-lockup" % key] = lk
        def inl(sv, style):
            return sv.replace('role="img"', "").replace("<svg ", '<svg style="%s" ' % style, 1)
        rows += ('<div class="row"><div class="lab"><b>%s</b><p>%s</p></div>'
                 '<div class="t pa">%s</div><div class="t bk">%s</div>'
                 '<div class="t pa">%s%s%s</div><div class="t pa wide">%s</div></div>') % (
            title, note, inl(on_paper, "width:170px;height:170px"), inl(on_bark, "width:170px;height:170px"),
            inl(av, "width:110px;height:110px"), inl(av, "width:40px;height:40px"), inl(av, "width:16px;height:16px"),
            inl(lk, "width:440px;height:auto"))
    for k, v in files.items():
        write("%s/%s.svg" % (OUT, k), v)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bark &amp; Sky, mark candidates</title><style>'
            'body{margin:0;background:#E9E5DA;padding:36px;font-family:Inter,system-ui,sans-serif;color:#2B211C}'
            'h1{font:600 26px/1 Inter;margin:0 0 6px}.intro{font:14px/1.45 Inter;color:#6B5A4E;max-width:760px;margin:0 0 28px}'
            '.row{display:grid;grid-template-columns:250px 170px 170px 230px 1fr;gap:18px;align-items:center;margin-bottom:22px}'
            '.lab b{display:block;font:600 15px/1.3 Inter;margin-bottom:6px}.lab p{margin:0;font:12.5px/1.45 Inter;color:#6B5A4E}'
            '.t{border-radius:12px;display:flex;align-items:center;justify-content:center;gap:18px;padding:0;height:170px}'
            '.t.pa{background:#fff}.t.bk{background:#2B211C}.t.wide{padding:0 28px;justify-content:flex-start}'
            '.t svg{display:block;border-radius:12px}'
            '</style></head><body><h1>Bark &amp; Sky: marks this direction allows</h1>'
            '<p class="intro">Signature needed weight and one bright accent, so the lined state won there. Bark &amp; Sky is quiet, serif and one weight, which admits marks that would look thin beside Bricolage. Each row: on Paper, on Bark, the avatar at 110, 40 and 16 px, and the horizontal lockup.</p>%s</body></html>') % rows
    write(OUT + "/candidates.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), os.path.join(ROOT, OUT, "candidates.html"), os.path.join(ROOT, OUT, "candidates.png"), "1500"], check=True)


if __name__ == "__main__":
    build()
    print("mark candidates written")
