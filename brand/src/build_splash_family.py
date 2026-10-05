"""Two splash pages that live in the Maine Policy Institute family: the shared rules are a navy top bar, a blue primary, one
warm accent on flat buttons, uppercase letterspaced labels and navigation, hard corners, and the Maine Policy credit in the
footer. Family A keeps Signature's type (Bricolage Grotesque, DM Sans) and lined state mark. Family B keeps Bark & Sky's
type (Hedvig Letters Serif, lowercase) and photographic hero. Both keep the creators and are trimmed of the quotes and newsletter
sections: what it is, what it hopes to achieve, the creators, where to find it.

  python3 brand/src/build_splash_family.py   # writes brand/identity/splash-family-a and splash-family-b
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_splash as S
import build_splash_barksky as B
import json

LOGO_A = os.path.join(S.ROOT, "brand", "identity", "logo-maine", "family-a")
LOGO_B = os.path.join(S.ROOT, "brand", "identity", "logo-maine", "family-b")
MURAL_A = json.load(open(os.path.join(LOGO_A, "mural.json")))

NAVY_A, BLUE_A, MG = "#0F2E4D", "#0556A5", "#EFB443"
NAVY_B, BLUE_B = "#112337", "#006CB5"
CREDIT = "© 2026 Generation Maine. An initiative of Maine Policy Institute. [CONFIRM: legal name, address and contact]"
COLS = [("What it is", "Young Mainers film the rules that shape their lives. Leases, licenses, permits, wages, and the fine print nobody reads until it costs them. Short videos, told from the towns they live in."),
        ("What we hope to achieve", "[CONFIRM: the project's aims in the client's words.] Young people in Maine who understand the rules behind everyday costs, and who say so in their own words."),
        ("Where to find it", "The videos are on TikTok, Instagram and YouTube. The full story, with the numbers, is in the newsletter on Substack. Nothing is published here.")]

# The audit (brand/07-family-ui-audit.md), applied. Keyed on the .static root class so the two original concepts are untouched.
STATIC_CSS = """
/* header: a plain sticky bar. No capsule morph, no hide on scroll, no progress bar, no nav dot. */
.static .top.scrolled .w{height:60px;max-width:1280px;margin:0 auto;padding-inline:var(--M);background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none;box-shadow:none;border-radius:0}
.static .top.scrolled{background:var(--pine);color:#fff}
.static .top.scrolled .lk{height:24px}.static .top.scrolled .lk.light{display:block}.static .top.scrolled .lk.dark{display:none}
.static .top.scrolled nav{gap:30px}.static .top.scrolled nav a{padding:12px 0;font-size:13px;background:none;color:inherit}
.static .top.scrolled nav a.on{background:none;color:inherit;text-decoration:underline;text-underline-offset:6px;text-decoration-thickness:1.5px}
.static .top nav a::before{display:none}.static .top.scrolled nav a::before{display:none}
.static .top.scrolled .cta{padding:12px 16px;font-size:13px}
.static .top.hide{transform:none}.static .prog{display:none}
.static .top.scrolled .w{box-shadow:0 1px 0 rgba(255,255,255,.12)}
/* corners: zero everywhere */
.static .btn,.static .top .cta,.static .form input,.static .form button,.static .top nav a,.static .sheet .foot .cta,.static .vid,.static .strip img,.static .ph img,.static .post .th,.static .qs-im,.static .who .av,.static .pv .av{border-radius:0}
.static .vid video,.static .vid img.clip{border-radius:0}
/* hover: color only */
.static .btn:hover{transform:none}
/* motion: static rules, no draw in; shorter section reveal; no page background cross fade */
.static .rule,.static .about .cols div::before,.static .words blockquote::before{transition:none;transform:none}
.static.js .reveal.pre .rule,.static.js .reveal.pre .cols div::before,.static.js .reveal.pre blockquote::before{transform:none}
.static .reveal .row-in{transition-duration:.5s}
.static body,.static .about{transition:none}
/* footer: no ping, no draw */
.static .site.on .lk .ping{animation:none}.static .site .lk .ping{display:none}
/* the dot stays on the hero only */
.static .h2 .d{display:none}
/* the sign up band under the hero: full width navy, one field, one button, like the parents */
.static .signup{background:var(--pine);color:#fff;padding:22px 0}
.static .signup .w{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:18px;align-items:center}
.static .signup b{font:600 14px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.static .signup input{height:48px;border:0;padding:0 16px;font:16px var(--body);background:#fff;color:var(--ink);min-width:0;width:100%%}
.static .signup .btn{padding:16px 28px}
.static .signup .note{grid-column:1/-1;margin:0;font-size:12px;opacity:.75}
@media (max-width:900px){.static .signup .w{grid-template-columns:1fr}.static .signup .btn{justify-self:start}}
/* about on its own flat band, not the page background */
.static .about{background:#fff;color:var(--ink)}.static .about .cols p{color:var(--muted)}
.static .stories-head,.static .stories{background:#fff}
"""

SIGNUP = ('<section class="signup" aria-label="Newsletter sign up"><div class="w"><b>Get the newsletter</b>'
          '<input type="email" placeholder="you@example.com" aria-label="Email" autocomplete="email">'
          '<a class="btn b1" href="https://CONFIRM-publication.substack.com/subscribe" target="_blank" rel="noopener">Sign up</a>'
          '<p class="note">Runs on Substack. Unsubscribe in one click. [CONFIRM: publication address]</p></div></section>')

FAMILY_A_CSS = """
/* Family A: Signature's type in the family's clothes */
:root{--sp:%(blue)s;--pine:%(navy)s;--ink:%(navy)s;--moss:#2191FF;--stone:#5B6B7A;--muted:#4B5A68;--sage:#EAF1F8;--sand:#F3F7FB;--card:#F3F7FB;--rule:rgba(15,46,77,.14);--bi:#FFFFFF}
.btn,.top .cta,.form input,.form button,.top nav a{border-radius:0}
.top.scrolled .w{border-radius:0}
.k,.top nav,.top .cta,.btn,.follow a b,.tl{text-transform:uppercase;letter-spacing:.1em}
.top nav{font-size:13px}.tl{font-size:13px}
.b1{background:%(mg)s;color:%(navy)s}.b1:hover{background:#F5C65C}
.b3{background:%(navy)s;color:#fff}.b3:hover{background:%(blue)s}
.top{background:%(navy)s}.top .cta{border-color:%(mg)s;color:%(mg)s}.top .cta:hover{background:%(mg)s;color:%(navy)s}
.top nav a::before{display:none}
.hero{background:%(blue)s}.hero h1 .nw{color:%(mg)s}.hero h1 .d{background:%(mg)s}.hero .k{color:#fff}
.hero .w{min-height:min(560px,72vh);padding-block:72px 80px}
.hero h1{font-size:clamp(44px,6vw,84px);letter-spacing:-.01em;line-height:1.0}
h2,h3{letter-spacing:-.01em}
.h2{font-size:clamp(34px,4vw,52px)}
.signup .btn{background:%(mg)s;color:%(navy)s}
/* the mural and the footer draw come back for Family A, with the slanted state */
.static .mural{display:block}.static .mural path{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1)}.static .mural.on path{stroke-dashoffset:0}
.static.js .site .lk path[stroke]{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .8s cubic-bezier(.2,.7,.2,1)}.static.js .site.on .lk path[stroke]{stroke-dashoffset:0}
.static .site .lk path:not([stroke]){stroke-dasharray:none}
@media (prefers-reduced-motion: reduce){.static .mural path,.static.js .site .lk path[stroke]{stroke-dashoffset:0;transition:none}}
.hero .w{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
@media (max-width:900px){.hero .w{grid-template-columns:1fr}.static .mural{order:-1;width:min(56vw,300px);justify-self:start;margin-bottom:8px}}
.site .lk{height:96px}
@media (max-width:900px){.site .lk{height:72px}}
.top .lk{height:26px}.static .top.scrolled .lk{height:26px}
.about .cols div::before{background:%(mg)s}.about.lit .cols div::before{background:%(mg)s}
.about .cols h3{font:800 18px/1.2 var(--display);letter-spacing:-.01em;text-transform:none}
.follow{background:#EAF1F8}
.site{background:%(navy)s}.site .fine{color:rgba(255,255,255,.75)}
.top.scrolled .w{background:rgba(255,255,255,.96)}
""" % dict(blue=BLUE_A, navy=NAVY_A, mg=MG)

FAMILY_B_CSS = """
/* Family B: Bark & Sky's type in the family's clothes */
.bs{--bark:%(navy)s;--bark2:#0B1A2B;--clay:#4F5B68;--blue:%(blue)s;--mg:%(mg)s;--rule:rgba(17,35,55,.16)}
.bs .btn,.bs .top .cta,.bs .form input,.bs .form button{border-radius:0}
.bs .top nav a,.bs .top .cta,.bs .btn,.bs .tl,.bs .sheet nav a,.bs .sheet .foot .cta,.bs .form button,.bs .k{text-transform:uppercase;letter-spacing:.1em;font-family:var(--body);font-size:13px}
.bs .hero .b1{background:%(mg)s;color:%(navy)s}.bs .hero .b1:hover{background:#F5C65C}
.bs .top{background:%(navy)s;color:#F4F3EE}.bs .top.scrolled,.bs .top.open{background:transparent}.bs .top:not(.scrolled) .cta{border-color:%(mg)s;color:%(mg)s}
.bs .hero .bg::after{background:linear-gradient(90deg,rgba(17,35,55,.88) 0%%,rgba(17,35,55,.7) 42%%,rgba(17,35,55,.3) 74%%,rgba(17,35,55,.2) 100%%),linear-gradient(180deg,rgba(17,35,55,.3) 0%%,rgba(17,35,55,0) 28%%,rgba(17,35,55,.45) 100%%)}
.bs .hero .w{padding-block:clamp(110px,16vh,160px) clamp(60px,9vh,96px)}
.bs .hero .k{display:block;color:%(mg)s;margin-bottom:18px}
.bs .about .cols div::before{background:%(blue)s}
.bs .follow{background:#EAF1F8}
.bs .site .fine{color:rgba(244,243,238,.75)}
.bs .top.scrolled .w{border-radius:0}
.bs.static .signup .btn{background:%(mg)s;color:%(navy)s}
.bs.static .top.scrolled{background:%(navy)s}
.bs .strip img,.bs .ph img{border-radius:0}
.bs .hero h1{font-size:clamp(42px,6vw,84px)}
/* the framed wordmark needs height: a taller bar, and room in the footer */
.bs.static .top .lk{height:26px;width:auto}.bs.static .top.scrolled .lk{height:26px}
@media (max-width:900px){.bs.static .top .lk{height:24px}}
.bs.static .site .lk{height:150px}@media (max-width:900px){.bs.static .site .lk{height:120px}}
/* footer: the frame draws itself. The long leg first, from the open end up and around; then the return from the corner back toward the opening; then the two words rise in. Hidden states do not depend on .js, or they would transition in at load; without script everything shows at once */
.bs.static .site .lk path[stroke]{stroke-dasharray:1;stroke-dashoffset:1}.bs.static .site .lk path[stroke]:nth-of-type(2){stroke-dashoffset:-1}
.bs.static .site .lk g path{opacity:0;transform-box:fill-box;transform:translateY(5%%)}
.bs.static:not(.js) .site .lk path[stroke],.bs.static .site.on .lk path[stroke]{stroke-dashoffset:0}
.bs.static:not(.js) .site .lk g path,.bs.static .site.on .lk g path{opacity:1;transform:none}
.bs.static.js .site .lk path[stroke]:nth-of-type(1){transition:stroke-dashoffset 1.9s cubic-bezier(.3,.6,.2,1) 0s!important}
.bs.static.js .site .lk path[stroke]:nth-of-type(2){transition:stroke-dashoffset .9s cubic-bezier(.3,.6,.2,1) 1.7s!important}
.bs.static.js .site .lk g path{transition:opacity 1s ease-out,transform 1.2s cubic-bezier(.2,.7,.2,1)}
.bs.static.js .site .lk g path:nth-of-type(1){transition-delay:1.4s!important}.bs.static.js .site .lk g path:nth-of-type(2){transition-delay:1.75s!important}
@media (prefers-reduced-motion: reduce){.bs.static .site .lk path[stroke]{stroke-dashoffset:0!important;transition:none!important}.bs.static .site .lk g path{opacity:1;transform:none;transition:none!important}}
""" % dict(blue=BLUE_B, navy=NAVY_B, mg=MG)

FAMILY_A = dict(S.SIGNATURE, css=STATIC_CSS + FAMILY_A_CSS, root_class="static", signup_band=SIGNUP, footer_at_bottom=True,
                logo=LOGO_A, nav_light="lockup-compact-reversed", nav_dark="lockup-compact-reversed", footer="lockup-two-line-reversed", mural_data=MURAL_A, title="Generation Maine", out="brand/identity/splash-family-a", media="",
                lean=True, hero_kicker="A Maine Policy Institute project", h2about="What this is", cols=COLS, footer_line=CREDIT, bg_follow="#EAF1F8", footer_ping=False)

B_CSS = B.CSS.replace("{media}", "") + STATIC_CSS.replace(".static", ".static.bs").replace(".static.bs.js", ".static.bs.js") + FAMILY_B_CSS
FAMILY_B = dict(B.BARK_SKY, css=B_CSS, title="Generation Maine", out="brand/identity/splash-family-b", media="", root_class="bs static", signup_band=SIGNUP, footer_at_bottom=True,
                logo=LOGO_B, nav_light="lockup-compact-reversed", nav_dark="lockup-compact-reversed", nav_rest="lockup-compact-reversed", footer="lockup-two-line-reversed",
                lean=True, hero_kicker="A Maine Policy Institute project", h2about="what this is", cols=COLS, footer_line=CREDIT, bg_follow="#EAF1F8",
                about_media="", band="", post_thumbs=["", "", ""], quote_stills=["", "", ""])

if __name__ == "__main__":
    S.page(FAMILY_A)
    S.page(FAMILY_B)
    print("family pages written")
