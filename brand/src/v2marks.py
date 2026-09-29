"""Generation Maine identity v2: brandmark geometry for both directions.

A2 "First Light": the outline of Maine cut out of an orange disc, the rising sun
and a camera's record light. The earlier G-sunrise symbol is kept as an alternate.

B2 "Postmark": a round postmark with the name set on the ring, Maine in the center
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
    body = b2_postmark_maine(R, R, R, ink)
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


# ---------------------------------------------------------------- Maine silhouette marks
from maine import maine_shape, project, ASPECT, LUBEC, TOWNS  # noqa: E402

TOL = 0.04     # simplification, degrees
ROUND = 1.2    # corner rounding, px at 200 px height


def sunrise_state(x, y, h, land, sun, line=None):
    """Maine silhouette with the sun rising just off Lubec. Box is (h*1.05) wide by h tall."""
    w = h * ASPECT
    s = h / 200.0
    d, _ = maine_shape(x, y, w, h, TOL, ROUND * s)
    lx, ly = project(LUBEC[0], LUBEC[1], x, y, w, h)
    r = h * 0.105
    gap = h * 0.025
    cx, cy = lx + r + gap * 1.6, ly - r - gap
    body = '<path d="%s" fill="%s"/>' % (d, land)
    if line:
        body += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (
            f(lx - h * 0.02), f(ly - h * 0.006), f(r * 2 + gap * 3.2 + h * 0.02), f(h * 0.018), line)
    body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), sun)
    return body, (cx + r) - x


def sun_badge(cx, cy, R, sun, land_knock):
    """Orange disc with Maine knocked out of it (drawn in the background color)."""
    h = R * 1.3
    w = h * ASPECT
    d, _ = maine_shape(cx - w / 2 - R * 0.02, cy - h / 2 + R * 0.02, w, h, TOL, ROUND * h / 200)
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"/><path d="%s" fill="%s"/>' % (f(cx), f(cy), f(R), sun, d, land_knock))


def b2_postmark_maine(cx, cy, R, ink, town=None, sub=None, dot=None, ring_top="GENERATION MAINE", ring_bottom="YOUNG MAINERS"):
    """Postmark with the Maine silhouette in the center and a dot on the creator's town."""
    lw = R * 0.028
    body = '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(cx), f(cy), f(R - lw / 2), ink, f(lw))
    body += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(cx), f(cy), f(R * 0.635), ink, f(lw * 0.6))
    ts = R * 0.13
    body += text_on_circle(ANTON, ring_top, ts, cx, cy, R * 0.755, 0, ink, tracking=140)
    body += text_on_circle(ANTON, ring_bottom, ts, cx, cy, R * 0.755, 180, ink, tracking=140, bottom=True)
    for ang in (90, 270):
        a = math.radians(ang)
        body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx + R * 0.80 * math.sin(a)), f(cy - R * 0.80 * math.cos(a)), f(R * 0.025), ink)
    h = R * (0.66 if town else 0.92)
    w = h * ASPECT
    mx, my = cx - w / 2, cy - h / 2 - (R * 0.15 if town else 0)
    d, _ = maine_shape(mx, my, w, h, TOL, ROUND * h / 200)
    body += '<path d="%s" fill="%s"/>' % (d, ink)
    if town:
        tx, ty = project(TOWNS[town][0], TOWNS[town][1], mx, my, w, h)
        body += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            f(tx), f(ty), f(R * 0.05), dot or "#FFD23F", ink, f(R * 0.018))
        cs = R * 0.15
        dd, ww = ANTON.path(town.upper(), cs, 0, 0, 40)
        dd, ww = ANTON.path(town.upper(), cs, cx - ww / 2, my + h + cs * 1.25, 40)
        body += '<path fill="%s" d="%s"/>' % (ink, dd)
        if sub:
            ms = R * 0.062
            d2, w2 = MONO.path(sub, ms, 0, 0, 40)
            d2, w2 = MONO.path(sub, ms, cx - w2 / 2, my + h + cs * 1.25 + ms * 1.7, 40)
            body += '<path fill="%s" d="%s"/>' % (ink, d2)
    return body


def gm_wordmark(x, baseline, size, fg):
    """Plain wordmark: 'Generation Maine' in Instrument Sans SemiBold. No italics."""
    d, w = SANS.path("Generation Maine", size, x, baseline, -18)
    return '<path fill="%s" d="%s"/>' % (fg, d), w


_UID = [0]


def badge(x, y, size, disc, land=None):
    """First Light brandmark: a sun/record-light disc with Maine cut out of it.

    If land is None the silhouette is a true cutout (transparent). Otherwise it is
    drawn in that color, which lets it animate or sit on a known background.
    """
    R = size / 2.0
    cx, cy = x + R, y + R
    h = size * 0.66
    w = h * ASPECT
    # Optical centering: Maine is heavy at the top right, so nudge it left and down a touch.
    mx, my = cx - w / 2 - size * 0.012, cy - h / 2 + size * 0.012
    d, _ = maine_shape(mx, my, w, h, TOL, ROUND * h / 200)
    if land:
        return '<circle cx="%s" cy="%s" r="%s" fill="%s"/><path d="%s" fill="%s"/>' % (f(cx), f(cy), f(R), disc, d, land)
    _UID[0] += 1
    mid = "gmcut%d" % _UID[0]
    return ('<mask id="%s" maskUnits="userSpaceOnUse" x="%s" y="%s" width="%s" height="%s">'
            '<rect x="%s" y="%s" width="%s" height="%s" fill="#fff"/><path d="%s" fill="#000"/></mask>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s" mask="url(#%s)"/>' % (
                mid, f(x), f(y), f(size), f(size), f(x), f(y), f(size), f(size), d, f(cx), f(cy), f(R), disc, mid))


def fl_lockup_h(fg, disc, size=100):
    """Badge left, 'Generation Maine' right, all Instrument Sans. Returns (svg, w, h)."""
    sym = size * 1.12
    wm, ww = gm_wordmark(sym + size * 0.30, size * 0.82, size, fg)
    return badge(0, (size * 1.06 - sym) / 2, sym, disc) + wm, sym + size * 0.30 + ww, size * 1.06


def fl_lockup_stacked(fg, disc, size=100):
    d1, w1 = SANS.path("Generation", size, 0, 0, -18)
    d2, w2 = SANS.path("Maine", size, 0, 0, -18)
    W = max(w1, w2)
    sym = size * 1.6
    body = badge((W - sym) / 2, 0, sym, disc)
    y1 = sym + size * 1.0
    y2 = y1 + size * 0.98
    d1, _ = SANS.path("Generation", size, (W - w1) / 2, y1, -18)
    d2, _ = SANS.path("Maine", size, (W - w2) / 2, y2, -18)
    body += '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (fg, d1, fg, d2)
    return body, W, y2 + size * 0.26
