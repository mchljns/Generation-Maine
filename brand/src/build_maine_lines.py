"""Bend lines meeting the silhouette of Maine. Three constructions:

  grain : Maine made of horizontal lines, the lines bending around the dot
  room  : a field of horizontal lines that flow around the shape of Maine, as if the shape displaced them
  gap   : a field of horizontal lines that stop at the shape, so Maine is the space the lines leave

The outline comes from Natural Earth (public domain) through maine.py, simplified hard so the
coast reads as a shape and not a map.

  python3 brand/src/build_maine_lines.py     # writes brand/identity/maine-lines/<key>/*.svg
"""
import math

from gmlib import write
from build_v4 import svg, rect, f
from build_v6 import C
import maine

OUT = "brand/identity/maine-lines"
SP, BI, MG, PI = C["spruce"], C["birch"], C["marigold"], C["pine"]


def dot(cx, cy, r, fill):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), fill)


def polyline(pts, stroke, w):
    if len(pts) < 2:
        return ""
    d = "M" + " L".join("%s %s" % (f(x), f(y)) for x, y in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (d, stroke, f(w))


def outline(x, y, w, h, tol):
    """Simplified mainland polygon fitted into the box, as a list of points."""
    s, ox, oy = maine._fit(x, y, w, h)
    M = maine._MAIN
    far = max(range(len(M)), key=lambda i: math.hypot(M[i][0] - M[0][0], M[i][1] - M[0][1]))
    pts = maine._dp(M[: far + 1], tol)[:-1] + maine._dp(M[far:] + [M[0]], tol)
    return [(ox + (px - maine._MINX) * s, oy + (py - maine._MINY) * s) for px, py in pts[:-1]]


def path_of(pts, fill, r=0):
    if r <= 0:
        return '<path fill="%s" d="M%sZ"/>' % (fill, " L".join("%s %s" % (f(a), f(b)) for a, b in pts))
    out = []
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def toward(a, b):
            L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
            dd = min(r, L / 2)
            return a[0] + (b[0] - a[0]) * dd / L, a[1] + (b[1] - a[1]) * dd / L
        a, b = toward(p1, p0), toward(p1, p2)
        out.append(("L" if out else "M") + "%s %s Q%s %s %s %s" % (f(a[0]), f(a[1]), f(p1[0]), f(p1[1]), f(b[0]), f(b[1])))
    return '<path fill="%s" d="%sZ"/>' % (fill, " ".join(out))


def vertical_hits(pts, px):
    """y values where the vertical line at px crosses the polygon, sorted."""
    ys = []
    n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        if (x0 <= px < x1) or (x1 <= px < x0):
            t = (px - x0) / (x1 - x0)
            ys.append(y0 + t * (y1 - y0))
    ys.sort()
    return ys


def inside_interval(ys, py):
    for i in range(0, len(ys) - 1, 2):
        if ys[i] <= py <= ys[i + 1]:
            return ys[i], ys[i + 1]
    return None


def smooth(vals, k):
    """Gaussian smoothing along a list, so bends have shoulders."""
    if k <= 0:
        return vals
    n = len(vals)
    out = []
    for i in range(n):
        acc, wsum = 0.0, 0.0
        for j in range(max(0, i - 3 * k), min(n, i + 3 * k + 1)):
            w = math.exp(-((j - i) / k) ** 2 / 2)
            acc += vals[j] * w
            wsum += w
        out.append(acc / wsum)
    return out


# ------------------------------------------------------------------ grain
def mark_grain(x, y, s, fg, mark, small=False, tol=0.05, dot_at="south"):
    """Maine drawn in horizontal lines. The lines bend around the dot."""
    n = 7 if small else 17
    w = s * (0.045 if small else 0.022)
    pts = outline(x + s * 0.12, y + s * 0.04, s * 0.76, s * 0.92, tol)
    # the dot: south sits low left inside the shape, centre sits in the middle, none draws no dot
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    if dot_at == "south":
        cx, cy = minx + (maxx - minx) * 0.30, miny + (maxy - miny) * 0.78
    else:
        cx, cy = minx + (maxx - minx) * 0.46, miny + (maxy - miny) * 0.52
    rd = s * (0.075 if small else 0.06)
    clear = rd * 1.8
    out = ""
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.04 + 0.92 * t)
        xs, ys = [], []
        steps = 90
        for k in range(steps + 1):
            px = minx + (maxx - minx) * k / steps
            dy0 = y0 - cy
            dx = px - cx
            ady = abs(dy0)
            sign = 1 if dy0 >= 0 else -1
            if ady < clear:
                amp, sig = clear - ady, clear * 0.75
            else:
                amp, sig = 0.42 * clear * math.exp(-((ady - clear) / (0.55 * clear)) ** 2), clear * 0.95
            off = amp * math.exp(-(dx / sig) ** 2)
            if ady < clear and abs(dx) < clear:
                off = max(off, math.sqrt(clear * clear - dx * dx) - ady)
            if dot_at == "none":
                off = 0
            xs.append(px); ys.append(y0 + sign * off)
        # keep only the parts inside the shape, as separate runs
        run = []
        for px, py in zip(xs, ys):
            hits = vertical_hits(pts, px)
            if inside_interval(hits, py):
                run.append((px, py))
            else:
                out += polyline(run, fg, w); run = []
        out += polyline(run, fg, w)
    if dot_at != "none":
        out += dot(cx, cy, rd, mark)
    return out


# ------------------------------------------------------------------ room
def mark_room(x, y, s, fg, mark, small=False, tol=0.08):
    """A field of lines that flow around the shape. The shape is the room the lines make."""
    n = 9 if small else 21
    w = s * (0.04 if small else 0.02)
    pad = s * 0.05
    pts = outline(x + s * 0.24, y + s * 0.1, s * 0.52, s * 0.8, tol)
    clear = s * (0.05 if small else 0.035)
    out = ""
    steps = 120
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        xs = [x + pad + (s - 2 * pad) * k / steps for k in range(steps + 1)]
        ys = []
        for px in xs:
            hits = vertical_hits(pts, px)
            iv = inside_interval(hits, y0)
            py = y0
            if iv:
                top, bot = iv
                # leave by the nearer edge
                py = (top - clear) if (y0 - top) < (bot - y0) else (bot + clear)
            else:
                # outside but close: keep a clearance from the edge
                for h in hits:
                    if abs(h - y0) < clear:
                        py = h - clear if y0 < h else h + clear
            ys.append(py)
        ys = smooth(ys, 5 if small else 7)
        out += polyline(list(zip(xs, ys)), fg, w)
    return out


# ------------------------------------------------------------------ gap
def mark_gap(x, y, s, fg, mark, small=False, tol=0.08):
    """A field of lines that stop at the shape. Maine is the space the lines leave."""
    n = 9 if small else 19
    w = s * (0.045 if small else 0.024)
    pad = s * 0.05
    pts = outline(x + s * 0.24, y + s * 0.08, s * 0.52, s * 0.84, tol)
    clear = s * (0.045 if small else 0.03)
    out = ""
    steps = 160
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        run = []
        for k in range(steps + 1):
            px = x + pad + (s - 2 * pad) * k / steps
            hits = vertical_hits(pts, px)
            blocked = inside_interval(hits, y0) is not None or any(abs(h - y0) < clear for h in hits)
            # also block a little horizontally so the ends do not touch the coast
            if not blocked:
                for ddx in (-clear, clear):
                    h2 = vertical_hits(pts, px + ddx)
                    if inside_interval(h2, y0) is not None:
                        blocked = True
            if blocked:
                out += polyline(run, fg, w); run = []
            else:
                run.append((px, y0))
        out += polyline(run, fg, w)
    return out


# ------------------------------------------------------------------ refined cuts
def mark_grain2(x, y, s, fg, mark, small=False):
    """Maine in lines, coast simplified, no scraps, weight growing toward the bottom."""
    n = 7 if small else 15
    pts = outline(x + s * 0.13, y + s * 0.05, s * 0.74, s * 0.9, 0.09)
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    out = ""
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.05 + 0.9 * t)
        w = s * ((0.03 + 0.03 * t) if small else (0.014 + 0.026 * t))
        hits = vertical_hits_h(pts, y0)
        for a, b in zip(hits[0::2], hits[1::2]):
            if b - a > s * 0.06:                       # drop scraps shorter than a dot
                out += polyline([(a + w / 2, y0), (b - w / 2, y0)], fg, w)
    return out


def vertical_hits_h(pts, py):
    """x values where the horizontal line at py crosses the polygon, sorted."""
    xs = []
    n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        if (y0 <= py < y1) or (y1 <= py < y0):
            t = (py - y0) / (y1 - y0)
            xs.append(x0 + t * (x1 - x0))
    xs.sort()
    return xs


def mark_room2(x, y, s, fg, mark, small=False):
    """Bend, with a small solid Maine where the dot was. The field makes room for the shape."""
    n = 6 if small else 15
    pad = s * 0.06
    sh = s * (0.34 if small else 0.3)
    sw = sh * maine.ASPECT
    ax, ay = x + s * 0.3 - sw / 2, y + s * 0.7 - sh / 2
    pts = outline(ax, ay, sw, sh, 0.12)
    clear = s * (0.05 if small else 0.035)
    out = ""
    steps = 120
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        w = s * ((0.03 + 0.045 * t) if small else (0.012 + 0.038 * t))
        xs = [x + pad + (s - 2 * pad) * k / steps for k in range(steps + 1)]
        ys = []
        for px in xs:
            hits = vertical_hits(pts, px)
            iv = inside_interval(hits, y0)
            py = y0
            if iv:
                top, bot = iv
                py = (top - clear) if (y0 - top) < (bot - y0) else (bot + clear)
            else:
                for h in hits:
                    if abs(h - y0) < clear:
                        py = h - clear if y0 < h else h + clear
            ys.append(py)
        ys = smooth(ys, 4 if small else 6)
        out += polyline(list(zip(xs, ys)), fg, w)
    out += path_of(pts, mark, r=s * 0.01)
    return out


# ------------------------------------------------------------------ gold in the mural
def mark_gap_gold(x, y, s, fg, mark, small=False, tol=0.08):
    """The field of lines that stop at the shape. Where a line meets the coast, its last stretch is gold."""
    n = 9 if small else 19
    w = s * (0.045 if small else 0.024)
    pad = s * 0.05
    pts = outline(x + s * 0.24, y + s * 0.08, s * 0.52, s * 0.84, tol)
    clear = s * (0.045 if small else 0.03)
    glow = s * (0.11 if small else 0.08)
    out = ""
    steps = 160
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        runs, run = [], []
        for k in range(steps + 1):
            px = x + pad + (s - 2 * pad) * k / steps
            hits = vertical_hits(pts, px)
            blocked = inside_interval(hits, y0) is not None or any(abs(h - y0) < clear for h in hits)
            if not blocked:
                for ddx in (-clear, clear):
                    if inside_interval(vertical_hits(pts, px + ddx), y0) is not None:
                        blocked = True
            if blocked:
                if run: runs.append(run)
                run = []
            else:
                run.append((px, y0))
        if run: runs.append(run)
        for r in runs:
            x0, x1 = r[0][0], r[-1][0]
            touches_left = x0 > x + pad + s * 0.01     # the run starts at the coast
            touches_right = x1 < x + s - pad - s * 0.01
            if x1 - x0 < glow * 1.2 or not (touches_left or touches_right):
                out += polyline(r, fg, w); continue
            a, b = x0, x1
            if touches_left:
                out += polyline([(a, y0), (a + glow, y0)], mark, w); a += glow
            if touches_right:
                out += polyline([(b - glow, y0), (b, y0)], mark, w); b -= glow
            if b > a:
                out += polyline([(a, y0), (b, y0)], fg, w)
    return out


def mark_room_gold(x, y, s, fg, mark, small=False, tol=0.08):
    """Lines flowing around the shape, gold where they bend."""
    n = 9 if small else 21
    w = s * (0.04 if small else 0.02)
    pad = s * 0.05
    pts = outline(x + s * 0.24, y + s * 0.1, s * 0.52, s * 0.8, tol)
    clear = s * (0.05 if small else 0.035)
    out = ""
    steps = 120
    for i in range(n):
        t = i / (n - 1)
        y0 = y + pad + (s - 2 * pad) * t
        xs = [x + pad + (s - 2 * pad) * k / steps for k in range(steps + 1)]
        ys = []
        for px in xs:
            hits = vertical_hits(pts, px)
            iv = inside_interval(hits, y0)
            py = y0
            if iv:
                top, bot = iv
                py = (top - clear) if (y0 - top) < (bot - y0) else (bot + clear)
            else:
                for h in hits:
                    if abs(h - y0) < clear:
                        py = h - clear if y0 < h else h + clear
            ys.append(py)
        ys = smooth(ys, 5 if small else 7)
        P = list(zip(xs, ys))
        run, gold = [], None
        for (px, py) in P:
            g = abs(py - y0) > s * 0.012
            if gold is None or g == gold:
                run.append((px, py))
            else:
                out += polyline(run, mark if gold else fg, w); run = [run[-1], (px, py)]
            gold = g
        out += polyline(run, mark if gold else fg, w)
    return out


def build():
    out = {}
    cases = [
        ("grain-south", lambda *a, **k: mark_grain(*a, **k, dot_at="south")),
        ("grain-centre", lambda *a, **k: mark_grain(*a, **k, dot_at="centre")),
        ("grain-none", lambda *a, **k: mark_grain(*a, **k, dot_at="none")),
        ("room", mark_room),
        ("gap", mark_gap),
        ("grain2", mark_grain2),
        ("room2", mark_room2),
        ("gap-gold", mark_gap_gold),
        ("room-gold", mark_room_gold),
    ]
    for key, fn in cases:
        m = {}
        m["mark"] = svg(240, 240, fn(0, 0, 240, SP, MG), "Generation Maine")
        m["mark-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + fn(0, 0, 240, BI, MG), "Generation Maine")
        m["mark-small"] = svg(240, 240, fn(0, 0, 240, SP, MG, small=True), "Generation Maine")
        m["avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + fn(36, 36, 168, BI, MG, small=True), "Generation Maine")
        for k, v in m.items():
            write("%s/%s/%s.svg" % (OUT, key, k), v)
        out[key] = m
    return out


if __name__ == "__main__":
    print("maine lines:", list(build()))
