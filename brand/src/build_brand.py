"""Builds every SVG in brand/logo and brand/social, plus the theme's inline logo.

Run from the repo root:  python3 brand/src/build_brand.py
Then render PNGs with:    node brand/src/render.mjs
"""
from gmlib import A, Face, contours, contour_group, svg, write

DISPLAY = Face("BricolageGrotesque-ExtraBold.ttf")
TRACK = -12  # tighter than default, in em/1000

C = A
# The "record dot": the orange tittle on the i in "Maine". It is the signature of the mark.
DOT_R = 96      # font units, a bit larger than the real tittle
DOT_CY = 628    # font units above baseline


def wordmark(text, size, x, y, fg, dot, dot_index=None):
    """Outlined text. If dot_index is given, that 'i' becomes a dotless i plus a round dot."""
    s = size / DISPLAY.upem
    if dot_index is None:
        d, w = DISPLAY.path(text, size, x, y, TRACK)
        return '<path fill="%s" d="%s"/>' % (fg, d), w
    t = text[:dot_index] + "ı" + text[dot_index + 1:]
    d, w = DISPLAY.path(t, size, x, y, TRACK)
    pos = [p for p in DISPLAY.glyph_positions(t, size, x, TRACK) if p[2] == dot_index][0]
    b = DISPLAY.glyph_bounds("dotlessi")
    cx = pos[1] + (b[0] + b[2]) / 2 * s
    cy = y - DOT_CY * s
    out = '<path fill="%s" d="%s"/><circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (
        fg, d, cx, cy, DOT_R * s, dot)
    return out, w


def lockup_horizontal(fg, dot, size=100, pad=0):
    body, w = wordmark("Generation Maine", size, pad, pad + size * 0.73, fg, dot, dot_index=13)
    return body, w + 2 * pad, size * 0.73 + size * 0.02 + 2 * pad


def lockup_stacked(fg, dot, size=100, pad=0):
    lead = size * 0.84
    b1, w1 = wordmark("Generation", size, pad, pad + size * 0.73, fg, dot)
    b2, w2 = wordmark("Maine", size, pad, pad + size * 0.73 + lead, fg, dot, dot_index=2)
    return b1 + b2, max(w1, w2) + 2 * pad, size * 0.73 + lead + size * 0.02 + 2 * pad


def icon_mark(cx, cy, size, fg, dot):
    """A bold G with the record dot at its upper right. Built to sit centered."""
    s = size / DISPLAY.upem
    gb = DISPLAY.glyph_bounds("G")
    gw = (gb[2] - gb[0]) * s
    gh = (gb[3] - gb[1]) * s
    r = DOT_R * 1.15 * s
    gap = r * 0.35
    total_w = gw + gap + 2 * r
    x0 = cx - total_w / 2 - gb[0] * s
    base = cy + gh / 2 + gb[1] * s
    d, _ = DISPLAY.path("G", size, x0, base)
    dcx = x0 + gb[2] * s + gap + r
    dcy = base - gb[3] * s + r
    return '<path fill="%s" d="%s"/><circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (
        fg, d, dcx, dcy, r, dot)


def icon_svg(variant):
    n = 512
    if variant == "color":
        body = '<rect width="512" height="512" rx="0" fill="%s"/>' % C["spruce"]
        body += icon_mark(256, 256, 400, C["fog"], C["signal"])
    elif variant == "black":
        body = icon_mark(256, 256, 400, "#000", "#000")
    else:
        body = icon_mark(256, 256, 400, "#fff", "#fff")
    return svg(n, n, body, "Generation Maine")


VARIANTS = {
    "": (C["spruce"], C["signal"]),
    "-black": ("#000", "#000"),
    "-white": ("#fff", "#fff"),
    "-reversed": (C["fog"], C["signal"]),
}


def build_logos():
    for suf, (fg, dot) in VARIANTS.items():
        body, w, h = lockup_horizontal(fg, dot, 100, 0)
        write("brand/logo/primary%s.svg" % suf, svg(round(w), round(h), body, "Generation Maine"))
        body, w, h = lockup_stacked(fg, dot, 100, 0)
        write("brand/logo/stacked%s.svg" % suf, svg(round(w), round(h), body, "Generation Maine"))
    write("brand/logo/icon.svg", icon_svg("color"))
    write("brand/logo/icon-black.svg", icon_svg("black"))
    write("brand/logo/icon-white.svg", icon_svg("white"))
    # Theme copies: header uses the reversed wordmark on spruce, favicon uses the color icon.
    body, w, h = lockup_horizontal(C["fog"], C["signal"], 100, 0)
    write("generation-maine/assets/img/wordmark-reversed.svg", svg(round(w), round(h), body, "Generation Maine"))
    body, w, h = lockup_horizontal(C["spruce"], C["signal"], 100, 0)
    write("generation-maine/assets/img/wordmark.svg", svg(round(w), round(h), body, "Generation Maine"))
    write("generation-maine/assets/img/icon.svg", icon_svg("color"))
    # Inline version for the header and footer: letters follow currentColor, dot follows the accent color.
    body, w, h = lockup_horizontal("currentColor", "DOT", 100, 0)
    body = body.replace('fill="DOT"', 'class="gm-dot" fill="#FF5B24"')
    write("generation-maine/assets/img/wordmark-inline.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
          'aria-label="Generation Maine" focusable="false">%s</svg>' % (round(w), round(h), round(w), round(h), body))


# ---------- Social kit ----------

FONT_BODY = "font-family:Inter,Arial,sans-serif"
FONT_DISP = "font-family:'Bricolage Grotesque',Arial,sans-serif;font-weight:800"


def text(x, y, s, size, fill, disp=False, weight=None, anchor="start", extra=""):
    style = FONT_DISP if disp else FONT_BODY
    if weight:
        style += ";font-weight:%d" % weight
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" style="%s" %s>%s</text>'
            % (x, y, size, fill, anchor, style, extra, s))


def placed(inner_svg_body, iw, ih, x, y, scale):
    return '<g transform="translate(%.1f %.1f) scale(%.4f)">%s</g>' % (x, y, scale, inner_svg_body)


def pattern_bg(w, h, cx, cy, rings, gap, stroke, width, opacity=1, seed=3, r0=60):
    return contour_group(contours(cx, cy, rings, r0, gap, seed), stroke, width, opacity)


def build_social():
    fog, spruce, signal, moss, lichen = C["fog"], C["spruce"], C["signal"], C["moss"], C["lichen"]
    attrib = "An initiative of Maine Policy Institute"

    # Avatar 1080: icon, circle-safe (all content inside a 760px circle).
    body = '<rect width="1080" height="1080" fill="%s"/>' % spruce
    body += pattern_bg(1080, 1080, 540, 540, 12, 46, moss, 3, 0.55, seed=7, r0=380)
    body += icon_mark(540, 540, 760, fog, signal)
    write("brand/social/avatar-1080.svg", svg(1080, 1080, body, "Generation Maine avatar"))

    # YouTube banner 2560x1440; safe area 1546x423 centered (x 507, y 508.5).
    body = '<rect width="2560" height="1440" fill="%s"/>' % spruce
    body += pattern_bg(2560, 1440, 2250, 300, 22, 58, moss, 4, 0.6, seed=11, r0=60)
    body += pattern_bg(2560, 1440, 260, 1250, 16, 58, moss, 4, 0.6, seed=5, r0=60)
    wm, w, h = lockup_horizontal(fog, signal, 100)
    sc = 1100 / w
    body += placed(wm, w, h, 507 + (1546 - 1100) / 2, 560, sc)
    body += text(1280, 820, "Young Mainers on building a life here.", 58, lichen, anchor="middle", weight=600)
    body += text(1280, 900, "[@handle]  ·  GenerationMaine.org", 40, fog, anchor="middle")
    body += ('<rect x="507" y="508.5" width="1546" height="423" fill="none" stroke="%s" '
             'stroke-dasharray="12 12" stroke-width="2" opacity="0" id="safe-area-guide"/>' % fog)
    write("brand/social/youtube-banner-2560x1440.svg", svg(2560, 1440, body, "Generation Maine YouTube banner"))

    # YouTube thumbnail 1280x720: face on the left, title on the right.
    body = '<rect width="1280" height="720" fill="%s"/>' % fog
    body += ('<rect x="40" y="40" width="660" height="640" rx="36" fill="%s"/>' % spruce)
    body += '<clipPath id="photo"><rect x="40" y="40" width="660" height="640" rx="36"/></clipPath>'
    body += '<g clip-path="url(#photo)">%s</g>' % pattern_bg(660, 640, 370, 360, 10, 40, moss, 3, 0.7, seed=9, r0=40)
    body += text(370, 372, "[Creator photo here]", 34, fog, anchor="middle", weight=600)
    body += text(750, 250, "[Three to five", 76, spruce, disp=True)
    body += text(750, 336, "word title]", 76, spruce, disp=True)
    body += '<rect x="750" y="400" width="140" height="16" rx="8" fill="%s"/>' % signal
    body += icon_mark(1190, 630, 110, spruce, signal)
    write("brand/social/youtube-thumbnail-1280x720.svg", svg(1280, 720, body, "Generation Maine YouTube thumbnail frame"))

    # 9:16 end card 1080x1920.
    body = '<rect width="1080" height="1920" fill="%s"/>' % spruce
    body += pattern_bg(1080, 1920, 900, 1700, 18, 52, moss, 3, 0.6, seed=4, r0=50)
    body += pattern_bg(1080, 1920, 120, 200, 10, 52, moss, 3, 0.6, seed=8, r0=50)
    wm, w, h = lockup_stacked(fog, signal, 100)
    sc = 760 / w
    body += placed(wm, w, h, 160, 520, sc)
    body += text(160, 1020, "Follow Generation Maine", 64, lichen, disp=True)
    rows = [("Instagram", "[@handle]"), ("TikTok", "[@handle]"), ("YouTube", "[@handle]"), ("Substack", "[name].substack.com")]
    y = 1140
    for label, handle in rows:
        body += '<circle cx="176" cy="%d" r="12" fill="%s"/>' % (y - 16, signal)
        body += text(214, y, label, 40, fog, weight=600)
        body += text(460, y, handle, 40, fog)
        y += 76
    body += text(160, 1520, attrib, 32, fog)
    write("brand/social/end-card-1080x1920.svg", svg(1080, 1920, body, "Generation Maine video end card"))

    # Lower third 1920x1080, transparent. Title-safe margin 96px.
    body = '<rect x="96" y="792" width="880" height="192" rx="28" fill="%s"/>' % fog
    body += '<rect x="96" y="792" width="28" height="192" rx="14" fill="%s"/>' % signal
    body += text(160, 880, "[Creator name]", 72, spruce, disp=True)
    body += text(162, 942, "[Hometown], Maine", 40, C["ink"], weight=600)
    write("brand/social/lower-third-1920x1080.svg", svg(1920, 1080, body, "Generation Maine lower third"))

    # Substack square logo and header wordmark.
    write("brand/social/substack-logo-1080.svg",
          svg(1080, 1080, '<rect width="1080" height="1080" fill="%s"/>' % spruce
              + icon_mark(540, 540, 700, fog, signal), "Generation Maine Substack logo"))
    wm, w, h = lockup_horizontal(spruce, signal, 100)
    sc = 1300 / w
    write("brand/social/substack-header-1600x400.svg",
          svg(1600, 400, placed(wm, w, h, 150, 200 - h * sc / 2, sc), "Generation Maine Substack header",
              bg=fog))

    # Open Graph share card 1200x630.
    body = '<rect width="1200" height="630" fill="%s"/>' % spruce
    body += pattern_bg(1200, 630, 1060, 120, 14, 44, moss, 3, 0.6, seed=2, r0=40)
    wm, w, h = lockup_horizontal(fog, signal, 100)
    sc = 860 / w
    body += placed(wm, w, h, 80, 210, sc)
    body += text(84, 400, "Young Mainers on building a life here.", 44, lichen, weight=600)
    body += text(84, 560, attrib, 28, fog)
    write("brand/social/og-share-card-1200x630.svg", svg(1200, 630, body, "Generation Maine"))


def build_pattern_tile():
    """Hero background art for the theme: contour rings on transparent, drawn in moss."""
    body = pattern_bg(1600, 1000, 1350, 250, 20, 48, C["moss"], 2.5, 0.75, seed=11, r0=40)
    body += pattern_bg(1600, 1000, 150, 900, 12, 48, C["moss"], 2.5, 0.75, seed=5, r0=40)
    write("generation-maine/assets/img/contours.svg",
          svg(1600, 1000, body, "").replace('role="img" aria-labelledby="t"><title id="t"></title>',
                                            'aria-hidden="true" preserveAspectRatio="xMidYMid slice">'))
    write("brand/social/pattern-contours.svg",
          svg(1600, 1000, body, "Contour pattern", bg=C["spruce"]))


if __name__ == "__main__":
    build_logos()
    build_social()
    build_pattern_tile()
    print("SVGs written")
