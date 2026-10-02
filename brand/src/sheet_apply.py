"""Contact sheet of the applied logo. python3 brand/src/sheet_apply.py"""
import os
import sys
from PIL import Image
from gmlib import ROOT

D = sys.argv[1] if len(sys.argv) > 1 else "apply"
M = os.path.join(ROOT, "brand", "identity", D, "mockups")
IDS = ["first", "lower", "end", "grid", "avatar", "substack", "collab"]


def tile(name, h):
    im = Image.open(os.path.join(M, name + ".png")).convert("RGB")
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


ts = [tile("l-" + i, 640) for i in IDS]
w = tile("l-web", 680)
W = max(sum(t.width for t in ts) + 20 * (len(ts) - 1), w.width) + 80
o = Image.new("RGB", (W, 640 + 680 + 120), "#E9E5DA")
x = 40
for t in ts:
    o.paste(t, (x, 40)); x += t.width + 20
o.paste(w, (40, 720))
o.save(os.path.join(ROOT, "brand", "identity", D, "applied-sheet.png"))
print("sheet", o.size)
