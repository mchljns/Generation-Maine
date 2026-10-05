"""Two splash pages that live in the Maine Policy Institute family: the shared rules are a navy top bar, a blue primary, one
warm accent on flat buttons, uppercase letterspaced labels and navigation, hard corners, and the Maine Policy credit in the
footer. Family A keeps Signature's type (Bricolage Grotesque, DM Sans) and lined state mark. Family B keeps Bark & Sky's
type (Hedvig Letters Serif, lowercase) and photographic hero. Both are trimmed to the three jobs the client asked for:
what it is, what it hopes to achieve, where to find it.

  python3 brand/src/build_splash_family.py   # writes brand/identity/splash-family-a and splash-family-b
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_splash as S
import build_splash_barksky as B

NAVY_A, BLUE_A, MG = "#0F2E4D", "#0556A5", "#EFB443"
NAVY_B, BLUE_B = "#112337", "#006CB5"
CREDIT = "© 2026 Generation Maine. An initiative of Maine Policy Institute. [CONFIRM: legal name, address and contact]"
COLS = [("What it is", "Young Mainers film the rules that shape their lives. Leases, licenses, permits, wages, and the fine print nobody reads until it costs them. Short videos, told from the towns they live in."),
        ("What we hope to achieve", "[CONFIRM: the project's aims in the client's words.] Young people in Maine who understand the rules behind everyday costs, and who say so in their own words."),
        ("Where to find it", "The videos are on TikTok, Instagram and YouTube. The full story, with the numbers, is in the newsletter on Substack. Nothing is published here.")]

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
.hero .w{min-height:min(620px,78vh)}
.mural{display:none}
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
""" % dict(blue=BLUE_B, navy=NAVY_B, mg=MG)

FAMILY_A = dict(S.SIGNATURE, css=FAMILY_A_CSS, title="Generation Maine", out="brand/identity/splash-family-a", media="",
                lean=True, hero_kicker="A Maine Policy Institute project", h2about="What this is", cols=COLS, footer_line=CREDIT, bg_follow="#EAF1F8", footer_ping=False)

B_CSS = B.CSS.replace("{media}", "") + FAMILY_B_CSS
FAMILY_B = dict(B.BARK_SKY, css=B_CSS, title="Generation Maine", out="brand/identity/splash-family-b", media="",
                lean=True, hero_kicker="A Maine Policy Institute project", h2about="what this is", cols=COLS, footer_line=CREDIT, bg_follow="#EAF1F8",
                about_media="", band="", post_thumbs=["", "", ""], quote_stills=["", "", ""], head_extra="")

if __name__ == "__main__":
    S.page(FAMILY_A)
    S.page(FAMILY_B)
    print("family pages written")
