"""Shared helpers for the Generation Maine brand build.

Text in logos is shaped with HarfBuzz and converted to outlined SVG paths,
so the logo files never depend on an installed font.
"""
import math
import os
import random

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = os.path.join(ROOT, "brand", "fonts")

# Direction A: "Spruce & Signal" (chosen)
A = {
    "spruce": "#0E3B2E",
    "fog": "#EEF2EC",
    "signal": "#FF5B24",
    "moss": "#2F6B4F",
    "lichen": "#C7DB6E",
    "ink": "#0A1A14",
    "signal_deep": "#C43D0E",
    "white": "#FFFFFF",
}


class Face:
    def __init__(self, filename):
        path = os.path.join(FONTS, filename) if not os.path.isabs(filename) else filename
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))
        self.order = self.tt.getGlyphOrder()

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        out, x = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset, pos.y_offset, info.cluster))
            x += pos.x_advance
        return out, x

    def glyph_bounds(self, name):
        bp = BoundsPen(self.gs)
        self.gs[name].draw(bp)
        return bp.bounds

    def path(self, text, size, x=0, y=0, tracking=0):
        """Return (d, width_px). y is the baseline. tracking in em/1000."""
        glyphs, adv = self.shape(text)
        s = size / self.upem
        pen = SVGPathPen(self.gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        tr = tracking * self.upem / 1000.0
        for i, (name, gx, gy, _) in enumerate(glyphs):
            ox = gx + i * tr
            tp = TransformPen(pen, (s, 0, 0, -s, x + ox * s, y - gy * s))
            self.gs[name].draw(tp)
        width = (adv + tr * (len(glyphs) - 1)) * s
        return pen.getCommands(), width

    def glyph_positions(self, text, size, x=0, tracking=0):
        glyphs, adv = self.shape(text)
        s = size / self.upem
        tr = tracking * self.upem / 1000.0
        return [(name, x + (gx + i * tr) * s, cl) for i, (name, gx, gy, cl) in enumerate(glyphs)]


def smooth_closed(points):
    """Catmull-Rom through points, returned as a closed cubic path."""
    n = len(points)
    d = "M%.1f %.1f" % points[0]
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d + "Z"


def contours(cx, cy, rings=9, r0=40, gap=34, seed=3, squash=1.0, wobble=0.16):
    """Concentric, hand-drawn-looking contour rings (the brand's pattern system).

    Abstract, not a real map: like the height lines on a trail map of a Maine hill.
    """
    rnd = random.Random(seed)
    harmonics = [(k, rnd.uniform(0, math.tau), rnd.uniform(0.3, 1.0)) for k in (2, 3, 5)]
    paths = []
    for r in range(rings):
        rad = r0 + r * gap
        pts = []
        for j in range(36):
            a = j / 36 * math.tau
            w = sum(amp * math.sin(k * a + ph + r * 0.18) for k, ph, amp in harmonics)
            rr = rad * (1 + wobble * w / 2)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * squash))
        paths.append(smooth_closed(pts))
    return paths


def contour_group(paths, stroke, width=2, opacity=1.0):
    ds = "".join('<path d="%s"/>' % d for d in paths)
    return ('<g fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" '
            'stroke-linejoin="round">%s</g>' % (stroke, width, opacity, ds))


def svg(w, h, body, title, extra_defs="", bg=None):
    rect = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'role="img" aria-labelledby="t"><title id="t">%s</title>%s%s%s</svg>\n'
            % (w, h, w, h, title, ("<defs>%s</defs>" % extra_defs) if extra_defs else "", rect, body))


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)
    return p
