"""Identity v4: three concepts built on Spruce & Signal (the direction that has worked best).

Audience: young adults who are new or recent voters, plus readers of The Maine Wire.
Palette: Spruce and Ballot Amber. No pink, no orange, no lime, no italics.

  Spruce & Amber : the v1 wordmark and record dot, recolored and tightened
  Ballot         : the dot on the i becomes a filled-in ballot oval
  Front Page     : a newspaper nameplate and TV-news chyrons

Writes brand/v4/concepts.html and brand/v4/<concept>/*.svg.
Run from the repo root: python3 brand/src/build_v4.py && node brand/src/render_v4.mjs
"""
import base64
import os

from gmlib import ROOT, Face, contours, contour_group, write
from build_brand import DISPLAY, TRACK, DOT_R, DOT_CY

OUT = "brand/v4"
COND = Face(os.path.join(ROOT, "brand", "fonts", "v4", "BricolageGrotesque-CondensedExtraBold.ttf"))

P = {
    "spruce": "#0B4A34", "pine": "#07261C", "amber": "#FFB81C", "paper": "#F2F4F7",
    "ink": "#121417", "moss": "#34795A", "white": "#FFFFFF", "mist": "#C9D3CF",
}


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def svg(w, h, body, label, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s%s</svg>'
            % (f(w), f(h), f(w), f(h), label, ("<defs>%s</defs>" % defs) if defs else "", body))


def rect(x, y, w, h, fill, rx=0):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h), f(rx), fill)


def text(x, y, s, size, fill, fam="Inter", weight=600, anchor="start", ls=0, upper=False):
    fams = {"Inter": "Inter,Arial,sans-serif", "Bric": "'Bricolage Grotesque',Arial,sans-serif",
            "Cond": "'Bricolage Condensed','Arial Narrow',sans-serif"}
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" style="font-family:%s;font-weight:%d;letter-spacing:%sem%s">%s</text>'
            % (f(x), f(y), f(size), fill, anchor, fams[fam], weight, ls, ";text-transform:uppercase" if upper else "", s))


# ------------------------------------------------------------------ wordmarks
def wm_dot(txt, size, x, y, fg, mark, dot_index, shape="circle"):
    """Bricolage ExtraBold wordmark. The i at dot_index loses its tittle and gets a circle or a ballot oval."""
    s = size / DISPLAY.upem
    t = txt[:dot_index] + "ı" + txt[dot_index + 1:]
    d, w = DISPLAY.path(t, size, x, y, TRACK)
    pos = [p for p in DISPLAY.glyph_positions(t, size, x, TRACK) if p[2] == dot_index][0]
    b = DISPLAY.glyph_bounds("dotlessi")
    cx = pos[1] + (b[0] + b[2]) / 2 * s
    cy = y - DOT_CY * s
    r = DOT_R * s
    out = '<path fill="%s" d="%s"/>' % (fg, d)
    if shape == "circle":
        out += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), mark)
    else:  # ballot oval: wider than tall, like the target on a Maine ballot
        out += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(cx), f(cy + r * 0.12), f(r * 1.42), f(r * 0.86), mark)
    return out, w


def wordmark_one_line(fg, mark, shape, size=100):
    body, w = wm_dot("Generation Maine", size, 0, size * 0.74, fg, mark, 13, shape)
    return body, w, size * 0.76


def wordmark_stacked(fg, mark, shape, size=100):
    b1, w1 = wm_dot("Generation", size, 0, size * 0.74, fg, mark, 7, shape)   # dot on the i in Generation too
    b1 = '<path fill="%s" d="%s"/>' % (fg, DISPLAY.path("Generation", size, 0, size * 0.74, TRACK)[0])
    w1 = DISPLAY.path("Generation", size, 0, size * 0.74, TRACK)[1]
    b2, w2 = wm_dot("Maine", size, 0, size * 0.74 + size * 0.84, fg, mark, 2, shape)
    return b1 + b2, max(w1, w2), size * 0.74 + size * 0.84 + size * 0.04


def g_icon(x, y, s, bg, fg, mark, shape="circle", rx=None):
    """Square icon: a bold G with the mark at its upper right."""
    size = s * 0.78
    sc = size / DISPLAY.upem
    gb = DISPLAY.glyph_bounds("G")
    gw, gh = (gb[2] - gb[0]) * sc, (gb[3] - gb[1]) * sc
    r = DOT_R * 1.15 * sc
    mw = r * (1.42 if shape == "oval" else 1)
    gap = r * 0.35
    total = gw + gap + 2 * mw
    x0 = x + (s - total) / 2 - gb[0] * sc
    base = y + s / 2 + gh / 2 + gb[1] * sc
    d, _ = DISPLAY.path("G", size, x0, base)
    mcx = x0 + gb[2] * sc + gap + mw
    mcy = base - gb[3] * sc + r
    out = rect(x, y, s, s, bg, rx if rx is not None else 0) if bg else ""
    out += '<path fill="%s" d="%s"/>' % (fg, d)
    if shape == "circle":
        out += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(mcx), f(mcy), f(r), mark)
    else:
        out += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(mcx), f(mcy), f(r * 1.42), f(r * 0.86), mark)
    return out


def placed(body, x, y, sc):
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (f(x), f(y), f(sc), body)


def pattern(w, h, color, op=0.5, seeds=((0.82, 0.18, 11), (0.12, 0.9, 5))):
    b = ""
    for fx, fy, sd in seeds:
        b += contour_group(contours(w * fx, h * fy, 18, 40, max(w, h) * 0.035, sd), color, max(w, h) / 600, op)
    return b


# ------------------------------------------------------------------ shared applications
HANDLES = (("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com"))


def end_card(shape, bullet):
    c = P
    e = rect(0, 0, 1080, 1920, c["spruce"]) + pattern(1080, 1920, c["moss"], 0.55)
    wm, w, h = wordmark_stacked(c["paper"], c["amber"], shape)
    e += placed(wm, 150, 480, 780 / w)
    e += text(150, 1030, "Follow along", 76, c["amber"], "Bric", 800, ls=-0.01)
    y = 1150
    for lab, hd in HANDLES:
        e += bullet(166, y - 14, 11)
        e += text(200, y, lab, 38, c["paper"], weight=600)
        e += text(470, y, hd, 38, c["paper"], weight=400)
        y += 74
    e += text(150, 1560, "An initiative of Maine Policy Institute", 32, c["paper"], weight=500)
    return svg(1080, 1920, e, "End card")


def hero_mock(shape, extra=""):
    c = P
    b = rect(0, 0, 1440, 760, c["spruce"]) + pattern(1440, 760, c["moss"], 0.6, ((0.86, 0.2, 11), (0.08, 1.0, 5)))
    b += rect(0, 0, 1440, 72, c["spruce"])
    wm, w, h = wordmark_one_line(c["paper"], c["amber"], shape)
    b += placed(wm, 96, 24, 200 / w)
    for i, t in enumerate(("About", "Creators", "Follow")):
        b += text(1150 + i * 100, 44, t, 16, c["paper"], weight=600)
    b += text(96, 220, "AN INITIATIVE OF MAINE POLICY INSTITUTE", 15, c["amber"], weight=700, ls=0.12)
    b += text(96, 316, "Young Mainers on", 84, c["paper"], "Bric", 800, ls=-0.015)
    b += text(96, 404, "building a life here.", 84, c["paper"], "Bric", 800, ls=-0.015)
    b += text(96, 470, "Short videos by young Maine creators about the rules that shape their lives.", 22, c["paper"], weight=400)
    b += rect(96, 520, 210, 56, c["amber"], 28) + text(201, 555, "Meet the creators", 18, c["ink"], weight=700, anchor="middle")
    b += '<rect x="322" y="521" width="178" height="54" rx="27" fill="none" stroke="%s" stroke-width="2"/>' % c["paper"]
    b += text(411, 555, "Follow along", 18, c["paper"], weight=700, anchor="middle")
    return svg(1440, 760, b + extra, "Website hero")


# ------------------------------------------------------------------ concept 1: Spruce & Amber
def build_amber():
    c = P
    s = {}
    dot = lambda x, y, r: '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), f(r), c["amber"])
    wm, w, h = wordmark_one_line(c["spruce"], c["amber"], "circle")
    s["lockup"] = svg(w, h, wm, "Generation Maine")
    wm, w, h = wordmark_one_line(c["paper"], c["amber"], "circle")
    s["lockup-rev"] = svg(w, h, wm, "Generation Maine")
    s["symbol"] = svg(200, 200, g_icon(0, 0, 200, c["spruce"], c["paper"], c["amber"], "circle", 0), "Icon")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["spruce"]) + pattern(1080, 1080, c["moss"], 0.5) + g_icon(190, 190, 700, None, c["paper"], c["amber"]), "Avatar")
    s["endcard"] = end_card("circle", dot)
    l = rect(96, 812, 820, 172, c["paper"], 26) + rect(96, 812, 26, 172, c["amber"], 13)
    l += text(160, 896, "[Creator name]", 64, c["spruce"], "Bric", 800, ls=-0.01)
    l += text(162, 952, "[Hometown], Maine", 38, c["ink"], weight=600)
    s["lowerthird"] = svg(1920, 1080, l, "Lower third")
    s["hero"] = hero_mock("circle")
    return s


# ------------------------------------------------------------------ concept 2: Ballot
def oval(x, y, r, fill, outline=None):
    o = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(x), f(y), f(r * 1.42), f(r * 0.86), fill)
    if outline:
        o = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            f(x), f(y), f(r * 1.42), f(r * 0.86), outline, f(r * 0.22)) + o
    return o


def build_ballot():
    c = P
    s = {}
    wm, w, h = wordmark_one_line(c["spruce"], c["amber"], "oval")
    s["lockup"] = svg(w, h, wm, "Generation Maine")
    wm, w, h = wordmark_one_line(c["paper"], c["amber"], "oval")
    s["lockup-rev"] = svg(w, h, wm, "Generation Maine")
    s["symbol"] = svg(200, 200, g_icon(0, 0, 200, c["spruce"], c["paper"], c["amber"], "oval", 0), "Icon")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["spruce"]) + pattern(1080, 1080, c["moss"], 0.5) + g_icon(190, 190, 700, None, c["paper"], c["amber"], "oval"), "Avatar")
    s["endcard"] = end_card("oval", lambda x, y, r: oval(x + 4, y, r, c["amber"]))
    l = rect(96, 812, 860, 172, c["paper"], 26)
    l += oval(150, 898, 22, c["amber"])
    l += text(204, 896, "[Creator name]", 64, c["spruce"], "Bric", 800, ls=-0.01)
    l += text(206, 952, "[Hometown], Maine", 38, c["ink"], weight=600)
    s["lowerthird"] = svg(1920, 1080, l, "Lower third")
    s["hero"] = hero_mock("oval")
    # Device: the topic list as a ballot. The filled oval marks the topic of the video.
    rows = ["Housing", "Jobs", "Cost of living", "Starting a business", "Staying in Maine"]
    d = rect(0, 0, 520, 380, c["paper"], 18) + text(32, 56, "THIS EPISODE", 18, c["moss"], weight=700, ls=0.12)
    for i, r_ in enumerate(rows):
        y = 104 + i * 58
        d += oval(52, y - 8, 14, c["amber"] if i == 0 else "none", c["spruce"])
        d += text(92, y, r_, 28, c["ink"], weight=600)
    s["device"] = svg(520, 380, d, "Ballot topic card")
    return s


# ------------------------------------------------------------------ concept 3: Front Page
def nameplate(fg, rule, dot, width=1000):
    """GENERATION MAINE set as a newspaper nameplate: heavy rule, condensed caps, thin rule, dateline."""
    size = 150
    d, w = COND.path("GENERATION MAINE", size, 0, 0, 10)
    sc = width / w
    b = rect(0, 0, width, 10, rule)
    d, w = COND.path("GENERATION MAINE", size * sc, 0, 22 + size * sc * 0.72, 10)
    b += '<path fill="%s" d="%s"/>' % (fg, d)
    y2 = 22 + size * sc * 0.72 + 22
    b += rect(0, y2, width, 3, rule)
    b += text(0, y2 + 34, "VOL. 1", 22, fg, weight=700, ls=0.12)
    b += text(width / 2, y2 + 34, "YOUNG MAINERS ON BUILDING A LIFE HERE", 22, fg, weight=700, anchor="middle", ls=0.12)
    b += '<circle cx="%s" cy="%s" r="7" fill="%s"/>' % (f(width - 112), f(y2 + 27), dot)
    b += text(width, y2 + 34, "MAINE", 22, fg, weight=700, anchor="end", ls=0.12)
    return b, width, y2 + 48


def fp_icon(x, y, s, bg, fg, dot):
    """GEN over ME, stacked in condensed caps between rules, like a newspaper ear."""
    b = rect(x, y, s, s, bg) if bg else ""
    k = s / 200.0
    b += rect(x + 28 * k, y + 30 * k, 144 * k, 8 * k, fg)
    d, w = COND.path("GEN", 70 * k, 0, 0, 20)
    d, w = COND.path("GEN", 70 * k, x + (s - w) / 2, y + 104 * k, 20)
    b += '<path fill="%s" d="%s"/>' % (fg, d)
    d, w2 = COND.path("ME", 70 * k, 0, 0, 20)
    d, w2 = COND.path("ME", 70 * k, x + (s - w2) / 2 - 10 * k, y + 164 * k, 20)
    b += '<path fill="%s" d="%s"/>' % (fg, d)
    b += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x + (s + w2) / 2 + 6 * k), f(y + 152 * k), f(9 * k), dot)
    b += rect(x + 28 * k, y + 174 * k, 144 * k, 3 * k, fg)
    return b


def build_frontpage():
    c = P
    s = {}
    b, w, h = nameplate(c["ink"], c["spruce"], c["amber"])
    s["lockup"] = svg(w, h, b, "Generation Maine nameplate")
    b, w, h = nameplate(c["paper"], c["amber"], c["amber"])
    s["lockup-rev"] = svg(w, h, b, "Generation Maine nameplate")
    s["symbol"] = svg(200, 200, fp_icon(0, 0, 200, c["spruce"], c["paper"], c["amber"]), "Icon")
    s["avatar"] = svg(1080, 1080, rect(0, 0, 1080, 1080, c["spruce"]) + fp_icon(170, 170, 740, None, c["paper"], c["amber"]), "Avatar")
    e = rect(0, 0, 1080, 1920, c["paper"])
    np_, w, h = nameplate(c["ink"], c["spruce"], c["amber"])
    e += placed(np_, 80, 120, 920 / w)
    e += rect(80, 440, 920, 1100, c["spruce"])
    e += text(130, 600, "WATCH THE NEXT STORY", 30, c["amber"], weight=700, ls=0.12)
    e += text(130, 780, "Follow along", 150, c["paper"], "Cond", 800)
    y = 960
    for lab, hd in HANDLES:
        e += text(130, y, lab.upper(), 34, c["amber"], weight=700, ls=0.08)
        e += text(450, y, hd, 40, c["paper"], weight=500)
        y += 110
    e += rect(80, 1620, 920, 4, c["ink"])
    e += text(80, 1690, "An initiative of Maine Policy Institute", 34, c["ink"], weight=600)
    s["endcard"] = svg(1080, 1920, e, "End card")
    # Chyron lower third, like the bar on TV news
    l = rect(96, 836, 1100, 96, c["paper"]) + rect(96, 836, 16, 96, c["amber"])
    l += text(140, 900, "[CREATOR NAME]", 54, c["ink"], "Cond", 800, ls=0.02)
    l += rect(96, 932, 1100, 52, c["spruce"])
    l += text(140, 968, "[HOMETOWN], ME", 26, c["paper"], weight=700, ls=0.1)
    l += text(1176, 968, "GENERATION MAINE", 26, c["amber"], weight=700, anchor="end", ls=0.1)
    s["lowerthird"] = svg(1920, 1080, l, "Chyron")
    np2, w2, h2 = nameplate(c["paper"], c["amber"], c["amber"])
    hero = rect(0, 0, 1440, 760, c["spruce"]) + pattern(1440, 760, c["moss"], 0.6, ((0.86, 0.2, 11), (0.08, 1.0, 5)))
    hero += placed(np2, 96, 60, 1248 / w2)
    hero += text(96, 380, "Young Mainers on building a life here.", 64, c["paper"], "Bric", 800, ls=-0.015)
    hero += text(96, 440, "Short videos by young Maine creators about the rules that shape their lives.", 22, c["paper"], weight=400)
    hero += rect(96, 490, 210, 56, c["amber"], 4) + text(201, 525, "Meet the creators", 18, c["ink"], weight=700, anchor="middle")
    hero += '<rect x="322" y="491" width="178" height="54" rx="4" fill="none" stroke="%s" stroke-width="2"/>' % c["paper"]
    hero += text(411, 525, "Follow along", 18, c["paper"], weight=700, anchor="middle")
    hero += rect(0, 640, 1440, 60, c["amber"]) + text(96, 679, "NOW PLAYING", 18, c["ink"], weight=800, ls=0.14)
    hero += text(270, 679, "[Creator name], [Hometown]: [episode title]", 20, c["ink"], weight=600)
    s["hero"] = svg(1440, 760, hero, "Website hero")
    return s


# ------------------------------------------------------------------ presentation
CRIT = [("Idea", 15), ("Distinct", 20), ("Small size", 15), ("Premium", 15), ("Audience fit", 15), ("Ease", 10), ("System", 10)]
LET = [(9.0, "A+"), (8.5, "A"), (8.0, "A-"), (7.5, "B+"), (7.0, "B"), (6.5, "B-"), (6.0, "C+"), (5.5, "C"), (5.0, "C-"), (0, "D")]


def overall(sc):
    return sum(a * w for a, (_, w) in zip(sc, CRIT)) / 100.0


def letter(v):
    return next(l for cut, l in LET if v >= cut)


CONCEPTS = [
    {"key": "ballot", "name": "Ballot", "build": build_ballot, "rec": True,
     "idea": "The dot on the i becomes a filled-in ballot oval, the mark every Maine voter makes. It says your voice counts without saying who to vote for. New voters get it on sight, and it stays nonpartisan.",
     "why": ["Speaks straight to first-time and recent voters without a party cue.",
             "Keeps everything that worked in Spruce & Signal: the heavy wordmark, the dot, the green.",
             "The oval becomes a device: topic cards set up like a ballot, bullets, a fill-in animation."],
     "risk": "Maine Policy Institute is a nonprofit, so the ballot can never sit next to a candidate, party, measure or \"vote\" call to action. The oval stands for having a say, not for an election.",
     "scores": [9, 8, 8, 7, 9, 9, 8]},
    {"key": "frontpage", "name": "Front Page", "build": build_frontpage, "rec": False,
     "idea": "Generation Maine set as a newspaper nameplate, with a dateline and TV-news chyrons on every video. It borrows the look Maine Wire readers already trust and gives it to young creators.",
     "why": ["Feels like news, which reads as credible to older readers.",
             "Chyrons are native to the short news clips young people already watch.",
             "The nameplate and chyron are easy to template in CapCut."],
     "risk": "Newspaper nameplates are common, and it could be mistaken for a Maine Wire section. That helps reach its readers but blurs the line between reporting and creator stories.",
     "scores": [8, 7, 7, 8, 9, 8, 9]},
    {"key": "amber", "name": "Spruce & Amber", "build": build_amber, "rec": False,
     "idea": "The Spruce & Signal you liked, with the orange swapped for Ballot Amber and the details tightened. The dot on the i is still a record light.",
     "why": ["The safest option: closest to what has already tested well with you.",
             "Amber on spruce is confident and passes AA contrast for text.",
             "Drops straight into the existing website theme."],
     "risk": "Still a styled font more than a brandmark, which caps Idea and Premium.",
     "scores": [6, 8, 8, 7, 8, 9, 7]},
]


def font64(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def build():
    secs, rows = "", ""
    for n, cpt in enumerate(CONCEPTS, 1):
        s = cpt["build"]()
        for k, v in s.items():
            write("%s/%s/%s.svg" % (OUT, cpt["key"], k), v)
        ov = overall(cpt["scores"])
        bars = "".join('<div class="row"><span>%s</span><i><b style="width:%d%%"></b></i><em>%d</em></div>' % (c[0], v * 10, v)
                       for v, c in zip(cpt["scores"], CRIT))
        extra = ('<div class="panel"><p class="label">Device</p>%s</div>' % s["device"]) if "device" in s else ""
        secs += """
<section class="c" id="%(key)s"><div class="wrap">
  <div class="head"><div><p class="label">Concept %(n)d%(rec)s</p><h2>%(name)s</h2><p class="lede">%(idea)s</p></div>
    <div class="grade"><strong>%(letter)s</strong><span>%(ov).2f / 10 projected</span></div></div>
  <div class="hero"><div class="panel web">%(hero)s</div></div>
  <div class="marks">
    <div class="panel light">%(lockup)s</div><div class="panel dark">%(lockrev)s</div>
    <div class="panel sm"><span style="width:96px">%(sym)s</span><span style="width:48px">%(sym)s</span><span style="width:32px">%(sym)s</span><span style="width:16px">%(sym)s</span></div>
  </div>
  <div class="apps">
    <figure class="round">%(avatar)s<figcaption>Avatar</figcaption></figure>
    <figure class="tall">%(end)s<figcaption>9:16 end card</figcaption></figure>
    <figure class="wide lower">%(lower)s<figcaption>Lower third over footage</figcaption></figure>
    %(extra)s
  </div>
  <div class="cols">
    <div><p class="label">Why it works for this audience</p><ul>%(why)s</ul>
      <p class="label" style="margin-top:22px">Risk</p><p>%(risk)s</p></div>
    <div><p class="label">Projected score</p><div class="bars">%(bars)s</div></div>
  </div>
</div></section>""" % {"key": cpt["key"], "n": n, "rec": " · Recommended" if cpt["rec"] else "", "name": cpt["name"],
                       "idea": cpt["idea"], "letter": letter(ov), "ov": ov, "hero": s["hero"], "lockup": s["lockup"],
                       "lockrev": s["lockup-rev"], "sym": s["symbol"], "avatar": s["avatar"], "end": s["endcard"],
                       "lower": s["lowerthird"], "extra": extra, "why": "".join("<li>%s</li>" % w for w in cpt["why"]),
                       "risk": cpt["risk"], "bars": bars}
        rows += "<tr><td><a href='#%s'>%s</a></td>%s<td><b>%.2f</b></td><td><b>%s</b></td></tr>" % (
            cpt["key"], cpt["name"], "".join("<td>%d</td>" % v for v in cpt["scores"]), ov, letter(ov))
    html = (TEMPLATE.replace("{{SECTIONS}}", secs).replace("{{ROWS}}", rows)
            .replace("{{CRITH}}", "".join("<th>%s<br><small>%d%%</small></th>" % c for c in CRIT))
            .replace("{{F_BRIC}}", font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"))
            .replace("{{F_COND}}", font64("brand/v4/fonts-web/bricolage-condensed-800.woff2"))
            .replace("{{F_INTER}}", font64("generation-maine/assets/fonts/inter-var.woff2")))
    for k, v in P.items():
        html = html.replace("{{%s}}" % k, v)
    write(OUT + "/concepts.html", html)
    for cpt in CONCEPTS:
        print("%-15s %.2f %s" % (cpt["name"], overall(cpt["scores"]), letter(overall(cpt["scores"]))))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine: v4 concepts</title>
<style>
@font-face{font-family:'Bricolage Grotesque';src:url(data:font/woff2;base64,{{F_BRIC}}) format("woff2");font-weight:800}
@font-face{font-family:'Bricolage Condensed';src:url(data:font/woff2;base64,{{F_COND}}) format("woff2");font-weight:800}
@font-face{font-family:Inter;src:url(data:font/woff2;base64,{{F_INTER}}) format("woff2");font-weight:400 700}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 Inter,system-ui,sans-serif;color:{{ink}};background:{{paper}}}
.wrap{max-width:1240px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}
.intro{background:{{spruce}};color:{{paper}};padding:72px 0 56px}
.intro h1{font:800 clamp(38px,6vw,78px)/1 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 18px}
.intro h1 span{color:{{amber}}}
.intro p{max-width:68ch}
.label{font:700 12px/1 Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin:0 0 10px}
table{border-collapse:collapse;width:100%;margin-top:26px;font-size:14px}
th,td{padding:8px 6px;border-bottom:1px solid rgba(242,244,247,.2);text-align:center}
th:first-child,td:first-child{text-align:left}
th small{opacity:.65;font-weight:500}
td a{color:{{amber}}}
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;font-size:14px}
@media(max-width:800px){.notes{grid-template-columns:1fr}}
.notes div{border-top:1px solid rgba(242,244,247,.25);padding-top:14px}
.notes b{display:block;margin-bottom:4px}
.c{padding:72px 0;border-bottom:1px solid #DCE1E6}
.c:nth-of-type(odd){background:#fff}
.head{display:flex;justify-content:space-between;gap:24px}
.head h2{font:800 clamp(38px,5vw,66px)/1 'Bricolage Grotesque';letter-spacing:-.02em;margin:0 0 12px;color:{{spruce}}}
.lede{font-size:19px;max-width:62ch}
.grade{text-align:right;flex:none}
.grade strong{display:block;font:800 76px/1 'Bricolage Grotesque';color:{{spruce}}}
.grade span{font-size:13px;opacity:.7}
.panel{border-radius:16px;padding:24px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.c:nth-of-type(odd) .panel.light{background:{{paper}}}
.panel.dark{background:{{spruce}}}
.panel svg{display:block;width:100%;height:auto}
.web{padding:0;overflow:hidden;margin-top:30px;box-shadow:0 30px 70px -30px rgba(0,0,0,.45)}
.marks{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.marks .panel.sm{grid-column:1/-1;display:flex;align-items:flex-end;gap:22px}
.marks .panel.sm span svg{width:100%;height:auto;border-radius:18%}
@media(max-width:860px){.marks{grid-template-columns:1fr}}
.apps{display:grid;grid-template-columns:1fr .7fr 1.6fr;gap:22px;margin-top:22px;align-items:start}
@media(max-width:860px){.apps{grid-template-columns:1fr 1fr}.apps .lower,.apps .panel{grid-column:1/-1}}
.apps figure{margin:0}
.apps figure svg{width:100%;height:auto;display:block;border-radius:14px;box-shadow:0 12px 40px -20px rgba(0,0,0,.45)}
.apps .round svg{border-radius:50%}
.apps .lower svg{background:linear-gradient(135deg,#3b4a42,#6b7a70 55%,#2a3530)}
.apps .panel{grid-column:1/-1;max-width:560px}
figcaption{font:700 11px/1 Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-top:30px}
@media(max-width:860px){.cols{grid-template-columns:1fr}}
ul{padding-left:18px;margin:0}li{margin-bottom:6px}
.bars .row{display:grid;grid-template-columns:110px 1fr 20px;gap:8px;align-items:center;font-size:13px;margin:4px 0}
.bars i{display:block;height:9px;background:#E3E7EC;border-radius:99px;overflow:hidden}
.bars b{display:block;height:100%;background:{{spruce}};border-radius:99px}
.bars em{font-style:normal;font-weight:700;text-align:right}
.end{background:{{spruce}};color:{{paper}};padding:56px 0}
.end p{font-size:20px;max-width:62ch}
</style></head><body>
<section class="intro"><div class="wrap">
  <p class="label">Generation Maine · Identity v4</p>
  <h1>Back to Spruce, now in <span>Amber</span>.</h1>
  <p>Built on the Spruce &amp; Signal direction, for young adults who are new or recent voters and for readers of The Maine Wire. The pink is gone. The accent is Ballot Amber (#FFB81C): 5.9:1 on Spruce, and at least delta E 24 from Baxter, Green Falls and 76crew colors. The heavy Bricolage wordmark and the dot on the i stay.</p>
  <table><tr><th>Concept</th>{{CRITH}}<th>Total</th><th>Grade</th></tr>{{ROWS}}</table>
  <div class="notes">
    <div><b>Audience fit replaces the old Fit score</b>It now asks: would a 19-year-old new voter follow this, and would a Maine Wire reader take it seriously?</div>
    <div><b>Nonpartisan by design</b>No party colors, no candidates, no calls to vote. Civic, not political.</div>
    <div><b>To verify</b>themainewire.com is blocked in this environment, so the side-by-side against it is still to do.</div>
  </div>
</div></section>
{{SECTIONS}}
<section class="end"><div class="wrap">
  <p class="label">Recommendation</p>
  <p>Lead with Ballot. It keeps what you liked in Spruce &amp; Signal and adds an idea new voters get at a glance. Front Page's chyron could be used inside Ballot as the video lower-third style if you want the news feel too.</p>
</div></section>
</body></html>
"""

if __name__ == "__main__":
    build()
