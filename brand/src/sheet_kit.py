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
