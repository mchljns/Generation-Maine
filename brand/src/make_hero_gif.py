"""The placeholder hero for Bark & Sky: four famous Maine settings drawn flat in the concept's palette, each a two second pan,
looping. Katahdin over a lake, Cadillac Mountain in Acadia, the Old Port in Portland, the potato fields of Aroostook County. No
lighthouse, no lobster, per the guardrails. Real footage replaces media/hero.gif one for one.

  python3 brand/src/make_hero_gif.py
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT

W, H = 640, 800          # the frame, 4 by 5
SW = 1280                # each scene is twice as wide as the frame, so the pan has somewhere to go
FPS, SECS = 12, 2.0
OUT = os.path.join(ROOT, "brand", "identity", "splash-bark-sky", "media", "hero.gif")
FONT = os.path.join(ROOT, "brand", "fonts", "alt", "IBMPlexMono-Medium.ttf")

SKY = (185, 201, 211); MIST = (228, 232, 230); PAPER = (244, 243, 238); CLAY = (91, 84, 76); BARK = (38, 32, 28)


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky(d, top, bottom, y0=0, y1=H):
    for y in range(y0, y1):
        d.line([(0, y), (SW, y)], fill=mix(top, bottom, (y - y0) / max(1, y1 - y0)))


def ridge(seed, y_base, amp, n=24, x0=0, x1=SW):
    rnd = random.Random(seed)
    pts = [(x0, H)]
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y_base - amp * (0.5 + 0.5 * math.sin(i * 1.3 + seed)) * rnd.uniform(0.6, 1.0)))
    pts.append((x1, H))
    return pts


def katahdin():
    im = Image.new("RGB", (SW, H), SKY); d = ImageDraw.Draw(im)
    sky(d, mix(SKY, PAPER, 0.35), SKY, 0, 520)
    # far ridge, the massif with the Knife Edge, the near woods, the lake
    d.polygon(ridge(3, 430, 70, n=30), fill=mix(SKY, CLAY, 0.35))
    massif = [(0, H), (120, 470), (330, 400), (470, 300), (560, 262), (640, 250), (700, 262), (760, 290), (860, 310), (900, 340), (1010, 380), (1280, 460), (1280, H)]
    d.polygon(massif, fill=mix(CLAY, SKY, 0.25))
    # the Knife Edge, a thin lighter line along the ridge
    d.line([(470, 300), (560, 262), (640, 250), (700, 262), (760, 290)], fill=mix(PAPER, SKY, 0.3), width=3)
    d.polygon(ridge(7, 560, 60, n=40), fill=mix(BARK, CLAY, 0.35))
    # lake with a reflection band
    d.rectangle((0, 600, SW, H), fill=mix(SKY, CLAY, 0.15))
    for y in range(600, H, 7):
        d.line([(0, y), (SW, y)], fill=mix(mix(SKY, CLAY, 0.15), PAPER, 0.06 if (y // 7) % 2 else 0.0))
    d.polygon(ridge(11, 640, 24, n=50), fill=mix(BARK, CLAY, 0.5))
    return im


def cadillac():
    im = Image.new("RGB", (SW, H), SKY); d = ImageDraw.Draw(im)
    sky(d, mix(SKY, PAPER, 0.45), mix(SKY, PAPER, 0.1), 0, 420)
    # the sea and the Porcupine Islands
    d.rectangle((0, 420, SW, H), fill=mix(SKY, CLAY, 0.22))
    for cx, w, h in ((260, 220, 26), (560, 300, 34), (880, 200, 22), (1150, 260, 30)):
        d.ellipse((cx - w / 2, 420 - h, cx + w / 2, 420 + h * 0.4), fill=mix(BARK, CLAY, 0.45))
        d.rectangle((cx - w / 2, 420, cx + w / 2, 420 + h * 0.4), fill=mix(SKY, CLAY, 0.22))
    # granite domes in the foreground, rounded, with lichen-grey tops
    for cx, w, h, t in ((200, 700, 300, 0.0), (760, 900, 360, 0.08), (1250, 700, 280, 0.04)):
        d.ellipse((cx - w / 2, H - h, cx + w / 2, H + h * 0.6), fill=mix(CLAY, PAPER, 0.35 + t))
    for cx, w, h in ((420, 500, 200), (1050, 600, 230)):
        d.ellipse((cx - w / 2, H - h, cx + w / 2, H + h * 0.6), fill=mix(CLAY, PAPER, 0.2))
    # a few low spruce
    rnd = random.Random(5)
    for _ in range(14):
        x = rnd.uniform(0, SW); y = rnd.uniform(560, 700); s = rnd.uniform(14, 30)
        d.polygon([(x, y - s * 2.2), (x - s * 0.6, y), (x + s * 0.6, y)], fill=mix(BARK, CLAY, 0.3))
    return im


def old_port():
    im = Image.new("RGB", (SW, H), SKY); d = ImageDraw.Draw(im)
    sky(d, mix(SKY, PAPER, 0.3), SKY, 0, 460)
    # brick blocks stepping down a hill toward the water, the Custom House tower among them
    rnd = random.Random(9)
    x = -40
    blocks = []
    while x < SW + 40:
        w = rnd.choice([120, 150, 180, 210]); top = rnd.choice([250, 290, 330, 370])
        blocks.append((x, top, w)); x += w + rnd.choice([0, 0, 14])
    for i, (bx, top, w) in enumerate(blocks):
        col = mix(CLAY, BARK, 0.15 + 0.12 * (i % 3)) if i % 4 else mix(CLAY, PAPER, 0.25)
        d.rectangle((bx, top, bx + w, 620), fill=col)
        # windows as a grid of pale slots
        for wy in range(top + 26, 600, 44):
            for wx in range(bx + 16, bx + w - 16, 30):
                d.rectangle((wx, wy, wx + 12, wy + 22), fill=mix(col, PAPER, 0.45))
    # the tower
    tx = 700
    d.rectangle((tx, 170, tx + 70, 620), fill=mix(CLAY, PAPER, 0.3))
    d.polygon([(tx - 6, 170), (tx + 35, 112), (tx + 76, 170)], fill=mix(CLAY, PAPER, 0.3))
    for wy in range(200, 600, 44):
        d.rectangle((tx + 29, wy, tx + 41, wy + 22), fill=mix(CLAY, PAPER, 0.6))
    # the street, cobbled in two tones, and the harbor at the end of it
    d.rectangle((0, 620, SW, H), fill=mix(CLAY, PAPER, 0.5))
    for y in range(620, H, 10):
        for x in range(0, SW, 20):
            if (x // 20 + y // 10) % 2:
                d.rectangle((x, y, x + 18, y + 8), fill=mix(CLAY, PAPER, 0.42))
    return im


def aroostook():
    im = Image.new("RGB", (SW, H), SKY); d = ImageDraw.Draw(im)
    sky(d, mix(SKY, PAPER, 0.5), SKY, 0, 470)
    # a line of spruce on the horizon, then the fields rolling toward us in rows that converge
    d.polygon(ridge(13, 470, 12, n=80), fill=mix(BARK, CLAY, 0.35))
    d.rectangle((0, 476, SW, H), fill=mix(CLAY, PAPER, 0.45))
    vx = 640
    for i in range(-30, 31):
        x_far = vx + i * 22
        x_near = vx + i * 110
        d.line([(x_far, 476), (x_near, H)], fill=mix(CLAY, PAPER, 0.30 if i % 2 else 0.52), width=6)
    # a barn and a potato house, low and plain
    d.rectangle((880, 420, 1000, 476), fill=mix(BARK, CLAY, 0.2))
    d.polygon([(870, 420), (940, 386), (1010, 420)], fill=mix(BARK, CLAY, 0.1))
    d.rectangle((330, 446, 420, 476), fill=mix(BARK, CLAY, 0.3))
    return im


SCENES = [("katahdin", katahdin), ("cadillac", cadillac), ("old port", old_port), ("aroostook", aroostook)]


def ease(t):
    return 0.5 - 0.5 * math.cos(t * math.pi)


def build():
    frames = []
    n = int(FPS * SECS)
    f = ImageFont.truetype(FONT, 11)
    for k, (name, draw) in enumerate(SCENES):
        scene = draw()
        for i in range(n):
            t = ease(i / (n - 1))
            # alternate the pan direction so the loop does not jump the same way every cut
            x = (SW - W) * (t if k % 2 == 0 else 1 - t)
            fr = scene.crop((round(x), 0, round(x) + W, H))
            d = ImageDraw.Draw(fr, "RGBA")
            tw = d.textlength("PLACEHOLDER", font=f)
            d.rounded_rectangle((W - tw - 26, H - 30, W - 10, H - 10), radius=4, fill=(38, 32, 28, 170))
            d.text((W - tw - 18, H - 25), "PLACEHOLDER", font=f, fill=(244, 243, 238, 235))
            frames.append(fr.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=int(1000 / FPS), loop=0, optimize=True)
    print("hero.gif", len(frames), "frames", os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    build()
