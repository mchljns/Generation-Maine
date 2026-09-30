"""Real Maine terrain for the Generation Maine contour pattern ("Home Ground").

Elevation comes from the AWS Terrain Tiles open dataset (Terrarium encoding), which
combines public sources such as USGS 3DEP and SRTM. Attribution is listed in
brand/system/README.md. Tiles are cached in brand/src/data/terrain/ so the build is
repeatable offline.

home_ground(lat, lon, km, ...) returns contour paths fitted to a box, plus the elevation grid
for halftone shading.
"""
import io
import json
import math
import os
import urllib.request

import numpy as np
from PIL import Image
import contourpy

CACHE = os.path.join(os.path.dirname(__file__), "data", "terrain")
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# Places used in the system. Coordinates are the town or summit centers.
PLACES = {
    "bigelow":   {"name": "Bigelow Range", "lat": 45.1470, "lon": -70.2890, "km": 14, "interval": 40},
    "camden":    {"name": "Camden Hills", "lat": 44.2368, "lon": -69.0700, "km": 10, "interval": 20},
    "mountblue": {"name": "Mount Blue", "lat": 44.7250, "lon": -70.4450, "km": 12, "interval": 30},
    "portland":  {"name": "Portland", "lat": 43.6591, "lon": -70.2568, "km": 12, "interval": 10},
    "bangor":    {"name": "Bangor", "lat": 44.8016, "lon": -68.7712, "km": 12, "interval": 10},
    "caribou":   {"name": "Caribou", "lat": 46.8606, "lon": -68.0120, "km": 14, "interval": 15},
    "machias":   {"name": "Machias", "lat": 44.7151, "lon": -67.4614, "km": 12, "interval": 15},
    "rumford":   {"name": "Rumford", "lat": 44.5537, "lon": -70.5509, "km": 12, "interval": 30},
}


def _tile_xy(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y


def _tile(z, x, y):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, "%d_%d_%d.png" % (z, x, y))
    if not os.path.exists(p):
        with urllib.request.urlopen(URL.format(z=z, x=x, y=y), timeout=60) as r:
            data = r.read()
        with open(p, "wb") as fh:
            fh.write(data)
    im = np.asarray(Image.open(p).convert("RGB")).astype(np.float64)
    return im[:, :, 0] * 256 + im[:, :, 1] + im[:, :, 2] / 256 - 32768


def elevation_grid(lat, lon, km, z=12, size=240):
    """Elevation in meters on a size x size grid covering km x km around (lat, lon)."""
    m_per_px = 156543.03 * math.cos(math.radians(lat)) / 2 ** z
    half_px = km * 1000 / m_per_px / 2
    cx, cy = _tile_xy(lat, lon, z)
    px, py = cx * 256, cy * 256
    x0, x1 = int((px - half_px) // 256), int((px + half_px) // 256)
    y0, y1 = int((py - half_px) // 256), int((py + half_px) // 256)
    rows = []
    for ty in range(y0, y1 + 1):
        rows.append(np.hstack([_tile(z, tx, ty) for tx in range(x0, x1 + 1)]))
    mosaic = np.vstack(rows)
    ox, oy = px - x0 * 256, py - y0 * 256
    crop = mosaic[int(oy - half_px):int(oy + half_px), int(ox - half_px):int(ox + half_px)]
    img = Image.fromarray(np.clip(crop, -200, 3000).astype(np.float32), mode="F").resize((size, size), Image.BILINEAR)
    g = np.asarray(img).astype(np.float64)
    # Light smoothing so lines read as drawn curves, not pixel steps.
    k = np.array([1, 4, 6, 4, 1], dtype=np.float64)
    k /= k.sum()
    for _ in range(2):
        g = np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), 1, g)
        g = np.apply_along_axis(lambda c: np.convolve(c, k, mode="same"), 0, g)
    return g[3:-3, 3:-3]


def _smooth_path(pts, x, y, sx, sy):
    if len(pts) < 3:
        return ""
    step = max(1, len(pts) // 160)
    pts = pts[::step]
    d = "M%.1f %.1f" % (x + pts[0][0] * sx, y + pts[0][1] * sy)
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i + 1][0]) / 2
        my = (pts[i][1] + pts[i + 1][1]) / 2
        d += "Q%.1f %.1f %.1f %.1f" % (x + pts[i][0] * sx, y + pts[i][1] * sy, x + mx * sx, y + my * sy)
    d += "L%.1f %.1f" % (x + pts[-1][0] * sx, y + pts[-1][1] * sy)
    return d


def home_ground(key, x, y, w, h, interval=None, min_len=12):
    """Contour lines for a place, fitted to cover (x, y, w, h). Returns (lines, index_lines, grid).

    lines are regular contours; index_lines are every fifth contour, drawn heavier, as on real topo maps.
    """
    pl = PLACES[key]
    g = elevation_grid(pl["lat"], pl["lon"], pl["km"])
    g = np.maximum(g, -1.0)  # sea becomes flat, so the 0 m contour is the coastline
    n = g.shape[0]
    iv = interval or pl["interval"]
    lo = math.floor(g.min() / iv) * iv
    hi = math.ceil(g.max() / iv) * iv
    gen = contourpy.contour_generator(z=g, line_type="Separate")
    s = max(w, h) / (n - 1)  # cover the box, cropping the longer side
    ox, oy = x + (w - (n - 1) * s) / 2, y + (h - (n - 1) * s) / 2
    lines, index = [], []
    lvl = lo
    k = 0
    while lvl <= hi:
        if lvl >= 0:
            for seg in gen.lines(lvl):
                if len(seg) >= min_len:
                    d = _smooth_path(seg.tolist(), ox, oy, s, s)
                    (index if (round(lvl / iv) % 5 == 0) else lines).append(d)
        lvl += iv
        k += 1
    return lines, index, g


def halftone(key, x, y, w, h, cols=64, color="#34795A", rmax=None, g=None):
    """Dot grid where each dot's size follows elevation: a terrain relief made of dots."""
    if g is None:
        pl = PLACES[key]
        g = elevation_grid(pl["lat"], pl["lon"], pl["km"])
    g = np.maximum(g, 0)
    n = g.shape[0]
    lo, hi = g.min(), g.max() or 1
    step = w / cols
    rows = int(h / step)
    rmax = rmax or step * 0.46
    out = []
    for j in range(rows):
        for i in range(cols):
            gx = int(i / cols * (n - 1))
            gy = int(j / max(rows, 1) * (n - 1))
            v = (g[gy, gx] - lo) / (hi - lo + 1e-9)
            r = rmax * (0.12 + 0.88 * v)
            out.append('<circle cx="%.1f" cy="%.1f" r="%.2f"/>' % (x + (i + 0.5) * step, y + (j + 0.5) * step, r))
    return '<g fill="%s">%s</g>' % (color, "".join(out))


def coords(key):
    pl = PLACES[key]
    return "%.4f° N, %.4f° W" % (pl["lat"], abs(pl["lon"]))


if __name__ == "__main__":
    for k in PLACES:
        lines, index, g = home_ground(k, 0, 0, 1000, 1000)
        print("%-10s lines %3d index %2d elev %.0f to %.0f m" % (k, len(lines), len(index), g.min(), g.max()))
