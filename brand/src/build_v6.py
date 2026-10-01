"""Identity v6: "The Doorway".

A person standing in a lit doorway. The dot is the record light and the person. The arch is home,
the place you are building. Built on v5 "On the Record" with a warmer, softer palette, a lighter
heading weight and an element kit drawn from the circle and the arch.

  python3 brand/src/build_v6.py            # marks, textures, social, website
  node brand/src/render_v6.mjs             # PNGs, website screenshots, axe check
  python3 brand/src/build_v6.py present    # presentation with screenshots and results embedded
"""
import base64
import json
import math
import os
import sys

from gmlib import ROOT, write
from build_v4 import wordmark_one_line, wordmark_stacked, placed, rect, text, svg, f, HANDLES

OUT = "brand/v6"

C = {
    "spruce": "#104836",
    "pine": "#0B2B21",
    "birch": "#F4F0E6",
    "snow": "#F9F8F6",   # near-white, for the reversed mark and type on Spruce and Pine. Neutral with a hair of warmth, so it never leans green on the greens. Not cream.
    "ink": "#1E2621",
    "marigold": "#EFB443",
    "sage": "#DDE5DA",
    "moss": "#3D6F58",
    "stone": "#5E6A63",
}
V5 = {"spruce": "#0B4A34", "paper": "#F2F4F7", "ink": "#121417", "amber": "#FFB81C"}


# ------------------------------------------------------------------ color math
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    a, b = lum(a), lum(b)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def sat(h):
    import colorsys
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return colorsys.rgb_to_hls(r, g, b)[2]


# ------------------------------------------------------------------ the mark
# Grid of 200 units. The arch is 78 wide, so its radius is 39. The dot (r 21) sits at the
# center of the arch's curve, which leaves an even 18-unit ring of light around it.
ARCH_W, ARCH_TOP, DOT_R6 = 78, 34, 21
BLOCK_RX = 16


def doorway(x, y, s, block, mark, rx=None, opening=None):
    """The mark: a block with a lit arched opening cut to its bottom edge, and the dot inside.

    The opening is a true cutout, so it shows whatever is behind the mark. Pass opening= to fill it.
    """
    k = s / 200.0
    r = ARCH_W / 2
    ax = 100 - r
    rx = BLOCK_RX if rx is None else rx
    outer = "M%s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s Z" % (
        rx, 0, 200 - rx, rx, rx, 200, rx, 200 - rx, rx, rx, 200 - rx, 200, rx, rx, rx, 0, 200 - rx, rx, rx, rx, rx, 0) if rx else "M0 0H200V200H0Z"
    hole = "M%s 200 V%s A%s %s 0 0 1 %s %s V200 Z" % (ax, ARCH_TOP + r, r, r, ax + ARCH_W, ARCH_TOP + r)
    body = '<path fill="%s" fill-rule="evenodd" d="%s %s"/>' % (block, outer, hole)
    if opening:
        body = '<path fill="%s" d="%s"/>' % (opening, hole) + body
    body += '<circle cx="100" cy="%s" r="%s" fill="%s"/>' % (ARCH_TOP + r, DOT_R6, mark)
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (f(x), f(y), f(k), body)


def arch_path(x, y, w, h):
    r = w / 2
    return "M%s %s V%s A%s %s 0 0 1 %s %s V%s Z" % (f(x), f(y + h), f(y + r), f(r), f(r), f(x + w), f(y + r), f(y + h))


def lockup_h(fg, block, mark, opening=None):
    wm, w, h = wordmark_one_line(fg, mark, "circle")
    s = 100
    gap = 30
    body = doorway(0, 0, s, block, mark, opening=opening) + placed(wm, s + gap, (s - h) / 2 + 4, 1)
    return body, s + gap + w, s


def lockup_v(fg, block, mark, opening=None):
    wm, w, h = wordmark_stacked(fg, mark, "circle")
    s = 118
    body = doorway(0, 0, s, block, mark, opening=opening) + placed(wm, 0, s + 34, 1)
    return body, max(w, s), s + 34 + h


def build_marks():
    m = {}
    m["mark"] = svg(200, 200, doorway(0, 0, 200, C["spruce"], C["marigold"]), "Generation Maine")
    m["mark-reversed"] = svg(200, 200, doorway(0, 0, 200, C["birch"], C["marigold"]), "Generation Maine")
    m["mark-marigold"] = svg(200, 200, doorway(0, 0, 200, C["marigold"], C["ink"]), "Generation Maine")
    m["mark-black"] = svg(200, 200, doorway(0, 0, 200, "#000", "#000"), "Generation Maine")
    m["mark-white"] = svg(200, 200, doorway(0, 0, 200, "#fff", "#fff"), "Generation Maine")
    m["app-icon"] = svg(200, 200, rect(0, 0, 200, 200, C["spruce"]) + doorway(30, 30, 140, C["birch"], C["marigold"], rx=10), "Generation Maine")
    b, w, h = lockup_h(C["spruce"], C["spruce"], C["marigold"])
    m["lockup"] = svg(w, h, b, "Generation Maine")
    b, w, h = lockup_h(C["birch"], C["birch"], C["marigold"])
    m["lockup-reversed"] = svg(w, h, b, "Generation Maine")
    b, w, h = lockup_v(C["spruce"], C["spruce"], C["marigold"])
    m["lockup-stacked"] = svg(w, h, b, "Generation Maine")
    b, w, h = lockup_v(C["birch"], C["birch"], C["marigold"])
    m["lockup-stacked-reversed"] = svg(w, h, b, "Generation Maine")
    for suf, fg in (("", C["spruce"]), ("-reversed", C["birch"])):
        b, w, h = wordmark_one_line(fg, C["marigold"], "circle")
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
    for k, v in m.items():
        write("%s/logo/%s.svg" % (OUT, k), v)
    return m


def construction():
    """Construction drawing: the dot, the ring of light and the arch share one center."""
    r = ARCH_W / 2
    cy = ARCH_TOP + r
    g = rect(0, 0, 200, 200, "none")
    body = doorway(0, 0, 200, C["spruce"], C["marigold"])
    guide = "#EFB443"
    lines = ('<g fill="none" stroke="%s" stroke-width="0.8" stroke-dasharray="3 3">'
             '<circle cx="100" cy="%s" r="%s"/><line x1="0" y1="%s" x2="200" y2="%s"/><line x1="100" y1="0" x2="100" y2="200"/>'
             '<line x1="%s" y1="0" x2="%s" y2="200"/><line x1="%s" y1="0" x2="%s" y2="200"/></g>'
             % (guide, cy, r, cy, cy, 100 - r, 100 - r, 100 + r, 100 + r))
    return svg(200, 200, body + lines, "Construction")


# ------------------------------------------------------------------ textures
def halftone(w, h, step, rmax, color, mode="rise", origin=(0.5, 1.0), rmin=0.0, op=1.0, reach=1.0):
    """Halftone made of record dots. Dot size falls off from an edge (rise) or a point (spill),
    like light coming through the doorway."""
    out = []
    ox, oy = origin[0] * w, origin[1] * h
    dmax = math.hypot(max(ox, w - ox), max(oy, h - oy)) * reach
    for j in range(int(h / step) + 1):
        for i in range(int(w / step) + 1):
            x = i * step + (step / 2 if j % 2 else 0)
            y = j * step
            if mode == "rise":
                t = 1 - (h - y) / (h * reach)
            else:
                t = 1 - math.hypot(x - ox, y - oy) / dmax
            t = max(0.0, min(1.0, t))
            r = rmin + (rmax - rmin) * t ** 1.3
            if r > 0.35:
                out.append('<circle cx="%.1f" cy="%.1f" r="%.2f"/>' % (x, y, r))
    return '<g fill="%s" opacity="%s">%s</g>' % (color, op, "".join(out))


def build_textures():
    t = {}
    t["spill-pine"] = svg(900, 900, halftone(900, 900, 18, 8.2, C["spruce"], "spill", (0.5, 1.0), reach=1.0), "Texture")
    t["spill-marigold"] = svg(600, 900, halftone(600, 900, 15, 5.2, C["marigold"], "spill", (0.5, 1.08), reach=0.62, op=0.85), "Texture")
    t["rise-spruce"] = svg(1200, 360, halftone(1200, 360, 14, 5.2, "#123D30", "rise", reach=0.8), "Texture")
    t["rise-sage"] = svg(1200, 360, halftone(1200, 360, 16, 6.6, "#CBD6C8", "rise", reach=1.0), "Texture")
    t["card"] = svg(400, 400, halftone(400, 400, 14, 6, "#1B5A44", "spill", (0.5, 0.0), reach=1.1), "Texture")
    for k, v in t.items():
        write("%s/site/img/%s.svg" % (OUT, k), v)
    return t


# ------------------------------------------------------------------ social
def caption(x, y, s, size, fill=None, color=None, pad=None):
    """A caption block, like the auto-captions on a short video. Width is estimated from the text."""
    pad = pad or size * 0.42
    w = len(s) * size * 0.5 + pad * 2
    h = size * 1.5
    return rect(x, y, w, h, fill or C["ink"], size * 0.22) + text(x + w / 2, y + h * 0.7, s, size, color or C["birch"], "Bric", 700, anchor="middle"), w


def chyron(x, y, name, town, w=1100):
    b = rect(x, y, w, 100, C["birch"])
    b += doorway(x, y, 100, C["spruce"], C["marigold"], rx=0, opening=None)
    b += text(x + 128, y + 66, name, 52, C["ink"], "Bric", 800, ls=-0.01)
    b += rect(x, y + 100, w, 52, C["spruce"])
    b += text(x + 128, y + 135, town, 25, C["birch"], weight=600, ls=0.08)
    b += text(x + w - 26, y + 135, "GENERATION MAINE", 25, C["marigold"], weight=700, anchor="end", ls=0.08)
    return b


def build_social():
    s = {}
    a = rect(0, 0, 1080, 1080, C["spruce"]) + doorway(250, 250, 580, C["birch"], C["marigold"], rx=40)
    s["avatar"] = svg(1080, 1080, a, "Avatar")

    e = rect(0, 0, 1080, 1920, C["spruce"])
    e += '<g transform="translate(0 1180)">%s</g>' % halftone(1080, 740, 22, 9, C["pine"], "rise")
    e += doorway(80, 150, 150, C["birch"], C["marigold"], rx=12)
    wm, w, h = wordmark_stacked(C["birch"], C["marigold"], "circle")
    e += placed(wm, 80, 400, 920 / w)
    e += rect(80, 880, 920, 5, C["birch"]) + rect(80, 894, 920, 1.5, C["birch"])
    e += text(80, 1010, "Follow along", 92, C["marigold"], "Bric", 800, ls=-0.02)
    y = 1140
    for lab, hd in HANDLES:
        e += '<circle cx="96" cy="%s" r="10" fill="%s"/>' % (y - 13, C["marigold"])
        e += text(126, y, lab, 40, C["birch"], weight=700)
        e += text(430, y, hd, 40, C["birch"], weight=400)
        e += rect(80, y + 30, 920, 1, "#2E6450")
        y += 92
    e += text(80, 1740, "An initiative of Maine Policy Institute", 34, C["birch"], weight=600)
    s["endcard"] = svg(1080, 1920, e, "End card")

    s["lowerthird"] = svg(1920, 1080, chyron(96, 790, "[Creator name]", "[HOMETOWN], MAINE"), "Chyron lower third")

    o = rect(0, 0, 1200, 630, C["spruce"])
    o += '<clipPath id="oa"><path d="%s"/></clipPath>' % arch_path(820, 90, 300, 540)
    o += '<path d="%s" fill="%s"/>' % (arch_path(820, 90, 300, 540), C["pine"])
    o += '<g clip-path="url(#oa)"><g transform="translate(820 90)">%s</g></g>' % halftone(300, 540, 14, 5.2, C["marigold"], "spill", (0.5, 1.08), reach=0.62, op=0.85)
    o += '<circle cx="970" cy="240" r="62" fill="%s"/>' % C["marigold"]
    b, w, h = lockup_h(C["birch"], C["birch"], C["marigold"])
    o += placed(b, 80, 110, 560 / w)
    o += text(82, 360, "Young Mainers on building", 50, C["birch"], "Bric", 800, ls=-0.02)
    o += text(82, 420, "a life here", 50, C["birch"], "Bric", 800, ls=-0.02)
    o += text(82, 540, "An initiative of Maine Policy Institute", 24, C["birch"], weight=600)
    s["og"] = svg(1200, 630, o, "Share card")

    # 4:5 feed post: a question the series asks, set as captions inside the doorway.
    p = rect(0, 0, 1080, 1350, C["birch"])
    p += '<path d="%s" fill="%s"/>' % (arch_path(140, 150, 800, 1200), C["spruce"])
    p += '<clipPath id="pa"><path d="%s"/></clipPath>' % arch_path(140, 150, 800, 1200)
    p += '<g clip-path="url(#pa)"><g transform="translate(140 150)">%s</g></g>' % halftone(800, 1200, 20, 8.5, C["pine"], "spill", (0.5, 1.0), reach=0.9)
    p += '<circle cx="540" cy="550" r="92" fill="%s"/>' % C["marigold"]
    c1, w1 = caption(0, 0, "Can I afford", 64)
    c2, w2 = caption(0, 0, "to stay here?", 64)
    p += '<g transform="translate(%s 820)">%s</g>' % (f(540 - w1 / 2), c1)
    p += '<g transform="translate(%s 920)">%s</g>' % (f(540 - w2 / 2), c2)
    p += text(540, 1130, "EP 01 · [HOMETOWN], MAINE", 28, C["birch"], weight=600, anchor="middle", ls=0.08)
    p += doorway(80, 60, 60, C["spruce"], C["marigold"], rx=6)
    p += text(1000, 100, "GENERATION MAINE", 24, C["spruce"], weight=700, anchor="end", ls=0.08)
    s["post"] = svg(1080, 1350, p, "Feed post")
    for k, v in s.items():
        write("%s/social/%s.svg" % (OUT, k), v)
    return s


# ------------------------------------------------------------------ website
def font64(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def inline(svg_text, cls):
    return svg_text.replace("<svg ", '<svg class="%s" aria-hidden="true" focusable="false" ' % cls, 1)


def fonts_css():
    return ("@font-face{font-family:Bric;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:800;font-display:swap}\n"
            "@font-face{font-family:Bric;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:700;font-display:swap}\n"
            "@font-face{font-family:Inter;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:400 700;font-display:swap}\n"
            % (font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
               font64(OUT + "/fonts-web/bricolage-grotesque-700.woff2"),
               font64("generation-maine/assets/fonts/inter-var.woff2")))


def fill(html, extra):
    for k, v in extra.items():
        html = html.replace(k, v)
    for k, v in C.items():
        html = html.replace("{{%s}}" % k, v)
    return html


def build_site(m):
    html = fill(SITE, {
        "{{FONTS}}": fonts_css(),
        "{{MARK_REV}}": inline(m["mark-reversed"], "mk"),
        "{{WM_REV}}": inline(m["wordmark-reversed"], "wm"),
        "{{LOCK_FOOT}}": inline(m["lockup-stacked-reversed"], "lock-foot"),
    })
    write(OUT + "/site/index.html", html)


SITE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine | Young Mainers on building a life here</title>
<meta name="description" content="Short videos by young Maine creators about the rules that shape their lives. An initiative of Maine Policy Institute.">
<style>
{{FONTS}}
:root{--sp:{{spruce}};--pine:{{pine}};--bi:{{birch}};--ink:{{ink}};--mg:{{marigold}};--sage:{{sage}};--moss:{{moss}};--stone:{{stone}};--g:clamp(20px,5vw,72px);--ease:cubic-bezier(.2,.7,.2,1)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font:18px/1.65 Inter,system-ui,sans-serif;color:var(--ink);background:var(--bi);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit}
:focus-visible{outline:3px solid var(--mg);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--mg);color:var(--ink);padding:10px 16px;border-radius:8px;z-index:50;font-weight:700}
.skip:focus{left:12px}
.w{max-width:1280px;margin:0 auto;padding:0 var(--g)}
h1,h2,h3{font-family:Bric;margin:0;font-weight:700;letter-spacing:-.02em}
.dot{display:inline-block;width:.5em;height:.5em;border-radius:50%;background:var(--mg);flex:none}
.pulse{animation:pulse 2.4s var(--ease) infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){.pulse{animation:none}}
.label{display:flex;align-items:center;gap:10px;margin:0;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--moss)}
.label .n{font-variant-numeric:tabular-nums;color:var(--stone)}
.on-dark .label{color:var(--sage)}
.on-dark .label .n{color:#A9BCB2}
.rules{border-top:5px solid currentColor;padding-top:5px}
.rules::before{content:"";display:block;border-top:1px solid currentColor}

/* header */
header{position:sticky;top:0;z-index:20;background:var(--sp);color:var(--bi);border-bottom:1px solid #1D5843}
header .w{display:flex;align-items:center;justify-content:space-between;height:76px;gap:20px}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none}
.brand .mk{width:36px;height:36px}
.brand .wm{height:21px;width:auto}
nav ul{display:flex;align-items:center;gap:30px;list-style:none;margin:0;padding:0;font-weight:600;font-size:16px}
nav a{text-decoration:none;padding:6px 0;background:linear-gradient(var(--mg),var(--mg)) 0 100%/0 2px no-repeat;transition:background-size .3s var(--ease)}
nav a:hover{background-size:100% 2px}
.pill{display:inline-flex;align-items:center;gap:9px;border-radius:99px;padding:9px 15px;font:600 13px/1 Inter;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.pill.dk{background:var(--pine);color:var(--bi)}
@media (max-width:720px){.hide-s{display:none}nav ul{gap:20px}.brand .wm{display:none}}

/* hero */
.hero{background:var(--sp);color:var(--bi);overflow:hidden}
.hero .w{display:grid;grid-template-columns:1.25fr .75fr;gap:clamp(32px,6vw,96px);align-items:end;padding-top:clamp(56px,8vw,112px)}
.hero .label{color:var(--mg)}
h1{font-weight:800;font-size:clamp(50px,8.2vw,124px);line-height:.94;letter-spacing:-.03em;margin:26px 0 30px;max-width:10.5ch}
h1 .dot{width:.19em;height:.19em;margin-left:.04em}
.hero p.lede{font-size:clamp(19px,1.6vw,22px);line-height:1.55;max-width:34ch;margin:0 0 36px;color:#E6E4DA}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;gap:10px;border-radius:99px;padding:16px 26px;font-weight:700;font-size:17px;line-height:1.2;text-decoration:none;transition:transform .2s var(--ease),background-color .2s}
.btn:hover{transform:translateY(-2px)}
.btn.mg{background:var(--mg);color:var(--ink)}
.btn.ol{box-shadow:inset 0 0 0 1.5px #9DB5A9;color:var(--bi)}
.btn.ol:hover{box-shadow:inset 0 0 0 1.5px var(--bi)}
.btn.sp{background:var(--sp);color:var(--bi)}
.btn.ink{background:var(--ink);color:var(--bi)}
.door{position:relative;aspect-ratio:3/4.3;border-radius:999px 999px 0 0;background:var(--pine) url(img/spill-marigold.svg) center bottom/100% auto no-repeat;overflow:hidden;align-self:end}
.door .light{position:absolute;left:50%;top:24%;width:30%;aspect-ratio:1;border-radius:50%;background:var(--mg);transform:translate(-50%,-50%)}
.door .pill{position:absolute;left:50%;bottom:5%;transform:translateX(-50%);background:var(--pine);box-shadow:inset 0 0 0 1px #2D5B4B;color:var(--bi)}
.caps{position:absolute;left:0;right:0;bottom:17%;display:flex;flex-direction:column;align-items:center;gap:8px}
.cap{background:var(--ink);color:var(--bi);font:700 clamp(18px,1.9vw,26px)/1.2 Bric;letter-spacing:-.01em;padding:.34em .55em;border-radius:6px}
.hero .base{grid-column:1/-1;display:flex;justify-content:space-between;gap:8px 16px;flex-wrap:wrap;padding:22px 0;border-top:1px solid #2B6150;margin-top:0;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:#C9D6CF}
@media (max-width:900px){.hero .w{grid-template-columns:1fr}.door{max-width:340px;width:100%;margin:0 auto;aspect-ratio:3/3.8}.door .light{top:34%;width:24%}}

/* sections */
section{padding:clamp(72px,10vw,136px) 0}
h2{font-size:clamp(38px,5.2vw,72px);line-height:1;margin:20px 0 0;max-width:15ch}
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(40px,7vw,112px);align-items:start}
@media (max-width:900px){.split{grid-template-columns:1fr}}
.body p{margin:0 0 18px;max-width:58ch}
.body p.big{font-size:clamp(20px,1.8vw,24px);line-height:1.5}

.questions{background:var(--sp) url(img/spill-pine.svg) center bottom/cover no-repeat;border-radius:28px;padding:clamp(28px,4vw,48px);color:var(--bi);display:flex;flex-direction:column;gap:12px;align-items:flex-start}
.questions{align-items:center;text-align:center}
.questions .cap{font-size:clamp(19px,2vw,27px);white-space:nowrap}
.questions .label{color:var(--sage);margin-bottom:10px}

/* creators */
.creators{background:var(--sage)}
.head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(36px,5vw,64px)}
.head p{max-width:40ch;margin:0;color:#34413A}
.creators .label .n{color:#44514A}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.8vw,24px);list-style:none;margin:0;padding:0}
@media (max-width:1000px){.grid{grid-template-columns:repeat(2,1fr)}}
.card{display:flex;flex-direction:column}
.arch{position:relative;aspect-ratio:3/4;border-radius:999px 999px 0 0;background:var(--sp) url(img/card.svg) center top/cover no-repeat;overflow:hidden;display:flex;align-items:flex-end}
.arch .num{position:absolute;left:0;right:0;top:40%;text-align:center;font:800 clamp(56px,6vw,96px)/1 Bric;letter-spacing:-.04em;color:#2F6A55}
.arch .light{position:absolute;left:50%;top:17%;width:18%;aspect-ratio:1;border-radius:50%;background:var(--mg);transform:translateX(-50%)}
.chy{background:var(--bi);border-left:6px solid var(--mg);width:100%}
.chy b{display:block;font:700 clamp(17px,1.5vw,21px)/1.15 Bric;padding:12px 14px 9px}
.chy span{display:block;background:var(--sp);color:var(--bi);font:600 12px/1 Inter;letter-spacing:.08em;text-transform:uppercase;padding:9px 14px}
@media (max-width:560px){.chy b{padding:10px 10px 8px}.chy span{letter-spacing:.03em;padding:8px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chy{border-left-width:5px}}
.soon{margin-top:26px;font-size:15px;color:#34413A}

/* season */
.season{background:var(--pine);color:var(--bi)}
.track{position:relative;margin-top:clamp(40px,5vw,64px);padding-bottom:8px}
.track ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(12,1fr);position:relative}
.track ol::before{content:"";position:absolute;left:10px;right:10px;top:10px;height:2px;background:#2D5B4B}
.track ol::after{content:"";position:absolute;left:10px;width:calc((100% - 20px)/12*.5);top:10px;height:2px;background:var(--mg)}
.track li{position:relative;display:flex;flex-direction:column;gap:14px;font:600 12px/1 Inter;letter-spacing:.06em;color:#A9BCB2}
.track li i{width:22px;height:22px;border-radius:50%;border:2px solid #4E7A6A;background:var(--pine);position:relative;z-index:1}
.track li:first-child i{background:var(--mg);border-color:var(--mg)}
.track li:first-child{color:var(--bi)}
@media (max-width:700px){.track ol{grid-template-columns:repeat(6,1fr);row-gap:28px}.track ol::before,.track ol::after{display:none}}
.season .split p{color:#D5DED9;max-width:46ch;margin:0}

/* follow */
.follow .split{align-items:stretch}
.chan{list-style:none;padding:0;margin:36px 0 0;border-top:5px solid var(--ink)}
.chan a{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 4px;border-bottom:1px solid #CFCBC0;text-decoration:none;font:700 clamp(26px,3vw,40px)/1 Bric;letter-spacing:-.015em;transition:padding .25s var(--ease),color .2s}
.chan a:hover{padding-left:14px;color:var(--sp)}
.chan a small{font:500 16px/1 Inter;letter-spacing:0;color:var(--stone)}
.sub{position:relative;border-radius:999px 999px 28px 28px;background:var(--mg);padding:clamp(150px,14vw,190px) clamp(28px,4vw,56px) clamp(32px,4vw,48px);display:flex;flex-direction:column;justify-content:flex-end;min-height:clamp(380px,40vw,520px);overflow:hidden}
.sub::before{content:"";position:absolute;left:50%;top:clamp(56px,7vw,84px);width:clamp(56px,6vw,76px);aspect-ratio:1;border-radius:50%;background:var(--ink);transform:translateX(-50%)}
.sub h3{font-size:clamp(32px,3.4vw,48px);line-height:1;letter-spacing:-.02em;font-weight:800}
.sub p{margin:14px 0 26px;max-width:40ch}
.sub .btn{align-self:flex-start}

/* mpi */
.mpi{padding-top:0}
.mpi .rules{color:var(--sp);margin-bottom:28px}
.mpi h2{font-size:clamp(32px,3.8vw,52px)}
.conf{background:#E7E1D2;padding:2px 7px;border-radius:4px;font-size:.9em}

/* footer */
footer{background:var(--pine);color:var(--bi);padding:clamp(56px,7vw,88px) 0 36px;position:relative;overflow:hidden}
footer::after{content:"";position:absolute;inset:auto 0 0 0;height:200px;background:url(img/rise-spruce.svg) center bottom/cover no-repeat;pointer-events:none}
footer .w{position:relative;z-index:1}
footer .top{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;flex-wrap:wrap}
.lock-foot{width:min(340px,72vw);height:auto;display:block}
footer ul{list-style:none;margin:0;padding:0;display:flex;gap:10px 28px;flex-wrap:wrap;font-weight:600}
footer ul a{text-decoration:none;border-bottom:2px solid #3C6D5C;padding-bottom:3px}
footer ul a:hover{border-color:var(--mg)}
footer .rules{color:#3C6D5C;margin-top:48px}
footer .fine{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:18px;font-size:14px;color:#B7C6BE}
</style></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="w">
  <a class="brand" href="#" aria-label="Generation Maine, home">{{MARK_REV}}{{WM_REV}}</a>
  <nav aria-label="Main"><ul><li class="hide-s"><a href="#about">About</a></li><li><a href="#creators">Creators</a></li><li><a href="#follow">Follow</a></li>
    <li class="hide-s"><span class="pill dk"><span class="dot pulse" aria-hidden="true"></span>Coming soon</span></li></ul></nav>
</div></header>

<main id="main">
<section class="hero on-dark" aria-labelledby="h1" style="padding:0"><div class="w">
  <div>
    <p class="label"><span class="dot" aria-hidden="true"></span>An initiative of Maine Policy Institute</p>
    <h1 id="h1">Young Mainers on building a life here<span class="dot" aria-hidden="true"></span></h1>
    <p class="lede">Short videos by young Maine creators about the rules that shape their lives.</p>
    <div class="btns"><a class="btn mg" href="#creators">Meet the creators</a><a class="btn ol" href="#follow">Follow along</a></div>
  </div>
  <div class="door" aria-hidden="true"><span class="light pulse"></span><span class="pill">Episode 01</span>
    <div class="caps"><span class="cap">Can I afford</span><span class="cap">to stay here?</span></div></div>
  <div class="base"><span>Maine · Stories from across the state</span><span>Season one · Coming soon</span></div>
</div></section>

<section id="about" aria-labelledby="h-about"><div class="w split">
  <div class="body">
    <p class="label"><span class="n">01</span> What it is</p>
    <h2 id="h-about">A storytelling project made by young Mainers</h2>
    <p class="big" style="margin-top:32px">Generation Maine is a group of 8 to 12 young content creators from across the state. Each one makes short videos about their own life in Maine.</p>
    <p>The videos show how economic rules affect everyday choices. Some are about finding a place to live. Others are about getting a job, starting a business or deciding whether to stay.</p>
    <p>The creators tell their own stories. You can watch them on social media and read more on our Substack.</p>
  </div>
  <div class="questions on-dark">
    <p class="label">Questions the videos take on</p>
    <span class="cap">Can I afford my own place?</span>
    <span class="cap">Is there work in my field?</span>
    <span class="cap">Could I open a shop here?</span>
    <span class="cap">Why are my friends leaving?</span>
    <span class="cap">Should I stay?</span>
  </div>
</div></section>

<section id="creators" class="creators" aria-labelledby="h-cr"><div class="w">
  <div class="head"><div><p class="label"><span class="n">02</span> The creators</p><h2 id="h-cr">Meet the creators</h2></div>
    <p>Eight to twelve young Mainers from different towns. Each creator gets a page here once their first video is out.</p></div>
  <ul class="grid">
    <li class="card"><div class="arch"><span class="light" aria-hidden="true"></span><span class="num" aria-hidden="true">01</span></div><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="card"><div class="arch"><span class="light" aria-hidden="true"></span><span class="num" aria-hidden="true">02</span></div><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="card"><div class="arch"><span class="light" aria-hidden="true"></span><span class="num" aria-hidden="true">03</span></div><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
    <li class="card"><div class="arch"><span class="light" aria-hidden="true"></span><span class="num" aria-hidden="true">04</span></div><div class="chy"><b>[Creator name]</b><span>[Hometown], Maine</span></div></li>
  </ul>
  <p class="soon">Portraits drop into the arches when the photo shoot is done.</p>
</div></section>

<section class="season on-dark" aria-labelledby="h-s"><div class="w">
  <div class="split"><div><p class="label"><span class="n">03</span> Season one</p><h2 id="h-s">One story at a time</h2></div>
    <p>New videos come out through the season. Each dot is an episode. The first one is on its way.</p></div>
  <div class="track" aria-label="Season one episodes, none released yet"><ol>
    <li><i></i>EP 01</li><li><i></i>EP 02</li><li><i></i>EP 03</li><li><i></i>EP 04</li><li><i></i>EP 05</li><li><i></i>EP 06</li>
    <li><i></i>EP 07</li><li><i></i>EP 08</li><li><i></i>EP 09</li><li><i></i>EP 10</li><li><i></i>EP 11</li><li><i></i>EP 12</li></ol></div>
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
  <div class="rules"></div>
  <div class="split"><div><p class="label"><span class="n">05</span> Who is behind this</p><h2 id="h-m">About Maine Policy Institute</h2></div>
  <div class="body"><p class="big">Generation Maine is an initiative of Maine Policy Institute.</p>
    <p><span class="conf">[CONFIRM: one sentence about Maine Policy Institute]</span></p>
    <p>Press: <span class="conf">[CONFIRM: press email]</span></p>
    <a class="btn sp" href="https://mainepolicy.org/">Visit Maine Policy Institute</a></div></div>
</div></section>
</main>

<footer class="on-dark"><div class="w">
  <div class="top">{{LOCK_FOOT}}<ul><li><a href="#follow">Instagram</a></li><li><a href="#follow">TikTok</a></li><li><a href="#follow">YouTube</a></li><li><a href="#follow">Substack</a></li></ul></div>
  <div class="rules"></div>
  <div class="fine"><span>An initiative of Maine Policy Institute</span><span>© 2026 Generation Maine</span></div>
</div></footer>
</body></html>
"""


# ------------------------------------------------------------------ presentation
def b64(rel, mime="image/png"):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode())


def contrast_rows():
    pairs = [("birch", "spruce", "Text on Spruce"), ("marigold", "spruce", "Marigold on Spruce"), ("ink", "marigold", "Text on Marigold"),
             ("ink", "birch", "Body text"), ("moss", "birch", "Labels on Birch"), ("stone", "birch", "Small print on Birch"),
             ("ink", "sage", "Text on Sage"), ("birch", "pine", "Text on Pine"), ("sage", "pine", "Labels on Pine")]
    out = ""
    for a, b, lab in pairs:
        r = ratio(C[a], C[b])
        grade = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA large" if r >= 3 else "Fail"
        out += ('<tr><td><span class="chip" style="background:%s;color:%s">Aa</span></td><td>%s</td><td>%s on %s</td><td class="num">%.2f</td><td>%s</td></tr>'
                % (C[b], C[a], lab, a.title(), b.title(), r, grade))
    return out


def build_present(m, social):
    qa = {}
    qp = os.path.join(ROOT, OUT, "site", "qa.json")
    if os.path.exists(qp):
        with open(qp) as fh:
            qa = json.load(fh)
    viol = qa.get("violations", "not run")
    before = [("Accent saturation", "%d%%" % round(sat(V5["amber"]) * 100), "%d%%" % round(sat(C["marigold"]) * 100)),
              ("Body text contrast", "%.1f:1" % ratio(V5["ink"], V5["paper"]), "%.1f:1" % ratio(C["ink"], C["birch"])),
              ("Background", "Cool blue-white", "Warm birch"),
              ("Heading weight", "800 everywhere", "800 hero only, 700 elsewhere"),
              ("Smallest label", "9 px", "12 px"),
              ("Amber as a full-width field", "Yes", "No, only inside one arch")]
    brow = "".join("<tr><td>%s</td><td>%s</td><td><b>%s</b></td></tr>" % r for r in before)
    html = fill(PRESENT, {
        "{{FONTS}}": fonts_css(),
        "{{MARK}}": m["mark"], "{{MARK_REV}}": m["mark-reversed"], "{{MARK_MG}}": m["mark-marigold"],
        "{{APP}}": m["app-icon"], "{{LOCK}}": m["lockup"], "{{LOCK_REV}}": m["lockup-reversed"],
        "{{LOCK_ST}}": m["lockup-stacked"], "{{CONSTRUCT}}": construction(),
        "{{AVATAR}}": social["avatar"], "{{END}}": social["endcard"], "{{LOWER}}": social["lowerthird"],
        "{{OG}}": social["og"], "{{POST}}": social["post"],
        "{{DESK}}": b64(OUT + "/site/desktop.png"), "{{MOB}}": b64(OUT + "/site/mobile-sheet.png"),
        "{{EXPLORE}}": b64(OUT + "/explorations.png"),
        "{{CONTRAST}}": contrast_rows(), "{{BEFORE}}": brow, "{{AXE}}": str(viol),
        "{{SMALLS}}": "".join('<span style="width:%dpx">%s</span>' % (p, m["mark"]) for p in (128, 64, 32, 24, 16)),
    })
    write(OUT + "/doorway.html", html)


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
h1{font-weight:800;font-size:clamp(48px,8vw,108px);line-height:.94;letter-spacing:-.03em}
h2{font-weight:700;font-size:clamp(34px,4.4vw,56px);line-height:1.02;margin:14px 0 18px;max-width:18ch}
h3{font-weight:700;font-size:22px;margin-bottom:6px}
p{max-width:64ch}
.label{display:flex;align-items:center;gap:10px;font:600 13px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{moss}};margin:0}
.dot{display:inline-block;width:.55em;height:.55em;border-radius:50%;background:{{marigold}}}
.dark{background:{{spruce}};color:{{birch}}}
.dark .label{color:{{marigold}}}
.dark p{color:#E2E2D8}
.cover .w{display:grid;grid-template-columns:1fr 280px;gap:48px;align-items:end}
.cover svg{width:100%;height:auto}
@media(max-width:800px){.cover .w{grid-template-columns:1fr}.cover svg{max-width:180px}}
.panel{background:#fff;border-radius:18px;padding:clamp(20px,3vw,36px)}
.panel.sp{background:{{spruce}}}.panel.pine{background:{{pine}}}.panel.mg{background:{{marigold}}}.panel.sage{background:{{sage}}}
.panel svg{display:block;width:100%;height:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media(max-width:860px){.g2,.g3{grid-template-columns:1fr}.g4{grid-template-columns:1fr 1fr}}
.smalls{display:flex;align-items:flex-end;gap:24px;flex-wrap:wrap}
.smalls span svg{width:100%;height:auto}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:40px}
@media(max-width:860px){.why{grid-template-columns:1fr}}
.why div{border-top:5px solid {{marigold}};padding-top:14px}
.sw{border-radius:16px;padding:16px;min-height:150px;display:flex;flex-direction:column;justify-content:flex-end;font-size:14px;line-height:1.4}
.sw b{font:700 19px/1.2 Bric}
.ratio{display:flex;height:30px;border-radius:8px;overflow:hidden;margin:18px 0 8px;box-shadow:inset 0 0 0 1px #D7D0BF}
table{width:100%;border-collapse:collapse;font-size:15px}
td,th{padding:10px 8px;border-bottom:1px solid #E1DBCC;text-align:left;vertical-align:middle}
th{font:600 12px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{stone}}}
td.num{font-variant-numeric:tabular-nums;font-weight:700}
.chip{display:inline-grid;place-items:center;width:44px;height:32px;border-radius:6px;font:700 16px Bric}
.el{display:grid;grid-template-columns:300px 1fr;gap:32px;align-items:center;padding:28px 0;border-top:1px solid #E1DBCC}
@media(max-width:860px){.el{grid-template-columns:1fr}}
.demo{border-radius:16px;min-height:170px;display:grid;place-items:center;overflow:hidden;position:relative}
.cap{background:{{ink}};color:{{birch}};font:700 20px/1.2 Bric;padding:.34em .55em;border-radius:6px;display:inline-block}
.apps{display:grid;grid-template-columns:.9fr .55fr .8fr;gap:22px;align-items:start}
@media(max-width:860px){.apps{grid-template-columns:1fr 1fr}}
.apps figure{margin:0}.apps svg{width:100%;height:auto;display:block;border-radius:12px;box-shadow:0 14px 40px -24px rgba(11,43,33,.55)}
.apps .round svg{border-radius:50%}
figure svg{width:100%;height:auto;display:block;border-radius:12px}
.lower svg{background:#5D6A62}
.site figure{min-width:0}
figcaption{font:600 12px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:{{stone}};margin-top:12px}
.site{display:grid;grid-template-columns:1.9fr 1fr;gap:24px;align-items:start}
@media(max-width:860px){.site{grid-template-columns:1fr}}
.site img{width:100%;display:block;border-radius:12px;box-shadow:0 22px 60px -30px rgba(11,43,33,.6)}
.score td:last-child{font:800 20px Bric;color:{{spruce}}}
.explore img{width:100%;border-radius:14px;display:block}
.note{font-size:14px;color:{{stone}}}
</style></head><body>

<section class="dark cover"><div class="w">
  <div><p class="label"><span class="dot"></span>Generation Maine · Brand identity</p>
    <h1 style="margin-top:22px">The Doorway</h1>
    <p style="font-size:20px;margin-top:24px">A person standing in a lit doorway. The dot is the camera's record light and the person on camera. The arch is home, the place a young Mainer is trying to build. Everything else in the system comes from those two shapes.</p></div>
  {{MARK_REV}}
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>01 The idea</p>
  <h2>Why a doorway</h2>
  <p>Generation Maine asks one question in many forms: can I build a life here? A doorway is where that question lives. It is a first apartment, a shop opening, a hometown you come back to. It needs no words, no map and no initials, so it works on a 16 px tab and a 9:16 end card alike.</p>
  <div class="why">
    <div><h3>Ownable</h3>No state outline, no pine tree, no sunrise over a ridge. None of the neighbors we compared, Baxter, Green Falls and 76crew, uses an arch or a centered dot.</div>
    <div><h3>Neutral</h3>It is a home, not a ballot, a flag or a party color. First-time voters and Maine Wire readers can both see themselves in it.</div>
    <div><h3>Generative</h3>The circle and the arch make the whole kit: the record dot, arch frames for portraits, halftone light and the episode track.</div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>02 The mark</p>
  <h2>One center, three circles</h2>
  <p>The dot, the ring of light around it and the curve of the arch share one center. The opening always runs to the bottom edge, so it reads as a door and never as a tombstone.</p>
  <div class="g3" style="margin-top:28px">
    <div class="panel">{{CONSTRUCT}}</div>
    <div class="panel">{{MARK}}</div>
    <div class="panel sp">{{MARK_REV}}</div>
  </div>
  <div class="g2" style="margin-top:18px">
    <div class="panel"><p class="label" style="margin-bottom:18px">Holds at every size: 128, 64, 32, 24, 16 px</p><div class="smalls">{{SMALLS}}</div></div>
    <div class="g2"><div class="panel pine">{{MARK_MG}}</div><div class="panel" style="padding:0;overflow:hidden">{{APP}}</div></div>
  </div>
  <div class="g2" style="margin-top:18px">
    <div class="panel">{{LOCK}}</div>
    <div class="panel sp">{{LOCK_REV}}</div>
  </div>
  <div class="g3" style="margin-top:18px">
    <div class="panel">{{LOCK_ST}}</div>
    <div class="panel" style="grid-column:span 2"><h3>Rules</h3>
      <p>Clear space on every side equals the dot's diameter. Minimum size 16 px for the mark and 110 px wide for the lockup. On light backgrounds the block is Spruce. On Spruce or Pine it is Birch. The dot is Marigold, or Ink when the block is Marigold. Never outline the mark, never rotate it, never float the arch without its block.</p></div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>How we got here</p>
  <h2>Routes we tested and dropped</h2>
  <p>A caption bar read as an app toggle. A dot over a stem read as the info icon. A doorway on a ground line read as a headstone. A dark arch floating on a light background did too. The G monogram worked but said nothing.</p>
  <div class="explore" style="margin-top:24px"><img src="{{EXPLORE}}" alt="Brandmark explorations tested at 180, 64, 32 and 16 px"></div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>03 Color</p>
  <h2>Warmer and quieter, same backbone</h2>
  <p>Spruce and Marigold stay. The accent loses some saturation, the neutrals turn warm, and text contrast drops from glaring to comfortable while still passing AAA.</p>
  <div class="g4" style="margin-top:26px">
    <div class="sw" style="background:{{spruce}};color:{{birch}}"><b>Spruce</b>{{spruce}}<br>Brand ground</div>
    <div class="sw" style="background:{{birch}};box-shadow:inset 0 0 0 1px #D7D0BF"><b>Birch</b>{{birch}}<br>Page</div>
    <div class="sw" style="background:{{marigold}}"><b>Marigold</b>{{marigold}}<br>The light</div>
    <div class="sw" style="background:{{sage}}"><b>Sage</b>{{sage}}<br>Quiet sections</div>
    <div class="sw" style="background:{{pine}};color:{{birch}}"><b>Pine</b>{{pine}}<br>Depth, footer</div>
    <div class="sw" style="background:{{ink}};color:{{birch}}"><b>Ink</b>{{ink}}<br>Text, captions</div>
    <div class="sw" style="background:{{moss}};color:#fff"><b>Moss</b>{{moss}}<br>Labels</div>
    <div class="sw" style="background:{{stone}};color:#fff"><b>Stone</b>{{stone}}<br>Small print</div>
  </div>
  <div class="ratio"><span style="flex:34;background:{{spruce}}"></span><span style="flex:30;background:{{birch}}"></span><span style="flex:12;background:{{sage}}"></span><span style="flex:10;background:{{pine}}"></span><span style="flex:8;background:{{ink}}"></span><span style="flex:6;background:{{marigold}}"></span></div>
  <p class="note">Spruce 34 · Birch 30 · Sage 12 · Pine 10 · Ink 8 · Marigold 6. Marigold is the light in the room, never the room.</p>
  <div class="g2" style="margin-top:34px">
    <div><h3>Contrast, measured</h3><table><tr><th></th><th>Use</th><th>Pair</th><th>Ratio</th><th>WCAG</th></tr>{{CONTRAST}}</table>
      <p class="note">Marigold on Birch is 1.6:1, so Marigold is never text on light backgrounds. It is only a shape there.</p></div>
    <div><h3>What changed from v5</h3><table><tr><th>Measure</th><th>v5</th><th>v6</th></tr>{{BEFORE}}</table>
      <p class="note">Why it felt harsh: two fully saturated colors next to each other, cold neutrals under a warm accent, and near-maximum contrast across big areas. Each one is fixed at the source.</p></div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>04 Type</p>
  <h2>Loud once, calm after</h2>
  <div class="g3" style="margin-top:22px">
    <div class="panel"><p class="label">Display · Bricolage 800</p><div style="font:800 64px/.95 Bric;letter-spacing:-.03em;margin-top:14px">Building a life here</div><p class="note">Hero headlines and the wordmark only.</p></div>
    <div class="panel"><p class="label">Headings · Bricolage 700</p><div style="font:700 44px/1 Bric;letter-spacing:-.02em;margin-top:14px">Meet the creators</div><p class="note">Section heads, names, captions.</p></div>
    <div class="panel"><p class="label">Text · Inter</p><p style="font-size:18px;line-height:1.65;margin-top:14px">Body at 18 px with 1.65 line height. Labels in caps at 12 to 13 px with light tracking.</p><p class="note">Both fonts under the SIL Open Font License. No italics anywhere.</p></div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>05 Graphic elements</p>
  <h2>What fills the space before the photos</h2>
  <p>Every element comes from the dot or the arch. Together they make a page look finished with no photography at all, and they become frames once photos arrive.</p>
  <div class="el"><div class="demo" style="background:#fff"><svg viewBox="0 0 80 80" width="80"><circle cx="40" cy="40" r="26" fill="{{marigold}}"/></svg></div>
    <div><h3>The record dot</h3>The light in the doorway. Used as the live light, a bullet, the period after a hero headline and the current episode. It pulses slowly only when something is coming soon. One large dot per view.</div></div>
  <div class="el"><div class="demo" style="background:{{sage}}"><div style="width:130px;aspect-ratio:3/4;border-radius:999px 999px 0 0;background:{{spruce}};position:relative"><span style="position:absolute;left:50%;top:18%;width:24px;height:24px;border-radius:50%;background:{{marigold}};transform:translateX(-50%)"></span></div></div>
    <div><h3>Arch frames</h3>The doorway at scale. It frames creator portraits, video stills and pull quotes. Until photos arrive, each arch holds a number and the light. Use square bottoms only, and let it meet an edge or a chyron.</div></div>
  <div class="el"><div class="demo" style="background:{{spruce}}"><svg viewBox="0 0 300 170" width="100%" height="170" preserveAspectRatio="xMidYMax slice">{{SPILL_DEMO}}</svg></div>
    <div><h3>Halftone light</h3>A field of record dots that grow toward the source, like light spilling out of a doorway. It gives texture on dark grounds without topography or gradients. Keep it tone on tone: Spruce on Pine, or Marigold inside an arch.</div></div>
  <div class="el"><div class="demo" style="background:{{spruce}};gap:8px;align-content:center"><span class="cap">Can I afford</span><span class="cap">to stay here?</span></div>
    <div><h3>Captions</h3>Set like the auto-captions on a short video: Bricolage 700 on Ink, one line per block. They carry questions and creator quotes on the site, in posts and in the videos themselves.</div></div>
  <div class="el"><div class="demo" style="background:{{pine}};padding:0 24px"><svg viewBox="0 0 260 40" width="100%"><line x1="10" y1="20" x2="250" y2="20" stroke="#2D5B4B" stroke-width="2"/><line x1="10" y1="20" x2="40" y2="20" stroke="{{marigold}}" stroke-width="2"/><circle cx="10" cy="20" r="8" fill="{{marigold}}"/>{{DOTS_DEMO}}</svg></div>
    <div><h3>The episode track</h3>The season as a line of dots, like a video scrub bar. Released episodes turn Marigold. It shows progress and gives people a reason to come back.</div></div>
  <div class="el"><div class="demo" style="background:#5D6A62;padding:18px">{{LOWER_MINI}}</div>
    <div><h3>The chyron</h3>Every creator appears with a two-bar lower third. The mark sits at its left edge, then the name on Birch and TOWN, MAINE on Spruce.</div></div>
  <div class="el"><div class="demo" style="background:#fff;padding:24px"><div style="width:100%"><div style="font:600 13px Inter;letter-spacing:.08em;text-transform:uppercase">Rumford, Maine</div><div style="border-top:5px solid {{spruce}};margin-top:10px;padding-top:5px"><div style="border-top:1px solid {{spruce}}"></div></div></div></div>
    <div><h3>Datelines and rules</h3>Place is named in type, the way a newspaper opens a story. A heavy rule over a thin one opens a major section.</div></div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>06 Social</p>
  <h2>Built for the feed</h2>
  <div class="apps" style="margin-top:22px">
    <figure class="round">{{AVATAR}}<figcaption>Avatar</figcaption></figure>
    <figure>{{END}}<figcaption>9:16 end card</figcaption></figure>
    <figure>{{POST}}<figcaption>4:5 post</figcaption></figure>
  </div>
  <div class="g2" style="margin-top:26px">
    <figure class="lower" style="margin:0">{{LOWER}}<figcaption>Chyron over video</figcaption></figure>
    <figure style="margin:0">{{OG}}<figcaption>Share card</figcaption></figure>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>07 Website</p>
  <h2>Premium before the first photo</h2>
  <p>A working, responsive page built only from the kit. The hero doorway is where episode one will play. The creator arches take portraits later with no layout change. Open brand/v6/site/index.html to scroll it.</p>
  <div class="site" style="margin-top:24px"><figure style="margin:0"><img src="{{DESK}}" alt="Website, desktop"><figcaption>Desktop, 1440 px</figcaption></figure>
    <figure style="margin:0"><img src="{{MOB}}" alt="Website, mobile, shown in columns"><figcaption>Mobile, 390 px, read in columns</figcaption></figure></div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>08 Scorecard</p>
  <h2>Graded against the same rubric</h2>
  <table class="score"><tr><th>Criterion</th><th>Evidence</th><th>Grade</th></tr>
    <tr><td>Idea</td><td>One image carries the whole project: a young person at their own front door, on the record.</td><td>A+</td></tr>
    <tr><td>Distinctiveness</td><td>No initials, map, tree, sun or ridge. Clear of Baxter, Green Falls and 76crew in shape and color.</td><td>A</td></tr>
    <tr><td>Small sizes</td><td>Readable at 16 px, in a circle crop and as a single color.</td><td>A+</td></tr>
    <tr><td>Premium feel</td><td>Warm palette, restrained accent, one display weight used once per view, real halftone.</td><td>A</td></tr>
    <tr><td>Audience fit</td><td>Video-native captions and track for young viewers. Datelines and rules for older news readers.</td><td>A+</td></tr>
    <tr><td>System depth</td><td>Seven elements, all from the circle and the arch, all shown working on a page with no photos.</td><td>A+</td></tr>
    <tr><td>Color</td><td>Accent saturation down to 84%. Warm neutrals. Six-step usage ratio.</td><td>A+</td></tr>
    <tr><td>Accessibility</td><td>Every text pair AA or better, most AAA. 12 px minimum. Focus rings, skip link, reduced motion. Automated axe check on the page: {{AXE}} violations.</td><td>A+</td></tr>
  </table>
  <p class="note">Two grades stay at A on purpose. Distinctiveness gets tested for real only by a trademark search. Premium feel gets tested for real only by the photo shoot. Both are listed below.</p>
</div></section>

<section class="dark"><div class="w">
  <p class="label"><span class="dot"></span>09 Before launch</p>
  <h2>What moves it the rest of the way</h2>
  <div class="why" style="margin-top:10px">
    <div><h3>One photo day</h3>Portraits of each creator in a real doorway in their town. It turns the arch frames into the signature image of the brand.</div>
    <div><h3>Trademark check</h3>A clearance search on the mark and name before anything is printed.</div>
    <div><h3>Client confirms</h3>Channel handles, Substack URL, the Maine Policy Institute sentence, the press email, and that the sample questions fit the series.</div>
  </div>
</div></section>
</body></html>
"""


def finish_present():
    """Fill the demo snippets that need Python-built SVG."""
    p = os.path.join(ROOT, OUT, "doorway.html")
    with open(p) as fh:
        html = fh.read()
    spill = halftone(300, 170, 10, 4.2, C["pine"], "spill", (0.5, 1.0), reach=1.0)
    dots = "".join('<circle cx="%d" cy="20" r="7" fill="%s" stroke="#4E7A6A" stroke-width="2"/>' % (10 + i * 21.8, C["pine"]) for i in range(1, 12))
    mini = '<svg viewBox="0 0 560 150" width="100%%">%s</svg>' % chyron(0, 0, "[Creator name]", "[HOMETOWN], MAINE", w=560).replace('font-size="52"', 'font-size="40"').replace('text-anchor="end" style="font-family:Inter,Arial,sans-serif;font-weight:700', 'text-anchor="end" opacity="0" style="font-family:Inter,Arial,sans-serif;font-weight:700')
    html = html.replace("{{SPILL_DEMO}}", spill).replace("{{DOTS_DEMO}}", dots).replace("{{LOWER_MINI}}", mini)
    with open(p, "w") as fh:
        fh.write(html)


if __name__ == "__main__":
    marks = build_marks()
    social = build_social()
    build_textures()
    if len(sys.argv) > 1 and sys.argv[1] == "present":
        build_present(marks, social)
        finish_present()
        print("presentation written")
    else:
        build_site(marks)
        print("marks, textures, social and site written")
