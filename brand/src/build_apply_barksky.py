"""Apply the Maine logo in Bark & Sky to the same real surfaces as Signature's brand/identity/apply: a video's first seconds, the lower
third, the end card, the profile grid, the avatar among other accounts, the Substack header, the collab post and the website hero.

Reuses the kit's mockup chrome and the Bark & Sky kit rules (lowercase Hedvig, one weight, Sky, Paper, Mist and Bark fields).
Logo files come from brand/identity/logo-maine/bark-sky/.

  python3 brand/src/build_apply_barksky.py && node brand/src/render_apply.mjs apply-bark-sky && python3 brand/src/sheet_apply.py apply-bark-sky
"""
import os

from gmlib import ROOT, write
from build_v6 import C
import build_kit as K
import build_kit_d as D
from build_apply import mural

OUT = "brand/identity/apply-bark-sky"
LOGO = os.path.join(ROOT, "brand", "identity", "logo-maine", "bark-sky")
BK, SK, PA, MIST, CL = D.D["bark"], D.D["sky"], D.D["paper"], D.D["mist"], D.D["clay"]


def logo(name, cls=""):
    with open(os.path.join(LOGO, name + ".svg")) as fh:
        return K.inl(fh.read(), cls)


def name(town):
    return '<p class="dname"><b>[Creator name]</b><span>%s, Maine</span></p>' % town


def mockups():
    bug = '<div class="bbug">%s</div>' % logo("bug")
    a = K.artboard
    out = []
    # 1 video, first seconds: the solid state and the name in Paper, nothing else
    out.append(a("l-first", "ph9 dz", '<div class="foot"></div>%s%s' % (bug, K.ui_overlay()), "1 · Video, first seconds. The solid cut and the name", 360, 640))
    # 2 lower third: the name in the serif, the town under it
    out.append(a("l-lower", "ph9 dz", '<div class="foot"></div>%s<div class="dl3">%s</div>%s' % (bug, name("Skowhegan"), K.ui_overlay()), "2 · Lower third, name in the serif, town in the sans", 360, 640))
    # 3 end card on Sky: the horizontal lockup, the state in Bark lines, the handles, the disclosure
    end = ('<div class="bend">%s<div class="bmur">%s</div><div><p class="dt">follow along</p>'
           '<ul class="dhl"><li><b>instagram</b>[@handle]</li><li><b>tiktok</b>[@handle]</li><li><b>youtube</b>[@handle]</li><li><b>substack</b>[name].substack.com</li></ul></div>'
           '<p class="ddisc">%s</p></div>') % (logo("lockup-horizontal", "lk"), mural(300, BK, BK, n=48), K.MPI)
    out.append(a("l-end", "ph9 dz", end, "3 · End card. The state, then the handles", 360, 640))
    # 4 profile grid: the full-cut avatar, nine covers on the concept's four fields
    covers = "".join('<div class="dcov %s"><p class="dt">%s</p><p class="dmeta"><b>[Creator name]</b>%s, Maine</p></div>' % (D.ORDER[i], K.TOPICS[i], K.TOWNS[i]) for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9">%s</div></div>') % (logo("avatar-full", "pa"), K.MPI, covers)
    out.append(a("l-grid", "ph9 light dz", grid, "4 · Profile grid", 360, 640))
    # 5 avatar among other accounts, by size: full at 110, mid at 40, solid at 16
    others = [("#7A4E9E", "RJ"), ("#2F6FA3", "MB"), ("#B4532A", "TK")]
    big = '<span class="oav" style="background:%s">%s</span><span class="gav">%s</span><span class="oav" style="background:%s">%s</span>' % (others[0][0], others[0][1], logo("avatar-full"), others[1][0], others[1][1])
    rows = '<li><span class="gav s">%s</span><b>Generation Maine</b><span class="fb">Follow</span></li>' % logo("avatar-solid")
    rows += "".join('<li><span class="oav s" style="background:%s">%s</span><b>Account name</b><span class="fb">Follow</span></li>' % (c, t) for c, t in others)
    tab = '<div class="tabbar"><span class="tab on"><i>%s</i>Generation Maine</span><span class="tab"><i class="g"></i>Other site</span></div>' % logo("favicon")
    avs = '<div class="avs"><p class="k">Profile size, 110 px: full cut</p><div class="row3">%s</div><p class="k">List size, 40 px: solid</p><ul class="sugg">%s</ul><p class="k">Browser tab, 16 px: solid</p>%s</div>' % (big, rows, tab)
    out.append(a("l-avatar", "light dz", avs, "5 · Avatar among other accounts, one cut per size", 480, 640))
    # 6 Substack header and email: the lockup centered on Paper, the disclosure under it
    sub = ('<div class="dsub"><div class="dsh">%s<p>%s</p></div><div class="dsb"><h3>[Post title in plain words]</h3>'
           '<p class="dmeta"><b>[Creator name]</b> · Belfast, Maine</p><p>[First paragraph in the creator\'s own words.]</p><p>[Body continues.]</p><p>[Body continues.]</p></div>'
           '<p class="dsf">%s</p></div>') % (logo("lockup-horizontal", "lk sub"), K.MPI, K.MPI)
    out.append(a("l-substack", "light dz", sub, "6 · Substack header and email", 480, 640))
    # 8 collab post on a creator's own account
    post = '<div class="pimg"><div class="foot"></div>%s<div class="dl3 p">%s</div></div>' % (bug, name("Machias"))
    collab = ('<div class="feed dfeed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    out.append(a("l-collab", "ph9 light dz", collab, "8 · Collab post on a creator's own account", 360, 640))
    # 7 website hero, as built: the state above the headline, centered on Sky, the lockup in the nav
    hero = ('<div class="dweb"><div class="dwn">%s<nav><span>about</span><span>creators</span><span>in their words</span><span>follow</span></nav></div>'
            '<div class="dwh bwh">%s<h1>Young Mainers on building a life here</h1>'
            '<p class="lede">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay.</p>'
            '<p class="dbtn"><span class="p">watch the stories</span><span class="s">get the newsletter</span></p></div></div>') % (logo("lockup-horizontal-solid", "lk nav"), logo("mark-full", "bm"))
    web = a("l-web", "dz", hero, "7 · Website hero, as built", 1200, 680)
    return "".join(out), web


CSS_ADD = r"""
.bbug{position:absolute;top:44px;left:var(--M)}
.bbug svg{height:22px;width:auto;display:block;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
.dz .dl3{bottom:196px}
.bend{position:absolute;inset:0;background:var(--sky);padding:40px var(--M) 26px;display:flex;flex-direction:column;align-items:center;text-align:center}
.bend .lk{height:28px;width:auto;display:block}
.bmur{flex:1;display:flex;align-items:center;justify-content:center;padding:14px 0 6px}
.bmur .mural{height:236px;width:auto;display:block}
.bend .dt{font-size:44px;margin-bottom:4px}
.bend .dhl{margin-top:12px}
.bend .ddisc{margin-top:18px}
.dsh .lk.sub{height:40px;width:auto;display:inline-block}
.dz .dwn .lk.nav{height:24px;width:auto}
.dz .dwn nav{font-size:14px}
.bwh .bm{height:120px;width:auto;display:block;margin:0 auto 20px}
.dz .bwh h1{font-size:74px;margin:0 auto 18px;max-width:13ch}
.dz .bwh{padding:0 120px 28px}
.dz .bwh .lede{font-size:17px;margin-bottom:24px}
.dz .dbtn{text-transform:lowercase}
"""


def build():
    K.build_logos()   # the round-two master files, still needed by the shared mockup helpers
    boards, web = mockups()
    css = K.CSS + D.css() + CSS_ADD
    for k, v in {"{{F800}}": K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
                 "{{F700}}": K.font64("brand/v6/fonts-web/bricolage-grotesque-700.woff2"),
                 "{{FCOND}}": K.font64("brand/v4/fonts-web/bricolage-condensed-800.woff2"),
                 "{{FINTER}}": K.font64("brand/fonts/inter-var.woff2")}.items():
        css = css.replace(k, v)
    for k, v in C.items():
        css = css.replace("{{%s}}" % k, v)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Generation Maine, the logo applied, Bark &amp; Sky</title><style>%s</style></head><body>'
            '<header class="top" style="background:#2B211C"><div class="w"><p class="k" style="color:#CFE3F0">Generation Maine · The logo applied · Bark &amp; Sky</p><h1 style="color:#CFE3F0">Maine in lines, in the second concept</h1>'
            '<p>The same size system in use: the full cut on the end card, the hero and the profile picture, the mid cut in lists, the solid cut in the video bug and the browser tab. One color per surface, the lowercase name, no dot.</p></div></header>'
            '<section><div class="w"><div class="cards">%s</div><div class="cards">%s</div></div></section></body></html>') % (css, boards, web)
    write(OUT + "/apply.html", page)


if __name__ == "__main__":
    build()
    print("apply-bark-sky/apply.html written")
