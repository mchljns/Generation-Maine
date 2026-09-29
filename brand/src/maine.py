"""Maine outline for the brandmark, from Natural Earth 1:10m (public domain).

maine_shape() returns an SVG path for the mainland, simplified to the requested
tolerance, fitted into a box. project() maps a longitude/latitude into the same box,
so towns and the sunrise point line up with the outline.
"""
import json
import math
import os

_DATA = json.load(open(os.path.join(os.path.dirname(__file__), "data", "maine.json")))
_LAT0 = 45.25
_K = math.cos(math.radians(_LAT0))


def _xy(lon, lat):
    return lon * _K, -lat


def _dp(pts, tol):
    """Douglas-Peucker simplification."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1e-9
    idx, dmax = 0, 0.0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = abs(dy * px - dx * py + x2 * y1 - y2 * x1) / n
        if d > dmax:
            idx, dmax = i, d
    if dmax > tol:
        return _dp(pts[: idx + 1], tol)[:-1] + _dp(pts[idx:], tol)
    return [pts[0], pts[-1]]


_MAIN = [_xy(lon, lat) for lon, lat in _DATA["mainland"]]
_MINX = min(p[0] for p in _MAIN)
_MAXX = max(p[0] for p in _MAIN)
_MINY = min(p[1] for p in _MAIN)
_MAXY = max(p[1] for p in _MAIN)
ASPECT = (_MAXX - _MINX) / (_MAXY - _MINY)  # width / height


def _fit(x, y, w, h):
    s = min(w / (_MAXX - _MINX), h / (_MAXY - _MINY))
    ox = x + (w - (_MAXX - _MINX) * s) / 2
    oy = y + (h - (_MAXY - _MINY) * s) / 2
    return s, ox, oy


def project(lon, lat, x, y, w, h):
    s, ox, oy = _fit(x, y, w, h)
    px, py = _xy(lon, lat)
    return ox + (px - _MINX) * s, oy + (py - _MINY) * s


def maine_shape(x, y, w, h, tol=0.02, round_corners=0.0):
    """SVG path data for mainland Maine fitted into (x, y, w, h). tol is in degrees of latitude."""
    s, ox, oy = _fit(x, y, w, h)
    # Split the closed ring at the point farthest from the start, simplify both halves.
    far = max(range(len(_MAIN)), key=lambda i: math.hypot(_MAIN[i][0] - _MAIN[0][0], _MAIN[i][1] - _MAIN[0][1]))
    pts = _dp(_MAIN[: far + 1], tol)[:-1] + _dp(_MAIN[far:] + [_MAIN[0]], tol)
    pts = [(ox + (px - _MINX) * s, oy + (py - _MINY) * s) for px, py in pts]
    if round_corners <= 0:
        return "M" + " L".join("%.2f %.2f" % p for p in pts[:-1]) + "Z", len(pts)
    # Rounded corners: cut each corner and join with a quadratic curve.
    out = []
    n = len(pts) - 1
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = round_corners
        def toward(a, b, dist):
            L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
            dd = min(dist, L / 2)
            return a[0] + (b[0] - a[0]) * dd / L, a[1] + (b[1] - a[1]) * dd / L
        a = toward(p1, p0, r)
        b = toward(p1, p2, r)
        out.append(("L" if out else "M") + "%.2f %.2f Q%.2f %.2f %.2f %.2f" % (a[0], a[1], p1[0], p1[1], b[0], b[1]))
    return " ".join(out) + "Z", n


# Points of interest (longitude, latitude)
LUBEC = (-66.95, 44.815)   # West Quoddy Head, the easternmost point of the US
TOWNS = {
    "Lewiston": (-70.215, 44.100),
    "Bangor": (-68.772, 44.801),
    "Caribou": (-68.012, 46.861),
    "Biddeford": (-70.453, 43.492),
    "Portland": (-70.255, 43.661),
}
