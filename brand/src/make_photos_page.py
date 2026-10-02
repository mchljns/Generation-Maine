"""The smaller photograph slots on the Bark & Sky page, cut from the Commons sources with the same filmic grade as the hero.
  python3 brand/src/make_photos_page.py
"""
import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT
from make_hero_real import grade, SRC, MEDIA

# slot, source, output size, vertical anchor
SLOTS = [("about.jpg", "belfast-2", (1600, 1067), 0.5),      # Belfast downtown from above, under the about heading
         ("band.jpg", "lewiston-5", (2400, 1000), 0.45),     # Lewiston, the mills and downtown, the wide band before the quotes
         ("post-1.jpg", "belfast-3", (720, 480), 0.5),       # the posts carry their towns: Belfast, Machias, Lewiston
         ("post-2.jpg", "machias-3", (720, 480), 0.5),
         ("post-3.jpg", "lewiston-3", (720, 480), 0.5)]


def cover(im, size, anchor):
    w, h = size
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = round((im.height - h) * anchor)
    return im.crop((x, y, x + w, y + h))


def build():
    cands = json.load(open(os.path.join(SRC, "candidates.json")))
    used = []
    for out, src, size, anchor in SLOTS:
        key, n = src.rsplit("-", 1)
        it = cands[key][int(n) - 1]
        im = Image.open(os.path.join(SRC, src + ".jpg")).convert("RGB")
        grade(cover(im, size, anchor)).save(os.path.join(MEDIA, out), quality=84, optimize=True, progressive=True)
        used.append((out, re.sub("<[^>]+>", "", it["artist"]).strip(), it["license"], it["title"], it["page"], "%dx%d" % (it["w"], it["h"])))
        print(out, size, used[-1][1], used[-1][2])
    with open(os.path.join(ROOT, "brand", "content", "photos", "CREDITS.md"), "a") as fh:
        fh.write("\n## The smaller slots\n\n")
        for out, author, lic, title, page, px in used:
            fh.write("- %s: %s, %s, %s. %s\n" % (out, author or "[CONFIRM: author]", lic, px, page))


if __name__ == "__main__":
    build()
