"""Builds identity v2 for both directions.

Outputs:
  brand/v2/first-light/logo/*.svg     A2 brandmark files
  brand/v2/first-light/social/*.svg   A2 applications
  brand/v2/postmark/logo/*.svg        B2 brandmark files
  brand/v2/postmark/social/*.svg      B2 applications
  brand/v2/identity-v2.html           presentation page (self-contained)

Run from the repo root: python3 brand/src/build_v2.py && node brand/src/render_v2.mjs
"""
import base64
import math
import os

from gmlib import ROOT, write
from v2marks import (A2, B2, ANTON, a2_lockup_h, a2_lockup_stacked, a2_symbol, b2_cancel_lines,
                     b2_lockup, b2_postmark, b2_small, f)

OUT = "brand/v2"


def svg(w, h, body, title, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" '
            'aria-label="%s">%s%s</svg>\n' % (f(w), f(h), f(w), f(h), title,
                                               ("<defs>%s</defs>" % defs) if defs else "", body))


def rect(w, h, fill, x=0, y=0, rx=0):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h), f(rx), fill)


def placed(body, x, y, scale):
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (f(x), f(y), f(scale), body)


SANS = "font-family:'Instrument Sans',Arial,sans-serif"
SERIF = "font-family:'Instrument Serif',Georgia,serif;font-style:italic"
ANT = "font-family:Anton,'Arial Narrow',sans-serif"
MONO = "font-family:'IBM Plex Mono',Menlo,monospace"


def t(x, y, s, size, fill, style=SANS, weight=400, anchor="start", ls=0, upper=False):
    st = "%s;font-weight:%d;letter-spacing:%sem%s" % (style, weight, ls, ";text-transform:uppercase" if upper else "")
    return '<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" style="%s">%s</text>' % (
        f(x), f(y), f(size), fill, anchor, st, s)


def horizon_rule(x1, x2, y, color, dot, dot_x=None, w=2, r=9):
    dx = dot_x if dot_x is not None else x2 - r
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x1), f(y), f(x2), f(y), color, f(w), f(dx), f(y - r), f(r), dot))


def silhouette(x, y, w, h, bg, fg, label, label_color, font=SANS):
    """Placeholder for a creator photo: flat background, simple head-and-shoulders shape, a label."""
    cx = x + w / 2
    head_r = min(w, h) * 0.16
    body = rect(w, h, bg, x, y)
    body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(y + h * 0.42), f(head_r), fg)
    body += '<path d="M%s %s Q%s %s %s %s L%s %s Q%s %s %s %s Z" fill="%s"/>' % (
        f(cx - w * 0.36), f(y + h), f(cx - w * 0.34), f(y + h * 0.62), f(cx), f(y + h * 0.62),
        f(cx), f(y + h * 0.62), f(cx + w * 0.34), f(y + h * 0.62), f(cx + w * 0.36), f(y + h), fg)
    body += t(x + 24, y + 44, label, 22, label_color, font, 500, ls=0.08, upper=True)
    return body


def perforated(x, y, w, h, fill, hole=7, pitch=24, bg="#ECECE6", mid=""):
    """A stamp with perforated edges: the holes are drawn in the background color."""
    body = rect(w, h, fill, x, y)
    body += mid
    n_w, n_h = int(w // pitch), int(h // pitch)
    sx, sy = (w - (n_w - 1) * pitch) / 2, (h - (n_h - 1) * pitch) / 2
    for i in range(n_w):
        for yy in (y, y + h):
            body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x + sx + i * pitch), f(yy), hole, bg)
    for j in range(n_h):
        for xx in (x, x + w):
            body += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(xx), f(y + sy + j * pitch), hole, bg)
    return body


# ============================================================ A2 First Light
def build_a2():
    a = A2
    d = OUT + "/first-light"
    variants = {
        "": (a["granite"], a["signal"], a["spruce"]),
        "-reversed": (a["fog"], a["signal"], a["fog"]),
        "-black": ("#000", "#000", "#000"),
        "-white": ("#fff", "#fff", "#fff"),
    }
    for suf, (fg, sun, ring) in variants.items():
        b, w, h = a2_lockup_h(fg, sun, ring)
        write("%s/logo/horizontal%s.svg" % (d, suf), svg(w, h, b, "Generation Maine"))
        b, w, h = a2_lockup_stacked(fg, sun, ring)
        write("%s/logo/stacked%s.svg" % (d, suf), svg(w, h, b, "Generation Maine"))
        write("%s/logo/symbol%s.svg" % (d, suf), svg(200, 200, a2_symbol(0, 0, 200, ring, sun), "Generation Maine"))
    write(d + "/logo/app-icon.svg", svg(512, 512, rect(512, 512, a["spruce"], rx=112)
                                        + a2_symbol(116, 116, 280, a["fog"], a["signal"]), "Generation Maine"))

    s = {}
    # Avatar
    s["avatar-1080"] = svg(1080, 1080, rect(1080, 1080, a["spruce"]) + a2_symbol(250, 250, 580, a["fog"], a["signal"]),
                           "Generation Maine avatar")
    # End card
    b = rect(1080, 1920, a["spruce"])
    b += t(540, 250, "Generation Maine", 30, a["dawn"], SANS, 600, "middle", 0.22, True)
    b += a2_symbol(390, 420, 300, a["fog"], a["signal"])
    b += t(540, 930, "Follow along", 128, a["fog"], SERIF, 400, "middle")
    rows = [("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com")]
    y = 1100
    for label, handle in rows:
        b += t(470, y, label, 30, a["dawn"], SANS, 600, "end", 0.14, True)
        b += t(510, y, handle, 40, a["fog"], SANS, 500)
        y += 84
    b += horizon_rule(140, 940, 1560, a["moss"], a["signal"], dot_x=540)
    b += t(540, 1650, "An initiative of Maine Policy Institute", 32, a["fog"], SANS, 500, "middle")
    s["end-card-1080x1920"] = svg(1080, 1920, b, "Generation Maine end card")
    # Thumbnail
    b = rect(1280, 720, a["pine"])
    b += silhouette(660, 0, 620, 720, "#0F3A2B", "#1A5640", "[Creator photo]", a["dawn"])
    b += a2_symbol(64, 60, 76, a["fog"], a["signal"])
    b += t(64, 390, "[What rent]", 104, a["fog"], SANS, 700, ls=-0.02)
    b += t(64, 505, "[costs here]", 116, a["dawn"], SERIF, 400)
    b += horizon_rule(64, 560, 620, a["moss"], a["signal"])
    s["youtube-thumbnail-1280x720"] = svg(1280, 720, b, "Generation Maine thumbnail")
    # Lower third
    b = rect(820, 172, a["fog"], 96, 812, 26)
    b += a2_symbol(126, 848, 100, a["spruce"], a["signal"])
    b += t(254, 896, "[Creator name]", 60, a["granite"], SANS, 600, ls=-0.01)
    b += t(256, 952, "[Hometown], Maine", 46, a["moss"], SERIF, 400)
    s["lower-third-1920x1080"] = svg(1920, 1080, b, "Generation Maine lower third")
    # Open Graph
    b = rect(1200, 630, a["spruce"])
    b += '<g opacity="0.22">%s</g>' % a2_symbol(760, 150, 620, a["moss"], a["moss"])
    lk, lw, lh = a2_lockup_h(a["fog"], a["signal"], a["fog"])
    b += placed(lk, 80, 190, 820 / lw)
    b += ('<text x="84" y="420" font-size="46" fill="%s" style="%s;font-weight:500">Young Mainers on building a life '
          '<tspan style="%s;font-weight:400" fill="%s" font-size="52">here.</tspan></text>' % (a["fog"], SANS, SERIF, a["dawn"]))
    b += t(84, 560, "An initiative of Maine Policy Institute", 26, a["fog"], SANS, 500, ls=0.02)
    s["og-share-card-1200x630"] = svg(1200, 630, b, "Generation Maine")
    # YouTube banner
    b = rect(2560, 1440, a["spruce"])
    b += '<g opacity="0.18">%s</g>' % a2_symbol(1900, -260, 1100, a["moss"], a["moss"])
    lk, lw, lh = a2_lockup_h(a["fog"], a["signal"], a["fog"])
    b += placed(lk, 1280 - 1000 / 2, 560, 1000 / lw)
    b += ('<text x="1280" y="840" font-size="60" text-anchor="middle" fill="%s" style="%s;font-weight:500">Young Mainers on building a life '
          '<tspan style="%s;font-weight:400" fill="%s" font-size="68">here.</tspan></text>' % (a["fog"], SANS, SERIF, a["dawn"]))
    s["youtube-banner-2560x1440"] = svg(2560, 1440, b, "Generation Maine banner")
    for k, v in s.items():
        write("%s/social/%s.svg" % (d, k), v)
    return s


# ============================================================ B2 Postmark
def build_b2():
    b2 = B2
    d = OUT + "/postmark"
    for suf, (ink, accent) in {"": (b2["blueberry"], None), "-ink": (b2["ink"], None), "-white": ("#fff", None),
                               "-black": ("#000", None)}.items():
        write("%s/logo/postmark%s.svg" % (d, suf), svg(200, 200, b2_postmark(100, 100, 100, ink), "Generation Maine"))
        body, w, h = b2_lockup(ink)
        write("%s/logo/lockup%s.svg" % (d, suf), svg(w, h, body, "Generation Maine"))
        write("%s/logo/small%s.svg" % (d, suf), svg(200, 200, b2_small(100, 100, 100, ink), "Generation Maine"))
    write(d + "/logo/app-icon.svg", svg(512, 512, rect(512, 512, b2["blueberry"], rx=112)
                                        + b2_small(256, 256, 170, b2["newsprint"]), "Generation Maine"))
    towns = [("LEWISTON", "POSTED 11.2026"), ("BANGOR", "POSTED 11.2026"), ("CARIBOU", "POSTED 12.2026"), ("BIDDEFORD", "POSTED 12.2026")]
    for town, sub in towns:
        write("%s/logo/creator-stamp-%s.svg" % (d, town.lower()),
              svg(200, 200, b2_postmark(100, 100, 100, b2["ink"], center_text=town, center_sub=sub), "Generation Maine, " + town.title()))

    s = {}
    s["avatar-1080"] = svg(1080, 1080, rect(1080, 1080, b2["blueberry"]) + b2_small(540, 540, 330, b2["newsprint"]),
                           "Generation Maine avatar")
    # End card
    b = rect(1080, 1920, b2["newsprint"])
    b += '<g transform="rotate(-6 400 640)">%s%s</g>' % (b2_postmark(400, 640, 290, b2["blueberry"]),
                                                          b2_cancel_lines(400 + 290 * 0.95, 640, 900, 290, b2["blueberry"]))
    b += '<rect x="100" y="1090" width="700" height="120" fill="%s" transform="rotate(-2 450 1150)"/>' % b2["yellow"]
    b += t(120, 1190, "FOLLOW ALONG", 120, b2["ink"], ANT, 400, ls=0.02)
    y = 1320
    for label, handle in [("INSTAGRAM", "[@handle]"), ("TIKTOK", "[@handle]"), ("YOUTUBE", "[@handle]"), ("SUBSTACK", "[name].substack.com")]:
        b += t(120, y, label, 30, b2["blueberry"], MONO, 500, ls=0.06)
        b += t(420, y, handle, 36, b2["ink"], MONO, 500)
        y += 70
    b += t(120, 1740, "AN INITIATIVE OF MAINE POLICY INSTITUTE", 28, b2["ink"], MONO, 500, ls=0.04)
    s["end-card-1080x1920"] = svg(1080, 1920, b, "Generation Maine end card")
    # Thumbnail
    b = rect(1280, 720, b2["newsprint"])
    mid = silhouette(70, 70, 520, 580, b2["blueberry"], "#5B50E0", "[Creator photo]", b2["newsprint"], MONO)
    b += perforated(70, 70, 520, 580, b2["blueberry"], mid=mid, bg=b2["newsprint"])
    b += '<g transform="rotate(-8 560 600)">%s</g>' % b2_postmark(560, 600, 105, b2["ink"])
    b += '<rect x="650" y="362" width="580" height="112" fill="%s" transform="rotate(-1.5 930 414)"/>' % b2["yellow"]
    b += t(664, 330, "[WHAT RENT]", 104, b2["ink"], ANT, 400, ls=0.01)
    b += t(664, 452, "[COSTS HERE]", 104, b2["ink"], ANT, 400, ls=0.01)
    b += t(666, 560, "GENERATION MAINE / EP. [00]", 26, b2["blueberry"], MONO, 500, ls=0.06)
    s["youtube-thumbnail-1280x720"] = svg(1280, 720, b, "Generation Maine thumbnail")
    # Lower third
    b = '<g transform="rotate(-1.2 500 900)">%s</g>' % rect(780, 176, b2["yellow"], 96, 812)
    b += b2_small(186, 900, 62, b2["ink"])
    b += t(276, 900, "[CREATOR NAME]", 70, b2["ink"], ANT, 400, ls=0.02)
    b += t(278, 950, "[HOMETOWN], ME", 30, b2["ink"], MONO, 500, ls=0.06)
    s["lower-third-1920x1080"] = svg(1920, 1080, b, "Generation Maine lower third")
    # OG
    b = rect(1200, 630, b2["newsprint"])
    b += '<g transform="rotate(-6 250 300)">%s%s</g>' % (b2_postmark(250, 300, 175, b2["blueberry"]),
                                                          b2_cancel_lines(250 + 175 * 0.95, 300, 1000, 175, b2["blueberry"]))
    b += '<rect x="500" y="446" width="620" height="76" fill="%s"/>' % b2["yellow"]
    b += t(512, 505, "YOUNG MAINERS, OWN WORDS", 58, b2["ink"], ANT, 400, ls=0.01)
    b += t(512, 575, "AN INITIATIVE OF MAINE POLICY INSTITUTE", 22, b2["ink"], MONO, 500, ls=0.04)
    s["og-share-card-1200x630"] = svg(1200, 630, b, "Generation Maine")
    # Banner
    b = rect(2560, 1440, b2["newsprint"])
    b += '<g transform="rotate(-6 820 720)">%s%s</g>' % (b2_postmark(820, 720, 250, b2["blueberry"]),
                                                          b2_cancel_lines(820 + 250 * 0.95, 720, 1100, 250, b2["blueberry"]))
    b += t(1180, 950, "[@handle]  /  GENERATIONMAINE.ORG", 40, b2["ink"], MONO, 500, ls=0.04)
    s["youtube-banner-2560x1440"] = svg(2560, 1440, b, "Generation Maine banner")
    for k, v in s.items():
        write("%s/social/%s.svg" % (d, k), v)
    return s


def inner(svg_text):
    """Strip the outer svg tag's size so it can scale inside a container."""
    return svg_text.replace('role="img"', 'role="img" preserveAspectRatio="xMidYMid meet"', 1)


def font64(name):
    with open(os.path.join(ROOT, "brand/v2/fonts-web", name), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def build_presentation(sa, sb):
    a, b2 = A2, B2
    # animated symbol: the sun rises from behind the horizon, then blinks like a record light
    s_anim = a2_symbol(0, 0, 200, a["fog"], a["signal"]).replace(
        '<circle ', '<circle class="sun" ', 1)
    s_anim = ('<svg viewBox="0 0 200 200" class="anim-a" role="img" aria-label="First Light brandmark, animated">'
              '<defs><clipPath id="above"><rect x="0" y="-60" width="200" height="160"/></clipPath></defs>'
              + s_anim.replace('<circle class="sun"', '<circle clip-path="url(#above)" class="sun"') + '</svg>')
    pm_anim = ('<svg viewBox="-20 -20 700 240" class="anim-b" role="img" aria-label="Postmark brandmark, animated">'
               '<g class="stamp">%s</g><g class="lines">%s</g></svg>' % (
                   b2_postmark(100, 100, 100, b2["blueberry"]), b2_cancel_lines(195, 100, 440, 100, b2["blueberry"])))

    def logo(path):
        with open(os.path.join(ROOT, path)) as fh:
            return inner(fh.read())

    # construction diagram for A2
    cons = a2_symbol(0, 0, 200, a["spruce"], a["signal"])
    cons_diag = ('<svg viewBox="-50 -34 300 290" class="cons" role="img" aria-label="Construction of the First Light brandmark">'
                 '<circle cx="100" cy="100" r="100" fill="none" stroke="#9AA4B2" stroke-dasharray="3 4"/>'
                 '<circle cx="100" cy="100" r="74" fill="none" stroke="#9AA4B2" stroke-dasharray="3 4"/>'
                 '<line x1="-20" y1="100" x2="220" y2="100" stroke="%s" stroke-width="1"/>' % a["signal"]
                 + cons +
                 '<text x="-48" y="94" font-size="9" fill="#6B7380" style="%s">horizon</text>' % SANS +
                 '<text x="168" y="30" font-size="9" fill="#6B7380" style="%s">sun / record light</text>' % SANS +
                 '<text x="100" y="236" text-anchor="middle" font-size="9" fill="#6B7380" style="%s">ring 100 · stroke 26 · sun 21 · gap 9</text></svg>' % SANS)

    towns = "".join('<figure>%s<figcaption>%s</figcaption></figure>' % (
        logo("brand/v2/postmark/logo/creator-stamp-%s.svg" % tn), tn.title()) for tn in ["lewiston", "bangor", "caribou", "biddeford"])

    def app(sset, key, cls, cap):
        return '<figure class="%s">%s<figcaption>%s</figcaption></figure>' % (cls, inner(sset[key]), cap)

    html = TEMPLATE
    rep = {
        "{{F_SANS}}": font64("instrument-sans.woff2"), "{{F_SERIF_I}}": font64("instrument-serif-italic.woff2"),
        "{{F_SERIF}}": font64("instrument-serif.woff2"), "{{F_ANTON}}": font64("anton-400.woff2"),
        "{{F_MONO}}": font64("plex-mono-500.woff2"),
        "{{A_ANIM}}": s_anim, "{{B_ANIM}}": pm_anim, "{{A_CONS}}": cons_diag,
        "{{A_H}}": logo(OUT + "/first-light/logo/horizontal.svg"),
        "{{A_H_REV}}": logo(OUT + "/first-light/logo/horizontal-reversed.svg"),
        "{{A_ST}}": logo(OUT + "/first-light/logo/stacked.svg"),
        "{{A_SYM}}": logo(OUT + "/first-light/logo/symbol.svg"),
        "{{A_SYM_REV}}": logo(OUT + "/first-light/logo/symbol-reversed.svg"),
        "{{A_ICON}}": logo(OUT + "/first-light/logo/app-icon.svg"),
        "{{A_AVATAR}}": app(sa, "avatar-1080", "round", "Avatar"),
        "{{A_END}}": app(sa, "end-card-1080x1920", "tall", "9:16 end card"),
        "{{A_THUMB}}": app(sa, "youtube-thumbnail-1280x720", "wide", "YouTube thumbnail"),
        "{{A_LOWER}}": app(sa, "lower-third-1920x1080", "wide lower", "Lower third over footage"),
        "{{A_OG}}": app(sa, "og-share-card-1200x630", "wide", "Share card"),
        "{{B_PM}}": logo(OUT + "/postmark/logo/postmark.svg"),
        "{{B_LOCK}}": logo(OUT + "/postmark/logo/lockup.svg"),
        "{{B_SMALL}}": logo(OUT + "/postmark/logo/small.svg"),
        "{{B_ICON}}": logo(OUT + "/postmark/logo/app-icon.svg"),
        "{{B_TOWNS}}": towns,
        "{{B_AVATAR}}": app(sb, "avatar-1080", "round", "Avatar"),
        "{{B_END}}": app(sb, "end-card-1080x1920", "tall", "9:16 end card"),
        "{{B_THUMB}}": app(sb, "youtube-thumbnail-1280x720", "wide", "YouTube thumbnail"),
        "{{B_LOWER}}": app(sb, "lower-third-1920x1080", "wide lower", "Lower third over footage"),
        "{{B_OG}}": app(sb, "og-share-card-1200x630", "wide", "Share card"),
        "{{A_SMALLS}}": "".join('<span style="width:%dpx;height:%dpx">%s</span>' % (z, z, logo(OUT + "/first-light/logo/symbol.svg")) for z in (96, 48, 32, 16)),
        "{{B_SMALLS}}": "".join('<span style="width:%dpx;height:%dpx">%s</span>' % (z, z, logo(OUT + "/postmark/logo/small.svg")) for z in (96, 48, 32, 16)),
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    for k, v in A2.items():
        html = html.replace("{{A.%s}}" % k, v)
    for k, v in B2.items():
        html = html.replace("{{B.%s}}" % k, v)
    write(OUT + "/identity-v2.html", html)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine identity v2</title>
<style>
@font-face{font-family:'Instrument Sans';src:url(data:font/woff2;base64,{{F_SANS}}) format("woff2");font-weight:400 700}
@font-face{font-family:'Instrument Serif';font-style:italic;src:url(data:font/woff2;base64,{{F_SERIF_I}}) format("woff2")}
@font-face{font-family:'Instrument Serif';font-style:normal;src:url(data:font/woff2;base64,{{F_SERIF}}) format("woff2")}
@font-face{font-family:Anton;src:url(data:font/woff2;base64,{{F_ANTON}}) format("woff2")}
@font-face{font-family:'IBM Plex Mono';src:url(data:font/woff2;base64,{{F_MONO}}) format("woff2");font-weight:400 700}
:root{--pad:clamp(20px,5vw,72px)}
*{box-sizing:border-box}
html{-webkit-font-smoothing:antialiased}
body{margin:0;background:#fff;color:{{A.granite}};font:17px/1.6 'Instrument Sans',system-ui,sans-serif}
em,.serif{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400}
section{padding:clamp(56px,9vw,128px) var(--pad);position:relative}
.wrap{max-width:1240px;margin:0 auto}
.label{font:600 12px/1 'Instrument Sans';letter-spacing:.2em;text-transform:uppercase;margin:0 0 20px;opacity:.75}
h1{font:600 clamp(44px,7vw,104px)/.98 'Instrument Sans';letter-spacing:-.03em;margin:0}
h2{font:600 clamp(32px,4.4vw,60px)/1.02 'Instrument Sans';letter-spacing:-.025em;margin:0 0 24px}
h3{font:600 20px/1.2 'Instrument Sans';margin:0 0 8px}
p{margin:0 0 14px;max-width:60ch}
.lede{font-size:clamp(19px,1.8vw,23px);line-height:1.5;max-width:44ch}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,64px);align-items:center}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media (max-width:860px){.grid2,.grid3{grid-template-columns:1fr}}
svg{display:block;max-width:100%;height:auto}
figure{margin:0}
figcaption{font:500 12px/1.4 'Instrument Sans';letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin-top:12px}
.hr{height:1px;background:currentColor;opacity:.2;margin:48px 0}

/* intro */
.intro{background:#0D0F12;color:#EDF0F4}
.intro h1 em{color:#FFC7A6}
.intro .cols{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:56px}
@media (max-width:860px){.intro .cols{grid-template-columns:1fr}}
.intro .cols div{border-top:1px solid rgba(237,240,244,.22);padding-top:18px}
.intro .cols b{display:block;font-size:15px;margin-bottom:6px}
.intro .cols p{font-size:15px;opacity:.8}

/* A2 */
.a-hero{background:{{A.spruce}};color:{{A.fog}};overflow:hidden}
.a-hero .anim-a{width:min(420px,70vw)}
.a-hero h2 em{color:{{A.dawn}}}
.a-light{background:{{A.fog}}}
.a-dark{background:{{A.pine}};color:{{A.fog}}}
.tile{background:#fff;border-radius:20px;padding:clamp(24px,4vw,48px);display:grid;place-items:center;min-height:220px}
.tile.dark{background:{{A.spruce}}}
.tile.pine{background:{{A.pine}}}
.smalls{display:flex;align-items:flex-end;gap:22px;margin-top:22px}
.smalls span{display:block}
.smalls span svg{width:100%;height:100%}
.cons{max-width:360px;margin:0 auto}
.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:10px}
@media (max-width:600px){.swatches{grid-template-columns:repeat(2,1fr)}}
.sw{border-radius:16px;padding:16px;min-height:130px;display:flex;flex-direction:column;justify-content:flex-end;font-size:13px}
.sw b{font-size:16px}
.apps{display:grid;grid-template-columns:repeat(12,1fr);gap:24px;align-items:start}
.apps figure{grid-column:span 4}
.apps figure.tall{grid-column:span 3}
.apps figure.wide{grid-column:span 5}
.apps figure.round svg{border-radius:50%}
.apps figure.lower svg{background:linear-gradient(135deg,#3b4a42,#6b7a70 55%,#2a3530)}
.apps figure svg{border-radius:14px;box-shadow:0 1px 2px rgba(0,0,0,.12),0 12px 40px -18px rgba(0,0,0,.35)}
@media (max-width:860px){.apps figure,.apps figure.tall,.apps figure.wide{grid-column:span 12}}
.a-dark .apps figure.round svg,.a-dark .apps figure svg{box-shadow:0 0 0 1px rgba(237,240,244,.12)}

.web{border-radius:18px;overflow:hidden;box-shadow:0 30px 80px -30px rgba(0,0,0,.45);background:{{A.spruce}};color:{{A.fog}}}
.web .bar{display:flex;gap:6px;padding:12px 16px;background:rgba(0,0,0,.25)}
.web .bar i{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.25)}
.web .nav{display:flex;justify-content:space-between;align-items:center;padding:18px 32px}
.web .nav .l svg{height:26px;width:auto}
.web .nav span{font-size:13px;opacity:.85;margin-left:22px}
.web .body{display:grid;grid-template-columns:1.3fr 1fr;align-items:end;padding:40px 32px 0;gap:20px;position:relative}
.web .body h3{font:600 clamp(34px,4.6vw,64px)/.98 'Instrument Sans';letter-spacing:-.03em;margin:14px 0 14px}
.web .body h3 em{color:{{A.dawn}}}
.web .body .eb{font:600 11px/1 'Instrument Sans';letter-spacing:.2em;text-transform:uppercase;color:{{A.dawn}}}
.web .btn{display:inline-block;background:{{A.signal}};color:{{A.granite}};font-weight:600;font-size:14px;padding:12px 20px;border-radius:99px;margin:8px 8px 34px 0}
.web .btn.o{background:transparent;color:{{A.fog}};box-shadow:inset 0 0 0 1.5px {{A.fog}}}
.web .big{align-self:end;justify-self:end;width:min(260px,70%);margin-bottom:-6%}
.web .rule{position:relative;height:1px;background:rgba(237,240,244,.3);margin:0 32px}
.web .rule::after{content:"";position:absolute;left:12%;top:-9px;width:18px;height:18px;border-radius:50%;background:{{A.signal}}}
.web .foot{padding:22px 32px 30px;font-size:13px;opacity:.85}

/* B2 */
.b-hero{background:{{B.newsprint}};color:{{B.ink}}}
.b-hero h2,.b h2,.b-blue h2{font:400 clamp(40px,5.6vw,84px)/1.02 Anton,sans-serif;text-transform:uppercase;letter-spacing:.005em}
.b-hero .anim-b{width:min(760px,100%)}
.b{background:{{B.newsprint}};color:{{B.ink}}}
.b .label,.b-hero .label{font-family:'IBM Plex Mono';letter-spacing:.08em;color:{{B.blueberry}};opacity:1}
.b p,.b-hero p{font-family:'IBM Plex Mono';font-size:15px;line-height:1.6}
.b-blue{background:{{B.blueberry}};color:{{B.newsprint}}}
.b-blue h2{color:{{B.newsprint}}}
.b-blue .label{color:{{B.yellow}}}
.hl{background:linear-gradient(transparent 8%,{{B.yellow}} 8%,{{B.yellow}} 96%,transparent 96%);padding:0 .1em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.towns{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media (max-width:700px){.towns{grid-template-columns:repeat(2,1fr)}}
.towns figcaption{font-family:'IBM Plex Mono'}
.btile{background:#fff;border-radius:6px;padding:clamp(24px,4vw,48px);display:grid;place-items:center;min-height:220px}
.btile.blue{background:{{B.blueberry}}}

/* motion */
.anim-a .sun{animation:rise 3.2s cubic-bezier(.2,.7,.2,1) both, rec 1.6s ease-in-out 3.4s 3}
@keyframes rise{from{transform:translateY(64px)}to{transform:translateY(0)}}
@keyframes rec{0%,100%{opacity:1}50%{opacity:.25}}
.anim-b .stamp{transform-origin:100px 100px;animation:stamp .7s cubic-bezier(.3,1.6,.5,1) both}
.anim-b .lines path{stroke-dasharray:900;stroke-dashoffset:900;animation:draw 1.2s ease-out .55s forwards}
@keyframes stamp{from{transform:scale(1.35) rotate(-14deg);opacity:0}to{transform:scale(1) rotate(-6deg);opacity:1}}
@keyframes draw{to{stroke-dashoffset:0}}
.replay{font:600 12px/1 'Instrument Sans';letter-spacing:.14em;text-transform:uppercase;background:none;border:1px solid currentColor;color:inherit;border-radius:99px;padding:10px 16px;cursor:pointer;margin-top:18px}
@media (prefers-reduced-motion:reduce){.anim-a .sun,.anim-b .stamp,.anim-b .lines path{animation:none!important;stroke-dashoffset:0!important;transform:rotate(-6deg)}}
.anim-b .stamp{transform:rotate(-6deg)}
.pick{display:inline-block;background:{{A.signal}};color:{{A.granite}};font:600 11px/1 'Instrument Sans';letter-spacing:.14em;text-transform:uppercase;padding:8px 12px;border-radius:99px;margin-bottom:18px}
</style>
</head>
<body>

<section class="intro"><div class="wrap">
  <p class="label">Generation Maine · Identity v2 · September 2026</p>
  <h1>From a logo to a <em>system</em>.</h1>
  <p class="lede" style="margin-top:28px">Version 1 set the name in a nice typeface and added an orange dot. Version 2 gives each direction a real brandmark with an idea inside it, a type pairing with range, and a set of rules a small team can repeat. v1 is saved in brand/archive/v1.</p>
  <div class="cols">
    <div><b>A real brandmark</b><p>A symbol that means something, works at 16 px, and can move.</p></div>
    <div><b>Typographic contrast</b><p>A precise grotesk paired with an expressive second voice. Fewer weights, more restraint.</p></div>
    <div><b>Repeatable devices</b><p>One or two graphic devices used the same way everywhere. That consistency is what reads as premium.</p></div>
  </div>
</div></section>

<!-- ================= A2 ================= -->
<section class="a-hero"><div class="wrap grid2">
  <div>
    <span class="pick">Recommended</span>
    <p class="label" style="color:{{A.dawn}}">Direction A, v2</p>
    <h2>First <em>Light</em></h2>
    <p class="lede">Maine is known as one of the first places in the country to see the sunrise (to verify: Cadillac Mountain, part of the year). The brandmark is a G whose open mouth holds a rising sun. The crossbar is the horizon. The sun is also the red light on a camera that says it is recording.</p>
    <p>A new generation, just coming up. Stories, recorded as they happen.</p>
    <button class="replay" onclick="var s=document.querySelector('.anim-a .sun');s.style.animation='none';s.offsetHeight;s.style.animation=''">Replay</button>
  </div>
  <div style="display:grid;place-items:center">{{A_ANIM}}</div>
</div></section>

<section class="a-light"><div class="wrap">
  <p class="label">The brandmark</p>
  <div class="grid2">
    <div class="tile">{{A_CONS}}</div>
    <div>
      <h2>A letter, a horizon, a <em>record light</em>.</h2>
      <p>Built from a circle, one straight bar and one dot. No gradients and no fine detail, so it holds at 16 px and on a phone screen at arm's length.</p>
      <p>The G stays green or white. The sun is always Signal orange in color versions. Nothing else in the system uses a filled orange circle, so the dot always points back to the brand.</p>
      <div class="smalls">{{A_SMALLS}}</div>
    </div>
  </div>
  <div class="hr"></div>
  <p class="label">Lockups</p>
  <div class="grid2">
    <div class="tile">{{A_H}}</div>
    <div class="tile dark">{{A_H_REV}}</div>
    <div class="tile">{{A_ST}}</div>
    <div class="tile pine" style="grid-template-columns:1fr 1fr;gap:24px"><div style="width:140px">{{A_ICON}}</div><div style="width:120px">{{A_SYM}}</div></div>
  </div>
  <div class="hr"></div>
  <div class="grid2" style="align-items:start">
    <div>
      <p class="label">Type</p>
      <h2 style="margin-bottom:6px">Instrument Sans</h2>
      <p>For names, headlines and everything functional. Set tight, semibold, sentence case.</p>
      <h2 style="margin:26px 0 6px"><em>Instrument Serif Italic</em></h2>
      <p>The second voice. One or two words at most: a place, a feeling, the word that matters. It is what makes a headline sound like a person.</p>
      <p style="font-size:13px;opacity:.7">Both under the SIL Open Font License.</p>
    </div>
    <div>
      <p class="label">Color</p>
      <div class="swatches">
        <div class="sw" style="background:{{A.spruce}};color:{{A.fog}}"><b>Spruce</b>{{A.spruce}}</div>
        <div class="sw" style="background:{{A.pine}};color:{{A.fog}}"><b>Pine</b>{{A.pine}}</div>
        <div class="sw" style="background:{{A.signal}};color:{{A.granite}}"><b>Signal</b>{{A.signal}}</div>
        <div class="sw" style="background:{{A.dawn}};color:{{A.granite}}"><b>Dawn</b>{{A.dawn}}</div>
        <div class="sw" style="background:{{A.fog}};color:{{A.granite}};box-shadow:inset 0 0 0 1px #d5dae2"><b>Fog</b>{{A.fog}}</div>
        <div class="sw" style="background:#fff;color:{{A.granite}};box-shadow:inset 0 0 0 1px #d5dae2"><b>Paper</b>#FFFFFF</div>
        <div class="sw" style="background:{{A.moss}};color:#fff"><b>Moss</b>{{A.moss}}</div>
        <div class="sw" style="background:{{A.granite}};color:{{A.fog}}"><b>Granite</b>{{A.granite}}</div>
      </div>
      <p style="font-size:13px;margin-top:12px;opacity:.75">Pine is new in v2: a near-black green for video backgrounds and dark sections. Signal stays a spark, about 3 percent of any layout.</p>
    </div>
  </div>
</div></section>

<section class="a-dark"><div class="wrap">
  <p class="label" style="color:{{A.dawn}}">Applications</p>
  <h2>The horizon rule</h2>
  <p>One thin line with the sun sitting on it. It divides sections, underlines titles and ends every video. Move the dot along the line to show progress through a series.</p>
  <div class="apps" style="margin-top:36px">
    {{A_AVATAR}}{{A_END}}{{A_THUMB}}{{A_LOWER}}{{A_OG}}
  </div>
  <div class="hr"></div>
  <p class="label" style="color:{{A.dawn}}">Website hero</p>
  <div class="web">
    <div class="bar"><i></i><i></i><i></i></div>
    <div class="nav"><div class="l">{{A_H_REV}}</div><div><span>About</span><span>Creators</span><span>Follow</span></div></div>
    <div class="body">
      <div>
        <span class="eb">An initiative of Maine Policy Institute</span>
        <h3>Young Mainers on building a life <em>here.</em></h3>
        <p style="opacity:.9;max-width:36ch">Short videos by young Maine creators about the rules that shape their lives.</p>
        <span class="btn">Meet the creators</span><span class="btn o">Follow along</span>
      </div>
      <div class="big">{{A_SYM_REV}}</div>
    </div>
    <div class="rule"></div>
    <div class="foot">Creators coming soon</div>
  </div>
</div></section>

<!-- ================= B2 ================= -->
<section class="b-hero"><div class="wrap grid2">
  <div>
    <p class="label">Direction B, v2</p>
    <h2>Postmark</h2>
    <p>Every story is sent from somewhere. The brandmark is a postmark with "ME" at its center: the postal code for Maine, and the first-person voice of every creator. Cancellation lines run off the edge like sound waves.</p>
    <p>It turns into a system on its own. Each creator gets a postmark with their town in the center.</p>
    <button class="replay" onclick="var g=document.querySelectorAll('.anim-b .stamp,.anim-b .lines path');g.forEach(function(e){e.style.animation='none';e.offsetHeight;e.style.animation=''})">Replay</button>
  </div>
  <div>{{B_ANIM}}</div>
</div></section>

<section class="b"><div class="wrap">
  <p class="label">The brandmark</p>
  <div class="grid2">
    <div class="btile">{{B_PM}}</div>
    <div>
      <h2>Posted from <span class="hl">Maine</span></h2>
      <p>Ring text in Anton: GENERATION MAINE across the top, YOUNG MAINERS across the bottom. A single ink color, like a real rubber stamp. At small sizes it drops the ring text and keeps the circle and ME.</p>
      <div class="smalls">{{B_SMALLS}}</div>
    </div>
  </div>
  <div class="hr"></div>
  <p class="label">Lockup and icon</p>
  <div class="grid2">
    <div class="btile">{{B_LOCK}}</div>
    <div class="btile blue"><div style="width:160px">{{B_ICON}}</div></div>
  </div>
  <div class="hr"></div>
  <p class="label">Creator postmarks</p>
  <h2>One stamp per <span class="hl">town</span></h2>
  <p>Town names are examples only. Each creator's postmark carries their hometown and the month they joined. It goes on their lower third, their profile card and their first video.</p>
  <div class="towns" style="margin-top:28px">{{B_TOWNS}}</div>
</div></section>

<section class="b-blue"><div class="wrap">
  <p class="label">Applications</p>
  <h2>Stamp, tape, type</h2>
  <p style="font-family:'IBM Plex Mono';font-size:15px">Three devices: the postmark, a strip of yellow label tape behind the key words, and perforated stamp edges around photos. Anton for headlines, IBM Plex Mono for everything else.</p>
  <div class="apps" style="margin-top:36px">
    {{B_AVATAR}}{{B_END}}{{B_THUMB}}{{B_LOWER}}{{B_OG}}
  </div>
</div></section>

<section class="intro"><div class="wrap">
  <p class="label">Recommendation</p>
  <h2>Lead with <em>First Light</em>.</h2>
  <p class="lede">It has the strongest single idea, it reads as polished next to a policy institute's name, and it stays calm enough to let the creators' faces lead. Postmark is the more playful option and has the best built-in system for featuring each creator. Its creator stamps could also live inside First Light as a campaign device.</p>
</div></section>

</body>
</html>
"""


if __name__ == "__main__":
    sa = build_a2()
    sb = build_b2()
    build_presentation(sa, sb)
    print("v2 built")
