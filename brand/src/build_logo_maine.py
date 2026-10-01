"""The Maine logo: the state drawn in horizontal lines from the precise Census outline.

The state is one color. Marigold is the dot on the i, and only there (client decision, October 1).

Three cuts, one drawing, chosen by size:
  full   : 16 lines, one for each county, weight from 2.6 to 4.4 percent of the height. 72 px and up
  mid    : the same 16 lines, heavier, on a lightly simplified coast. 36 to 72 px. The cut the horizontal lockups ship with
  solid  : the silhouette alone, simplified so the edge stays clean. Below 36 px

  python3 brand/src/build_logo_maine.py     # writes brand/identity/logo-maine/*.svg
"""
import math

from gmlib import Face, write
from build_v4 import svg, rect, f, wordmark_one_line, wordmark_stacked
from build_v6 import C
import maine2
from maine import _dp


def simplified(ring, tol):
    """Douglas-Peucker on a closed ring, tolerance in the ring's own units."""
    far = max(range(len(ring)), key=lambda i: math.hypot(ring[i][0] - ring[0][0], ring[i][1] - ring[0][1]))
    pts = _dp(ring[: far + 1], tol)[:-1] + _dp(ring[far:] + [ring[0]], tol)
    return pts[:-1]

OUT = "brand/identity/logo-maine"
SP, BI, MG, PI = C["spruce"], C["snow"], C["marigold"], C["pine"]
D = {"sky": "#CFE3F0", "bark": "#2B211C", "paper": "#FFFFFF", "clay": "#6B5A4E"}
MPI = "An initiative of Maine Policy Institute"
INTER = Face("Inter-SemiBold.ttf")
HEDVIG = Face("d/HedvigLettersSerif-24.ttf")
HEDVIG_SANS = Face("d/HedvigLettersSans-Regular.ttf")


def seg(x0, x1, y, w, color):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(x0), f(y), f(x1), f(y), color, f(w))


def maine_lines(x, y, h, fg, mark, cut="full", gold=True):
    """Maine fitted to height h, left edge at x, top at y. Returns (svg body, width)."""
    w_box = h * maine2.ASPECT
    ring = maine2.fit(x, y, w_box, h)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    if cut == "solid":
        ring = simplified(ring, h * 0.012)
        return '<path fill="%s" d="%s"/>' % (fg, maine2.path(ring)), maxx - minx
    if cut == "mid":
        ring = simplified(ring, h * 0.006)
    # Sixteen lines for Maine's sixteen counties. The first line sits at 3.4 percent of the height, where the
    # state is two separate pieces, each crossed once: the northwest tip at Estcourt Station and the hump over
    # the St. John valley. Each is drawn as a short pill 2.2 line weights long, so the two points match. Higher up the hump
    # is still two tiny pieces and the points draw on top of each other.
    n, w_lo, w_hi, keep, top, span = (16, h * 0.026, h * 0.044, 1.8, 0.034, 0.936) if cut == "full" else (16, h * 0.034, h * 0.046, 2.2, 0.034, 0.936)
    rows = []
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (top + span * t)
        w = w_lo + (w_hi - w_lo) * t
        xs = maine2.crossings(ring, y0)
        runs = []
        for a, b in zip(xs[0::2], xs[1::2]):
            if i == 0:
                # the two points at the top are drawn as two equal short pills, 2.2 line weights long, so the top reads as two matching points
                c = (a + b) / 2
                runs.append((c - w * 0.6, c + w * 0.6))
            elif b - a >= w * keep:
                runs.append((a + w / 2, b - w / 2))
        rows.append((y0, w, runs))
    widest = max(range(n), key=lambda i: sum(b - a for a, b in rows[i][2]))
    out = ""
    for i, (y0, w, runs) in enumerate(rows):
        col = mark if (gold and i == widest) else fg
        for a, b in runs:
            out += seg(a, b, y0, w, col)
    return out, maxx - minx


def outlined(face, text, size, x, y, fill, anchor="start"):
    d, w = face.path(text, size, x, y, 0)
    if anchor == "middle":
        d, w = face.path(text, size, x - w / 2, y, 0)
    return '<path fill="%s" d="%s"/>' % (fill, d), w


def signature():
    """Signature set under the October 1 rule: the state is one color, Marigold is the dot on the i."""
    m = {}
    for cut in ("full", "mid", "solid"):
        body, w = maine_lines(0, 0, 240, SP, SP, cut, gold=False)
        m["mark-" + cut] = svg(w, 240, body, "Generation Maine")
        body, w = maine_lines(0, 0, 240, BI, BI, cut, gold=False)
        m["mark-%s-reversed" % cut] = svg(w, 240, body, "Generation Maine")
    body, w = maine_lines(0, 0, 240, "#000000", "#000000", "full", gold=False)
    m["mark-full-black"] = svg(w, 240, body, "Generation Maine")
    body, w = maine_lines(0, 0, 240, "#FFFFFF", "#FFFFFF", "full", gold=False)
    m["mark-full-white"] = svg(w, 240, body, "Generation Maine")
    for suf, fg in (("", SP), ("-reversed", BI)):
        b, w, h = wordmark_one_line(fg, MG, "circle", 100)
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        b2, w2, h2 = wordmark_stacked(fg, MG, "circle", 100)
        m["wordmark-stacked" + suf] = svg(w2, h2, b2, "Generation Maine")
    # lockups. The dot stays Marigold in every color version. Mono, black and white carry no second color.
    for suf, fg, mk in (("", SP, MG), ("-reversed", BI, MG), ("-mono", SP, SP), ("-black", "#000000", "#000000"), ("-white", "#FFFFFF", "#FFFFFF")):
        cut = "full"
        b, w, h = wordmark_one_line(fg, mk, "circle", 100)
        b2, w2, h2 = wordmark_stacked(fg, mk, "circle", 100)
        mh, gap = 96, 26
        # horizontal: the state stands taller than the capitals, like a flag beside the name.
        # The mark is small in this lockup, so it ships with the mid cut. The large version carries the full cut, for 600 px wide and up. The solid version is for under 300 px wide.
        RISE = mh - 74 - 6   # the state stands 16 units above the wordmark box, so every file includes that room
        for lsuf, lcut in (("", "mid"), ("-large", "full"), ("-solid", "solid")):
            mb, mw = maine_lines(0, 74 - mh + 6 + RISE, mh, fg, fg, lcut, gold=False)
            m["lockup-horizontal" + lsuf + suf] = svg(w + mw + gap, h + RISE, mb + '<g transform="translate(%s %s)">%s</g>' % (f(mw + gap), f(RISE), b), "Generation Maine")
            body = mb + '<g transform="translate(%s %s)">%s</g>' % (f(mw + gap), f(RISE), b) + rect(mw + gap, RISE + h + 22, w, 2, fg)
            t, _ = outlined(INTER, MPI, 27, mw + gap, RISE + h + 60, fg)
            m["lockup-endorsed" + lsuf + suf] = svg(w + mw + gap, RISE + h + 72, body + t, "Generation Maine, an initiative of Maine Policy Institute")
        mb, mw = maine_lines(0, 74 - mh + 6 + RISE, mh, fg, fg, "mid", gold=False)
        # horizontal, state after the name
        m["lockup-horizontal-right" + suf] = svg(w + mw + gap, h + RISE, '<g transform="translate(0 %s)">%s</g>' % (f(RISE), b) + '<g transform="translate(%s 0)">%s</g>' % (f(w + gap), mb), "Generation Maine")
        # compact: the state sits inside the cap height, for bylines and tight bars
        ch, cgap = 66, 20
        mb, cw = maine_lines(0, 74 - ch, ch, fg, fg, "mid", gold=False)
        m["lockup-compact" + suf] = svg(w + cw + cgap, h, mb + '<g transform="translate(%s 0)">%s</g>' % (f(cw + cgap), b), "Generation Maine")
        # stacked left: the state over the two-line name
        ms = 170
        mb, mw = maine_lines(0, 0, ms, fg, fg, cut, gold=False)
        m["lockup-stacked" + suf] = svg(max(w2, mw), ms + 30 + h2, mb + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 30), b2), "Generation Maine")
        # stacked centered: the state over the one-line name
        mb, mw = maine_lines((w - ms * maine2.ASPECT) / 2, 0, ms, fg, fg, cut, gold=False)
        m["lockup-stacked-centered" + suf] = svg(w, ms + 34 + h, mb + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 34), b), "Generation Maine")
        # two-line: the state beside the two-line name, as tall as both lines
        th = 150
        mb, mw = maine_lines(0, 8, th, fg, fg, cut, gold=False)
        m["lockup-two-line" + suf] = svg(mw + 30 + w2, h2, mb + '<g transform="translate(%s 0)">%s</g>' % (f(mw + 30), b2), "Generation Maine")
        # endorsed stacked, centered, for the narrow end card and print
        mb, mw = maine_lines((w - ms * maine2.ASPECT) / 2, 0, ms, fg, fg, cut, gold=False)
        body = mb + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 34), b) + rect(0, ms + 34 + h + 18, w, 2, fg)
        t, _ = outlined(INTER, MPI, 27, w / 2, ms + 34 + h + 56, fg, anchor="middle")
        m["lockup-endorsed-stacked" + suf] = svg(w, ms + 34 + h + 70, body + t, "Generation Maine, an initiative of Maine Policy Institute")
    # avatars by size, favicon solid. No Marigold in the mark alone.
    for name, cut, fg, bg in (("avatar-full", "full", BI, SP), ("avatar-mid", "mid", BI, SP), ("avatar-solid", "solid", BI, SP), ("avatar-birch", "mid", SP, C["birch"])):
        mb, mw = maine_lines(0, 0, 164, fg, fg, cut, gold=False)
        m[name] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % bg + '<g transform="translate(%s 38)">%s</g>' % (f((240 - mw) / 2), mb), "Generation Maine")
    mb, mw = maine_lines(0, 0, 150, BI, BI, "mid", gold=False); m["app-icon"] = svg(240, 240, rect(0, 0, 240, 240, SP, 52) + '<g transform="translate(%s 45)">%s</g>' % (f((240 - mw) / 2), mb), "Generation Maine")
    mb, mw = maine_lines(0, 0, 20, BI, BI, "solid"); m["favicon"] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="%s"/>' % SP + '<g transform="translate(%s 6)">%s</g>' % (f((32 - mw) / 2), mb), "Generation Maine")
    # the video bug: solid cut, Birch, with the name. The dot stays, the one Marigold in the frame.
    b, w, h = wordmark_one_line(BI, MG, "circle", 100)
    mb, mw = maine_lines(0, 0, 96, BI, BI, "solid", gold=False)
    m["bug"] = svg(w + mw + 26, h + 16, mb + '<g transform="translate(%s 16)">%s</g>' % (f(mw + 26), b), "Generation Maine")
    return m


def bark_sky():
    m = {}
    bk, sk, pa, cl = D["bark"], D["sky"], D["paper"], D["clay"]
    for cut in ("full", "mid", "solid"):
        body, w = maine_lines(0, 0, 240, bk, bk, cut, gold=False); m["mark-" + cut] = svg(w, 240, body, "Generation Maine")
        body, w = maine_lines(0, 0, 240, sk, sk, cut, gold=False); m["mark-%s-reversed" % cut] = svg(w, 240, body, "Generation Maine")

    def wm(fg):
        d, w = HEDVIG.path("generation maine", 100, 0, 78, -8)
        return '<path fill="%s" d="%s"/>' % (fg, d), w, 100
    for suf, fg, mk in (("", bk, cl), ("-reversed", sk, pa)):
        b, w, h = wm(fg)
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        mh = 100
        mb, mw = maine_lines(0, 0, mh, fg, fg, "mid", gold=False)
        m["lockup-horizontal" + suf] = svg(w + mw + 28, h + 14, mb + '<g transform="translate(%s 14)">%s</g>' % (f(mw + 28), b), "Generation Maine")
        ms = 180
        mb, mw = maine_lines((w - ms * maine2.ASPECT) / 2, 0, ms, fg, fg, "full", gold=False)
        m["lockup-stacked" + suf] = svg(w, ms + 34 + h, mb + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 34), b), "Generation Maine")
        body = mb + '<g transform="translate(0 %s)">%s</g>' % (f(ms + 34), b) + rect(0, ms + 34 + h + 12, w, 1.5, fg)
        t, _ = outlined(HEDVIG_SANS, MPI, 24, w / 2, ms + 34 + h + 48, fg, anchor="middle")
        m["lockup-endorsed" + suf] = svg(w, ms + 34 + h + 62, body + t, "Generation Maine, an initiative of Maine Policy Institute")
    mb, mw = maine_lines(0, 0, 164, sk, sk, "mid", gold=False); m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % bk + '<g transform="translate(%s 38)">%s</g>' % (f((240 - mw) / 2), mb), "Generation Maine")
    mb, mw = maine_lines(0, 0, 164, bk, bk, "mid", gold=False); m["avatar-sky"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % sk + '<g transform="translate(%s 38)">%s</g>' % (f((240 - mw) / 2), mb), "Generation Maine")
    mb, mw = maine_lines(0, 0, 20, sk, sk, "solid"); m["favicon"] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="%s"/>' % bk + '<g transform="translate(%s 6)">%s</g>' % (f((32 - mw) / 2), mb), "Generation Maine")
    return m


def build():
    s, b = signature(), bark_sky()
    for k, v in s.items():
        write("%s/signature/%s.svg" % (OUT, k), v)
    for k, v in b.items():
        write("%s/bark-sky/%s.svg" % (OUT, k), v)
    return s, b


if __name__ == "__main__":
    s, b = build()
    print("signature:", len(s), "bark-sky:", len(b))
