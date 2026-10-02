"""Placeholder photography for the Bark & Sky splash. The sources are small generated thumbnails (the only imagery reachable from
this environment), so each is enlarged softly, graded cool, and grained, the way the clip placeholders were, and tagged PLACEHOLDER.
Real licensed photography replaces these files one for one. The shot list is in brand/content/photos/SHOTLIST.md.

  python3 brand/src/make_photos.py   # writes brand/identity/splash-bark-sky/media/photo-*.jpg and portrait-*.jpg
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT

SRC = os.path.join(ROOT, "brand", "content", "photos")
PORTRAITS = os.path.join(ROOT, "brand", "content", "portraits")
OUT = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media")
SKY = (185, 201, 211)
FONT = os.path.join(ROOT, "brand", "fonts", "alt", "IBMPlexMono-Medium.ttf")


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def treat(im, w, h, tag=True):
    im = cover(im.convert("RGB"), w, h)
    im = im.filter(ImageFilter.GaussianBlur(max(0.8, w / 700)))
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(0.9)
    im = Image.blend(im, Image.new("RGB", im.size, SKY), 0.05)
    noise = Image.effect_noise(im.size, 14).convert("L")
    im = Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.06)
    if tag:
        d = ImageDraw.Draw(im, "RGBA")
        f = ImageFont.truetype(FONT, max(10, w // 70))
        t = "PLACEHOLDER"
        tw = d.textlength(t, font=f)
        pad = w // 90
        d.rounded_rectangle((w - tw - pad * 4, h - f.size - pad * 3, w - pad * 2, h - pad), radius=4, fill=(38, 32, 28, 160))
        d.text((w - tw - pad * 3, h - f.size - pad * 2), t, font=f, fill=(244, 243, 238, 230))
    return im


def build():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("tailgate.jpg", "photo-hero.jpg", 880, 1100), ("tailgate.jpg", "photo-hero-wide.jpg", 1200, 800)]
    for src, dst, w, h in jobs:
        treat(Image.open(os.path.join(SRC, src)), w, h).save(os.path.join(OUT, dst), quality=82, optimize=True)
        print(dst, os.path.getsize(os.path.join(OUT, dst)) // 1024, "KB")
    for i in range(1, 10):
        p = os.path.join(PORTRAITS, "creator-%d.jpg" % i)
        if os.path.exists(p):
            treat(Image.open(p), 300, 400, tag=False).save(os.path.join(OUT, "portrait-%d.jpg" % i), quality=80, optimize=True)
    print("portraits written")


if __name__ == "__main__":
    build()
