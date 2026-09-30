"""Brandmarks and lockups for both directions. Hand-built SVG geometry, no font outlines in the
Signature mark, so it can be redrawn at any size and cut in any material.

Signature mark, "the open G": a geometric G whose bar is the Marigold dot. Without the dot it is an
arc. With the dot it is a G. Described in one sentence: a G whose bar is a dot. The sentence does
not restate the name or the brief, so it passes the on-the-nose test.

Bark & Sky mark, "the g": the lowercase Hedvig g set inside a circle, with its tail leaving the
circle at the bottom. One sentence: a g whose tail leaves the circle.

  python3 brand/src/build_marks.py     # writes brand/identity/marks/*.svg
"""
import math
import os

from gmlib import ROOT, Face, write
from build_v4 import wordmark_one_line, wordmark_stacked, svg, rect, text, f
from build_v6 import C

OUT = "brand/identity/marks"
MPI = "An initiative of Maine Policy Institute"
D = {"sky": "#CFE3F0", "bark": "#2B211C", "paper": "#FFFFFF", "mist": "#EEF4F8", "clay": "#6B5A4E"}
HEDVIG = Face("d/HedvigLettersSerif-24.ttf")


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def annulus_sector(cx, cy, ro, ri, a0, a1, fill):
    """Filled ring segment from a0 to a1 degrees, clockwise in screen space (0 = 3 o'clock)."""
    sweep = (a1 - a0) % 360
    large = 1 if sweep > 180 else 0
    x0, y0 = pol(cx, cy, ro, a0); x1, y1 = pol(cx, cy, ro, a1)
    x2, y2 = pol(cx, cy, ri, a1); x3, y3 = pol(cx, cy, ri, a0)
    d = "M%s %s A%s %s 0 %d 1 %s %s L%s %s A%s %s 0 %d 0 %s %s Z" % (
        f(x0), f(y0), f(ro), f(ro), large, f(x1), f(y1), f(x2), f(y2), f(ri), f(ri), large, f(x3), f(y3))
    return '<path fill="%s" d="%s"/>' % (fill, d)


# ------------------------------------------------------------------ Signature: the open G
def open_g(x, y, s, fg, dot, variant="a", mono=False):
    """A G in a box of side s. Stroke is 0.19 s, like the Bricolage stem. The opening faces right.
    variant a: the dot sits where the bar would be, just inside the counter.
    variant b: the dot sits in the opening, on the ring's centerline, closing the gap.
    variant c: the arc ends in a short vertical spur, the dot is the bar."""
    cx, cy = x + s / 2, y + s / 2
    ro = s * 0.46
    st = s * 0.19
    ri = ro - st
    rm = (ro + ri) / 2
    dr = st * 0.62
    dot_fill = fg if mono else dot
    out = ""
    if variant == "a":
        out += annulus_sector(cx, cy, ro, ri, 8, 300, fg)          # gap from -60 to 8 degrees
        dx, dy = cx + rm * 0.55, cy + rm * 0.02
        out += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(dx), f(dy), f(dr), dot_fill)
    elif variant == "b":
        out += annulus_sector(cx, cy, ro, ri, 20, 300, fg)         # gap from -60 to 20 degrees
        dx, dy = pol(cx, cy, rm, -20)
        out += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(dx), f(dy), f(dr), dot_fill)
    else:
        out += annulus_sector(cx, cy, ro, ri, 0, 300, fg)          # arc stops at 3 o'clock
        # a vertical spur rising from the terminal, like Bricolage's G
        spur_h = s * 0.16
        out += rect(cx + ri, cy - spur_h, st, spur_h, fg)
        dx, dy = cx + ri - dr - s * 0.02, cy - spur_h / 2
        out += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(dx), f(dy), f(dr), dot_fill)
    return out


# ------------------------------------------------------------------ the challenge: non-letter marks
def dot(cx, cy, r, fill):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), fill)


def mark_endmark(x, y, s, field, dotc, bg=None):
    """A field with the dot in its lower left corner, where the headline ends."""
    return rect(x, y, s, s, field) + dot(x + s * 0.27, y + s * 0.73, s * 0.135, dotc)


def mark_notch(x, y, s, field, dotc, bg="none"):
    """A field with a quarter circle cut from the lower left corner. The dot sits in the cut with
    clear space around it. The field makes room, and the mark shows its own clear space rule."""
    R = s * 0.34            # radius of the cut
    r = s * 0.16            # radius of the dot
    cx, cy = x, y + s       # the corner
    d = ("M%s %s H%s V%s H%s V%s A%s %s 0 0 0 %s %s Z" % (
        f(x), f(y), f(x + s), f(y + s), f(x + R), f(y + s), f(R), f(R), f(x), f(y + s - R)))
    return '<path fill="%s" d="%s"/>' % (field, d) + dot(cx + R * 0.5, cy - R * 0.5, r, dotc)


def mark_corner(x, y, s, field, dotc, bg=None):
    """A field with the dot centred on its lower left corner, half in and half out."""
    r = s * 0.17
    R = r + s * 0.07
    d = ("M%s %s H%s V%s H%s A%s %s 0 0 0 %s %s Z" % (
        f(x), f(y), f(x + s), f(y + s), f(x + R), f(R), f(R), f(x), f(y + s - R)))
    return '<path fill="%s" d="%s"/>' % (field, d) + dot(x, y + s, r, dotc)


def mark_ring(x, y, s, field, dotc, bg=None):
    """A ring open at the lower left, the dot in the gap."""
    cx, cy = x + s / 2, y + s / 2
    ro, st = s * 0.46, s * 0.17
    body = annulus_sector(cx, cy, ro, ro - st, 165, 105, field)
    dx, dy = pol(cx, cy, ro - st / 2, 135)
    return body + dot(dx, dy, st * 0.62, dotc)


def mark_frame(x, y, s, field, dotc, bg=None):
    """A 9:16 frame with the dot low left. Shown to be rejected: it says video."""
    w = s * 0.5625
    x0 = x + (s - w) / 2
    st = s * 0.075
    d = "M%s %s H%s V%s H%s Z M%s %s V%s H%s V%s Z" % (f(x0), f(y), f(x0 + w), f(y + s), f(x0),
                                                     f(x0 + st), f(y + st), f(y + s - st), f(x0 + w - st), f(y + st))
    return '<path fill="%s" fill-rule="evenodd" d="%s"/>' % (field, d) + dot(x0 + st + s * 0.11, y + s - st - s * 0.11, s * 0.075, dotc)


def mark_letter(x, y, s, field, dotc, bg=None):
    return open_g(x, y, s, field, dotc, "b")


CANDIDATES = [
    ("letter", "The open G, the control", mark_letter, "A G whose bar is a dot. Reads as a C. Looks like every fintech mark."),
    ("endmark", "The end mark", mark_endmark, "A field with the dot in its lower left, where every headline ends. Abstract and editorial. Looks like a notification badge at small sizes."),
    ("notch", "The notch", mark_notch, "A field with a corner cut away for the dot. The field makes room. The mark shows its own clear space."),
    ("corner", "The corner", mark_corner, "The dot centred on the corner of a field, half in and half out. A sticker."),
    ("ring", "The open ring", mark_ring, "A ring open at the lower left with the dot in the gap. A target, or a record button. The record dot failed once already."),
    ("frame", "The frame", mark_frame, "A vertical frame with the dot low left. Says video. Fails the on-the-nose test."),
]


from build_brand import DISPLAY


def mark_borrowed_g(x, y, s, field, dotc, bg=None):
    """Bricolage's own C, with the Marigold dot where the G's bar would sit. A letter mark with the
    wordmark's drawing in it, not a compass-and-ruler G."""
    size = s * 1.02
    sc = size / DISPLAY.upem
    b = DISPLAY.glyph_bounds("C")
    gw, gh = (b[2] - b[0]) * sc, (b[3] - b[1]) * sc
    gx = x + (s - gw) / 2 - b[0] * sc
    base = y + (s + gh) / 2 + b[1] * sc
    d, _ = DISPLAY.path("C", size, gx, base)
    # the bar of a G sits a little below the centre of the counter, at the right
    cx = gx + b[2] * sc - s * 0.13
    cy = base - gh * 0.47 + s * 0.02
    return '<path fill="%s" d="%s"/>' % (field, d) + dot(cx, cy, s * 0.115, dotc)


def mark_window(x, y, s, field, dotc, bg=None):
    """A field with a round window in its lower left. You see through the brand to what is behind
    it. On colour the window holds the dot; in one colour the window is simply open."""
    r = s * 0.2
    cx, cy = x + s * 0.3, y + s * 0.7
    d = ("M%s %s H%s V%s H%s Z M%s %s a%s %s 0 1 0 %s 0 a%s %s 0 1 0 %s 0 Z" % (
        f(x), f(y), f(x + s), f(y + s), f(x), f(cx - r), f(cy), f(r), f(r), f(2 * r), f(r), f(r), f(-2 * r)))
    body = '<path fill="%s" fill-rule="evenodd" d="%s"/>' % (field, d)
    if dotc != field:
        body += dot(cx, cy, r * 0.66, dotc)
    return body


def mark_set_period(x, y, s, field, dotc, bg=None):
    """A period that sits: a dot with a flat base, resting on a short rule. The dot that ends
    every headline, drawn as its own glyph."""
    r = s * 0.27
    cx = x + s * 0.5
    base = y + s * 0.74
    flat = r * 0.32
    cy = base - r + flat * 0.5
    # circle with the bottom cut flat
    k = math.sqrt(max(r * r - (r - flat) ** 2, 0))
    d = "M%s %s A%s %s 0 1 1 %s %s Z" % (f(cx - k), f(base), f(r), f(r), f(cx + k), f(base))
    body = '<path fill="%s" d="%s"/>' % (dotc, d)
    body += rect(x + s * 0.12, base + s * 0.06, s * 0.76, s * 0.055, field)
    return body


def mark_pair(x, y, s, field, dotc, bg=None):
    """Two fields, one tall and one short, in the column habit, the dot ending the short one.
    Shown to test whether the grid habit can be a glyph."""
    g = s * 0.1
    w = (s - g) / 2
    body = rect(x, y, w, s, field) + rect(x + w + g, y, w, s * 0.62, field)
    body += dot(x + w + g + w / 2, y + s * 0.62 + (s - s * 0.62) / 2 + s * 0.02, s * 0.1, dotc)
    return body


CANDIDATES += [
    ("borrowed", "The borrowed G", mark_borrowed_g, "Bricolage's own C with the dot as the G's bar. A letter mark that carries the wordmark's drawing."),
    ("window", "The window", mark_window, "A field with a round window low left. You see through the brand to what is behind it. In one colour the window stays open."),
    ("period", "The set period", mark_set_period, "The dot that ends every headline, drawn as a glyph: a dot with a flat base, sitting on its line."),
    ("pair", "The pair", mark_pair, "Two columns, one short, the dot ending the short one. The grid habit as a glyph."),
]


def tile(mark_body, s, bg, rx=None, circle=False):
    if circle:
        base = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(s / 2), f(s / 2), f(s / 2), bg)
    else:
        base = rect(0, 0, s, s, bg, rx or 0)
    return base + mark_body


def sig_lockups(variant):
    m = {}
    sp, bi, mg, pi = C["spruce"], C["birch"], C["marigold"], C["pine"]
    # the mark alone, positive and reversed, mono, and in a circle for avatars
    m["mark"] = svg(200, 200, open_g(0, 0, 200, sp, mg, variant), "Generation Maine")
    m["mark-reversed"] = svg(200, 200, open_g(0, 0, 200, bi, mg, variant), "Generation Maine")
    m["mark-mono"] = svg(200, 200, open_g(0, 0, 200, sp, mg, variant, mono=True), "Generation Maine")
    m["mark-black"] = svg(200, 200, open_g(0, 0, 200, "#000000", mg, variant, mono=True), "Generation Maine")
    m["avatar"] = svg(200, 200, tile(open_g(22, 22, 156, bi, mg, variant), 200, sp, circle=True), "Generation Maine")
    m["avatar-birch"] = svg(200, 200, tile(open_g(22, 22, 156, sp, mg, variant), 200, bi, circle=True), "Generation Maine")
    m["avatar-marigold"] = svg(200, 200, tile(open_g(22, 22, 156, pi, pi, variant, mono=True), 200, mg, circle=True), "Generation Maine")
    m["app-icon"] = svg(200, 200, tile(open_g(30, 30, 140, bi, mg, variant), 200, sp, rx=44), "Generation Maine")
    # horizontal lockup: mark height equals the wordmark's cap height plus a little
    for suf, fg in (("", sp), ("-reversed", bi)):
        b, w, h = wordmark_one_line(fg, mg, "circle", 100)
        mh = 92
        gap = 26
        body = open_g(0, h - mh - 2, mh, fg, mg, variant) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + gap), b)
        m["lockup-horizontal" + suf] = svg(w + mh + gap, h, body, "Generation Maine")
        # stacked: mark above the stacked wordmark, both left aligned
        b2, w2, h2 = wordmark_stacked(fg, mg, "circle", 100)
        ms = 150
        body = open_g(0, 0, ms, fg, mg, variant) + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 34), b2)
        m["lockup-stacked" + suf] = svg(max(w2, ms), ms + 34 + h2, body, "Generation Maine")
        # endorsed: horizontal lockup, a hairline, the institute line
        b, w, h = wordmark_one_line(fg, mg, "circle", 100)
        body = open_g(0, h - mh - 2, mh, fg, mg, variant) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + gap), b)
        tw = w + mh + gap
        body += rect(0, h + 24, tw, 2, fg) + text(0, h + 66, MPI, 30, fg, weight=500)
        m["lockup-endorsed" + suf] = svg(tw, h + 80, body, "Generation Maine, an initiative of Maine Policy Institute")
    return m


# ------------------------------------------------------------------ Bark & Sky: the g
def hedvig_g(x, y, s, fg, bg=None, tail_out=True):
    """Lowercase g in a circle of diameter s. The tail leaves the circle at the bottom."""
    cx, cy = x + s / 2, y + s / 2
    out = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(s / 2), bg) if bg else ""
    size = s * 0.86
    sc = size / HEDVIG.upem
    b = HEDVIG.glyph_bounds("g")
    gw = (b[2] - b[0]) * sc
    gx = cx - gw / 2 - b[0] * sc
    # x-height of the g sits a little above centre, so the tail drops out of the circle
    base = cy + s * (0.18 if tail_out else 0.10)
    d, _ = HEDVIG.path("g", size, gx, base)
    return out + '<path fill="%s" d="%s"/>' % (fg, d)


def lower_wordmark(fg, size=100):
    d, w = HEDVIG.path("generation maine", size, 0, size * 0.78, -8)
    return '<path fill="%s" d="%s"/>' % (fg, d), w, size * 1.0


def bs_lockups():
    m = {}
    bk, sk, pa = D["bark"], D["sky"], D["paper"]
    m["mark"] = svg(200, 240, hedvig_g(0, 0, 200, bk), "Generation Maine")
    m["mark-in-circle"] = svg(200, 240, hedvig_g(0, 0, 200, sk, bk), "Generation Maine")
    m["mark-in-circle-sky"] = svg(200, 240, hedvig_g(0, 0, 200, bk, sk), "Generation Maine")
    m["avatar"] = svg(200, 200, hedvig_g(0, 0, 200, sk, bk, tail_out=False), "Generation Maine")
    m["avatar-sky"] = svg(200, 200, hedvig_g(0, 0, 200, bk, sk, tail_out=False), "Generation Maine")
    for suf, fg in (("", bk), ("-reversed", pa)):
        b, w, h = lower_wordmark(fg)
        ms = 96
        body = hedvig_g(0, h - ms - 6, ms, fg) + '<g transform="translate(%s 0)">%s</g>' % (f(ms + 22), b)
        m["lockup-horizontal" + suf] = svg(w + ms + 22, h + 20, body, "Generation Maine")
        ms = 150
        body = hedvig_g((w - ms) / 2, 0, ms, fg) + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 60), b)
        m["lockup-stacked" + suf] = svg(w, ms + 60 + h, body, "Generation Maine")
        body = b + rect(0, h + 18, w, 1.5, fg) + text(w / 2, h + 56, MPI, 26, fg, fam="Inter", weight=400, anchor="middle")
        m["lockup-endorsed" + suf] = svg(w, h + 70, body, "Generation Maine, an initiative of Maine Policy Institute")
    return m


def build_candidates():
    sp, bi, mg, pi = C["spruce"], C["birch"], C["marigold"], C["pine"]
    out = {}
    for key, name, fn, note in CANDIDATES:
        m = {}
        m["mark"] = svg(200, 200, fn(0, 0, 200, sp, mg), "Generation Maine")
        m["mark-reversed"] = svg(200, 200, fn(0, 0, 200, bi, mg), "Generation Maine")
        m["mark-mono"] = svg(200, 200, fn(0, 0, 200, sp, sp), "Generation Maine")
        m["avatar"] = svg(200, 200, tile(fn(36, 36, 128, bi, mg), 200, sp, circle=True), "Generation Maine")
        m["avatar-birch"] = svg(200, 200, tile(fn(36, 36, 128, sp, mg), 200, bi, circle=True), "Generation Maine")
        b, w, h = wordmark_one_line(sp, mg, "circle", 100)
        mh = 66
        body = fn(0, 8, mh, sp, mg) + '<g transform="translate(%s 0)">%s</g>' % (f(mh + 24), b)
        m["lockup"] = svg(w + mh + 24, h, body, "Generation Maine")
        for k, v in m.items():
            write("%s/candidates/%s/%s.svg" % (OUT, key, k), v)
        out[key] = (name, note, m)
    return out


def build():
    out = {}
    for v in "abc":
        for k, s in sig_lockups(v).items():
            write("%s/signature-%s/%s.svg" % (OUT, v, k), s)
        out["sig-" + v] = sig_lockups(v)
    out["bs"] = bs_lockups()
    for k, s in out["bs"].items():
        write("%s/bark-sky/%s.svg" % (OUT, k), s)
    return out


if __name__ == "__main__":
    o = build()
    c = build_candidates()
    print("marks written:", {k: len(v) for k, v in o.items()}, "candidates:", list(c))
