"""The splash page: one page, the brand's lines as the motion system, the page background changing as you scroll.

Sections: nav with the compact lockup, the hero with the sixteen-line mural as the only lines, about,
the stories (creator-uploaded placeholders), in their words, the newsletter, follow, footer.

  python3 brand/src/build_splash.py   # writes brand/identity/splash/index.html and artifact.html
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import build_kit as K
import maine2
from build_v6 import C

LOGO = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")
TOWNS = ["Skowhegan", "Presque Isle", "Biddeford", "Machias", "Lewiston", "Rumford", "Belfast", "Fort Kent", "Sanford"]
TOPICS = ["Finding a place", "Starting a shop", "Who stays", "The commute", "Coming home", "Moving out", "Two jobs", "Doing the math", "Winter work"]
# where each story was filmed, kept for a later map. Town centers, degrees. [CONFIRM: towns once creators are cast]
TOWN_LL = {"Skowhegan": (44.765, -69.719), "Presque Isle": (46.681, -68.016), "Biddeford": (43.493, -70.453), "Machias": (44.715, -67.461), "Lewiston": (44.100, -70.215),
           "Rumford": (44.553, -70.551), "Belfast": (44.426, -69.006), "Fort Kent": (47.258, -68.590), "Sanford": (43.439, -70.774)}
# platform marks, drawn by hand at 24 units, one color, so they take the text color of wherever they sit
ICONS = {
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.3" fill="currentColor"/>',
    "tiktok": '<path d="M13.2 2h3.1c.2 2.4 1.7 4 4.2 4.3v3.1c-1.6 0-3-.5-4.2-1.3v6.6a6 6 0 1 1-6-6c.4 0 .7 0 1 .1v3.2a2.9 2.9 0 1 0 1.9 2.7V2z" fill="currentColor"/>',
    "youtube": '<path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2C2 8.8 2 12 2 12s0 3.2.4 4.8a2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8c.4-1.6.4-4.8.4-4.8s0-3.2-.4-4.8z" fill="currentColor"/><path d="M10 9v6l5-3z" fill="var(--icon-bg,#fff)"/>',
    "substack": '<rect x="4" y="3" width="16" height="2.4" fill="currentColor"/><rect x="4" y="8" width="16" height="2.4" fill="currentColor"/><path d="M4 13h16v8l-8-4.4L4 21z" fill="currentColor"/>',
}


def avatar():
    return ('<svg class="av" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="rgba(255,255,255,.22)"/>'
            '<circle cx="20" cy="15.5" r="6.5" fill="#FFFFFF"/><path d="M8.5 34a11.5 11.5 0 0 1 23 0" fill="#FFFFFF"/></svg>')


def icon(name):
    return '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS[name]


FIELDS = ["sp", "bi", "pi", "sp", "bi", "pi", "sp", "bi", "mg"]


def logo(name, cls=""):
    with open(os.path.join(LOGO, name + ".svg")) as fh:
        return fh.read().replace('role="img"', "").replace("<svg ", '<svg class="%s" ' % cls, 1)


def draw_paths(svg_text):
    """Give each stroked path a unit length and a stagger, so the mark can draw itself in like the hero mural."""
    n = [0]
    def one(m):
        i = n[0]; n[0] += 1
        return '<path pathLength="1" style="transition-delay:%dms" ' % (i * 40)
    return re.sub(r"<path ", one, svg_text)


def ping_dot(svg_text):
    """The dot on the i gets a ring behind it that pings like the hero period."""
    return re.sub(r"<circle ([^>]*)/>", lambda m: '<circle class="ping" %s/><circle class="dot" %s/>' % (m.group(1), m.group(1)), svg_text, count=1)


def mural_rows(h=720):
    """The hero mural is the logo's full cut at hero scale: sixteen lines, the two points kept, as row data for the draw-in."""
    w_box = h * maine2.ASPECT
    ring = maine2.fit((720 - w_box) / 2, 0, w_box, h)
    s = min(w_box / (maine2._MAXX - maine2._MINX), h / (maine2._MAXY - maine2._MINY))
    ox = (720 - w_box) / 2 + (w_box - (maine2._MAXX - maine2._MINX) * s) / 2
    oy = (h - (maine2._MAXY - maine2._MINY) * s) / 2
    minx, miny, maxx, maxy = maine2.bbox(ring)
    rows = []
    for i in range(16):
        t = i / 15
        y0 = miny + (maxy - miny) * (0.034 + 0.936 * t)
        w = h * (0.026 + 0.018 * t)
        xs = maine2.crossings(ring, y0)
        runs = []
        for a, b in zip(xs[0::2], xs[1::2]):
            if i == 0:
                c = (a + b) / 2
                runs.append([round(c - w * 0.6, 2), round(c + w * 0.6, 2)])   # the two points as equal short pills
            elif b - a >= w * 1.8:
                runs.append([round(a + w / 2, 1), round(b - w / 2, 1)])
        rows.append({"y": round(y0, 1), "w": round(w, 2), "runs": runs})
    towns = []
    for name, (lat, lon) in TOWN_LL.items():
        towns.append([name, round(ox + (lon * maine2._K - maine2._MINX) * s, 1), round(oy + (-lat - maine2._MINY) * s, 1)])
    return {"rows": rows, "towns": towns}


def dot(text, cls="", pulse=False):
    head, _, last = text.rpartition(" ")
    return '<span class="%s">%s<b class="nw">%s<i class="d%s"></i></b></span>' % (cls, (head + " ") if head else "", last, " pulse" if pulse else "")


CSS = r"""
/* Layout: one column. The page background changes color as sections enter, and every section pairs ink text with a light field.
   Light fields run from white into light green: white, a pale green, a deeper sage. The warm cream is gone from the page. */
:root{
  --sp:#104836;--pine:#0B2B21;--bi:#FFFFFF;--ink:#1E2621;--mg:#EFB443;--sage:#D3DDD4;--moss:#3D6F58;--stone:#5E6A63;--sand:#E6EEE8;--white:#FFFFFF;--snow:#F7F8F6;
  --bg:var(--bi);--fg:var(--ink);--muted:#4F5B55;--rule:rgba(30,38,33,.14);--card:#F6F9F6;
  --display:'Bricolage Grotesque',Arial,sans-serif;--body:'DM Sans',system-ui,Arial,sans-serif;
  --M:clamp(16px,4.5vw,64px);
}
/* One palette in every theme. The page commits to its own colors so text and background always pair. */
:root{color-scheme:light}
@font-face{font-family:'Bricolage Grotesque';font-weight:800;font-display:swap;src:url(data:font/woff2;base64,{{F800}}) format('woff2')}
@font-face{font-family:'DM Sans';font-weight:100 900;font-display:swap;src:url(data:font/ttf;base64,{{FDM}}) format('truetype')}
@font-face{font-family:Inter;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,{{FINTER}}) format('woff2')}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--fg);font:19px/1.55 var(--body);-webkit-font-smoothing:antialiased;transition:background .7s ease}
a{color:inherit}
.w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.03em;line-height:.92;margin:0;text-wrap:balance}
.d{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--mg);margin-left:.05em;vertical-align:baseline}
.nw{white-space:nowrap;font-weight:inherit}
.k{font:600 12px/1.2 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0}
/* buttons: pills, like the capsule and the round ends of the lines. Primary is Spruce on light fields and Snow on green;
   secondary is an outline in the current color. Marigold is never a button. */
.btn{display:inline-block;font:600 15px/1 var(--body);padding:16px 26px;border-radius:999px;text-decoration:none;border:1.5px solid transparent;transition:transform .25s cubic-bezier(.2,.7,.2,1),background .25s}
.btn:hover{transform:translateY(-2px)}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--mg);outline-offset:3px}
.b1{background:var(--snow);color:var(--sp)}.b1:hover{background:#FFFFFF}.b2{color:var(--snow);border-color:rgba(255,255,255,.55)}.b2:hover{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.8)}
.b3{background:var(--sp);color:var(--snow)}.b3:hover{background:var(--pine)}

/* nav: a transparent bar over the top of the hero. On the first scroll it folds into a floating frosted capsule with a reading line.
   The active section carries the dot. It hides on the way down past the hero and comes back on the way up. */
.top{position:fixed;top:0;left:0;right:0;z-index:20;padding-top:env(safe-area-inset-top,0px);color:var(--snow);transition:color .35s,transform .4s cubic-bezier(.2,.7,.2,1)}
.top.hide{transform:translateY(-120%)}
.top .w{position:relative;display:flex;align-items:center;justify-content:space-between;gap:24px;height:68px;max-width:1280px;margin:0 auto;padding-inline:var(--M);border-radius:0;background:rgba(255,255,255,0);
  transition:height .45s cubic-bezier(.2,.7,.2,1),max-width .55s cubic-bezier(.2,.7,.2,1),margin .45s cubic-bezier(.2,.7,.2,1),padding .45s cubic-bezier(.2,.7,.2,1),border-radius .45s cubic-bezier(.2,.7,.2,1),background .35s,box-shadow .45s}
.top .lk{height:24px;width:auto;display:block}
.top .lk.dark{display:none}
.top nav{display:flex;gap:30px;font:600 14px/1 var(--body);align-items:center}
.top nav a{position:relative;text-decoration:none;opacity:.88;padding:6px 0;border-radius:999px;transition:background .25s,padding .35s,opacity .25s}
.top nav a:hover{opacity:1}
.top nav a::before{content:"";position:absolute;left:-14px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:var(--mg);transform:scale(0);transition:transform .3s cubic-bezier(.3,1.4,.4,1)}
.top nav a.on{opacity:1}.top nav a.on::before{transform:scale(1)}
.top .cta{font:600 14px/1 var(--body);text-decoration:none;padding:12px 16px;border-radius:999px;border:1.5px solid rgba(255,255,255,.55);transition:background .25s,color .25s,border-color .25s,padding .35s}
.top .cta:hover{background:rgba(255,255,255,.1)}
.top.scrolled{color:var(--ink)}
.top.scrolled .w{height:52px;max-width:880px;margin:10px auto 0;padding-inline:10px;background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(18px) saturate(1.1);backdrop-filter:blur(18px) saturate(1.1);border-radius:999px;box-shadow:0 10px 30px rgba(11,43,33,.14);overflow:hidden;gap:16px}
.top.scrolled .w>a:first-child{padding-left:12px}
.top.scrolled .lk{height:20px}
.top.scrolled .lk.light{display:none}.top.scrolled .lk.dark{display:block}
.top.scrolled nav{gap:4px}
.top.scrolled nav a{padding:9px 12px;font-size:13px}
.top.scrolled nav a:hover{background:rgba(16,72,54,.08)}
.top.scrolled nav a.on{background:var(--sp);color:var(--snow)}
.top.scrolled nav a::before{display:none}
.top.scrolled .cta{padding:10px 14px;font-size:13px;background:var(--sp);color:var(--snow);border-color:var(--sp)}
.top.scrolled .menu{margin-right:0}
@media (max-width:900px){.top.scrolled .w{margin:10px 12px 0;height:48px}}
.prog{position:absolute;left:0;bottom:0;height:2px;background:var(--sp);width:0;transition:width .15s linear;opacity:0}
.top.scrolled .prog{opacity:1}
@media (prefers-reduced-motion: reduce){.top,.top .w,.top nav a,.top .cta{transition:none}}
.menu{display:none;position:relative;width:44px;height:44px;margin-right:-10px;background:none;border:0;color:inherit;padding:0;cursor:pointer}
.menu i{position:absolute;left:11px;width:22px;height:2px;border-radius:1px;background:currentColor;transition:transform .4s cubic-bezier(.2,.7,.2,1),opacity .25s}
.menu i:nth-child(1){top:15px}.menu i:nth-child(2){top:21px}.menu i:nth-child(3){top:27px}
.menu[aria-expanded="true"] i:nth-child(1){transform:translateY(6px) rotate(45deg)}.menu[aria-expanded="true"] i:nth-child(2){opacity:0;transform:scaleX(.2)}.menu[aria-expanded="true"] i:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.top.open{color:var(--snow);transform:none!important}
.top.open .w{background:rgba(255,255,255,0);box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none}
.top.open .lk.light{display:block}.top.open .lk.dark{display:none}.top.open .prog{opacity:0}
.sheet{position:fixed;inset:0;z-index:19;background:var(--sp);color:var(--snow);padding:calc(68px + env(safe-area-inset-top,0px)) var(--M) 32px;display:flex;flex-direction:column;opacity:0;visibility:hidden;transition:opacity .35s,visibility 0s .35s}
.sheet.open{opacity:1;visibility:visible;transition:opacity .35s}
.sheet nav{display:flex;flex-direction:column;gap:6px;margin-top:24px}
.sheet nav a{font:800 clamp(38px,11vw,56px)/1.05 var(--display);letter-spacing:-.03em;text-decoration:none;padding:8px 0;opacity:0;transform:translateY(14px);transition:opacity .45s,transform .55s cubic-bezier(.2,.7,.2,1)}
.sheet.open nav a{opacity:1;transform:none}
.sheet.open nav a:nth-child(2){transition-delay:.06s}.sheet.open nav a:nth-child(3){transition-delay:.12s}.sheet.open nav a:nth-child(4){transition-delay:.18s}
.sheet .foot{opacity:0;transition:opacity .4s .25s}.sheet.open .foot{opacity:1}
@media (prefers-reduced-motion: reduce){.sheet nav a,.sheet .foot{opacity:1;transform:none;transition:none}}
.sheet nav a .d{width:.18em;height:.18em}
.sheet .foot{margin-top:auto;display:flex;flex-direction:column;gap:14px}
.sheet .foot a{font:600 16px/1 var(--body);text-decoration:none}
.sheet .foot .cta{align-self:flex-start;background:var(--snow);color:var(--sp);padding:16px 26px;border-radius:999px;font:600 15px/1 var(--body);text-decoration:none}
@media (max-width:900px){.top nav,.top .cta{display:none}.menu{display:block}}
.hero{padding-top:68px}

/* hero */
.hero{position:relative;background:var(--sp);color:var(--snow);overflow:hidden}
.hero .w{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:32px;padding-block:80px 88px;min-height:620px;align-items:end}
.hero h1{font-size:clamp(46px,8.2vw,112px);max-width:11ch}
.hero .lede{font-size:clamp(19px,1.6vw,23px);line-height:1.5;max-width:38ch;margin:28px 0 30px;color:var(--snow);opacity:.92}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.mural{position:relative;justify-self:end;width:min(100%,480px);aspect-ratio:1;max-width:100%}
.mural svg{width:100%;height:100%;display:block}
/* the hero period pulses like a location marker: the dot holds still, a ring breathes out of it and fades */
.d.pulse{position:relative}
.d.pulse::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background:var(--mg);opacity:0;animation:pulse 2.4s cubic-bezier(.2,.6,.3,1) infinite 1.4s}
@keyframes pulse{0%{transform:scale(1);opacity:.6}65%{transform:scale(3);opacity:0}100%{transform:scale(3);opacity:0}}
@media (prefers-reduced-motion: reduce){.d.pulse::after{animation:none}}

.mural path{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1)}
.mural.on path{stroke-dashoffset:0}
@media (prefers-reduced-motion: reduce){.mural path{stroke-dashoffset:0;transition:none}}
@media (max-width:900px){.hero .w{grid-template-columns:1fr;min-height:0;padding-block:56px 64px}.mural{justify-self:start;width:min(64vw,340px);order:-1}}
.hero .rise{transition:transform .9s cubic-bezier(.2,.7,.2,1),opacity .9s}
.hero .rise.pre{opacity:0;transform:translateY(18px)}

/* on scroll: headings land their dot, rules draw from the left, rows rise. Visible at rest; script adds .pre then removes it */
.js .reveal.pre .d{transform:scale(0)}.reveal .d{transition:transform .5s cubic-bezier(.3,1.4,.4,1) .35s}
.js .reveal.pre .rule{transform:scaleX(0)}.rule{display:block;height:1.5px;background:var(--fg);transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.js .reveal.pre .row-in{transform:translateY(14px);opacity:.001}.row-in{transition:transform .7s cubic-bezier(.2,.7,.2,1),opacity .7s}
.reveal .row-in:nth-child(2){transition-delay:.08s}.reveal .row-in:nth-child(3){transition-delay:.16s}.reveal .row-in:nth-child(4){transition-delay:.24s}
@media (prefers-reduced-motion: reduce){.js .reveal.pre .d,.js .reveal.pre .rule,.js .reveal.pre .row-in{transform:none;opacity:1}}

/* sections sit on the page background, which the script changes as each one enters */
section{padding-block:clamp(56px,8vw,112px);scroll-margin-top:60px}
.h2{font-size:clamp(34px,4.6vw,60px)}
/* about starts on the green with white text. The page scrubs from green to white across the whole first scroll, from the top of the
   page until about has risen into the upper part of the screen (its top at 60% of the height), driven by scroll position so it tracks the hand and reverses the same way.
   The type does not crossfade through grey: it switches to ink in one quick step once the field is light enough. */
.about{color:var(--snow);transition:color .15s}.about.lit{color:var(--ink)}
body.scrub{transition:none}
.about .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px}
.about .cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;align-self:end}
.about .cols h3{font:600 15px/1.3 var(--body);letter-spacing:0;margin:0 0 8px;color:inherit}
.about .cols p{margin:0;color:rgba(255,255,255,.82);line-height:1.55;transition:color .15s}.about.lit .cols p{color:var(--muted)}
.about .cols div{padding-top:16px;position:relative}.about .cols div::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:#FFFFFF;transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1),background .15s}.about.lit .cols div::before{background:var(--fg)}
.js .reveal.pre .cols div::before,.js .reveal.pre blockquote::before{transform:scaleX(0)}
.about .cols div:nth-child(2)::before{transition-delay:.1s}.about .cols div:nth-child(3)::before{transition-delay:.2s}

/* the creators: the head, then a pinned stage. Scrolling steps through the nine; each one's details arrive from the right. */
.stories-head{padding-bottom:0}
.stories-head .lede{color:var(--muted);max-width:46ch;margin:18px 0 0}
.stories{padding:36px 0 clamp(80px,12vh,160px);height:calc(9 * 80vh + clamp(80px,12vh,160px));min-height:calc(9 * 520px);box-sizing:border-box}
/* the pinned block is its own height and sits a little below the capsule, so no empty screen opens up before it pins */
.stories .pinw{position:sticky;top:max(92px,calc(50vh - 330px))}
.stories .w{width:100%;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:28px clamp(28px,5vw,72px);align-items:center}
.stage{height:min(64vh,560px);display:flex;align-items:center}
.vid{position:relative;aspect-ratio:9/16;height:100%;max-height:620px;width:auto;max-width:100%;border-radius:14px;overflow:hidden;background:var(--pine);box-shadow:0 1px 0 var(--rule)}
.vid video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:0;transform:scale(1.04);transition:opacity .6s ease,transform 1.2s cubic-bezier(.2,.7,.2,1)}
.vid video.on{opacity:1;transform:none}
/* the social header on the clip: the creator's avatar and handle, as they appear on their own feed. Uploaded with the post in WordPress. */
.who{position:absolute;left:12px;top:12px;display:flex;align-items:center;gap:10px;z-index:2;color:#FFFFFF;opacity:0;transition:opacity .5s}.who.on{opacity:1}
.who .av{width:36px;height:36px;display:block;border-radius:50%}
.who span{display:flex;flex-direction:column;gap:3px;font:400 12px/1 var(--body);text-shadow:0 1px 2px rgba(11,43,33,.4)}.who span b{font-weight:600;font-size:13px}
.vid .dur{position:absolute;right:12px;top:12px;font:600 11px/1 var(--body);letter-spacing:.06em;color:#FFFFFF;background:rgba(11,43,33,.55);padding:6px 8px;border-radius:4px;z-index:2}
/* where you are among the nine: a counter, nine lines, and the town that arrives next */
.where{grid-column:1 / -1;display:flex;align-items:center;gap:20px;margin-top:8px;font:600 12px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.where .n{color:var(--fg);font-variant-numeric:tabular-nums;min-width:6ch}
.where .segs{display:flex;gap:6px;flex:1}
.where .segs button{flex:1;height:14px;padding:0;border:0;background:none;cursor:pointer;position:relative}
.where .segs button::before{content:"";position:absolute;left:0;right:0;top:6px;height:2px;border-radius:1px;background:var(--rule);transition:background .3s,transform .3s}
.where .segs button.on::before,.where .segs button.done::before{background:var(--fg)}
.where .segs button.done::before{opacity:.35}
.where .segs button:hover::before{transform:scaleY(1.5)}
.where .next{min-width:16ch;text-align:right;transition:opacity .4s}
.where .next.sw{opacity:0}
.panels{position:relative;height:min(64vh,560px)}
.panel{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;opacity:0;pointer-events:none;visibility:hidden;transition:visibility 0s .5s}
.panel.on{opacity:1;pointer-events:auto;visibility:visible;transition:none}
.panel>*{transition:transform .7s cubic-bezier(.2,.7,.2,1),opacity .5s;transform:translateX(44px);opacity:0}
.panel.on>*{transform:none;opacity:1}
.panel.prev>*{transform:translateX(-28px)}
.panel.on>:nth-child(3){transition-delay:.06s}.panel.on>:nth-child(4){transition-delay:.12s}.panel.on>:nth-child(5){transition-delay:.18s}.panel.on>:nth-child(6){transition-delay:.24s}
.panel .k{margin-bottom:14px;position:relative}.panel .k .d{width:.5em;height:.5em;margin-left:.3em;vertical-align:baseline}
.panel h2{font-size:clamp(38px,4.6vw,66px);max-width:10ch}
.panel .bio{font-size:19px;line-height:1.5;margin:22px 0 26px;max-width:42ch;color:var(--fg)}
.soc{display:flex;gap:22px;flex-wrap:wrap}.soc a{display:inline-flex;align-items:center;gap:8px;font:600 14px/1 var(--body);text-decoration:none;color:var(--fg)}.soc .ic{width:20px;height:20px;--icon-bg:#fff}.soc a:hover .ic{transform:translateY(-1px)}
.panel .pv{display:none}
@media (prefers-reduced-motion: reduce){.panel>*,.panel.prev>*{transform:none;transition:opacity .3s}}
@media (max-width:900px){
  .stories{height:auto;min-height:0;padding:0 0 clamp(40px,6vw,80px)}.stories .pinw{position:static}
  .stories .w{grid-template-columns:1fr}.stage{display:none}.panels{height:auto}.where{display:none}
  .panel{position:static;opacity:1;visibility:visible;pointer-events:auto;padding-block:36px;border-top:1.5px solid var(--rule)}.panel:first-child{border-top:0}.panel>*{transform:none;opacity:1}.panel .pv{display:block;aspect-ratio:9/16;width:min(62vw,270px);border-radius:12px;overflow:hidden;background:var(--pine);margin-bottom:22px}
  .panel .pv{position:relative}.panel .pv video{width:100%;height:100%;object-fit:cover;display:block}.panel .pv .who{opacity:1}
}


.news .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.news .lede{color:var(--muted);max-width:42ch;margin:18px 0 26px}
.form{display:flex;gap:10px;flex-wrap:wrap;max-width:520px}
.form input{flex:1 1 220px;min-width:0;font:16px var(--body);padding:15px 20px;border-radius:999px;border:1.5px solid var(--rule);background:var(--card);color:var(--fg)}
.form .note{flex-basis:100%;font-size:13px;color:var(--muted);margin:4px 0 0}
.form .ok{flex-basis:100%;font:600 15px var(--body);color:var(--fg);margin:4px 0 0}
.posts{display:grid;gap:0;position:relative}
.post{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.post h3{font-size:clamp(22px,2vw,28px);margin:0 0 8px}
.post p{margin:0;color:var(--muted);font-size:17px}
.post .by{font:600 13px/1.3 var(--body);color:var(--fg);margin-top:10px}.post .by span{font-weight:400;color:var(--muted)}
.post .dt{font:600 13px/1.3 var(--body);color:var(--muted);white-space:nowrap;padding-top:6px}
.form .ok{opacity:0;transition:opacity .4s}.form .ok.show{opacity:1}
@media (max-width:900px){.about .w,.news .w{grid-template-columns:1fr}.about .cols{grid-template-columns:1fr}}

/* the one Marigold section: what they say, in their words */
.words{color:var(--ink);background:var(--mg)}
.words .h2 .d{background:var(--ink)}
.words .qs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:40px}
@media (max-width:900px){.words .qs{grid-template-columns:1fr}}
.words blockquote{margin:0;padding-top:18px;position:relative}
.words blockquote::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:var(--ink);transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.words blockquote:nth-child(2)::before{transition-delay:.1s}.words blockquote:nth-child(3)::before{transition-delay:.2s}
.words blockquote p{font:800 clamp(22px,2.1vw,30px)/1.1 var(--display);letter-spacing:-.02em;margin:0 0 14px;text-wrap:balance}
.words blockquote footer{font:600 15px/1.3 var(--body)}.words blockquote footer span{font-weight:400}

.follow .row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media (max-width:760px){.follow .row{grid-template-columns:repeat(2,minmax(0,1fr))}}
.follow a{display:block;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.follow a b{display:block;font:600 15px/1.3 var(--body)}.follow a span{color:var(--muted);font-size:17px}
.follow .ic{display:block;width:28px;height:28px;margin-bottom:14px;color:var(--fg);--icon-bg:var(--sage);transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.follow a:hover .ic{transform:translateY(-2px)}
.follow .h2{margin-bottom:28px}

.site{background:var(--pine);color:var(--snow);padding-block:48px 40px}
.site .w{display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:end}
.site .lk{height:110px;width:auto;display:block}
.js .site .lk path{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .8s cubic-bezier(.2,.7,.2,1)}.js .site.on .lk path{stroke-dashoffset:0}
.site .lk .ping{transform-box:fill-box;transform-origin:center;opacity:0}.site.on .lk .ping{animation:pulse 2.4s cubic-bezier(.2,.6,.3,1) infinite 1.4s}
@media (prefers-reduced-motion: reduce){.js .site .lk path{stroke-dashoffset:0;transition:none}.site.on .lk .ping{animation:none}}
.site p{margin:0;font-size:14px;color:rgba(255,255,255,.8);max-width:60ch}
.site .fine{margin-top:12px;font-size:13px}
@media (max-width:640px){.site .w{grid-template-columns:1fr}.site .lk{height:90px}}
"""

CARDS = [
    ("t1", "Skowhegan", "Finding a place", "Three apartments in town. One I could afford. Here is what the lease said.", "0:52"),
    ("t2", "Presque Isle", "Starting a shop", "I wanted to sell coffee from a cart. It took eleven signatures.", "1:04"),
    ("t3", "Biddeford", "Who stays", "Half my graduating class left. I asked the ones who stayed why.", "0:47"),
    ("t4", "Machias", "The commute", "Forty minutes each way for a job that pays the rent. Barely.", "0:58"),
    ("t5", "Lewiston", "Coming home", "I moved back in with my parents at 26. Here is the math that made me.", "0:49"),
    ("t6", "Rumford", "Moving out", "My first lease. My first security deposit. My first surprise fee.", "0:55"),
    ("t1", "Belfast", "Two jobs", "One job pays for the room. The second one pays for everything else.", "1:01"),
    ("t2", "Fort Kent", "Doing the math", "What a nursing license costs before the first paycheck.", "0:44"),
    ("t3", "Sanford", "Winter work", "Landscaping stops in November. What I do until April.", "0:50"),
]


def page():
    rows = mural_rows()
    stagevids, panels, idx, whos = "", "", "", ""
    for i, (tone, town, topic, cap, dur) in enumerate(CARDS):
        stagevids += '<video data-i="%d" data-dur="%s" src="media/creator-%d.webm" muted loop playsinline preload="%s" aria-label="Placeholder clip, %s, %s, Maine"%s></video>' % (
            i, dur, i + 1, "auto" if i < 2 else "metadata", topic, town, ' class="on"' if i == 0 else "")
        who = '<div class="who%s">%s<span><b>@handle</b>[Creator name]</span></div>' % (' on' if i == 0 else '', avatar())
        whos += who
        idx += '<button type="button" aria-label="Creator %d, [Creator name], %s" data-name="[Creator name]"%s></button>' % (i + 1, town, ' class="on"' if i == 0 else "")
        socials = ''.join('<a href="#" aria-label="%s">%s<span>@handle</span></a>' % (n.capitalize(), icon(n)) for n in ("instagram", "tiktok", "youtube"))
        panels += ('<article class="panel%s" id="story-%d" data-i="%d"><div class="pv"><video src="media/creator-%d.webm" muted loop playsinline preload="metadata"></video>%s</div>'
                   '<p class="k">%s, Maine<i class="d pulse"></i></p><h2>%s</h2><p class="bio">[Two or three sentences in the creator\'s words: who they are, what they do, how long they have lived here.]</p>'
                   '<div class="soc">%s</div></article>') % (
                       " on" if i == 0 else "", i + 1, i, i + 1, who, town, "[Creator name]", socials)
    body = r"""
<header class="top" id="topbar"><div class="w"><a href="#top" aria-label="Generation Maine, home">%(lock)s%(lock_dark)s</a>
<nav aria-label="Page"><a href="#about" data-for="about">About</a><a href="#creators" data-for="creators">Creators</a><a href="#words" data-for="words">In their words</a><a href="#follow" data-for="follow">Follow</a></nav>
<a class="cta" href="#news">Get the newsletter</a><button class="menu" id="menu" aria-expanded="false" aria-controls="sheet" aria-label="Menu"><i></i><i></i><i></i></button><span class="prog" id="prog" aria-hidden="true"></span></div></header>
<div class="sheet" id="sheet" aria-hidden="true">
<nav aria-label="Page"><a href="#about">About<i class="d"></i></a><a href="#creators">Creators<i class="d"></i></a><a href="#words">In their words<i class="d"></i></a><a href="#follow">Follow<i class="d"></i></a></nav>
<div class="foot"><a class="cta" href="#news">Get the newsletter</a></div></div>

<section class="hero" id="top"><div class="w">
  <div class="h1"><h1 id="h1" class="rise">%(h1)s</h1>
  <p id="lede" class="lede rise">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay. Told from the towns they live in.</p>
  <p class="ctas rise" id="ctas"><a class="btn b1" href="#creators">Watch the stories</a><a class="btn b2" href="#news">Get the newsletter</a></p></div>
  <div class="mural" id="mural" aria-hidden="true"></div>
</div></section>

<section class="about reveal" id="about"><div class="w">
  <h2 class="h2">%(h2about)s</h2>
  <div class="cols">
    <div class="row-in"><h3>Who makes it</h3><p>Young Mainers with a phone and a story. They pick what to film and say it their own way.</p></div>
    <div class="row-in"><h3>What it is about</h3><p>The rules behind everyday costs. Leases, licenses, permits, wages, and the fine print nobody reads until it costs them.</p></div>
    <div class="row-in"><h3>Where to find it</h3><p>Short videos on TikTok, Instagram and YouTube. The full story, with the numbers, by email.</p></div>
  </div>
</div></section>

<section class="stories-head reveal" id="creators" data-bg="var(--bi)"><div class="w">
  <h2 class="h2">%(h2cre)s</h2><p class="lede">Nine young Mainers in nine towns. Each one films where they live and says it their own way. Names and faces arrive after the shoot.</p>
</div></section>
<section class="stories" id="stories" data-bg="var(--bi)"><div class="pinw"><div class="w">
  <div class="stage"><div class="vid" id="stage">%(stagevids)s%(whos)s<span class="dur" id="dur">0:52</span></div></div>
  <div class="panels" id="panels">%(panels)s</div>
  <div class="where" id="where"><span class="n" id="wn">01 / 09</span><span class="segs" id="segs">%(segs)s</span><span class="next" id="wnext"></span></div>
</div></div></section>
<section class="words reveal" id="words"><div class="w">
  <h2 class="h2">%(h2words)s</h2>
  <div class="qs">
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Belfast, Maine</span></footer></blockquote>
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Machias, Maine</span></footer></blockquote>
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Lewiston, Maine</span></footer></blockquote>
  </div>
</div></section>

<section class="news reveal" id="news" data-bg="var(--bi)"><div class="w">
  <div><h2 class="h2">%(h2news)s</h2><p class="lede">Each story in full, with the numbers behind it. Written by the creator who filmed it. Your address stays with us. [CONFIRM: privacy line]</p>
  <form class="form" id="signup" novalidate method="get" action="https://CONFIRM-publication.substack.com/subscribe" target="_blank" rel="noopener" data-confirm="[CONFIRM: publication address]"><label class="k" for="email" style="flex-basis:100%%">Email</label><input id="email" type="email" name="email" placeholder="you@example.com" autocomplete="email" required><button class="btn b3" type="submit">Subscribe</button>
  <p class="note">Runs on Substack. Unsubscribe in one click.</p><p class="ok" id="ok" hidden>Check your inbox. The confirmation is on its way.</p></form></div>
  <div class="posts"><span class="rule" aria-hidden="true"></span>
    <a class="post row-in" href="#"><div><h3>[Post title, plain words]</h3><p>[One line on what the creator found out.]</p><p class="by">[Creator name] <span>Belfast, Maine</span></p></div><span class="dt">[Date]</span></a>
    <a class="post row-in" href="#"><div><h3>[Post title, plain words]</h3><p>[One line on what the creator found out.]</p><p class="by">[Creator name] <span>Machias, Maine</span></p></div><span class="dt">[Date]</span></a>
    <a class="post row-in" href="#"><div><h3>[Post title, plain words]</h3><p>[One line on what the creator found out.]</p><p class="by">[Creator name] <span>Lewiston, Maine</span></p></div><span class="dt">[Date]</span></a>
  </div>
</div></section>

<section class="follow reveal" id="follow" data-bg="var(--sage)"><div class="w">
  <h2 class="h2">%(h2follow)s</h2>
  <span class="rule" aria-hidden="true"></span><div class="row">
    <a class="row-in" href="#">%(ic_ig)s<b>Instagram</b><span>[@handle]</span></a>
    <a class="row-in" href="#">%(ic_tt)s<b>TikTok</b><span>[@handle]</span></a>
    <a class="row-in" href="#">%(ic_yt)s<b>YouTube</b><span>[@handle]</span></a>
    <a class="row-in" href="#">%(ic_ss)s<b>Substack</b><span>[name].substack.com</span></a>
  </div>
</div></section>

<footer class="site"><div class="w">%(two)s<div><p>Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.</p><p class="fine">© 2026 Generation Maine. [CONFIRM: legal name, address and contact]</p></div></div></footer>

<script id="maine-data" type="application/json">%(json)s</script>
<script>
(() => {
  const MOSS = '#3D6F58', BI = '#F7F8F6';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const h1 = document.getElementById('h1'), lede = document.getElementById('lede'), ctas = document.getElementById('ctas');
  if (!reduced) { [h1, lede, ctas].forEach(el => el.classList.add('pre')); requestAnimationFrame(() => requestAnimationFrame(() => { h1.classList.remove('pre'); setTimeout(() => lede.classList.remove('pre'), 120); setTimeout(() => ctas.classList.remove('pre'), 240); })); }

  // The mural: the logo's sixteen lines at hero scale, drawing themselves in from the top.
  const d = JSON.parse(document.getElementById('maine-data').textContent), ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('viewBox', '0 0 720 720');
  d.rows.forEach((row, i) => row.runs.forEach(([a, b]) => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M' + a + ' ' + row.y + ' L' + b + ' ' + row.y); p.setAttribute('stroke', BI); p.setAttribute('stroke-width', row.w); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('fill', 'none'); p.setAttribute('pathLength', '1'); p.style.transitionDelay = (i * 45) + 'ms'; svg.appendChild(p); }));
  const m = document.getElementById('mural'); m.appendChild(svg);
  new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) m.classList.add('on'); }), { threshold: .2 }).observe(m);

  // The page background changes as each section passes the middle of the screen.
  // The page color is a function of scroll position, worked out every frame: green under the hero and about,
  // white once about reaches the top of the screen, with about's own text turning to ink, then whatever the section at the middle asks for.
  const aboutEl = document.getElementById('about'), bgs = [...document.querySelectorAll('[data-bg]')];
  let bgNow = '';
  const canMix = CSS.supports('color', 'color-mix(in oklab, red, blue)');
  function paint() {
    const top = aboutEl.getBoundingClientRect().top, start = top + scrollY, end = innerHeight * .6, t = Math.min(1, Math.max(0, (start - top) / (start - end)));
    aboutEl.classList.toggle('lit', t >= .4);
    let c; if (t <= 0) c = 'var(--sp)'; else if (t < 1) c = canMix ? 'color-mix(in oklab, var(--sp), var(--bi) ' + (t * 100).toFixed(1) + '%%)' : (t < .4 ? 'var(--sp)' : 'var(--bi)'); else { c = 'var(--bi)'; const mid = innerHeight / 2; for (const el of bgs) { if (el.getBoundingClientRect().top <= mid) c = el.dataset.bg; } }
    document.body.classList.toggle('scrub', t > 0 && aboutEl.getBoundingClientRect().bottom > 0);
    if (c !== bgNow) { bgNow = c; document.body.style.background = c; }
  }
  paint();

  // The stage: one pinned clip that changes as each story panel reaches the middle of the screen. Phones get a clip per panel.
  const stage = document.getElementById('stage'), stageVids = stage ? [...stage.querySelectorAll('video')] : [], whos = stage ? [...stage.querySelectorAll('.who')] : [], marks = [...document.querySelectorAll('#segs button')], dur = document.getElementById('dur'), wn = document.getElementById('wn'), wnext = document.getElementById('wnext');
  const panelVids = [...document.querySelectorAll('.panel .pv video')];
  const wide = () => matchMedia('(min-width: 901px)').matches;
  const panels = [...document.querySelectorAll('.panel')], storiesEl = document.getElementById('stories'); let cur = -1;
  function show(i) { if (i === cur) return; const back = i < cur; panels.forEach((p, k) => { p.classList.toggle('on', k === i); p.classList.toggle('prev', back ? k > i : k < i); }); cur = i;
    stageVids.forEach((v, k) => { const on = k === i; v.classList.toggle('on', on); if (on) { v.play().catch(() => {}); } else v.pause(); }); whos.forEach((w, k) => w.classList.toggle('on', k === i)); marks.forEach((m, k) => { m.classList.toggle('on', k === i); m.classList.toggle('done', k < i); }); if (dur && stageVids[i]) dur.textContent = stageVids[i].dataset.dur;
    wn.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(panels.length).padStart(2, '0'); const nx = marks[i + 1]; wnext.textContent = nx ? 'Next: ' + nx.dataset.name : 'Last one'; }
  // Scroll position steps through the creators while the stage is pinned.
  const step = () => { if (!wide()) return; const total = storiesEl.offsetHeight - innerHeight; const t = Math.min(1, Math.max(0, (scrollY - storiesEl.offsetTop) / total)); show(Math.min(panels.length - 1, Math.floor(t * panels.length))); };
  marks.forEach((m, k) => m.addEventListener('click', () => { const total = storiesEl.offsetHeight - innerHeight; scrollTo({ top: storiesEl.offsetTop + (k + .5) / panels.length * total }); }));
  addEventListener('scroll', step, { passive: true }); addEventListener('resize', () => { step(); paint(); }); step(); if (cur < 0) show(0);
  if (reduced) { stageVids.forEach(v => { v.controls = true; }); panelVids.forEach(v => { v.controls = true; }); }
  else { const mo = new IntersectionObserver(es => es.forEach(e => { if (!wide()) { if (e.isIntersecting) e.target.play().catch(() => {}); else e.target.pause(); } }), { threshold: .4 }); panelVids.forEach(v => mo.observe(v)); }

  // The bar turns solid once the hero scrolls away, marks the section in view, and opens the phone menu.
  const bar = document.getElementById('topbar'), heroEl = document.querySelector('.hero');
  const prog = document.getElementById('prog');
  let lastY = scrollY, ticking = false;
  addEventListener('scroll', () => { if (ticking) return; ticking = true; requestAnimationFrame(() => { const y = scrollY, dy = y - lastY; bar.classList.toggle('scrolled', y > 12); paint(); if (y > heroEl.offsetHeight && dy > 6) bar.classList.add('hide'); else if (dy < -6 || y <= heroEl.offsetHeight) bar.classList.remove('hide'); lastY = y; const max = document.documentElement.scrollHeight - innerHeight; if (prog) prog.style.width = (Math.min(1, y / max) * 100).toFixed(1) + '%%'; ticking = false; }); }, { passive: true });
  const links = [...bar.querySelectorAll('nav a')];
  const ao = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(l => l.classList.toggle('on', l.dataset.for === e.target.id)); }), { rootMargin: '-40%% 0px -55%% 0px', threshold: 0 });
  ['about', 'creators', 'words', 'follow'].forEach(id => { const el = document.getElementById(id); if (el) ao.observe(el); });
  const sheet = document.getElementById('sheet'), menu = document.getElementById('menu');
  const setMenu = o => { sheet.classList.toggle('open', o); bar.classList.toggle('open', o); sheet.setAttribute('aria-hidden', String(!o)); menu.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; };
  menu.addEventListener('click', () => setMenu(!sheet.classList.contains('open')));
  sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

  // Sections: mark them before they enter, release them as they do.
  document.documentElement.classList.add('js');
  const secs = [...document.querySelectorAll('.reveal')]; secs.forEach(sc => sc.classList.add('pre'));
  const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.remove('pre'); so.unobserve(e.target); } }), { threshold: .18 });
  secs.forEach(sc => so.observe(sc));
  const site = document.querySelector('.site'); new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) site.classList.add('on'); }), { threshold: .3 }).observe(site);

  // The signup form hands off to Substack: the address rides in the query string to the publication's subscribe page, which opens
  // in a new tab and sends the confirmation email. The page shows its own line. Until the publication exists, the hand-off is held.
  const f = document.getElementById('signup'), em = document.getElementById('email'), ok = document.getElementById('ok');
  f.addEventListener('submit', ev => { if (!em.checkValidity()) { ev.preventDefault(); em.focus(); em.setAttribute('aria-invalid', 'true'); return; } em.removeAttribute('aria-invalid');
    if (f.action.includes('CONFIRM')) ev.preventDefault();
    ok.hidden = false; requestAnimationFrame(() => ok.classList.add('show')); f.querySelector('button').disabled = true; });
})();
</script>
""" % dict(
        lock=logo("lockup-compact-reversed", "lk light"), lock_dark=logo("lockup-compact", "lk dark"), two=ping_dot(draw_paths(logo("lockup-two-line-reversed", "lk"))),
        h1=dot("Young Mainers on building a life here", pulse=True), h2about=dot("Made by the people it is about"), h2cre=dot("The creators"),
        h2words=dot("In their words"), h2news=dot("The full story, by email"), h2follow=dot("Follow along"),
        ic_ig=icon("instagram"), ic_tt=icon("tiktok"), ic_yt=icon("youtube"), ic_ss=icon("substack"),
        stagevids=stagevids, whos=whos, panels=panels, segs=idx, json=json.dumps(rows, separators=(",", ":")))
    css = CSS.replace("{{F800}}", K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2")).replace("{{FINTER}}", K.font64("generation-maine/assets/fonts/inter-var.woff2")).replace("{{FDM}}", K.font64("generation-maine/assets/fonts/dm-sans-var.ttf"))
    head = '<title>Generation Maine</title>\n<meta name="description" content="Young Mainers film the rules that shape their lives. Short videos and a newsletter, made in Maine.">\n<style>%s</style>' % css
    artifact = head + body
    standalone = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">%s</head><body>%s</body></html>' % (head, body)
    write("brand/identity/splash/index.html", standalone)
    write("brand/identity/splash/artifact.html", artifact)


if __name__ == "__main__":
    page()
    print("splash written")
