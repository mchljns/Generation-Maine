"""Pushing the line language further. Four experiments, each rendered on a real surface:

  text-room  : the field of lines makes room for words. Hero, cover, lower third
  grain-type : the wordmark and a headline drawn in the same horizontal lines as Maine
  voice      : lines that bend to a voice, a sample envelope for layout only
  mural-hero : the precise Maine mural as a website hero, with the headline in its room

Writes brand/identity/push/*.svg and a sheet. Motion lives in brand/identity/motion/.
  python3 brand/src/build_push.py
"""
import math
import re

from gmlib import write
from build_v4 import svg, rect, f
from build_v6 import C
from build_brand import DISPLAY, TRACK
from build_v4 import wordmark_one_line
import maine2

OUT = "brand/identity/push"
SP, BI, MG, PI, MOSS, SAGE, INK, STONE = C["spruce"], C["birch"], C["marigold"], C["pine"], C["moss"], C["sage"], C["ink"], C["stone"]
MPI = "An initiative of Maine Policy Institute"


def poly(pts, w, color, opacity=1.0):
    if len(pts) < 2:
        return ""
    op = "" if opacity >= 1 else ' opacity="%s"' % f(opacity)
    return '<path d="M%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" fill="none"%s/>' % (
        " L".join("%s %s" % (f(a), f(b)) for a, b in pts), color, f(w), op)


def glyphs(text, size, x, y, fill, face=DISPLAY, track=TRACK):
    d, w = face.path(text, size, x, y, track)
    return '<path fill="%s" d="%s"/>' % (fill, d), w


def label(x, y, s, size, fill, weight=600, anchor="start", upper=False, fam="Inter"):
    fams = {"Inter": "Inter,Arial,sans-serif", "Bric": "'Bricolage Grotesque',Arial,sans-serif"}
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" style="font-family:%s;font-weight:%d%s">%s</text>'
            % (f(x), f(y), f(size), fill, anchor, fams[fam], weight, ";text-transform:uppercase;letter-spacing:.08em" if upper else "", s))


# ------------------------------------------------------------------ the field, generalised
def smooth(vals, k):
    if k <= 0:
        return vals
    n = len(vals)
    out = []
    for i in range(n):
        acc = wsum = 0.0
        for j in range(max(0, i - 3 * k), min(n, i + 3 * k + 1)):
            wt = math.exp(-((j - i) / k) ** 2 / 2)
            acc += vals[j] * wt; wsum += wt
        out.append(acc / wsum)
    return out


def field(x, y, w, h, n, obstacles, clear, line, gold, w_lo, w_hi, steps=240, gold_on=None, pad=0, opacity=1.0, y_from=None, y_to=None, mode="wrap"):
    """Horizontal lines across a box that make room for obstacles.
    obstacles: list of ("rect", x0, y0, x1, y1, gold_ok) or ("circle", cx, cy, r, gold_ok).
    A line that is pushed turns gold where it bends, if the obstacle allows gold."""
    out = ""
    ya = y + pad if y_from is None else y_from
    yb = y + h - pad if y_to is None else y_to
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        y0 = ya + (yb - ya) * t
        lw = w_lo + (w_hi - w_lo) * t
        xs = [x + pad + (w - 2 * pad) * k / steps for k in range(steps + 1)]
        ys, gold_ok_at, cut = [], [], []
        for px in xs:
            py = y0
            gk = False
            best = 0
            broken = False
            for ob in obstacles:
                if ob[0] == "rect":
                    _, x0, y0r, x1, y1r, ok = ob
                    dx = 0 if x0 <= px <= x1 else (x0 - px if px < x0 else px - x1)
                    if dx >= clear:
                        continue
                    hh = math.sqrt(clear * clear - dx * dx)
                    top, bot = y0r - hh, y1r + hh
                    if top < y0 < bot and mode == "gap":
                        broken = True
                    elif top < y0 < bot:
                        cand = top if (y0 - top) < (bot - y0) else bot
                        if abs(cand - y0) > best:
                            best, py, gk = abs(cand - y0), cand, ok
                    else:
                        # the neighbours bow away, and in gap mode the nearest ones turn gold
                        gap = min(abs(y0 - top), abs(y0 - bot))
                        k_bow = 0.55 if mode == "gap" else 0.22
                        bow = k_bow * clear * math.exp(-((gap) / (0.7 * clear)) ** 2)
                        if bow > best and bow > 0.02 * clear:
                            best, py = bow, (y0 - bow if y0 <= top else y0 + bow)
                            gk = ok and mode == "gap" and gap < clear * 0.9
                else:
                    _, cx, cy, r, ok = ob
                    R = r + clear
                    dx = px - cx
                    if abs(dx) >= R * 1.6:
                        continue
                    dy0 = y0 - cy
                    ady = abs(dy0)
                    sign = 1 if dy0 >= 0 else -1
                    if ady < R:
                        amp, sig = R - ady, R * 0.75
                    else:
                        amp, sig = 0.42 * R * math.exp(-((ady - R) / (0.55 * R)) ** 2), R * 0.95
                    off = amp * math.exp(-(dx / sig) ** 2)
                    if ady < R and abs(dx) < R:
                        off = max(off, math.sqrt(R * R - dx * dx) - ady)
                    if off > best:
                        best, py, gk = off, y0 + sign * off, ok and ady < R
            ys.append(py); gold_ok_at.append(gk); cut.append(broken)
        ys = smooth(ys, max(2, int(steps * clear / (w - 2 * pad) * 0.5)))
        # colour by displacement, and break the line where it is cut
        run, is_gold = [], None
        for px, py, gk, br in zip(xs, ys, gold_ok_at, cut):
            if br:
                out += poly(run, lw, gold if is_gold else line, opacity); run, is_gold = [], None
                continue
            g = gk and abs(py - y0) > (0.3 if mode == "wrap" else 0.18) * clear
            if is_gold is None or g == is_gold:
                run.append((px, py))
            else:
                out += poly(run, lw, gold if is_gold else line, opacity); run = [run[-1], (px, py)]
            is_gold = g
        out += poly(run, lw, gold if is_gold else line, opacity)
    return out


# ------------------------------------------------------------------ 1. text is the room
def hero_text_room(W=1200, H=680):
    b = rect(0, 0, W, H, SP)
    wm, ww, wh = wordmark_one_line(BI, BI, "circle", 100)   # no dot: the mark is elsewhere on the page
    b += '<g transform="translate(56 26) scale(.26)">%s</g>' % wm
    for i, s in enumerate(["About", "Creators", "Follow"]):
        b += label(W - 56 - (2 - i) * 110, 47, s, 15, BI, anchor="end")
    b += label(56, 80, MPI, 12, SAGE, weight=500)
    # headline, three lines, low left
    size = 104
    lines = ["Young Mainers", "on building a", "life here."]
    x0, base0, lead = 56, 372, size * 0.9
    tx = ""
    maxw = 0
    for i, s in enumerate(lines):
        g, tw = glyphs(s, size, x0, base0 + i * lead, BI)
        tx += g; maxw = max(maxw, tw)
    top = base0 - size * 0.7
    bot = base0 + 2 * lead + size * 0.2
    # lede and buttons, right
    lx = 780
    lede = ["Short videos by young Maine creators", "about the rules that shape their lives."]
    for i, s in enumerate(lede):
        b_ = label(lx, 470 + i * 26, s, 17, BI, weight=400)
        tx += b_
    tx += rect(lx, 520, 190, 50, BI, 3) + label(lx + 95, 552, "Meet the creators", 16, INK, weight=700, anchor="middle")
    tx += '<rect x="%s" y="520" width="150" height="50" rx="3" fill="none" stroke="%s" stroke-width="1.5"/>' % (lx + 206, SAGE) + label(lx + 281, 552, "Follow along", 16, BI, weight=700, anchor="middle")
    obstacles = [("rect", x0, top, x0 + maxw, bot, True), ("rect", lx - 6, 452, lx + 366, 572, False)]
    b += field(0, 0, W, H, 26, obstacles, 30, MOSS, MG, 1.6, 3.4, steps=300, pad=0, y_from=118, y_to=H - 16, mode="gap")
    b += tx
    return svg(W, H, b, "Website hero, the field makes room for the words")


def cover_text_room(W=360, H=480, bg=PI, line=MOSS, title=("Two", "jobs."), name="[Creator name]", town="Belfast"):
    b = rect(0, 0, W, H, bg)
    size = 56
    x0, base0, lead = 24, H - 24 - size * 0.9 * (len(title) - 1) - 6, size * 0.92
    tx = ""; maxw = 0
    for i, s in enumerate(title):
        g, tw = glyphs(s, size, x0, base0 + i * lead, BI)
        tx += g; maxw = max(maxw, tw)
    top = base0 - size * 0.7
    bot = base0 + (len(title) - 1) * lead + size * 0.14
    tx += label(24, 40, name, 11, BI, weight=600) + label(24, 56, "%s, Maine" % town, 11, BI, weight=400)
    obstacles = [("rect", x0 - 4, top, x0 + maxw + 4, bot, True)]
    b += field(0, 0, W, H, 19, obstacles, 16, line, MG, 1.4, 3.2, steps=200, y_from=76, y_to=H - 12, mode="gap")
    b += tx
    return svg(W, H, b, "Cover, the field makes room for the title")


def lower_third(W=360, H=640):
    b = rect(0, 0, W, H, "#56625B")
    b += label(W / 2, H * 0.46, "Creator footage", 11, "rgba(255,255,255,.28)", weight=600, anchor="middle", upper=True)
    # the band of lines sits on the safe line, 30 percent up from the bottom
    band_top, band_bot = H * 0.62, H * 0.76
    tx = ""
    g1, w1 = glyphs("[Creator name]", 22, 20, band_top + 48, "#FFFFFF")
    tx += g1 + label(20, band_top + 70, "Skowhegan, Maine", 12, "#FFFFFF", weight=500)
    obstacles = [("rect", 20, band_top + 30, 20 + max(w1, 150), band_top + 76, True)]
    b += field(0, 0, W * 0.72, H, 7, obstacles, 12, "rgba(255,255,255,.9)", MG, 2.2, 3.6, steps=180, y_from=band_top, y_to=band_bot, pad=0)
    b += tx
    # the platform's chrome, so we see what it covers
    b += rect(0, H - 48, W, 48, "#000")
    for i in range(5):
        b += rect(28 + i * 72, H - 34, 20 if i != 2 else 36, 20, "#666" if i != 2 else "#fff", 5)
    b += label(12, H - 78, "@creator.handle", 13, "#fff", weight=700) + label(12, H - 60, "[Caption from the creator]", 13, "#fff", weight=400)
    return svg(W, H, b, "Lower third, the band makes room for the name")


# ------------------------------------------------------------------ 2. type in grain
def flatten(d):
    """fontTools SVG path data to a list of rings (polygons)."""
    toks = re.findall(r"[MLQCZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    rings, cur, i = [], [], 0
    pos = (0, 0)
    while i < len(toks):
        c = toks[i]; i += 1
        if c == "M":
            if len(cur) > 2: rings.append(cur)
            pos = (float(toks[i]), float(toks[i + 1])); i += 2; cur = [pos]
        elif c == "L":
            pos = (float(toks[i]), float(toks[i + 1])); i += 2; cur.append(pos)
        elif c == "Q":
            c1 = (float(toks[i]), float(toks[i + 1])); p = (float(toks[i + 2]), float(toks[i + 3])); i += 4
            for k in range(1, 9):
                t = k / 8
                cur.append(((1 - t) ** 2 * pos[0] + 2 * (1 - t) * t * c1[0] + t * t * p[0], (1 - t) ** 2 * pos[1] + 2 * (1 - t) * t * c1[1] + t * t * p[1]))
            pos = p
        elif c == "C":
            c1 = (float(toks[i]), float(toks[i + 1])); c2 = (float(toks[i + 2]), float(toks[i + 3])); p = (float(toks[i + 4]), float(toks[i + 5])); i += 6
            for k in range(1, 9):
                t = k / 8
                cur.append(((1 - t) ** 3 * pos[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * p[0],
                            (1 - t) ** 3 * pos[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * p[1]))
            pos = p
        elif c == "Z":
            if len(cur) > 2: rings.append(cur)
            cur = []
    if len(cur) > 2: rings.append(cur)
    return rings


def crossings(rings, py):
    xs = []
    for ring in rings:
        n = len(ring)
        for i in range(n):
            (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
            if (y0 <= py < y1) or (y1 <= py < y0):
                xs.append(x0 + (py - y0) / (y1 - y0) * (x1 - x0))
    xs.sort()
    return xs


def grain_text(text, size, x, y, n, fg, gold, w_lo, w_hi, face=DISPLAY, track=TRACK, gold_widest=True):
    d, w = face.path(text, size, x, y, track)
    rings = flatten(d)
    top = y - size * 0.72
    bot = y + size * 0.22
    rows = []
    for i in range(n):
        t = i / (n - 1)
        y0 = top + (bot - top) * t
        lw = w_lo + (w_hi - w_lo) * t
        xs = crossings(rings, y0)
        runs = [(a + lw / 2, b - lw / 2) for a, b in zip(xs[0::2], xs[1::2]) if b - a > lw * 1.2]
        rows.append((y0, lw, runs))
    widest = max(range(n), key=lambda i: sum(b - a for a, b in rows[i][2])) if gold_widest else -1
    out = ""
    for i, (y0, lw, runs) in enumerate(rows):
        col = gold if i == widest else fg
        for a, b in runs:
            out += poly([(a, y0), (b, y0)], lw, col)
    return out, w


def grain_wordmark(W=1200, H=300):
    b = rect(0, 0, W, H, BI)
    body, w = grain_text("Generation Maine", 150, 0, 0, 44, SP, MG, 1.2, 2.6)
    b += '<g transform="translate(%s 175)">%s</g>' % (f((W - w) / 2), body)
    return svg(W, H, b, "The wordmark drawn in grain")


def grain_cover(W=360, H=480):
    b = rect(0, 0, W, H, SP)
    body, w = grain_text("Winter", 78, 0, 0, 30, BI, MG, 0.9, 1.6)
    body2, w2 = grain_text("work.", 78, 0, 0, 30, BI, MG, 0.9, 1.6, gold_widest=False)
    b += '<g transform="translate(24 %s)">%s</g><g transform="translate(24 %s)">%s</g>' % (H - 96, body, H - 24, body2)
    b += label(24, 40, "[Creator name]", 11, BI, weight=600) + label(24, 56, "Fort Kent, Maine", 11, BI, weight=400)
    return svg(W, H, b, "A cover title drawn in grain")


# ------------------------------------------------------------------ 3. a voice
def voice_band(W=1200, H=300):
    """Lines that bend to a voice. The envelope here is made up for layout: the real one comes
    from the creator's audio."""
    b = rect(0, 0, W, H, PI)
    n = 15
    import random
    rnd = random.Random(7)
    env = [0.0] * 401
    # a sample envelope: bursts like speech, for layout only
    for start, length, amp in [(20, 40, .6), (70, 30, .9), (110, 60, .7), (190, 25, 1.0), (225, 50, .5), (300, 70, .8)]:
        for k in range(start, min(400, start + length)):
            tt = (k - start) / length
            env[k] = max(env[k], amp * math.sin(math.pi * tt) * (0.7 + 0.3 * rnd.random()))
    env = smooth(env, 3)
    cy = H * 0.5
    for i in range(n):
        t = i / (n - 1)
        y0 = 24 + (H - 48) * t
        lw = 1.6 + 3.2 * t
        d0 = abs(y0 - cy) / (H * 0.5)
        pts = []
        for k in range(401):
            px = 40 + (W - 80) * k / 400
            sign = 1 if y0 >= cy else -1
            push = env[k] * (H * 0.34) * max(0, 1 - d0) ** 1.5
            pts.append((px, y0 + sign * push * (1 - d0 * 0.4)))
        # gold where the push is large
        run, g0 = [], None
        for (px, py), e in zip(pts, env):
            g = e > 0.55 and abs(py - y0) > 6
            if g0 is None or g == g0:
                run.append((px, py))
            else:
                b += poly(run, lw, MG if g0 else SAGE); run = [run[-1], (px, py)]
            g0 = g
        b += poly(run, lw, MG if g0 else SAGE)
    b += label(40, H - 14, "Sample envelope for layout only. The real one comes from the creator's audio.", 11, STONE, weight=500)
    return svg(W, H, b, "Lines that bend to a voice")


# ------------------------------------------------------------------ 4. the mural as a hero
def mural_hero(W=1200, H=680):
    b = rect(0, 0, W, H, SP)
    wm, ww, wh = wordmark_one_line(BI, BI, "circle", 100)
    b += '<g transform="translate(56 26) scale(.26)">%s</g>' % wm
    for i, s in enumerate(["About", "Creators", "Follow"]):
        b += label(W - 56 - (2 - i) * 110, 47, s, 15, BI, anchor="end")
    b += label(56, 80, MPI, 12, SAGE, weight=500)
    # Maine in fine lines, right of centre, bleeding off the top and bottom
    ring = maine2.fit(560, -40, 720, 760)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    n = 64
    rows = []
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.01 + 0.98 * t)
        lw = 1.4 + 3.4 * t
        xs = maine2.crossings(ring, y0)
        runs = [(a + lw / 2, b_ - lw / 2) for a, b_ in zip(xs[0::2], xs[1::2]) if b_ - a > lw * 1.6]
        rows.append((y0, lw, runs))
    widest = max(range(n), key=lambda i: sum(b_ - a for a, b_ in rows[i][2]))
    for i, (y0, lw, runs) in enumerate(rows):
        if y0 < 104 or y0 > H - 12:
            continue
        col = MG if i == widest else MOSS
        for a, b_ in runs:
            b += poly([(a, y0), (b_, y0)], lw, col)
    size = 96
    lines = ["Young Mainers", "on building a", "life here."]
    x0, base0, lead = 56, 400, size * 0.9
    for i, s in enumerate(lines):
        g, tw = glyphs(s, size, x0, base0 + i * lead, BI)
        b += g
    return svg(W, H, b, "The mural as a hero")


def build():
    m = {"hero-text-room": hero_text_room(), "cover-text-room": cover_text_room(), "cover-text-room-2": cover_text_room(bg=SP, title=("Finding a", "place."), town="Rumford"),
         "lower-third": lower_third(), "grain-wordmark": grain_wordmark(), "grain-cover": grain_cover(), "voice": voice_band(), "mural-hero": mural_hero()}
    for k, v in m.items():
        write("%s/%s.svg" % (OUT, k), v)
    return m


if __name__ == "__main__":
    print("push:", list(build()))
