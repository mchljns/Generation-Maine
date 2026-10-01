"""Alternate brandmark, client idea October 1: a square of sixteen lines with the solid state on it, a stamp.
Tests the state in Marigold, Birch and Moss on Spruce lines, in Spruce and Marigold on Birch lines, and
the knockout where the lines stop at the state.

  python3 brand/src/build_stamp.py
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_v4 import svg, f, rect
from build_v6 import C
import maine2
from build_logo_maine import simplified

SP, BI, MG, MOSS, PINE = C["spruce"], C["birch"], C["marigold"], C["moss"], C["pine"]
OUT = "brand/identity/stamp"


def stamp(s, bg, line, state, mode="over", rx=None, pad=0.12, w=None, inset=0.10):
    """A square s wide: bg field, 16 lines across it, the solid state. mode over: state on the lines.
    mode knockout: the lines stop short of the state and the state is drawn in the field color."""
    w = w or s * 0.028
    rx = s * 0.12 if rx is None else rx
    h = s * (1 - 2 * pad)
    ring = maine2.fit((s - h * maine2.ASPECT) / 2, s * pad, h * maine2.ASPECT, h)
    ring = simplified(ring, h * 0.005)   # the stamp is seen large, so the coast keeps more of its detail
    body = rect(0, 0, s, s, bg, rx)
    lines = ""
    for i in range(16):
        t = i / 15
        y = s * (inset + (1 - 2 * inset) * t)
        x0, x1 = s * inset, s * (1 - inset)
        if mode == "knockout":
            xs = maine2.crossings(ring, y)
            gap = w * 1.6
            segs = []
            cur = x0
            for a, b in zip(xs[0::2], xs[1::2]):
                if a - gap > cur: segs.append((cur, a - gap))
                cur = b + gap
            if x1 > cur: segs.append((cur, x1))
            for a, b in segs:
                if b - a > w * 2: lines += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(a + w / 2), f(y), f(b - w / 2), f(y), line, f(w))
        else:
            lines += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(x0 + w / 2), f(y), f(x1 - w / 2), f(y), line, f(w))
    body += lines
    body += '<path fill="%s" d="%s"/>' % (state, maine2.path(ring))
    return svg(s, s, body, "Generation Maine")


def build():
    V = [
        ("A. Marigold state on Spruce", SP, BI, MG, "over"),
        ("B. Birch state on Spruce", SP, BI, BI, "over"),
        ("C. Moss state on Spruce", SP, BI, MOSS, "over"),
        ("D. Spruce state on Birch", BI, SP, SP, "over"),
        ("E. Marigold state on Birch", BI, SP, MG, "over"),
        ("F. Knockout on Spruce: the lines stop at the state", SP, BI, SP, "knockout"),
        ("G. Knockout on Birch", BI, SP, BI, "knockout"),
        ("H. Knockout on Marigold, Spruce lines", MG, SP, MG, "knockout"),
    ]
    html = ""
    for lab, bg, line, state, mode in V:
        key = lab[0]
        sv = stamp(240, bg, line, state, mode)
        write("%s/stamp-%s.svg" % (OUT, key), sv)
        sv = sv.replace('role="img"', '')
        cells = "".join('<div class="t"><svg style="width:%dpx;height:%dpx;display:block;border-radius:%dpx" %s</div>' % (px, px, round(px * 0.12), sv[5:]) for px in (240, 110, 48, 24))
        html += '<p class="lab">%s</p><div class="g">%s</div>' % (lab, cells)
    page = ('<!doctype html><html><head><meta charset="utf-8"><style>body{background:#E9E5DA;padding:24px;font-family:Inter,sans-serif}.lab{margin:16px 0 6px;font:600 14px Inter;color:#1E2621}'
            '.g{display:flex;gap:20px;align-items:flex-end}.t{display:flex}</style></head><body><h1 style="font:800 26px Inter;margin:0 0 4px">The stamp</h1>'
            '<p style="font:14px Inter;color:#5E6A63;margin:0 0 10px">Sixteen lines across a square, the solid state on top. Each at 240, 110, 48 and 24 px, at 1x.</p>%s</body></html>') % html
    write(OUT + "/stamp.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand/src/shot.mjs"), os.path.join(ROOT, OUT, "stamp.html"), os.path.join(ROOT, OUT, "stamp.png"), "1100", "1"], check=True)


if __name__ == "__main__":
    build(); print("stamp written")
