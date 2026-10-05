"""Where marigold works. Marigold fails as text on light fields, so this sheet shows the places it carries weight:
as a field with navy on it, on navy, as a button, a rule, a tag, a sticker, a clip caption band, an avatar.
  python3 brand/src/build_marigold_apps.py
"""
import base64, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import maine2
from build_slant16 import slant16
from build_family_marks import word, svg

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family")
NAVY, BLUE, MG, PAPER, WHITE = "#0F2E4D", "#0556A5", "#EFB443", "#F4F3EE", "#FFFFFF"
KW = dict(angle=62, fill=0.62, accent_at=10)
HERO = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media", "hero-poster.jpg")
PORTRAIT = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media", "portrait-2.jpg")


def mark_svg(fg, acc, h, idn):
    body, w, _ = slant16(h, fg, acc, idn=idn, **(KW if acc else dict(KW, accent_at=-1)))
    return svg(w, h, body)

def lockup_svg(fg, second, acc, idn):
    mk, mw, _ = slant16(100, fg, acc, idn=idn, **KW)
    t1, w1 = word("Generation ", 70, fg, mw + 26, 80); t2, w2 = word("Maine", 70, second, mw + 26 + w1, 80)
    return svg(mw + 26 + w1 + w2 + 4, 100, mk + t1 + t2)

def data(s): return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


def build():
    m_navy_on_mg = data(mark_svg(NAVY, NAVY, 240, "a"))          # one color navy, for the marigold field
    m_white_mg = data(mark_svg(WHITE, MG, 240, "b"))             # white with marigold stripe, for navy
    lk_navy_field = data(lockup_svg(NAVY, NAVY, NAVY, "c"))      # navy one color on marigold
    lk_on_navy = data(lockup_svg(WHITE, MG, MG, "d"))
    lk_on_paper = data(lockup_svg(NAVY, BLUE, BLUE, "e"))
    css = """
    body{margin:0;background:#E9E5DA;color:#0F2E4D;font:15px/1.5 'DM Sans',system-ui;padding:48px 56px}
    h1{font:800 34px/1.05 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 8px}p.in{max-width:84ch;color:#4B5A68;margin:0 0 24px}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.c{border-radius:12px;overflow:hidden;background:#fff}.c .v{height:230px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
    .c .n{padding:12px 14px 14px}.c .n b{display:block;font-weight:700;font-size:14px}.c .n p{margin:3px 0 0;font-size:12px;color:#4B5A68;line-height:1.45}
    .mg{background:#EFB443}.nv{background:#0F2E4D}.bl{background:#0556A5}.pa{background:#F4F3EE}
    .up{font:700 11px/1 'DM Sans';letter-spacing:.12em;text-transform:uppercase}
    .btn{display:inline-block;padding:14px 22px;background:#EFB443;color:#0F2E4D}.btn2{display:inline-block;padding:14px 22px;background:#0F2E4D;color:#fff;margin-left:10px}
    .tag{display:inline-block;padding:5px 9px;background:#EFB443;color:#0F2E4D}
    .h1{font:800 34px/1 'Bricolage Grotesque';letter-spacing:-.02em;color:#fff}.h1 em{font-style:normal;color:#EFB443}
    .rule{width:72px;height:4px;background:#EFB443}
    .card{width:200px;height:200px;border-radius:10px;overflow:hidden;position:relative;background:#333}.card img{width:100%;height:100%;object-fit:cover;display:block}
    .band{position:absolute;left:0;right:0;bottom:0;background:#EFB443;color:#0F2E4D;padding:10px 12px;font:600 12px/1.3 'DM Sans'}
    .stk{width:150px;height:150px;border-radius:50%;background:#EFB443;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(0,0,0,.18)}
    .av{width:110px;height:110px;border-radius:50%;background:#EFB443;display:flex;align-items:center;justify-content:center}
    .hero{position:absolute;inset:0;background:url(file://HERO) center/cover}.scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,46,77,.9),rgba(15,46,77,.4))}
    .in{position:relative;padding:22px}
    .quote{font:800 24px/1.1 'Bricolage Grotesque';letter-spacing:-.01em;color:#0F2E4D;max-width:26ch}.quote small{display:block;font:600 11px/1 'DM Sans';letter-spacing:.1em;text-transform:uppercase;margin-top:12px;color:#0F2E4D}
    .stat{font:800 64px/1 'Bricolage Grotesque';color:#EFB443;letter-spacing:-.03em}.stat small{display:block;font:600 12px/1.3 'DM Sans';color:#fff;margin-top:8px;letter-spacing:.06em;text-transform:uppercase}
    """.replace("HERO", HERO)
    fonts = "@font-face{font-family:'Bricolage Grotesque';font-weight:800;src:url(file://%s)}@font-face{font-family:'DM Sans';font-weight:100 900;src:url(file://%s)}" % (
        os.path.join(ROOT, "brand", "fonts", "BricolageGrotesque-ExtraBold.ttf"), os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"))
    cards = [
        ("mg", '<img src="%s" style="height:150px">' % m_navy_on_mg, "The mark on a marigold field", "Navy on marigold is 7.4:1. The field carries the color and the mark stays one color. Sticker, pin, social tile."),
        ("mg", '<img src="%s" style="height:52px">' % lk_navy_field, "The lockup on a marigold field", "One-color navy lockup on the yellow. The loudest version of the brand, for a banner or a shirt."),
        ("nv", '<img src="%s" style="height:52px">' % lk_on_navy, "On navy, second word in marigold", "7.4:1. The site footer and the end card."),
        ("bl", '<div class="in"><div class="h1">Young Mainers on <em>building a life here</em></div></div>', "Hero headline, last line in marigold", "The parent's own move. Large type on blue, 3.9:1, which passes for display sizes."),
        ("pa", '<div class="in"><span class="up btn">Watch the stories</span><span class="up btn2">Newsletter</span></div>', "Buttons", "Marigold button with navy text is the one place marigold lives on a light page. The secondary is navy."),
        ("pa", '<div class="in"><span class="up tag">What it is</span><div style="height:14px"></div><div class="rule"></div><div style="font:800 18px \'Bricolage Grotesque\';margin-top:10px">Who makes it</div></div>', "Tag and rule", "Section label as a marigold tag with navy text, and a short marigold rule under column heads. Shape, not text."),
        ("pa", '<div class="card"><img src="file://%s"><div class="band">Three apartments in town. One I could afford. Here is what the lease said.</div></div>' % PORTRAIT, "Clip caption band", "The caption band on every creator clip in marigold with navy text. Readable over any footage, and it makes the clips recognizably ours in a feed."),
        ("nv", '<div class="in"><div class="stat">9<small>towns, nine creators</small></div></div>', "A number in marigold on navy", "Big figures in marigold on the dark field, for the newsletter and slides."),
        ("pa", '<div class="in"><div class="quote">“I came back after two years in Portland. My first video was about the three apartments I could look at and the one I could afford.”<small>Maya, Skowhegan</small></div></div>'.replace('class="in"', 'class="in" style="background:#EFB443;height:100%;width:100%;box-sizing:border-box;display:flex;align-items:center"'), "Pull quote on a marigold panel", "Navy type on the yellow panel. The quotes section of the page, or a social quote card."),
        ("nv", '<div class="hero"></div><div class="scrim"></div><div class="in" style="color:#fff"><span class="up" style="color:#EFB443">A Maine Policy Institute project</span><div class="h1" style="margin-top:10px;font-size:28px">Young Mainers on <em>building a life here</em></div></div>', "Over photography", "Kicker in marigold over a navy scrim, headline white with the last line in marigold."),
        ("pa", '<div class="stk"><img src="%s" style="height:96px"></div>' % m_navy_on_mg, "Sticker", "The round marigold sticker with the navy state. The laptop in the Lewiston coffee shop."),
        ("pa", '<div style="display:flex;gap:18px;align-items:center"><div class="av"><img src="%s" style="height:70px"></div><div class="av" style="background:#0F2E4D"><img src="%s" style="height:70px"></div></div>' % (m_navy_on_mg, m_white_mg), "Avatars", "Marigold field with the navy state, or navy field with the white state and marigold stripe. Both read at 40 px."),
    ]
    h = ['<!doctype html><meta charset="utf-8"><title>marigold</title><style>%s%s</style>' % (css, fonts)]
    h.append("<h1>Where the marigold works</h1><p class='in'>Marigold cannot be text on a light field, so it does its work as a field, a button, a band, a tag, a rule, and as the second color on navy and blue. Twelve applications.</p><div class='grid'>")
    for cls, inner, title, note in cards:
        h.append("<div class='c'><div class='v %s'>%s</div><div class='n'><b>%s</b><p>%s</p></div></div>" % (cls, inner, title, note))
    h.append("</div>")
    out = os.path.join(OUT, "marigold-apps.html"); write(out, "".join(h))
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), out, os.path.join(OUT, "marigold-apps.png"), "1500", "1.4"], check=True)
    print("wrote", out)

if __name__ == "__main__":
    build()
