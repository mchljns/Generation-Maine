"""Apply the Maine logo to the real surfaces from brand/00-platform.md, so it can be judged where
it will live: a video's first seconds, the lower third, the end card, the profile grid, the
avatar among other accounts, the Substack header, the website hero and a collab post.

Reuses the kit's mockup chrome and the round-two Signature rules. Logo files come from
brand/identity/logo-maine/signature/.

  python3 brand/src/build_apply.py && node brand/src/render_apply.mjs && python3 brand/src/sheet_apply.py
"""
import os

from gmlib import ROOT, write
from build_v6 import C
import build_kit as K
import maine2

OUT = "brand/identity/apply"
LOGO = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")
SP, BI, MG, MOSS = C["spruce"], C["birch"], C["marigold"], C["moss"]


def logo(name, cls=""):
    with open(os.path.join(LOGO, name + ".svg")) as fh:
        return K.inl(fh.read(), cls)


def mural(h, fg, mark, n=60, w_lo=None, w_hi=None, keep=1.6):
    """Maine in fine lines fitted to a height, as an inline SVG. Width follows the outline."""
    w_box = h * maine2.ASPECT
    ring = maine2.fit(0, 0, w_box, h)
    minx, miny, maxx, maxy = maine2.bbox(ring)
    w_lo = w_lo or h * 0.004
    w_hi = w_hi or h * 0.011
    rows = []
    for i in range(n):
        t = i / (n - 1)
        y0 = miny + (maxy - miny) * (0.01 + 0.98 * t)
        w = w_lo + (w_hi - w_lo) * t
        xs = maine2.crossings(ring, y0)
        runs = [(a + w / 2, b - w / 2) for a, b in zip(xs[0::2], xs[1::2]) if b - a > w * keep]
        rows.append((y0, w, runs))
    widest = max(range(n), key=lambda i: sum(b - a for a, b in rows[i][2]))
    body = ""
    for i, (y0, w, runs) in enumerate(rows):
        col = mark if i == widest else fg
        for a, b in runs:
            body += '<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.2f" stroke-linecap="round" fill="none"/>' % (a, y0, b, y0, col, w)
    return '<svg class="mural" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f">%s</svg>' % (w_box, h, body)


def mockups():
    bug = '<div class="lbug">%s</div>' % logo("bug")
    lock_rev = logo("lockup-horizontal-reversed", "lk")
    two_rev = logo("lockup-two-line-reversed", "lk two")
    a = K.artboard
    out = []
    # 1 video, first seconds: the solid state and the name, Birch, nothing else
    out.append(a("l-first", "ph9", '<div class="foot"></div>%s%s' % (bug, K.ui_overlay()), "1 · Video, first seconds. The solid cut and the name", 360, 640))
    # 2 lower third: name and town, plain, on the safe line
    out.append(a("l-lower", "ph9", '<div class="foot"></div>%s<div class="sl3">%s</div>%s' % (bug, K.credit(town="Skowhegan", cls="lg"), K.ui_overlay()), "2 · Lower third, name and town plain", 360, 640))
    # 3 end card: the two-line lockup at top, the mural in one color, the headline keeps its Marigold dot
    end = ('<div class="lend">%s<div class="lmur">%s</div><div class="lbot">%s'
           '<ul class="hl s"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li><li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul>'
           '<p class="disc">%s</p></div></div>') % (two_rev, mural(300, BI, BI, n=48), K.ttl("Follow along", "xl"), K.MPI)
    out.append(a("l-end", "ph9", end, "3 · End card. The mural, then the handles", 360, 640))
    # 4 profile grid: the full-cut avatar, nine covers on the round-two rules
    covers = "".join('<div class="cov s %s">%s%s</div>' % (K.ORDER[i], K.credit(town=K.TOWNS[i], cls="cv"), K.ttl(K.TOPICS[i], "cv")) for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9">%s</div></div>') % (logo("avatar-full", "pa"), K.MPI, covers)
    out.append(a("l-grid", "ph9 light", grid, "4 · Profile grid", 360, 640))
    # 5 avatar among other accounts, by size: full at 110, mid at 40, solid at 16
    others = [("#7A4E9E", "RJ"), ("#2F6FA3", "MB"), ("#B4532A", "TK")]
    big = '<span class="oav" style="background:%s">%s</span><span class="gav">%s</span><span class="oav" style="background:%s">%s</span>' % (others[0][0], others[0][1], logo("avatar-full"), others[1][0], others[1][1])
    rows = '<li><span class="gav s">%s</span><b>Generation Maine</b><span class="fb">Follow</span></li>' % logo("avatar-solid")
    rows += "".join('<li><span class="oav s" style="background:%s">%s</span><b>Account name</b><span class="fb">Follow</span></li>' % (c, t) for c, t in others)
    tab = '<div class="tabbar"><span class="tab on"><i>%s</i>Generation Maine</span><span class="tab"><i class="g"></i>Other site</span></div>' % logo("favicon")
    avs = '<div class="avs"><p class="k">Profile size, 110 px: full cut</p><div class="row3">%s</div><p class="k">List size, 40 px: solid, since the state inside is 27 px</p><ul class="sugg">%s</ul><p class="k">Browser tab, 16 px: solid</p>%s</div>' % (big, rows, tab)
    out.append(a("l-avatar", "light", avs, "5 · Avatar among other accounts, one cut per size", 480, 640))
    # 6 Substack header and email: the lockup on a Spruce masthead, the disclosure under it
    sub = ('<div class="subst s"><div class="ssh">%s</div><p class="sdisc">%s</p><div class="sb"><h3>[Post title in plain words]</h3>%s'
           '<p>[First paragraph in the creator\'s own words.]</p><p>[Body continues.]</p><p>[Body continues.]</p></div>'
           '<p class="sfoot">Short videos and this newsletter are made by young Maine creators. %s.</p></div>') % (two_rev, K.MPI, K.credit(town="Belfast", cls="by"), K.MPI)
    out.append(a("l-substack", "light", sub, "6 · Substack header and email", 480, 640))
    # 8 collab post on a creator's own account
    post = '<div class="pimg"><div class="foot"></div>%s<div class="sl3 p">%s</div></div>' % (bug, K.credit(town="Machias", cls="lg"))
    collab = ('<div class="feed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    out.append(a("l-collab", "ph9 light", collab, "8 · Collab post on a creator's own account", 360, 640))
    # 7 website hero, no photo: the mural to the right, the headline low left, the lockup in the nav
    hero = ('<div class="web s lhero"><div class="wn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<p class="sdisc w">%s</p><div class="lmural">%s</div>'
            '<div class="lh1">%s'
            '<p class="wlede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="wbtn"><span class="b1">Meet the creators</span><span class="b2">Follow along</span></p></div></div>') % (lock_rev, K.MPI, mural(760, MOSS, MOSS, n=64), K.ttl("Young Mainers on building a life here", "lh"))
    web = a("l-web", "", hero, "7 · Website hero, no photo", 1200, 680)
    return "".join(out), web


CSS_ADD = r"""
.lbug{position:absolute;top:44px;left:var(--M)}
.lbug svg{height:22px;width:auto;display:block;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
.lk{height:auto;display:block}
.lend{position:absolute;inset:0;background:var(--sp);padding:44px var(--M) var(--M);display:flex;flex-direction:column}
.lend .lk.two{width:148px}
.lmur{flex:1;display:flex;align-items:center;justify-content:center;padding:18px 0 10px}
.lmur .mural{height:272px;width:auto;display:block}
.lend .ttl{margin-bottom:16px;font-size:52px}
.lend .hl.s{font-size:13px}.lend .hl.s li{padding:8px 0}
.lend .disc{margin-top:18px}
.pav svg{width:62px;height:62px;border-radius:50%;display:block}
.gav svg{width:100%;height:100%;display:block}
.tab i svg{width:16px;height:16px;display:block}
.ssh .lk.two{width:200px}
.web.s .wn .lk{height:28px;width:auto}
.lmural{position:absolute;right:56px;top:-40px;height:760px;z-index:1}
.lmural .mural{height:100%;width:auto;display:block}
.lh1{position:absolute;left:56px;bottom:56px;z-index:2;max-width:640px}
.lh1 .ttl.lh{font:800 92px/.9 Bric;letter-spacing:-.03em;margin:0 0 26px;max-width:11ch;color:var(--bi)}
.lh1 .wlede{margin:0 0 22px;font-size:18px;max-width:40ch}
"""


def build():
    m = K.build_logos()   # the round-two master files, still needed by the shared mockup helpers
    boards, web = mockups()
    css = K.CSS + CSS_ADD
    for k, v in {"{{F800}}": K.font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
                 "{{F700}}": K.font64("brand/v6/fonts-web/bricolage-grotesque-700.woff2"),
                 "{{FCOND}}": K.font64("brand/v4/fonts-web/bricolage-condensed-800.woff2"),
                 "{{FINTER}}": K.font64("generation-maine/assets/fonts/inter-var.woff2")}.items():
        css = css.replace(k, v)
    for k, v in C.items():
        css = css.replace("{{%s}}" % k, v)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Generation Maine, the logo applied</title><style>%s</style></head><body>'
            '<header class="top"><div class="w"><p class="k" style="color:var(--mg)">Generation Maine · The logo applied</p><h1>Maine in lines, where it will live</h1>'
            '<p>The size system in use: the full cut on the end card, the hero and the profile picture, the mid cut in lists, the solid cut in the video bug and the browser tab. The state is one color. Marigold is the dot, once per frame.</p></div></header>'
            '<section><div class="w"><div class="cards">%s</div><div class="cards">%s</div></div></section></body></html>') % (css, boards, web)
    write(OUT + "/apply.html", page)


if __name__ == "__main__":
    build()
    print("apply.html written")
