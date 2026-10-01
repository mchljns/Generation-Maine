"""The logo for each concept, complete.

Signature  : the margin-room mark in Spruce and Marigold, the Bricolage wordmark, lockups,
             reversed and one-colour versions, avatar and favicon, clear space, and a large-size
             variant where the field of lines is Maine itself.
Bark & Sky : the same rule drawn for the second concept. Thin Bark lines, the bends in Clay,
             the lowercase Hedvig wordmark, centred lockups.

All text is outlined, so the files never depend on an installed font.
  python3 brand/src/build_logos.py     # writes brand/identity/logo/<concept>/*.svg and logos.html
"""
import math
import os

from gmlib import ROOT, Face, write
from build_v4 import svg, rect, f, wordmark_one_line, wordmark_stacked
from build_v6 import C
from build_push import field
from build_mark2 import half_room
import maine2

OUT = "brand/identity/logo"
SP, BI, MG, PI, MOSS = C["spruce"], C["birch"], C["marigold"], C["pine"], C["moss"]
D = {"sky": "#CFE3F0", "bark": "#2B211C", "paper": "#FFFFFF", "mist": "#EEF4F8", "clay": "#6B5A4E"}
MPI = "An initiative of Maine Policy Institute"
INTER = Face("Inter-SemiBold.ttf")
HEDVIG = Face("d/HedvigLettersSerif-24.ttf")
HEDVIG_SANS = Face("d/HedvigLettersSans-Regular.ttf")


def outlined(face, text, size, x, y, fill, track=0, anchor="start"):
    d, w = face.path(text, size, x, y, track)
    if anchor == "middle":
        d, w = face.path(text, size, x - w / 2, y, track)
    return '<path fill="%s" d="%s"/>' % (fill, d), w


# ------------------------------------------------------------------ Signature
def sig_mark(x, y, s, fg, mark, small=False):
    return half_room(x, y, s, fg, mark, small=small, where="left", n=(6 if small else 9), wt=(0.016, 0.06), r_k=0.2)


def sig_maine_mark(x, y, s, fg, mark):
    """Large-size variant: the field of lines is Maine, the room opens from the western edge.
    For 110 px and up, where the state can be read."""
    ring = maine2.fit(x + s * 0.1, y + s * 0.04, s * 0.8, s * 0.92)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    n = 21
    cx, cy = minx, miny + (maxy - miny) * 0.64
    r = s * 0.1
    clear = s * 0.04
    R = r + clear
    out = ""
    steps = 160
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.03 + 0.94 * t)
        w = s * (0.012 + 0.024 * t)
        dy0 = y0 - cy
        ady = abs(dy0)
        sign = 1 if dy0 >= 0 else -1
        if ady < R:
            amp, sig = R - ady, R * 0.75
        else:
            amp, sig = 0.42 * R * math.exp(-((ady - R) / (0.55 * R)) ** 2), R * 0.95
        pts = []
        for k in range(steps + 1):
            px = minx + (maxx - minx) * k / steps
            dx = px - cx
            off = amp * math.exp(-(dx / sig) ** 2)
            if ady < R and abs(dx) < R:
                off = max(off, math.sqrt(R * R - dx * dx) - ady)
            pts.append((px, y0 + sign * off, off / R))
        run, gold = [], None
        def flush(run, gold):
            if len(run) < 2 or (run[-1][0] - run[0][0]) < w * 1.6:
                return ""
            return '<path d="M%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" fill="none"/>' % (
                " L".join("%s %s" % (f(a), f(b)) for a, b, _ in run), mark if gold else fg, f(w))
        for px, py, o in pts:
            xs = maine2.crossings(ring, py)
            inside = any(a <= px <= b for a, b in zip(xs[0::2], xs[1::2]))
            g = o > 0.18 and ady < R
            if not inside:
                out += flush(run, gold); run, gold = [], None
                continue
            if gold is None or g == gold:
                run.append((px, py, o))
            else:
                out += flush(run, gold); run = [run[-1], (px, py, o)]
            gold = g
        out += flush(run, gold)
    return out


def sig_logos():
    m = {}
    # the mark
    m["mark"] = svg(240, 240, sig_mark(0, 0, 240, SP, MG), "Generation Maine")
    m["mark-reversed"] = svg(240, 240, sig_mark(0, 0, 240, BI, MG), "Generation Maine")
    m["mark-mono"] = svg(240, 240, sig_mark(0, 0, 240, SP, SP), "Generation Maine")
    m["mark-black"] = svg(240, 240, sig_mark(0, 0, 240, "#000000", "#000000"), "Generation Maine")
    m["mark-white"] = svg(240, 240, sig_mark(0, 0, 240, "#FFFFFF", "#FFFFFF"), "Generation Maine")
    m["mark-small"] = svg(240, 240, sig_mark(0, 0, 240, SP, MG, small=True), "Generation Maine")
    m["mark-maine"] = svg(240, 240, sig_maine_mark(0, 0, 240, SP, MG), "Generation Maine")
    m["mark-maine-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + sig_maine_mark(0, 0, 240, BI, MG), "Generation Maine")
    # the wordmark: the dot on the i only when it stands alone
    for suf, fg in (("", SP), ("-reversed", BI), ("-black", "#000000"), ("-white", "#FFFFFF")):
        b, w, h = wordmark_one_line(fg, MG if suf in ("", "-reversed") else fg, "circle", 100)
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
    # lockups: the mark's lines span the cap height, the room's mouth sits on the left edge
    for suf, fg in (("", SP), ("-reversed", BI), ("-mono", SP), ("-black", "#000000"), ("-white", "#FFFFFF")):
        mk = MG if suf in ("", "-reversed") else fg
        b, w, h = wordmark_one_line(fg, fg, "circle", 100)
        mh = 78
        gap = 22
        body = sig_mark(0, 74 - mh + 4, mh, fg, mk) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + gap), b)
        m["lockup-horizontal" + suf] = svg(w + mh + gap, h, body, "Generation Maine")
        b2, w2, h2 = wordmark_stacked(fg, fg, "circle", 100)
        ms = 132
        body = sig_mark(-ms * 0.06, 0, ms, fg, mk) + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 26), b2)
        m["lockup-stacked" + suf] = svg(max(w2, ms), ms + 26 + h2, body, "Generation Maine")
        # endorsed: the horizontal lockup, a hairline, the institute line, all outlined
        b, w, h = wordmark_one_line(fg, fg, "circle", 100)
        tw = w + mh + gap
        body = sig_mark(0, 74 - mh + 4, mh, fg, mk) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + gap), b)
        body += rect(mh + gap, h + 22, w, 2, fg)
        t, _ = outlined(INTER, MPI, 27, mh + gap, h + 60, fg)
        body += t
        m["lockup-endorsed" + suf] = svg(tw, h + 72, body, "Generation Maine, an initiative of Maine Policy Institute")
    # avatar, favicon, app icon
    m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + sig_mark(44, 44, 152, BI, MG, small=True), "Generation Maine")
    m["avatar-birch"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % BI + sig_mark(44, 44, 152, SP, MG, small=True), "Generation Maine")
    m["avatar-maine"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + sig_maine_mark(30, 24, 180, BI, MG), "Generation Maine")
    m["app-icon"] = svg(240, 240, rect(0, 0, 240, 240, SP, 52) + sig_mark(40, 40, 160, BI, MG, small=True), "Generation Maine")
    m["favicon"] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="%s"/>' % SP + sig_mark(6, 6, 20, BI, MG, small=True), "Generation Maine")
    return m


# ------------------------------------------------------------------ Bark & Sky
def bs_mark(x, y, s, fg, mark, small=False):
    """The same rule, drawn quieter: seven thin lines of one weight, the bends in Clay."""
    n = 5 if small else 7
    w = s * (0.045 if small else 0.022)
    pad = s * 0.06
    r = s * (0.26 if small else 0.22)
    ob = [("circle", x + pad, y + s * 0.6, r, True)]
    return field(x, y, s, s, n, ob, s * (0.07 if small else 0.05), fg, mark, w, w, steps=180, pad=pad, mode="wrap")


def bs_wordmark(fg, size=100):
    d, w = HEDVIG.path("generation maine", size, 0, size * 0.78, -8)
    return '<path fill="%s" d="%s"/>' % (fg, d), w, size * 1.0


def bs_logos():
    m = {}
    bk, sk, pa, cl = D["bark"], D["sky"], D["paper"], D["clay"]
    m["mark"] = svg(240, 240, bs_mark(0, 0, 240, bk, cl), "Generation Maine")
    m["mark-on-sky"] = svg(240, 240, rect(0, 0, 240, 240, sk) + bs_mark(0, 0, 240, bk, pa), "Generation Maine")
    m["mark-reversed"] = svg(240, 240, rect(0, 0, 240, 240, bk) + bs_mark(0, 0, 240, sk, pa), "Generation Maine")
    m["mark-mono"] = svg(240, 240, bs_mark(0, 0, 240, bk, bk), "Generation Maine")
    m["mark-small"] = svg(240, 240, bs_mark(0, 0, 240, bk, cl, small=True), "Generation Maine")
    for suf, fg in (("", bk), ("-reversed", pa), ("-sky", sk)):
        b, w, h = bs_wordmark(fg)
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
    for suf, fg, mk in (("", bk, cl), ("-reversed", sk, pa), ("-mono", bk, bk)):
        b, w, h = bs_wordmark(fg)
        mh = 70
        gap = 24
        body = bs_mark(0, h - mh - 8, mh, fg, mk) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + gap), b)
        m["lockup-horizontal" + suf] = svg(w + mh + gap, h, body, "Generation Maine")
        # stacked and centred, which is how this concept sets everything
        ms = 120
        body = bs_mark((w - ms) / 2, 0, ms, fg, mk) + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 30), b)
        m["lockup-stacked" + suf] = svg(w, ms + 30 + h, body, "Generation Maine")
        body = b + rect(0, h + 14, w, 1.5, fg)
        t, _ = outlined(HEDVIG_SANS, MPI, 24, w / 2, h + 50, fg, anchor="middle")
        body += t
        m["lockup-endorsed" + suf] = svg(w, h + 64, body, "Generation Maine, an initiative of Maine Policy Institute")
    m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % bk + bs_mark(44, 44, 152, sk, pa, small=True), "Generation Maine")
    m["avatar-sky"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % sk + bs_mark(44, 44, 152, bk, pa, small=True), "Generation Maine")
    m["app-icon"] = svg(240, 240, rect(0, 0, 240, 240, sk, 52) + bs_mark(40, 40, 160, bk, pa, small=True), "Generation Maine")
    m["favicon"] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="%s"/>' % bk + bs_mark(6, 6, 20, sk, pa, small=True), "Generation Maine")
    return m


def build():
    s, b = sig_logos(), bs_logos()
    for k, v in s.items():
        write("%s/signature/%s.svg" % (OUT, k), v)
    for k, v in b.items():
        write("%s/bark-sky/%s.svg" % (OUT, k), v)
    return s, b


if __name__ == "__main__":
    s, b = build()
    print("signature:", len(s), "bark-sky:", len(b))
