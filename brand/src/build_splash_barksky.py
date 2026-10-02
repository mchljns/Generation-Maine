"""The splash page in Bark & Sky, the second concept, built on the same template and motion as Signature.

What changes: Sky, Bark, Paper, Mist and Clay in place of the greens; Hedvig Letters Serif and Sans at one weight, all lowercase for
titles, names, nav and buttons; a centered, airy hero with the sixteen-line state in Bark above the headline; no dot anywhere; the one
dark section is Bark, not Marigold. What stays: every section, the scroll-driven field, the capsule, the pinned creators, the hand-off.

  python3 brand/src/build_splash_barksky.py   # writes brand/identity/splash-bark-sky/index.html and artifact.html
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import build_splash as S

FONTS = """@font-face{font-family:'Hedvig Letters Serif';font-weight:400;font-display:swap;src:url(data:font/ttf;base64,{{FSERIF}}) format('truetype')}
@font-face{font-family:'Hedvig Letters Sans';font-weight:400;font-display:swap;src:url(data:font/ttf;base64,{{FSANS}}) format('truetype')}"""

CSS = r"""
/* Bark & Sky. The variables the page and its script already use are pointed at the concept's palette, then the few rules that
   assumed green get their counterparts. Sky is the hero field, Paper the page, Bark the dark fields, Mist the light one, Clay the quiet text. */
:root{
  --sky:#CFE3F0;--bark:#2B211C;--paper:#FFFFFF;--mist:#EEF4F8;--clay:#5E4E43;--bark2:#3A2D26;
  --sp:var(--sky);--pine:var(--bark);--bi:var(--paper);--ink:var(--bark);--snow:var(--bark);--mg:var(--clay);--sage:var(--mist);--sand:var(--mist);--moss:var(--clay);
  --fg:var(--bark);--muted:var(--clay);--rule:rgba(43,33,28,.16);--card:var(--mist);
  --display:'Hedvig Letters Serif',Georgia,'Times New Roman',serif;--body:'Hedvig Letters Sans',system-ui,Arial,sans-serif;
}
/* one weight each, set on every element the template makes heavy, so nothing is synthesized bold. Emphasis in reading text becomes the serif. */
.bs h1,.bs h2,.bs h3,.bs .k,.bs .btn,.bs .tl,.bs .top .cta,.bs .top nav,.bs .where,.bs .soc a,.bs .follow a b,.bs .post .by,.bs .post .dt,.bs .form .ok,.bs .form .err,.bs .form button,
.bs .about .cols h3,.bs .words blockquote p,.bs .words blockquote footer,.bs .sheet nav a,.bs .sheet .foot a,.bs .who span b,.bs .vid .dur,.bs .site p,.bs b,.bs strong{font-weight:400}
.bs .bio b,.bs .bio strong,.bs .lede b,.bs .lede strong{font-family:var(--display);font-size:1.06em}
.bs h1,.bs h2,.bs h3{letter-spacing:-.02em;line-height:1.02;text-transform:lowercase}
.bs .d{display:none}
.bs .k{text-transform:lowercase;letter-spacing:.08em;font-size:13px}
.bs .top nav,.bs .top .cta,.bs .btn,.bs .tl,.bs .sheet nav a,.bs .sheet .foot .cta,.bs .where,.bs .form button{text-transform:lowercase}
/* buttons: Bark pills with Paper type, everywhere. The text link is Bark. */
.bs .b1,.bs .b3{background:var(--bark);color:var(--paper)}.bs .b1:hover,.bs .b3:hover{background:var(--bark2)}
.bs .tl{color:var(--bark)}
/* the bar: no band. Bark type on the Sky hero, then the frosted capsule; the open sheet is Bark with Sky type and the Sky lockup */
.bs .top{background:transparent;color:var(--bark)}
.bs .top .lk{height:28px}.bs .top.scrolled .lk{height:22px}
.bs .top .lk.light,.bs .top .lk.dark{display:none}.bs .top .lk.rest{display:block}
.bs .top.scrolled .lk.rest{display:none}.bs .top.scrolled .lk.dark{display:block}
.bs .top.open .lk.rest,.bs .top.open .lk.dark{display:none}.bs .top.open .lk.light{display:block}
.bs .sheet .foot .sheet-soc a{color:var(--sky)}.bs .sheet .foot .sheet-soc .ic{--icon-bg:var(--bark)}
.bs .top nav a::before{display:none}.bs .top nav a.on{text-decoration:underline;text-underline-offset:6px;text-decoration-thickness:1px}
.bs .top .cta{border-color:var(--bark)}.bs .top .cta:hover{background:rgba(43,33,28,.08)}
.bs .top.scrolled .w{box-shadow:0 10px 30px rgba(43,33,28,.14)}
.bs .top.scrolled nav a:hover{background:rgba(43,33,28,.08)}
.bs .top.scrolled nav a.on{background:var(--bark);color:var(--paper);text-decoration:none}
.bs .top.scrolled .cta{background:var(--bark);color:var(--paper);border-color:var(--bark)}
.bs .prog{background:var(--bark)}
.bs .top.open{color:var(--sky)}
.bs .sheet{background:var(--bark);color:var(--sky)}.bs .sheet .foot .cta{background:var(--sky);color:var(--bark)}
/* the hero: centered and airy. The state in Bark sits above the headline, the headline in the serif at one weight. */
.bs .hero .w{grid-template-columns:1fr;justify-items:center;text-align:center;align-items:start;padding-block:28px 80px;min-height:0;gap:0}
.bs .mural{order:-1;width:min(30vw,200px,22vh);justify-self:center;margin:0 0 22px}
.bs .hero h1{font-size:clamp(40px,min(7.4vw,10.5vh),104px);max-width:13ch}
.bs .hero .lede{margin:20px auto 26px;max-width:46ch;font-size:clamp(17px,min(1.6vw,2.6vh),22px)}
.bs .hero .ctas{justify-content:center}
@media (max-width:900px){.bs .hero .w{padding-block:36px 64px}.bs .mural{width:min(36vw,150px);margin-bottom:22px}}
/* section heads are centered, like the hero and the kit's end card and header. Reading text inside them stays left-aligned. */
.bs .h2{text-align:center;margin-inline:auto;max-width:18ch;text-wrap:balance}
.bs .about .w{grid-template-columns:1fr;gap:44px;justify-items:center}
.bs .about .cols{width:100%;text-align:left}
.bs .stories-head .w{text-align:center}.bs .stories-head .lede{margin:18px auto 0}
.bs .words .h2{margin-bottom:8px}
.bs .news .w{grid-template-columns:1fr;gap:48px;justify-items:center}
.bs .news .w>div:first-child{text-align:center;display:flex;flex-direction:column;align-items:center}
.bs .news .lede{margin:18px auto 26px}
.bs .form{justify-content:center}.bs .form .k{text-align:left}.bs .form .note,.bs .form .ok,.bs .form .err{text-align:center}
.bs .posts{width:100%;max-width:820px}
.bs .follow .h2{margin-bottom:36px}
/* about: Bark type from the start, on Sky scrubbing to Paper. The columns' rules are Bark. */
.bs .about,.bs .about.lit{color:var(--bark)}
.bs .about .cols p{color:var(--bark)}.bs .about.lit .cols p{color:var(--clay)}
.bs .about .cols div::before{background:var(--bark)}
/* the creators: the name in the serif, the town in Clay */
.bs .panel h2{font-size:clamp(36px,4.4vw,64px)}
.bs .panel .k{color:var(--clay)}
.bs .where{letter-spacing:.08em}
/* in their words: the one dark section is Bark with Sky type */
.bs .words{background:var(--bark);color:var(--sky)}
.bs .words blockquote::before{background:rgba(207,227,240,.4)}
.bs .words blockquote p{font-size:clamp(24px,2.3vw,34px);line-height:1.15;letter-spacing:-.01em}
.bs .words blockquote footer{font:400 17px/1.3 var(--display);color:var(--sky)}
.bs .words blockquote footer span{font:400 13px/1.3 var(--body);color:rgba(207,227,240,.72);margin-left:6px}
.bs .post .by{font:400 16px/1.3 var(--display);color:var(--bark)}.bs .post .by span{font:400 13px/1.3 var(--body);color:var(--clay);margin-left:4px}
.bs .who span{font:400 14px/1 var(--display)}.bs .who span b{font:400 12px/1 var(--body)}
.bs .follow a b{font-size:15px;color:var(--bark)}.bs .follow a span{font-size:15px;color:var(--clay)}
/* follow on Mist, footer on Bark with the Sky lockup */
.bs .follow .ic{--icon-bg:var(--mist)}
.bs .site{background:var(--bark);color:var(--sky)}.bs .site p{color:var(--sky)}
/* the horizontal lockup is wide, so it is sized by width: it never runs past the screen */
.bs .site .lk{width:min(100%,720px);height:auto}
"""

BARK_SKY = dict(
    logo=os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky"),
    nav_light="lockup-horizontal-solid-reversed", nav_dark="lockup-horizontal-solid", nav_rest="wordmark", footer="lockup-horizontal-large-reversed", footer_ping=False,
    fonts=FONTS, font_files={"FSERIF": "brand/fonts/d/HedvigLettersSerif-24.ttf", "FSANS": "brand/fonts/d/HedvigLettersSans-Regular.ttf"},
    mural="#2B211C", bg_follow="var(--mist)", css=CSS, title="Generation Maine, Bark & Sky", root_class="bs",
    out="brand/identity/splash-bark-sky", media="")

if __name__ == "__main__":
    S.page(BARK_SKY)   # the clips live beside the page, in the concept's own colors (brand/src/make_gifs.py --theme bark-sky)
    print("bark & sky splash written")
