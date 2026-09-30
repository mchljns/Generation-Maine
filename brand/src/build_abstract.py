"""Abstract brandmark candidates, built from one atom: the dot.

Every mark is generated from a construction rule, so it has a full version with real intricacy and
a reduced version for small sizes that follows the same rule with fewer parts. No letters, no
pictures. Each is described in one sentence that does not restate the name or the brief.

  python3 brand/src/build_abstract.py     # writes brand/identity/abstract/<key>/*.svg
"""
import math

from gmlib import write
from build_v4 import svg, rect, f
from build_v6 import C

OUT = "brand/identity/abstract"
SP, BI, MG, PI = C["spruce"], C["birch"], C["marigold"], C["pine"]
ANCHOR = (0.30, 0.70)   # the low-left anchor every headline uses, as a fraction of the box


def dot(cx, cy, r, fill):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), fill)


def polyline(pts, stroke, w, opacity=1):
    d = "M" + " L".join("%s %s" % (f(x), f(y)) for x, y in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"%s/>' % (
        d, stroke, f(w), (' opacity="%s"' % f(opacity)) if opacity < 1 else "")


# ------------------------------------------------------------------ 1. Hex: a circle made of dots
def hex_points(rings):
    pts = [(0, 0)]
    for k in range(1, rings + 1):
        for side in range(6):
            a0 = math.radians(60 * side)
            a1 = math.radians(60 * (side + 1))
            for t in range(k):
                x = k * math.cos(a0) + t * (math.cos(a1) - math.cos(a0))
                y = k * math.sin(a0) + t * (math.sin(a1) - math.sin(a0))
                pts.append((x, y))
    return pts


def mark_hex(x, y, s, fg, mark, small=False):
    """A circle made of dots, one of them Marigold. Reduces to seven dots, then to one."""
    rings = 2 if small else 4
    pitch = s / (2 * rings + 1.2)
    r = pitch * 0.36
    cx, cy = x + s / 2, y + s / 2
    out = ""
    pts = hex_points(rings)
    # the Marigold dot sits low left, on the ring next to the edge
    target = (-(rings - 1) * math.cos(math.radians(60)) - (rings - 1) * 0.5 * 0, (rings - 1) * math.sin(math.radians(60)))
    best = min(pts, key=lambda p: (p[0] - (-(rings - 1) * 0.5)) ** 2 + (p[1] - (rings - 1) * 0.866) ** 2)
    for px, py in pts:
        fill = mark if (px, py) == best else fg
        out += dot(cx + px * pitch, cy + py * pitch, r * (1.25 if fill == mark else 1), fill)
    return out


# ------------------------------------------------------------------ 2. Bend: lines that make room
def mark_bend(x, y, s, fg, mark, small=False):
    """Horizontal lines that bend around one dot. The field makes room for the person."""
    n = 6 if small else 13
    cx, cy = x + ANCHOR[0] * s, y + ANCHOR[1] * s
    rd = s * (0.11 if small else 0.085)
    clear = rd * 1.9
    out = ""
    w = s * (0.055 if small else 0.028)
    pad = s * 0.06
    for i in range(n):
        y0 = y + pad + (s - 2 * pad) * i / (n - 1)
        pts = []
        steps = 64
        for k in range(steps + 1):
            px = x + pad + (s - 2 * pad) * k / steps
            dx = px - cx
            dy0 = y0 - cy
            dist = math.hypot(dx, dy0)
            if dist < clear * 1.6:
                # push the line out of a circle of radius clear, softly
                want = math.sqrt(max(clear * clear - dx * dx, 0)) if abs(dx) < clear else 0
                sign = 1 if dy0 >= 0 else -1
                py = cy + sign * max(abs(dy0), want) if abs(dx) < clear else y0
                # blend back to y0 with distance so the bend has shoulders
                blend = max(0, min(1, (dist - clear) / (clear * 0.6)))
                py = py * (1 - blend) + y0 * blend
            else:
                py = y0
            pts.append((px, py))
        out += polyline(pts, fg, w)
    out += dot(cx, cy, rd, mark)
    return out


# ------------------------------------------------------------------ 3. Nest: fields within fields
def mark_nest(x, y, s, fg, mark, small=False):
    """Nested squares, each stepping toward the lower left, the dot in the last one."""
    n = 3 if small else 6
    w = s * (0.11 if small else 0.06)
    out = ""
    step = s * 0.115
    for i in range(n):
        side = s - i * 2 * step * 0.72
        sx = x + i * step * 0.35
        sy = y + (s - side) - i * step * 0.35
        half = w / 2
        out += ('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="%s"/>'
                % (f(sx + half), f(sy + half), f(side - w), f(side - w), fg, f(w)))
    last_side = s - (n - 1) * 2 * step * 0.72
    lx = x + (n - 1) * step * 0.35
    ly = y + (s - last_side) - (n - 1) * step * 0.35
    out += dot(lx + last_side * 0.5, ly + last_side * 0.5, last_side * 0.19, mark)
    return out


# ------------------------------------------------------------------ 4. Strips: a disc cut into strips
def mark_strips(x, y, s, fg, mark, small=False):
    """A disc cut into diagonal strips that slide apart. One strip is Marigold."""
    n = 5 if small else 11
    cx, cy = x + s / 2, y + s / 2
    R = s * 0.46
    gap = s * (0.05 if small else 0.028)
    out = ""
    total = 2 * R
    wdt = (total - gap * (n - 1)) / n
    # rotate the whole disc by 30 degrees, and slide alternate strips a little
    ang = -30
    out += '<g transform="rotate(%s %s %s)">' % (ang, f(cx), f(cy))
    for i in range(n):
        x0 = cx - R + i * (wdt + gap)
        x1 = x0 + wdt
        # clip strip to the circle: vertical extent at x0 and x1
        def h(px):
            d = abs(px - cx)
            return math.sqrt(max(R * R - d * d, 0))
        slide = (s * 0.035 if not small else s * 0.05) * (1 if i % 2 else -1) * (0 if i in (0, n - 1) else 1)
        # build the strip as the intersection of a vertical band with the circle, approximated by polygon
        pts = []
        steps = 12
        for k in range(steps + 1):
            px = x0 + (x1 - x0) * k / steps
            pts.append((px, cy - h(px) + slide))
        for k in range(steps, -1, -1):
            px = x0 + (x1 - x0) * k / steps
            pts.append((px, cy + h(px) + slide))
        fill = mark if i == (1 if small else 2) else fg
        d = "M" + " L".join("%s %s" % (f(a), f(b)) for a, b in pts) + " Z"
        out += '<path d="%s" fill="%s"/>' % (d, fill)
    out += "</g>"
    return out


# ------------------------------------------------------------------ 5. Threads: one line interrupted
def mark_threads(x, y, s, fg, mark, small=False):
    """Vertical lines, evenly set. One is interrupted by the dot."""
    n = 5 if small else 11
    pad = s * 0.08
    w = s * (0.07 if small else 0.034)
    cy = y + ANCHOR[1] * s
    rd = s * (0.12 if small else 0.075)
    out = ""
    k = 1 if small else 3   # which line the dot sits on
    for i in range(n):
        px = x + pad + (s - 2 * pad) * i / (n - 1)
        if i == k:
            out += polyline([(px, y + pad), (px, cy - rd * 1.6)], fg, w)
            out += polyline([(px, cy + rd * 1.6), (px, y + s - pad)], fg, w)
            out += dot(px, cy, rd, mark)
        else:
            out += polyline([(px, y + pad), (px, y + s - pad)], fg, w)
    return out


# ------------------------------------------------------------------ 6. Halftone: dots that gather
def mark_gather(x, y, s, fg, mark, small=False):
    """A lattice of dots that grow toward the lower left, until one is Marigold."""
    n = 4 if small else 8
    pad = s * 0.1
    ax, ay = x + pad, y + s - pad
    out = ""
    pitch = (s - 2 * pad) / (n - 1)
    maxd = math.hypot(s - 2 * pad, s - 2 * pad)
    for i in range(n):
        for j in range(n):
            px, py = x + pad + i * pitch, y + pad + j * pitch
            d = math.hypot(px - ax, py - ay) / maxd
            r = pitch * (0.08 + 0.36 * max(0.0, 1 - d) ** 1.6)
            if i == 0 and j == n - 1:
                out += dot(px, py, pitch * 0.46, mark)
            else:
                out += dot(px, py, r, fg)
    return out


# ------------------------------------------------------------------ Bend, refined
def bend_lines(x, y, s, fg, mark, n, w_lo, w_hi, clear_k, anchor=ANCHOR, clip_circle=False, pad_k=0.06, dot_k=0.085, fade=False):
    """Horizontal lines that bow around the dot. Lines inside the clearance are pushed out to
    touch it; lines just outside bow a little, so the field reacts as one surface."""
    cx, cy = x + anchor[0] * s, y + anchor[1] * s
    rd = s * dot_k
    clear = rd * clear_k
    pad = s * pad_k
    out = ""
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        w = w_lo + (w_hi - w_lo) * t
        dy0 = y0 - cy
        ady = abs(dy0)
        sign = 1 if dy0 >= 0 else -1
        if ady < clear:
            amp = clear - ady
            sig = clear * 0.75
        else:
            amp = 0.42 * clear * math.exp(-((ady - clear) / (0.55 * clear)) ** 2)
            sig = clear * 0.95
        pts = []
        steps = 72
        for k in range(steps + 1):
            px = x + pad + (s - 2 * pad) * k / steps
            dx = px - cx
            off = amp * math.exp(-(dx / sig) ** 2)
            # inside the clearance the line must hug the circle, not just a gaussian
            if ady < clear and abs(dx) < clear:
                need = math.sqrt(clear * clear - dx * dx) - ady
                off = max(off, need)
            py = y0 + sign * off
            if clip_circle:
                R = s / 2 - pad * 0.2
                ddx = px - (x + s / 2)
                if abs(ddx) > R:
                    continue
                lim = math.sqrt(R * R - ddx * ddx)
                if abs(py - (y + s / 2)) > lim:
                    continue
            pts.append((px, py))
        if len(pts) > 1:
            out += polyline(pts, fg, w, opacity=(0.45 + 0.55 * t) if fade else 1)
    out += dot(cx, cy, rd, mark)
    return out


def mark_bend2(x, y, s, fg, mark, small=False):
    """Bend, even weight, smooth shoulders."""
    if small:
        return bend_lines(x, y, s, fg, mark, 6, s * 0.052, s * 0.052, 1.75, dot_k=0.11)
    return bend_lines(x, y, s, fg, mark, 13, s * 0.03, s * 0.03, 1.8)


def mark_bend3(x, y, s, fg, mark, small=False):
    """Bend, weight grows toward the bottom, like type anchored low."""
    if small:
        return bend_lines(x, y, s, fg, mark, 6, s * 0.03, s * 0.075, 1.75, dot_k=0.11)
    return bend_lines(x, y, s, fg, mark, 15, s * 0.012, s * 0.05, 1.8)


def mark_bend4(x, y, s, fg, mark, small=False):
    """Bend, cut to a disc."""
    if small:
        return bend_lines(x, y, s, fg, mark, 7, s * 0.05, s * 0.05, 1.7, anchor=(0.36, 0.64), clip_circle=True, dot_k=0.105)
    return bend_lines(x, y, s, fg, mark, 15, s * 0.028, s * 0.028, 1.8, anchor=(0.36, 0.64), clip_circle=True)


def mark_bend5(x, y, s, fg, mark, small=False):
    """Bend, fine and many, the dot larger. The most intricate cut."""
    if small:
        return bend_lines(x, y, s, fg, mark, 6, s * 0.05, s * 0.05, 1.75, dot_k=0.11)
    return bend_lines(x, y, s, fg, mark, 21, s * 0.016, s * 0.022, 1.7, dot_k=0.1)


# ------------------------------------------------------------------ gold in the lines, not a dot
def mix(a, b, t):
    a = tuple(int(a[i:i + 2], 16) for i in (1, 3, 5)); b = tuple(int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bend_field(x, y, s, n, w_lo, w_hi, clear, anchor=ANCHOR, pad_k=0.06, steps=72):
    """Returns, for each line, its points and its per-point displacement as a fraction of clear."""
    cx, cy = x + anchor[0] * s, y + anchor[1] * s
    pad = s * pad_k
    lines = []
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        w = w_lo + (w_hi - w_lo) * t
        dy0 = y0 - cy
        ady = abs(dy0)
        sign = 1 if dy0 >= 0 else -1
        if ady < clear:
            amp, sig = clear - ady, clear * 0.75
        else:
            amp, sig = 0.42 * clear * math.exp(-((ady - clear) / (0.55 * clear)) ** 2), clear * 0.95
        pts, offs = [], []
        for k in range(steps + 1):
            px = x + pad + (s - 2 * pad) * k / steps
            dx = px - cx
            off = amp * math.exp(-(dx / sig) ** 2)
            if ady < clear and abs(dx) < clear:
                off = max(off, math.sqrt(clear * clear - dx * dx) - ady)
            pts.append((px, y0 + sign * off)); offs.append(off / clear)
        lines.append((pts, offs, w, amp / clear))
    return lines, (cx, cy)


def segments(pts, offs, w, color_of):
    """Draw a line as short segments, each colored by its displacement."""
    out = ""
    for i in range(len(pts) - 1):
        c = color_of((offs[i] + offs[i + 1]) / 2)
        out += polyline([pts[i], pts[i + 1]], c, w)
    return out


def mark_gold_soft(x, y, s, fg, mark, small=False):
    """Lines that turn gold where they bend. The room stays empty."""
    n, wl, wh = (6, s * 0.03, s * 0.075) if small else (15, s * 0.012, s * 0.05)
    clear = s * (0.19 if small else 0.15)
    lines, _ = bend_field(x, y, s, n, wl, wh, clear)
    out = ""
    for pts, offs, w, a in lines:
        if a < 0.04:
            out += polyline(pts, fg, w)
        else:
            out += segments(pts, offs, w, lambda o: mix(fg, mark, min(1, o * 1.6) ** 0.8))
    return out


def mark_gold_flat(x, y, s, fg, mark, small=False):
    """The same, in two flat colors. The bent part of each line is gold, the rest is Spruce."""
    n, wl, wh = (6, s * 0.03, s * 0.075) if small else (15, s * 0.012, s * 0.05)
    clear = s * (0.19 if small else 0.15)
    lines, _ = bend_field(x, y, s, n, wl, wh, clear)
    out = ""
    for pts, offs, w, a in lines:
        if a < 0.08:
            out += polyline(pts, fg, w); continue
        run, gold = [], None
        for p, o in zip(pts, offs):
            g = o > 0.12
            if gold is None or g == gold:
                run.append(p)
            else:
                out += polyline(run, mark if gold else fg, w); run = [run[-1], p]
            gold = g
        out += polyline(run, mark if gold else fg, w)
    return out


def mark_gold_line(x, y, s, fg, mark, small=False):
    """One line of the field is gold: the one that bends the most."""
    n, wl, wh = (6, s * 0.03, s * 0.075) if small else (15, s * 0.012, s * 0.05)
    clear = s * (0.19 if small else 0.15)
    lines, _ = bend_field(x, y, s, n, wl, wh, clear)
    top = max(range(len(lines)), key=lambda i: lines[i][3])
    return "".join(polyline(pts, mark if i == top else fg, w) for i, (pts, offs, w, a) in enumerate(lines))


def mark_gold_dash(x, y, s, fg, mark, small=False):
    """The lines make room for a short gold line: one voice among the others."""
    n, wl, wh = (6, s * 0.03, s * 0.075) if small else (15, s * 0.012, s * 0.05)
    clear = s * (0.17 if small else 0.14)
    lines, (cx, cy) = bend_field(x, y, s, n, wl, wh, clear)
    out = "".join(polyline(pts, fg, w) for pts, offs, w, a in lines)
    dw = s * (0.07 if small else 0.045)
    out += polyline([(cx - clear * 0.62, cy), (cx + clear * 0.62, cy)], mark, dw)
    return out


CANDIDATES = [
    ("gold-soft", "Gold where it bends, soft", mark_gold_soft, "Lines turn gold where they bend. The room stays empty for the person."),
    ("gold-flat", "Gold where it bends, flat", mark_gold_flat, "The same in two flat colors. The bent part is gold, the straight part is Spruce."),
    ("gold-line", "One gold line", mark_gold_line, "One line of the field is gold, the one that bends the most."),
    ("gold-dash", "Gold dash", mark_gold_dash, "The lines make room for a short gold line, one voice among the others."),
    ("bend3", "Bend with the dot", mark_bend3, "For comparison."),
]



def build():
    out = {}
    for key, name, fn, note in CANDIDATES:
        m = {}
        m["mark"] = svg(240, 240, fn(0, 0, 240, SP, MG), "Generation Maine")
        m["mark-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + fn(0, 0, 240, BI, MG), "Generation Maine")
        m["mark-mono"] = svg(240, 240, fn(0, 0, 240, SP, SP), "Generation Maine")
        m["mark-small"] = svg(240, 240, fn(0, 0, 240, SP, MG, small=True), "Generation Maine")
        m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + fn(40, 40, 160, BI, MG, small=True), "Generation Maine")
        m["avatar-full"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + fn(34, 34, 172, BI, MG), "Generation Maine")
        for k, v in m.items():
            write("%s/%s/%s.svg" % (OUT, key, k), v)
        out[key] = m
    return out


if __name__ == "__main__":
    print("abstract marks:", list(build()))
