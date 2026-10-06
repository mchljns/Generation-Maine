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
MG = "#FAC800"   # Maine Policy's gold
MPI_NAVY, MPI_BLUE = "#0F2E4D", "#0556A5"

SITE_CSS = lambda css: "\n".join(l for l in css.splitlines() if ".site" in l)

LEAN_A = dict(
    key="v2-a", out="brand/identity/splash-lean-a", root_class="static lean", navy="#0F2E4D", blue="#0556A5", ink="#0F2E4D", paper="#FFFFFF", tint="#EAF1F8",
    fonts=S.SIGNATURE_FONTS, font_files={}, logo=F.LOGO_A, mural=F.MURAL_A, hero="mural", credits="",
    display="'Bricolage Grotesque',system-ui,sans-serif", body="'DM Sans',system-ui,sans-serif", label="'DM Sans',system-ui,sans-serif",
    h1="Young Mainers<br>on building<br>a life <em>here<i class=\"d pulse\" aria-hidden=\"true\"></i></em>", h2_about="What this is", h2_creators="The creators", h2_follow="Where to find it",
    site_css=SITE_CSS(F.STATIC_CSS) + "\n" + SITE_CSS(F.FAMILY_A_CSS % dict(blue="#0556A5", navy="#0F2E4D", mg=MG)),
    css="""
.lean h1,.lean h2,.lean .h2{font-family:var(--display);font-weight:800;letter-spacing:-.01em}
.lean h1 em{font-style:normal;color:var(--mg)}
.lean h1 .d{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--mg);margin-left:.05em;vertical-align:baseline;position:relative}
.lean h1 .d::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background:var(--mg);opacity:0;animation:pulse 2.4s cubic-bezier(.2,.6,.3,1) infinite 1.4s}
@keyframes pulse{0%{transform:scale(1);opacity:.6}65%{transform:scale(3);opacity:0}100%{transform:scale(3);opacity:0}}
@media (prefers-reduced-motion: reduce){.lean h1 .d::after{animation:none}}
.lean .col b{font-family:var(--body);font-weight:700}
.lean .hero .k{color:#fff}
.site .flegal .ph{color:rgba(255,255,255,.75)}
""")

LEAN_B = dict(
    key="v2-b", out="brand/identity/splash-lean-b", root_class="bs static lean", navy=MPI_NAVY, blue=MPI_BLUE, ink=MPI_NAVY, paper="#FFFFFF", tint="#EAF1F8",
    fonts=B.FONTS, font_files=B.BARK_SKY["font_files"], logo=F.LOGO_B, mural=None, hero="video", credits="",
    display="'Hedvig Letters Serif',Georgia,serif", body="'Hedvig Letters Sans',system-ui,sans-serif", label="'Hedvig Letters Sans',system-ui,sans-serif",
    h1="young mainers<br>on building<br>a life here", h2_about="what this is", h2_creators="the creators", h2_follow="where to find it",
    site_css=SITE_CSS(F.STATIC_CSS) + "\n" + SITE_CSS(F.FAMILY_B["css"]),
    css="""
:root{--bark:#0F2E4D;--sky:#fff}
.lean h1,.lean h2,.lean .h2{font-family:var(--display);font-weight:400;letter-spacing:-.015em}
.lean .col b{font-family:var(--body);font-weight:400}
.lean .hero{color:#fff}
.site .flegal .ph{color:rgba(255,255,255,.75)}
.bs.static .site .lk{height:124px}@media (max-width:900px){.bs.static .site .lk{height:104px}}
.lean .hero .bg{position:absolute;inset:0;overflow:hidden;background:var(--navy)}
.lean .hero .bg video{width:100%;height:100%;object-fit:cover;display:block}
.lean .hero .bg .plates{display:none;position:absolute;inset:0;overflow:hidden}
.lean .hero .bg .plate{position:absolute;inset:-6%;width:112%;height:112%;object-fit:cover;opacity:0;animation:plate 26s linear infinite}
.lean .hero .bg .p1{animation-delay:0s}.lean .hero .bg .p2{animation-delay:5.2s}.lean .hero .bg .p3{animation-delay:10.4s}.lean .hero .bg .p4{animation-delay:15.6s}.lean .hero .bg .p5{animation-delay:20.8s}
.lean .hero .bg .p2,.lean .hero .bg .p4{animation-name:plate-r}
@keyframes plate{0%{opacity:0;transform:translateX(-1.5%) scale(1)}5%{opacity:1}20%{opacity:1}25%{opacity:0;transform:translateX(1.5%) scale(1.05)}100%{opacity:0;transform:translateX(1.5%) scale(1.05)}}
@keyframes plate-r{0%{opacity:0;transform:translateX(1.5%) scale(1.05)}5%{opacity:1}20%{opacity:1}25%{opacity:0;transform:translateX(-1.5%) scale(1)}100%{opacity:0;transform:translateX(-1.5%) scale(1)}}
.lean .hero.plates-on .bg video{display:none}.lean .hero.plates-on .bg .plates{display:block}
.lean .hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,46,77,.78) 0%,rgba(15,46,77,.55) 45%,rgba(15,46,77,.18) 100%)}
.lean .hero .credit{position:absolute;right:var(--M);bottom:14px;margin:0;font-size:13px;color:rgba(255,255,255,.72);max-width:46ch;text-align:right}
.lean .hero .lede{color:rgba(255,255,255,.92)}
@media (prefers-reduced-motion: reduce){.lean .hero .bg video,.lean .hero .bg .plates{display:none!important}.lean .hero .bg{background:url(media/hero-poster.jpg) center/cover no-repeat}}
@media (max-width:900px){
/* phones: the picture fills the first screen and the words sit in its lower third over a gradient that rises from the bottom */
.lean .hero{min-height:calc(100svh - 68px);align-items:end;padding-block:0 40px}
.lean .hero .bg::after{background:linear-gradient(180deg,rgba(15,46,77,0) 0%,rgba(15,46,77,.12) 35%,rgba(15,46,77,.72) 62%,rgba(15,46,77,.94) 100%)}
.lean .hero .k{font-size:12px;letter-spacing:.08em;margin-bottom:14px}
.lean .hero h1{font-size:clamp(40px,11.5vw,48px);margin-bottom:16px}
.lean .hero .lede{font-size:16px;max-width:none}
.lean .hero .ctas{margin-top:22px}
}
""")

def stepper_css():
    """The pinned stepper's rules from the original splash, from the section rule to the end of its phone block."""
    a = S.CSS.index(".stories{overflow-x:clip")
    b = S.CSS.index(".panel .bio{font-size:16px", a)
    b = S.CSS.index("\n}", b) + 2
    return S.CSS[a:b]


STEPPER_OVERRIDES = """
:root{--rule:rgba(15,46,77,.18);--fg:var(--ink);--muted:rgba(15,46,77,.7);--bi:var(--tint)}
.stories-head{padding-bottom:0!important}
.stories{padding-top:48px}
.stories{background:var(--tint)}
.stories .w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
.vid,.vid video,.vid img.clip{border-radius:0}.vid{box-shadow:none;background:var(--navy)}
.vid .dur{border-radius:0;background:rgba(17,35,55,.6)}
.who span{text-shadow:0 1px 2px rgba(0,0,0,.45)}
.panel .k{color:var(--blue)}
.where{color:var(--muted)}.where .n{color:var(--ink)}
.where .segs button::before{background:rgba(15,46,77,.2);border-radius:0}.where .segs button.on::before,.where .segs button.done::before{background:var(--navy)}
.soc a{color:var(--ink)}.soc .ic{color:var(--blue)}
@media (max-width:900px){
.stories .pinw{top:calc(84px + env(safe-area-inset-top,0px))}
/* phones: the position row stands on its side along the left of the clip, so the clip and the creator's details share one screen */
.stories .w{display:grid;grid-template-columns:40px minmax(0,1fr);grid-template-rows:auto auto;gap:14px 12px;align-items:stretch}
.where{grid-column:1;grid-row:1;order:0;margin:0;flex-direction:column;align-items:center;gap:12px;height:var(--stageh,52vh)}
.where .n{writing-mode:vertical-rl;transform:rotate(180deg);min-width:0;line-height:1}
.where .segs{flex-direction:column;flex:1;width:40px;gap:4px}
.where .segs button{flex:1;width:40px;height:auto}
.where .segs button::before{left:19px;right:auto;top:0;bottom:0;width:2px;height:auto}
.where .segs button:hover::before{transform:scaleX(1.5)}
.where .next{display:none}
.stage{grid-column:2;grid-row:1;order:1;justify-content:flex-start}
.panels{grid-column:1/-1;grid-row:2;order:2}
}
"""

GOAL = ("Generation Maine wants young people in Maine to see the rules behind what their lives cost, and to say so in public. "
        "Young Mainers film where they live. Each clip takes one rule, a lease clause, a license fee, a permit, a line on a pay stub, "
        "and shows what it says and what it costs. The clips go out on the creators' own accounts, where their friends already are. "
        "The newsletter follows the paperwork behind each one, with the numbers. The more people see the same rule from different towns, "
        "the harder it gets to ignore.")
FOLLOW = [("instagram", "Instagram", "[@handle]", "#follow"),
          ("tiktok", "TikTok", "[@handle]", "#follow"),
          ("youtube", "YouTube", "[@handle]", "#follow"),
          ("substack", "Substack", "[name].substack.com", "https://CONFIRM-publication.substack.com/")]


def bars():
    """Three slanted bars, the last in gold: the family's mark, at label size, before a kicker."""
    return ('<svg class="bars" viewBox="0 0 30 12" aria-hidden="true"><path d="M4 12 L8 0 h5 L9 12z" fill="currentColor"/>'
            '<path d="M12 12 L16 0 h5 L17 12z" fill="currentColor"/><path d="M20 12 L24 0 h5 L25 12z" class="g"/></svg>')


def utm(href):
    """Outbound links carry a source so the newsletter and the accounts can see what the page sends them."""
    if not href.startswith("http"):
        return href
    return href + ("&" if "?" in href else "?") + UTM


PHONE_SITE = """
@media (max-width:900px){
.static .site .fsocial{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}
.static .site .fsocial a{display:flex;align-items:center;min-height:48px;padding:0;border-top:1px solid rgba(255,255,255,.14);gap:12px;font-size:15px}
.static .site .fsocial .ic{width:22px;height:22px}
}
"""

CSS = r"""
{{FONTS}}
:root{color-scheme:light;--navy:%(navy)s;--blue:%(blue)s;--mg:#FAC800;--ink:%(ink)s;--paper:%(paper)s;--tint:%(tint)s;--pine:%(navy)s;--snow:#fff;--display:%(display)s;--body:%(body)s;--M:60px;--ctl:48px}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;scroll-behavior:smooth;scroll-padding-top:68px}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 var(--body);-webkit-font-smoothing:antialiased}
img,svg,video{max-width:100%%}
a{color:inherit}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--mg);outline-offset:3px}
.skip{position:absolute;left:var(--M);top:-60px;z-index:50;background:var(--mg);color:var(--navy);padding:0 16px;height:var(--ctl);line-height:var(--ctl);font:600 13px/var(--ctl) var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none}
.skip:focus{top:8px}
.w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
.k{font:600 13px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;display:inline-flex;align-items:center;gap:10px}
.bars{width:30px;height:12px;flex:none;margin-right:10px;vertical-align:-1px;color:#fff}.about .bars{color:var(--blue)}.bars .g{fill:var(--mg)}
.k{display:inline-flex}.hero .k,.about .aim .k,.follow .nl .k{display:flex}
.lede{font-size:19px;line-height:1.55;margin:0}
h2,.h2{font-size:clamp(34px,4vw,52px);line-height:1.05;margin:0}
.btn,.tl{display:inline-flex;align-items:center;justify-content:center;height:var(--ctl);padding:0 24px;font:600 13px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;border:1px solid transparent;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.btn.b1{background:var(--mg);color:var(--navy);border-color:var(--mg)}.btn.b1:hover{background:#FFD633;border-color:#FFD633}
.btn.b2{background:transparent;color:inherit;border-color:currentColor}.btn.b2:hover{background:var(--mg);color:var(--navy);border-color:var(--mg)}
.tl{padding:0 4px;text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1.5px}
/* the bar: one height, one state */
.top{position:sticky;top:0;z-index:20;background:var(--navy);color:#fff;box-shadow:0 1px 0 rgba(255,255,255,.12)}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:24px;height:68px}
.top .lk{height:32px;width:auto;display:block}
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
.hero h1{font-size:clamp(44px,6.2vw,84px);line-height:1;margin:0 0 24px}
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
.about .body{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:stretch}
.about .media{display:grid;grid-template-rows:auto auto;gap:10px}
.about .media .ph{position:relative;overflow:hidden;background:var(--tint);aspect-ratio:3/4}
.about .media .ph img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;display:block}
.about .media .cap{margin:0;font-size:13px;color:rgba(15,46,77,.7)}
.about .towns{background:var(--navy);color:#fff;padding:32px 28px;display:grid;align-content:start;gap:22px}
.about .towns .k{color:var(--mg)}
.about .towns ul{list-style:none;margin:0;padding:0;columns:2;column-gap:24px}
.about .towns li{font-family:var(--display);font-size:clamp(22px,2vw,28px);line-height:1.25;break-inside:avoid;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.about .body{grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:56px;align-items:center}
.about .aim .k{display:block;color:var(--blue);margin-bottom:20px}
.about .aim .big{font-family:var(--display);font-size:clamp(28px,3vw,42px);line-height:1.18;margin:0;max-width:20ch}
.about .aim .note{margin:14px 0 0;font-size:13px;color:rgba(15,46,77,.6)}
.about .goal{margin:28px 0 0;padding-top:24px;border-top:1px solid var(--navy);font-size:17px;line-height:1.65;max-width:58ch}
/* the cast: nine faces, the name under each, the town and the handle */
.roster{background:var(--tint)}
.roster .grid{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:16px 10px}
.roster .tile{display:grid;gap:12px;text-decoration:none;color:inherit;align-content:start}
.roster .tile .ph{aspect-ratio:4/5;background:var(--navy);overflow:hidden;position:relative}
.roster .tile .ph img{width:100%%;height:100%%;object-fit:cover;display:block;filter:saturate(.92)}
.roster .tile .who{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;border-top:1px solid var(--navy);padding-top:10px;align-items:baseline}
.roster .tile .who .n{font:600 13px/1 var(--label);letter-spacing:.1em;color:var(--blue)}
.roster .tile .who .town{grid-column:2}
.roster .tile b{font-size:17px;line-height:1.2;font-weight:700;font-family:var(--body)}
.roster .tile .town{font-size:13px;line-height:1.3;color:rgba(15,46,77,.7)}
a.roster-tile:hover .who{border-top-color:var(--blue)}a.roster-tile:hover b{color:var(--blue)}
/* where to find it: three feeds as an editorial list, then the newsletter band */
.follow{background:var(--navy);color:#fff}
.follow .list{border-top:1px solid rgba(255,255,255,.22)}
.follow .row{display:grid;grid-template-columns:48px 1fr auto;gap:0 24px;align-items:center;padding:26px 0;border-bottom:1px solid rgba(255,255,255,.22);text-decoration:none;color:inherit}
.follow .row .ic{width:28px;height:28px;color:var(--mg)}
.follow .row .name{font-family:var(--display);font-size:clamp(26px,2.6vw,34px);line-height:1;transition:color .2s}
.follow .row .h{font:600 13px/1 var(--label);letter-spacing:.06em;color:var(--mg);white-space:nowrap;justify-self:end}
a.row:hover .name{color:var(--mg)}
.follow .nl{margin-top:72px;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:center;padding:48px 0 0;border-top:1px solid var(--mg)}
.follow .nl .k{display:block;color:var(--mg);margin-bottom:16px}
.follow .nl h3{font-family:var(--display);font-size:clamp(30px,3.2vw,44px);line-height:1.05;margin:0}
.follow .nl .lede{color:rgba(255,255,255,.85);font-size:17px;max-width:40ch}
.follow form{display:grid;grid-template-columns:1fr auto;gap:12px}
.follow input{height:var(--ctl);border:1px solid rgba(255,255,255,.4);background:#fff;color:var(--ink);padding:0 16px;font:16px var(--body);width:100%%}
.follow input:focus-visible{outline-color:var(--mg)}
.follow .fine{grid-column:1/-1;margin:8px 0 0;font-size:13px;color:rgba(255,255,255,.65)}
.follow .fine a{color:inherit}
/* responsive */
@media (max-width:1100px){.roster .grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (max-width:700px){.roster .grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px 10px}.roster .tile b{font-size:15px}}
@media (max-width:900px){
 :root{--M:20px}
 body{font-size:16px}
 .top nav,.top .cta{display:none}.top .menu{display:block}
 .sheet{display:block;position:fixed;inset:68px 0 0 0;background:var(--navy);color:#fff;z-index:19;padding:24px var(--M);transform:translateY(-8px);opacity:0;pointer-events:none;transition:opacity .2s,transform .25s}
 .sheet.open{opacity:1;transform:none;pointer-events:auto}
 .sheet nav{display:grid;gap:6px}.sheet nav a{font:600 15px/1 var(--label);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:#fff;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.12)}
 .sheet .btn{margin-top:20px;width:100%%}
 .hero{padding-block:32px 48px;min-height:0}
 .hero .mural path{transition-duration:1.1s}
 .follow.block{padding-bottom:40px}
 .static .site{padding-block:36px 24px}
 /* tap targets: 44 pt tall where a finger lands; the visual stays the same */
 .top .w>a:first-child{display:flex;align-items:center;min-height:44px}
 .static .site .flinks{gap:0 20px}.static .site .flinks a{display:inline-flex;align-items:center;min-height:44px;padding:0}
 .static .site .fsocial{gap:0 18px}.static .site .fsocial a{min-height:44px;padding:0}
 .static .site .fpartners a,.static .site .plist a{display:inline-flex;align-items:center;min-height:44px;margin:0 18px 0 0}
 .static .site .plist a{display:flex;margin:0}
 .static .site .flegal a,.static .site .flegal .ph{display:inline-flex;align-items:center;min-height:44px}
 .static .site .ffine{gap:0}.static .site .fpartners{gap:0}
 /* social links on phones: labeled chips, 44 pt tall, a thumb's width apart */
 .stories .soc{gap:10px;margin-top:4px}
 .stories .soc a{min-height:44px;padding:0 14px 0 12px;border:1px solid rgba(15,46,77,.3);gap:9px;font-size:13px;font-weight:600;letter-spacing:.02em}
 .stories .soc a span{display:none}
 .stories .soc a::after{content:attr(aria-label)}
 .stories .soc .ic{width:20px;height:20px}

 .hero .w{grid-template-columns:1fr;gap:28px}
 .hero .mural{order:-1;width:min(56vw,300px);justify-self:start}
 .hero h1{max-width:none}
 section.block{padding-block:56px}
 .block .head{grid-template-columns:1fr;gap:16px;margin-bottom:32px}
 .about .cols{grid-template-columns:1fr;gap:28px}
 .about .body{grid-template-columns:1fr;gap:28px}.about .media .ph{aspect-ratio:4/3}.about .goal{margin-top:24px}
 .follow .row{grid-template-columns:36px 1fr;gap:4px 16px;padding:20px 0}.follow .row .ic{width:24px;height:24px;grid-row:1/3}.follow .row .h{grid-column:2;justify-self:start;margin-top:4px}
 .follow .nl{grid-template-columns:1fr;gap:24px;margin-top:48px;padding-top:36px}
 .follow form{grid-template-columns:1fr}
}
%(stepper_css)s
%(site_css)s
%(css)s
%(phone_site)s
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
    <span class="k rise" id="k">%(bars)sA Maine Policy Institute project</span>
    <h1 class="rise" id="h1">%(h1)s</h1>
    <p class="lede rise" id="lede">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay. Told from the towns they live in.</p>
    <div class="ctas rise" id="ctas"><a class="btn b1" href="#follow">Follow along</a></div>
  </div>
  %(hero_side)s
</div>%(hero_credit)s</section>

<section class="block about" id="about"><div class="w">
  <div class="body">%(about_media)s<div class="aim"><span class="k">%(bars)sWhat we hope to achieve</span><p class="big">Everyone who leaves Maine has a reason. We want the people who stay to show what it costs, one rule at a time.</p><p class="note">[CONFIRM: the aim, in Maine Policy Institute's words. This is a draft to edit.]</p><p class="goal">%(cols)s</p></div></div>
</div></section>

<section class="block roster stories-head" id="creators"><div class="w">
  <div class="head" style="margin-bottom:0"><h2>%(h2_creators)s</h2></div>
</div></section>
%(stepper)s

<section class="block follow" id="follow"><div class="w">
  <div class="head"><h2>%(h2_follow)s</h2><p class="lede">Nothing is published on this page. The clips live on the feeds. The paperwork lives in the newsletter.</p></div>
  %(follow)s
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
    d.lines.forEach(([x0, y0, x1, y1, w, c], i) => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M' + x0 + ' ' + y0 + ' L' + x1 + ' ' + y1); p.setAttribute('stroke', c || '#FFFFFF'); p.setAttribute('stroke-width', w); p.setAttribute('fill', 'none'); p.setAttribute('pathLength', '1'); p.style.transitionDelay = (i * (matchMedia('(max-width: 900px)').matches ? 35 : (d.stagger || 35))) + 'ms'; g.appendChild(p); });
    m.appendChild(svg); requestAnimationFrame(() => requestAnimationFrame(() => m.classList.add('on')));
  }
  // The stage: one pinned clip that changes as each story panel reaches the middle of the screen.
  const stage = document.getElementById('stage'), stageVids = stage ? [...stage.querySelectorAll('video, img.clip')] : [], whos = stage ? [...stage.querySelectorAll('.who')] : [], marks = [...document.querySelectorAll('#segs button')], dur = document.getElementById('dur'), wn = document.getElementById('wn'), wnext = document.getElementById('wnext');
  const panels = [...document.querySelectorAll('.panel')], storiesEl = document.getElementById('stories'); let cur = -1;
  function show(i) { if (i === cur) return; const back = i < cur; panels.forEach((p, k) => { p.classList.toggle('on', k === i); p.classList.toggle('prev', back ? k > i : k < i); }); cur = i;
    stageVids.forEach((v, k) => { const on = k === i; v.classList.toggle('on', on); if (!v.play) return; if (on) { v.play().catch(() => {}); } else v.pause(); }); whos.forEach((w, k) => w.classList.toggle('on', k === i)); marks.forEach((m, k) => { m.classList.toggle('on', k === i); m.classList.toggle('done', k < i); }); if (dur && stageVids[i]) dur.textContent = stageVids[i].dataset.dur;
    wn.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(panels.length).padStart(2, '0'); const nx = marks[i + 1]; wnext.textContent = nx ? 'Next: ' + nx.dataset.name : 'Last one'; }
  const panelsEl = document.getElementById('panels'), stageEl = document.querySelector('.stage');
  const fit = () => { if (matchMedia('(min-width: 901px)').matches) { panelsEl.style.height = ''; stageEl.style.removeProperty('--stageh'); return; } let h = 0; panels.forEach(p => { h = Math.max(h, p.scrollHeight); }); panelsEl.style.height = (h + 6) + 'px';
    const top = 84 + 16, room = innerHeight - top - (h + 6) - 14 - 20, colw = stageEl.clientWidth || (innerWidth - 72);
    const sh = Math.round(Math.max(240, Math.min(colw * 16 / 9, room))); stageEl.style.setProperty('--stageh', sh + 'px'); document.querySelector('.where').style.height = sh + 'px'; };
  const step = () => { const total = storiesEl.offsetHeight - innerHeight; const t = Math.min(1, Math.max(0, (scrollY - storiesEl.offsetTop) / total)); show(Math.min(panels.length - 1, Math.floor(t * panels.length))); };
  fit(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { fit(); step(); }); addEventListener('load', fit);
  marks.forEach((m, k) => m.addEventListener('click', () => { const total = storiesEl.offsetHeight - innerHeight; scrollTo({ top: storiesEl.offsetTop + (k + .5) / panels.length * total }); }));
  addEventListener('scroll', step, { passive: true }); addEventListener('resize', () => { fit(); step(); }); step(); if (cur < 0) show(0);
  if (reduced) stageVids.forEach(v => { if (v.play) v.controls = true; });
  // the hero loop: where WebM cannot play, the five plates drift and dissolve in CSS instead
  const hv = document.querySelector('.hero .bg video');
  if (hv) { const ok = hv.canPlayType('video/webm; codecs="vp9"') || hv.canPlayType('video/webm'); if (!ok) document.querySelector('.hero').classList.add('plates-on'); else { hv.play().catch(() => document.querySelector('.hero').classList.add('plates-on')); } }
  // the footer mark draws once the page is scrolled to its end
  const site = document.querySelector('.site');
  const fire = () => { site.classList.add('on'); removeEventListener('scroll', atEnd); };
  const atEnd = () => { if (innerHeight + scrollY >= document.documentElement.scrollHeight - 24) fire(); };
  addEventListener('scroll', atEnd, { passive: true }); atEnd();
  new IntersectionObserver(es => es.forEach(e => { if (e.intersectionRatio >= .95) fire(); }), { threshold: [.95, 1] }).observe(site.querySelector('.lk'));
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
    return GOAL


ABOUT_PHOTO = ("lewiston-3.jpg", "Lisbon Street, Lewiston, Maine", "Lisbon Street, Lewiston. Photograph: David Wilson, CC BY 2.0")


def about_media(theme):
    return '<figure class="media" style="margin:0"><div class="ph"><img src="media/about.jpg" alt="%s" width="1200" height="1600" loading="lazy"></div></figure>' % ABOUT_PHOTO[1]


def tiles_html():
    """The cast: one tile per creator, the face above the name. Placeholder names and portraits until the shoot; the handle
    links out once the account exists, so a tile is a plain block until then."""
    out = []
    for i, c in enumerate(S.CREATORS):
        inner = ('<span class="ph"><img src="media/portrait-%d.jpg" alt="" width="300" height="400"></span>'
                 '<span class="who"><span class="n">%02d</span><b>%s</b><span class="town">%s, Maine</span></span>' % (i + 1, i + 1, c["name"], c["town"]))
        # the tile links to the creator's feed once the account exists; until then it is a plain block
        out.append('<div class="tile" data-handle="%s" aria-label="%s, %s, Maine">%s</div>' % (c["handle"], c["name"], c["town"], inner))
    return "".join(out)


def stepper_html():
    """The pinned clip stepper from the first preview: one clip on the stage, the creator's details beside it, the position row."""
    stagevids, panels, idx, whos = "", "", "", ""
    for i, (tone, town, topic, cap, dur) in enumerate(S.CARDS):
        cr = S.CREATORS[i]
        clip = cr.get("clip", "creator-%d.webm" % (i + 1))
        if clip.endswith((".gif", ".png", ".jpg", ".webp")):
            stagevids += '<img class="clip%s" data-i="%d" data-dur="%s" src="media/%s" alt="" loading="%s">' % (' on' if i == 0 else '', i, dur, clip, "eager" if i < 2 else "lazy")
        else:
            stagevids += '<video data-i="%d" data-dur="%s" src="media/%s" muted loop playsinline preload="%s" aria-label="Placeholder clip, %s, %s, Maine"%s></video>' % (i, dur, clip, "auto" if i < 2 else "metadata", topic, town, ' class="on"' if i == 0 else "")
        who = '<div class="who%s">%s<span><b>%s</b>%s</span></div>' % (' on' if i == 0 else '', S.avatar(), cr["handle"], cr["name"])
        whos += who
        idx += '<button type="button" aria-label="Creator %d, %s, %s" data-name="%s"%s></button>' % (i + 1, cr["name"], town, cr["name"], ' class="on"' if i == 0 else "")
        socials = ''.join('<a href="#follow" aria-label="%s">%s<span>%s</span></a>' % (lbl, S.icon(n), cr["handle"]) for n, lbl in (("instagram", "Instagram"), ("tiktok", "TikTok"), ("youtube", "YouTube")))
        panels += ('<article class="panel%s" id="story-%d" data-i="%d"><div class="pv">%s</div><p class="k">%s, Maine</p><h2>%s</h2><p class="bio">%s</p><div class="soc">%s</div></article>'
                   % (" on" if i == 0 else "", i + 1, i, who, town, cr["name"], cr["bio"], socials))
    return ('<section class="stories" id="stories"><div class="pinw"><div class="w">'
            '<div class="stage"><div class="vid" id="stage">%s%s<span class="dur" id="dur">0:52</span></div></div>'
            '<div class="panels" id="panels">%s</div>'
            '<div class="where" id="where"><span class="n" id="wn">01 / 09</span><span class="segs" id="segs">%s</span><span class="next" id="wnext"></span></div>'
            '</div></div></section>' % (stagevids, whos, panels, idx))


def follow_html():
    rows = []
    for key, name, handle, href in FOLLOW:
        rows.append('<a class="row" href="%s" rel="noopener"%s>%s<span class="name">%s</span><span class="h">%s</span></a>'
                    % (utm(href), ' target="_blank"' if href.startswith("http") else "", S.icon(key), name, handle))
    nl = ('<div class="nl" id="newsletter"><div><span class="k">' + bars() + 'Newsletter</span><h3>The paperwork behind each clip, by email.</h3></div>'
          '<form id="nl" action="%s" method="get" target="_blank" rel="noopener"><label for="em" style="position:absolute;left:-9999px">Email</label>'
          '<input id="em" name="email" type="email" placeholder="you@example.com" autocomplete="email" required inputmode="email"><button class="btn b1" type="submit">Sign up</button>'
          '<p class="fine">Runs on Substack. Unsubscribe in one click. [CONFIRM: publication address]</p></form></div>' % utm("https://CONFIRM-publication.substack.com/subscribe"))
    return '<div class="list">%s</div>%s' % ("".join(rows), nl)


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
    css = (CSS % dict(theme, site_css=theme["site_css"], stepper_css=stepper_css() + STEPPER_OVERRIDES, phone_site=PHONE_SITE))
    css = css.replace("{{FONTS}}", theme["fonts"]).replace("{{F800}}", K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2")).replace("{{FINTER}}", K.font64("brand/fonts/inter-var.woff2")).replace("{{FDM}}", K.font64("generation-maine/assets/fonts/dm-sans-var.ttf"))
    for k, v in theme["font_files"].items():
        css = css.replace("{{%s}}" % k, K.font64(v))
    if theme["hero"] == "video":
        plates = "".join('<img class="plate p%d" src="media/plate-%d.jpg" alt="" width="1600" height="900" loading="lazy">' % (i, i) for i in range(1, 6))
        hero_bg = '<div class="bg" aria-hidden="true"><video autoplay muted loop playsinline preload="metadata" poster="media/hero-poster.jpg"><source src="media/hero.webm" type="video/webm"></video><div class="plates">%s</div></div>' % plates
        hero_side = ""
        hero_credit = ""   # placeholder footage; credits for the sources stay in brand/content/photos/CREDITS.md
        # the loop and its poster: the lighter render if present, else the one the family page uses
        fam = os.path.join(ROOT, "brand", "identity", "splash-family-b", "media")
        from PIL import Image
        for i in range(1, 6):
            Image.open(os.path.join(ROOT, "brand", "content", "photos", "hero-frames", "scene-%d.jpg" % i)).convert("RGB").resize((1600, 900), Image.LANCZOS).save(os.path.join(ROOT, out_dir, "media", "plate-%d.jpg" % i), quality=80)
        for f in ("hero.webm", "hero-poster.jpg"):
            dst = os.path.join(ROOT, out_dir, "media", f)
            if not os.path.exists(dst):
                shutil.copy(os.path.join(fam, f), dst)
    else:
        hero_bg = ""
        hero_side = '<div class="mural" id="mural" aria-hidden="true"></div>'
        hero_credit = ""
    fam_b = os.path.join(ROOT, "brand", "identity", "splash-family-b", "media")
    for i in range(1, 10):
        shutil.copy(os.path.join(fam_b, "portrait-%d.jpg" % i), os.path.join(ROOT, out_dir, "media", "portrait-%d.jpg" % i))
        shutil.copy(os.path.join(fam_b, "creator-%d.gif" % i), os.path.join(ROOT, out_dir, "media", "creator-%d.gif" % i))
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "brand", "content", "photos", "commons", ABOUT_PHOTO[0])).convert("RGB")
    w, h = im.size; tw = int(h * 3 / 4); x0 = (w - tw) // 2 + int(w * 0.04)   # a 3 by 4 crop, a touch right of center, toward the street
    im.crop((x0, 0, x0 + tw, h)).resize((1200, 1600), Image.LANCZOS).save(os.path.join(ROOT, out_dir, "media", "about.jpg"), quality=84)
    footer = F.family_footer(S.draw_paths(S.logo("lockup-two-line-reversed", "lk", theme["logo"])), dict(credits=theme["credits"]))
    footer = footer.replace('href="#signup"', 'href="#newsletter"')
    footer = footer.replace('<a href="#" aria-label=', '<a href="#follow" aria-label=')
    footer = footer.replace('<a href="#">Privacy</a>', '<span class="ph" title="[CONFIRM: privacy policy page]">Privacy</span>')
    footer = footer.replace('<a href="#">Contact</a>', '<a href="%s" rel="noopener" title="Maine Policy Institute, contact [CONFIRM: a Generation Maine address]">Contact</a>' % "https://mainepolicy.org/contact/")   # the source parameter is added with the other outbound links below
    footer = re.sub(r'href="(https?://[^"]+)"', lambda m: 'href="%s"' % utm(m.group(1)), footer)
    url = LIVE + theme["key"] + "/"
    html = HTML % dict(root_class=theme["root_class"], css=css, url=url, bar_logo=S.logo("lockup-compact-reversed", "lk", theme["logo"]), h1=theme["h1"],
                       hero_bg=hero_bg, hero_side=hero_side, hero_credit=hero_credit, h2_about=theme["h2_about"], h2_creators=theme["h2_creators"], h2_follow=theme["h2_follow"],
                       bars=bars(), cols=cols_html(), about_media=about_media(theme), tiles=tiles_html(), stepper=stepper_html(), follow=follow_html(), footer=footer, mural_json=json.dumps(theme["mural"]) if theme["mural"] else "{}")
    html = html.replace("#EFB443", MG)
    write(os.path.join(out_dir, "index.html"), html)
    icons(theme, out_dir)
    share_card(theme, out_dir)
    print("wrote", out_dir)


if __name__ == "__main__":
    for t in (LEAN_A, LEAN_B):
        page(t)
