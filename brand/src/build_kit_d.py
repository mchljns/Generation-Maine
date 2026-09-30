"""Concept D, "Bark & Sky": a second, fully separate direction for the client to compare with Signature.

Nothing is shared with Signature except the name, the audience and the Maine Policy Institute line.
  Palette : Sky #CFE3F0, Bark #2B211C, Paper #FFFFFF, Mist #EEF4F8, Clay #6B5A4E
  Type    : Hedvig Letters Serif (OFL) for the wordmark, titles and names, Hedvig Letters Sans (OFL) for text.
            One weight each. The serif is instanced at optical size 24 for display and 12 for small sizes.
  Case    : the wordmark, titles, names, nav and buttons are all lowercase. Reading text and the
            Maine Policy Institute line keep normal case, so the institute's name always reads clearly.
  Layout  : centered and airy. No end dot, no heavy weights.

Called from build_kit.py, which passes in its shared mockup helpers.
"""
import base64
import os

from gmlib import ROOT, Face, write
from build_v4 import svg, f

D = {"sky": "#CFE3F0", "bark": "#2B211C", "paper": "#FFFFFF", "mist": "#EEF4F8", "clay": "#6B5A4E"}
SERIF = Face("d/HedvigLettersSerif-24.ttf")
SERIF_SB = Face("d/HedvigLettersSerif-12.ttf")  # sturdier small-size cut, used for the video bug
OUT = "brand/kit/assets/logo-d"


def wordmark(fg, size=100, face=None):
    d, w = (face or SERIF).path("generation maine", size, 0, size * 0.78, -8)
    return '<path fill="%s" d="%s"/>' % (fg, d), w, size * 1.0


def monogram(bg, fg, s=200):
    """Lowercase g and m, set tight, centered in a circle-safe square."""
    size = s * 0.5
    d, w = SERIF.path("gm", size, 0, 0, -20)
    x = (s - w) / 2
    base = s / 2 + size * 0.2
    d, w = SERIF.path("gm", size, x, base, -20)
    bgr = '<rect width="%s" height="%s" fill="%s"/>' % (s, s, bg) if bg else ""
    return bgr + '<path fill="%s" d="%s"/>' % (fg, d)


def build_logos():
    m = {}
    for suf, fg in (("", D["bark"]), ("-reversed", D["paper"])):
        b, w, h = wordmark(fg)
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        b, w, h = wordmark(fg, face=SERIF_SB)
        m["wordmark-small" + suf] = svg(w, h, b, "Generation Maine")
    m["avatar"] = svg(200, 200, monogram(D["bark"], D["sky"]), "Generation Maine")
    m["avatar-sky"] = svg(200, 200, monogram(D["sky"], D["bark"]), "Generation Maine")
    for k, v in m.items():
        write("%s/%s.svg" % (OUT, k), v)
    return m


def font64(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


CSS = r"""
@font-face{font-family:Fraun;src:url(data:font/ttf;base64,{{FR}}) format('truetype');font-weight:100 1000}
@font-face{font-family:FraunS;src:url(data:font/ttf;base64,{{FRSB}}) format('truetype');font-weight:100 1000}
@font-face{font-family:ISans;src:url(data:font/ttf;base64,{{IS4}}) format('truetype');font-weight:100 1000}
.dz{--sky:#CFE3F0;--bark:#2B211C;--paper:#FFFFFF;--mist:#EEF4F8;--clay:#6B5A4E;font-family:ISans,Inter,sans-serif;font-synthesis:none}
.dz .dt,.dz .dname,.dz .dmeta,.dz .dwn nav,.dz .dbtn,.dz .dhl,.dz .dwh h1,.dz .dsb h3{text-transform:lowercase}
.dz .dmeta b,.dz .dhl b{font-family:FraunS}
.dz .dbug{position:absolute;top:42px;left:18px}
.dz .dbug svg{width:112px;height:auto;display:block;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
.dz .dname{margin:0;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.45)}
.dz .dname b{display:block;font:400 26px/1.1 Fraun;letter-spacing:-.01em}
.dz .dname span{display:block;font:400 14px/1.5 ISans}
.dz .dname b{font-family:Fraun}
.dz .dl3{position:absolute;left:18px;bottom:196px}
.dz .dt{margin:0;font:400 30px/1.08 Fraun;letter-spacing:-.015em;color:var(--bark);text-align:center}
.dz .dmeta{margin:0;font:400 11px/1.4 ISans;color:var(--clay);text-align:center}
.dz .dmeta b{font-weight:400;color:var(--bark)}
.dz .dend{position:absolute;inset:0;background:var(--sky);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:52px 24px 30px;text-align:center}
.dz .dend .wm{width:190px;height:auto}
.dz .dend .dt{font-size:46px}
.dz .dhl{list-style:none;margin:22px 0 0;padding:0;font:400 14px/1 ISans;color:var(--bark)}
.dz .dhl li{padding:8px 0}.dz .dhl b{font-weight:400;margin-right:8px}
.dz .ddisc{margin:0;font:400 13px/1.35 ISans;color:var(--bark)}
.dz .grid9{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}
.dz .dcov{position:relative;aspect-ratio:3/4;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px;text-align:center}
.dz .dcov.sky{background:var(--sky)}.dz .dcov.paper{background:var(--paper);box-shadow:inset 0 0 0 1px #E6E9EC}.dz .dcov.mist{background:var(--mist)}.dz .dcov.bark{background:var(--bark)}
.dz .dcov .dt{font-size:22px;line-height:1.02;margin-top:-10px}
.dz .dcov.bark .dt{color:var(--sky)}.dz .dcov.bark .dmeta,.dz .dcov.bark .dmeta b{color:var(--mist)}
.dz .dcov .dmeta{position:absolute;left:4px;right:4px;bottom:7px;font-size:7.5px;line-height:1.3}
.dz .dcov .dmeta b{display:block}
.dz .dsub{position:absolute;inset:0;background:var(--paper)}
.dz .dsh{text-align:center;padding:30px 32px 16px}
.dz .dsh .wm{width:240px;height:auto}
.dz .dsh p{margin:8px 0 0;font:400 12px ISans;color:var(--clay)}
.dz .dsb{padding:26px 44px 0;font:400 14px/1.65 ISans;color:#2F2A27;border-top:1px solid #E6E9EC}
.dz .dsb h3{font:400 32px/1.08 Fraun;letter-spacing:-.015em;margin:4px 0 10px;text-align:center;color:var(--bark)}
.dz .dsb .dmeta{margin-bottom:22px;font-size:13px}
.dz .dsf{position:absolute;left:0;right:0;bottom:14px;margin:0;text-align:center;font:400 11px ISans;color:var(--clay)}
.dz .dweb{position:absolute;inset:0;background:var(--sky);color:var(--bark);display:flex;flex-direction:column}
.dz .dwn{display:flex;justify-content:space-between;align-items:center;padding:26px 56px}
.dz .dwn .wm{height:30px;width:auto}
.dz .dwn nav{display:flex;gap:28px;font:400 15px ISans}
.dz .dwh{text-align:center;padding:0 120px 40px;flex:1;display:flex;flex-direction:column;justify-content:center}
.dz .dwh .ddisc{font-weight:400;font-size:14px;color:var(--clay)}
.dz .dwh h1{font:400 96px/1.0 Fraun;letter-spacing:-.025em;margin:22px auto 22px;max-width:14ch}
.dz .dwh .lede{font:400 19px/1.55 ISans;max-width:40ch;margin:0 auto 30px}
.dz .dbtn{display:flex;gap:12px;justify-content:center;margin:0}
.dz .dbtn span{padding:14px 24px;border-radius:999px;font:400 15px ISans}
.dz .dbtn .p{background:var(--bark);color:var(--paper)}.dz .dbtn .s{box-shadow:inset 0 0 0 1.5px var(--bark)}
.dz .dfeed .dl3{bottom:22px}
.dz .dav{width:110px;height:110px;border-radius:50%;overflow:hidden;flex:none}
.dz .dav svg{width:100%;height:100%;display:block}
"""

ORDER = ["sky", "paper", "sky", "bark", "sky", "paper", "sky", "bark", "mist"]


def mockups(m, h):
    """h: helpers from build_kit (inl, artboard, ui_overlay, MPI, TOWNS, TOPICS)."""
    inl, artboard, ui, MPI = h["inl"], h["artboard"], h["ui_overlay"], h["MPI"]
    wm_rev = inl(m["wordmark-reversed"], "wm")
    wm = inl(m["wordmark"], "wm")
    bug = '<div class="dbug">%s</div>' % inl(m["wordmark-small-reversed"], "wm")
    name = lambda town: '<p class="dname"><b>[Creator name]</b><span>%s, Maine</span></p>' % town
    first = '<div class="foot"></div>%s%s' % (bug, ui())
    lower = '<div class="foot"></div>%s<div class="dl3">%s</div>%s' % (bug, name("Skowhegan"), ui())
    end = ('<div class="dend">%s<div><p class="dt">Follow along</p><ul class="dhl"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
           '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul></div><p class="ddisc">%s</p></div>') % (wm, MPI)
    covers = "".join('<div class="dcov %s"><p class="dt">%s</p><p class="dmeta"><b>[Creator name]</b>%s, Maine</p></div>'
                     % (ORDER[i], h["TOPICS"][i], h["TOWNS"][i]) for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9">%s</div></div>') % (inl(m["avatar"], "pa"), MPI, covers)
    sub = ('<div class="dsub"><div class="dsh">%s<p>%s</p></div><div class="dsb"><h3>[Post title in plain words]</h3>'
           '<p class="dmeta"><b>[Creator name]</b> · Belfast, Maine</p><p>[First paragraph in the creator\'s own words.]</p><p>[Body continues.]</p><p>[Body continues.]</p></div>'
           '<p class="dsf">%s</p></div>') % (wm, MPI, MPI)
    hero = ('<div class="dweb"><div class="dwn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<div class="dwh"><p class="ddisc">%s</p><h1>Young Mainers on building a life here</h1>'
            '<p class="lede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="dbtn"><span class="p">Meet the creators</span><span class="s">Follow along</span></p></div></div>') % (wm, MPI)
    post = '<div class="pimg"><div class="foot"></div>%s<div class="dl3">%s</div></div>' % (bug, name("Machias"))
    collab = ('<div class="feed dfeed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    others = [("#7A4E9E", "RJ"), ("#2F6FA3", "MB")]
    avs = ('<div class="avs"><p class="k">Profile size, 110 px</p><div class="row3"><span class="oav" style="background:%s">%s</span>'
           '<span class="dav">%s</span><span class="oav" style="background:%s">%s</span></div>'
           '<p class="k">Other versions</p><div class="row3"><span class="dav">%s</span><span class="dav" style="width:40px;height:40px">%s</span><span class="dav" style="width:32px;height:32px">%s</span></div></div>'
           ) % (others[0][0], others[0][1], inl(m["avatar"], ""), others[1][0], others[1][1], inl(m["avatar-sky"], ""), inl(m["avatar"], ""), inl(m["avatar"], ""))
    a = artboard
    out = [a("d-first", "ph9 dz", first, "D1 · Video, first seconds. Only the wordmark.", 360, 640),
           a("d-lower", "ph9 dz", lower, "D2 · Name and town", 360, 640),
           a("d-end", "ph9 dz", end, "D3 · End card", 360, 640),
           a("d-grid", "ph9 light dz", grid, "D4 · Profile grid of nine covers", 360, 640),
           a("d-substack", "light dz", sub, "D6 · Substack header and email", 480, 640),
           a("d-collab", "ph9 light dz", collab, "D8 · Collab post on a creator's own account", 360, 640),
           a("d-avatar", "light dz", avs, "D5 · Avatar at 110, 40 and 32 px", 480, 640)]
    return out, a("d-web", "dz", hero, "D7 · Website hero, no photo", 1200, 680)


def css():
    c = CSS
    for k, v in {"{{FR}}": "brand/fonts/d/HedvigLettersSerif-24.ttf", "{{FRSB}}": "brand/fonts/d/HedvigLettersSerif-12.ttf",
                 "{{IS4}}": "brand/fonts/d/HedvigLettersSans-Regular.ttf"}.items():
        c = c.replace(k, font64(v))
    return c


SECTION = r"""<section><div class="w">
  <p class="k">Second direction, for the client to compare</p>
  <h2>Concept D: Bark &amp; Sky</h2>
  <p>A fully separate direction. It shares only the name, the audience and the Maine Policy Institute line with Signature. Where Signature is dark, heavy and low left, this one is light, soft and centered.</p>
  <p>The test sentence: lowercase serif titles, centered on pale blue and white, with brown for type. It says nothing about youth, Maine or economics.</p>
  <ol class="rules">
    <li>Paper and Sky make up most of every surface. Bark is for type and one cover in four.</li>
    <li>Hedvig Letters Serif for the wordmark, titles and names. Hedvig Letters Sans for text. One weight each, so hierarchy comes from size and color alone.</li>
    <li>The wordmark, titles, names, nav and buttons are all lowercase. Reading text and the Maine Policy Institute line keep normal case, so the institute's name always reads clearly.</li>
    <li>The avatar is a lowercase gm in the serif.</li>
    <li>The creator's name is set in the serif, the same as a title. Their town sits under it in the sans.</li>
    <li>No bold anywhere, nothing boxed, and buttons fully rounded.</li>
  </ol>
  <div class="cards">{{D}}</div>
  <div class="cards">{{D_WEB}}</div>
  <p class="k" style="margin-top:34px">Against the test, first pass</p>
  <table class="checks"><tr><th>Criterion</th><th>Signature, round two</th><th>Concept D: Bark &amp; Sky</th></tr>
  <tr><td>1 Signs, does not cover</td><td>Pass</td><td>Pass. A small lowercase wordmark, top left.</td></tr>
  <tr><td>2 Survives the crop</td><td>Pass</td><td>Pass at 110, 40 and 32 px. Not yet tested as a 16 px favicon, where two letters may merge.</td></tr>
  <tr><td>3 Carries a person</td><td>Pass</td><td>Pass. The name is set in the brand serif, the same as a title.</td></tr>
  <tr><td>4 Neutral</td><td>Pass</td><td>Pass. The blue stays pale and sits with brown, never with red.</td></tr>
  <tr><td>5 Both audiences</td><td>Pass</td><td>Pass on Substack and the site, where it reads as literary and calm. Partial on TikTok, where soft covers may not stop the scroll.</td></tr>
  <tr><td>6 Stands without photos</td><td>Pass</td><td>Pass. Space and type carry it.</td></tr>
  <tr><td>7 Ownable</td><td>Partial</td><td>Partial, and closer. Brown with pale blue is unusual in civic and news media. Hedvig is rarely seen, and all-lowercase serif titles are a distinct voice. Lowercase alone is a common move.</td></tr>
  <tr><td>8 Easy to make</td><td>Pass</td><td>Pass. One centered text box on one of four fields.</td></tr>
  </table>
  <p class="note" style="margin-top:14px">Where they split: Signature is louder and better on TikTok. Bark &amp; Sky is warmer and better for the older Substack reader. Both keep the Maine Policy Institute line on every end card, bio and footer.</p>
</div></section>
"""
