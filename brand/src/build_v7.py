"""Identity v7: "Big House, Little House, Back House, Barn".

Maine's connected farms joined house, ell, shed and barn into one line. Historian Thomas Hubka
showed they were built that way to make a living as the economy changed, not to reach the barn in
the snow. Generation Maine is young people doing the same thing now. The brand draws its shapes from
that elevation: the farm line, four building modules, lit windows and clapboard.

  python3 brand/src/build_v7.py            # marks, social, website
  node brand/src/render_v7.mjs             # PNGs, website screenshots, axe check
  python3 brand/src/build_v7.py present    # presentation with screenshots and results embedded
"""
import json
import os
import sys

from gmlib import ROOT, write
from build_brand import DISPLAY, TRACK, DOT_R, DOT_CY
from build_v4 import placed, rect, text, svg, f, HANDLES
from build_v6 import C, ratio, sat, V5, fonts_css, fill, inline, b64

OUT = "brand/v7"
H = 88  # farm elevation height in grid units; width is 200


# ------------------------------------------------------------------ the farm
def _p(pts, x, y, k):
    return "M" + " L".join("%s %s" % (f(x + px * k), f(y + (H - py) * k)) for px, py in pts) + " Z"


# Elevation, 200 x 88 grid, measured from the ground up. Pitches follow a 12/12 Maine roof.
BIG = [(0, 0), (0, 46), (28, 76), (56, 46), (56, 0)]
CHIMNEY = [(35, 64), (35, 84), (43, 84), (43, 56)]
ELL = [(58, 0), (58, 40), (100, 34), (100, 0)]
BACK = [(102, 0), (102, 30), (136, 26), (136, 0)]
BARN = [(138, 0), (138, 52), (169, 86), (200, 52), (200, 0)]
BARN_DOOR = [(154, 0), (154, 30), (184, 30), (184, 0)]
WINDOW = (12, 38, 12, 15)  # x, top (from ground), w, h


def farm(x, y, w, fill_, lit, door=None):
    """The farm line. door= fills the barn door opening (use the background color)."""
    k = w / 200.0
    d = " ".join(_p(s, x, y, k) for s in (BIG, CHIMNEY, ELL, BACK, BARN))
    out = '<path fill="%s" d="%s"/>' % (fill_, d)
    wx, wt, ww, wh = WINDOW
    out += rect(x + wx * k, y + (H - wt) * k, ww * k, wh * k, lit)
    if door:
        out += '<path fill="%s" d="%s"/>' % (door, _p(BARN_DOOR, x, y, k))
    return out


def farm_line(x, y, w, stroke, sw=1.2, labels=None, lit=None):
    """Elevation drawing in line, with optional labels under each building."""
    k = w / 200.0
    d = " ".join(_p(s, x, y, k) for s in (BIG, CHIMNEY, ELL, BACK, BARN, BARN_DOOR))
    out = '<path fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" d="%s"/>' % (stroke, sw, d)
    wx, wt, ww, wh = WINDOW
    out += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        f(x + wx * k), f(y + (H - wt) * k), f(ww * k), f(wh * k), lit or "none", stroke, sw)
    out += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (f(x - 6 * k), f(y + H * k), f(x + 206 * k), f(y + H * k), stroke, sw)
    if labels:
        for cx, lab, dy in ((28, "BIG HOUSE", 0), (79, "LITTLE HOUSE", 1), (119, "BACK HOUSE", 0), (169, "BARN", 1)):
            px = x + cx * k
            drop = dy * labels * 1.6
            out += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (f(px), f(y + H * k + 4), f(px), f(y + H * k + 8 + drop), stroke, sw)
            out += text(px, y + H * k + 10 + labels + drop, lab, labels, stroke, weight=600, anchor="middle", ls=0.06)
    return out


def icon(x, y, s, bg, fg, lit):
    """Small mark: the big house and its ell, the first addition."""
    k = s / 200.0
    base = 160
    big = [(34, 0), (34, 64), (74, 106), (114, 64), (114, 0)]
    chim = [(86, 92), (86, 124), (98, 124), (98, 80)]
    ell = [(118, 0), (118, 56), (172, 46), (172, 0)]

    def pp(pts):
        return "M" + " L".join("%s %s" % (f(x + px * k), f(y + (base - py) * k)) for px, py in pts) + " Z"
    out = rect(x, y, s, s, bg) if bg else ""
    out += '<path fill="%s" d="%s %s %s"/>' % (fg, pp(big), pp(chim), pp(ell))
    out += rect(x + 52 * k, y + (base - 52) * k, 18 * k, 22 * k, lit)
    return out


# ------------------------------------------------------------------ wordmark with a lit window for a tittle
def wm_window(txt, size, x, y, fg, lit, dot_index):
    s = size / DISPLAY.upem
    t = txt[:dot_index] + "ı" + txt[dot_index + 1:]
    d, w = DISPLAY.path(t, size, x, y, TRACK)
    pos = [p for p in DISPLAY.glyph_positions(t, size, x, TRACK) if p[2] == dot_index][0]
    b = DISPLAY.glyph_bounds("dotlessi")
    cx = pos[1] + (b[0] + b[2]) / 2 * s
    cy = y - DOT_CY * s
    r = DOT_R * s * 0.9
    return '<path fill="%s" d="%s"/>' % (fg, d) + rect(cx - r, cy - r * 1.1, 2 * r, 2.2 * r, lit), w


def wordmark(fg, lit, size=100):
    b, w = wm_window("Generation Maine", size, 0, size * 0.74, fg, lit, 13)
    return b, w, size * 0.78


def wordmark_stacked(fg, lit, size=100):
    d, w1 = DISPLAY.path("Generation", size, 0, size * 0.74, TRACK)
    b2, w2 = wm_window("Maine", size, 0, size * 1.58, fg, lit, 2)
    return '<path fill="%s" d="%s"/>' % (fg, d) + b2, max(w1, w2), size * 1.62


def lockup_farm(fg, lit, door):
    """Primary lockup: the farm line standing on the stacked wordmark, same width."""
    wm, w, h = wordmark_stacked(fg, lit)
    fh = H * w / 200.0
    return farm(0, 0, w, fg, lit, door) + placed(wm, 0, fh + 26, 1), w, fh + 26 + h


def lockup_h(fg, lit, bg):
    wm, w, h = wordmark(fg, lit)
    s = 104
    return icon(0, -8, s, None, fg, lit) + placed(wm, s + 18, 8, 1), s + 18 + w, s - 8


def build_marks():
    m = {}
    for suf, fg, bg in (("", C["spruce"], C["birch"]), ("-reversed", C["birch"], C["spruce"])):
        b, w, h = lockup_farm(fg, C["marigold"], bg)
        m["lockup" + suf] = svg(w, h, b, "Generation Maine")
        b, w, h = lockup_h(fg, C["marigold"], bg)
        m["lockup-h" + suf] = svg(w, h, b, "Generation Maine")
        b, w, h = wordmark(fg, C["marigold"])
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        m["farm" + suf] = svg(200, H, farm(0, 0, 200, fg, C["marigold"], bg), "Generation Maine")
    m["icon"] = svg(200, 200, icon(0, 0, 200, C["spruce"], C["birch"], C["marigold"]), "Generation Maine")
    m["icon-light"] = svg(200, 200, icon(0, 0, 200, C["birch"], C["spruce"], C["marigold"]), "Generation Maine")
    m["icon-marigold"] = svg(200, 200, icon(0, 0, 200, C["marigold"], C["ink"], C["birch"]), "Generation Maine")
    m["elevation"] = svg(220, 150, farm_line(10, 10, 200, C["spruce"], 0.9, labels=7, lit=C["marigold"]), "Big house, little house, back house, barn")
    for k, v in m.items():
        write("%s/logo/%s.svg" % (OUT, k), v)
    return m


# ------------------------------------------------------------------ textures
def clapboard(w, h, gap, color, op=1.0, shadow=None):
    """Clapboard siding: evenly spaced boards, each with a thin shadow line under the lap."""
    out = []
    y = gap
    while y < h:
        out.append(rect(0, y, w, 1.2, color))
        if shadow:
            out.append(rect(0, y + 1.2, w, 2.4, shadow))
        y += gap
    return '<g opacity="%s">%s</g>' % (op, "".join(out))


# ------------------------------------------------------------------ social
def build_social():
    s = {}
    s["avatar"] = svg(1080, 1080, icon(0, 0, 1080, C["spruce"], C["birch"], C["marigold"]), "Avatar")

    e = rect(0, 0, 1080, 1920, C["spruce"]) + clapboard(1080, 1500, 34, "#154F3C")
    wm, w, h = wordmark_stacked(C["birch"], C["marigold"])
    e += placed(wm, 80, 170, 920 / w)
    e += text(80, 700, "Follow along", 92, C["marigold"], "Bric", 800, ls=-0.02)
    y = 830
    for lab, hd in HANDLES:
        e += rect(80, y - 28, 22, 26, C["marigold"])
        e += text(126, y, lab, 40, C["birch"], weight=700)
        e += text(430, y, hd, 40, C["birch"], weight=400)
        e += rect(80, y + 30, 920, 1, "#2E6450")
        y += 92
    e += rect(0, 1560, 1080, 360, C["birch"])
    e += farm(360, 1560 - H * 3.6, 720, C["birch"], C["marigold"], C["spruce"])
    e += text(80, 1760, "An initiative of", 30, C["spruce"], weight=600)
    e += text(80, 1806, "Maine Policy Institute", 30, C["spruce"], weight=700)
    s["endcard"] = svg(1080, 1920, e, "End card")

    lt = rect(96, 790, 1100, 100, C["birch"]) + rect(96, 790, 100, 152, C["spruce"])
    lt += icon(96, 790, 100, None, C["birch"], C["marigold"])
    lt += text(224, 856, "[Creator name]", 52, C["ink"], "Bric", 800, ls=-0.01)
    lt += rect(196, 890, 1000, 52, C["spruce"])
    lt += text(224, 925, "[HOMETOWN], MAINE", 25, C["birch"], weight=600, ls=0.08)
    lt += text(1170, 925, "GENERATION MAINE", 25, C["marigold"], weight=700, anchor="end", ls=0.08)
    s["lowerthird"] = svg(1920, 1080, lt, "Chyron lower third")

    o = rect(0, 0, 1200, 630, C["spruce"]) + clapboard(1200, 630, 22, "#154F3C")
    b, w, h = lockup_h(C["birch"], C["marigold"], C["spruce"])
    o += placed(b, 80, 90, 520 / w)
    o += text(82, 300, "Young Mainers on building", 50, C["birch"], "Bric", 800, ls=-0.02)
    o += text(82, 360, "a life here", 50, C["birch"], "Bric", 800, ls=-0.02)
    o += rect(0, 560, 1200, 70, C["birch"])
    o += farm(620, 560 - H * 2.9, 580, C["birch"], C["marigold"], C["spruce"])
    o += text(82, 605, "An initiative of Maine Policy Institute", 22, C["spruce"], weight=600)
    s["og"] = svg(1200, 630, o, "Share card")

    # 4:5 post announcing a creator. The gable is the frame for their portrait.
    p = rect(0, 0, 1080, 1350, C["birch"])
    gx, gy, gw, gh = 180, 170, 720, 900
    gable = "M%s %s V%s L%s %s L%s %s V%s Z" % (gx, gy + gh, gy + 300, gx + gw / 2, gy, gx + gw, gy + 300, gy + gh)
    p += '<clipPath id="pg"><path d="%s"/></clipPath><path d="%s" fill="%s"/>' % (gable, gable, C["spruce"])
    p += '<g clip-path="url(#pg)"><g transform="translate(%s %s)">%s</g></g>' % (gx, gy, clapboard(gw, gh, 30, "#154F3C"))
    p += rect(gx + 120, gy + 380, 110, 140, C["marigold"])
    p += text(gx + gw / 2, gy + 700, "Meet [Creator name]", 60, C["birch"], "Bric", 800, anchor="middle", ls=-0.015)
    p += text(gx + gw / 2, gy + 770, "[HOMETOWN], MAINE", 28, C["sage"], weight=600, anchor="middle", ls=0.08)
    p += icon(80, 50, 80, None, C["spruce"], C["marigold"])
    p += text(1000, 100, "GENERATION MAINE", 24, C["spruce"], weight=700, anchor="end", ls=0.08)
    p += text(540, 1200, "Portrait goes in the gable. The window lights when their first video is out.", 24, C["stone"], weight=500, anchor="middle")
    s["post"] = svg(1080, 1350, p, "Feed post")
    for k, v in s.items():
        write("%s/social/%s.svg" % (OUT, k), v)
    return s


# ------------------------------------------------------------------ website
def build_site(m):
    farm_hero = svg(200, H, farm(0, 0, 200, C["birch"], C["marigold"], C["spruce"]), "")
    farm_foot = svg(200, H, farm(0, 0, 200, "#123F30", "#123F30", C["pine"]), "")
    html = fill(SITE, {
        "{{FONTS}}": fonts_css(),
        "{{ICON}}": inline(svg(200, 200, icon(0, 0, 200, None, C["birch"], C["marigold"]), "Generation Maine"), "mk"),
        "{{WM_REV}}": inline(m["wordmark-reversed"], "wm"),
        "{{FARM_HERO}}": inline(farm_hero, "farm"),
        "{{ELEVATION}}": inline(svg(224, 150, farm_line(12, 12, 200, C["spruce"], 0.8, labels=6.5, lit=C["marigold"]), ""), "elev"),
        "{{LOCK_FOOT}}": inline(m["lockup-reversed"].replace(C["spruce"], C["pine"]), "lock-foot"),
        "{{FARM_FOOT}}": inline(farm_foot, "farm-foot"),
    })
    write(OUT + "/site/index.html", html)


SITE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine | Young Mainers on building a life here</title>
<meta name="description" content="Short videos by young Maine creators about the rules that shape their lives. An initiative of Maine Policy Institute.">
<style>
{{FONTS}}
:root{--sp:{{spruce}};--pine:{{pine}};--bi:{{birch}};--ink:{{ink}};--mg:{{marigold}};--sage:{{sage}};--moss:{{moss}};--stone:{{stone}};--g:clamp(20px,5vw,72px);--ease:cubic-bezier(.2,.7,.2,1);
  --clap:repeating-linear-gradient(180deg,transparent 0 33px,rgba(244,240,230,.055) 33px 34px,rgba(0,0,0,.09) 34px 36px)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font:18px/1.65 Inter,system-ui,sans-serif;color:var(--ink);background:var(--bi);-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:3px solid var(--mg);outline-offset:3px;border-radius:2px}
.skip{position:absolute;left:-999px;top:8px;background:var(--mg);color:var(--ink);padding:10px 16px;z-index:50;font-weight:700}
.skip:focus{left:12px}
.w{max-width:1280px;margin:0 auto;padding:0 var(--g)}
h1,h2,h3{font-family:Bric;margin:0;font-weight:700;letter-spacing:-.02em}
.win{display:inline-block;width:.46em;height:.56em;background:var(--mg);flex:none}
.win.off{background:transparent;box-shadow:inset 0 0 0 1.5px currentColor;opacity:.55}
.label{display:flex;align-items:center;gap:10px;margin:0;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--moss)}
.label .n{color:var(--stone);font-variant-numeric:tabular-nums}
.on-dark .label{color:var(--sage)}
.on-dark .label .n{color:#A9BCB2}

header{position:sticky;top:0;z-index:20;background:var(--sp);color:var(--bi);border-bottom:1px solid #1D5843}
header .w{display:flex;align-items:center;justify-content:space-between;height:76px;gap:20px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand .mk{width:42px;height:42px}
.brand .wm{height:21px;width:auto}
nav ul{display:flex;align-items:center;gap:30px;list-style:none;margin:0;padding:0;font-weight:600;font-size:16px}
nav a{text-decoration:none;padding:6px 0;background:linear-gradient(var(--mg),var(--mg)) 0 100%/0 2px no-repeat;transition:background-size .3s var(--ease)}
nav a:hover{background-size:100% 2px}
.status{display:inline-flex;align-items:center;gap:9px;font:600 13px/1 Inter;letter-spacing:.06em;text-transform:uppercase;color:#C9D6CF}
@media (max-width:720px){.hide-s{display:none}nav ul{gap:20px}.brand .wm{display:none}}

.hero{background:var(--sp) var(--clap);color:var(--bi);position:relative;padding-top:clamp(56px,8vw,104px)}
.hero .w{display:grid;grid-template-columns:1.3fr .7fr;gap:clamp(28px,5vw,80px);align-items:end}
@media (max-width:900px){.hero .w{grid-template-columns:1fr}}
.hero .label{color:var(--mg)}
h1{font-weight:800;font-size:clamp(50px,8vw,120px);line-height:.94;letter-spacing:-.03em;margin:24px 0 0;max-width:10.5ch}
.hero p.lede{font-size:clamp(19px,1.6vw,22px);line-height:1.55;margin:0 0 30px;color:#E6E4DA;max-width:32ch}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:16px 24px;font-weight:700;font-size:17px;line-height:1.2;text-decoration:none;border-radius:3px;transition:transform .2s var(--ease)}
.btn:hover{transform:translateY(-2px)}
.btn.mg{background:var(--mg);color:var(--ink)}
.btn.ol{box-shadow:inset 0 0 0 1.5px #9DB5A9;color:var(--bi)}
.btn.sp{background:var(--sp);color:var(--bi)}
.btn.ink{background:var(--ink);color:var(--bi)}
.horizon{position:relative;margin-top:clamp(48px,7vw,96px);height:clamp(110px,19vw,270px)}
.horizon .farm{position:absolute;right:var(--g);bottom:-1px;height:100%;width:auto;max-width:calc(100% - 2*var(--g))}
.horizon::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--bi)}
.horizon .cap{position:absolute;left:var(--g);bottom:18px;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:#C9D6CF;max-width:34ch}
@media (max-width:700px){.horizon .cap{display:none}}

section{padding:clamp(72px,10vw,136px) 0}
h2{font-size:clamp(38px,5.2vw,72px);line-height:1;margin:20px 0 0;max-width:15ch}
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(40px,7vw,112px);align-items:start}
@media (max-width:900px){.split{grid-template-columns:1fr}}
.body p{margin:0 0 18px;max-width:58ch}
.body p.big{font-size:clamp(20px,1.8vw,24px);line-height:1.5}
.plan{border-top:5px solid var(--sp);padding-top:5px}
.plan::before{content:"";display:block;border-top:1px solid var(--sp)}
.plan .elev{width:100%;height:auto;display:block;margin:28px 0 8px}
.plan p{font-size:15px;line-height:1.6;color:#46524B;margin:0;max-width:52ch}
.plan p b{color:var(--ink)}

.creators{background:var(--sage)}
.head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(36px,5vw,64px)}
.head p{max-width:40ch;margin:0;color:#34413A}
.creators .label .n{color:#44514A}
.row{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(0,.9fr) minmax(0,.8fr) minmax(0,1.18fr);gap:6px;align-items:end;list-style:none;margin:0;padding:0;border-bottom:3px solid var(--sp)}
.bld{position:relative;background:var(--sp) var(--clap);color:var(--bi);display:flex;flex-direction:column;justify-content:flex-end}
.bld.big{aspect-ratio:1/1.5;clip-path:polygon(0 100%,0 34%,50% 5%,64% 13%,64% 0,76% 0,76% 20%,100% 34%,100% 100%)}
.bld.ell{aspect-ratio:1/1.12;clip-path:polygon(0 100%,0 6%,100% 16%,100% 100%)}
.bld.back{aspect-ratio:1/1;clip-path:polygon(0 100%,0 8%,100% 16%,100% 100%)}
.bld.barn{aspect-ratio:1/1.34;clip-path:polygon(0 100%,0 32%,50% 0,100% 32%,100% 100%)}
.bld .window{position:absolute;left:18%;top:44%;width:17%;aspect-ratio:12/15;box-shadow:inset 0 0 0 2px #4E7A6A}
.bld.ell .window,.bld.back .window{top:26%}
.bld.barn .window{left:auto;right:18%}
.bld .num{position:absolute;right:14px;top:auto;bottom:112px;font:800 clamp(44px,4.6vw,72px)/1 Bric;letter-spacing:-.04em;color:#2F6A55}
.chy{background:var(--bi);color:var(--ink);border-left:6px solid var(--mg);margin:0 10px 10px}
.chy b{display:block;font:700 clamp(16px,1.4vw,20px)/1.15 Bric;padding:11px 12px 8px}
.chy span{display:block;background:var(--pine);color:var(--bi);font:600 12px/1 Inter;letter-spacing:.06em;text-transform:uppercase;padding:9px 12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:900px){.row{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:28px;border-bottom:0}.bld{border-bottom:3px solid var(--sp)}.bld .num{display:none}.chy{margin:0 6px 6px}.chy b{padding:9px 9px 7px}.chy span{white-space:normal;line-height:1.3;padding:7px 9px;letter-spacing:.04em}}
.soon{margin-top:22px;font-size:15px;color:#34413A;display:flex;gap:10px;align-items:center}
.soon .win.off{color:var(--sp);opacity:.8}

.season{background:var(--pine);color:var(--bi)}
.season .split p{color:#D5DED9;max-width:44ch;margin:0}
.street{list-style:none;margin:clamp(40px,5vw,64px) 0 0;padding:0;display:grid;grid-template-columns:repeat(12,1fr);gap:10px}
.street li{display:flex;flex-direction:column;gap:12px;font:600 12px/1 Inter;letter-spacing:.06em;color:#A9BCB2}
.street li i{display:block;aspect-ratio:12/15;box-shadow:inset 0 0 0 2px #3F6D5D;background:linear-gradient(#3F6D5D,#3F6D5D) 50% 0/2px 100% no-repeat,linear-gradient(#3F6D5D,#3F6D5D) 0 50%/100% 2px no-repeat}
.street li.on i{background:var(--mg);box-shadow:none}
.street li.on{color:var(--bi)}
@media (max-width:700px){.street{grid-template-columns:repeat(6,1fr);row-gap:22px}}

.follow .split{align-items:end}
.chan{list-style:none;padding:0;margin:36px 0 0;border-top:5px solid var(--ink)}
.chan a{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 4px;border-bottom:1px solid #CFCBC0;text-decoration:none;font:700 clamp(26px,3vw,40px)/1 Bric;letter-spacing:-.015em;transition:padding .25s var(--ease),color .2s}
.chan a:hover{padding-left:14px;color:var(--sp)}
.chan a small{font:500 16px/1 Inter;letter-spacing:0;color:var(--stone)}
.sub{background:var(--mg);clip-path:polygon(0 100%,0 30%,50% 0,100% 30%,100% 100%);padding:clamp(150px,15vw,210px) clamp(28px,4vw,56px) clamp(32px,4vw,48px);display:flex;flex-direction:column;min-height:clamp(420px,42vw,560px);justify-content:flex-end;position:relative}
.sub::before{content:"";position:absolute;left:50%;top:clamp(90px,10vw,130px);width:clamp(40px,4vw,56px);aspect-ratio:12/15;background:var(--ink);transform:translateX(-50%)}
.sub h3{font-size:clamp(32px,3.4vw,48px);line-height:1;letter-spacing:-.02em;font-weight:800}
.sub p{margin:14px 0 26px;max-width:40ch}
.sub .btn{align-self:flex-start}

.mpi{padding-top:0}
.mpi .plan{margin-bottom:28px;border-top-color:var(--sp)}
.mpi h2{font-size:clamp(32px,3.8vw,52px)}
.conf{background:#E7E1D2;padding:2px 7px;font-size:.9em}

footer{background:var(--pine);color:var(--bi);padding:clamp(56px,7vw,88px) 0 36px;position:relative;overflow:hidden}
footer .farm-foot{position:absolute;right:-2%;bottom:0;height:78%;width:auto;pointer-events:none;opacity:.7}
@media (max-width:700px){footer .farm-foot{display:none}}
footer .w{position:relative;z-index:1}
footer .top{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;flex-wrap:wrap}
.lock-foot{width:min(300px,64vw);height:auto;display:block}
footer ul{list-style:none;margin:0;padding:0;display:flex;gap:10px 28px;flex-wrap:wrap;font-weight:600}
footer ul a{text-decoration:none;border-bottom:2px solid #3C6D5C;padding-bottom:3px}
footer ul a:hover{border-color:var(--mg)}
footer .fine{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:44px;padding-top:18px;border-top:1px solid #2D5B4B;font-size:14px;color:#B7C6BE}
</style></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="w">
  <a class="brand" href="#" aria-label="Generation Maine, home">{{ICON}}{{WM_REV}}</a>
  <nav aria-label="Main"><ul><li class="hide-s"><a href="#about">About</a></li><li><a href="#creators">Creators</a></li><li><a href="#follow">Follow</a></li>
    <li class="hide-s"><span class="status"><span class="win" aria-hidden="true"></span>Season one coming soon</span></li></ul></nav>
</div></header>

<main id="main">
<section class="hero on-dark" aria-labelledby="h1" style="padding-bottom:0"><div class="w">
  <div><p class="label"><span class="win" aria-hidden="true"></span>An initiative of Maine Policy Institute</p>
    <h1 id="h1">Young Mainers on building a life here</h1></div>
  <div><p class="lede">Short videos by young Maine creators about the rules that shape their lives.</p>
    <div class="btns"><a class="btn mg" href="#creators">Meet the creators</a><a class="btn ol" href="#follow">Follow along</a></div></div>
</div>
<div class="horizon" aria-hidden="true"><span class="cap">Big house, little house, back house, barn</span>{{FARM_HERO}}</div>
</section>

<section id="about" aria-labelledby="h-about" style="padding-top:clamp(56px,7vw,96px)"><div class="w split">
  <div class="body">
    <p class="label"><span class="n">01</span> What it is</p>
    <h2 id="h-about">A storytelling project made by young Mainers</h2>
    <p class="big" style="margin-top:32px">Generation Maine is a group of 8 to 12 young content creators from across the state. Each one makes short videos about their own life in Maine.</p>
    <p>The videos show how economic rules affect everyday choices. Some are about finding a place to live. Others are about getting a job, starting a business or deciding whether to stay.</p>
    <p>The creators tell their own stories. You can watch them on social media and read more on our Substack.</p>
  </div>
  <figure class="plan" style="margin:0">
    {{ELEVATION}}
    <figcaption><p><b>Why a farm.</b> In the 1800s, Maine farm families joined house, ell, shed and barn into one line. Historian Thomas Hubka found they did it to make a living as the economy changed, adding home work like cheese and candle making. Young Mainers are still adding on.</p></figcaption>
  </figure>
</div></section>

<section id="creators" class="creators" aria-labelledby="h-cr"><div class="w">
  <div class="head"><div><p class="label"><span class="n">02</span> The creators</p><h2 id="h-cr">Meet the creators</h2></div>
    <p>Eight to twelve young Mainers from different towns. Together they make one connected line, like the farms.</p></div>
  <ul class="row">
    <li class="bld big"><span class="window" aria-hidden="true"></span><span class="num" aria-hidden="true">01</span><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="bld ell"><span class="window" aria-hidden="true"></span><span class="num" aria-hidden="true">02</span><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="bld back"><span class="window" aria-hidden="true"></span><span class="num" aria-hidden="true">03</span><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="bld barn"><span class="window" aria-hidden="true"></span><span class="num" aria-hidden="true">04</span><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
  </ul>
  <p class="soon"><span class="win off" aria-hidden="true"></span>Each window lights up when that creator's first video is out.</p>
</div></section>

<section class="season on-dark" aria-labelledby="h-s"><div class="w">
  <div class="split"><div><p class="label"><span class="n">03</span> Season one</p><h2 id="h-s">One story at a time</h2></div>
    <p>New videos come out through the season. Each window is an episode. The first one is on its way.</p></div>
  <ol class="street" aria-label="Season one episodes, none released yet">
    <li><i></i>EP 01</li><li><i></i>EP 02</li><li><i></i>EP 03</li><li><i></i>EP 04</li><li><i></i>EP 05</li><li><i></i>EP 06</li>
    <li><i></i>EP 07</li><li><i></i>EP 08</li><li><i></i>EP 09</li><li><i></i>EP 10</li><li><i></i>EP 11</li><li><i></i>EP 12</li></ol>
</div></section>

<section id="follow" class="follow" aria-labelledby="h-f"><div class="w split">
  <div><p class="label"><span class="n">04</span> Follow</p><h2 id="h-f">Follow along</h2>
    <ul class="chan">
      <li><a href="#follow">Instagram <small>[@handle]</small></a></li>
      <li><a href="#follow">TikTok <small>[@handle]</small></a></li>
      <li><a href="#follow">YouTube <small>[@handle]</small></a></li>
    </ul></div>
  <div class="sub"><h3>Read the Substack</h3><p>Get new stories from the creators by email.</p><a class="btn ink" href="#follow">Subscribe on Substack</a></div>
</div></section>

<section class="mpi" aria-labelledby="h-m"><div class="w">
  <div class="plan"></div>
  <div class="split"><div><p class="label"><span class="n">05</span> Who is behind this</p><h2 id="h-m">About Maine Policy Institute</h2></div>
  <div class="body"><p class="big">Generation Maine is an initiative of Maine Policy Institute.</p>
    <p><span class="conf">[CONFIRM: one sentence about Maine Policy Institute]</span></p>
    <p>Press: <span class="conf">[CONFIRM: press email]</span></p>
    <a class="btn sp" href="https://mainepolicy.org/">Visit Maine Policy Institute</a></div></div>
</div></section>
</main>

<footer class="on-dark">{{FARM_FOOT}}<div class="w">
  <div class="top">{{LOCK_FOOT}}<ul><li><a href="#follow">Instagram</a></li><li><a href="#follow">TikTok</a></li><li><a href="#follow">YouTube</a></li><li><a href="#follow">Substack</a></li></ul></div>
  <div class="fine"><span>An initiative of Maine Policy Institute</span><span>© 2026 Generation Maine</span></div>
</div></footer>
</body></html>
"""


# ------------------------------------------------------------------ presentation
def build_present(m, social):
    qp = os.path.join(ROOT, OUT, "site", "qa.json")
    viol = json.load(open(qp)).get("violations", "not run") if os.path.exists(qp) else "not run"
    sizes = "".join('<span style="width:%dpx">%s</span>' % (p, m["icon"]) for p in (128, 64, 32, 24, 16))
    html = fill(PRESENT, {
        "{{FONTS}}": fonts_css(),
        "{{LOCK}}": m["lockup"], "{{LOCK_REV}}": m["lockup-reversed"], "{{LOCK_H}}": m["lockup-h"], "{{LOCK_H_REV}}": m["lockup-h-reversed"],
        "{{FARM}}": m["farm"], "{{FARM_REV}}": m["farm-reversed"], "{{ICON}}": m["icon"], "{{ICON_L}}": m["icon-light"], "{{ICON_M}}": m["icon-marigold"],
        "{{ELEV}}": m["elevation"], "{{SIZES}}": sizes,
        "{{AVATAR}}": social["avatar"], "{{END}}": social["endcard"], "{{LOWER}}": social["lowerthird"], "{{OG}}": social["og"], "{{POST}}": social["post"],
        "{{DESK}}": b64(OUT + "/site/desktop.png"), "{{MOB}}": b64(OUT + "/site/mobile-sheet.png"), "{{AXE}}": str(viol),
        "{{CLAP}}": svg(300, 170, rect(0, 0, 300, 170, C["spruce"]) + clapboard(300, 170, 17, "#1D5843", shadow="#0D3A2B"), ""),
    })
    write(OUT + "/big-house.html", html)


PRESENT = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine Identity</title>
<style>
{{FONTS}}
*{box-sizing:border-box}
body{margin:0;font:17px/1.65 Inter,system-ui,sans-serif;color:{{ink}};background:{{birch}};-webkit-font-smoothing:antialiased}
.w{max-width:1200px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}
section{padding:clamp(64px,8vw,104px) 0;border-bottom:1px solid #E1DBCC}
h1,h2,h3{font-family:Bric;margin:0;letter-spacing:-.02em}
h1{font-weight:800;font-size:clamp(44px,7vw,96px);line-height:.95;letter-spacing:-.03em;max-width:12ch}
h2{font-weight:700;font-size:clamp(34px,4.4vw,56px);line-height:1.02;margin:14px 0 18px;max-width:18ch}
h3{font-weight:700;font-size:22px;margin-bottom:6px}
p{max-width:64ch}
.label{display:flex;align-items:center;gap:10px;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{moss}};margin:0}
.win{display:inline-block;width:.5em;height:.62em;background:{{marigold}}}
.dark{background:{{spruce}};color:{{birch}}}
.dark .label{color:{{marigold}}}
.dark p{color:#E2E2D8}
.cover{padding-bottom:0}
.cover svg.f{display:block;width:100%;height:auto;margin-top:56px}
.panel{background:#fff;padding:clamp(20px,3vw,36px)}
.panel.sp{background:{{spruce}}}.panel.mg{background:{{marigold}}}.panel.sage{background:{{sage}}}
.panel svg,figure svg{display:block;width:100%;height:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:860px){.g2,.g3{grid-template-columns:1fr}}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:36px}
@media(max-width:860px){.cols{grid-template-columns:1fr}}
.cols div{border-top:5px solid {{marigold}};padding-top:14px}
.quote{font:700 clamp(24px,2.6vw,34px)/1.2 Bric;letter-spacing:-.015em;max-width:30ch;margin:28px 0 8px}
.src{font-size:14px;color:{{stone}}}
.smalls{display:flex;align-items:flex-end;gap:22px;flex-wrap:wrap}
.smalls span svg{width:100%;height:auto}
.el{display:grid;grid-template-columns:320px 1fr;gap:32px;align-items:center;padding:28px 0;border-top:1px solid #E1DBCC}
@media(max-width:860px){.el{grid-template-columns:1fr}}
.demo{min-height:170px;display:grid;place-items:center;overflow:hidden;padding:20px}
.demo svg{width:100%;height:auto;display:block}
.apps{display:grid;grid-template-columns:.9fr .55fr .8fr;gap:22px;align-items:start}
@media(max-width:860px){.apps{grid-template-columns:1fr 1fr}}
figure{margin:0}
.apps svg,.g2 figure svg{box-shadow:0 14px 40px -24px rgba(11,43,33,.55)}
.lower svg{background:#5D6A62}
figcaption{font:600 12px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{stone}};margin-top:12px}
.site{display:grid;grid-template-columns:1.9fr 1fr;gap:24px;align-items:start}
.site figure{min-width:0}
@media(max-width:860px){.site{grid-template-columns:1fr}}
.site img{width:100%;display:block;box-shadow:0 22px 60px -30px rgba(11,43,33,.6)}
table{width:100%;border-collapse:collapse;font-size:15px}
td,th{padding:11px 8px;border-bottom:1px solid #E1DBCC;text-align:left;vertical-align:top}
th{font:600 12px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{stone}}}
.note{font-size:14px;color:{{stone}}}
.mini-row{display:flex;align-items:flex-end;gap:5px;border-bottom:3px solid {{spruce}};width:100%}
.mini-row i{display:block;background:{{spruce}}}
</style></head><body>

<section class="dark cover"><div class="w">
  <p class="label"><span class="win"></span>Generation Maine · Brand identity</p>
  <h1 style="margin-top:22px">Big house, little house, back house, barn</h1>
  <p style="font-size:20px;margin-top:24px">An identity drawn from the most Maine building there is: the connected farm. It is a picture of people changing how they live and work to stay on their own land. That is what this project is about.</p>
  <svg class="f" viewBox="0 0 200 88" preserveAspectRatio="xMidYMax meet">{{FARM_REV_BODY}}</svg>
</div></section>

<section><div class="w">
  <p class="label"><span class="win"></span>01 The research</p>
  <h2>Maine has built its way through hard times before</h2>
  <p>Drive any back road in Maine and you will see them: a house, a smaller ell, a long shed and a barn, all joined in one line. Most people think they were joined so farmers could reach the barn in the snow.</p>
  <p class="quote">They were joined to make a living.</p>
  <p>In the 1840s and 1850s, bigger farms in the Midwest undercut New England farmers. Families answered by connecting their buildings and adding home work, like cheese and candle making, under one roof. Historian Thomas Hubka made the case in his book, whose title is the old children's rhyme: "Big House, Little House, Back House, Barn."</p>
  <p class="src">Source: Thomas C. Hubka, Big House, Little House, Back House, Barn: The Connected Farm Buildings of New England (University Press of New England, 1984).</p>
  <div class="cols">
    <div><h3>It is the brief</h3>Young people shaping their lives around economic rules. The farms are the same story, 180 years earlier, told in wood.</div>
    <div><h3>It is only here</h3>Connected farms are a northern New England form, strongest in Maine. No flag, no lobster, no lighthouse, no state outline.</div>
    <div><h3>It bridges the audience</h3>Rural and older readers know these buildings by heart. Young viewers get a line of buildings that keeps adding on, like a group of creators.</div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="win"></span>02 The mark</p>
  <h2>The farm line</h2>
  <p>A true elevation, not a house icon. Gable-front house with its center chimney, the ell and back house stepping down, then the gable-front barn with its big door. One window is lit: someone is home. For small sizes, the icon keeps the first addition, the house and its ell.</p>
  <div class="g2" style="margin-top:26px">
    <div class="panel">{{LOCK}}</div>
    <div class="panel sp">{{LOCK_REV}}</div>
  </div>
  <div class="g2" style="margin-top:18px">
    <div class="panel">{{LOCK_H}}</div>
    <div class="panel sp">{{LOCK_H_REV}}</div>
  </div>
  <div class="g3" style="margin-top:18px">
    <div class="panel"><p class="label" style="margin-bottom:18px">Icon at 128, 64, 32, 24, 16 px</p><div class="smalls">{{SIZES}}</div></div>
    <div class="panel" style="padding:0">{{ICON_L}}</div>
    <div class="panel" style="padding:0">{{ICON_M}}</div>
  </div>
  <p class="note" style="margin-top:18px">The tittle on the i in "Maine" is a lit window, the same proportion as the one in the farm. Clear space equals the height of the barn door. Minimum width of the farm line is 64 px. Never add trees, fences, a sun or snow to it.</p>
</div></section>

<section><div class="w">
  <p class="label"><span class="win"></span>03 The element system</p>
  <h2>Everything is part of the farm</h2>
  <p>No shape here is decoration. Each one is a real part of a connected farm, and each one does a job on the page.</p>
  <div class="el"><div class="demo panel sage"><div class="mini-row" style="height:120px"><i style="width:30%;height:100%;clip-path:polygon(0 100%,0 34%,50% 5%,100% 34%,100% 100%)"></i><i style="width:22%;height:72%;clip-path:polygon(0 100%,0 6%,100% 16%,100% 100%)"></i><i style="width:20%;height:60%;clip-path:polygon(0 100%,0 8%,100% 16%,100% 100%)"></i><i style="width:28%;height:92%;clip-path:polygon(0 100%,0 32%,50% 0,100% 32%,100% 100%)"></i></div></div>
    <div><h3>Four building modules</h3>Big house, little house, back house and barn become the containers for creators, posts and pages. Four creators side by side make one farm. Twelve make three. The row always shares one ground line.</div></div>
  <div class="el"><div class="demo panel sp"><div style="display:flex;gap:10px"><span style="width:44px;height:55px;background:{{marigold}}"></span><span style="width:44px;height:55px;box-shadow:inset 0 0 0 2px #4E7A6A"></span><span style="width:44px;height:55px;box-shadow:inset 0 0 0 2px #4E7A6A"></span></div></div>
    <div><h3>Lit windows</h3>The accent shape. A window lights up in Marigold when something is live: a creator's first video, a new episode, the tittle in the wordmark. Unlit windows mean coming soon. The site gets a working reason to come back.</div></div>
  <div class="el"><div class="demo" style="padding:0">{{CLAP}}</div>
    <div><h3>Clapboard</h3>The texture. Evenly spaced boards with a thin shadow under each lap, tone on tone on Spruce. It replaces the swirls and halftone with something every Mainer has touched.</div></div>
  <div class="el"><div class="demo panel">{{ELEV}}</div>
    <div><h3>Elevation drawings</h3>Thin architect's lines with labels, for explaining. The story of the brand, the parts of a series, how a creator's life fits together. It reads as a plan, which suits a project about building.</div></div>
  <div class="el"><div class="demo panel sp" style="padding:0;align-items:end">{{FARM_REV_WIDE}}</div>
    <div><h3>The horizon</h3>The farm line sits on the edge between two sections, so the next section becomes the ground. It opens the website, closes the end card and signs the footer.</div></div>
  <div class="el"><div class="demo" style="background:#5D6A62">{{LOWER_MINI}}</div>
    <div><h3>The chyron</h3>Each creator appears with a two-bar lower third led by the icon: name on Birch, TOWN, MAINE on Spruce.</div></div>
</div></section>

<section><div class="w">
  <p class="label"><span class="win"></span>04 Social</p>
  <h2>Built for the feed</h2>
  <div class="apps" style="margin-top:22px">
    <figure>{{AVATAR}}<figcaption>Avatar</figcaption></figure>
    <figure>{{END}}<figcaption>9:16 end card</figcaption></figure>
    <figure>{{POST}}<figcaption>4:5 creator announcement</figcaption></figure>
  </div>
  <div class="g2" style="margin-top:26px">
    <figure class="lower">{{LOWER}}<figcaption>Chyron over video</figcaption></figure>
    <figure>{{OG}}<figcaption>Share card</figcaption></figure>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="win"></span>05 Website</p>
  <h2>A page that stands up without photos</h2>
  <p>The hero ends on the farm line. The about section tells the farm story in one drawing. The creators stand in a connected row, windows dark until their first video is out. Open brand/v7/site/index.html to scroll it.</p>
  <div class="site" style="margin-top:24px"><figure><img src="{{DESK}}" alt="Website, desktop"><figcaption>Desktop, 1440 px</figcaption></figure>
    <figure><img src="{{MOB}}" alt="Website, mobile, shown in columns"><figcaption>Mobile, 390 px, read in columns</figcaption></figure></div>
  <p class="note" style="margin-top:18px">Automated axe check on desktop and mobile: {{AXE}} violations. Colors and contrast carry over from the previous round unchanged.</p>
</div></section>

<section class="dark"><div class="w">
  <p class="label"><span class="win"></span>06 Honest risks</p>
  <h2>What to test before we commit</h2>
  <div class="cols" style="margin-top:10px">
    <div><h3>Too rural?</h3>A creator from Portland may not see a farm as theirs. The fix is the story, told once, and the modules used for every kind of life. Worth one question in a creator call.</div>
    <div><h3>Barns are common</h3>Farm groups use barn icons. The four-part connected line is the ownable part, never the barn alone. Run a trademark search on the farm line.</div>
    <div><h3>Client check</h3>Confirm Maine Policy Institute is comfortable telling the Hubka story. It frames adapting to competition, which fits their work, but it is their call.</div>
  </div>
</div></section>
</body></html>
"""


def finish_present(m):
    p = os.path.join(ROOT, OUT, "big-house.html")
    html = open(p).read()
    body = farm(0, 0, 200, C["birch"], C["marigold"], C["spruce"])
    wide = svg(300, 150, rect(0, 138, 300, 12, C["birch"]) + farm(90, 138 - H * 1.0, 200, C["birch"], C["marigold"], C["spruce"]), "")
    lt = rect(0, 0, 560, 100, C["birch"]) + rect(0, 0, 100, 152, C["spruce"]) + icon(0, 0, 100, None, C["birch"], C["marigold"])
    lt += text(124, 64, "[Creator name]", 40, C["ink"], "Bric", 800) + rect(100, 100, 460, 52, C["spruce"])
    lt += text(124, 135, "[HOMETOWN], MAINE", 24, C["birch"], weight=600, ls=0.08)
    html = html.replace("{{FARM_REV_BODY}}", body).replace("{{FARM_REV_WIDE}}", wide).replace("{{LOWER_MINI}}", svg(560, 152, lt, ""))
    open(p, "w").write(html)


if __name__ == "__main__":
    marks = build_marks()
    social = build_social()
    if len(sys.argv) > 1 and sys.argv[1] == "present":
        build_present(marks, social)
        finish_present(marks)
        print("presentation written")
    else:
        build_site(marks)
        print("marks, social and site written")
