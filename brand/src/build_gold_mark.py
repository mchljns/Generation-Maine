"""Client question, October 1: yellow in the brandmark, mirroring the thickness of the lines from top to bottom.
Four readings, each on Spruce and Birch at 240, 96 and 44 px, and in the avatar.

  A  interleave : a Marigold line between each pair of lines, heavy at the top where the ink is light
  B  split      : each line is two colors. Marigold takes the share the ink gives up, so the state goes gold toward the bottom
  C  mirror     : Marigold lines heavy at the top and thin at the bottom, the ink lines the other way, same rows
  D  fade       : one set of lines whose color runs from ink at the top to Marigold at the bottom

  python3 brand/src/build_gold_mark.py
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_v4 import svg, f, wordmark_one_line
from build_v6 import C
import maine2

SP, BI, MG = C["spruce"], C["birch"], C["marigold"]
OUT = "brand/identity/gold-mark"


def rows(x, y, h, n=21, lo=0.015, hi=0.034, keep=1.8):
    ring = maine2.fit(x, y, h * maine2.ASPECT, h)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    out = []
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.035 + 0.93 * t)
        w = h * (lo + (hi - lo) * t)
        xs = maine2.crossings(ring, y0)
        out.append((t, y0, w, [(a, b) for a, b in zip(xs[0::2], xs[1::2]) if b - a >= w * keep]))
    return out, maxx - minx


def seg(a, b, y, w, col):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>' % (f(a + w / 2), f(y), f(b - w / 2), f(y), col, f(w))


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def mark(variant, x, y, h, fg):
    R, w = rows(x, y, h)
    body = ""
    for i, (t, y0, wt, runs) in enumerate(R):
        if variant == "A":
            for a, b in runs: body += seg(a, b, y0, wt, fg)
            if i < len(R) - 1:
                t2, y1, w1, _ = R[i + 1]
                ym = (y0 + y1) / 2; wg = h * (0.030 - 0.022 * t)   # heavy at the top, thin at the bottom
                ring = maine2.fit(x, y, h * maine2.ASPECT, h); xs = maine2.crossings(ring, ym)
                for a, b in zip(xs[0::2], xs[1::2]):
                    if b - a >= wg * 1.8: body += seg(a, b, ym, wg, MG)
        elif variant == "B":
            for a, b in runs:
                body += seg(a, b, y0 - wt * (1 - t) / 2 * 0, wt, fg)
                # the gold share of the stroke grows with t: drawn as a thinner line on top of the ink
                body += seg(a, b, y0 + wt * (1 - t) / 2, wt * t, MG)
        elif variant == "C":
            for a, b in runs: body += seg(a, b, y0, wt, fg)
            if i < len(R) - 1:
                t2, y1, w1, _ = R[i + 1]
                ym = (y0 + y1) / 2; wg = h * (0.034 - 0.019 * t)
                ring = maine2.fit(x, y, h * maine2.ASPECT, h); xs = maine2.crossings(ring, ym)
                for a, b in zip(xs[0::2], xs[1::2]):
                    if b - a >= wg * 1.8: body += seg(a, b, ym, wg * 0.55, MG)
        elif variant == "D":
            for a, b in runs: body += seg(a, b, y0, wt, mix(fg, MG, t ** 1.4))
    return body, w


def tile(variant, fg, bg, h):
    b, w = mark(variant, 0, 0, h, fg)
    return '<div class="t" style="background:%s;height:%dpx">%s</div>' % (bg, h + 40, svg(w, h, b, "").replace('role="img"', ''))


def build():
    html = ""
    names = {"A": "A. Interleave. A Marigold line between each pair, heavy at the top where the ink is light.",
             "B": "B. Split. Each line is two colors. Marigold takes the share the ink gives up, so the state goes gold toward the bottom.",
             "C": "C. Mirror. Thin Marigold lines in the gaps, heavy at the top and thin at the bottom, the ink the other way.",
             "D": "D. Fade. One set of lines, ink at the top to Marigold at the bottom."}
    for v in "ABCD":
        b, w = mark(v, 0, 0, 164, BI)
        av = svg(240, 240, '<circle cx="120" cy="120" r="120" fill="%s"/>' % SP + '<g transform="translate(%s 38)">%s</g>' % (f((240 - w) / 2), b), "").replace('role="img"', '')
        bw, ww, hh = wordmark_one_line(BI, MG, "circle", 100)
        mb, mw = mark(v, 0, 74 - 96 + 6, 96, BI)
        lock = svg(ww + mw + 26, hh, mb + '<g transform="translate(%s 0)">%s</g>' % (f(mw + 26), bw), "").replace('role="img"', '')
        html += '<p class="lab">%s</p><div class="g">%s%s%s%s%s<div class="t" style="background:%s;height:204px"><div style="width:110px;height:110px">%s</div></div><div class="t lk" style="background:%s">%s</div></div>' % (
            names[v], tile(v, BI, SP, 240), tile(v, SP, BI, 240), tile(v, BI, SP, 96), tile(v, SP, BI, 96), tile(v, BI, SP, 44), BI, av, SP, lock)
        write("%s/mark-%s.svg" % (OUT, v), svg(w, 164, b, "Generation Maine"))
    css = open(os.path.join(ROOT, "brand/identity/apply/apply.html")).read().split("<style>")[1].split("</style>")[0]
    page = ('<!doctype html><html><head><meta charset="utf-8"><style>%s body{background:#E9E5DA;padding:28px}.lab{margin:22px 0 8px;font:600 14px Inter;color:#1E2621}'
            '.g{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.t{border-radius:10px;padding:20px 28px;display:flex;align-items:center;justify-content:center}.t svg{display:block;height:100%%;width:auto}'
            '.t.lk{height:120px;padding:20px 30px}.t.lk svg{height:48px}</style></head><body><h1 style="font:800 28px Bric;margin:0 0 4px">Yellow in the brandmark, by line weight</h1>'
            '<p style="font:14px Inter;color:#5E6A63;margin:0">Each reading at 240, 96 and 44 px on Spruce and Birch, then the avatar and the lockup.</p>%s</body></html>') % (css, html)
    write(OUT + "/gold-mark.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand/src/shot.mjs"), os.path.join(ROOT, OUT, "gold-mark.html"), os.path.join(ROOT, OUT, "gold-mark.png"), "1700", "1.3"], check=True)


if __name__ == "__main__":
    build(); print("gold-mark written")
