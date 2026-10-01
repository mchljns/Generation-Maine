"""The splash page: one page, no photos yet, the brand's line field as the motion system.

Sections: nav with the horizontal lockup, the hero with the field and the mural, what this is,
the creators (placeholders), the newsletter, the Institute line in its own section, follow, footer.

  python3 brand/src/build_splash.py   # writes brand/identity/splash/index.html and artifact.html
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import build_kit as K
import maine2
from build_v6 import C

LOGO = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")
MPI = "An initiative of Maine Policy Institute"
TOWNS = ["Skowhegan", "Presque Isle", "Biddeford", "Machias", "Lewiston", "Rumford", "Belfast", "Fort Kent", "Sanford"]
TOPICS = ["Finding a place", "Starting a shop", "Who stays", "The commute", "Coming home", "Moving out", "Two jobs", "Doing the math", "Winter work"]
FIELDS = ["sp", "bi", "pi", "sp", "bi", "pi", "sp", "bi", "mg"]


def logo(name, cls=""):
    with open(os.path.join(LOGO, name + ".svg")) as fh:
        return fh.read().replace('role="img"', "").replace("<svg ", '<svg class="%s" ' % cls, 1)


def mural_rows(h=720):
    """The hero mural is the logo's full cut at hero scale: sixteen lines, the two points kept, as row data for the draw-in."""
    w_box = h * maine2.ASPECT
    ring = maine2.fit((720 - w_box) / 2, 0, w_box, h)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    rows = []
    for i in range(16):
        t = i / 15
        y0 = miny + (maxy - miny) * (0.024 + 0.946 * t)
        w = h * (0.026 + 0.018 * t)
        xs = maine2.crossings(ring, y0)
        runs = []
        for a, b in zip(xs[0::2], xs[1::2]):
            if i == 0:
                if b - a < w:
                    c = (a + b) / 2
                    a, b = c - w / 2, c + w / 2
                runs.append([round(a + w / 2 * 0.999, 1), round(b - w / 2 * 0.999, 1)])
            elif b - a >= w * 1.8:
                runs.append([round(a + w / 2, 1), round(b - w / 2, 1)])
        rows.append({"y": round(y0, 1), "w": round(w, 2), "runs": runs})
    return {"rows": rows}


def dot(text, cls=""):
    head, _, last = text.rpartition(" ")
    return '<span class="%s">%s<b class="nw">%s<i class="d"></i></b></span>' % (cls, (head + " ") if head else "", last)


CSS = r"""
/* Layout: one column, big tight type low left, the field of lines as the only picture. */
:root{
  --sp:#104836;--pine:#0B2B21;--bi:#F4F0E6;--ink:#1E2621;--mg:#EFB443;--sage:#DDE5DA;--moss:#3D6F58;--stone:#5E6A63;
  --bg:var(--bi);--fg:var(--ink);--muted:var(--stone);--rule:rgba(30,38,33,.14);--card:#FFFFFF;
  --display:'Bricolage Grotesque',Arial,sans-serif;--body:Inter,system-ui,Arial,sans-serif;
  --M:clamp(16px,4.5vw,64px);
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:var(--pine);--fg:var(--bi);--muted:#AEBDB4;--rule:rgba(244,240,230,.16);--card:#0F3A2C;color-scheme:dark}}
:root[data-theme="dark"]{--bg:var(--pine);--fg:var(--bi);--muted:#AEBDB4;--rule:rgba(244,240,230,.16);--card:#0F3A2C;color-scheme:dark}
@font-face{font-family:'Bricolage Grotesque';font-weight:800;font-display:swap;src:url(data:font/woff2;base64,{{F800}}) format('woff2')}
@font-face{font-family:Inter;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,{{FINTER}}) format('woff2')}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 var(--body);-webkit-font-smoothing:antialiased}
a{color:inherit}
.w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.03em;line-height:.92;margin:0;text-wrap:balance}
.d{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--mg);margin-left:.05em;vertical-align:baseline}
.nw{white-space:nowrap;font-weight:inherit}
.k{font:600 12px/1.2 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.btn{display:inline-block;font:600 15px/1 var(--body);padding:16px 22px;border-radius:6px;text-decoration:none;border:1.5px solid transparent;transition:transform .25s cubic-bezier(.2,.7,.2,1),background .25s}
.btn:hover{transform:translateY(-2px)}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--mg);outline-offset:3px}
.b1{background:var(--bi);color:var(--sp)}.b2{color:var(--bi);border-color:rgba(244,240,230,.55)}.b2:hover{background:rgba(244,240,230,.08)}
.b3{background:var(--sp);color:var(--bi)}

/* nav */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--sp);color:var(--bi)}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:24px;height:68px}
.top .lk{height:30px;width:auto;display:block}
.top nav{display:flex;gap:28px;font:600 14px/1 var(--body)}
.top nav a{text-decoration:none;opacity:.92}.top nav a:hover{opacity:1;text-decoration:underline;text-underline-offset:4px}
@media (max-width:640px){.top nav{display:none}}
.disc{background:var(--pine);color:var(--bi)}
.disc .w{font:600 13px/1.3 var(--body);padding-block:10px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.disc a{opacity:.85;text-decoration:underline;text-underline-offset:3px}

/* hero */
.hero{position:relative;background:var(--sp);color:var(--bi);overflow:hidden}
.hero .w{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:32px;padding-block:72px 80px;min-height:640px;align-items:end}
#field{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:1}
.hero h1{font-size:clamp(46px,8.2vw,112px);max-width:11ch}
.hero .lede{font-size:clamp(17px,1.5vw,21px);line-height:1.45;max-width:42ch;margin:28px 0 30px;color:rgba(244,240,230,.9)}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.mural{position:relative;justify-self:end;width:min(100%,520px);aspect-ratio:1;max-width:100%}
.mural svg{width:100%;height:100%;display:block}
.mural path{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1)}
.mural.on path{stroke-dashoffset:0}
@media (prefers-reduced-motion: reduce){.mural path{stroke-dashoffset:0;transition:none}}
@media (max-width:900px){.hero .w{grid-template-columns:1fr;min-height:0;padding-block:56px 64px}.mural{justify-self:start;width:min(70vw,360px);order:-1}}
.hero .h1{opacity:1;transform:none}
.hero .rise{transition:transform .9s cubic-bezier(.2,.7,.2,1),opacity .9s}
.hero .rise.pre{opacity:0;transform:translateY(18px)}

/* on scroll: headings land their dot, rules draw from the left, rows rise. Visible at rest; script adds .pre then removes it */
.js .reveal.pre .d{transform:scale(0)}.reveal .d{transition:transform .5s cubic-bezier(.3,1.4,.4,1) .35s}
.js .reveal.pre .rule{transform:scaleX(0)}.rule{transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.js .reveal.pre .row-in{transform:translateY(14px);opacity:.001}.row-in{transition:transform .7s cubic-bezier(.2,.7,.2,1),opacity .7s}
.reveal .row-in:nth-child(2){transition-delay:.08s}.reveal .row-in:nth-child(3){transition-delay:.16s}.reveal .row-in:nth-child(4){transition-delay:.24s}
@media (prefers-reduced-motion: reduce){.js .reveal.pre .d,.js .reveal.pre .rule,.js .reveal.pre .row-in{transform:none;opacity:1}}
/* sections */
section{padding-block:clamp(56px,8vw,112px)}
.what .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px}
.what h2{font-size:clamp(34px,4.6vw,60px)}
.what .cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;align-self:end}
.what .cols h3{font:600 15px/1.3 var(--body);letter-spacing:0;margin:0 0 8px;color:var(--fg)}
.what .cols p{margin:0;color:var(--muted);line-height:1.5}
.what .cols div{padding-top:16px;position:relative}.what .cols div::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:var(--fg)}
@media (max-width:900px){.what .w,.news .w,.who .w{grid-template-columns:1fr}.what .cols{grid-template-columns:1fr}}

.creators{background:var(--sage);color:var(--ink)}
:root[data-theme="dark"] .creators{background:#0F3A2C;color:var(--bi)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .creators{background:#0F3A2C;color:var(--bi)}}
.creators .head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:36px}
.creators h2{font-size:clamp(34px,4.6vw,60px)}
.creators .head p{max-width:46ch;margin:0;color:inherit;opacity:.8}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
@media (max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.grid{grid-template-columns:1fr}}
.cov{position:relative;aspect-ratio:4/5;border-radius:10px;overflow:hidden;padding:22px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none;isolation:isolate;transform:translateY(0);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.cov:hover{transform:translateY(-4px)}
.cov.sp{background:var(--sp);color:var(--bi)}.cov.pi{background:var(--pine);color:var(--bi)}.cov.bi{background:#FFFFFF;color:var(--sp)}.cov.mg{background:var(--mg);color:var(--ink)}
.cov .lines{position:absolute;inset:0;z-index:-1;background:repeating-linear-gradient(to bottom,transparent 0 11px,currentColor 11px 12.5px);opacity:0;transform:translateX(-8%);transition:opacity .5s,transform .7s cubic-bezier(.2,.7,.2,1);mask-image:linear-gradient(to right,black 0,black 38%,transparent 72%);-webkit-mask-image:linear-gradient(to right,black 0,black 38%,transparent 72%)}
.cov:hover .lines,.cov.on .lines{opacity:.09;transform:none}
.cov .nm{font:600 13px/1.3 var(--body);margin:0}.cov .nm span{font-weight:400;opacity:.8}
.cov h3{font-size:clamp(30px,2.6vw,40px);max-width:9ch}
.cov .ph{position:absolute;right:18px;top:18px;font:600 11px/1 var(--body);letter-spacing:.06em;text-transform:uppercase;opacity:.5}

.news .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.news h2{font-size:clamp(34px,4.6vw,60px)}
.news .lede{color:var(--muted);max-width:42ch;margin:18px 0 26px}
.form{display:flex;gap:10px;flex-wrap:wrap;max-width:520px}
.form input{flex:1 1 220px;min-width:0;font:16px var(--body);padding:15px 16px;border-radius:6px;border:1.5px solid var(--rule);background:var(--card);color:var(--fg)}
.form .note{flex-basis:100%;font-size:13px;color:var(--muted);margin:4px 0 0}
.form .ok{flex-basis:100%;font:600 15px var(--body);color:var(--fg);margin:4px 0 0}
.posts{display:grid;gap:0;position:relative}.posts .rule,.follow .rule{display:block;height:1.5px;background:var(--fg)}
.post{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.post h3{font-size:clamp(22px,2vw,28px);margin:0 0 8px}
.post p{margin:0;color:var(--muted);font-size:15px}
.post .by{font:600 13px/1.3 var(--body);color:var(--fg);margin-top:10px}.post .by span{font-weight:400;color:var(--muted)}
.post .dt{font:600 13px/1.3 var(--body);color:var(--muted);white-space:nowrap;padding-top:6px}

.who{background:var(--sp);color:var(--bi)}
.who .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px}
.who h2{font-size:clamp(34px,4.6vw,60px)}
.who p{margin:0 0 16px;max-width:58ch;line-height:1.55;color:rgba(244,240,230,.92)}
.who .mpi{font:600 clamp(20px,2vw,26px)/1.3 var(--body);margin:0 0 20px}
.who a{color:var(--bi)}

.follow .row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media (max-width:760px){.follow .row{grid-template-columns:repeat(2,minmax(0,1fr))}}
.follow a{display:block;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.follow a b{display:block;font:600 15px/1.3 var(--body)}.follow a span{color:var(--muted);font-size:15px}
.follow h2{font-size:clamp(34px,4.6vw,60px);margin-bottom:28px}

footer{background:var(--pine);color:var(--bi);padding-block:48px 40px}
footer .w{display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:end}
footer .lk{height:120px;width:auto;display:block}
footer p{margin:0;font-size:14px;color:rgba(244,240,230,.8);max-width:60ch}
footer .fine{margin-top:12px;font-size:13px}
@media (max-width:640px){footer .w{grid-template-columns:1fr}footer .lk{height:96px}}
"""


def page():
    rows = mural_rows()
    covers = ""
    for i in range(9):
        covers += ('<a class="cov %s" href="#" aria-label="%s, %s, Maine"><span class="lines" aria-hidden="true"></span><p class="nm">[Creator name] <span>%s, Maine</span></p>'
                   '<h3>%s</h3><span class="ph">[Placeholder]</span></a>') % (FIELDS[i], TOPICS[i], TOWNS[i], TOWNS[i], dot(TOPICS[i]))
    body = r'''
<header class="top"><div class="w"><a href="#top" aria-label="Generation Maine, home">%(lock)s</a>
<nav aria-label="Page"><a href="#what">About</a><a href="#creators">Creators</a><a href="#news">Newsletter</a><a href="#who">Funding</a></nav></div></header>
<div class="disc"><div class="w"><span>%(mpi)s.</span><a href="#who">Read how it is funded</a></div></div>

<section class="hero" id="top"><canvas id="field" aria-hidden="true"></canvas><div class="w">
  <div class="h1"><h1 id="h1" class="rise">%(h1)s</h1>
  <p id="lede" class="lede rise">Short videos and a newsletter by young Maine creators about the rules that shape their lives. Rent, wages, licenses, permits and what they cost.</p>
  <p class="ctas rise" id="ctas"><a class="btn b1" href="#creators">Meet the creators</a><a class="btn b2" href="#news">Follow along</a></p></div>
  <div class="mural" id="mural" aria-hidden="true"></div>
</div></section>

<section class="what reveal" id="what"><div class="w">
  <h2>%(h2what)s</h2>
  <div class="cols">
    <div class="row-in"><h3>Who makes it</h3><p>Young Mainers, each filming in their own town. They choose the stories and tell them in their own words.</p></div>
    <div class="row-in"><h3>What it covers</h3><p>The rules behind everyday costs. Finding an apartment, opening a shop, getting licensed, deciding whether to stay.</p></div>
    <div class="row-in"><h3>Where it lives</h3><p>Short vertical videos on TikTok, Instagram and YouTube. A longer read on Substack.</p></div>
  </div>
</div></section>

<section class="creators reveal" id="creators"><div class="w">
  <div class="head"><h2>%(h2cre)s</h2><p>One story from each creator. Names and portraits arrive after the shoot. Every card is a real town.</p></div>
  <div class="grid">%(covers)s</div>
</div></section>

<section class="news reveal" id="news"><div class="w">
  <div><h2>%(h2news)s</h2><p class="lede">A creator's story in full, with the numbers behind it, by email. Your address is never shared. [CONFIRM: privacy line]</p>
  <form class="form" id="signup" novalidate><label class="k" for="email" style="flex-basis:100%%">Email</label><input id="email" type="email" name="email" placeholder="you@example.com" autocomplete="email" required><button class="btn b3" type="submit">Subscribe</button>
  <p class="note">Runs on Substack. Unsubscribe in one click.</p><p class="ok" id="ok" hidden>Check your inbox. The confirmation is on its way.</p></form></div>
  <div class="posts"><span class="rule" aria-hidden="true"></span>
    <a class="post row-in" href="#"><div><h3>[Post title in plain words]</h3><p>[One sentence on what the creator found out, in their words.]</p><p class="by">[Creator name] <span>Belfast, Maine</span></p></div><span class="dt">[Date]</span></a>
    <a class="post row-in" href="#"><div><h3>[Post title in plain words]</h3><p>[One sentence on what the creator found out, in their words.]</p><p class="by">[Creator name] <span>Machias, Maine</span></p></div><span class="dt">[Date]</span></a>
    <a class="post row-in" href="#"><div><h3>[Post title in plain words]</h3><p>[One sentence on what the creator found out, in their words.]</p><p class="by">[Creator name] <span>Lewiston, Maine</span></p></div><span class="dt">[Date]</span></a>
  </div>
</div></section>

<section class="who reveal" id="who"><div class="w">
  <h2>%(h2who)s</h2>
  <div><p class="mpi">Generation Maine is %(mpilower)s.</p>
  <p>The Institute pays for the project and the creators' time. The creators choose their own stories and keep their own voice. Nothing is scripted.</p>
  <p>The Institute's name appears on every video end card, in every channel bio and on this page. To see who funds the Institute, start here: <a href="#">[CONFIRM: link to the Institute's funding page]</a>.</p>
  <p>Questions about the project go to <a href="#">[CONFIRM: contact email]</a>.</p></div>
</div></section>

<section class="follow reveal" id="follow"><div class="w">
  <h2>%(h2follow)s</h2>
  <span class="rule" aria-hidden="true"></span><div class="row">
    <a class="row-in" href="#"><b>Instagram</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>TikTok</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>YouTube</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>Substack</b><span>[name].substack.com</span></a>
  </div>
</div></section>

<footer><div class="w">%(two)s<div><p>Short videos and a newsletter by young Maine creators about the rules that shape their lives. %(mpi)s.</p><p class="fine">© 2026 Maine Policy Institute. [CONFIRM: legal name and address]</p></div></div></footer>

<script id="maine-data" type="application/json">%(json)s</script>
<script>
(() => {
  const SP = '#104836', MOSS = '#3D6F58', MG = '#EFB443', BI = '#F4F0E6';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.querySelector('.hero'), cv = document.getElementById('field'), ctx = cv.getContext('2d');
  const h1 = document.getElementById('h1'), lede = document.getElementById('lede'), ctas = document.getElementById('ctas');
  if (!reduced) { [h1, lede, ctas].forEach(el => el.classList.add('pre')); requestAnimationFrame(() => requestAnimationFrame(() => { h1.classList.remove('pre'); setTimeout(() => lede.classList.remove('pre'), 120); setTimeout(() => ctas.classList.remove('pre'), 240); })); }

  // The field: lines across the hero make room for the headline on load and for the pointer as it moves. The lines stay Moss, so the headline's dot is the frame's one Marigold.
  let W = 0, H = 0, lines = []; const N = 16, STEPS = 200;
  const ptr = { x: -9999, y: -9999, tx: -9999, ty: -9999, r: 22 };
  let open = 0, t0 = performance.now(), running = true;
  function rects() { const hb = hero.getBoundingClientRect(); return [h1, lede].map((el, i) => { const r = el.getBoundingClientRect(); return { x0: r.left - hb.left - 8, y0: r.top - hb.top + (i ? -6 : 10), x1: r.right - hb.left + 8, y1: r.bottom - hb.top + (i ? 6 : -4), gold: false }; }); }
  function resize() { const b = hero.getBoundingClientRect(); W = b.width; H = b.height; const dpr = Math.min(2, devicePixelRatio || 1); cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); const top = Math.min(120, H * .17), bot = H - 14; lines = []; for (let i = 0; i < N; i++) { const t = i / (N - 1); lines.push({ y: top + (bot - top) * t, w: 1.4 + 2.2 * t, ph: Math.random() * 6.283, ys: new Float32Array(STEPS + 1), gold: new Uint8Array(STEPS + 1), cut: new Uint8Array(STEPS + 1) }); } }
  function smooth(a, k) { const n = a.length, o = new Float32Array(n); for (let i = 0; i < n; i++) { let acc = 0, ws = 0; for (let j = Math.max(0, i - 2 * k); j <= Math.min(n - 1, i + 2 * k); j++) { const w = Math.exp(-(((j - i) / k) ** 2) / 2); acc += a[j] * w; ws += w; } o[i] = acc / ws; } return o; }
  function frame(now) {
    const clearMax = Math.min(34, W * .028);
    if (!reduced) { const e = Math.min(1, (now - t0) / 1200); open = 1 - Math.pow(1 - e, 3); } else open = 1;
    const clear = clearMax * open; ptr.x += (ptr.tx - ptr.x) * .14; ptr.y += (ptr.ty - ptr.y) * .14;
    const obs = rects(); ctx.clearRect(0, 0, W, H);
    const dx = W / STEPS, k = Math.max(2, Math.round(STEPS * clearMax / W * .6)); const T = now / 1000;
    for (const L of lines) {
      const y0 = L.y, drift = reduced ? 0 : 2.2;
      for (let s = 0; s <= STEPS; s++) {
        const px = s * dx; let py = y0 + drift * Math.sin(T * .35 + L.ph + px / W * 2.4), best = 0, gk = 0, cut = 0;
        for (const r of obs) { const ddx = px < r.x0 ? r.x0 - px : (px > r.x1 ? px - r.x1 : 0); if (ddx >= clear || clear <= 0) continue; const hh = Math.sqrt(clear * clear - ddx * ddx), top = r.y0 - hh, bot = r.y1 + hh; if (y0 > top && y0 < bot) { cut = 1; continue; } const gap = Math.min(Math.abs(y0 - top), Math.abs(y0 - bot)); const bow = .55 * clear * Math.exp(-(((gap) / (.7 * clear)) ** 2)); if (bow > best && bow > .02 * clear) { best = bow; py = y0 <= top ? y0 - bow : y0 + bow; gk = 0; } }
        const R = ptr.r + clear * .9, pdx = px - ptr.x, dy0 = y0 - ptr.y, ady = Math.abs(dy0), sign = dy0 >= 0 ? 1 : -1;
        if (Math.abs(pdx) < R * 1.8 && ptr.x > -100) { let amp, sig; if (ady < R) { amp = R - ady; sig = R * .75; } else { amp = .42 * R * Math.exp(-(((ady - R) / (.55 * R)) ** 2)); sig = R * .95; } let off = amp * Math.exp(-((pdx / sig) ** 2)); if (ady < R && Math.abs(pdx) < R) off = Math.max(off, Math.sqrt(R * R - pdx * pdx) - ady); if (off > best) { best = off; py = y0 + sign * off; gk = 0; } }
        L.ys[s] = py; L.gold[s] = gk; L.cut[s] = cut;
      }
      const ys = smooth(L.ys, k); ctx.lineWidth = L.w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      let run = [], isGold = null; const flush = () => { if (run.length > 1) { ctx.strokeStyle = isGold ? MG : MOSS; ctx.beginPath(); ctx.moveTo(run[0][0], run[0][1]); for (let i = 1; i < run.length; i++) ctx.lineTo(run[i][0], run[i][1]); ctx.stroke(); } };
      for (let s = 0; s <= STEPS; s++) { const px = s * dx, py = ys[s]; if (L.cut[s]) { flush(); run = []; isGold = null; continue; } const g = L.gold[s] && Math.abs(py - y0) > .18 * clearMax ? 1 : 0; if (isGold === null || g === isGold) run.push([px, py]); else { flush(); run = [run[run.length - 1], [px, py]]; } isGold = g; }
      flush();
    }
    if (running && !reduced) requestAnimationFrame(frame);
  }
  hero.addEventListener('pointermove', e => { const b = hero.getBoundingClientRect(); ptr.tx = e.clientX - b.left; ptr.ty = e.clientY - b.top; });
  hero.addEventListener('pointerleave', () => { ptr.tx = -9999; ptr.ty = -9999; });
  addEventListener('resize', () => { resize(); if (reduced) requestAnimationFrame(frame); });
  new IntersectionObserver(es => es.forEach(e => { const was = running; running = e.isIntersecting; if (running && !was) requestAnimationFrame(frame); }), { threshold: 0 }).observe(hero);
  resize(); requestAnimationFrame(frame);

  // The mural: Maine in lines, drawing itself in as it enters.
  const d = JSON.parse(document.getElementById('maine-data').textContent), ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('viewBox', '0 0 720 720');
  d.rows.forEach((row, i) => row.runs.forEach(([a, b]) => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M' + a + ' ' + row.y + ' L' + b + ' ' + row.y); p.setAttribute('stroke', BI); p.setAttribute('stroke-width', row.w); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('fill', 'none'); p.setAttribute('pathLength', '1'); p.style.transitionDelay = (i * 16) + 'ms'; svg.appendChild(p); }));
  const m = document.getElementById('mural'); m.appendChild(svg);
  new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) m.classList.add('on'); }), { threshold: .2 }).observe(m);

  // Creator cards: the lines slide in as each card enters, staggered by column, then settle.
  const covs = [...document.querySelectorAll('.cov')];
  const io = new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; io.unobserve(e.target); const i = covs.indexOf(e.target); setTimeout(() => { e.target.classList.add('on'); setTimeout(() => e.target.classList.remove('on'), 1500); }, (i %% 3) * 90); }), { threshold: .35 });
  covs.forEach(c => io.observe(c));

  // Sections: mark them before they enter, release them as they do.
  document.documentElement.classList.add('js');
  const secs = [...document.querySelectorAll('.reveal')]; secs.forEach(sc => sc.classList.add('pre'));
  const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.remove('pre'); so.unobserve(e.target); } }), { threshold: .18 });
  secs.forEach(sc => so.observe(sc));

  // The signup form has nowhere to go yet. It validates and confirms in the page.
  const f = document.getElementById('signup'), em = document.getElementById('email'), ok = document.getElementById('ok');
  f.addEventListener('submit', ev => { ev.preventDefault(); if (!em.checkValidity()) { em.focus(); em.setAttribute('aria-invalid', 'true'); return; } em.removeAttribute('aria-invalid'); ok.hidden = false; f.querySelector('button').disabled = true; });
})();
</script>
''' % dict(
        lock=logo("lockup-horizontal-reversed", "lk"), two=logo("lockup-two-line-reversed", "lk"), mpi=MPI, mpilower="an initiative of Maine Policy Institute",
        h1=dot("Young Mainers on building a life here"), h2what=dot("Made by the people it is about"), h2cre=dot("The creators"),
        h2news=dot("One story, in full"), h2who=dot("Who is behind it"), h2follow=dot("Follow along"),
        covers=covers, json=json.dumps(rows, separators=(",", ":")))
    css = CSS.replace("{{F800}}", K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2")).replace("{{FINTER}}", K.font64("generation-maine/assets/fonts/inter-var.woff2"))
    head = '<title>Generation Maine</title>\n<meta name="description" content="Short videos and a newsletter by young Maine creators about the rules that shape their lives. An initiative of Maine Policy Institute.">\n<style>%s</style>' % css
    artifact = head + body
    standalone = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">%s</head><body>%s</body></html>' % (head, body)
    write("brand/identity/splash/index.html", standalone)
    write("brand/identity/splash/artifact.html", artifact)


if __name__ == "__main__":
    page()
    print("splash written")
