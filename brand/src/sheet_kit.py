"""Before and after contact sheet for Signature round one (q-) and round two (s-).
Run after render_kit.mjs: python3 brand/src/sheet_kit.py"""
import os
from PIL import Image, ImageDraw
from gmlib import ROOT

M = os.path.join(ROOT, "brand", "kit", "mockups")
IDS = ["first", "lower", "end", "grid", "substack", "collab"]


def tile(name, h):
    im = Image.open(os.path.join(M, name + ".png")).convert("RGB")
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def row(prefix, h=640):
    ts = [tile(prefix + i, h) for i in IDS]
    out = Image.new("RGB", (sum(t.width for t in ts) + 20 * (len(ts) - 1), h), "#E9E5DA")
    x = 0
    for t in ts:
        out.paste(t, (x, 0)); x += t.width + 20
    return out


a, b = row("q-"), row("s-")
wa, wb = tile("q-web", 680), tile("s-web", 680)
W = max(a.width, wa.width + wb.width + 20)
sheet = Image.new("RGB", (W + 80, 40 + a.height + 40 + b.height + 40 + wa.height + 40), "#E9E5DA")
sheet.paste(a, (40, 40)); sheet.paste(b, (40, 80 + a.height))
y = 120 + a.height + b.height
sheet.paste(wa, (40, y)); sheet.paste(wb, (60 + wa.width, y))
sheet.save(os.path.join(ROOT, "brand", "kit", "signature-before-after.png"))
print("sheet", sheet.size)


# Signature round two (s-) against Offset (o-), row by row, with labels.
from PIL import ImageFont

F = ImageFont.truetype(os.path.join(ROOT, "brand", "fonts", "Inter-SemiBold.ttf"), 30)
FS = ImageFont.truetype(os.path.join(ROOT, "brand", "fonts", "Inter-Regular.ttf"), 22)
LABELS = ["Video, first seconds", "Lower third", "End card", "Profile grid", "Substack", "Collab post"]
def compare(b, name_b, out):
    rs, ro = row("s-"), row(b)
    ws, wo = tile("s-web", 560), tile(b + "web", 560)
    gs, go = tile("s-grid", 900), tile(b + "grid", 900)
    L = 220
    W = L + max(rs.width, ws.width + wo.width + 20, gs.width + go.width + 20) + 40
    H = 40 + 40 + rs.height + 30 + ro.height + 70 + ws.height + 70 + gs.height + 40
    cmp = Image.new("RGB", (W, H), "#E9E5DA")
    d = ImageDraw.Draw(cmp)
    x = L
    for lab, t in zip(LABELS, [tile("s-" + i, 640) for i in IDS]):
        d.text((x, 40), lab, font=FS, fill="#5E6A63"); x += t.width + 20
    y = 80
    d.text((40, y + 8), "Signature", font=F, fill="#104836"); cmp.paste(rs, (L, y)); y += rs.height + 30
    d.text((40, y + 8), name_b, font=F, fill="#104836"); cmp.paste(ro, (L, y)); y += ro.height + 70
    d.text((L, y - 34), "Website hero: Signature, then " + name_b, font=FS, fill="#5E6A63")
    cmp.paste(ws, (L, y)); cmp.paste(wo, (L + ws.width + 20, y)); y += ws.height + 70
    d.text((L, y - 34), "Profile grid, larger: Signature, then " + name_b, font=FS, fill="#5E6A63")
    cmp.paste(gs, (L, y)); cmp.paste(go, (L + gs.width + 20, y))
    cmp.save(os.path.join(ROOT, "brand", "kit", out))
    print(out, cmp.size)


compare("o-", "Offset", "signature-vs-offset.png")
compare("d-", "Bark & Sky", "signature-vs-bark-sky.png")
