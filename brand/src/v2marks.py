"""Generation Maine identity v2: brandmark geometry for both directions.

A2 "First Light": a geometric G whose open mouth holds a rising sun. The crossbar is
the horizon. The sun is also the record light from v1.

B2 "Postmark": a round postmark with the name set on the ring, "GM" in the center
and cancellation lines that run off to the right. Each creator can get their own
postmark with their town in the center.

All text is shaped with HarfBuzz and outlined, so the files never need the fonts installed.
"""
import math
import os

from gmlib import ROOT, Face

V2 = os.path.join(ROOT, "brand", "fonts", "v2")
SANS = Face(os.path.join(V2, "InstrumentSans-SemiBold.ttf"))
SANS_MED = Face(os.path.join(V2, "InstrumentSans-Medium.ttf"))
SERIF_I = Face(os.path.join(V2, "InstrumentSerif-Italic.ttf"))
SERIF = Face(os.path.join(V2, "InstrumentSerif-Regular.ttf"))
ANTON = Face(os.path.join(V2, "Anton-Regular.ttf"))
MONO = Face(os.path.join(V2, "IBMPlexMono-Medium.ttf"))

# ---------------------------------------------------------------- palettes
A2 = {
    "spruce": "#0B4A34",   # brand green
    "pine": "#07261C",     # deepest background, for night/dark mode and video
    "fog": "#EDF0F4",      # light background
    "paper": "#FFFFFF",
    "signal": "#FF5B24",   # the sun / record light
    "dawn": "#FFC7A6",     # warm accent text on dark
    "granite": "#121417",  # text
    "moss": "#34795A",     # lines, secondary text on light
}
B2 = {
    "blueberry": "#3D2FD1",
    "ink": "#141414",
    "newsprint": "#ECECE6",
    "yellow": "#FFD23F",
    "paper": "#FFFFFF",
}


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- A2 symbol
def a2_symbol(x=0, y=0, size=200, ring="#0B4A34", sun="#FF5B24", gap_deg=58):
    """G-sunrise symbol in a size x size box whose top-left corner is (x, y)."""
    s = size / 200.0
    cx, cy = x + 100 * s, y + 100 * s
    R, t = 100 * s, 26 * s
    r = R - t

    def pt(rad, deg):
        a = math.radians(deg)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)

    # Ring from gap_deg counterclockwise round to 360 (the horizon on the right).
    o1, o2 = pt(R, gap_deg), pt(R, 0)
    i2, i1 = pt(r, 0), pt(r, gap_deg)
    ring_d = ("M%s %s A%s %s 0 1 0 %s %s L%s %s A%s %s 0 1 1 %s %s Z" % (
        f(o1[0]), f(o1[1]), f(R), f(R), f(o2[0]), f(o2[1]),
        f(i2[0]), f(i2[1]), f(r), f(r), f(i1[0]), f(i1[1])))
    # Crossbar = horizon. Top edge sits exactly on the center line.
    bar_d = "M%s %s H%s V%s H%s Z" % (f(cx + 6 * s), f(cy), f(cx + R), f(cy + t), f(cx + 6 * s))
    # Rising sun, sitting just above the horizon inside the mouth of the G.
    sr = 21 * s
    scx, scy = cx + 57 * s, cy - (sr + 9 * s)
    return ('<path fill="%s" d="%s"/><path fill="%s" d="%s"/><circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            % (ring, ring_d, ring, bar_d, f(scx), f(scy), f(sr), sun))


def a2_wordmark(x, baseline, size, fg, accent=None):
    """'Generation' in Instrument Sans SemiBold, 'Maine' in Instrument Serif Italic.

    Returns (svg, width). The serif is set 12 percent larger so the x-heights match.
    """
    d1, w1 = SANS.path("Generation", size, x, baseline, -18)
    gap = size * 0.22
    d2, w2 = SERIF_I.path("Maine", size * 1.08, x + w1 + gap, baseline, 0)
    col2 = accent or fg
    return ('<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg, d1, col2, d2)), w1 + gap + w2


def a2_lockup_h(fg, sun, ring=None, size=100):
    """Symbol left, wordmark right. Returns (svg, w, h)."""
    ring = ring or fg
    sym = size * 1.02
    wm, ww = a2_wordmark(sym + size * 0.34, size * 0.80, size, fg)
    body = a2_symbol(0, (size * 1.0 - sym) / 2 + size * 0.02, sym, ring, sun) + wm
    return body, sym + size * 0.34 + ww, size * 1.06


def a2_lockup_stacked(fg, sun, ring=None, size=100):
    ring = ring or fg
    d1, w1 = SANS.path("Generation", size, 0, 0, -18)
    d2, w2 = SERIF_I.path("Maine", size * 1.08, 0, 0, 0)
    W = max(w1, w2)
    sym = size * 1.5
    body = a2_symbol((W - sym) / 2, 0, sym, ring, sun)
    y1 = sym + size * 1.02
    y2 = y1 + size * 1.0
    d1, _ = SANS.path("Generation", size, (W - w1) / 2, y1, -18)
    d2, _ = SERIF_I.path("Maine", size * 1.08, (W - w2) / 2, y2, 0)
    body += '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg, d1, fg, d2)
    return body, W, y2 + size * 0.28


# ---------------------------------------------------------------- B2 postmark
def text_on_circle(face, text, size, cx, cy, radius, center_deg, fill, tracking=0, bottom=False):
    """Set text around a circle. center_deg: 0 = top, clockwise. bottom=True reads left to right along the bottom."""
    glyphs, adv = face.shape(text)
    sc = size / face.upem
    tr = tracking * face.upem / 1000.0
    total = (adv + tr * (len(glyphs) - 1)) * sc
    circ_r = radius
    span = total / circ_r  # radians
    out = []
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    x_along = 0.0
    for i, (name, gx, gy, cl) in enumerate(glyphs):
        gadv = face.hbfont.get_glyph_h_advance(face.tt.getGlyphID(name)) * sc
        mid = x_along + gadv / 2
        if not bottom:
            ang = math.radians(center_deg) - span / 2 + mid / circ_r
            px, py = cx + circ_r * math.sin(ang), cy - circ_r * math.cos(ang)
            rot = math.degrees(ang)
        else:
            ang = math.radians(center_deg) + span / 2 - mid / circ_r
            px, py = cx + circ_r * math.sin(ang), cy - circ_r * math.cos(ang)
            rot = math.degrees(ang) - 180
        pen = SVGPathPen(face.gs, ntos=f)
        # glyph drawn centered on its advance, baseline at the circle
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        # font units -> local (x right, y down) -> rotate -> translate
        ox, oy = -gadv / 2, 0
        if bottom:
            oy = size * 0.72  # push the cap height outward so letters sit inside the ring
        tx = px + ox * ca - oy * sa
        ty = py + ox * sa + oy * ca
        tp = TransformPen(pen, (sc * ca, sc * sa, sc * sa, -sc * ca, tx, ty))
        face.gs[name].draw(tp)
        out.append('<path fill="%s" d="%s"/>' % (fill, pen.getCommands()))
        x_along += gadv + tr * sc
    return "".join(out)


def b2_postmark(cx, cy, R, ink, center_text="ME", ring_top="GENERATION MAINE", ring_bottom="YOUNG MAINERS",
                center_sub=None, accent=None):
    """Round postmark. Returns svg string. R is the outer radius."""
    lw = R * 0.028
    body = '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(cx), f(cy), f(R - lw / 2), ink, f(lw))
    body += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(cx), f(cy), f(R * 0.635), ink, f(lw * 0.6))
    ts = R * 0.13
    body += text_on_circle(ANTON, ring_top, ts, cx, cy, R * 0.755, 0, ink, tracking=140)
    body += text_on_circle(ANTON, ring_bottom, ts, cx, cy, R * 0.755, 180, ink, tracking=140, bottom=True)
    # separator dots at 9 and 3 o'clock
    for ang in (90, 270):
        a = math.radians(ang)
        body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (
            f(cx + R * 0.80 * math.sin(a)), f(cy - R * 0.80 * math.cos(a)), f(R * 0.025), accent or ink)
    # center
    cs = R * (0.56 if len(center_text) <= 2 else 0.27)
    d, w = ANTON.path(center_text, cs, 0, 0, 20)
    cap = 0.715 * cs  # Anton cap height is tall
    base = cy + cap / 2 - (R * 0.07 if center_sub else 0)
    d, w = ANTON.path(center_text, cs, cx - w / 2, base, 20)
    body += '<path fill="%s" d="%s"/>' % (ink, d)
    if center_sub:
        ms = R * 0.085
        d2, w2 = MONO.path(center_sub, ms, 0, 0, 40)
        d2, w2 = MONO.path(center_sub, ms, cx - w2 / 2, base + ms * 1.9, 40)
        body += '<path fill="%s" d="%s"/>' % (ink, d2)
    return body


def b2_cancel_lines(x0, cy, length, R, ink, n=5):
    """Wavy cancellation lines, like a postal cancel, running right from the stamp."""
    gap = R * 0.16
    amp = R * 0.05
    wl = R * 0.55
    body = ""
    for i in range(n):
        yy = cy + (i - (n - 1) / 2) * gap
        d = "M%s %s" % (f(x0), f(yy))
        steps = int(length / (wl / 2))
        for k in range(steps):
            xa = x0 + (k + 0.5) * wl / 2
            xb = x0 + (k + 1) * wl / 2
            ya = yy + (amp if k % 2 == 0 else -amp)
            d += " Q%s %s %s %s" % (f(xa), f(ya), f(xb), f(yy))
        body += '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (d, ink, f(R * 0.03))
    return body


def b2_lockup(ink, accent=None, R=100, lines=True):
    """Postmark plus cancel lines. Returns (svg, w, h)."""
    body = b2_postmark(R, R, R, ink, accent=accent)
    w = 2 * R
    if lines:
        body += b2_cancel_lines(2 * R - R * 0.05, R, R * 2.2, R, ink)
        w = 2 * R + R * 2.15
    return body, w, 2 * R


def b2_small(cx, cy, R, ink, fill=None):
    """Small-size postmark for avatars and favicons: one ring and GM, no ring text."""
    body = ""
    if fill:
        body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(R), fill)
    lw = R * 0.07
    body += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(cx), f(cy), f(R * 0.86), ink, f(lw))
    cs = R * 0.86
    d, w = ANTON.path("ME", cs, 0, 0, 20)
    d, w = ANTON.path("ME", cs, cx - w / 2, cy + 0.715 * cs / 2, 20)
    return body + '<path fill="%s" d="%s"/>' % (ink, d)
