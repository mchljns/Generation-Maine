"""Bark & Sky, round two of color and mark.

Color: four field pairings that keep the concept's logic (a pale sky, a dark ground, paper between) and ask what the sky and the
ground are made of; then the accent question on the chosen pairing, since the concept has no equivalent of Marigold once per frame.
Mark: the Rising from the ground disc pushed through six variations: horizon height, state size, the lined state, the light line
through the state, the container, equal halves.

  python3 brand/src/build_explore2_barksky.py   # writes brand/identity/marks-bark-sky/explore/{colors,rising}.png and svgs
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, Face, write
from build_v4 import svg, f, rect
import maine2
from build_logo_maine import maine_lines, simplified
import build_marks_barksky as M
import build_horizon_barksky as H
import build_kit as K

OUT = "brand/identity/marks-bark-sky/explore"
S = 240
_N = [0]


def uid(p):
    _N[0] += 1
    return "%s%d" % (p, _N[0])


def lum(hexc):
    r, g, b = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# ------------------------------------------------------------------ the rising mark, parametrized
def rising(sky, ground, line, y_frac=0.6, h=170, base=0.72, cut="solid", through=False, container="disc", size=S):
    """The state stands on the horizon and rises into the sky. cut: solid silhouette, or 'lined' above the horizon.
    through: the light line crosses the state too. container: disc, square (rounded) or none."""
    y = size * y_frac
    cid = uid("r")
    if container == "disc":
        clip = '<circle cx="%s" cy="%s" r="%s"/>' % (f(size / 2), f(size / 2), f(size / 2))
    elif container == "square":
        clip = '<rect x="0" y="0" width="%s" height="%s" rx="%s"/>' % (f(size), f(size), f(size * 0.12))
    else:
        clip = '<rect x="0" y="0" width="%s" height="%s"/>' % (f(size), f(size))
    x0 = (size - h * maine2.ASPECT) / 2
    y0 = y - h * base
    if cut == "lined":
        body, _ = maine_lines(x0, y0, h, ground, ground, "full", gold=False)
        # lines above the horizon, the solid silhouette below it, so the base reads as ground
        ring = simplified(maine2.fit(x0, y0, h * maine2.ASPECT, h), h * 0.012)
        a, b = uid("a"), uid("b")
        state = ('<defs><clipPath id="%s"><rect x="0" y="0" width="%s" height="%s"/></clipPath><clipPath id="%s"><rect x="0" y="%s" width="%s" height="%s"/></clipPath></defs>'
                 '<g clip-path="url(#%s)">%s</g><path d="%s" fill="%s" clip-path="url(#%s)"/>') % (a, f(size), f(y), b, f(y), f(size), f(size), a, body, maine2.path(ring), ground, b)
    else:
        ring = simplified(maine2.fit(x0, y0, h * maine2.ASPECT, h), h * 0.012)
        state = '<path d="%s" fill="%s"/>' % (maine2.path(ring), ground)
    hl = '<rect x="0" y="%s" width="%s" height="3" fill="%s"/>' % (f(y - 1.5), f(size), line)
    inner = rect(0, 0, size, y, sky) + rect(0, y, size, size - y, ground) + state + hl if through else rect(0, 0, size, y, sky) + rect(0, y, size, size - y, ground) + state + hl.replace('width="%s"' % f(size), 'width="0"')
    if not through:
        # the line sits on the ground only where the state is not: draw it, then the state over it, then a strip of ground across
        # the state's footprint so the coast's inlets at the horizon do not leave specks of line
        ring_w = h * maine2.ASPECT
        xs = maine2.crossings(simplified(maine2.fit(x0, y0, ring_w, h), h * 0.012), y)
        strip = rect(xs[0] + 1, y - 2, xs[-1] - xs[0] - 2, 6, ground) if len(xs) >= 2 else ""
        inner = rect(0, 0, size, y, sky) + rect(0, y, size, size - y, ground) + hl + state + strip
    if container == "none":
        return inner
    return '<defs><clipPath id="%s">%s</clipPath></defs><g clip-path="url(#%s)">%s</g>' % (cid, clip, cid, inner)


# ------------------------------------------------------------------ color
PALETTES = [
    ("Bark & Sky", "as it stands", dict(sky="#CFE3F0", ground="#2B211C", paper="#FFFFFF", mist="#EEF4F8", clay="#5E4E43"),
     "A clear morning over dark ground. Cool against warm, which is what keeps it from reading as a weather app."),
    ("Dawn", "a warmer sky", dict(sky="#F2DCCA", ground="#33251E", paper="#FFFCF8", mist="#F9F0E8", clay="#78584A"),
     "Seven in the morning in October. Warm on warm is softer and more literary, and it loses the one contrast the concept had. It also drifts toward a bakery."),
    ("Fog & Granite", "a cooler ground", dict(sky="#DCE3E6", ground="#2E3236", paper="#FFFFFF", mist="#F0F3F4", clay="#5A6266"),
     "Coastal fog over ledge. Calm and serious, and it is the palette of every public-radio app. Nothing in it says warmth or a person."),
    ("Barrens", "a redder ground", dict(sky="#CFE3F0", ground="#46261F", paper="#FFFFFF", mist="#EEF4F8", clay="#6E4A3D"),
     "The blueberry barrens after the first frost, when the whole ground turns rust. Still a brown, so still clear of the flag, and it is the one ground that is a Maine thing without being a picture of one."),
]

ACCENTS = [
    ("None", None, "The concept as written. Links and buttons are Bark. Nothing is ever the loud thing."),
    ("Blueberry", "#2F4E7A", "The sky's dark sibling. Links, the horizon line on paper, and the one-in-nine cover. It stays in the family and it reads as a link without being told to."),
    ("Lichen", "#8FA98B", "The pale green on the north side of a spruce. Quiet, and too close to Signature's greens to be this concept's own."),
    ("Lamp", "#D9A54E", "One warm light in a window. It is Marigold by another name, and it drags Signature's one idea into the quiet concept."),
]


def font_css():
    return ("@font-face{font-family:HS;src:url(data:font/ttf;base64,%s) format('truetype')}@font-face{font-family:HSans;src:url(data:font/ttf;base64,%s) format('truetype')}"
            % (K.font64("brand/fonts/d/HedvigLettersSerif-24.ttf"), K.font64("brand/fonts/d/HedvigLettersSans-Regular.ttf")))


def wm(fg):
    d, w = M.SERIF.path("generation maine", 100, 0, 78, -8)
    return '<path fill="%s" d="%s"/>' % (fg, d), w


def colors_sheet():
    rows = ""
    files = {}
    for name, sub, c, note in PALETTES:
        sky, gr, pa, mi, cl = c["sky"], c["ground"], c["paper"], c["mist"], c["clay"]
        mark = svg(S, S, rising(sky, gr, pa), name)
        files["palette-%s" % name.lower().replace(" & ", "-").replace(" ", "-")] = mark
        b, w = wm(gr)
        lk = svg(w + S * 0.46 + 28, 114, '<g transform="translate(0 2) scale(.4583)">%s</g>' % rising(sky, gr, pa) + '<g transform="translate(%s 14)">%s</g>' % (f(S * 0.46 + 28), b), name)
        def inl(sv, style):
            return sv.replace('role="img"', "").replace("<svg ", '<svg style="%s" ' % style, 1)
        hero = ('<div class="hero" style="background:%s;color:%s">%s<p class="h1">young mainers on building a life here</p>'
                '<p class="lede" style="color:%s">Young Mainers film the rules that shape their lives.</p><span class="btn" style="background:%s;color:%s">watch the stories</span></div>'
                % (sky, gr, inl(mark, "width:72px;height:72px"), gr, gr, pa))
        dark = ('<div class="dark" style="background:%s;color:%s"><p class="q">“Forty minutes each way for a job that pays the rent. Barely.”</p><p class="by">Cole <span style="color:%s;opacity:.72">Machias, Maine</span></p></div>' % (gr, sky, sky))
        paper = ('<div class="paper" style="background:%s;color:%s"><p class="k" style="color:%s">skowhegan, maine</p><p class="nm">maya</p><p class="bio">I grew up here and came back after two years in Portland.</p>'
                 '<div class="sw"><i style="background:%s"></i><i style="background:%s"></i><i style="background:%s"></i><i style="background:%s;box-shadow:inset 0 0 0 1px #ddd"></i><i style="background:%s"></i></div></div>' % (pa, gr, cl, sky, gr, mi, pa, cl))
        contrast = ("<table class=\"c\"><tr><td>ground on sky</td><td>%.1f</td></tr><tr><td>clay on sky</td><td>%.1f</td></tr><tr><td>clay on paper</td><td>%.1f</td></tr><tr><td>sky on ground</td><td>%.1f</td></tr></table>"
                    % (ratio(gr, sky), ratio(cl, sky), ratio(cl, pa), ratio(sky, gr)))
        rows += ('<div class="row"><div class="lab"><b>%s</b><span>%s</span><p>%s</p>%s</div>%s%s%s<div class="t lk">%s</div></div>'
                 % (name, sub, note, contrast, hero, dark, paper, inl(lk, "width:100%;height:auto")))
    # the accent question on the base palette
    c = PALETTES[0][2]
    sky, gr, pa, mi, cl = c["sky"], c["ground"], c["paper"], c["mist"], c["clay"]
    arows = ""
    for name, acc, note in ACCENTS:
        link = acc or gr
        btn_bg = acc or gr
        line = acc or pa
        cover_bg = acc or mi
        cover_fg = pa if acc else gr
        mk = rising(sky, gr, line if acc else pa)
        arows += ('<div class="arow"><div class="lab"><b>%s</b>%s<p>%s</p></div>'
                  '<div class="paper acc" style="background:%s;color:%s"><p class="bio">Each story in full, with <a style="color:%s;border-bottom:1.5px solid %s">the numbers behind it</a>.</p>'
                  '<span class="btn" style="background:%s;color:%s">subscribe</span></div>'
                  '<div class="cov" style="background:%s;color:%s"><p>starting a shop</p></div>'
                  '<div class="t"><svg style="width:120px;height:120px" viewBox="0 0 240 240">%s</svg></div></div>'
                  % (name, (' <i class="dot" style="background:%s"></i>' % acc) if acc else "", note, pa, gr, link, link, btn_bg, pa, cover_bg, cover_fg, mk))
    page = ('<!doctype html><html><head><meta charset="utf-8"><title>Bark &amp; Sky, color</title><style>%s'
            'body{margin:0;background:#E9E5DA;padding:36px;font-family:HSans,sans-serif;color:#2B211C}h1{font:400 30px HS;margin:0 0 6px}.intro{font:14px/1.45 HSans;color:#5E4E43;max-width:820px;margin:0 0 26px}'
            'h2{font:400 22px HS;margin:34px 0 14px}'
            '.row{display:grid;grid-template-columns:300px 300px 230px 230px 1fr;gap:16px;align-items:stretch;margin-bottom:18px}'
            '.lab b{display:block;font:400 18px HS}.lab span{display:block;font:12px HSans;color:#5E4E43;margin:2px 0 8px}.lab p{margin:0 0 10px;font:12.5px/1.45 HSans;color:#5E4E43}'
            'table.c{border-collapse:collapse;font:11px HSans;color:#5E4E43}table.c td{padding:2px 10px 2px 0}table.c td:last-child{color:#2B211C}'
            '.hero,.dark,.paper{border-radius:12px;padding:22px;display:flex;flex-direction:column;justify-content:center}'
            '.hero{align-items:center;text-align:center}.hero svg{display:block;margin-bottom:12px}.h1{font:400 30px/1.02 HS;letter-spacing:-.02em;margin:0 0 10px;max-width:11ch}.lede{font:13px/1.45 HSans;margin:0 0 14px;max-width:26ch}'
            '.btn{display:inline-block;padding:10px 18px;border-radius:999px;font:13px HSans}'
            '.q{font:400 22px/1.15 HS;margin:0 0 12px}.by{font:400 15px HS;margin:0}.by span{font:12px HSans;margin-left:6px}'
            '.k{font:12px HSans;letter-spacing:.08em;margin:0 0 6px}.nm{font:400 36px/1 HS;margin:0 0 10px}.bio{font:15px/1.45 HSans;margin:0 0 14px}'
            '.sw{display:flex;gap:6px}.sw i{display:block;width:26px;height:26px;border-radius:50%%}'
            '.t{border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;padding:18px}.t.lk{padding:24px 28px}'
            '.arow{display:grid;grid-template-columns:300px 360px 200px 160px;gap:16px;margin-bottom:16px;align-items:stretch}.arow .lab b{font-size:17px;display:inline-block}.dot{display:inline-block;width:12px;height:12px;border-radius:50%%;vertical-align:middle;margin-left:8px}'
            '.acc{border-radius:12px;padding:22px}.acc a{text-decoration:none;padding-bottom:1px}.cov{border-radius:12px;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px}.cov p{font:400 24px/1.05 HS;margin:0}'
            '</style></head><body><h1>Bark &amp; Sky: the color question</h1>'
            '<p class="intro">The concept is a pale sky, a dark ground and paper between. Four pairings ask what the sky and the ground are made of, each shown as a hero, a dark surface, a paper surface and the lockup, with contrast measured. Then the accent question on the current pairing: the concept has no equivalent of Marigold once per frame, and four answers are tried on a link, a button, a cover and the horizon line.</p>'
            '<h2>Four pairings</h2>%s<h2>The accent, on Bark &amp; Sky</h2>%s</body></html>') % (font_css(), rows, arows)
    for k, v in files.items():
        write("%s/%s.svg" % (OUT, k), v)
    write(OUT + "/colors.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), os.path.join(ROOT, OUT, "colors.html"), os.path.join(ROOT, OUT, "colors.png"), "1560"], check=True)


# ------------------------------------------------------------------ the mark
BK, SK, PA = H.BK, H.SK, H.PA
RISING = [
    ("r1", "Rising, as drawn", "Horizon at 60 percent, the state at 170, its base a third under the ground.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK)),
    ("r2", "Lower horizon, larger state", "Horizon at 66 percent, the state at 200. More sky, more land, a smaller strip of ground.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, y_frac=0.66, h=200, base=0.7)),
    ("r3", "The lined state rising", "The shared sixteen lines above the horizon, the solid silhouette below it. The system mark and the disc in one, with the lines standing in for weather.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, cut="lined")),
    ("r4", "The line runs through", "The light line crosses the state as well as the ground, so the horizon is one unbroken stroke.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, through=True)),
    ("r5", "Square tile", "The same drawing in a rounded square, for app icons and covers.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, container="square")),
    ("r6", "No container", "The horizon runs to the edge of whatever holds it. A field, not a badge, for the hero and the end card.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, container="none")),
    ("r8", "Recommended: lower horizon, line through", "Horizon at 64 percent, the state at 190, the light line unbroken. The state stands behind the horizon like land seen across water.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, y_frac=0.64, h=190, base=0.7, through=True)),
    ("r7", "Equal halves", "Horizon at 50 percent. Calmer, and the state has less sky to stand in.", lambda fg, bg: rising(SK, H.ground_of(fg), PA if fg == BK else BK, y_frac=0.5, h=150, base=0.66)),
]

if __name__ == "__main__":
    colors_sheet()
    M.build([(k, t, n, d, "round") for k, t, n, d in RISING], OUT, "Rising from the ground, pushed",
            "Seven variations on the mark the client picked. Each row: on Paper, on Bark, the avatar at 110, 40 and 16 px, and the horizontal lockup.")
    os.replace(os.path.join(ROOT, OUT, "candidates.png"), os.path.join(ROOT, OUT, "rising.png"))
    os.replace(os.path.join(ROOT, OUT, "candidates.html"), os.path.join(ROOT, OUT, "rising.html"))
    print("explore sheets written")
