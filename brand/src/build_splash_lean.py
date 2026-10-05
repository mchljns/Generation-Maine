"""The lean splash page, in both concepts. Garrick's brief: a bare bones page that says what the project is, what it hopes to
achieve, and where the content lives, in the look of the Maine Policy family. Five blocks: the bar, the hero, two columns,
the creators roster, and four follow tiles with the newsletter form inside the Substack tile. Then the family footer.

The two audits are folded in. One control height, 48. No text under 13 px. Column labels at body size. The newsletter
button goes to the newsletter. The sign up field is a real form that hands the address to Substack. A share card, a title
with the one line, a skip link, a favicon. Outbound links carry a source. No stepper, no clips, no hidden sections.

  python3 brand/src/build_splash_lean.py          # writes brand/identity/splash-lean-a and splash-lean-b
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_splash as S
import build_splash_barksky as B
import build_splash_family as F
import build_kit as K
from gmlib import ROOT, write

LIVE = "https://mchljns.github.io/Generation-Maine/"
UTM = "utm_source=generationmaine&utm_medium=splash"
MG = "#EFB443"

SITE_CSS = lambda css: "\n".join(l for l in css.splitlines() if ".site" in l)

LEAN_A = dict(
    key="lean-a", out="brand/identity/splash-lean-a", root_class="static lean", navy="#0F2E4D", blue="#0556A5", ink="#0F2E4D", paper="#FFFFFF", tint="#EAF1F8",
    fonts=S.SIGNATURE_FONTS, font_files={}, logo=F.LOGO_A, mural=F.MURAL_A, hero="mural", credits="",
    display="'Bricolage Grotesque',system-ui,sans-serif", body="'DM Sans',system-ui,sans-serif", label="'DM Sans',system-ui,sans-serif",
    h1="Young Mainers on building a life <em>here.</em>", h2_about="What this is", h2_creators="The creators", h2_follow="Where to find it",
    site_css=SITE_CSS(F.STATIC_CSS) + "\n" + SITE_CSS(F.FAMILY_A_CSS % dict(blue="#0556A5", navy="#0F2E4D", mg=MG)),
    css="""
.lean h1,.lean h2,.lean .h2{font-family:var(--display);font-weight:800;letter-spacing:-.01em}
.lean h1 em{font-style:normal;color:var(--mg)}
.lean .col b{font-family:var(--body);font-weight:700}
""")

LEAN_B = dict(
    key="lean-b", out="brand/identity/splash-lean-b", root_class="bs static lean", navy="#112337", blue="#006CB5", ink="#112337", paper="#F4F3EE", tint="#EAF1F8",
    fonts=B.FONTS, font_files=B.BARK_SKY["font_files"], logo=F.LOGO_B, mural=None, hero="video", credits=B.BARK_SKY["credits"],
    display="'Hedvig Letters Serif',Georgia,serif", body="'Hedvig Letters Sans',system-ui,sans-serif", label="'Hedvig Letters Sans',system-ui,sans-serif",
    h1="young mainers on building a life here", h2_about="what this is", h2_creators="the creators", h2_follow="where to find it",
    site_css=SITE_CSS(F.STATIC_CSS) + "\n" + SITE_CSS(F.FAMILY_B["css"]),
    css="""
:root{--bark:#112337;--sky:#fff}
.lean h1,.lean h2,.lean .h2{font-family:var(--display);font-weight:400;letter-spacing:-.015em}
.lean .col b{font-family:var(--body);font-weight:400}
.lean .hero{color:#fff}
.lean .hero .bg{position:absolute;inset:0;overflow:hidden;background:var(--navy)}
.lean .hero .bg video{width:100%;height:100%;object-fit:cover;display:block}
.lean .hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,35,55,.78) 0%,rgba(17,35,55,.55) 45%,rgba(17,35,55,.18) 100%)}
.lean .hero .credit{position:absolute;right:var(--M);bottom:14px;margin:0;font-size:13px;color:rgba(255,255,255,.72);max-width:46ch;text-align:right}
.lean .hero .lede{color:rgba(255,255,255,.92)}
@media (prefers-reduced-motion: reduce){.lean .hero .bg video{display:none}.lean .hero .bg{background:url(media/hero-poster.jpg) center/cover no-repeat}}
@media (max-width:900px){.lean .hero .credit{position:static;text-align:left;margin-top:28px;max-width:none}}
""")

COLS = F.COLS[:2]
FOLLOW = [("instagram", "Instagram", "Short clips, most days.", "[@handle]", "#"),
          ("tiktok", "TikTok", "The same clips, where most of the audience is.", "[@handle]", "#"),
          ("youtube", "YouTube", "Longer cuts and the full interviews.", "[@handle]", "#"),
          ("substack", "Substack", "The full story, with the numbers, by email.", "[name].substack.com", "https://CONFIRM-publication.substack.com/subscribe")]


def utm(href):
    """Outbound links carry a source so the newsletter and the accounts can see what the page sends them."""
    if not href.startswith("http"):
        return href
    return href + ("&" if "?" in href else "?") + UTM


CSS = r"""
{{FONTS}}
:root{color-scheme:light;--navy:%(navy)s;--blue:%(blue)s;--mg:#EFB443;--ink:%(ink)s;--paper:%(paper)s;--tint:%(tint)s;--pine:%(navy)s;--snow:#fff;--display:%(display)s;--body:%(body)s;--M:60px;--ctl:48px}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;scroll-behavior:smooth;scroll-padding-top:68px}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 var(--body);-webkit-font-smoothing:antialiased}
img,svg,video{max-width:100%%}
a{color:inherit}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--mg);outline-offset:3px}
.skip{position:absolute;left:var(--M);top:-60px;z-index:50;background:var(--mg);color:var(--navy);padding:0 16px;height:var(--ctl);line-height:var(--ctl);font:600 13px/var(--ctl) var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none}
.skip:focus{top:8px}
.w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
.k{font:600 13px/1 var(--label);letter-spacing:.1em;text-transform:uppercase}
.lede{font-size:19px;line-height:1.55;margin:0}
h2,.h2{font-size:clamp(34px,4vw,52px);line-height:1.05;margin:0}
.btn,.tl{display:inline-flex;align-items:center;justify-content:center;height:var(--ctl);padding:0 24px;font:600 13px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;border:1px solid transparent;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.btn.b1{background:var(--mg);color:var(--navy);border-color:var(--mg)}.btn.b1:hover{background:#F3C364;border-color:#F3C364}
.btn.b2{background:transparent;color:inherit;border-color:currentColor}.btn.b2:hover{background:var(--mg);color:var(--navy);border-color:var(--mg)}
.tl{padding:0 4px;text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1.5px}
/* the bar: one height, one state */
.top{position:sticky;top:0;z-index:20;background:var(--navy);color:#fff;box-shadow:0 1px 0 rgba(255,255,255,.12)}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:24px;height:68px}
.top .lk{height:26px;width:auto;display:block}
.top nav{display:flex;gap:30px}
.top nav a{font:600 13px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;padding:12px 0;color:#fff}
.top nav a:hover{color:var(--mg)}
.top .cta{height:40px;padding:0 16px;border-color:var(--mg);color:var(--mg)}.top .cta:hover{background:var(--mg);color:var(--navy)}
.top .menu{display:none;width:44px;height:44px;border:0;background:none;color:#fff;cursor:pointer;padding:0;margin-right:-10px}
.top .menu svg{display:block;margin:auto}
.sheet{display:none}
/* the hero */
.hero{position:relative;background:var(--blue);color:#fff;min-height:min(calc(100svh - 68px),820px);display:grid;align-items:center;padding-block:72px}
.hero .w{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:40px;align-items:center;width:100%%}
.hero .k{display:block;margin-bottom:18px;color:var(--mg)}
.hero h1{font-size:clamp(44px,6.2vw,84px);line-height:1;margin:0 0 24px;max-width:12ch}
.hero .lede{max-width:46ch}
.hero .ctas{display:flex;flex-wrap:wrap;gap:18px;align-items:center;margin-top:28px}
.hero .mural{width:min(100%%,440px);justify-self:end;aspect-ratio:1}
.hero .mural svg{width:100%%;height:100%%;display:block}
.hero .mural path{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1.9s cubic-bezier(.3,.6,.2,1)}.hero .mural.on path{stroke-dashoffset:0}
.js .rise{opacity:0;transform:translateY(14px);transition:opacity .7s ease-out,transform .9s cubic-bezier(.2,.7,.2,1)}.js .rise.in{opacity:1;transform:none}
@media (prefers-reduced-motion: reduce){.hero .mural path{stroke-dashoffset:0;transition:none}.js .rise{opacity:1;transform:none;transition:none}}
/* sections */
section.block{padding-block:112px}
.block .head{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start;margin-bottom:48px}
.block .head .lede{max-width:56ch}
.about{background:var(--paper)}
.about .cols{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.about .col{border-top:2px solid var(--blue);padding-top:18px}
.about .col b{display:block;font-size:19px;line-height:1.3;margin-bottom:10px}
.about .col p{margin:0;font-size:17px;line-height:1.6;max-width:52ch}
/* the roster: nine towns, no faces until the shoot */
.roster{background:var(--tint)}
.roster .grid{display:grid;grid-template-columns:repeat(9,1fr);gap:12px}
.roster .tile{background:var(--paper);border-top:2px solid var(--blue);padding:16px 14px 18px;min-height:112px;display:grid;align-content:space-between;gap:14px;text-decoration:none;color:inherit}
.roster .tile .n{font:600 13px/1 var(--label);letter-spacing:.1em;color:var(--blue)}
.roster .tile b{font-size:17px;line-height:1.2;font-weight:700;font-family:var(--body)}
.roster .tile .av{width:44px;height:44px;border-radius:50%%;background:var(--tint);display:none}
.roster .tile.ready .av{display:block}
a.roster-tile:hover{border-top-color:var(--navy)}
/* follow tiles: the conversion block */
.follow{background:var(--navy);color:#fff}
.follow .tiles{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.follow .tile{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);padding:28px;display:grid;grid-template-columns:28px 1fr;gap:16px 18px;align-items:start;text-decoration:none;color:inherit;min-height:168px;transition:border-color .2s,background .2s}
a.follow-tile:hover{border-color:var(--mg);background:rgba(255,255,255,.1)}
.follow .tile .ic{width:28px;height:28px;color:var(--mg);margin-top:2px}
.follow .tile b{display:block;font-size:19px;line-height:1.2;font-weight:600;font-family:var(--body);margin-bottom:6px}
.follow .tile p{margin:0;font-size:15px;line-height:1.5;color:rgba(255,255,255,.82)}
.follow .tile .h{display:block;margin-top:14px;font:600 13px/1 var(--label);letter-spacing:.06em;color:var(--mg)}
.follow .tile .meta{grid-column:2}
.follow form{grid-column:1/-1;display:grid;grid-template-columns:1fr auto;gap:12px;margin-top:6px}
.follow input{height:var(--ctl);border:1px solid rgba(255,255,255,.4);background:#fff;color:var(--ink);padding:0 16px;font:16px var(--body);width:100%%}
.follow input:focus-visible{outline-color:var(--mg)}
.follow .fine{grid-column:1/-1;margin:10px 0 0;font-size:13px;color:rgba(255,255,255,.65)}
/* responsive */
@media (max-width:1100px){.roster .grid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:900px){
 :root{--M:20px}
 body{font-size:16px}
 .top nav,.top .cta{display:none}.top .menu{display:block}
 .sheet{display:block;position:fixed;inset:68px 0 0 0;background:var(--navy);color:#fff;z-index:19;padding:24px var(--M);transform:translateY(-8px);opacity:0;pointer-events:none;transition:opacity .2s,transform .25s}
 .sheet.open{opacity:1;transform:none;pointer-events:auto}
 .sheet nav{display:grid;gap:6px}.sheet nav a{font:600 15px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:#fff;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.12)}
 .sheet .btn{margin-top:20px;width:100%%}
 .hero{padding-block:48px 56px;min-height:0}
 .hero .w{grid-template-columns:1fr;gap:28px}
 .hero .mural{order:-1;width:min(56vw,300px);justify-self:start}
 .hero h1{max-width:none}
 section.block{padding-block:56px}
 .block .head{grid-template-columns:1fr;gap:16px;margin-bottom:32px}
 .about .cols{grid-template-columns:1fr;gap:28px}
 .follow .tiles{grid-template-columns:1fr}
 .follow form{grid-template-columns:1fr}
}
%(site_css)s
%(css)s
"""

HTML = """<!doctype html><html lang="en" class="%(root_class)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><script>document.documentElement.classList.add("js")</script>
<title>Generation Maine: young Mainers on the rules that shape their lives</title>
<meta name="description" content="Young Mainers film the rules that shape their lives. Short videos on TikTok, Instagram and YouTube, and the full story by email. A Maine Policy Institute project.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="app-icon.png">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website"><meta property="og:site_name" content="Generation Maine"><meta property="og:url" content="%(url)s">
<meta property="og:title" content="Generation Maine"><meta property="og:description" content="Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.">
<meta property="og:image" content="%(url)smedia/share.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Generation Maine">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Generation Maine"><meta name="twitter:description" content="Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine."><meta name="twitter:image" content="%(url)smedia/share.jpg">
<style>%(css)s</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="w">
  <a href="#top" aria-label="Generation Maine, home">%(bar_logo)s</a>
  <nav aria-label="Page"><a href="#about">About</a><a href="#creators">Creators</a><a href="#follow">Follow</a></nav>
  <a class="btn b2 cta" href="#newsletter">Get the newsletter</a>
  <button class="menu" id="menu" aria-label="Menu" aria-expanded="false" aria-controls="sheet"><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="2"/></svg></button>
</div></header>
<div class="sheet" id="sheet" aria-hidden="true"><nav aria-label="Page"><a href="#about">About</a><a href="#creators">Creators</a><a href="#follow">Follow</a></nav><a class="btn b1" href="#newsletter">Get the newsletter</a></div>
<main id="main">
<section class="hero" id="top">%(hero_bg)s<div class="w">
  <div>
    <span class="k rise" id="k">A Maine Policy Institute project</span>
    <h1 class="rise" id="h1">%(h1)s</h1>
    <p class="lede rise" id="lede">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay. Told from the towns they live in.</p>
    <div class="ctas rise" id="ctas"><a class="btn b1" href="#follow">Follow along</a><a class="tl" href="#about">What this is</a></div>
  </div>
  %(hero_side)s
</div>%(hero_credit)s</section>

<section class="block about" id="about"><div class="w">
  <div class="head"><h2>%(h2_about)s</h2><p class="lede">Short videos from young people in Maine about the rules behind everyday costs, and a newsletter with the full story. Nothing is published on this page; it points to where the work lives.</p></div>
  <div class="cols">%(cols)s</div>
</div></section>

<section class="block roster" id="creators"><div class="w">
  <div class="head"><h2>%(h2_creators)s</h2><p class="lede">Nine young Mainers in nine towns. Each one films where they live and says it their own way. Names and faces arrive after the shoot. First clips [CONFIRM: month].</p></div>
  <div class="grid">%(tiles)s</div>
</div></section>

<section class="block follow" id="follow"><div class="w">
  <div class="head"><h2>%(h2_follow)s</h2><p class="lede">The videos are on TikTok, Instagram and YouTube. The full story, with the numbers, is in the newsletter on Substack.</p></div>
  <div class="tiles">%(follow)s</div>
</div></section>
</main>
<footer class="site">%(footer)s</footer>
<script id="maine-data" type="application/json">%(mural_json)s</script>
<script>
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // hero type rises in
  const rise = [...document.querySelectorAll('.hero .rise')];
  requestAnimationFrame(() => requestAnimationFrame(() => rise.forEach((el, i) => setTimeout(() => el.classList.add('in'), reduced ? 0 : 90 * i))));
  // the mural, on Family A: sixteen stripes drawing themselves in
  const m = document.getElementById('mural');
  if (m) {
    const d = JSON.parse(document.getElementById('maine-data').textContent), ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('viewBox', '0 0 720 720'); svg.setAttribute('aria-hidden', 'true');
    const defs = document.createElementNS(ns, 'defs'), cp = document.createElementNS(ns, 'clipPath'); cp.setAttribute('id', 'muralclip');
    const cpp = document.createElementNS(ns, 'path'); cpp.setAttribute('d', d.clip); cp.appendChild(cpp); defs.appendChild(cp); svg.appendChild(defs);
    const g = document.createElementNS(ns, 'g'); g.setAttribute('clip-path', 'url(#muralclip)'); svg.appendChild(g);
    d.lines.forEach(([x0, y0, x1, y1, w, c], i) => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M' + x0 + ' ' + y0 + ' L' + x1 + ' ' + y1); p.setAttribute('stroke', c || '#FFFFFF'); p.setAttribute('stroke-width', w); p.setAttribute('fill', 'none'); p.setAttribute('pathLength', '1'); p.style.transitionDelay = (i * (d.stagger || 35)) + 'ms'; g.appendChild(p); });
    m.appendChild(svg); requestAnimationFrame(() => requestAnimationFrame(() => m.classList.add('on')));
  }
  // the footer mark draws once the page is scrolled to its end
  const site = document.querySelector('.site');
  const atEnd = () => { if (innerHeight + scrollY >= document.documentElement.scrollHeight - 2) { site.classList.add('on'); removeEventListener('scroll', atEnd); } };
  addEventListener('scroll', atEnd, { passive: true }); atEnd();
  // phone menu
  const sheet = document.getElementById('sheet'), menu = document.getElementById('menu');
  const setMenu = o => { sheet.classList.toggle('open', o); sheet.setAttribute('aria-hidden', String(!o)); menu.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; };
  menu.addEventListener('click', () => setMenu(!sheet.classList.contains('open')));
  sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  // the newsletter form hands the address to Substack, which prefills it
  const f = document.getElementById('nl');
  if (f) f.addEventListener('submit', e => { e.preventDefault(); const em = f.email.value.trim(); if (!em) { f.email.focus(); return; } const u = new URL(f.action); u.searchParams.set('email', em); window.open(u.toString(), '_blank', 'noopener'); });
})();
</script>
</body></html>"""


def cols_html():
    return "".join('<div class="col"><b>%s</b><p>%s</p></div>' % (t, p) for t, p in COLS)


def tiles_html():
    out = []
    for i, town in enumerate(S.TOWNS):
        out.append('<div class="tile" aria-label="Creator %d, %s, Maine"><span class="n">%02d</span><span class="av" aria-hidden="true"></span><b>%s</b></div>' % (i + 1, town, i + 1, town))
    return "".join(out)


def follow_html():
    out = []
    for key, name, line, handle, href in FOLLOW:
        if key == "substack":
            out.append('<div class="tile" id="newsletter">%s<div class="meta"><b>%s</b><p>%s</p><span class="h">%s</span></div>'
                       '<form id="nl" action="%s" method="get" target="_blank" rel="noopener"><label class="k" for="em" style="position:absolute;left:-9999px">Email</label>'
                       '<input id="em" name="email" type="email" placeholder="you@example.com" autocomplete="email" required inputmode="email"><button class="btn b1" type="submit">Sign up</button>'
                       '<p class="fine">Runs on Substack. Unsubscribe in one click. [CONFIRM: publication address]</p></form></div>'
                       % (S.icon(key), name, line, handle, utm(href)))
        else:
            out.append('<a class="tile follow-tile" href="%s" rel="noopener"%s>%s<span class="meta"><b>%s</b><p>%s</p><span class="h">%s</span></span></a>'
                       % (utm(href), ' target="_blank"' if href.startswith("http") else "", S.icon(key), name, line, handle))
    return "".join(out)


def share_card(theme, out_dir):
    """A 1200 by 630 share image. Family B crops the hero poster under the mark; Family A sets the mark on navy."""
    media = os.path.join(ROOT, out_dir, "media")
    os.makedirs(media, exist_ok=True)
    lk = S.logo("lockup-two-line-reversed", "lk", theme["logo"])
    bg = ('<img src="hero-poster.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
          '<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,35,55,.82),rgba(17,35,55,.35))"></div>') if theme["hero"] == "video" else ""
    html = ('<!doctype html><meta charset="utf-8"><style>body{margin:0;width:1200px;height:630px;background:%s;position:relative;overflow:hidden;font-family:system-ui}'
            '.lk{position:absolute;left:90px;top:50%%;transform:translateY(-50%%);height:%dpx;width:auto}.lk path{stroke-dashoffset:0!important}'
            '.t{position:absolute;left:90px;bottom:70px;color:#fff;font-size:26px;line-height:1.3;max-width:620px;opacity:.9}</style>'
            '<body>%s%s</body>' % (theme["navy"], 300 if theme["hero"] == "video" else 260, bg, lk))
    path = os.path.join(media, "share.html")
    open(path, "w").write(html)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), path, os.path.join(media, "share.png"), "1200", "1"], check=True)
    from PIL import Image
    im = Image.open(os.path.join(media, "share.png")).convert("RGB").crop((0, 0, 1200, 630))
    im.save(os.path.join(media, "share.jpg"), quality=86)
    os.remove(path); os.remove(os.path.join(media, "share.png"))


def icons(theme, out_dir):
    """favicon.svg and a 180 px app icon from the concept's avatar mark."""
    fav = "favicon.svg" if os.path.exists(os.path.join(theme["logo"], "favicon.svg")) else "avatar-square.svg"
    shutil.copy(os.path.join(theme["logo"], fav), os.path.join(ROOT, out_dir, "favicon.svg"))
    src = os.path.join(theme["logo"], "app-icon.svg" if os.path.exists(os.path.join(theme["logo"], "app-icon.svg")) else "avatar-square.svg")
    html = '<!doctype html><meta charset="utf-8"><style>body{margin:0;width:180px;height:180px}img{width:180px;height:180px;display:block}</style><img src="file://%s">' % src
    p = os.path.join(ROOT, out_dir, "icon.html"); open(p, "w").write(html)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), p, os.path.join(ROOT, out_dir, "app-icon.png"), "180", "1"], check=True)
    os.remove(p)


def page(theme):
    out_dir = theme["out"]
    os.makedirs(os.path.join(ROOT, out_dir, "media"), exist_ok=True)
    css = (CSS % dict(theme, site_css=theme["site_css"]))
    css = css.replace("{{FONTS}}", theme["fonts"]).replace("{{F800}}", K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2")).replace("{{FINTER}}", K.font64("brand/fonts/inter-var.woff2")).replace("{{FDM}}", K.font64("generation-maine/assets/fonts/dm-sans-var.ttf"))
    for k, v in theme["font_files"].items():
        css = css.replace("{{%s}}" % k, K.font64(v))
    if theme["hero"] == "video":
        hero_bg = '<div class="bg" aria-hidden="true"><video autoplay muted loop playsinline preload="metadata" poster="media/hero-poster.jpg"><source src="media/hero.webm" type="video/webm"></video></div>'
        hero_side = ""
        hero_credit = '<p class="credit">Katahdin, Aroostook County, Cadillac Mountain, Portland Head Light, the Old Port. Photographs via Wikimedia Commons, credits in the footer.</p>'
        # the loop and its poster: the lighter render if present, else the one the family page uses
        fam = os.path.join(ROOT, "brand", "identity", "splash-family-b", "media")
        for f in ("hero.webm", "hero-poster.jpg"):
            dst = os.path.join(ROOT, out_dir, "media", f)
            if not os.path.exists(dst):
                shutil.copy(os.path.join(fam, f), dst)
    else:
        hero_bg = ""
        hero_side = '<div class="mural" id="mural" aria-hidden="true"></div>'
        hero_credit = ""
    footer = F.family_footer(S.draw_paths(S.logo("lockup-two-line-reversed", "lk", theme["logo"])), dict(credits=theme["credits"]))
    footer = footer.replace('href="#signup"', 'href="#newsletter"')
    footer = re.sub(r'href="(https?://[^"]+)"', lambda m: 'href="%s"' % utm(m.group(1)), footer)
    url = LIVE + theme["key"] + "/"
    html = HTML % dict(root_class=theme["root_class"], css=css, url=url, bar_logo=S.logo("lockup-compact-reversed", "lk", theme["logo"]), h1=theme["h1"],
                       hero_bg=hero_bg, hero_side=hero_side, hero_credit=hero_credit, h2_about=theme["h2_about"], h2_creators=theme["h2_creators"], h2_follow=theme["h2_follow"],
                       cols=cols_html(), tiles=tiles_html(), follow=follow_html(), footer=footer, mural_json=json.dumps(theme["mural"]) if theme["mural"] else "{}")
    write(os.path.join(out_dir, "index.html"), html)
    icons(theme, out_dir)
    share_card(theme, out_dir)
    print("wrote", out_dir)


if __name__ == "__main__":
    for t in (LEAN_A, LEAN_B):
        page(t)
