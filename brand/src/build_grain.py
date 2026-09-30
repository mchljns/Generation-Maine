"""Grain: Maine drawn in horizontal lines, from the precise Census outline. Gold carried by the
lines, never as a dot.

  grain        : Spruce lines only
  grain-widest : the longest line is gold, a geometric rule rather than a geographic one
  grain-room   : the lines make room at the state's centre and turn gold where they bend
  mural        : sixty fine lines, for the website hero and the end card

  python3 brand/src/build_grain.py     # writes brand/identity/grain/*.svg
"""
import math

from gmlib import write
from build_v4 import svg, rect, f
from build_v6 import C
import maine2

OUT = "brand/identity/grain"
SP, BI, MG, PI = C["spruce"], C["birch"], C["marigold"], C["pine"]


def seg(x0, x1, y, w, color):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(x0), f(y), f(x1), f(y), color, f(w))


def poly(pts, w, color):
    if len(pts) < 2:
        return ""
    return '<path d="M%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" fill="none"/>' % (
        " L".join("%s %s" % (f(a), f(b)) for a, b in pts), color, f(w))


def fit_ring(x, y, s):
    """The outline fitted into a square box with a little air, and its bounds."""
    ring = maine2.fit(x + s * 0.1, y + s * 0.04, s * 0.8, s * 0.92)
    return ring, maine2.bbox(ring)


def scan(ring, y0, min_len, w):
    """Runs of the horizontal line at y0 that lie inside the shape, trimmed by half a stroke."""
    xs = maine2.crossings(ring, y0)
    runs = []
    for a, b in zip(xs[0::2], xs[1::2]):
        if b - a >= min_len:
            runs.append((a + w / 2, b - w / 2))
    return runs


def grain(x, y, s, fg, mark, n=21, gold=None, small=False, w_lo=None, w_hi=None):
    ring, (minx, miny, maxx, maxy) = fit_ring(x, y, s)
    w_lo = w_lo or s * (0.03 if small else 0.012)
    w_hi = w_hi or s * (0.062 if small else 0.036)
    rows = []
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.035 + 0.93 * t)
        w = w_lo + (w_hi - w_lo) * t
        rows.append((y0, w, scan(ring, y0, w * 1.6, w)))
    widest = max(range(n), key=lambda i: sum(b - a for a, b in rows[i][2]))
    out = ""
    for i, (y0, w, runs) in enumerate(rows):
        color = mark if (gold == "widest" and i == widest) else fg
        for a, b in runs:
            out += seg(a, b, y0, w, color)
    return out


def smooth(vals, k):
    n = len(vals)
    out = []
    for i in range(n):
        acc = wsum = 0.0
        for j in range(max(0, i - 3 * k), min(n, i + 3 * k + 1)):
            wt = math.exp(-((j - i) / k) ** 2 / 2)
            acc += vals[j] * wt; wsum += wt
        out.append(acc / wsum)
    return out


def grain_room(x, y, s, fg, mark, n=21, small=False):
    """Lines inside Maine that bend around an empty room at the state's centre, gold where they bend."""
    ring, (minx, miny, maxx, maxy) = fit_ring(x, y, s)
    # centre of the shape: the mean of the ring, which sits in Piscataquis County
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)
    w_lo, w_hi = (s * 0.03, s * 0.062) if small else (s * 0.012, s * 0.036)
    clear = s * (0.15 if small else 0.11)
    out = ""
    steps = 140
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.035 + 0.93 * t)
        w = w_lo + (w_hi - w_lo) * t
        dy0 = y0 - cy
        ady = abs(dy0)
        sign = 1 if dy0 >= 0 else -1
        if ady < clear:
            amp, sig = clear - ady, clear * 0.75
        else:
            amp, sig = 0.42 * clear * math.exp(-((ady - clear) / (0.55 * clear)) ** 2), clear * 0.95
        pts = []
        for k in range(steps + 1):
            px = minx + (maxx - minx) * k / steps
            dx = px - cx
            off = amp * math.exp(-(dx / sig) ** 2)
            if ady < clear and abs(dx) < clear:
                off = max(off, math.sqrt(clear * clear - dx * dx) - ady)
            pts.append((px, y0 + sign * off, off / clear))
        # keep the parts inside the shape, split into runs, colour by bend
        run, gold = [], None
        def flush(run, gold):
            return poly([(a, b) for a, b, _ in run], w, mark if gold else fg) if len(run) > 1 and (run[-1][0] - run[0][0]) >= w * 1.6 else ""
        for px, py, o in pts:
            xs = maine2.crossings(ring, py)
            inside = any(a <= px <= b for a, b in zip(xs[0::2], xs[1::2]))
            g = o > 0.12
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


def build():
    m = {}
    m["grain"] = svg(240, 240, grain(0, 0, 240, SP, MG), "Generation Maine")
    m["grain-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + grain(0, 0, 240, BI, MG), "Generation Maine")
    m["grain-small"] = svg(240, 240, grain(0, 0, 240, SP, MG, n=8, small=True), "Generation Maine")
    m["grain-avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + grain(30, 30, 180, BI, MG, n=8, small=True), "Generation Maine")
    m["grain-widest"] = svg(240, 240, grain(0, 0, 240, SP, MG, gold="widest"), "Generation Maine")
    m["grain-widest-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + grain(0, 0, 240, BI, MG, gold="widest"), "Generation Maine")
    m["grain-widest-small"] = svg(240, 240, grain(0, 0, 240, SP, MG, n=8, gold="widest", small=True), "Generation Maine")
    m["grain-widest-avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + grain(30, 30, 180, BI, MG, n=8, gold="widest", small=True), "Generation Maine")
    m["grain-room"] = svg(240, 240, grain_room(0, 0, 240, SP, MG), "Generation Maine")
    m["grain-room-reversed"] = svg(240, 240, rect(0, 0, 240, 240, SP) + grain_room(0, 0, 240, BI, MG), "Generation Maine")
    m["grain-room-small"] = svg(240, 240, grain_room(0, 0, 240, SP, MG, n=8, small=True), "Generation Maine")
    m["grain-room-avatar"] = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + grain_room(30, 30, 180, BI, MG, n=8, small=True), "Generation Maine")
    m["mural"] = svg(720, 720, grain(0, 0, 720, SP, MG, n=60, gold="widest", w_lo=720 * 0.004, w_hi=720 * 0.011), "Generation Maine")
    m["mural-reversed"] = svg(720, 720, rect(0, 0, 720, 720, SP) + grain(0, 0, 720, BI, MG, n=60, gold="widest", w_lo=720 * 0.004, w_hi=720 * 0.011), "Generation Maine")
    m["outline"] = svg(240, 240, '<path d="%s" fill="%s"/>' % (maine2.path(fit_ring(0, 0, 240)[0]), SP), "Maine")
    for k, v in m.items():
        write("%s/%s.svg" % (OUT, k), v)
    return m


if __name__ == "__main__":
    print("grain:", list(build()))
