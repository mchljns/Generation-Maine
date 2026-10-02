"""The splash page in Bark & Sky, the second concept, built on the same template and motion as Signature.

October 2, the Field notes treatment: for a Gen Z audience that leans masculine, still understated. A steel sky instead of a pastel
one, bone paper instead of white, a grid that sits left, IBM Plex Mono for every label and number the way gear tags and camera overlays
use one, and the horizon mark (the state rising from the ground) as the badge in the bar and the footer. The serif keeps the names
and headlines. Nothing heavy, nothing black, no texture.

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
@font-face{font-family:'Hedvig Letters Sans';font-weight:400;font-display:swap;src:url(data:font/ttf;base64,{{FSANS}}) format('truetype')}
@font-face{font-family:'IBM Plex Mono';font-weight:500;font-display:swap;src:url(data:font/ttf;base64,{{FMONO}}) format('truetype')}"""

CSS = r"""
/* Bark & Sky. The variables the page and its script already use are pointed at the concept's palette, then the few rules that
   assumed green get their counterparts. Sky is the hero field, Paper the page, Bark the dark fields, Mist the light one, Clay the quiet text. */
:root{
  --sky:#B9C9D3;--bark:#26201C;--paper:#F4F3EE;--mist:#E4E8E6;--clay:#5B544C;--blue:#2B4760;--bark2:#352C26;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
  --sp:var(--sky);--pine:var(--bark);--bi:var(--paper);--ink:var(--bark);--snow:var(--bark);--mg:var(--clay);--sage:var(--mist);--sand:var(--mist);--moss:var(--clay);
  --fg:var(--bark);--muted:var(--clay);--rule:rgba(43,33,28,.16);--card:var(--mist);
  --display:'Hedvig Letters Serif',Georgia,'Times New Roman',serif;--body:'Hedvig Letters Sans',system-ui,Arial,sans-serif;
}
/* the white page is bone, and the blue that was a link's only hint becomes the link color */
.bs body,body.bs{background:var(--paper)}
.bs a:not(.btn):not(.tl):not(.cta):not(.post):not(.soc a):not(.follow a):not(nav a):not(.lk):not(.top .w>a){color:var(--blue)}
/* one weight each, set on every element the template makes heavy, so nothing is synthesized bold. Emphasis in reading text becomes the serif. */
.bs h1,.bs h2,.bs h3,.bs .k,.bs .btn,.bs .tl,.bs .top .cta,.bs .top nav,.bs .where,.bs .soc a,.bs .follow a b,.bs .post .by,.bs .post .dt,.bs .form .ok,.bs .form .err,.bs .form button,
.bs .about .cols h3,.bs .words blockquote p,.bs .words blockquote footer,.bs .sheet nav a,.bs .sheet .foot a,.bs .who span b,.bs .vid .dur,.bs .site p,.bs b,.bs strong{font-weight:400}
.bs .bio b,.bs .bio strong,.bs .lede b,.bs .lede strong{font-family:var(--display);font-size:1.06em}
.bs h1,.bs h2,.bs h3{letter-spacing:-.02em;line-height:1.02;text-transform:lowercase}
.bs .d{display:none}
/* the monospace is for numbers only: the counter, the clip length, the dates. Everything else is the sans in sentence case. */
.bs .where .n,.bs .vid .dur,.bs .post .dt{font-family:var(--mono);letter-spacing:.04em}
.bs .k{text-transform:none;letter-spacing:0;font-size:14px}
.bs .where{text-transform:none;letter-spacing:0;font-size:13px}
/* the town is a line under the name, not a label over it */
.bs .panel h2{order:0}.bs .panel .k{order:1;margin:8px 0 18px;font-size:16px;color:var(--clay)}.bs .panel .bio{order:2}.bs .panel .soc{order:3}.bs .panel .k .d{display:none}
.bs .form .k{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.bs .about .cols h3{font-size:17px;margin-bottom:8px}
.bs .top nav a,.bs .top .cta,.bs .btn,.bs .tl,.bs .sheet nav a,.bs .sheet .foot .cta,.bs .form button{text-transform:lowercase}
/* buttons: Bark pills with Paper type, everywhere. The text link is Bark. */
.bs .b1,.bs .b3{background:var(--bark);color:var(--paper)}.bs .b1:hover,.bs .b3:hover{background:var(--bark2)}
.bs .tl{color:var(--bark)}
/* the bar: no band. Bark type on the Sky hero, then the frosted capsule; the open sheet is Bark with Sky type and the Sky lockup */
.bs .top{background:transparent;color:var(--bark)}
.bs .top .lk{height:22px}.bs .top.scrolled .lk{height:19px}
.bs .top .lk.light,.bs .top .lk.dark{display:none}.bs .top .lk.rest{display:block}
.bs .top.scrolled .lk.rest{display:none}.bs .top.scrolled .lk.dark{display:block}
.bs .top.open .lk.rest,.bs .top.open .lk.dark{display:none}.bs .top.open .lk.light{display:block}
.bs .sheet .foot .sheet-soc a{color:var(--sky)}.bs .sheet .foot .sheet-soc .ic{--icon-bg:var(--bark)}
.bs .top nav a::before{display:none}.bs .top nav a.on{text-decoration:underline;text-underline-offset:7px;text-decoration-thickness:1px}
.bs .tl{color:var(--bark)}.bs .top.scrolled nav a.on{text-decoration:none}
.bs .top.scrolled .w{background:rgba(244,243,238,.92)}
.bs .top .cta{border-color:var(--bark)}.bs .top .cta:hover{background:rgba(43,33,28,.08)}
.bs .top.scrolled .w{box-shadow:0 10px 30px rgba(43,33,28,.14)}
.bs .top.scrolled nav a:hover{background:rgba(43,33,28,.08)}
.bs .top.scrolled nav a.on{background:var(--bark);color:var(--paper);text-decoration:none}
.bs .top.scrolled .cta{background:var(--bark);color:var(--paper);border-color:var(--bark)}
.bs .prog{background:var(--bark)}
.bs .top.open{color:var(--sky)}
.bs .sheet{background:var(--bark);color:var(--sky)}.bs .sheet .foot .cta{background:var(--sky);color:var(--bark)}
/* the hero: centered and airy. The state in Bark sits above the headline, the headline in the serif at one weight. */
/* the hero is the video, edge to edge. The words sit low left in Paper on a Bark scrim that is heaviest where they are. */
.bs .hero{background:var(--bark);color:var(--paper);min-height:min(860px,100svh);display:flex;align-items:flex-end}
.bs .hero .bg{position:absolute;inset:0;overflow:hidden;z-index:0;background:var(--bark)}
.bs .hero .bg video,.bs .hero .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.bs .hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(38,32,28,.80) 0%,rgba(38,32,28,.62) 42%,rgba(38,32,28,.18) 74%,rgba(38,32,28,.08) 100%),linear-gradient(180deg,rgba(38,32,28,.32) 0%,rgba(38,32,28,0) 28%,rgba(38,32,28,.42) 100%)}
.bs .hero .w{position:static;display:block;width:100%;padding-block:clamp(120px,18vh,180px) clamp(60px,9vh,96px);min-height:0}
.bs .hero .h1{position:relative;z-index:2;max-width:760px}
.bs .hero h1{font-size:clamp(42px,min(6.4vw,11vh),92px);max-width:12ch;color:var(--paper);text-shadow:0 1px 2px rgba(38,32,28,.25)}
.bs .hero .lede{margin:22px 0 28px;max-width:40ch;font-size:clamp(17px,min(1.5vw,2.6vh),21px);color:var(--paper)}
.bs .hero .b1{background:var(--paper);color:var(--bark)}.bs .hero .b1:hover{background:#fff}
.bs .hero .tl{color:var(--paper)}
.bs .mural{display:none}
.bs .hero .credit{position:absolute;right:var(--M);bottom:16px;z-index:2;margin:0;font:400 11px/1.35 var(--body);color:rgba(244,243,238,.72);max-width:44ch;text-align:right}
@media (prefers-reduced-motion: reduce){.bs .hero .bg video{display:none}.bs .hero .bg{background:url({media}media/hero-poster.jpg) center/cover no-repeat}}
/* the smaller photograph slots: a town under the about heading, a wide band before the quotes, a thumbnail on each post, a still beside each quote */
.bs .about .w{align-items:start}
.bs .ph{margin:34px 0 0;max-width:460px}.bs .ph img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:12px;background:var(--mist)}
.bs .ph figcaption{font:400 12px/1.4 var(--body);color:var(--clay);margin-top:10px}
.bs .band{position:relative;height:min(520px,56vh);padding-block:0;overflow:hidden;background:var(--bark);color:var(--paper);display:flex;flex-direction:column;justify-content:flex-end}
.bs .band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.bs .band::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(38,32,28,.08) 0%,rgba(38,32,28,0) 30%,rgba(38,32,28,0) 70%,rgba(38,32,28,.42) 100%)}
.bs .band .w{position:relative;z-index:2;width:100%;padding-block:0 48px}
.bs .band p{margin:0;font:400 clamp(26px,3.2vw,44px)/1.08 var(--display);max-width:18ch;text-wrap:balance;text-shadow:0 1px 2px rgba(38,32,28,.3)}
.bs .band .credit{position:absolute;right:var(--M);bottom:16px;z-index:2;font:400 11px/1.3 var(--body);color:rgba(244,243,238,.72)}
.bs .post{grid-template-columns:112px minmax(0,1fr) auto;align-items:start}
.bs .post .th{display:block;width:112px;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:8px;background:var(--mist)}
.bs .words blockquote footer{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.bs .qs-im{display:block;width:40px;height:52px;object-fit:cover;border-radius:6px;background:var(--bark2)}
@media (max-width:900px){.bs .ph{max-width:none;margin-top:26px}.bs .band{height:min(380px,52vh)}.bs .band .w{padding-block:0 18px}.bs .band .credit{position:static;display:block;padding:0 var(--M) 14px;color:rgba(244,243,238,.72)}.bs .post{grid-template-columns:88px minmax(0,1fr) auto}.bs .post .th{width:88px}}
/* the bar over the video: Paper type and the Sky wordmark until the page scrolls, then the capsule as before */
.bs .top{color:var(--paper)}.bs .top .tl{color:var(--paper)}
.bs .top:not(.scrolled) .cta{border-color:rgba(244,243,238,.75)}.bs .top:not(.scrolled) .cta:hover{background:rgba(244,243,238,.14)}
.bs .top:not(.scrolled) nav a:hover{background:rgba(244,243,238,.12)}
.bs .top.scrolled{color:var(--bark)}.bs .top.scrolled .tl{color:var(--bark)}
@media (max-width:900px){.bs .hero{min-height:min(760px,100svh)}.bs .hero .w{padding-block:124px 56px}.bs .top .lk{height:26px}.bs .hero .credit{position:static;text-align:left;margin-top:26px;max-width:none}.bs .hero .bg::after{background:linear-gradient(180deg,rgba(38,32,28,.42) 0%,rgba(38,32,28,.18) 30%,rgba(38,32,28,.74) 100%)}}
/* section heads are centered, like the hero and the kit's end card and header. Reading text inside them stays left-aligned. */
.bs .h2{max-width:14ch;text-wrap:balance}
.bs .strip{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px;margin-top:34px}
.bs .strip img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:8px;background:var(--mist)}
@media (max-width:900px){.bs .strip{grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}.bs .strip img:nth-child(n+6){display:none}}
.bs .follow .h2{margin-bottom:32px}
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
.bs .follow a b{font-size:15px;color:var(--bark)}.bs .follow a span{font-size:13px;color:var(--clay);overflow-wrap:anywhere}
@media (max-width:760px){.bs .follow a span{font-size:11px}}
/* follow on Mist, footer on Bark with the Sky lockup */
.bs .follow .ic{--icon-bg:var(--mist)}
.bs .site{background:var(--bark);color:var(--sky)}.bs .site p{color:var(--sky)}
/* the horizontal lockup is wide, so it is sized by width: it never runs past the screen */
.bs .site{background:var(--bark);padding-block:44px 40px}
.bs .site .w{grid-template-columns:auto minmax(0,1fr);gap:48px;align-items:center}
.bs .site .lk{width:auto;height:34px}
.bs .site .lk path{stroke-dasharray:none;stroke-dashoffset:0}
.bs .site p{max-width:52ch}
@media (max-width:640px){.bs .site .w{grid-template-columns:1fr;gap:22px}.bs .site .lk{height:28px}}
"""

BARK_SKY = dict(
    logo=os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky"),
    nav_light="wordmark-reversed", nav_dark="wordmark", nav_rest="wordmark-reversed", footer="wordmark-reversed", footer_ping=False,
    hero_media='<div class="bg" aria-hidden="true"><video autoplay muted loop playsinline preload="auto" poster="{media}media/hero-poster.jpg"><source src="{media}media/hero.webm" type="video/webm"></video></div><p class="credit">Katahdin, Aroostook County, Cadillac Mountain, Portland Head Light, the Old Port. Photographs via Wikimedia Commons, credits in the footer.</p>',
    about_media='<figure class="ph"><img src="{media}media/about.jpg" alt="Belfast, Maine, the brick downtown and the harbor from above." width="1600" height="1067" loading="lazy"><figcaption>Belfast. Photograph via Wikimedia Commons, credits in the footer.</figcaption></figure>',
    band='<section class="band" aria-label="Lewiston, Maine from above"><img src="{media}media/band.jpg" alt="" width="2400" height="1000" loading="lazy"><span class="credit">Lewiston. Photograph via Wikimedia Commons, credits in the footer.</span></section>',
    post_thumbs=['<img class="th" src="{media}media/post-%d.jpg" alt="" width="720" height="480" loading="lazy">' % i for i in (1, 2, 3)],
    quote_stills=['<img class="qs-im" src="{media}media/portrait-%d.jpg" alt="" width="120" height="160" loading="lazy">' % i for i in (2, 7, 4)],
    credits="Photographs in the opening loop, via Wikimedia Commons: Michael Sipos (CC BY-SA 4.0), Jack Delano for the Farm Security Administration (public domain), John Manard (CC BY-SA 2.0), Derek Ramsey (CC BY-SA 4.0), Domenico Convertini (CC BY-SA 2.0). Towns: Quintin Soloviev (Belfast and Lewiston from above, CC BY 4.0), FujiAppleSan (Belfast, CC0), Zedmaster375 (Machias, CC BY-SA 3.0), David Wilson (Lewiston, CC BY 2.0).",
    head_extra='<div class="strip" aria-hidden="true">' + ''.join('<img src="{media}media/portrait-%d.jpg" alt="" loading="lazy">' % i for i in range(1, 10)) + '</div>',
    fonts=FONTS, font_files={"FSERIF": "brand/fonts/d/HedvigLettersSerif-24.ttf", "FSANS": "brand/fonts/d/HedvigLettersSans-Regular.ttf", "FMONO": "brand/fonts/alt/IBMPlexMono-Medium.ttf"},
    mural="#2B211C", bg_follow="var(--mist)", css=CSS, title="Generation Maine, Bark & Sky", root_class="bs",
    out="brand/identity/splash-bark-sky", media="")

if __name__ == "__main__":
    BARK_SKY["css"] = CSS.replace("{media}", BARK_SKY["media"])
    S.page(BARK_SKY)   # the clips and photos live beside the page (make_gifs.py --theme bark-sky, make_photos.py)
    print("bark & sky splash written")
