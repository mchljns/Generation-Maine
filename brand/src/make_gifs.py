"""Placeholder creator GIFs: a generated portrait with a slow push in, the story's caption on a flat Pine band, the town
and the Marigold dot, and a small PLACEHOLDER tag so a generated face is never mistaken for a real creator. Silent by nature.

Reads brand/content/creators-placeholder.json and brand/content/portraits/creator-N.jpg (any size; the full-size files from
Canva replace the thumbnails when dropped into the same folder). Writes brand/identity/splash/media/creator-N.gif.

  python3 brand/src/make_gifs.py                    # Signature: Pine band, Marigold dot, DM Sans
  python3 brand/src/make_gifs.py --theme bark-sky   # Bark & Sky: Bark band, no dot, Hedvig Sans, into splash-bark-sky/media
"""
import json
import os
import random
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT

W, H = 324, 576            # 9:16, small enough for a GIF the page can carry
FRAMES, FPS, LOOP_S = 18, 8, 2.25
THEMES = {
    "signature": dict(band=(11, 43, 33), dot=(239, 180, 67), font=os.path.join(ROOT, "generation-maine", "assets", "fonts", "dm-sans-var.ttf"),
                      media=os.path.join(ROOT, "brand", "identity", "splash", "media"), lower=False),
    "bark-sky": dict(band=(38, 32, 28), dot=None, font=os.path.join(ROOT, "brand", "fonts", "d", "HedvigLettersSans-Regular.ttf"),
                     media=os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media"), lower=True),
}
THEME = THEMES["bark-sky" if "--theme" in sys.argv and "bark-sky" in sys.argv else "signature"]
PINE = THEME["band"]
MG = THEME["dot"]
FONT = THEME["font"]
MEDIA = THEME["media"]
PORTRAITS = os.path.join(ROOT, "brand", "content", "portraits")


def font(size, weight=600):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def cover(im, w, h):
    """Scale and crop to fill w by h."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def grain(im, amount=10, seed=0):
    rnd = random.Random(seed)
    noise = Image.effect_noise((im.width, im.height), amount).convert("L")
    noise = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(im, noise, 0.08)


def build_one(i, c):
    src = os.path.join(PORTRAITS, "creator-%d.jpg" % (i + 1))
    if not os.path.exists(src):
        return None
    base = Image.open(src).convert("RGB")
    # a thumbnail-size source is softened on purpose so the upscale reads as film, not as pixels
    small = base.width < 400
    big = cover(base, round(W * 1.14), round(H * 1.14))
    if small:
        big = big.filter(ImageFilter.GaussianBlur(0.9))
        big = ImageEnhance.Contrast(big).enhance(1.08)
    frames = []
    cap_f, k_f, tag_f = font(19, 600), font(10, 600), font(9, 700)
    for n in range(FRAMES):
        t = n / (FRAMES - 1)
        # a slow push in with a drift, eased so the loop point hides
        ease = 0.5 - 0.5 * __import__("math").cos(t * 3.14159 * 2)
        zoom = 1.0 + 0.09 * ease
        fw, fh = round(W * 1.14 / zoom), round(H * 1.14 / zoom)
        cx = (big.width - fw) / 2 + (big.width * 0.03) * (0.5 - ease)
        cy = (big.height - fh) / 2 + (big.height * 0.02) * (ease - 0.5)
        fr = big.crop((round(cx), round(cy), round(cx) + fw, round(cy) + fh)).resize((W, H), Image.LANCZOS)
        d = ImageDraw.Draw(fr, "RGBA")
        # the caption on a flat Pine band, no gradient
        lines = wrap(d, c["caption"], cap_f, W - 40)
        band_h = 20 + len(lines) * 27 + 44
        d.rectangle((0, H - band_h, W, H), fill=PINE + (225,))
        y = H - band_h + 16
        for ln in lines:
            d.text((20, y), ln, font=cap_f, fill=(255, 255, 255))
            y += 27
        town = ("%s, maine" % c["town"].lower()) if THEME["lower"] else ("%s, Maine" % c["town"].upper())
        d.text((20, H - 26), town, font=k_f, fill=(255, 255, 255, 220))
        tw = d.textlength(town, font=k_f)
        if MG:
            d.ellipse((20 + tw + 8, H - 24, 20 + tw + 15, H - 17), fill=MG)
        # the tag: this is a stand-in
        tag = "PLACEHOLDER"
        tl = d.textlength(tag, font=tag_f)
        d.rounded_rectangle((W - tl - 34, H - 33, W - 16, H - 15), radius=4, fill=(255, 255, 255, 40))
        d.text((W - tl - 25, H - 29), tag, font=tag_f, fill=(255, 255, 255, 210))
        frames.append(fr.quantize(colors=72, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    os.makedirs(MEDIA, exist_ok=True)
    out = os.path.join(MEDIA, "creator-%d.gif" % (i + 1))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(1000 / FPS), loop=0, optimize=True)
    return out


def build():
    with open(os.path.join(ROOT, "brand", "content", "creators-placeholder.json")) as fh:
        creators = json.load(fh)["creators"]
    for i, c in enumerate(creators):
        out = build_one(i, c)
        print("gif", i + 1, c["name"], "%dKB" % (os.path.getsize(out) // 1024) if out else "no portrait")


if __name__ == "__main__":
    build()
