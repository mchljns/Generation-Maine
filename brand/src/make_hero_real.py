"""The hero media for Bark & Sky from licensed photographs: five Maine settings, a slow two second move across each, looping.
Writes the graded scene plates the video recorder uses, the poster, and the credits. Sources and licenses are in
brand/content/photos/CREDITS.md and the page's footer. Sources are 3840 px wide or wider, for a 1920 by 1080 hero.

  python3 brand/src/make_hero_real.py && node brand/src/make_hero_video.mjs
"""
import json
import os
import re
import sys

from PIL import Image, ImageEnhance

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT

MEDIA = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media")
SRC = os.path.join(ROOT, "brand", "content", "photos", "commons")
PLATES = os.path.join(ROOT, "brand", "content", "photos", "hero-frames")
# setting, candidate key, index, where to anchor the vertical crop (0 top, 1 bottom)
PICKS = [("Mount Katahdin from Abol Bridge", "katahdin", 1, 0.45),
         ("potato farms in Aroostook County, 1940", "aroostook", 5, 0.5),
         ("sunrise from Cadillac Mountain, Acadia", "cadillac2", 4, 0.5),
         ("Portland Head Light, Cape Elizabeth", "headlight", 6, 0.5),
         ("the Old Port waterfront, Portland", "oldport", 2, 0.5)]
W, H = 1920, 1080
ROOM = 1.12  # the plate is 12 percent larger than the frame so the move has somewhere to go
SKY = (185, 201, 211)
MIN_SRC_W = 3000


def grade(im):
    im = ImageEnhance.Color(im).enhance(0.84)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return Image.blend(im, Image.new("RGB", im.size, SKY), 0.06)


def plate(key, n, anchor):
    im = Image.open(os.path.join(SRC, "%s-%d.jpg" % (key, n))).convert("RGB")
    assert im.width >= MIN_SRC_W, "%s-%d is %d px wide; the hero needs %d" % (key, n, im.width, MIN_SRC_W)
    pw, ph = round(W * ROOM), round(H * ROOM)
    s = max(pw / im.width, ph / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - pw) // 2
    y = round((im.height - ph) * anchor)
    return grade(im.crop((x, y, x + pw, y + ph)))


def build():
    os.makedirs(MEDIA, exist_ok=True)
    os.makedirs(PLATES, exist_ok=True)
    cands = json.load(open(os.path.join(SRC, "candidates.json")))
    credits = []
    for k, (desc, key, idx, anchor) in enumerate(PICKS):
        it = cands[key][idx - 1]
        credits.append(dict(setting=desc, author=re.sub("<[^>]+>", "", it["artist"]).strip(), license=it["license"], title=it["title"], page=it["page"], source_px="%dx%d" % (it["w"], it["h"])))
        pl = plate(key, idx, anchor)
        pl.save(os.path.join(PLATES, "scene-%d.jpg" % (k + 1)), quality=92)
        if k == 0:
            x, y = (pl.width - W) // 2, (pl.height - H) // 2
            pl.crop((x, y, x + W, y + H)).save(os.path.join(MEDIA, "hero-poster.jpg"), quality=82, optimize=True, progressive=True)
        print("scene", k + 1, desc, pl.size, credits[-1]["author"], credits[-1]["license"])
    with open(os.path.join(ROOT, "brand", "content", "photos", "CREDITS.md"), "w") as fh:
        fh.write("# Photography credits\n\nThe hero loop uses these photographs from Wikimedia Commons. CC BY and CC BY-SA require the credit below wherever the loop appears, and CC BY-SA requires the same license on any adaptation of the images themselves. The page carries the credit line in its footer. Sources are listed with their pixel size; all are 3840 px wide or wider as fetched.\n\nPortland Head Light is a client-directed exception to the direction's rule against lighthouse imagery (05-identity-system.md).\n\n")
        for c in credits:
            fh.write("- %s: %s, %s, %s. %s\n" % (c["setting"], c["author"] or "[CONFIRM: author]", c["license"], c["source_px"], c["page"]))
    json.dump(credits, open(os.path.join(MEDIA, "credits.json"), "w"), indent=1)


if __name__ == "__main__":
    build()
