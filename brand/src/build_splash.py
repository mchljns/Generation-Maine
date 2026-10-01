"""The splash page: one page, the brand's lines as the motion system, the page background changing as you scroll.

Sections: nav with the compact lockup, the hero with the sixteen-line mural as the only lines, about,
the stories (creator-uploaded placeholders), in their words, the newsletter, follow, footer.

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
/* Layout: one column. The page background changes color as sections enter, and every section pairs ink text with a light field. */
:root{
  --sp:#104836;--pine:#0B2B21;--bi:#F4F0E6;--ink:#1E2621;--mg:#EFB443;--sage:#DDE5DA;--moss:#3D6F58;--stone:#5E6A63;--sand:#E8E1D1;--white:#FFFFFF;
  --bg:var(--bi);--fg:var(--ink);--muted:#4F5B55;--rule:rgba(30,38,33,.14);--card:#FFFFFF;
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
.btn{display:inline-block;font:600 15px/1 var(--body);padding:16px 22px;border-radius:6px;text-decoration:none;border:1.5px solid transparent;transition:transform .25s cubic-bezier(.2,.7,.2,1),background .25s}
.btn:hover{transform:translateY(-2px)}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--mg);outline-offset:3px}
.b1{background:var(--bi);color:var(--sp)}.b2{color:var(--bi);border-color:rgba(244,240,230,.55)}.b2:hover{background:rgba(244,240,230,.08)}
.b3{background:var(--sp);color:#F4F0E6}

/* nav: transparent over the hero, a frosted Birch bar once the page scrolls. The active section carries the dot. */
.top{position:fixed;top:0;left:0;right:0;z-index:20;padding-top:env(safe-area-inset-top,0px);color:#F4F0E6;transition:background .35s,color .35s,box-shadow .35s,transform .4s cubic-bezier(.2,.7,.2,1)}
.top.hide{transform:translateY(-110%)}
@media (prefers-reduced-motion: reduce){.top{transition:background .35s,color .35s,box-shadow .35s}}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:24px;height:68px;transition:height .35s}
.top .lk{height:24px;width:auto;display:block}
.top .lk.dark{display:none}
.top nav{display:flex;gap:30px;font:600 14px/1 var(--body);align-items:center}
.top nav a{position:relative;text-decoration:none;opacity:.88;padding:6px 0}
.top nav a:hover{opacity:1}
.top nav a::before{content:"";position:absolute;left:-14px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:var(--mg);transform:scale(0);transition:transform .3s cubic-bezier(.3,1.4,.4,1)}
.top nav a.on{opacity:1}.top nav a.on::before{transform:scale(1)}
.top .cta{font:600 14px/1 var(--body);text-decoration:none;padding:12px 16px;border-radius:6px;border:1.5px solid rgba(244,240,230,.55);transition:background .25s,color .25s,border-color .25s}
.top .cta:hover{background:rgba(244,240,230,.1)}
.top.solid{background:rgba(244,240,230,.94);-webkit-backdrop-filter:blur(18px) saturate(1.1);backdrop-filter:blur(18px) saturate(1.1);color:var(--ink);box-shadow:0 1px 0 var(--rule)}
.top.solid .w{height:60px}
.top.solid .lk.light{display:none}.top.solid .lk.dark{display:block}
.top.solid .cta{background:var(--sp);color:#F4F0E6;border-color:var(--sp)}
/* capsule variant: once scrolled, the bar becomes a floating frosted capsule with a reading-progress line. Switch with #capsule */
html.capsule .top.solid{background:transparent;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none}
html.capsule .top.solid .w{height:52px;max-width:880px;margin:10px auto 0;padding-inline:10px 10px;background:rgba(244,240,230,.9);-webkit-backdrop-filter:blur(18px) saturate(1.1);backdrop-filter:blur(18px) saturate(1.1);border-radius:999px;box-shadow:0 1px 0 var(--rule),0 10px 30px rgba(11,43,33,.12);position:relative;overflow:hidden;gap:16px}
html.capsule .top.solid .w>a:first-child{padding-left:12px}
html.capsule .top.solid .lk{height:20px}
html.capsule .top.solid nav{gap:4px}
html.capsule .top.solid nav a{padding:9px 12px;border-radius:999px;font-size:13px;transition:background .25s}
html.capsule .top.solid nav a:hover{background:rgba(16,72,54,.08)}
html.capsule .top.solid nav a.on{background:var(--sp);color:#F4F0E6}
html.capsule .top.solid nav a::before{display:none}
html.capsule .top.solid .cta{padding:10px 14px;border-radius:999px;font-size:13px}
html.capsule .top.solid .prog{display:block}
.prog{display:none;position:absolute;left:0;bottom:0;height:2px;background:var(--sp);width:0;transition:width .15s linear}
.menu{display:none;font:600 14px/1 var(--body);background:none;border:0;color:inherit;padding:10px 0;cursor:pointer}
.sheet{position:fixed;inset:0;z-index:30;background:var(--sp);color:#F4F0E6;padding:calc(24px + env(safe-area-inset-top,0px)) var(--M) 32px;display:none;flex-direction:column}
.sheet.open{display:flex}
.sheet .bar{display:flex;justify-content:space-between;align-items:center;height:44px}
.sheet .bar .lk{height:24px;width:auto}
.sheet nav{display:flex;flex-direction:column;gap:6px;margin-top:40px}
.sheet nav a{font:800 clamp(38px,11vw,56px)/1.05 var(--display);letter-spacing:-.03em;text-decoration:none;padding:8px 0;opacity:0;transform:translateY(14px);transition:opacity .45s,transform .55s cubic-bezier(.2,.7,.2,1)}
.sheet.open nav a{opacity:1;transform:none}
.sheet.open nav a:nth-child(2){transition-delay:.06s}.sheet.open nav a:nth-child(3){transition-delay:.12s}.sheet.open nav a:nth-child(4){transition-delay:.18s}
.sheet .foot{opacity:0;transition:opacity .4s .25s}.sheet.open .foot{opacity:1}
@media (prefers-reduced-motion: reduce){.sheet nav a,.sheet .foot{opacity:1;transform:none;transition:none}}
.sheet nav a .d{width:.18em;height:.18em}
.sheet .foot{margin-top:auto;display:flex;flex-direction:column;gap:14px}
.sheet .foot a{font:600 16px/1 var(--body);text-decoration:none}
.sheet .foot .cta{align-self:flex-start;background:#F4F0E6;color:var(--sp);padding:16px 22px;border-radius:6px;font:600 15px/1 var(--body);text-decoration:none}
@media (max-width:900px){.top nav,.top .cta{display:none}.menu{display:block}}
.hero{padding-top:68px}

/* hero */
.hero{position:relative;background:var(--sp);color:#F4F0E6;overflow:hidden}
.hero .w{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:32px;padding-block:80px 88px;min-height:620px;align-items:end}
.hero h1{font-size:clamp(46px,8.2vw,112px);max-width:11ch}
.hero .lede{font-size:clamp(19px,1.6vw,23px);line-height:1.5;max-width:38ch;margin:28px 0 30px;color:rgba(244,240,230,.9)}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.mural{position:relative;justify-self:end;width:min(100%,480px);aspect-ratio:1;max-width:100%}
.mural svg{width:100%;height:100%;display:block}
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
section{padding-block:clamp(56px,8vw,112px)}
.h2{font-size:clamp(34px,4.6vw,60px)}
.about .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px}
.about .cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;align-self:end}
.about .cols h3{font:600 15px/1.3 var(--body);letter-spacing:0;margin:0 0 8px;color:var(--fg)}
.about .cols p{margin:0;color:var(--muted);line-height:1.55}
.about .cols div{padding-top:16px;position:relative}.about .cols div::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:var(--fg)}
@media (max-width:900px){.about .w,.news .w{grid-template-columns:1fr}.about .cols{grid-template-columns:1fr}}

.stories-head .head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap}
.stories-head .head p{max-width:46ch;margin:0;color:var(--muted)}
.stories-head{padding-bottom:0}
.stories{padding-top:0}
.stories .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(28px,5vw,72px);align-items:start}
.stage{position:sticky;top:calc(60px + env(safe-area-inset-top,0px) + 28px);align-self:start;height:min(64vh,560px);display:flex;align-items:center}
.vid{position:relative;aspect-ratio:9/16;height:100%;max-height:620px;width:auto;max-width:100%;border-radius:14px;overflow:hidden;background:var(--pine);box-shadow:0 1px 0 var(--rule)}
.vid video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:0;transition:opacity .6s ease}
.vid video.on{opacity:1}
.vid .dur{position:absolute;right:12px;top:12px;font:600 11px/1 var(--body);letter-spacing:.06em;color:#F4F0E6;background:rgba(11,43,33,.55);padding:6px 8px;border-radius:4px;z-index:2}
.vid .idx{position:absolute;left:12px;top:12px;display:flex;gap:4px;z-index:2}
.vid .idx i{display:block;width:14px;height:2px;background:rgba(244,240,230,.45);border-radius:1px;transition:background .3s}.vid .idx i.on{background:#EFB443}
.panels{display:grid;gap:0}
.panel{min-height:min(64vh,560px);display:flex;flex-direction:column;justify-content:center;padding-block:40px;border-top:1.5px solid var(--rule)}
.panel:first-child{border-top:0}
.panel .k{margin-bottom:14px}
.panel h2{font-size:clamp(38px,4.6vw,66px);max-width:10ch}
.panel .say{font:600 clamp(20px,1.7vw,24px)/1.35 var(--body);margin:22px 0 18px;max-width:34ch;color:var(--fg)}
.panel .nm{font:600 15px/1.3 var(--body);margin:0 0 22px}.panel .nm span{font-weight:400;color:var(--muted)}
.panel .go{display:inline-flex;gap:10px;align-items:center;font:600 15px/1 var(--body);text-decoration:none;border-bottom:1.5px solid var(--fg);padding-bottom:6px}
.panel .pv{display:none}
@media (max-width:900px){
  .stories .w{grid-template-columns:1fr}.stage{display:none}
  .panel{min-height:0;padding-block:36px}.panel .pv{display:block;aspect-ratio:9/16;width:min(70vw,300px);border-radius:12px;overflow:hidden;background:var(--pine);margin-bottom:22px}
  .panel .pv video{width:100%;height:100%;object-fit:cover;display:block}
}

.news .w{grid-template-columns:1fr}.about .cols{grid-template-columns:1fr}}

.stories-head .head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap}
.stories-head .head p{max-width:46ch;margin:0;color:var(--muted)}
.stories-head{padding-bottom:0}
.story{padding-block:clamp(28px,4vw,56px)}
.story .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(28px,5vw,72px);align-items:center}
.story.flip .w{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
.story.flip .vid{order:2}
.vid{position:relative;aspect-ratio:9/16;max-height:560px;width:100%;max-width:315px;justify-self:center;border-radius:14px;overflow:hidden;background:var(--pine);box-shadow:0 1px 0 var(--rule)}
.vid video{width:100%;height:100%;object-fit:cover;display:block}
.vid .dur{position:absolute;right:12px;top:12px;font:600 11px/1 var(--body);letter-spacing:.06em;color:#F4F0E6;background:rgba(11,43,33,.55);padding:6px 8px;border-radius:4px}
.story .txt .k{margin-bottom:14px}
.story .txt h2{font-size:clamp(40px,5.2vw,72px);max-width:10ch}
.story .txt .say{font:600 clamp(18px,1.6vw,22px)/1.35 var(--body);margin:22px 0 18px;max-width:34ch;color:var(--fg)}
.story .txt .nm{font:600 15px/1.3 var(--body);margin:0 0 22px}.story .txt .nm span{font-weight:400;color:var(--muted)}
.story .txt .go{display:inline-flex;gap:10px;align-items:center;font:600 15px/1 var(--body);text-decoration:none;border-bottom:1.5px solid var(--fg);padding-bottom:6px}
@media (max-width:900px){.story .w,.story.flip .w{grid-template-columns:1fr}.story.flip .vid{order:0}.vid{justify-self:start;max-width:300px}}

.news .w{grid-template-columns:1fr}.about .cols{grid-template-columns:1fr}}

.creators .head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:36px}
.creators .head p{max-width:46ch;margin:0;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
@media (max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.grid{grid-template-columns:1fr}}
.card{display:block;background:var(--card);color:var(--fg);border-radius:12px;overflow:hidden;text-decoration:none;transform:translateY(0);transition:transform .35s cubic-bezier(.2,.7,.2,1);box-shadow:0 1px 0 var(--rule)}
.card:hover{transform:translateY(-4px)}
.still{position:relative;aspect-ratio:4/5;background:var(--stone);display:flex;flex-direction:column;justify-content:space-between;padding:16px;color:#F4F0E6;isolation:isolate}
.still.t1{background:#6B7A70}.still.t2{background:#7E6F5E}.still.t3{background:#5E6A63}.still.t4{background:#8A7F6A}.still.t5{background:#4E6058}.still.t6{background:#776B63}
.still::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(11,43,33,.55),rgba(11,43,33,0) 55%);z-index:-1}
.still .tag{font:600 11px/1 var(--body);letter-spacing:.06em;text-transform:uppercase;opacity:.9;display:flex;justify-content:space-between}
.still .cap{font:600 clamp(18px,1.6vw,22px)/1.25 var(--body);margin:0;text-wrap:balance;max-width:16ch}
.card .meta{padding:16px 18px 20px}
.card .meta .nm{font:600 14px/1.3 var(--body);margin:0 0 6px}.card .meta .nm span{font-weight:400;color:var(--muted)}
.card .meta h3{font-size:clamp(24px,2vw,30px)}

.news .w{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.news .lede{color:var(--muted);max-width:42ch;margin:18px 0 26px}
.form{display:flex;gap:10px;flex-wrap:wrap;max-width:520px}
.form input{flex:1 1 220px;min-width:0;font:16px var(--body);padding:15px 16px;border-radius:6px;border:1.5px solid var(--rule);background:var(--card);color:var(--fg)}
.form .note{flex-basis:100%;font-size:13px;color:var(--muted);margin:4px 0 0}
.form .ok{flex-basis:100%;font:600 15px var(--body);color:var(--fg);margin:4px 0 0}
.posts{display:grid;gap:0;position:relative}
.post{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.post h3{font-size:clamp(22px,2vw,28px);margin:0 0 8px}
.post p{margin:0;color:var(--muted);font-size:17px}
.post .by{font:600 13px/1.3 var(--body);color:var(--fg);margin-top:10px}.post .by span{font-weight:400;color:var(--muted)}
.post .dt{font:600 13px/1.3 var(--body);color:var(--muted);white-space:nowrap;padding-top:6px}

/* the one Marigold section: what they say, in their words */
.words{color:var(--ink)}
.words .h2 .d{background:var(--ink)}
.words .qs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:40px}
@media (max-width:900px){.words .qs{grid-template-columns:1fr}}
.words blockquote{margin:0;padding-top:18px;position:relative}
.words blockquote::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:var(--ink)}
.words blockquote p{font:800 clamp(22px,2.1vw,30px)/1.1 var(--display);letter-spacing:-.02em;margin:0 0 14px;text-wrap:balance}
.words blockquote footer{font:600 14px/1.3 var(--body)}.words blockquote footer span{font-weight:400;opacity:.75}

.follow .row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media (max-width:760px){.follow .row{grid-template-columns:repeat(2,minmax(0,1fr))}}
.follow a{display:block;padding:22px 0;border-bottom:1.5px solid var(--rule);text-decoration:none}
.follow a b{display:block;font:600 15px/1.3 var(--body)}.follow a span{color:var(--muted);font-size:17px}
.follow .h2{margin-bottom:28px}

.site{background:var(--pine);color:#F4F0E6;padding-block:48px 40px}
.site .w{display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:end}
.site .lk{height:110px;width:auto;display:block}
.site p{margin:0;font-size:14px;color:rgba(244,240,230,.8);max-width:60ch}
.site .fine{margin-top:12px;font-size:13px}
.site .review{margin-top:22px;padding-top:14px;border-top:1px solid rgba(244,240,230,.2)}
.sw{font:600 13px/1 var(--body);color:#F4F0E6;background:none;border:1.5px solid rgba(244,240,230,.4);border-radius:999px;padding:7px 12px;margin-left:6px;cursor:pointer}
.sw.on{background:#F4F0E6;color:var(--sp);border-color:#F4F0E6}
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
    stagevids, panels, idx = "", "", ""
    for i, (tone, town, topic, cap, dur) in enumerate(CARDS):
        stagevids += '<video data-i="%d" data-dur="%s" src="media/creator-%d.webm" muted loop playsinline preload="%s" aria-label="Placeholder clip, %s, %s, Maine"%s></video>' % (
            i, dur, i + 1, "auto" if i < 2 else "metadata", topic, town, ' class="on"' if i == 0 else "")
        idx += '<i%s></i>' % (' class="on"' if i == 0 else "")
        panels += ('<article class="panel reveal" id="story-%d" data-i="%d"><div class="pv"><video src="media/creator-%d.webm" muted loop playsinline preload="metadata"></video></div>'
                   '<p class="k">Story %02d</p><h2>%s</h2><p class="say">"%s"</p><p class="nm">[Creator name] <span>%s, Maine</span></p>'
                   '<a class="go" href="#">Watch the full video [CONFIRM: link]</a></article>') % (i + 1, i, i + 1, i + 1, dot(topic), cap, town)
    body = r"""
<header class="top" id="topbar"><div class="w"><a href="#top" aria-label="Generation Maine, home">%(lock)s%(lock_dark)s</a>
<nav aria-label="Page"><a href="#about" data-for="about">About</a><a href="#creators" data-for="creators">Stories</a><a href="#words" data-for="words">In their words</a><a href="#follow" data-for="follow">Follow</a></nav>
<a class="cta" href="#news">Get the newsletter</a><button class="menu" id="menu" aria-expanded="false" aria-controls="sheet">Menu</button><span class="prog" id="prog" aria-hidden="true"></span></div></header>
<div class="sheet" id="sheet" aria-hidden="true"><div class="bar">%(lock)s<button class="menu" id="close" style="display:block">Close</button></div>
<nav aria-label="Page"><a href="#about">About<i class="d"></i></a><a href="#creators">Stories<i class="d"></i></a><a href="#words">In their words<i class="d"></i></a><a href="#follow">Follow<i class="d"></i></a></nav>
<div class="foot"><a class="cta" href="#news">Get the newsletter</a></div></div>

<section class="hero" id="top"><div class="w">
  <div class="h1"><h1 id="h1" class="rise">%(h1)s</h1>
  <p id="lede" class="lede rise">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay. Told from the towns they live in.</p>
  <p class="ctas rise" id="ctas"><a class="btn b1" href="#creators">Watch the stories</a><a class="btn b2" href="#news">Get the newsletter</a></p></div>
  <div class="mural" id="mural" aria-hidden="true"></div>
</div></section>

<section class="about reveal" id="about" data-bg="var(--bi)"><div class="w">
  <h2 class="h2">%(h2about)s</h2>
  <div class="cols">
    <div class="row-in"><h3>Who makes it</h3><p>Young Mainers with a phone and a story. They pick what to film and say it their own way.</p></div>
    <div class="row-in"><h3>What it is about</h3><p>The rules behind everyday costs. Leases, licenses, permits, wages, and the fine print nobody reads until it costs them.</p></div>
    <div class="row-in"><h3>Where to find it</h3><p>Short videos on TikTok, Instagram and YouTube. The full story, with the numbers, by email.</p></div>
  </div>
</div></section>

<section class="stories-head reveal" id="creators" data-bg="var(--sand)"><div class="w">
  <div class="head"><h2 class="h2">%(h2cre)s</h2><p>One story from each creator, filmed where they live. Names and faces arrive after the shoot. The towns are real.</p></div>
</div></section>
<section class="stories" data-bg="var(--sand)"><div class="w">
  <div class="stage"><div class="vid" id="stage">%(stagevids)s<span class="dur" id="dur">0:52</span><span class="idx" id="idx">%(idx)s</span></div></div>
  <div class="panels">%(panels)s</div>
</div></section>
<section class="words reveal" id="words" data-bg="#EFB443"><div class="w">
  <h2 class="h2">%(h2words)s</h2>
  <div class="qs">
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Belfast, Maine</span></footer></blockquote>
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Machias, Maine</span></footer></blockquote>
    <blockquote class="row-in"><p>"[A sentence from the creator's video, in their words.]"</p><footer>[Creator name] <span>Lewiston, Maine</span></footer></blockquote>
  </div>
</div></section>

<section class="news reveal" id="news" data-bg="var(--bi)"><div class="w">
  <div><h2 class="h2">%(h2news)s</h2><p class="lede">Each story in full, with the numbers behind it. Written by the creator who filmed it. Your address stays with us. [CONFIRM: privacy line]</p>
  <form class="form" id="signup" novalidate><label class="k" for="email" style="flex-basis:100%%">Email</label><input id="email" type="email" name="email" placeholder="you@example.com" autocomplete="email" required><button class="btn b3" type="submit">Subscribe</button>
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
    <a class="row-in" href="#"><b>Instagram</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>TikTok</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>YouTube</b><span>[@handle]</span></a>
    <a class="row-in" href="#"><b>Substack</b><span>[name].substack.com</span></a>
  </div>
</div></section>

<footer class="site"><div class="w">%(two)s<div><p>Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.</p><p class="fine">© 2026 Generation Maine. [CONFIRM: legal name, address and contact]</p><p class="fine review">Mockup review. Nav style: <button type="button" class="sw" id="sw-bar">Bar</button> <button type="button" class="sw" id="sw-cap">Capsule</button></p></div></div></footer>

<script id="maine-data" type="application/json">%(json)s</script>
<script>
(() => {
  const MOSS = '#3D6F58', BI = '#F4F0E6';
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
  const bgs = [...document.querySelectorAll('[data-bg]')];
  const bo = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) document.body.style.background = e.target.dataset.bg; }), { rootMargin: '-45%% 0px -45%% 0px', threshold: 0 });
  bgs.forEach(el => bo.observe(el));

  // The stage: one pinned clip that changes as each story panel reaches the middle of the screen. Phones get a clip per panel.
  const stage = document.getElementById('stage'), stageVids = stage ? [...stage.querySelectorAll('video')] : [], marks = [...document.querySelectorAll('#idx i')], dur = document.getElementById('dur');
  const panelVids = [...document.querySelectorAll('.panel .pv video')];
  const wide = () => matchMedia('(min-width: 901px)').matches;
  function show(i) { stageVids.forEach((v, k) => { const on = k === i; v.classList.toggle('on', on); if (on) { v.play().catch(() => {}); } else v.pause(); }); marks.forEach((m, k) => m.classList.toggle('on', k === i)); if (dur && stageVids[i]) dur.textContent = stageVids[i].dataset.dur; }
  const po = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && wide()) show(+e.target.dataset.i); }), { rootMargin: '-45%% 0px -45%% 0px', threshold: 0 });
  document.querySelectorAll('.panel').forEach(p => po.observe(p));
  if (!reduced && wide()) show(0);
  if (reduced) { stageVids.forEach(v => { v.controls = true; }); panelVids.forEach(v => { v.controls = true; }); }
  else { const mo = new IntersectionObserver(es => es.forEach(e => { if (!wide()) { if (e.isIntersecting) e.target.play().catch(() => {}); else e.target.pause(); } }), { threshold: .4 }); panelVids.forEach(v => mo.observe(v)); }

  // The bar turns solid once the hero scrolls away, marks the section in view, and opens the phone menu.
  const bar = document.getElementById('topbar'), heroEl = document.querySelector('.hero');
  new IntersectionObserver(es => es.forEach(e => bar.classList.toggle('solid', !e.isIntersecting)), { rootMargin: '-68px 0px 0px 0px', threshold: 0 }).observe(heroEl);
  // Two nav styles ship for comparison. #capsule turns the scrolled bar into a floating capsule with a reading-progress line.
  let capsule = location.hash === '#capsule'; try { if (location.hash === '') capsule = localStorage.getItem('gm-nav') === 'capsule'; } catch (e) {}
  const setNav = () => { document.documentElement.classList.toggle('capsule', capsule); document.getElementById('sw-bar').classList.toggle('on', !capsule); document.getElementById('sw-cap').classList.toggle('on', capsule); try { localStorage.setItem('gm-nav', capsule ? 'capsule' : 'bar'); } catch (e) {} };
  setNav(); addEventListener('hashchange', () => { capsule = location.hash === '#capsule'; setNav(); });
  document.getElementById('sw-bar').addEventListener('click', () => { capsule = false; setNav(); scrollTo({ top: document.getElementById('about').offsetTop - 80 }); });
  document.getElementById('sw-cap').addEventListener('click', () => { capsule = true; setNav(); scrollTo({ top: document.getElementById('about').offsetTop - 80 }); });
  const prog = document.getElementById('prog');
  let lastY = scrollY, ticking = false;
  addEventListener('scroll', () => { if (ticking) return; ticking = true; requestAnimationFrame(() => { const y = scrollY, dy = y - lastY; if (y > heroEl.offsetHeight && dy > 6) bar.classList.add('hide'); else if (dy < -6 || y <= heroEl.offsetHeight) bar.classList.remove('hide'); lastY = y; const max = document.documentElement.scrollHeight - innerHeight; if (prog) prog.style.width = (Math.min(1, y / max) * 100).toFixed(1) + '%%'; ticking = false; }); }, { passive: true });
  const links = [...bar.querySelectorAll('nav a')];
  const ao = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(l => l.classList.toggle('on', l.dataset.for === e.target.id)); }), { rootMargin: '-40%% 0px -55%% 0px', threshold: 0 });
  ['about', 'creators', 'words', 'follow'].forEach(id => { const el = document.getElementById(id); if (el) ao.observe(el); });
  const sheet = document.getElementById('sheet'), menu = document.getElementById('menu');
  const setMenu = o => { sheet.classList.toggle('open', o); sheet.setAttribute('aria-hidden', String(!o)); menu.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; };
  menu.addEventListener('click', () => setMenu(true)); document.getElementById('close').addEventListener('click', () => setMenu(false));
  sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

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
""" % dict(
        lock=logo("lockup-compact-reversed", "lk light"), lock_dark=logo("lockup-compact", "lk dark"), two=logo("lockup-two-line-reversed", "lk"),
        h1=dot("Young Mainers on building a life here"), h2about=dot("Made by the people it is about"), h2cre=dot("The stories"),
        h2words=dot("In their words"), h2news=dot("The full story, by email"), h2follow=dot("Follow along"),
        stagevids=stagevids, panels=panels, idx=idx, json=json.dumps(rows, separators=(",", ":")))
    css = CSS.replace("{{F800}}", K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2")).replace("{{FINTER}}", K.font64("generation-maine/assets/fonts/inter-var.woff2")).replace("{{FDM}}", K.font64("generation-maine/assets/fonts/dm-sans-var.ttf"))
    head = '<title>Generation Maine</title>\n<meta name="description" content="Young Mainers film the rules that shape their lives. Short videos and a newsletter, made in Maine.">\n<style>%s</style>' % css
    artifact = head + body
    standalone = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">%s</head><body>%s</body></html>' % (head, body)
    write("brand/identity/splash/index.html", standalone)
    write("brand/identity/splash/artifact.html", artifact)


if __name__ == "__main__":
    page()
    print("splash written")
