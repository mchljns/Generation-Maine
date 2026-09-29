"""Builds brand/directions.html: both creative directions side by side, self-contained.

Also prints the WCAG contrast ratios used in brand/02-directions.md.
Run from the repo root: python3 brand/src/build_directions.py
"""
import base64
import os

from gmlib import A, ROOT, Face, contours, contour_group, write
from build_brand import icon_mark, lockup_stacked, lockup_horizontal

B = {
    "ink": "#141414",
    "newsprint": "#ECECE6",
    "blueberry": "#3D2FD1",
    "highlighter": "#FFD23F",
    "white": "#FFFFFF",
}

COND = Face(os.path.join(ROOT, "brand/fonts/alt/Anton-Regular.ttf"))


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


PAIRS_A = [("ink", "fog"), ("spruce", "fog"), ("fog", "spruce"), ("dawn", "spruce"),
           ("ink", "signal"), ("signal_deep", "fog"), ("signal", "spruce"), ("signal", "fog")]
PAIRS_B = [("ink", "newsprint"), ("blueberry", "newsprint"), ("white", "blueberry"),
           ("ink", "highlighter"), ("blueberry", "highlighter"), ("highlighter", "newsprint")]


def verdict(r):
    return "Passes AA" if r >= 4.5 else ("Large text only (AA 3:1)" if r >= 3 else "Fails, decoration only")


def pair_rows(pal, pairs):
    rows = ""
    for fg, bg in pairs:
        r = ratio(pal[fg], pal[bg])
        rows += ('<tr><td><span class="chip" style="background:%s;color:%s">Aa</span></td>'
                 "<td>%s on %s</td><td>%.2f:1</td><td>%s</td></tr>" % (pal[bg], pal[fg], fg, bg, r, verdict(r)))
    return rows


def b_logo_stacked(x, y, size, ink, hl):
    d1, w1 = COND.path("GENERATION", size, x, y + size * 0.72, 10)
    d2, w2 = COND.path("MAINE", size, x, y + size * 0.72 + size * 0.86, 10)
    hy = y + size * 0.86 + size * 0.06
    swipe = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" transform="rotate(-3 %.1f %.1f)"/>'
             % (x - size * 0.08, hy, w2 + size * 0.16, size * 0.78, hl, x, hy))
    return swipe + '<path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (ink, d1, ink, d2), max(w1, w2)


def b_icon(cx, cy, size, ink, hl):
    d, w = COND.path("GM", size, 0, 0, 10)
    s = size / COND.upem
    return ('<g transform="rotate(-4 %.1f %.1f)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
            '<path transform="translate(%.1f %.1f)" fill="%s" d="%s"/></g>'
            % (cx, cy, cx - w / 2 - size * 0.14, cy - size * 0.5, w + size * 0.28, size * 0.92, hl,
               cx - w / 2, cy + size * 0.33, ink, d))


def svgwrap(w, h, body, label):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (w, h, label, body))


def font64(name):
    with open(os.path.join(ROOT, "generation-maine/assets/fonts", name), "rb") as f:
        return base64.b64encode(f.read()).decode()


def build():
    a, b = A, B
    # Direction A mockups
    a_avatar = svgwrap(512, 512, '<rect width="512" height="512" fill="%s"/>' % a["spruce"]
                       + icon_mark(256, 256, 360, a["fog"], a["signal"]), "Direction A avatar")
    body = '<rect width="1080" height="1920" fill="%s"/>' % a["spruce"]
    body += contour_group(contours(900, 1700, 18, 50, 52, 4), a["moss"], 3, 0.6)
    wm, w, h = lockup_stacked(a["fog"], a["signal"], 100)
    body += '<g transform="translate(160 560) scale(%.3f)">%s</g>' % (760 / w, wm)
    wm2, w2, h2 = lockup_horizontal(a["dawn"], a["dawn"], 100)
    body += ('<text x="160" y="1060" font-size="64" fill="%s" style="font-family:GMDisplay">Follow Generation Maine</text>'
             '<text x="160" y="1150" font-size="44" fill="%s" style="font-family:GMBody">[@handle] on Instagram, TikTok, YouTube</text>'
             '<text x="160" y="1520" font-size="34" fill="%s" style="font-family:GMBody">An initiative of Maine Policy Institute</text>'
             % (a["dawn"], a["fog"], a["fog"]))
    a_end = svgwrap(1080, 1920, body, "Direction A end card")
    a_contours = contour_group(contours(640, 60, 14, 30, 38, 11), a["moss"], 2, 0.8)

    # Direction B mockups
    b_avatar = svgwrap(512, 512, '<rect width="512" height="512" fill="%s"/>' % b["newsprint"]
                       + b_icon(256, 256, 260, b["ink"], b["highlighter"]), "Direction B avatar")
    body = '<rect width="1080" height="1920" fill="%s"/>' % b["newsprint"]
    lg, lw = b_logo_stacked(0, 0, 200, b["ink"], b["highlighter"])
    body += '<g transform="translate(110 520) scale(%.3f)">%s</g>' % (860 / lw, lg)
    body += ('<rect x="110" y="1000" width="860" height="8" fill="%s"/>'
             '<text x="110" y="1100" font-size="54" fill="%s" style="font-family:GMCond;letter-spacing:1px">FOLLOW GENERATION MAINE</text>'
             '<text x="110" y="1180" font-size="38" fill="%s" style="font-family:GMMono">[@handle]</text>'
             '<text x="110" y="1520" font-size="30" fill="%s" style="font-family:GMMono">An initiative of Maine Policy Institute</text>'
             % (b["ink"], b["blueberry"], b["ink"], b["ink"]))
    b_end = svgwrap(1080, 1920, body, "Direction B end card")
    b_hero_logo, blw = b_logo_stacked(0, 0, 100, b["ink"], b["highlighter"])

    wm_a, wa, ha = lockup_horizontal(a["fog"], a["signal"], 100)

    def swatches(pal, names):
        return "".join('<div class="sw"><span style="background:%s"></span><b>%s</b><code>%s</code></div>'
                       % (pal[n], n.replace("_", " ").title(), pal[n]) for n in names)

    html = TEMPLATE
    repl = {
        "{{FONT_DISPLAY}}": font64("bricolage-grotesque-800.woff2"),
        "{{FONT_BODY}}": font64("inter-var.woff2"),
        "{{FONT_COND}}": font64("anton-400.woff2"),
        "{{FONT_MONO}}": font64("plex-mono-500.woff2"),
        "{{A_AVATAR}}": a_avatar, "{{A_END}}": a_end, "{{B_AVATAR}}": b_avatar, "{{B_END}}": b_end,
        "{{A_WORDMARK}}": svgwrap(round(wa), round(ha), wm_a, "Generation Maine"),
        "{{A_CONTOURS}}": a_contours,
        "{{B_LOGO}}": svgwrap(round(blw) + 20, 200, '<g transform="translate(10 8)">%s</g>' % b_hero_logo, "Generation Maine"),
        "{{A_SWATCHES}}": swatches(a, ["spruce", "fog", "signal", "moss", "dawn", "ink", "signal_deep"]),
        "{{B_SWATCHES}}": swatches(b, ["ink", "newsprint", "blueberry", "highlighter"]),
        "{{A_PAIRS}}": pair_rows(a, PAIRS_A), "{{B_PAIRS}}": pair_rows(b, PAIRS_B),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    for k, v in A.items():
        html = html.replace("{{A.%s}}" % k, v)
    for k, v in B.items():
        html = html.replace("{{B.%s}}" % k, v)
    write("brand/directions.html", html)

    print("Direction A")
    for fg, bg in PAIRS_A:
        print("  %-12s on %-8s %5.2f:1  %s" % (fg, bg, ratio(a[fg], a[bg]), verdict(ratio(a[fg], a[bg]))))
    print("Direction B")
    for fg, bg in PAIRS_B:
        print("  %-12s on %-11s %5.2f:1  %s" % (fg, bg, ratio(b[fg], b[bg]), verdict(ratio(b[fg], b[bg]))))


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine: two creative directions</title>
<style>
@font-face{font-family:GMDisplay;src:url(data:font/woff2;base64,{{FONT_DISPLAY}}) format("woff2");font-weight:800}
@font-face{font-family:GMBody;src:url(data:font/woff2;base64,{{FONT_BODY}}) format("woff2");font-weight:400 700}
@font-face{font-family:GMCond;src:url(data:font/woff2;base64,{{FONT_COND}}) format("woff2");font-weight:400 900}
@font-face{font-family:GMMono;src:url(data:font/woff2;base64,{{FONT_MONO}}) format("woff2");font-weight:500}
:root{--page:#f6f6f3;--text:#161616;--muted:#555}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--text);font:16px/1.55 GMBody,system-ui,sans-serif}
header.top{max-width:1320px;margin:0 auto;padding:48px 24px 8px}
header.top h1{font:800 clamp(32px,4vw,52px)/1.05 GMDisplay,sans-serif;margin:0 0 8px}
header.top p{max-width:720px;color:var(--muted);margin:0}
.grid{max-width:1320px;margin:0 auto;padding:24px;display:grid;grid-template-columns:1fr 1fr;gap:28px}
@media (max-width:980px){.grid{grid-template-columns:1fr}}
.dir{background:#fff;border-radius:20px;padding:28px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.tag{display:inline-block;font:600 12px/1 GMBody;letter-spacing:.08em;text-transform:uppercase;padding:6px 10px;border-radius:99px;background:#eee}
.tag.pick{background:{{A.signal}};color:{{A.ink}}}
.dir h2{margin:12px 0 4px;font-size:30px;line-height:1.1}
.dirA h2{font-family:GMDisplay;font-weight:800}
.dirB h2{font-family:GMCond;font-weight:900;text-transform:uppercase;letter-spacing:.01em;font-size:36px}
h3{font-size:14px;letter-spacing:.06em;text-transform:uppercase;margin:24px 0 8px;color:var(--muted)}
.mocks{display:grid;grid-template-columns:120px 150px 1fr;gap:16px;align-items:start;margin-top:16px}
@media (max-width:620px){.mocks{grid-template-columns:120px 1fr}.mocks .hero{grid-column:1/-1}}
.avatar svg{width:120px;height:120px;border-radius:50%;display:block}
.endcard svg{width:150px;height:auto;border-radius:12px;display:block}
.cap{font-size:12px;color:var(--muted);margin-top:6px}
.hero{border-radius:14px;overflow:hidden;position:relative;min-height:266px}
.heroA{background:{{A.spruce}};color:{{A.fog}};padding:22px}
.heroA .pat{position:absolute;inset:0;width:100%;height:100%}
.heroA .in{position:relative}
.heroA .wm{width:150px;display:block;margin-bottom:26px}
.heroA .eyebrow{font:600 11px/1 GMBody;letter-spacing:.08em;text-transform:uppercase;color:{{A.dawn}}}
.heroA .h{font:800 28px/1.02 GMDisplay;margin:8px 0 10px;max-width:14ch}
.heroA .sub{font-size:13px;max-width:34ch;margin:0 0 14px}
.btnA{display:inline-block;background:{{A.signal}};color:{{A.ink}};font:600 13px/1 GMBody;padding:10px 14px;border-radius:99px}
.btnA2{display:inline-block;border:2px solid {{A.fog}};color:{{A.fog}};font:600 13px/1 GMBody;padding:8px 14px;border-radius:99px;margin-left:6px}
.heroB{background:{{B.newsprint}};color:{{B.ink}};padding:22px;border:2px solid {{B.ink}}}
.heroB .logo svg{height:60px;width:auto;display:block;margin-bottom:18px}
.heroB .eyebrow{font:500 11px/1 GMMono;text-transform:uppercase;color:{{B.blueberry}}}
.heroB .h{font:900 38px/.95 GMCond;text-transform:uppercase;margin:8px 0 10px}
.heroB .sub{font:500 12px/1.5 GMMono;max-width:40ch;margin:0 0 14px}
.btnB{display:inline-block;background:{{B.blueberry}};color:#fff;font:500 12px/1 GMMono;padding:10px 14px;text-transform:uppercase}
.btnB2{display:inline-block;background:{{B.highlighter}};color:{{B.ink}};font:500 12px/1 GMMono;padding:10px 14px;text-transform:uppercase;margin-left:6px}
.sws{display:flex;flex-wrap:wrap;gap:10px}
.sw{width:112px;font-size:12px}
.sw span{display:block;height:56px;border-radius:10px;border:1px solid rgba(0,0,0,.1);margin-bottom:6px}
.sw b{display:block}.sw code{color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:13px}
td{padding:6px 8px;border-bottom:1px solid #eee;vertical-align:middle}
.chip{display:inline-block;width:40px;text-align:center;padding:4px 0;border-radius:6px;font-weight:700;border:1px solid rgba(0,0,0,.1)}
.typeA .d{font:800 34px/1.05 GMDisplay}.typeA .b{font:400 15px/1.5 GMBody}
.typeB .d{font:900 40px/1 GMCond;text-transform:uppercase}.typeB .b{font:500 14px/1.5 GMMono}
dl{margin:0}dt{font-weight:700;margin-top:10px}dd{margin:2px 0 0}
footer{max-width:1320px;margin:0 auto;padding:8px 24px 48px;color:var(--muted);font-size:14px}
</style>
</head>
<body>
<header class="top">
  <h1>Generation Maine: two creative directions</h1>
  <p>Two different concepts for the same project. Each shows the logo as a round social avatar, a 9:16 video end card and the website hero. Direction A is the recommended pick. The written rationale is in brand/02-directions.md.</p>
</header>
<main class="grid">
<section class="dir dirA" aria-labelledby="da">
  <span class="tag pick">Recommended</span>
  <h2 id="da">A. Spruce &amp; Signal</h2>
  <p>Maine's working landscape, drawn as clean contour lines, with one bright orange dot that reads as a camera's record light. It feels local and current without using a single postcard cliché.</p>
  <div class="mocks">
    <div class="avatar">{{A_AVATAR}}<div class="cap">Avatar, circle crop</div></div>
    <div class="endcard">{{A_END}}<div class="cap">9:16 end card</div></div>
    <div class="hero heroA"><svg class="pat" viewBox="0 0 700 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{{A_CONTOURS}}</svg>
      <div class="in"><div class="wm">{{A_WORDMARK}}</div>
      <div class="eyebrow">An initiative of Maine Policy Institute</div>
      <div class="h">Young Mainers on building a life here</div>
      <p class="sub">Short videos by young Maine creators about rent, work and staying.</p>
      <span class="btnA">Meet the creators</span><span class="btnA2">Follow along</span></div>
    </div>
  </div>
  <h3>Moodboard (words)</h3>
  <p>Trail map contour lines. Spruce woods at dusk. The orange of a hunter's cap, a buoy line or a trail blaze. Fog over a harbor town at 7 a.m. Phone footage shot in a kitchen, a garage workshop, a first apartment. Clean sans type on a flat green field.</p>
  <h3>Logo approach</h3>
  <p>Wordmark plus a small symbol. The wordmark says the name in full, which matters for a new project. The orange dot on the i in "Maine" works as a record light and carries into the G icon for avatars.</p>
  <h3>Type</h3>
  <div class="typeA"><div class="d">Bricolage Grotesque</div><div class="b">Inter for body text. Both under the SIL Open Font License 1.1.</div></div>
  <h3>Palette</h3>
  <div class="sws">{{A_SWATCHES}}</div>
  <h3>Contrast (calculated)</h3>
  <table>{{A_PAIRS}}</table>
  <h3>Risk</h3>
  <p>Green and orange is a friendly, outdoorsy pairing and could drift toward an outfitter or a state park look. The contour lines and the record dot have to be used consistently to keep it tied to storytelling.</p>
</section>
<section class="dir dirB" aria-labelledby="db">
  <span class="tag">Alternate</span>
  <h2 id="db">B. Paper Route</h2>
  <p>A photocopied zine made by kids in a small town: condensed headlines, typewriter captions and a highlighter swipe. It feels handmade and a little loud, like the creators made it themselves.</p>
  <div class="mocks">
    <div class="avatar">{{B_AVATAR}}<div class="cap">Avatar, circle crop</div></div>
    <div class="endcard">{{B_END}}<div class="cap">9:16 end card</div></div>
    <div class="hero heroB">
      <div class="logo">{{B_LOGO}}</div>
      <div class="eyebrow">An initiative of Maine Policy Institute</div>
      <div class="h">Young Mainers on building a life here</div>
      <p class="sub">Short videos by young Maine creators about rent, work and staying.</p>
      <span class="btnB">Meet the creators</span><span class="btnB2">Follow along</span>
    </div>
  </div>
  <h3>Moodboard (words)</h3>
  <p>Photocopied flyers on a coffee shop corkboard. Highlighter on newsprint. Label maker tape. Wild blueberry blue. Handwritten notes in the margins of a lease. Black and white photos with one bright color on top.</p>
  <h3>Logo approach</h3>
  <p>Stacked wordmark in condensed capitals with a highlighter swipe behind "MAINE". The avatar is a "GM" sticker set at a slight angle. It relies on type and a single gesture, so it is easy to copy in Canva.</p>
  <h3>Type</h3>
  <div class="typeB"><div class="d">Anton</div><div class="b">IBM Plex Mono for captions. Both under the SIL Open Font License 1.1.</div></div>
  <h3>Palette</h3>
  <div class="sws">{{B_SWATCHES}}</div>
  <h3>Contrast (calculated)</h3>
  <table>{{B_PAIRS}}</table>
  <h3>Risk</h3>
  <p>Zine styling is common in youth media and can look dated in two years. It can also read as unserious next to a policy institute's name. The highlighter yellow fails contrast on light backgrounds, so it can only sit behind dark text.</p>
</section>
</main>
<footer>Mockups use placeholder copy. Fonts are embedded so this file works offline.</footer>
</body>
</html>
"""

if __name__ == "__main__":
    build()
