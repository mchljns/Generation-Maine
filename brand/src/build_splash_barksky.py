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
  --sky:#CFE3F0;--bark:#2B211C;--paper:#FFFFFF;--mist:#EEF4F8;--clay:#6B5A4E;--bark2:#3A2D26;
  --sp:var(--sky);--pine:var(--bark);--bi:var(--paper);--ink:var(--bark);--snow:var(--bark);--mg:var(--clay);--sage:var(--mist);--sand:var(--mist);--moss:var(--clay);
  --fg:var(--bark);--muted:var(--clay);--rule:rgba(43,33,28,.16);--card:var(--mist);
  --display:'Hedvig Letters Serif',Georgia,'Times New Roman',serif;--body:'Hedvig Letters Sans',system-ui,Arial,sans-serif;
}
/* one weight each, so nothing is ever synthesized bold */
.bs *{font-weight:400!important}
.bs h1,.bs h2,.bs h3{letter-spacing:-.02em;line-height:1.02;text-transform:lowercase}
.bs .d{display:none}
.bs .k{text-transform:lowercase;letter-spacing:.08em;font-size:13px}
.bs .top nav,.bs .top .cta,.bs .btn,.bs .tl,.bs .sheet nav a,.bs .sheet .foot .cta,.bs .where,.bs .follow a b,.bs .form button{text-transform:lowercase}
/* buttons: Bark pills with Paper type, everywhere. The text link is Bark. */
.bs .b1,.bs .b3{background:var(--bark);color:var(--paper)}.bs .b1:hover,.bs .b3:hover{background:var(--bark2)}
.bs .tl{color:var(--bark)}
/* the bar: no band. Bark type on the Sky hero, then the frosted capsule; the open sheet is Bark with Sky type and the Sky lockup */
.bs .top{background:transparent;color:var(--bark)}
.bs .top:not(.open) .lk.light{display:none}.bs .top:not(.open) .lk.dark{display:block}
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
.bs .hero .w{grid-template-columns:1fr;justify-items:center;text-align:center;align-items:start;padding-block:40px 96px;min-height:0;gap:0}
.bs .mural{order:-1;width:min(30vw,200px);justify-self:center;margin:0 0 28px}
.bs .hero h1{font-size:clamp(44px,7.4vw,104px);max-width:13ch}
.bs .hero .lede{margin:28px auto 32px;max-width:46ch}
.bs .hero .ctas{justify-content:center}
@media (max-width:900px){.bs .hero .w{padding-block:36px 64px}.bs .mural{width:min(36vw,150px);margin-bottom:22px}}
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
.bs .words blockquote footer span{color:rgba(207,227,240,.7)}
/* follow on Mist, footer on Bark with the Sky lockup */
.bs .follow .ic{--icon-bg:var(--mist)}
.bs .site{background:var(--bark);color:var(--sky)}.bs .site p{color:var(--sky)}
/* the horizontal lockup is wide, so it is sized by width: it never runs past the screen */
.bs .site .lk{width:min(100%,720px);height:auto}
"""

BARK_SKY = dict(
    logo=os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky"),
    nav_light="lockup-horizontal-solid-reversed", nav_dark="lockup-horizontal-solid", footer="lockup-horizontal-large-reversed", footer_ping=False,
    fonts=FONTS, font_files={"FSERIF": "brand/fonts/d/HedvigLettersSerif-24.ttf", "FSANS": "brand/fonts/d/HedvigLettersSans-Regular.ttf"},
    mural="#2B211C", bg_follow="var(--mist)", css=CSS, title="Generation Maine, Bark & Sky", root_class="bs",
    out="brand/identity/splash-bark-sky", media="../splash/")

if __name__ == "__main__":
    standalone, _ = S.page(BARK_SKY, media="../splash/")   # the repo copy reads the clips from the Signature splash's media folder
    _, artifact = S.page(BARK_SKY, media="")               # the artifact copy carries the clips beside it
    write(BARK_SKY["out"] + "/index.html", standalone)
    print("bark & sky splash written")
