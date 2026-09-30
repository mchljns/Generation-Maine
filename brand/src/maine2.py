"""Precise Maine outline: US Census Bureau cartographic boundary file, 1:500,000, clipped to the
shoreline (public domain). 2,265 points, no simplification unless asked for.

fit(x, y, w, h) returns the ring in box coordinates. crossings(ring, y) gives the x values where a
horizontal line crosses the polygon, so the shape can be drawn in lines.
"""
import json
import math
import os

_RING = json.load(open(os.path.join(os.path.dirname(__file__), "data", "maine-census.json")))["ring"]
_LAT0 = 45.25
_K = math.cos(math.radians(_LAT0))
_XY = [(lon * _K, -lat) for lon, lat in _RING]
_MINX, _MAXX = min(p[0] for p in _XY), max(p[0] for p in _XY)
_MINY, _MAXY = min(p[1] for p in _XY), max(p[1] for p in _XY)
ASPECT = (_MAXX - _MINX) / (_MAXY - _MINY)


def fit(x, y, w, h):
    s = min(w / (_MAXX - _MINX), h / (_MAXY - _MINY))
    ox = x + (w - (_MAXX - _MINX) * s) / 2
    oy = y + (h - (_MAXY - _MINY) * s) / 2
    return [(ox + (px - _MINX) * s, oy + (py - _MINY) * s) for px, py in _XY]


def bbox(pts):
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def crossings(ring, py):
    xs = []
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        if (y0 <= py < y1) or (y1 <= py < y0):
            xs.append(x0 + (py - y0) / (y1 - y0) * (x1 - x0))
    xs.sort()
    return xs


def path(ring):
    return "M" + " L".join("%.2f %.2f" % p for p in ring) + "Z"
