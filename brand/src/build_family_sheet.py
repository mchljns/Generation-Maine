"""A comparison sheet: each concept as built, and a version that could live in the Maine Policy Institute family
(navy top bar, blue primary, one warm accent on flat buttons, uppercase letterspaced labels, hard corners). The parent
sites sit on the top row for reference. Nothing here touches the live pages.

  python3 brand/src/build_family_sheet.py   # writes brand/identity/family-sheet.html and family-sheet.png
"""
import base64
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write

LOGO_S = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")
LOGO_B = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
REF = os.path.join(ROOT, "brand", "content", "reference")
HERO = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media", "hero-poster.jpg")
ABOUT = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media", "about.jpg")


def svg_data(path, recolor=None):
    s = open(path).read()
    if recolor:
        s = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="%s"' % recolor, s)
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


def font(fam, path, weight="400"):
    return "@font-face{font-family:'%s';font-weight:%s;src:url(file://%s)}" % (fam, weight, path)


FONTS = (font("Bricolage Grotesque", os.path.join(ROOT, "generation-maine", "assets", "fonts", "bricolage-grotesque-800.woff2"), "800")
         + font("DM Sans", os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"), "100 900")
         + font("Hedvig Letters Serif", os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSerif-24.ttf"))
         + font("Hedvig Letters Sans", os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSans-Regular.ttf"))
         + font("IBM Plex Mono", os.path.join(ROOT, "brand", "fonts", "alt", "IBMPlexMono-Medium.ttf"), "500"))

H1 = "Young Mainers on building a life here"
LEDE = "Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay."
COLS = [("Who makes it", "Young Mainers with a phone and a story."), ("What it is about", "Leases, licenses, permits, wages, the fine print."), ("Where to find it", "Short videos on TikTok, Instagram and YouTube. The full story by email.")]


def mock(cls, logo, title, h1_html, kicker, btn1, btn2, cols_label, swatches, notes, photo=None, band=False, slash=False):
    cols = "".join('<div><h4>%s</h4><p>%s</p></div>' % c for c in COLS)
    bg = ' style="background-image:url(file://%s)"' % photo if photo else ""
    kicker = ('<span class="sl">//</span> ' + kicker) if slash else kicker
    bandhtml = ('<div class="band"><span>Sign up for updates</span><i></i><i></i><b>Sign up</b></div>') if band else ""
    return ('<div class="item"><div class="card %s"><div class="top"><img src="%s" class="lk"><span class="nav">about · creators · follow</span><span class="cta">newsletter</span></div>'
            '<div class="hero"%s><div class="scrim"></div><div class="in"><span class="k">%s</span><h1>%s</h1><p>%s</p><div class="bt"><b>%s</b><i>%s</i></div></div></div>'
            '%s<div class="about"><span class="lab">%s</span><div class="cols">%s</div></div>'
            '<div class="foot"><img src="%s" class="lk2"><span>© 2026 Generation Maine · An initiative of Maine Policy Institute</span></div></div>'
            '<div class="meta"><h3>%s</h3><div class="sw">%s</div><p>%s</p></div></div>'
            % (cls, logo, bg, kicker, h1_html, LEDE, btn1, btn2, bandhtml, cols_label, cols, logo, title, "".join('<i style="background:%s" title="%s"></i>' % s for s in swatches), notes))


def build():
    css = """
    body{margin:0;background:#E9E5DA;color:#1E2621;font:14px/1.45 'DM Sans',system-ui;padding:44px 48px}
    h2{font:400 30px/1.05 'Hedvig Letters Serif';margin:0 0 6px;color:#26201C}p.in{max-width:84ch;color:#5B544C;margin:0 0 22px}
    .refs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:34px}.refs img{width:100%;height:230px;object-fit:cover;object-position:top;border-radius:10px;display:block}
    .refs .lab{font:600 11px/1 'DM Sans';letter-spacing:.08em;text-transform:uppercase;color:#5B544C;margin-top:8px}
    .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:start}.item{min-width:0}
    .card{position:relative;border-radius:10px;overflow:hidden;background:#fff;box-shadow:0 1px 0 rgba(0,0,0,.08)}
    .top{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 14px;font-size:9px;white-space:nowrap}.top .lk{height:16px;width:auto}.top .nav{letter-spacing:.02em}.top .cta{padding:5px 9px;border:1px solid currentColor;border-radius:999px}
    .hero{position:relative;padding:46px 18px 30px;min-height:250px;background-size:cover;background-position:center}.hero .scrim{position:absolute;inset:0}.hero .in{position:relative}
    .hero .k{display:block;font-size:9px;margin-bottom:10px;opacity:.85}.hero h1{margin:0 0 10px;font-size:26px;line-height:1.02;max-width:11ch}.hero p{margin:0 0 14px;font-size:10.5px;line-height:1.45;max-width:34ch;opacity:.9}
    .bt{display:flex;gap:10px;align-items:center;font-size:9.5px}.bt b{padding:8px 12px;border-radius:999px;font-weight:600}.bt i{font-style:normal;text-decoration:underline;text-underline-offset:3px}
    .about{padding:16px 14px 18px}.about .lab{display:inline-block;font-size:8.5px;margin-bottom:12px;color:#5B544C}.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.cols h4{margin:0 0 4px;font-size:9.5px;padding-top:7px;border-top:1.5px solid currentColor}.cols p{margin:0;font-size:8.5px;line-height:1.4;color:#5B544C}
    .foot{display:flex;align-items:center;gap:10px;padding:12px 14px;font-size:8px}.foot .lk2{height:14px;width:auto}
    .meta{padding:14px 2px 0}.meta h3{margin:0 0 6px;font:400 17px 'Hedvig Letters Serif';color:#26201C}.sw{display:flex;gap:5px;margin-bottom:8px}.sw i{display:block;width:18px;height:18px;border-radius:4px;border:1px solid rgba(0,0,0,.08)}.meta p{margin:0;font-size:11.5px;color:#5B544C;line-height:1.45}

    .band{display:flex;align-items:center;gap:8px;padding:10px 14px;font-size:8px}.band span{font-weight:600;white-space:nowrap}.band i{flex:1;height:16px;background:#fff;display:block}.band b{padding:5px 9px;font-size:7.5px;text-transform:uppercase;letter-spacing:.1em}
    .sl{color:#FAC800;font-weight:700;margin-right:3px}
    /* Maine Policy palette, Signature type */
    .m1 .top{background:#0F2E4D;color:#fff}.m1 .top .nav,.m1 .top .cta{text-transform:uppercase;letter-spacing:.1em;font-weight:700;font-size:7px;white-space:nowrap}.m1 .top .cta{background:#FAC800;color:#0F2E4D;border:0;border-radius:0}
    .m1 .hero{background:#0556A5;color:#fff;min-height:220px;padding-bottom:22px}.m1 h1{font:800 26px/1.02 'Bricolage Grotesque';letter-spacing:-.02em}.m1 h1 em{font-style:normal;color:#FAC800}.m1 .k{font:700 8px 'DM Sans';letter-spacing:.14em;text-transform:uppercase;color:#fff}
    .m1 .bt b{background:#FAC800;color:#0F2E4D;border-radius:0;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;font-weight:700}.m1 .bt i{color:#fff;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;text-decoration:none;border-bottom:1.5px solid #FAC800}
    .m1 .band{background:#0F2E4D;color:#fff}.m1 .band b{background:#0556A5;color:#fff}
    .m1 .about{background:#fff;color:#0F2E4D}.m1 .about .lab{background:#FAC800;color:#0F2E4D;padding:3px 7px;text-transform:uppercase;letter-spacing:.1em;font-weight:700}.m1 .cols h4{font:800 10px 'Bricolage Grotesque';border-top-color:#FAC800}.m1 .foot{background:#0F2E4D;color:#fff}
    /* Maine Policy palette, Bark & Sky type */
    .m2 .top{background:#0F2E4D;color:#fff}.m2 .top .nav,.m2 .top .cta{text-transform:uppercase;letter-spacing:.1em;font-weight:700;font-size:7px;font-family:'DM Sans';white-space:nowrap}.m2 .top .cta{background:#FAC800;color:#0F2E4D;border:0;border-radius:0}
    .m2 .hero{color:#fff;min-height:220px;padding-bottom:22px}.m2 .scrim{background:linear-gradient(90deg,rgba(5,86,165,.92),rgba(15,46,77,.55))}.m2 h1{font:400 27px/1.02 'Hedvig Letters Serif';text-transform:lowercase}.m2 h1 em{font-style:normal;color:#FAC800}.m2 .k{font:700 8px 'DM Sans';letter-spacing:.14em;text-transform:uppercase;color:#fff}
    .m2 .bt b{background:#FAC800;color:#0F2E4D;border-radius:0;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;font-family:'DM Sans';font-weight:700}.m2 .bt i{color:#fff;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;text-decoration:none;border-bottom:1.5px solid #FAC800;font-family:'DM Sans'}.m2 .hero p{font-family:'Hedvig Letters Sans'}
    .m2 .band{background:#0F2E4D;color:#fff;font-family:'DM Sans'}.m2 .band b{background:#0556A5;color:#fff}
    .m2 .about{background:#fff;color:#0F2E4D;font-family:'Hedvig Letters Sans'}.m2 .about .lab{background:#FAC800;color:#0F2E4D;padding:3px 7px;text-transform:uppercase;letter-spacing:.1em;font-weight:700;font-family:'DM Sans'}.m2 .cols h4{font:400 11px 'Hedvig Letters Serif';border-top-color:#0556A5}.m2 .foot{background:#0F2E4D;color:#fff;font-family:'Hedvig Letters Sans'}
    /* Signature as built */
    .s1 .top{background:#104836;color:#fff}.s1 .hero{background:#104836;color:#fff}.s1 h1{font:800 26px/1.02 'Bricolage Grotesque';letter-spacing:-.02em}.s1 .hero p{color:#fff}.s1 .k{font:600 9px 'DM Sans';color:#EFB443}
    .s1 .bt b{background:#fff;color:#104836}.s1 .bt i{color:#fff}.s1 .about{background:#fff;color:#1E2621}.s1 .cols h4{font:600 9.5px 'DM Sans'}.s1 .foot{background:#0B2B21;color:#D3DDD4}
    /* Signature, in the family */
    .s2 .top{background:#0F2E4D;color:#fff}.s2 .top .nav,.s2 .top .cta{text-transform:uppercase;letter-spacing:.1em;font-weight:600;font-size:7px;white-space:nowrap}.s2 .top .cta{background:#EFB443;color:#0F2E4D;border:0;border-radius:0}
    .s2 .hero{background:#0556A5;color:#fff}.s2 h1{font:800 26px/1.02 'Bricolage Grotesque';letter-spacing:-.02em}.s2 h1 em{font-style:normal;color:#EFB443}.s2 .k{font:600 8px 'DM Sans';letter-spacing:.14em;text-transform:uppercase;color:#fff}
    .s2 .bt b{background:#EFB443;color:#0F2E4D;border-radius:0;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px}.s2 .bt i{color:#fff;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;text-decoration:none;border-bottom:1.5px solid #EFB443}
    .s2 .about{background:#fff;color:#0F2E4D}.s2 .about .lab{background:#FFF7D9;color:#0F2E4D;padding:3px 7px;text-transform:uppercase;letter-spacing:.1em;font-weight:600}.s2 .cols h4{font:800 10px 'Bricolage Grotesque';border-top-color:#EFB443}.s2 .foot{background:#0F2E4D;color:#fff}
    /* Bark & Sky as built */
    .b1 .top{background:transparent;color:#F4F3EE;position:absolute;width:100%;box-sizing:border-box;z-index:2}.b1 .hero{color:#F4F3EE;padding-top:58px}.b1 .scrim{background:linear-gradient(90deg,rgba(38,32,28,.78),rgba(38,32,28,.2))}.b1 h1{font:400 27px/1.02 'Hedvig Letters Serif';text-transform:lowercase}.b1 .k{display:none}
    .b1 .bt b{background:#F4F3EE;color:#26201C;font-family:'Hedvig Letters Sans';font-weight:400}.b1 .bt i{color:#F4F3EE;font-family:'Hedvig Letters Sans'}.b1 .hero p{font-family:'Hedvig Letters Sans'}.b1 .about{background:#F4F3EE;color:#26201C;font-family:'Hedvig Letters Sans'}.b1 .cols h4{font:400 10px 'Hedvig Letters Sans'}.b1 .about .lab{display:none}.b1 .foot{background:#26201C;color:#B9C9D3;font-family:'Hedvig Letters Sans'}
    /* Bark & Sky, in the family */
    .b2 .top{background:#112337;color:#fff}.b2 .top .nav,.b2 .top .cta{text-transform:uppercase;letter-spacing:.1em;font-weight:600;font-size:7px;font-family:'DM Sans';white-space:nowrap}.b2 .top .cta{background:#EFB443;color:#112337;border:0;border-radius:0}
    .b2 .hero{color:#F4F3EE}.b2 .scrim{background:linear-gradient(90deg,rgba(17,35,55,.86),rgba(17,35,55,.35))}.b2 h1{font:400 27px/1.02 'Hedvig Letters Serif';text-transform:lowercase}.b2 .k{font:600 8px 'DM Sans';letter-spacing:.14em;text-transform:uppercase;color:#EFB443}
    .b2 .bt b{background:#EFB443;color:#112337;border-radius:0;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;font-family:'DM Sans'}.b2 .bt i{color:#fff;text-transform:uppercase;letter-spacing:.1em;font-size:8.5px;text-decoration:none;border-bottom:1.5px solid #EFB443;font-family:'DM Sans'}.b2 .hero p{font-family:'Hedvig Letters Sans'}
    .b2 .about{background:#fff;color:#112337;font-family:'Hedvig Letters Sans'}.b2 .about .lab{background:#E4E8E6;color:#112337;padding:3px 7px;text-transform:uppercase;letter-spacing:.1em;font-weight:600;font-family:'DM Sans'}.b2 .cols h4{font:400 11px 'Hedvig Letters Serif';border-top-color:#006CB5}.b2 .foot{background:#112337;color:#B9C9D3;font-family:'Hedvig Letters Sans'}
    """
    refs = "".join('<div><img src="file://%s"><div class="lab">%s</div></div>' % (os.path.join(REF, p), l) for p, l in (("mpi/mpi-home.png", "Maine Policy Institute"), ("wire/wire-1.png", "The Maine Wire"), ("mca/mca-1.png", "Maine Civic Action")))
    cards = [
        mock("s1", svg_data(os.path.join(LOGO_S, "lockup-compact-reversed.svg")), "Signature, as built",
             H1, "Made in Maine", "Watch the stories", "Get the newsletter", "", [("#104836", "Spruce"), ("#0B2B21", "Pine"), ("#EFB443", "Marigold"), ("#D3DDD4", "Sage"), ("#FFFFFF", "Snow")],
             "Spruce and pine with one marigold accent. Bricolage Grotesque 800 and DM Sans. Pills, rounded corners, the lined state as the mark. Stands apart from the family on purpose."),
        mock("s2", svg_data(os.path.join(LOGO_S, "lockup-compact-reversed.svg")), "Signature, in the family",
             "Young Mainers on <em>building a life here</em>", "Generation Maine", "Watch the stories", "Get the newsletter", "What it is", [("#0F2E4D", "Navy"), ("#0556A5", "Blue"), ("#EFB443", "Marigold"), ("#FFF7D9", "Marigold tint"), ("#FFFFFF", "White")],
             "The greens become Maine Policy's navy and blue; marigold stays as the one warm accent, where the parent uses yellow and Civic Action uses coral. Same Bricolage headline with the second line in the accent, the way the parent sets its heroes. Uppercase labels, flat buttons, hard corners, boxed section label. The lined state mark stays in marigold."),
        mock("b1", svg_data(os.path.join(LOGO_B, "wordmark-reversed.svg")), "Bark & Sky, as built",
             H1, "", "watch the stories", "get the newsletter", "", [("#26201C", "Bark"), ("#B9C9D3", "Sky"), ("#F4F3EE", "Paper"), ("#E4E8E6", "Mist"), ("#5B544C", "Clay")],
             "Bark, Sky and Paper. Hedvig Letters Serif lowercase at one weight, Hedvig Sans for reading. No labels, no uppercase, pills, a photographic hero. The quietest thing in the room, and the furthest from the family.", HERO),
        mock("b2", svg_data(os.path.join(LOGO_B, "wordmark-reversed.svg"), "#FFFFFF"), "Bark & Sky, in the family",
             H1, "Generation Maine", "watch the stories", "get the newsletter", "What it is", [("#112337", "Navy"), ("#006CB5", "Blue"), ("#EFB443", "Marigold"), ("#B9C9D3", "Sky"), ("#F4F3EE", "Paper")],
             "Bark becomes Civic Action's navy; Sky stays as the secondary; marigold arrives as the warm accent on flat buttons. The serif headline stays lowercase, which keeps the voice, but navigation, labels and buttons go uppercase in a sans like the siblings. Hard corners, boxed section label, photographic hero under a navy scrim. The wordmark goes white.", HERO),
    ]
    cards2 = [
        mock("m1", svg_data(os.path.join(LOGO_S, "lockup-compact-reversed.svg")), "Maine Policy's palette, Signature type",
             "Young Mainers on <em>building a life here</em>", "Your voice for what it costs to stay", "Watch the stories", "Get the newsletter", "What it is", [("#0F2E4D", "Navy"), ("#0556A5", "Blue"), ("#FAC800", "Yellow"), ("#2191FF", "Light blue"), ("#FFFFFF", "White")],
             "The parent's own blue, navy and yellow, the slash kicker, the yellow second line, the navy sign-up band under the hero, yellow section label. Only the Bricolage headline and the lined state mark say Generation Maine. Reads as a Maine Policy program page.", band=True, slash=True),
        mock("m2", svg_data(os.path.join(LOGO_B, "wordmark-reversed.svg"), "#FFFFFF"), "Maine Policy's palette, Bark & Sky type",
             "young mainers on <em>building a life here</em>", "Your voice for what it costs to stay", "watch the stories", "get the newsletter", "What it is", [("#0F2E4D", "Navy"), ("#0556A5", "Blue"), ("#FAC800", "Yellow"), ("#B9C9D3", "Sky"), ("#FFFFFF", "White")],
             "The same parent parts with the lowercase serif and the photograph under a blue scrim. Yellow second line in the serif, slash kicker, sign-up band. The serif is the only thing keeping it from being the parent site; it is also what makes the yellow feel borrowed.", HERO, band=True, slash=True),
    ]
    page = ('<!doctype html><meta charset="utf-8"><title>family sheet</title><style>%s%s</style>'
            '<h2>living with the family</h2><p class="in">Top row: the parent properties as they are today (headless fonts fell back to Arial, so read color and layout). Below: each concept as built, and a version that could sit beside them. Shared family rules applied to both: navy top bar, a blue primary, one warm accent carried by flat buttons, uppercase letterspaced labels and navigation, hard corners, a boxed section label. Each concept keeps its own typeface and its own voice.</p>'
            '<div class="refs">%s</div><div class="grid">%s</div>'
            '<h2 style="margin-top:40px">closer still: Maine Policy\'s own palette and parts</h2><p class="in">Two more alternates that take the parent\'s actual colors (blue, navy, yellow) and its page parts (the slash kicker, the yellow second line, the navy sign-up band, the yellow section label), one in each concept\'s typeface. Footers on every card now carry the Maine Policy credit.</p>'
            '<div class="grid">%s</div>') % (FONTS, css, refs, "".join(cards), "".join(cards2))
    out = os.path.join(ROOT, "brand", "identity", "family-sheet.html")
    write(out, page)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(ROOT, "brand", "identity", "family-sheet.png"), "1600", "1.5"], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build()
