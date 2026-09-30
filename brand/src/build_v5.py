"""Identity v5: "On the Record".

The record dot (the live light on a camera) is the brand's one shape. News cues (chyrons,
datelines, heavy and thin rules) give it credibility. Big type and color blocks carry the
website until photography exists. Spruce, Paper and Amber. No italics, no swirls.

Two passes, because the presentation embeds screenshots of the website mock:
  python3 brand/src/build_v5.py            # logo, social, website mock
  node brand/src/render_v5.mjs             # PNGs and website screenshots
  python3 brand/src/build_v5.py present    # presentation with screenshots embedded
"""
import base64
import os
import sys

from gmlib import ROOT, write
from build_v4 import P, wordmark_one_line, wordmark_stacked, g_icon, placed, rect, text, svg, f, HANDLES
from build_brand import DISPLAY, TRACK

OUT = "brand/v5"
C = P  # spruce #0B4A34, pine #07261C, amber #FFB81C, paper #F2F4F7, ink #121417, moss #34795A


def dot(x, y, r, fill=None):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), f(r), fill or C["amber"])


# ------------------------------------------------------------------ logo files
def build_logo():
    s = {}
    for suf, fg in (("", C["spruce"]), ("-reversed", C["paper"]), ("-black", "#000"), ("-white", "#fff")):
        mk = C["amber"] if suf in ("", "-reversed") else fg
        b, w, h = wordmark_one_line(fg, mk, "circle")
        s["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        b, w, h = wordmark_stacked(fg, mk, "circle")
        s["stacked" + suf] = svg(w, h, b, "Generation Maine")
    s["icon"] = svg(200, 200, g_icon(0, 0, 200, C["spruce"], C["paper"], C["amber"], "circle", 0), "Generation Maine")
    s["icon-amber"] = svg(200, 200, g_icon(0, 0, 200, C["amber"], C["ink"], C["spruce"], "circle", 0), "Generation Maine")
    # The live pill: the dot plus a label. Used in the header, on thumbnails and at the start of videos.
    pill = rect(0, 0, 290, 56, C["ink"], 28) + dot(30, 28, 10) + text(52, 36, "ON THE RECORD", 20, C["paper"], weight=700, ls=0.12)
    s["pill"] = svg(290, 56, pill, "On the record")
    for k, v in s.items():
        write("%s/logo/%s.svg" % (OUT, k), v)
    return s


# ------------------------------------------------------------------ social
def chyron(x, y, name, town, w=1100):
    b = rect(x, y, w, 96, C["paper"]) + rect(x, y, 16, 96, C["amber"])
    b += text(x + 44, y + 64, name, 54, C["ink"], "Bric", 800, ls=-0.005)
    b += rect(x, y + 96, w, 52, C["spruce"])
    b += dot(x + 44, y + 122, 9)
    b += text(x + 66, y + 132, town, 26, C["paper"], weight=700, ls=0.1)
    b += text(x + w - 24, y + 132, "GENERATION MAINE", 26, C["amber"], weight=700, anchor="end", ls=0.1)
    return b


def build_social():
    s = {}
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, C["spruce"]) + g_icon(170, 170, 740, None, C["paper"], C["amber"]), "Avatar")
    e = rect(0, 0, 1080, 1920, C["spruce"])
    e += rect(0, 0, 1080, 14, C["amber"])
    e += rect(80, 150, 330, 64, C["ink"], 32) + dot(116, 182, 12) + text(142, 192, "ON THE RECORD", 24, C["paper"], weight=700, ls=0.12)
    wm, w, h = wordmark_stacked(C["paper"], C["amber"], "circle")
    e += placed(wm, 80, 420, 920 / w)
    e += rect(80, 900, 920, 6, C["paper"]) + rect(80, 916, 920, 2, C["paper"])
    e += text(80, 1040, "Follow along", 96, C["amber"], "Bric", 800, ls=-0.01)
    y = 1170
    for lab, hd in HANDLES:
        e += dot(96, y - 13, 11)
        e += text(126, y, lab, 40, C["paper"], weight=700)
        e += text(420, y, hd, 40, C["paper"], weight=400)
        e += rect(80, y + 30, 920, 1, C["moss"])
        y += 92
    e += text(80, 1700, "An initiative of Maine Policy Institute", 34, C["paper"], weight=600)
    s["endcard"] = svg(1080, 1920, e, "End card")
    s["lowerthird"] = svg(1920, 1080, chyron(96, 800, "[Creator name]", "[HOMETOWN], MAINE"), "Chyron lower third")
    o = rect(0, 0, 1200, 630, C["spruce"]) + rect(0, 0, 1200, 10, C["amber"])
    wm, w, h = wordmark_one_line(C["paper"], C["amber"], "circle")
    o += placed(wm, 80, 170, 820 / w)
    o += text(82, 360, "Young Mainers on building a life here", 44, C["paper"], "Bric", 800, ls=-0.01) + dot(862, 353, 7)
    o += rect(80, 470, 1040, 3, C["moss"])
    o += text(82, 540, "An initiative of Maine Policy Institute", 26, C["paper"], weight=600)
    s["og"] = svg(1200, 630, o, "Share card")
    for k, v in s.items():
        write("%s/social/%s.svg" % (OUT, k), v)
    return s


# ------------------------------------------------------------------ website mock (responsive HTML)
def font64(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def inline(svg_text, cls):
    return svg_text.replace("<svg ", '<svg class="%s" ' % cls, 1)


def build_site(logo):
    html = SITE
    rep = {
        "{{F_BRIC}}": font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
        "{{F_INTER}}": font64("generation-maine/assets/fonts/inter-var.woff2"),
        "{{WM_REV}}": inline(logo["wordmark-reversed"], "wm"),
        "{{WM_FOOT}}": inline(logo["stacked-reversed"], "wm-foot"),
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    for k, v in C.items():
        html = html.replace("{{%s}}" % k, v)
    write(OUT + "/site/index.html", html)


SITE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine | Young Mainers on building a life here</title>
<style>
@font-face{font-family:Bric;src:url(data:font/woff2;base64,{{F_BRIC}}) format("woff2");font-weight:800;font-display:swap}
@font-face{font-family:Inter;src:url(data:font/woff2;base64,{{F_INTER}}) format("woff2");font-weight:400 700;font-display:swap}
:root{--sp:{{spruce}};--pine:{{pine}};--am:{{amber}};--pa:{{paper}};--ink:{{ink}};--moss:{{moss}};--g:clamp(20px,5vw,72px)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:17px/1.6 Inter,system-ui,sans-serif;color:var(--ink);background:var(--pa);-webkit-font-smoothing:antialiased}
a{color:inherit}
.w{max-width:1280px;margin:0 auto;padding:0 var(--g)}
.dot{display:inline-block;width:.5em;height:.5em;border-radius:50%;background:var(--am);vertical-align:.08em;flex:none}
.pulse{animation:pulse 1.8s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.pulse{animation:none}}
.label{display:flex;align-items:center;gap:10px;font:700 13px/1.3 Inter;letter-spacing:.14em;text-transform:uppercase}
.label .n{opacity:.6}
.rule{height:6px;background:currentColor}
.rule+.thin{height:1px;background:currentColor;margin-top:6px}
h1,h2,h3{font-family:Bric;font-weight:800;letter-spacing:-.02em;margin:0}

/* header */
header{position:sticky;top:0;z-index:10;background:var(--sp);color:var(--pa)}
header .w{display:flex;align-items:center;justify-content:space-between;height:72px;gap:18px}
header .wm{height:24px;width:auto;display:block}
nav{display:flex;align-items:center;gap:28px;font-weight:600;font-size:15px}
nav a{text-decoration:none}
nav a:hover{text-decoration:underline;text-decoration-color:var(--am);text-decoration-thickness:3px;text-underline-offset:6px}
.pill{display:inline-flex;align-items:center;gap:9px;background:var(--ink);color:var(--pa);border-radius:99px;padding:9px 16px;font:700 12px/1 Inter;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
@media (max-width:640px){nav .hide{display:none}nav{gap:18px}header .wm{height:18px}}

/* hero */
.hero{background:var(--sp);color:var(--pa);padding:clamp(56px,9vw,120px) 0 0}
.hero .label{color:var(--am)}
.hero h1{font-size:clamp(52px,9.4vw,140px);line-height:.92;margin:26px 0 30px;max-width:11ch}
.hero h1 .dot{width:.2em;height:.2em;vertical-align:baseline;margin-left:.03em}
.hero p{font-size:clamp(18px,1.7vw,22px);max-width:40ch;margin:0 0 34px}
.hero p.label{max-width:none;font-size:13px;margin:0}
.hgrid{display:grid;grid-template-columns:1fr 330px;gap:56px;align-items:end}
@media (max-width:980px){.hgrid{grid-template-columns:1fr}}
.frame{aspect-ratio:9/16;background:var(--ink);border-radius:26px;padding:16px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 0 0 8px var(--pine)}
.frame .pill{align-self:flex-start;background:rgba(255,255,255,.1)}
.frame .num{font:800 150px/1 Bric;letter-spacing:-.04em;color:var(--pa);opacity:.12;padding-left:6px}
.frame .chy{border-left:8px solid var(--am);background:var(--pa);color:var(--ink)}
.frame .chy b{display:block;font:800 22px/1.1 Bric;padding:11px 12px 7px}
.frame .chy span{display:flex;gap:8px;align-items:center;background:var(--sp);color:var(--pa);font:700 11px/1 Inter;letter-spacing:.12em;text-transform:uppercase;padding:9px 12px}
.frame .bar{height:4px;background:rgba(255,255,255,.18);border-radius:2px;margin-top:14px}
.frame .bar i{display:block;width:38%;height:100%;background:var(--am);border-radius:2px}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;gap:10px;border-radius:99px;padding:16px 26px;font-weight:700;text-decoration:none;font-size:17px}
.btn.am{background:var(--am);color:var(--ink)}
.btn.ol{box-shadow:inset 0 0 0 2px var(--pa);color:var(--pa)}
.hero .meta{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-top:clamp(48px,7vw,96px);padding-bottom:22px;flex-wrap:wrap}
.dateline{font:700 13px/1.4 Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.85}
.ticker{background:var(--am);color:var(--ink);font:700 14px/1 Inter;letter-spacing:.12em;text-transform:uppercase;overflow:hidden;white-space:nowrap}
.ticker .w{display:flex;gap:26px;align-items:center;height:52px}
.ticker .dot{background:var(--ink)}

/* sections */
section{padding:clamp(64px,9vw,128px) 0}
.sec-head{display:grid;grid-template-columns:1fr;gap:18px;margin-bottom:clamp(32px,4vw,56px)}
.sec-head h2{font-size:clamp(40px,6vw,88px);line-height:.95;max-width:14ch}
.two{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(32px,6vw,96px)}
@media (max-width:860px){.two{grid-template-columns:1fr}}
.lead{font-size:clamp(19px,1.7vw,23px);line-height:1.5;margin:0 0 18px}
.topics{list-style:none;margin:0;padding:0;border-top:6px solid var(--sp)}
.topics li{display:flex;align-items:baseline;gap:18px;padding:18px 0;border-bottom:1px solid #C9D3CF;font:800 clamp(22px,2.4vw,32px)/1.1 Bric;letter-spacing:-.01em;color:var(--sp)}
.topics li span{font:700 13px/1 Inter;letter-spacing:.12em;color:var(--moss);min-width:28px}

/* creators */
.creators{background:#fff}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
@media (max-width:980px){.grid{grid-template-columns:repeat(2,1fr);gap:14px}}

.card{background:var(--sp);color:var(--pa);border-radius:4px;aspect-ratio:4/5;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;position:relative}
.card .top{padding:18px;display:flex;justify-content:space-between;align-items:center}
.card .ph{font:700 11px/1 Inter;letter-spacing:.14em;text-transform:uppercase;background:var(--am);color:var(--ink);padding:6px 9px;border-radius:99px}
.card .big{font:800 clamp(64px,7vw,104px)/1 Bric;letter-spacing:-.03em;padding:0 18px;opacity:.16}
.card .chy{background:var(--pa);color:var(--ink);border-left:8px solid var(--am)}
.card .chy b{display:block;font:800 22px/1.1 Bric;padding:12px 14px 8px}
.card .chy span{display:flex;align-items:center;gap:8px;background:var(--pine);color:var(--pa);font:700 11px/1 Inter;letter-spacing:.12em;text-transform:uppercase;padding:9px 14px}
.note{margin-top:22px;font-size:14px;color:#56605C}

/* follow */
.follow{background:var(--am);color:var(--ink)}
.follow h2{font-size:clamp(56px,11vw,168px);line-height:.9;margin:18px 0 40px}
.chan{list-style:none;padding:0;margin:0;border-top:6px solid var(--ink)}
.chan a{display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:1px solid rgba(18,20,23,.35);text-decoration:none;font:800 clamp(26px,3.4vw,44px)/1 Bric;letter-spacing:-.01em}
.chan a small{font:600 15px/1 Inter;letter-spacing:.02em;opacity:.75}
.chan a:hover{background:rgba(18,20,23,.06)}
.sub{background:var(--ink);color:var(--pa);border-radius:4px;padding:clamp(24px,3vw,40px);margin-top:40px;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.sub h3{font-size:clamp(28px,3vw,40px)}
.sub p{margin:6px 0 0;opacity:.85}
.sub .btn{background:var(--am);color:var(--ink)}

/* mpi */
.mpi .rule{color:var(--sp)}
.mpi h2{font-size:clamp(34px,4.6vw,60px);line-height:1;margin-top:18px}
.conf{background:#E4E9E6;padding:2px 6px;border-radius:3px;font-size:.92em}
.btn.dk{box-shadow:inset 0 0 0 2px var(--sp);color:var(--sp);margin-top:10px}

/* footer */
footer{background:var(--pine);color:var(--pa);padding:56px 0 40px}
footer .wm-foot{width:min(360px,70vw);height:auto;display:block}
footer .row{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
footer .rule{color:var(--pa);margin-top:36px}
@media (max-width:640px){footer .row>div{text-align:left!important}footer .row .label{justify-content:flex-start!important}}
footer small{display:block;margin-top:18px;opacity:.75;font-size:13px}
@media (max-width:980px){.frame{display:none}}
@media (max-width:560px){.card .top{padding:10px}.card .ph{font-size:9px;padding:5px 7px}.card{aspect-ratio:3/4}.card .big{font-size:56px;padding:0 10px}.card .chy{border-left-width:5px}.card .chy b{font-size:16px;padding:9px 9px 6px}.card .chy span{font-size:9px;padding:7px 9px;gap:6px}}
</style></head>
<body>
<header><div class="w">
  <a href="#" aria-label="Generation Maine home">{{WM_REV}}</a>
  <nav aria-label="Sections"><a href="#about" class="hide">About</a><a href="#creators">Creators</a><a href="#follow">Follow</a>
    <span class="pill hide"><span class="dot pulse" aria-hidden="true"></span>On the record</span></nav>
</div></header>

<main>
<section class="hero" aria-labelledby="h1" style="padding-bottom:0"><div class="w">
  <div class="hgrid"><div>
  <p class="label"><span class="dot" aria-hidden="true"></span>An initiative of Maine Policy Institute</p>
  <h1 id="h1">Young Mainers on building a life here<span class="dot" aria-hidden="true"></span></h1>
  <p>Short videos by young Maine creators about the rules that shape their lives.</p>
  <div class="btns"><a class="btn am" href="#creators">Meet the creators</a><a class="btn ol" href="#follow">Follow along</a></div>
  </div>
  <div class="frame" aria-hidden="true"><span class="pill"><span class="dot pulse"></span>Episode 01</span><div class="num">01</div>
    <div><div class="chy"><b>[Creator name]</b><span><i class="dot" style="width:8px;height:8px"></i>[Hometown], Maine</span></div><div class="bar"><i></i></div></div></div>
  </div>
  <div class="meta"><span class="dateline">Maine · Stories from across the state</span><span class="pill"><span class="dot pulse" aria-hidden="true"></span>Recording soon</span></div>
</div>
<div class="ticker" aria-hidden="true"><div class="w"><span>Coming soon</span><span class="dot"></span><span>8 to 12 creators</span><span class="dot"></span><span>Housing</span><span class="dot"></span><span>Jobs</span><span class="dot"></span><span>Cost of living</span><span class="dot"></span><span>Staying in Maine</span></div></div>
</section>

<section id="about" aria-labelledby="h-about"><div class="w two">
  <div>
    <div class="sec-head"><p class="label"><span class="dot"></span><span class="n">01</span> What it is</p>
      <h2 id="h-about">A storytelling project made by young Mainers</h2></div>
    <p class="lead">Generation Maine is a group of 8 to 12 young content creators from across the state. Each one makes short videos about their own life in Maine.</p>
    <p>The videos show how economic rules affect everyday choices. Some are about finding a place to live. Others are about getting a job, starting a business or deciding whether to stay.</p>
    <p>The creators tell their own stories. You can watch them on social media and read more on our Substack.</p>
  </div>
  <div><p class="label" style="margin-bottom:18px;color:var(--moss)">What the videos cover</p>
    <ul class="topics"><li><span>01</span>Housing</li><li><span>02</span>Jobs</li><li><span>03</span>Cost of living</li><li><span>04</span>Starting a business</li><li><span>05</span>Staying in Maine</li></ul></div>
</div></section>

<section id="creators" class="creators" aria-labelledby="h-cr"><div class="w">
  <div class="sec-head"><p class="label"><span class="dot"></span><span class="n">02</span> The creators</p>
    <h2 id="h-cr">Meet the creators</h2></div>
  <div class="grid">
    <article class="card"><div class="top"><span class="ph">Placeholder</span><span class="dot"></span></div><div class="big">01</div><div class="chy"><b>[Creator name]</b><span><i class="dot" style="width:8px;height:8px"></i>[Hometown], Maine</span></div></article>
    <article class="card"><div class="top"><span class="ph">Placeholder</span><span class="dot"></span></div><div class="big">02</div><div class="chy"><b>[Creator name]</b><span><i class="dot" style="width:8px;height:8px"></i>[Hometown], Maine</span></div></article>
    <article class="card"><div class="top"><span class="ph">Placeholder</span><span class="dot"></span></div><div class="big">03</div><div class="chy"><b>[Creator name]</b><span><i class="dot" style="width:8px;height:8px"></i>[Hometown], Maine</span></div></article>
    <article class="card"><div class="top"><span class="ph">Placeholder</span><span class="dot"></span></div><div class="big">04</div><div class="chy"><b>[Creator name]</b><span><i class="dot" style="width:8px;height:8px"></i>[Hometown], Maine</span></div></article>
  </div>
  <p class="note">Each card becomes the creator's portrait with the chyron over the bottom edge. Until photos arrive, the card holds its number.</p>
</div></section>

<section id="follow" class="follow" aria-labelledby="h-f"><div class="w">
  <p class="label"><span class="dot" style="background:var(--ink)"></span><span class="n">03</span> Follow</p>
  <h2 id="h-f">Follow along</h2>
  <ul class="chan">
    <li><a href="#follow">Instagram <small>[@handle]</small></a></li>
    <li><a href="#follow">TikTok <small>[@handle]</small></a></li>
    <li><a href="#follow">YouTube <small>[@handle]</small></a></li>
  </ul>
  <div class="sub"><div><h3>Read the Substack</h3><p>Get new stories from the creators by email.</p></div><a class="btn" href="#follow">Subscribe on Substack</a></div>
</div></section>

<section class="mpi" aria-labelledby="h-m"><div class="w two">
  <div><div class="rule"></div><div class="thin"></div>
    <p class="label" style="margin-top:22px"><span class="dot"></span><span class="n">04</span> Who is behind this</p>
    <h2 id="h-m">About Maine Policy Institute</h2></div>
  <div><p class="lead">Generation Maine is an initiative of Maine Policy Institute.</p>
    <p><span class="conf">[CONFIRM: one sentence about Maine Policy Institute]</span></p>
    <p>Press: <span class="conf">[CONFIRM: press email]</span></p>
    <a class="btn dk" href="https://mainepolicy.org/">Visit Maine Policy Institute</a></div>
</div></section>
</main>

<footer><div class="w">
  <div class="row">{{WM_FOOT}}<div style="text-align:right"><p class="label" style="justify-content:flex-end"><span class="dot"></span>An initiative of Maine Policy Institute</p></div></div>
  <div class="rule"></div><div class="thin"></div>
  <small>© 2026 Generation Maine. Stories by young Mainers.</small>
</div></footer>
</body></html>
"""


# ------------------------------------------------------------------ presentation
def b64png(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


def build_present(logo, social):
    html = PRESENT
    rep = {
        "{{F_BRIC}}": font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
        "{{F_INTER}}": font64("generation-maine/assets/fonts/inter-var.woff2"),
        "{{WM}}": logo["wordmark"], "{{WM_REV}}": logo["wordmark-reversed"], "{{ST}}": logo["stacked"],
        "{{ICON}}": logo["icon"], "{{ICON_AM}}": logo["icon-amber"], "{{PILL}}": logo["pill"],
        "{{AVATAR}}": social["avatar"], "{{END}}": social["endcard"], "{{LOWER}}": social["lowerthird"], "{{OG}}": social["og"],
        "{{DESK}}": b64png(OUT + "/site/desktop.png"), "{{MOB}}": b64png(OUT + "/site/mobile.png"),
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    for k, v in C.items():
        html = html.replace("{{%s}}" % k, v)
    write(OUT + "/on-the-record.html", html)


PRESENT = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine: On the Record</title>
<style>
@font-face{font-family:Bric;src:url(data:font/woff2;base64,{{F_BRIC}}) format("woff2");font-weight:800}
@font-face{font-family:Inter;src:url(data:font/woff2;base64,{{F_INTER}}) format("woff2");font-weight:400 700}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 Inter,system-ui,sans-serif;color:{{ink}};background:{{paper}}}
.w{max-width:1240px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}
section{padding:72px 0;border-bottom:1px solid #DCE1E6}
h1,h2,h3{font-family:Bric;font-weight:800;letter-spacing:-.02em;margin:0}
h1{font-size:clamp(46px,8vw,112px);line-height:.92}
h2{font-size:clamp(32px,4.4vw,58px);line-height:1;margin-bottom:16px}
h3{font-size:22px;margin-bottom:6px}
.dot{display:inline-block;width:.5em;height:.5em;border-radius:50%;background:{{amber}}}
.label{display:flex;align-items:center;gap:10px;font:700 12px/1 Inter;letter-spacing:.14em;text-transform:uppercase;margin:0 0 14px;opacity:.8}
.intro{background:{{spruce}};color:{{paper}}}
.intro .label{color:{{amber}};opacity:1}
.intro p{font-size:19px;max-width:62ch}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:36px}
@media(max-width:860px){.cols3{grid-template-columns:1fr}}
.cols3 div{border-top:6px solid {{amber}};padding-top:14px}
.panel{background:#fff;border-radius:14px;padding:26px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.panel.dk{background:{{spruce}}}
.panel svg{display:block;width:100%;height:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:860px){.g2,.g3{grid-template-columns:1fr}}
.sizes{display:flex;gap:20px;align-items:flex-end}
.sizes span svg{width:100%;height:auto;border-radius:18%}
.el{display:grid;grid-template-columns:260px 1fr;gap:28px;align-items:center;padding:24px 0;border-top:1px solid #DCE1E6}
@media(max-width:860px){.el{grid-template-columns:1fr}}
.el .demo{background:#fff;border-radius:12px;padding:20px;min-height:110px;display:grid;place-items:center}
.pulse{animation:p 1.8s ease-in-out infinite}@keyframes p{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.pulse{animation:none}}
.sw{border-radius:12px;padding:14px;min-height:130px;display:flex;flex-direction:column;justify-content:flex-end;font-size:13px}
.sw b{font-size:16px}
.ratio{display:flex;height:34px;border-radius:8px;overflow:hidden;margin-top:14px}
.dd{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px}
.do,.dont{background:#fff;border-radius:10px;padding:12px 14px;border-left:6px solid {{spruce}}}
.dont{border-left-color:#B3261E}
.do b,.dont b{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px}
.apps{display:grid;grid-template-columns:1fr .6fr 1.4fr;gap:20px;align-items:start}
@media(max-width:860px){.apps{grid-template-columns:1fr 1fr}.apps .wide{grid-column:1/-1}}
.apps figure{margin:0}.apps svg{width:100%;height:auto;display:block;border-radius:12px;box-shadow:0 12px 40px -20px rgba(0,0,0,.45)}
.apps .round svg{border-radius:50%}
.apps .lower svg{background:linear-gradient(135deg,#3b4a42,#6b7a70 55%,#2a3530)}
figcaption{font:700 11px/1 Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.site{display:grid;grid-template-columns:1fr 300px;gap:24px;align-items:start}
@media(max-width:860px){.site{grid-template-columns:1fr}}
.site img{width:100%;display:block;border-radius:10px;box-shadow:0 20px 60px -25px rgba(0,0,0,.5)}
.site .mob img{border-radius:22px}
</style></head><body>

<section class="intro"><div class="w">
  <p class="label"><span class="dot"></span>Generation Maine · Identity v5</p>
  <h1>On the Record</h1>
  <p style="margin-top:22px">The project is young Mainers telling their own stories on camera. The one symbol of that is the light that says a camera is recording. It becomes the brand's only shape. News cues make it credible to Maine Wire readers. Big type and color blocks carry the website until there are photos.</p>
  <div class="cols3">
    <div><h3>Why the dot</h3>It is neutral, native to phones and cannot be read as partisan. It is also the dot on the i you liked in Spruce &amp; Signal.</div>
    <div><h3>Why news cues</h3>Chyrons, datelines and heavy rules say "real people, real places". Older readers trust them; younger viewers see them in every news clip.</div>
    <div><h3>What was cut</h3>The swirls (decoration with no meaning), the ballot oval (reads as electoral) and the pink.</div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>01 The mark</p>
  <h2>A wordmark with a live light</h2>
  <p style="max-width:62ch">The heavy wordmark from Spruce &amp; Signal. The dot on the i in "Maine" is the record light, now in Amber. The G icon carries the same dot for avatars and favicons.</p>
  <div class="g2" style="margin-top:22px">
    <div class="panel">{{WM}}</div><div class="panel dk">{{WM_REV}}</div>
    <div class="panel">{{ST}}</div>
    <div class="panel"><div class="sizes"><span style="width:96px">{{ICON}}</span><span style="width:48px">{{ICON}}</span><span style="width:32px">{{ICON}}</span><span style="width:16px">{{ICON}}</span><span style="width:96px;margin-left:auto">{{ICON_AM}}</span></div></div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>02 The element system</p>
  <h2>One shape, three news cues, big type</h2>
  <div class="el"><div class="demo"><svg viewBox="0 0 60 60" width="60"><circle class="pulse" cx="30" cy="30" r="22" fill="{{amber}}"/></svg></div>
    <div><h3>The record dot</h3>The only shape in the system. Amber, always a perfect circle. It is the live indicator, the bullet, the period at the end of a headline and the section marker. It pulses slowly only when something is live or coming soon. One large dot per screen at most.</div></div>
  <div class="el"><div class="demo">{{PILL}}</div>
    <div><h3>The live pill</h3>Dot plus a short label in caps on Ink: ON THE RECORD, RECORDING SOON, NEW EPISODE. Header, thumbnails and the first second of every video.</div></div>
  <div class="el"><div class="demo" style="background:#56605C"><svg viewBox="0 0 560 150" width="100%"><rect width="560" height="96" fill="{{paper}}"/><rect width="10" height="96" fill="{{amber}}"/><text x="28" y="64" font-size="44" fill="{{ink}}" style="font-family:Bric;font-weight:800">[Creator name]</text><rect y="96" width="560" height="50" fill="{{spruce}}"/><circle cx="30" cy="121" r="8" fill="{{amber}}"/><text x="48" y="130" font-size="20" fill="{{paper}}" style="font-family:Inter;font-weight:700;letter-spacing:.1em">[HOMETOWN], MAINE</text></svg></div>
    <div><h3>The chyron</h3>Two bars, like a TV news lower third: the name in Bricolage on Paper with an Amber edge, the hometown in caps on Spruce. Every creator appearance uses it, on video and on the website.</div></div>
  <div class="el"><div class="demo"><div style="width:100%"><div style="font:700 13px/1.4 Inter;letter-spacing:.14em;text-transform:uppercase">Rumford, Maine</div><div style="height:6px;background:{{spruce}};margin-top:10px"></div><div style="height:1px;background:{{spruce}};margin-top:6px"></div></div></div>
    <div><h3>Datelines and rules</h3>Place is set as type, the way a newspaper opens a story: TOWN, MAINE in caps. A heavy rule over a thin rule opens major sections. This replaces the swirl texture: place is named, not decorated.</div></div>
  <div class="el"><div class="demo" style="background:{{spruce}};color:{{paper}};font:800 44px/0.95 Bric;letter-spacing:-.02em;text-align:left;place-items:start">Building a life here<span class="dot" style="width:.2em;height:.2em;margin-left:2px"></span></div>
    <div><h3>Big type and color blocks</h3>With no photos, scale does the work: headlines at 90 to 150 px on desktop, full-width blocks of Spruce, Paper and Amber, and numbered sections (01, 02, 03). This is what makes the page feel designed rather than empty.</div></div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>03 Color and type</p>
  <div class="g2">
    <div><div class="g3" style="grid-template-columns:repeat(3,1fr)">
      <div class="sw" style="background:{{spruce}};color:{{paper}}"><b>Spruce</b>{{spruce}}</div>
      <div class="sw" style="background:{{paper}};box-shadow:inset 0 0 0 1px #DCE1E6"><b>Paper</b>{{paper}}</div>
      <div class="sw" style="background:{{amber}}"><b>Amber</b>{{amber}}</div>
      <div class="sw" style="background:{{pine}};color:{{paper}}"><b>Pine</b>{{pine}}</div>
      <div class="sw" style="background:{{ink}};color:{{paper}}"><b>Ink</b>{{ink}}</div>
      <div class="sw" style="background:{{moss}};color:#fff"><b>Moss</b>{{moss}}</div></div>
      <div class="ratio"><span style="flex:45;background:{{spruce}}"></span><span style="flex:30;background:{{paper}};box-shadow:inset 0 0 0 1px #C9D0D6"></span><span style="flex:10;background:{{ink}}"></span><span style="flex:10;background:{{amber}}"></span><span style="flex:5;background:{{moss}}"></span></div>
      <p style="font-size:13px">Spruce 45 · Paper 30 · Ink 10 · Amber 10 · Moss 5. Amber on Spruce 5.9:1, Ink on Amber 10.7:1, Paper on Spruce 9.3:1. All pass WCAG AA.</p></div>
    <div><h3 style="font-size:40px">Bricolage Grotesque ExtraBold</h3><p>Headlines, names, the wordmark. Tight, sentence case, big.</p>
      <h3 style="font-family:Inter;font-weight:700;letter-spacing:0;font-size:26px">Inter</h3><p>Body text, labels, datelines and chyron bottoms. Caps with wide tracking for labels.</p>
      <p style="font-size:13px">Both under the SIL Open Font License. Both already self-hosted in the theme. No italics anywhere.</p></div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>04 Rules</p>
  <div class="dd">
    <div class="do"><b>Do</b>Use one large dot per screen, as a period or a live light.</div><div class="dont"><b>Don't</b>Scatter dots as decoration or make them any color but Amber.</div>
    <div class="do"><b>Do</b>Name places in datelines: BANGOR, MAINE.</div><div class="dont"><b>Don't</b>Add maps, outlines, mountains or swirl textures.</div>
    <div class="do"><b>Do</b>Use the chyron for every creator appearance.</div><div class="dont"><b>Don't</b>Use the pill to say VOTE or to point at any candidate or measure.</div>
    <div class="do"><b>Do</b>Let headlines run huge and let color blocks fill the width.</div><div class="dont"><b>Don't</b>Fill empty space with stock photos or patterns.</div>
    <div class="do"><b>Do</b>Keep "An initiative of Maine Policy Institute" on every piece.</div><div class="dont"><b>Don't</b>Use italics, gradients or drop shadows.</div>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>05 Social</p>
  <div class="apps">
    <figure class="round">{{AVATAR}}<figcaption>Avatar</figcaption></figure>
    <figure>{{END}}<figcaption>9:16 end card</figcaption></figure>
    <figure class="wide lower">{{LOWER}}<figcaption>Chyron lower third</figcaption></figure>
    <figure class="wide" style="grid-column:1/-1;max-width:640px">{{OG}}<figcaption>Share card</figcaption></figure>
  </div>
</div></section>

<section><div class="w">
  <p class="label"><span class="dot"></span>06 Website</p>
  <h2>Premium with no photos</h2>
  <p style="max-width:62ch">A working, responsive page built only from the system: type, color blocks, the dot, chyrons and rules. Open brand/v5/site/index.html in a browser to scroll it. When portraits arrive they drop into the creator cards under the chyron.</p>
  <div class="site" style="margin-top:22px"><div><img src="{{DESK}}" alt="Website mock, desktop"><figcaption>Desktop, 1440 px</figcaption></div>
    <div class="mob"><img src="{{MOB}}" alt="Website mock, mobile"><figcaption>Mobile, 390 px</figcaption></div></div>
</div></section>

</body></html>
"""

if __name__ == "__main__":
    logo = build_logo()
    social = build_social()
    if len(sys.argv) > 1 and sys.argv[1] == "present":
        build_present(logo, social)
        print("presentation written")
    else:
        build_site(logo)
        print("logo, social and site written")
