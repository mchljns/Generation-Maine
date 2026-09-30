"""Identity v3: three concepts built to reach the A range.

  Viewfinder   : camera frame brackets around ME
  Growth Rings : a tree's cross-section, one ring per generation
  Woven        : a Generation Maine plaid, one thread per creator

Writes brand/v3/concepts.html (self-contained) and brand/v3/<concept>/*.svg.
Run from the repo root: python3 brand/src/build_v3.py && node brand/src/render_v3.mjs
"""
import base64
import math
import os
import random

from gmlib import ROOT, Face, smooth_closed, write
from v2marks import SANS, MONO, f

V3 = os.path.join(ROOT, "brand", "fonts", "v3")
SANS_B = Face(os.path.join(ROOT, "brand", "fonts", "v2", "InstrumentSans-Bold.ttf"))
FRAUNCES = Face(os.path.join(V3, "Fraunces-SemiBold.ttf"))
OUT = "brand/v3"

VF = {"ink": "#111318", "paper": "#F5F6F8", "blue": "#3D2FD1", "pink": "#F0509A", "gray": "#8A909C", "white": "#FFFFFF"}
RG = {"spruce": "#0B4A34", "pine": "#07261C", "fog": "#EDF0F4", "lupine": "#F0509A", "blossom": "#FFC2DD", "moss": "#34795A", "ink": "#121417"}
WV = {"indigo": "#2A2E7A", "wool": "#E9E8EE", "lupine": "#F0509A", "moss": "#34795A", "sky": "#9DB8EC", "ink": "#15161C", "white": "#FFFFFF"}


def svg(w, h, body, label, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s%s</svg>'
            % (f(w), f(h), f(w), f(h), label, ("<defs>%s</defs>" % defs) if defs else "", body))


def rect(x, y, w, h, fill, rx=0):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h), f(rx), fill)


def text(x, y, s, size, fill, fam="'Instrument Sans'", weight=600, anchor="start", ls=0, upper=False):
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" style="font-family:%s,Arial,sans-serif;font-weight:%d;'
            'letter-spacing:%sem%s">%s</text>' % (f(x), f(y), f(size), fill, anchor, fam, weight, ls,
                                                 ";text-transform:uppercase" if upper else "", s))


def wordmark(face, x, baseline, size, fill, tracking=-18, text_="Generation Maine"):
    d, w = face.path(text_, size, x, baseline, tracking)
    return '<path fill="%s" d="%s"/>' % (fill, d), w


# ======================================================================= Viewfinder
def vf_symbol(x, y, s, color, inner=None):
    """Four corner brackets around ME. Box s x s."""
    k = s / 200.0
    t, a = 17 * k, 58 * k
    b = ""
    for cx, cy, sx, sy in ((x, y, 1, 1), (x + s, y, -1, 1), (x, y + s, 1, -1), (x + s, y + s, -1, -1)):
        b += '<path fill="%s" d="M%s %sh%sv%sh%sv%sh%sz"/>' % (
            color, f(cx), f(cy), f(sx * a), f(sy * t), f(-sx * (a - t)), f(sy * (a - t)), f(-sx * t))
    if inner is None:
        size = 96 * k
        d, w = SANS_B.path("ME", size, 0, 0, -10)
        d, w = SANS_B.path("ME", size, x + (s - w) / 2, y + s / 2 + 0.36 * size, -10)
        b += '<path fill="%s" d="%s"/>' % (color, d)
    else:
        b += inner
    return b


def vf_frame(x, y, w, h, color, arm, t):
    """Corner brackets on a rectangle of any shape."""
    b = ""
    for cx, cy, sx, sy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        b += '<path fill="%s" d="M%s %sh%sv%sh%sv%sh%sz"/>' % (
            color, f(cx), f(cy), f(sx * arm), f(sy * t), f(-sx * (arm - t)), f(sy * (arm - t)), f(-sx * t))
    return b


def vf_lockup(color, text_color=None, size=100):
    sym = vf_symbol(0, 0, size * 1.1, color)
    wm, w = wordmark(SANS, size * 1.1 + size * 0.32, size * 0.78, size * 0.86, text_color or color)
    return sym + wm, size * 1.1 + size * 0.32 + w, size * 1.1


def build_viewfinder():
    c = VF
    s = {}
    s["symbol"] = svg(200, 200, vf_symbol(0, 0, 200, c["blue"]), "Viewfinder mark")
    b, w, h = vf_lockup(c["blue"], c["ink"])
    s["lockup"] = svg(w, h, b, "Generation Maine")
    b, w, h = vf_lockup(c["white"])
    s["lockup-rev"] = svg(w, h, b, "Generation Maine")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["blue"]) + vf_symbol(250, 250, 580, c["white"]), "Viewfinder avatar")
    # End card: the brackets become the frame of the whole screen
    e = rect(0, 0, 1080, 1920, c["ink"])
    e += vf_frame(70, 70, 940, 1780, c["white"], 150, 22)
    e += '<circle cx="150" cy="190" r="14" fill="%s"/>' % c["pink"]
    e += text(180, 202, "REC  00:59", 34, c["white"], "'IBM Plex Mono'", 500, ls=0.06)
    e += vf_symbol(390, 520, 300, c["white"])
    e += text(540, 1010, "Follow along", 104, c["white"], weight=600, anchor="middle", ls=-0.02)
    y = 1150
    for lab, hd in (("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com")):
        e += text(480, y, lab.upper(), 30, c["gray"], "'IBM Plex Mono'", 500, "end", 0.06)
        e += text(510, y, hd, 38, c["white"], "'IBM Plex Mono'", 500)
        y += 70
    e += text(540, 1640, "An initiative of Maine Policy Institute", 32, c["white"], weight=500, anchor="middle")
    s["endcard"] = svg(1080, 1920, e, "Viewfinder end card")
    # Lower third: the name sits inside brackets
    l = vf_symbol(96, 790, 0.1, c["white"], inner="")  # placeholder to keep structure simple
    l = ""
    bx, by, bw, bh = 96, 800, 760, 190
    k = bh / 200.0
    for cx, cy, sx, sy in ((bx, by, 1, 1), (bx + bw, by, -1, 1), (bx, by + bh, 1, -1), (bx + bw, by + bh, -1, -1)):
        l += '<path fill="%s" d="M%s %sh%sv%sh%sv%sh%sz"/>' % (
            c["white"], f(cx), f(cy), f(sx * 50 * k), f(sy * 14 * k), f(-sx * (50 - 14) * k), f(sy * (50 - 14) * k), f(-sx * 14 * k))
    l += text(bx + 40, by + 96, "[Creator name]", 64, c["white"], weight=600, ls=-0.01)
    l += text(bx + 42, by + 150, "ME / [HOMETOWN]", 30, c["white"], "'IBM Plex Mono'", 500, ls=0.08)
    s["lowerthird"] = svg(1920, 1080, l, "Viewfinder lower third")
    # Creator system: the brackets frame each creator's face, with their town under it
    towns = ["PORTLAND", "BANGOR", "CARIBOU", "BIDDEFORD", "MACHIAS", "RUMFORD"]
    sys_ = ""
    for i, t in enumerate(towns):
        x = i * 180
        sys_ += rect(x, 0, 160, 200, "#E4E6EB", 10)
        sys_ += '<circle cx="%s" cy="78" r="30" fill="#C7CBD3"/><path d="M%s 200 q0 -70 55 -70 q55 0 55 70z" fill="#C7CBD3"/>' % (f(x + 80), f(x + 25))
        sys_ += vf_symbol(x + 36, 36, 88, c["blue"], inner="")
        sys_ += text(x + 80, 232, "ME / " + t, 16, c["ink"], "'IBM Plex Mono'", 500, "middle", 0.04)
    s["system"] = svg(1060, 240, sys_, "Creator frames")
    return s


# ======================================================================= Growth Rings
def ring_paths(cx, cy, R, n, seed, wobble=0.035):
    """Eccentric tree rings: the pith sits off center and rings drift outward unevenly."""
    rnd = random.Random(seed)
    px, py = cx - R * 0.14, cy + R * 0.08   # pith offset
    harm = [(k, rnd.uniform(0, math.tau), rnd.uniform(0.4, 1.0)) for k in (2, 3, 5)]
    paths = []
    for i in range(n):
        tfrac = (i + 1) / n
        rr = R * (0.18 + 0.82 * tfrac)
        ox = px + (cx - px) * tfrac
        oy = py + (cy - py) * tfrac
        pts = []
        for j in range(48):
            a = j / 48 * math.tau
            w = sum(amp * math.sin(k * a + ph + i * 0.3) for k, ph, amp in harm)
            r = rr * (1 + wobble * w)
            pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
        paths.append(smooth_closed(pts))
    return paths, (px, py)


def rg_symbol(x, y, s, line, accent, pith=None, n=5, seed=4, small=False):
    k = s / 200.0
    n = 3 if small else n
    paths, (px, py) = ring_paths(x + s / 2, y + s / 2, s * 0.47, n, seed)
    sw = (10 if small else 7) * k
    b = ""
    for i, d in enumerate(paths):
        last = i == len(paths) - 1
        b += '<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, accent if last else line, f(sw * (1.9 if last else 1)))
    b += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(px), f(py), f((12 if small else 9) * k), pith or line)
    return b


def rg_lockup(line, accent, text_color, size=100):
    sym = rg_symbol(0, 0, size * 1.12, line, accent)
    wm, w = wordmark(SANS, size * 1.12 + size * 0.32, size * 0.8, size * 0.86, text_color)
    return sym + wm, size * 1.12 + size * 0.32 + w, size * 1.12


def build_rings():
    c = RG
    s = {}
    s["symbol"] = svg(200, 200, rg_symbol(0, 0, 200, c["spruce"], c["lupine"]), "Growth Rings mark")
    s["symbol-small"] = svg(200, 200, rg_symbol(0, 0, 200, c["spruce"], c["lupine"], small=True), "Growth Rings small mark")
    b, w, h = rg_lockup(c["spruce"], c["lupine"], c["ink"])
    s["lockup"] = svg(w, h, b, "Generation Maine")
    b, w, h = rg_lockup(c["fog"], c["lupine"], c["fog"])
    s["lockup-rev"] = svg(w, h, b, "Generation Maine")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["spruce"]) + rg_symbol(200, 200, 680, c["fog"], c["lupine"], small=False), "Growth Rings avatar")
    e = rect(0, 0, 1080, 1920, c["spruce"])
    big, _ = ring_paths(760, 1560, 900, 11, 9, 0.03)
    e += '<g fill="none" stroke="%s" stroke-width="3" opacity=".55">%s</g>' % (c["moss"], "".join('<path d="%s"/>' % d for d in big))
    e += rg_symbol(390, 360, 300, c["fog"], c["lupine"])
    e += text(540, 850, "Follow along", 104, c["fog"], weight=600, anchor="middle", ls=-0.02)
    y = 990
    for lab, hd in (("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com")):
        e += text(480, y, lab, 32, c["blossom"], weight=600, anchor="end")
        e += text(510, y, hd, 40, c["fog"], weight=500)
        y += 76
    e += text(540, 1420, "An initiative of Maine Policy Institute", 32, c["fog"], weight=500, anchor="middle")
    s["endcard"] = svg(1080, 1920, e, "Growth Rings end card")
    l = rect(96, 812, 800, 172, c["fog"], 86)
    l += rg_symbol(118, 834, 128, c["spruce"], c["lupine"], small=True)
    l += text(272, 894, "[Creator name]", 60, c["ink"], weight=600, ls=-0.01)
    l += text(274, 950, "[Hometown], Maine", 38, c["moss"], weight=600)
    s["lowerthird"] = svg(1920, 1080, l, "Growth Rings lower third")
    sys_ = ""
    for i, (nm, seed) in enumerate([("Creator 1", 11), ("Creator 2", 23), ("Creator 3", 37), ("Creator 4", 41), ("Creator 5", 58), ("Creator 6", 64)]):
        x = i * 180
        sys_ += '<circle cx="%s" cy="80" r="80" fill="%s"/>' % (f(x + 80), c["spruce"])
        sys_ += rg_symbol(x + 12, 12, 136, c["fog"], c["lupine"], n=4 + i % 3, seed=seed)
        sys_ += text(x + 80, 200, nm, 18, c["ink"], weight=600, anchor="middle")
    s["system"] = svg(1060, 220, sys_, "One ring pattern per creator")
    return s


# ======================================================================= Woven
SETT = [("indigo", 28), ("lupine", 4), ("indigo", 10), ("moss", 12), ("sky", 3), ("moss", 12), ("indigo", 10), ("wool", 6)]


def plaid(x, y, w, h, colors, sett=None, scale=3.0, pid="p"):
    """Tartan-style plaid: the same stripe sequence as warp and weft, the weft at half opacity, plus a twill hatch."""
    sett = sett or SETT
    seq = sett + list(reversed(sett))
    unit = sum(wd for _, wd in seq) * scale
    stripes_v, stripes_h = "", ""
    pos = 0.0
    for col, wd in seq:
        stripes_v += rect(pos, 0, wd * scale, unit, colors[col])
        stripes_h += '<rect x="0" y="%s" width="%s" height="%s" fill="%s" opacity=".55"/>' % (f(pos), f(unit), f(wd * scale), colors[col])
        pos += wd * scale
    hatch = "".join('<line x1="%s" y1="0" x2="%s" y2="%s" stroke="#000" stroke-opacity=".08" stroke-width="%s"/>'
                    % (f(i * scale * 2), f(i * scale * 2 - unit), f(unit), f(scale * 0.7)) for i in range(int(unit / scale) + 2))
    defs = ('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse" x="%s" y="%s">%s%s%s</pattern>'
            % (pid, f(unit), f(unit), f(x), f(y), stripes_v, stripes_h, hatch))
    return defs, '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x), f(y), f(w), f(h), pid)


_WVID = [0]


def wv_symbol(x, y, s, a, b_, gap_color=None):
    """A 3 x 3 basket weave tile. Thin transparent cuts show where a band tucks under the other."""
    k = s / 200.0
    band, gap = 52 * k, 22 * k
    step = band + gap
    cut = 5 * k
    _WVID[0] += 1
    mid = "wvcut%d" % _WVID[0]
    lines = ""
    body = ""
    for i in range(3):
        body += rect(x, y + i * step, s, band, a)
    for j in range(3):
        body += rect(x + j * step, y, band, s, b_)
    for i in range(3):
        for j in range(3):
            cx, cy = x + j * step, y + i * step
            if (i + j) % 2 == 1:   # weft over warp: redraw weft, cut along its top and bottom edges
                body += rect(cx - 0.8 * k, cy, band + 1.6 * k, band, a)
                lines += rect(cx, cy - cut, band, cut, "#000") + rect(cx, cy + band, band, cut, "#000")
            else:                  # warp over weft: cut along the warp's left and right edges
                lines += rect(cx - cut, cy, cut, band, "#000") + rect(cx + band, cy, cut, band, "#000")
    mask = ('<mask id="%s" maskUnits="userSpaceOnUse" x="%s" y="%s" width="%s" height="%s">%s%s</mask>'
            % (mid, f(x - 1), f(y - 1), f(s + 2), f(s + 2), rect(x - 1, y - 1, s + 2, s + 2, "#fff"), lines))
    out = rect(x, y, s, s, gap_color) if gap_color else ""
    return out + mask + '<g mask="url(#%s)">%s</g>' % (mid, body)


def wv_lockup(a, b_, text_color, size=100):
    sym = wv_symbol(0, 0, size * 1.02, a, b_)
    wm, w = wordmark(FRAUNCES, size * 1.02 + size * 0.34, size * 0.8, size * 0.9, text_color, tracking=-10)
    return sym + wm, size * 1.02 + size * 0.34 + w, size * 1.02


def build_woven():
    c = WV
    s = {}
    s["symbol"] = svg(200, 200, wv_symbol(0, 0, 200, c["indigo"], c["lupine"]), "Woven mark")
    b, w, h = wv_lockup(c["indigo"], c["lupine"], c["ink"])
    s["lockup"] = svg(w, h, b, "Generation Maine")
    b, w, h = wv_lockup(c["wool"], c["lupine"], c["wool"])
    s["lockup-rev"] = svg(w, h, b, "Generation Maine")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["indigo"]) + wv_symbol(270, 270, 540, c["wool"], c["lupine"]), "Woven avatar")
    defs, pl = plaid(0, 0, 1080, 1920, c, scale=4.2, pid="pe")
    e = pl + rect(90, 420, 900, 1080, c["wool"], 28)
    e += wv_symbol(450, 500, 180, c["indigo"], c["lupine"])
    e += text(540, 830, "Follow along", 100, c["ink"], "Fraunces", 600, "middle", -0.01)
    y = 960
    for lab, hd in (("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com")):
        e += text(510, y, lab, 32, c["indigo"], weight=600, anchor="end")
        e += text(540, y, hd, 40, c["ink"], weight=500)
        y += 76
    e += text(540, 1400, "An initiative of Maine Policy Institute", 32, c["ink"], weight=500, anchor="middle")
    s["endcard"] = svg(1080, 1920, e, "Woven end card", defs)
    defs, pl = plaid(96, 812, 40, 172, c, scale=2.2, pid="pl")
    l = rect(96, 812, 820, 172, c["wool"], 10) + pl
    l += text(172, 894, "[Creator name]", 62, c["ink"], "Fraunces", 600)
    l += text(174, 950, "[Hometown], Maine", 38, c["indigo"], weight=600)
    s["lowerthird"] = svg(1920, 1080, l, "Woven lower third", defs)
    # Creator system: each creator adds one thread color; the plaid grows as they join
    threads = ["#F0509A", "#FFD0A8", "#9DB8EC", "#34795A", "#B79CF0", "#F6E7A1"]
    sys_, defs_all = "", ""
    for i in range(6):
        sett = [("indigo", 26)]
        for j in range(i + 1):
            sett += [("t%d" % j, 4), ("indigo", 8)]
        cols = dict(c)
        for j, tc in enumerate(threads):
            cols["t%d" % j] = tc
        d_, p_ = plaid(i * 180, 0, 160, 160, cols, sett=sett, scale=2.0, pid="ps%d" % i)
        defs_all += d_
        sys_ += '<g>%s</g>' % p_
        sys_ += text(i * 180 + 80, 190, "%d creator%s" % (i + 1, "" if i == 0 else "s"), 17, c["ink"], weight=600, anchor="middle")
    s["system"] = svg(1060, 210, sys_, "The plaid grows one thread per creator", defs_all)
    return s


# ======================================================================= presentation
CRIT = [("Idea", 15), ("Distinct", 20), ("Small size", 15), ("Premium", 15), ("Fit", 15), ("Ease", 10), ("System", 10)]
LET = [(9.0, "A+"), (8.5, "A"), (8.0, "A-"), (7.5, "B+"), (7.0, "B"), (6.5, "B-"), (6.0, "C+"), (5.5, "C"), (5.0, "C-"), (0, "D")]


def overall(sc):
    return sum(a * w for a, (_, w) in zip(sc, CRIT)) / 100.0


def letter(v):
    return next(l for cut, l in LET if v >= cut)


CONCEPTS = [
    {
        "key": "viewfinder", "name": "Viewfinder", "build": build_viewfinder, "bg": VF["paper"], "dark": VF["ink"], "accent": VF["blue"],
        "idea": "Camera frame brackets around ME. It reads three ways at once: the focus frame on a phone camera, the postal code for Maine, and me, the creator speaking for themselves.",
        "why": ["The whole project is phones and first-person video. The mark is the thing on their screen.",
                "No map, no sun, no mountain, no badge. Nothing a neighbor owns.",
                "Two letters and four corners: perfect at 16 px, and anyone can rebuild it in Canva."],
        "system": "The brackets frame each creator's face in thumbnails and bracket their name on lower thirds. Captions use a camera-style timecode.",
        "palette": [("Ink", "ink"), ("Paper", "paper"), ("Blueberry", "blue"), ("Lupine (REC only)", "pink")], "pal": VF,
        "type": "Instrument Sans Bold for the mark and headlines, IBM Plex Mono for timecodes and captions.",
        "scores": [9, 8, 10, 8, 9, 10, 9],
        "risk": "Corner brackets are a common video motif on their own. The ME inside is what makes it ownable, so the brackets never appear without it in the logo.",
        "aplus": "Commission a custom-drawn ME (a type designer, a few days) and clear the mark with a trademark search. That lifts Distinct and Premium to 9 and the total to A+.",
    },
    {
        "key": "rings", "name": "Growth Rings", "build": build_rings, "bg": RG["fog"], "dark": RG["spruce"], "accent": RG["lupine"],
        "idea": "A tree's cross-section. Each ring is a generation; the outer ring, in Lupine, is this one. Maine is the Pine Tree State, but the mark never draws a tree.",
        "why": ["Generation is the brand's first word. Rings are the most literal picture of generations there is.",
                "Every creator gets a ring pattern of their own, so the system grows with the project.",
                "Keeps the Spruce and Lupine colors the site already uses."],
        "system": "Each creator's avatar is a unique ring pattern drawn from a seed. A season adds a ring. The end card crops a giant cross-section.",
        "palette": [("Spruce", "spruce"), ("Fog", "fog"), ("Lupine", "lupine"), ("Blossom", "blossom")], "pal": RG,
        "type": "Instrument Sans throughout. No second typeface needed.",
        "scores": [9, 8, 7, 9, 9, 8, 10],
        "risk": "Rings fill in below 24 px, so the small version drops to three rings. Tree rings also appear in some sustainability branding, which keeps Distinct at 8.",
        "aplus": "Draw a bolder three-ring favicon by hand and test it on real phone home screens. With Small size at 9 the total reaches A.",
    },
    {
        "key": "woven", "name": "Woven", "build": build_woven, "bg": WV["wool"], "dark": WV["indigo"], "accent": WV["lupine"],
        "idea": "A Generation Maine plaid. Each creator adds one thread color, so the fabric is literally made of the people in it. It nods to Maine's mill towns and to flannel, without any cliché pictures.",
        "why": ["A plaid is registrable and instantly ownable. No neighbor has one.",
                "The best creator story of the three: the plaid is finished when the cohort is.",
                "Works on merch, stickers and backdrops, not only screens."],
        "system": "The master plaid is the brand pattern. Each creator's thread color appears on their lower third and profile. New cohorts add threads.",
        "palette": [("Indigo", "indigo"), ("Wool", "wool"), ("Lupine", "lupine"), ("Moss", "moss")], "pal": WV,
        "type": "Fraunces SemiBold (upright) for the wordmark and headlines, Instrument Sans for everything else.",
        "scores": [9, 9, 7, 9, 8, 7, 10],
        "risk": "Plaid can tip into lumberjack or retail catalog if it is used everywhere. The pattern should frame content, never sit behind text, and the flat weave tile is the logo.",
        "aplus": "Have a textile designer finalize the sett and record it with the Scottish Register of Tartans, and simplify the weave tile for 16 px. That lifts Small size and Ease and the total to A.",
    },
]


def font64(n):
    with open(os.path.join(ROOT, "brand/v2/fonts-web", n), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def build():
    sections, table = "", ""
    for cpt in CONCEPTS:
        s = cpt["build"]()
        for k, v in s.items():
            write("%s/%s/%s.svg" % (OUT, cpt["key"], k), v)
        ov = overall(cpt["scores"])
        pal = cpt["pal"]
        sw = "".join('<div class="sw" style="background:%s;color:%s"><b>%s</b>%s</div>' % (
            pal[k], "#fff" if k in ("ink", "blue", "spruce", "indigo", "moss") else "#121417", n, pal[k]) for n, k in cpt["palette"])
        bars = "".join('<div class="row"><span>%s</span><i><b style="width:%d%%;background:%s"></b></i><em>%d</em></div>' % (
            c[0], v * 10, cpt["dark"], v) for v, c in zip(cpt["scores"], CRIT))
        small = s.get("symbol-small", s["symbol"])
        sections += """
<section class="c" id="%(key)s" style="--bg:%(bg)s;--dark:%(dark)s;--acc:%(acc)s">
  <div class="wrap">
    <div class="head">
      <div><p class="label">Concept %(n)d</p><h2>%(name)s</h2><p class="lede">%(idea)s</p></div>
      <div class="grade"><strong>%(letter)s</strong><span>%(ov).2f / 10 projected</span></div>
    </div>
    <div class="hero">
      <div class="big">%(symbol)s</div>
      <div class="lock"><div class="l1">%(lockup)s</div><div class="l2">%(lockrev)s</div>
        <div class="smalls"><span style="width:64px">%(sm)s</span><span style="width:32px">%(sm)s</span><span style="width:16px">%(sm)s</span></div></div>
    </div>
    <div class="apps">
      <figure class="round">%(avatar)s<figcaption>Avatar</figcaption></figure>
      <figure class="tall">%(end)s<figcaption>9:16 end card</figcaption></figure>
      <figure class="wide lower">%(lower)s<figcaption>Lower third over footage</figcaption></figure>
    </div>
    <div class="sys"><p class="label">Creator system</p><p>%(system)s</p>%(sysimg)s</div>
    <div class="cols">
      <div><p class="label">Why it can reach the A range</p><ul>%(why)s</ul>
        <p class="label" style="margin-top:22px">Color</p><div class="swatches">%(sw)s</div>
        <p class="label" style="margin-top:22px">Type</p><p>%(type)s</p></div>
      <div><p class="label">Projected score</p><div class="bars">%(bars)s</div>
        <p class="label" style="margin-top:22px">Risk</p><p>%(risk)s</p>
        <p class="label" style="margin-top:22px">What gets it to A+</p><p>%(aplus)s</p></div>
    </div>
  </div>
</section>""" % {
            "key": cpt["key"], "bg": cpt["bg"], "dark": cpt["dark"], "acc": cpt["accent"], "n": CONCEPTS.index(cpt) + 1,
            "name": cpt["name"], "idea": cpt["idea"], "letter": letter(ov), "ov": ov,
            "symbol": s["symbol"], "lockup": s["lockup"], "lockrev": s["lockup-rev"], "sm": small,
            "avatar": s["avatar"], "end": s["endcard"], "lower": s["lowerthird"], "system": cpt["system"], "sysimg": s["system"],
            "why": "".join("<li>%s</li>" % w for w in cpt["why"]), "sw": sw, "type": cpt["type"], "bars": bars,
            "risk": cpt["risk"], "aplus": cpt["aplus"]}
        table += "<tr><td><a href='#%s'>%s</a></td>%s<td><b>%.2f</b></td><td><b>%s</b></td></tr>" % (
            cpt["key"], cpt["name"], "".join("<td>%d</td>" % v for v in cpt["scores"]), ov, letter(ov))
    html = (TEMPLATE.replace("{{SECTIONS}}", sections).replace("{{TABLE}}", table)
            .replace("{{CRITH}}", "".join("<th>%s<br><small>%d%%</small></th>" % c for c in CRIT))
            .replace("{{F_SANS}}", font64("instrument-sans.woff2")).replace("{{F_MONO}}", font64("plex-mono-500.woff2"))
            .replace("{{F_FR6}}", font64("fraunces-600.woff2")).replace("{{F_FR4}}", font64("fraunces-400.woff2")))
    write(OUT + "/concepts.html", html)
    for cpt in CONCEPTS:
        print("%-13s %.2f %s" % (cpt["name"], overall(cpt["scores"]), letter(overall(cpt["scores"]))))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine: three A-range concepts</title>
<style>
@font-face{font-family:'Instrument Sans';src:url(data:font/woff2;base64,{{F_SANS}}) format("woff2");font-weight:400 700}
@font-face{font-family:'IBM Plex Mono';src:url(data:font/woff2;base64,{{F_MONO}}) format("woff2");font-weight:400 700}
@font-face{font-family:Fraunces;src:url(data:font/woff2;base64,{{F_FR6}}) format("woff2");font-weight:600}
@font-face{font-family:Fraunces;src:url(data:font/woff2;base64,{{F_FR4}}) format("woff2");font-weight:400}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 'Instrument Sans',system-ui,sans-serif;color:#121417;background:#fff}
.wrap{max-width:1240px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}
.intro{background:#0D0F12;color:#EDF0F4;padding:72px 0 56px}
.intro h1{font:700 clamp(38px,6vw,76px)/1 'Instrument Sans';letter-spacing:-.03em;margin:0 0 18px}
.intro p{max-width:66ch;opacity:.9}
.label{font:600 12px/1 'Instrument Sans';letter-spacing:.16em;text-transform:uppercase;opacity:.65;margin:0 0 10px}
table{border-collapse:collapse;width:100%;margin-top:26px;font-size:14px}
th,td{padding:8px 6px;border-bottom:1px solid rgba(237,240,244,.18);text-align:center}
th:first-child,td:first-child{text-align:left}
th small{opacity:.6;font-weight:500}
td a{color:#FFC2DD}
.aplus{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:30px}
@media(max-width:800px){.aplus{grid-template-columns:1fr}}
.aplus div{border-top:1px solid rgba(237,240,244,.25);padding-top:14px;font-size:14px}
.aplus b{display:block;margin-bottom:4px}
.c{background:var(--bg);padding:72px 0}
.head{display:flex;justify-content:space-between;gap:24px;align-items:flex-start}
.head h2{font:700 clamp(36px,5vw,64px)/1 'Instrument Sans';letter-spacing:-.03em;margin:0 0 12px;color:var(--dark)}
.lede{font-size:19px;max-width:58ch}
.grade{text-align:right;flex:none}
.grade strong{display:block;font:700 72px/1 'Instrument Sans';color:var(--dark)}
.grade span{font-size:13px;opacity:.7}
.hero{display:grid;grid-template-columns:1fr 1.4fr;gap:28px;margin-top:34px;align-items:center}
@media(max-width:860px){.hero{grid-template-columns:1fr}}
.big{background:#fff;border-radius:20px;padding:48px;display:grid;place-items:center}
.big svg{width:min(260px,100%);height:auto}
.lock{display:grid;gap:16px}
.l1,.l2{border-radius:16px;padding:28px;background:#fff}
.l2{background:var(--dark)}
.lock svg{width:100%;max-width:520px;height:auto;display:block}
.smalls{display:flex;gap:18px;align-items:flex-end}
.smalls span svg{width:100%;height:auto;display:block}
.apps{display:grid;grid-template-columns:1fr .7fr 1.6fr;gap:22px;margin-top:28px;align-items:start}
@media(max-width:860px){.apps{grid-template-columns:1fr 1fr}.apps .lower{grid-column:1/-1}}
.apps figure{margin:0}
.apps svg{width:100%;height:auto;display:block;border-radius:14px;box-shadow:0 12px 40px -20px rgba(0,0,0,.45)}
.apps .round svg{border-radius:50%}
.apps .lower svg{background:linear-gradient(135deg,#3b4a42,#6b7a70 55%,#2a3530)}
figcaption{font:600 11px/1 'Instrument Sans';letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.sys{background:#fff;border-radius:18px;padding:24px;margin-top:28px}
.sys svg{width:100%;height:auto;display:block;margin-top:10px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-top:30px}
@media(max-width:860px){.cols{grid-template-columns:1fr}}
ul{padding-left:18px;margin:0}
li{margin-bottom:6px}
.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.sw{border-radius:12px;padding:12px;min-height:88px;display:flex;flex-direction:column;justify-content:flex-end;font-size:12px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.sw b{font-size:14px}
.bars .row{display:grid;grid-template-columns:86px 1fr 20px;gap:8px;align-items:center;font-size:13px;margin:4px 0}
.bars i{display:block;height:9px;background:rgba(0,0,0,.08);border-radius:99px;overflow:hidden}
.bars b{display:block;height:100%;border-radius:99px}
.bars em{font-style:normal;font-weight:700;text-align:right}
.note{background:#0D0F12;color:#EDF0F4;padding:56px 0}
</style></head><body>
<section class="intro"><div class="wrap">
  <p class="label">Generation Maine · Identity v3 · three concepts</p>
  <h1>Built for the A range.</h1>
  <p>Same seven criteria as the scorecard. An A+ needs 9s almost everywhere, and above all in distinctiveness: nothing Baxter, Green Falls or 76crew already owns (no orange, no sun, no mountain, no Maine outline, no round badge, no lime, no navy and red). Each concept below starts from what the project actually is: young people, their phones, their own voices, their towns.</p>
  <table><tr><th>Concept</th>{{CRITH}}<th>Total</th><th>Grade</th></tr>{{TABLE}}</table>
  <div class="aplus">
    <div><b>Why none is marked A+ yet</b>A designer grading their own concepts is not evidence. A+ should be earned with outside proof, not projected.</div>
    <div><b>The proof that moves a concept to A+</b>A trademark knockout search, a five-minute test with 8 to 10 young Mainers (which mark do you remember, what does it say), and a custom-drawn final mark.</div>
    <div><b>What stays the same</b>No italics, no em dashes, OFL fonts only, hand-built SVG, "An initiative of Maine Policy Institute" on every piece.</div>
  </div>
</div></section>
{{SECTIONS}}
<section class="note"><div class="wrap">
  <p class="label">Recommendation</p>
  <p style="font-size:20px;max-width:60ch">Show all three. Lead with Viewfinder: it has the highest projected score, it is the easiest for a small team, and it is the most clearly about young people making their own videos. Growth Rings is the safest continuation of the current site colors. Woven is the boldest and the best for merch.</p>
</div></section>
</body></html>
"""

if __name__ == "__main__":
    build()
