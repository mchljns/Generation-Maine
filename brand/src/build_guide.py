"""Builds brand/brand-guide.html (self-contained). Export to PDF with: node brand/src/guide-pdf.mjs"""
import base64
import os

from gmlib import A, ROOT, contours, contour_group, write
from build_brand import icon_mark, lockup_horizontal, lockup_stacked
from build_directions import ratio

C = A


def f64(name):
    with open(os.path.join(ROOT, "generation-maine/assets/fonts", name), "rb") as f:
        return base64.b64encode(f.read()).decode()


def svg(w, h, body, label="", cls=""):
    return ('<svg class="%s" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">%s</svg>'
            % (cls, w, h, label, body))


def logo(kind, fg, dot, pad=0):
    if kind == "icon":
        return svg(512, 512, icon_mark(256, 256, 400, fg, dot), "Icon")
    fn = lockup_horizontal if kind == "primary" else lockup_stacked
    body, w, h = fn(fg, dot, 100, pad)
    return svg(round(w), round(h), body, "Generation Maine")


ICONS = {
    "Housing": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M10 20v-5h4v5"/>',
    "Jobs": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 12h18"/>',
    "Cost of living": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "Small business": '<path d="M4 9l1-5h14l1 5M4 9h16M5 9v11h14V9M10 20v-5h4v5"/>',
    "Place": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "Video": '<rect x="3" y="7" width="12" height="10" rx="2"/><path d="M15 11l6-3v8l-6-3z"/>',
}


def icon_svg(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-label="%s" role="img">%s</svg>' % (C["spruce"], name, ICONS[name]))


def misuse():
    body, w, h = lockup_horizontal(C["spruce"], C["lupine"], 100)
    blue, _, _ = lockup_horizontal(C["spruce"], "#2B59C3", 100)
    fogfg, _, _ = lockup_horizontal(C["moss"], C["lupine"], 100)
    W, H = round(w), round(h)
    cases = [
        ("Do not stretch or squash it", '<g transform="scale(1 1.6) translate(0 -14)">%s</g>' % body, C["fog"]),
        ("Do not change the dot color", blue, C["fog"]),
        ("Do not rotate it", '<g transform="translate(30 30) rotate(-6 350 37) scale(.9)">%s</g>' % body, C["fog"]),
        ("Do not add shadows or effects",
         '<defs><filter id="sh"><feDropShadow dx="6" dy="6" stdDeviation="3" flood-opacity=".5"/></filter></defs>'
         '<g filter="url(#sh)">%s</g>' % body, C["fog"]),
        ("Do not place it on low-contrast colors", fogfg, C["spruce"]),
        ("Do not retype it in another font",
         '<text x="0" y="62" font-size="74" font-family="Georgia, serif" fill="%s">Generation Maine</text>'
         % C["spruce"], C["fog"]),
    ]
    out = ""
    for label, b, bg in cases:
        out += ('<figure class="mis"><div class="mis-art" style="background:%s">%s<span class="x" aria-hidden="true"></span></div>'
                '<figcaption>%s</figcaption></figure>' % (bg, svg(W, H + 110, '<g transform="translate(0 55)">%s</g>' % b, label), label))
    return out


def build():
    pat_cover = contour_group(contours(1000, 80, 18, 30, 44, 11), C["moss"], 2, 0.8)
    pat_demo = contour_group(contours(420, 160, 14, 20, 30, 7), C["moss"], 2, 0.8)
    pat_small = contour_group(contours(200, 110, 8, 14, 24, 5), C["moss"], 2, 0.9)

    pairs = [("ink", "fog"), ("spruce", "fog"), ("fog", "spruce"), ("blossom", "spruce"), ("ink", "lupine"),
             ("lupine_deep", "fog"), ("moss", "white"), ("lupine", "spruce"), ("lupine", "fog")]
    rows = ""
    for fg, bg in pairs:
        r = ratio(C[fg], C[bg])
        v = "Passes AA, any size" if r >= 4.5 else ("Large text only (24 px+, or 19 px bold)" if r >= 3 else "Never for text")
        rows += ('<tr><td><span class="chip" style="background:%s;color:%s">Aa</span></td><td>%s on %s</td>'
                 '<td>%.2f:1</td><td>%s</td></tr>' % (C[bg], C[fg], fg.replace("_", " ").title(), bg.title(), r, v))

    icons = "".join('<figure class="ic">%s<figcaption>%s</figcaption></figure>' % (icon_svg(n), n) for n in ICONS)

    html = TEMPLATE
    rep = {
        "{{F1}}": f64("bricolage-grotesque-800.woff2"), "{{F2}}": f64("inter-var.woff2"),
        "{{COVER_LOGO}}": logo("stacked", C["fog"], C["lupine"]), "{{PAT_COVER}}": pat_cover,
        "{{PAT_DEMO}}": pat_demo, "{{PAT_SMALL}}": pat_small,
        "{{P_COLOR}}": logo("primary", C["spruce"], C["lupine"]), "{{P_REV}}": logo("primary", C["fog"], C["lupine"]),
        "{{P_BLACK}}": logo("primary", "#000", "#000"), "{{P_WHITE}}": logo("primary", "#fff", "#fff"),
        "{{S_COLOR}}": logo("stacked", C["spruce"], C["lupine"]), "{{S_REV}}": logo("stacked", C["fog"], C["lupine"]),
        "{{I_COLOR}}": svg(512, 512, '<rect width="512" height="512" rx="96" fill="%s"/>' % C["spruce"]
                           + icon_mark(256, 256, 400, C["fog"], C["lupine"]), "Icon"),
        "{{I_BLACK}}": logo("icon", "#000", "#000"),
        "{{I_CIRCLE}}": svg(512, 512, '<circle cx="256" cy="256" r="256" fill="%s"/>' % C["spruce"]
                            + icon_mark(256, 256, 360, C["fog"], C["lupine"]), "Icon in a circle crop"),
        "{{MISUSE}}": misuse(), "{{PAIRS}}": rows, "{{ICONS}}": icons,
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    for k, v in C.items():
        html = html.replace("{{%s}}" % k, v)
    write("brand/brand-guide.html", html)
    print("brand-guide.html written")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine brand guide</title>
<style>
@font-face{font-family:GMD;src:url(data:font/woff2;base64,{{F1}}) format("woff2");font-weight:800}
@font-face{font-family:GMB;src:url(data:font/woff2;base64,{{F2}}) format("woff2");font-weight:400 700}
@page{size:11in 8.5in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#d9ddd7}
body{font:15px/1.55 GMB,system-ui,sans-serif;color:{{ink}}}
.page{width:11in;height:8.5in;margin:24px auto;background:{{fog}};position:relative;overflow:hidden;padding:.6in .7in;page-break-after:always;break-after:page;display:flex;flex-direction:column}
@media print{html,body{background:none}.page{margin:0;box-shadow:none}}
.page.dark{background:{{spruce}};color:{{fog}}}
.num{position:absolute;right:.7in;bottom:.35in;font-size:11px;color:{{moss}}}
.dark .num{color:{{blossom}}}
.kicker{font:600 12px/1 GMB;letter-spacing:.1em;text-transform:uppercase;color:{{moss}};margin:0 0 10px}
.dark .kicker{color:{{blossom}}}
h1,h2,h3{font-family:GMD;font-weight:800;letter-spacing:-.012em;margin:0}
h2{font-size:40px;line-height:1.05;margin-bottom:18px}
h3{font-size:19px;margin:0 0 6px}
p{margin:0 0 10px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:28px 40px;flex:1}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:#fff;border-radius:16px;padding:18px 20px}
.dark .card{background:rgba(255,255,255,.06)}
.pat{position:absolute;inset:0;width:100%;height:100%}
.cover .inner{position:relative;margin-top:auto}
.cover .logo svg{width:480px;height:auto;display:block;margin-bottom:36px}
.cover p{font-size:18px;max-width:40ch}
table{border-collapse:collapse;width:100%;font-size:13px}
td,th{padding:6px 8px;border-bottom:1px solid rgba(10,26,20,.12);text-align:left;vertical-align:top}
th{font-weight:700}
.chip{display:inline-block;width:40px;text-align:center;padding:3px 0;border-radius:6px;font-weight:700;border:1px solid rgba(0,0,0,.1)}
.lg{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.lg .tile{border-radius:14px;display:grid;place-items:center;padding:22px;min-height:120px}
.lg .tile svg{width:100%;height:auto;max-height:110px}
.lg .tile.sq svg{width:96px}
.cap{font-size:12px;color:{{moss}};margin-top:6px}
.cs{position:relative;background:#fff;border-radius:14px;padding:40px;display:inline-block}
.cs .box{position:relative;padding:28px;outline:2px dashed {{lupine}}}
.cs svg{width:420px;display:block}
.cs .lbl{position:absolute;font-size:11px;color:{{lupine_deep}};font-weight:700}
.dotx{display:inline-block;width:14px;height:14px;border-radius:50%;background:{{lupine}};vertical-align:-2px}
.mins{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px}
.mins .card svg{display:block;margin:8px 0}
.misgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mis{margin:0}
.mis-art{position:relative;border-radius:12px;padding:18px 22px;height:118px;display:grid;place-items:center}
.mis-art svg{width:100%;height:auto;max-height:84px}
.x{position:absolute;top:8px;right:8px;width:26px;height:26px;border-radius:50%;background:#B3261E}
.x::before,.x::after{content:"";position:absolute;left:12px;top:5px;width:2px;height:16px;background:#fff;transform:rotate(45deg)}
.x::after{transform:rotate(-45deg)}
.mis figcaption{font-size:13px;font-weight:600;margin-top:6px}
.sw{border-radius:14px;padding:14px;min-height:118px;display:flex;flex-direction:column;justify-content:flex-end;font-size:12px}
.sw b{font-size:15px}
.ratio{display:flex;height:40px;border-radius:10px;overflow:hidden;margin:6px 0 4px}
.ratio span{display:block}
.type-row{display:grid;grid-template-columns:130px 1fr 200px;gap:16px;align-items:baseline;border-bottom:1px solid rgba(10,26,20,.12);padding:8px 0}
.type-row .spec{font-size:12px;color:{{moss}}}
.ic{margin:0;text-align:center;font-size:12px}
.ic svg{width:48px;height:48px;background:#fff;border-radius:12px;padding:10px;box-sizing:content-box}
.icons{display:flex;gap:14px;flex-wrap:wrap}
.frame{flex:0 0 110px;width:110px;height:196px;border-radius:18px;background:{{moss}};position:relative;overflow:hidden}
.dd{display:grid;grid-template-columns:1fr 1fr;gap:6px 16px;font-size:13px}
.dd .do{border-left:4px solid {{moss}};padding:4px 10px;background:#fff;border-radius:0 8px 8px 0}
.dd .dont{border-left:4px solid #B3261E;padding:4px 10px;background:#fff;border-radius:0 8px 8px 0}
.dd h4{margin:0 0 2px;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
ol.steps{padding-left:20px;margin:0}
ol.steps li{margin-bottom:7px}
.hl{font-family:GMD;font-size:20px;line-height:1.15;margin:0 0 10px}
.attr{background:#fff;border-radius:14px;padding:18px 22px;font-size:16px}
code{font-size:12px;background:rgba(10,26,20,.07);padding:1px 5px;border-radius:4px}
</style>
</head>
<body>

<section class="page dark cover">
  <svg class="pat" viewBox="0 0 1100 850" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{{PAT_COVER}}</svg>
  <div class="inner">
    <div class="logo">{{COVER_LOGO}}</div>
    <p class="kicker">Brand guide · version 1.0 · September 2026</p>
    <p>How to use the Generation Maine name, logo, colors, type and voice. Written for the project lead and the creators.</p>
    <p style="font-size:14px;margin-top:22px">An initiative of Maine Policy Institute</p>
  </div>
</section>

<section class="page">
  <p class="kicker">01 · Strategy</p>
  <h2>Young Mainers on building a life here</h2>
  <div class="cols">
    <div>
      <h3>Positioning</h3>
      <p>Generation Maine is a set of short videos and a Substack made by 8 to 12 young Maine creators about how economic rules shape their lives. Most youth policy media is national, partisan or produced by adults. Generation Maine is local, made by the creators themselves and open about who funds it.</p>
      <h3 style="margin-top:14px">Brand promise</h3>
      <p>You will hear young Mainers describe their own lives in their own words, and you will always know who is behind the project.</p>
      <h3 style="margin-top:14px">Credibility stance</h3>
      <p><b>Radical transparency.</b> "An initiative of Maine Policy Institute" appears on the site, every end card and every channel bio. It is never hidden or shrunk into fine print.</p>
      <p><b>Creator ownership.</b> Creators' faces and voices lead. Their name and hometown appear on every lower third. The logo signs the work and never covers it.</p>
    </div>
    <div>
      <h3>Personality</h3>
      <table>
        <tr><th>Trait</th><th>This</th><th>Not that</th></tr>
        <tr><td>Local</td><td>Real towns, real rents, real commutes</td><td>"America" or "Gen Z" in general</td></tr>
        <tr><td>Straightforward</td><td>What happened and what it cost</td><td>Hype, slogans, talking points</td></tr>
        <tr><td>Curious</td><td>Asks why a rule works the way it does</td><td>Tells the viewer what to think</td></tr>
        <tr><td>Warm</td><td>A friend explaining their week</td><td>A campaign or a classroom</td></tr>
      </table>
      <h3 style="margin-top:18px">Stay away from</h3>
      <p>Flags, stars, eagles and founding-era Americana. Heavy red and blue pairings. Stock photos. Gradients everywhere. Literal lobsters and lighthouses.</p>
    </div>
  </div>
  <span class="num">2</span>
</section>

<section class="page">
  <p class="kicker">02 · Logo suite</p>
  <h2>One wordmark, one dot</h2>
  <p style="max-width:70ch">The dot on the i in "Maine" is a record light. It is always round, always Lupine pink in the full-color logo and never moves. The icon pairs a bold G with the same dot for avatars and favicons.</p>
  <div class="lg" style="margin-top:12px">
    <div><div class="tile" style="background:#fff">{{P_COLOR}}</div><div class="cap">Primary, full color</div></div>
    <div><div class="tile" style="background:{{spruce}}">{{P_REV}}</div><div class="cap">Primary, reversed on Spruce</div></div>
    <div><div class="tile" style="background:#fff">{{P_BLACK}}</div><div class="cap">One color, black</div></div>
    <div><div class="tile" style="background:#222">{{P_WHITE}}</div><div class="cap">One color, white</div></div>
    <div><div class="tile" style="background:#fff">{{S_COLOR}}</div><div class="cap">Stacked, full color</div></div>
    <div><div class="tile" style="background:{{spruce}}">{{S_REV}}</div><div class="cap">Stacked, reversed</div></div>
    <div><div class="tile sq" style="background:#fff">{{I_COLOR}}</div><div class="cap">Icon</div></div>
    <div><div class="tile sq" style="background:#fff">{{I_CIRCLE}}</div><div class="cap">Icon in a circle crop</div></div>
  </div>
  <p class="cap" style="margin-top:12px">Files: <code>brand/logo/</code> has SVG plus 512 and 1024 px PNGs for every version, and the favicon set.</p>
  <span class="num">3</span>
</section>

<section class="page">
  <p class="kicker">03 · Clear space and minimum size</p>
  <h2>Give it room</h2>
  <div class="cols">
    <div>
      <div class="cs"><div class="box">{{P_COLOR}}</div>
        <span class="lbl" style="left:40px;top:14px">2 dots</span><span class="lbl" style="right:12px;top:52px">2 dots</span></div>
      <p style="margin-top:16px"><b>Clear space rule:</b> keep empty space on every side equal to two diameters of the pink dot <span class="dotx"></span>. No text, edges or other logos inside that space. The same rule applies to the stacked logo and the icon.</p>
    </div>
    <div>
      <h3>Minimum sizes</h3>
      <table>
        <tr><th>Version</th><th>Screen</th><th>Print</th></tr>
        <tr><td>Primary (one line)</td><td>120 px wide</td><td>1.25 in wide</td></tr>
        <tr><td>Stacked</td><td>72 px wide</td><td>0.75 in wide</td></tr>
        <tr><td>Icon</td><td>16 px (favicon)</td><td>0.3 in</td></tr>
      </table>
      <p style="margin-top:12px">Below 120 px wide, switch from the primary logo to the icon. On creator videos, the logo sits in a corner at no more than 12 percent of the frame width.</p>
    </div>
  </div>
  <span class="num">4</span>
</section>

<section class="page">
  <p class="kicker">04 · Misuse</p>
  <h2>Six things to avoid</h2>
  <div class="misgrid">{{MISUSE}}</div>
  <p style="margin-top:14px">When in doubt, use the file from <code>brand/logo/</code> as it is. Do not rebuild the logo in Canva with live text.</p>
  <span class="num">5</span>
</section>

<section class="page">
  <p class="kicker">05 · Color</p>
  <h2>Mostly green, one pink dot</h2>
  <div class="cols">
    <div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px">
        <div class="sw" style="background:{{spruce}};color:{{fog}}"><b>Spruce</b>{{spruce}}</div>
        <div class="sw" style="background:{{fog}};color:{{ink}};border:1px solid #ccd"><b>Fog</b>{{fog}}</div>
        <div class="sw" style="background:{{lupine}};color:{{ink}}"><b>Lupine</b>{{lupine}}</div>
        <div class="sw" style="background:{{ink}};color:{{fog}}"><b>Ink</b>{{ink}}</div>
        <div class="sw" style="background:{{moss}};color:#fff"><b>Moss</b>{{moss}}</div>
        <div class="sw" style="background:{{blossom}};color:{{ink}}"><b>Blossom</b>{{blossom}}</div>
        <div class="sw" style="background:{{lupine_deep}};color:#fff"><b>Lupine Deep</b>{{lupine_deep}}</div>
        <div class="sw" style="background:#fff;color:{{ink}};border:1px solid #ccd"><b>White</b>#FFFFFF</div>
      </div>
      <h3 style="margin-top:18px">Usage ratio</h3>
      <div class="ratio"><span style="flex:50;background:{{spruce}}"></span><span style="flex:30;background:#fff"></span><span style="flex:10;background:{{ink}}"></span><span style="flex:7;background:{{moss}}"></span><span style="flex:3;background:{{lupine}}"></span></div>
      <p class="cap">Spruce 50 · Fog and White 30 · Ink 10 · Moss and Blossom 7 · Lupine 3. Lupine is a spark, not a fill.</p>
    </div>
    <div>
      <h3>Text pairs (WCAG 2.1, calculated)</h3>
      <table>{{PAIRS}}</table>
    </div>
  </div>
  <span class="num">6</span>
</section>

<section class="page">
  <p class="kicker">06 · Type</p>
  <h2>Two free fonts</h2>
  <p>Bricolage Grotesque ExtraBold for headlines. Inter for everything else. Both are under the SIL Open Font License, so they are free to use, embed and share. Files are in <code>brand/fonts/</code>.</p>
  <div style="margin-top:8px">
    <div class="type-row"><span class="spec">H1 · web hero</span><span style="font:800 56px/1 GMD;letter-spacing:-.012em">Building a life here</span><span class="spec">Bricolage 800 · 42 to 80 px · line 1.0</span></div>
    <div class="type-row"><span class="spec">H2 · section</span><span style="font:800 36px/1.05 GMD">Meet the creators</span><span class="spec">Bricolage 800 · 32 to 48 px · line 1.05</span></div>
    <div class="type-row"><span class="spec">H3 · card</span><span style="font:800 24px/1.15 GMD">Read the Substack</span><span class="spec">Bricolage 800 · 21 to 26 px</span></div>
    <div class="type-row"><span class="spec">Lead</span><span style="font:400 20px/1.5 GMB">Short videos by young Maine creators.</span><span class="spec">Inter 400 · 18 to 22 px · line 1.5</span></div>
    <div class="type-row"><span class="spec">Body</span><span style="font:400 17px/1.6 GMB">Each one makes short videos about their own life in Maine.</span><span class="spec">Inter 400 · 17 px · line 1.6</span></div>
    <div class="type-row"><span class="spec">Eyebrow</span><span style="font:600 13px/1 GMB;letter-spacing:.08em;text-transform:uppercase;color:{{moss}}">What is Generation Maine</span><span class="spec">Inter 600 · 13 to 15 px · caps · +0.08em</span></div>
    <div class="type-row"><span class="spec">Caption</span><span style="font:400 13px/1.4 GMB">© 2026 Generation Maine</span><span class="spec">Inter 400 · 13 px</span></div>
  </div>
  <p class="cap" style="margin-top:10px">On 1080 px social graphics, headlines run 64 to 96 px and captions no smaller than 32 px.</p>
  <span class="num">7</span>
</section>

<section class="page">
  <p class="kicker">07 · Graphic elements</p>
  <h2>Contour lines, frames and the dot</h2>
  <div class="cols3">
    <div class="card" style="background:{{spruce}};color:{{fog}};position:relative;overflow:hidden;min-height:200px">
      <svg class="pat" viewBox="0 0 400 220" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{{PAT_DEMO}}</svg>
      <div style="position:relative"><h3>Contour lines</h3><p style="font-size:13px">Moss lines on Spruce, 2 to 4 px thick. Crop freely. Keep them off faces and away from text. Ready-made: <code style="background:rgba(255,255,255,.12);color:{{fog}}">pattern-contours.png</code>.</p></div>
    </div>
    <div class="card">
      <h3>Frames</h3>
      <div style="display:flex;gap:12px;align-items:flex-end">
        <div class="frame"><svg class="pat" viewBox="0 0 110 196" aria-hidden="true">{{PAT_SMALL}}</svg></div>
        <p style="font-size:13px">Photos and video stills sit in rounded rectangles with a 24 px corner radius (18 px on small items). Vertical 9:16 frames nod to phone video.</p>
      </div>
    </div>
    <div class="card">
      <h3>The dot</h3>
      <p style="font-size:13px"><span class="dotx"></span> One Lupine dot per composition. Use it as a period at the end of a headline, a record light, or a bullet. Never more than one large dot on a page or screen.</p>
      <h3 style="margin-top:12px">Icons</h3>
      <div class="icons">{{ICONS}}</div>
      <p class="cap">24 px grid, 2 px stroke, round caps and joins, no fills.</p>
    </div>
  </div>
  <span class="num">8</span>
</section>

<section class="page">
  <p class="kicker">08 · Photography</p>
  <h2>Real creators in real Maine places</h2>
  <div class="cols">
    <div>
      <h3>Do</h3>
      <p>Photograph the creators where their stories happen: a kitchen table, a job site, a Main Street storefront, a bus stop, a dorm room, a town office.</p>
      <p>Use natural light. Morning and late-afternoon light suit the palette.</p>
      <p>Let people look like themselves. Work clothes, winter coats and messy rooms are fine.</p>
      <p>Shoot vertical first. Leave space above the head for a title on thumbnails.</p>
      <p>Get written permission from every person shown, and a parent's permission for anyone under 18.</p>
    </div>
    <div>
      <h3>Do not</h3>
      <p>Use stock photos of smiling young people in offices.</p>
      <p>Pose people in front of lighthouses, lobster traps or flags to signal "Maine."</p>
      <p>Add heavy filters, color grades or gradients over faces.</p>
      <p>Show a person in a way that suggests they hold a policy view they have not stated.</p>
      <div class="card" style="margin-top:12px"><h3>Portrait for the website</h3><p style="font-size:13px">4:5 ratio, at least 1000 × 1250 px, face in the upper half, plain or real background. Upload it as the creator's Portrait (featured image).</p></div>
    </div>
  </div>
  <span class="num">9</span>
</section>

<section class="page">
  <p class="kicker">09 · Voice and tone</p>
  <h2>Stories, not positions</h2>
  <div class="cols">
    <div class="dd">
      <div class="do"><h4>Do</h4>"My rent went up $200 when the lease renewed."</div>
      <div class="dont"><h4>Don't</h4>"The housing crisis is crushing our generation!"</div>
      <div class="do"><h4>Do</h4>Name the town: "in Waterville"</div>
      <div class="dont"><h4>Don't</h4>Go national: "across America"</div>
      <div class="do"><h4>Do</h4>"Here is what the permit process looked like for me."</div>
      <div class="dont"><h4>Don't</h4>"Politicians don't want you to know this."</div>
      <div class="do"><h4>Do</h4>Ask: "Why does this license cost so much?"</div>
      <div class="dont"><h4>Don't</h4>Declare: "This law is a disaster."</div>
      <div class="do"><h4>Do</h4>Plain words: "The town said no."</div>
      <div class="dont"><h4>Don't</h4>Jargon: "regulatory burden on small enterprise"</div>
    </div>
    <div>
      <h3>Example video headlines</h3>
      <p class="cap" style="margin-bottom:10px">Samples of the style only. They are not real videos.</p>
      <p class="hl">What rent costs in Lewiston</p>
      <p class="hl">I tried to open a food truck</p>
      <p class="hl">Why my friends moved to Boston</p>
      <p class="hl">My first paycheck, line by line</p>
      <p class="hl">How long a building permit took</p>
      <p class="hl">Should I stay after college?</p>
      <p class="cap">Keep titles to 3 to 7 words. No em dashes. No all-caps sentences.</p>
    </div>
  </div>
  <span class="num">10</span>
</section>

<section class="page">
  <p class="kicker">10 · Maine Policy Institute attribution</p>
  <h2>Always visible, always the same words</h2>
  <div class="attr">An initiative of Maine Policy Institute</div>
  <div class="cols" style="margin-top:18px">
    <div>
      <h3>Exact wording</h3>
      <p>"An initiative of Maine Policy Institute." Do not shorten it to "MPI" and do not replace it with "sponsored by" or "presented by."</p>
      <h3 style="margin-top:12px">Where it appears</h3>
      <p>Website: in the hero above the headline, in its own "About Maine Policy Institute" section and in the footer.</p>
      <p>Social: every channel bio, every 9:16 end card, the YouTube banner and the Substack about page.</p>
    </div>
    <div>
      <h3>Minimum size</h3>
      <p>Website: 13 px or larger, in Inter, at full contrast (Fog on Spruce or Ink on light backgrounds).</p>
      <p>1080 × 1920 end card: 32 px or larger. 1200 × 630 share card: 28 px or larger.</p>
      <p>Never lower its contrast below 4.5:1 and never place it on top of busy footage.</p>
    </div>
  </div>
  <span class="num">11</span>
</section>

<section class="page">
  <p class="kicker">11 · Canva and CapCut</p>
  <h2>Using the social kit</h2>
  <div class="cols">
    <div>
      <h3>Set up Canva once</h3>
      <ol class="steps">
        <li>Open Brand Kit and add the colors: {{spruce}}, {{fog}}, {{lupine}}, {{ink}}, {{moss}}, {{blossom}}.</li>
        <li>Upload <code>BricolageGrotesque-ExtraBold.ttf</code> and the two Inter files from <code>brand/fonts/</code> (font upload needs Canva Pro). Without Pro, pick Inter from Canva's font list and a bold sans-serif for headlines.</li>
        <li>Upload the logo PNGs from <code>brand/logo/</code> to the Brand Kit logos.</li>
        <li>Upload the <code>-blank.png</code> backgrounds from <code>brand/social/</code>.</li>
      </ol>
    </div>
    <div>
      <h3>Make a post</h3>
      <ol class="steps">
        <li>Create a design at the right size (for example 1080 × 1920 for an end card).</li>
        <li>Drag in the matching blank background and lock it.</li>
        <li>Add text boxes where the placeholders were. Use the finished PNG as your guide.</li>
        <li>Check the attribution line is there and readable.</li>
      </ol>
      <h3 style="margin-top:12px">CapCut</h3>
      <ol class="steps">
        <li>Add <code>lower-third-1920x1080-blank.png</code> as an overlay and type the name and hometown on top.</li>
        <li>End every video with the end card for 3 to 5 seconds.</li>
      </ol>
    </div>
  </div>
  <span class="num">12</span>
</section>

</body>
</html>
"""

if __name__ == "__main__":
    build()
