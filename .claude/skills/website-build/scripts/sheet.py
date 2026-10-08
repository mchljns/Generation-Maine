#!/usr/bin/env python3
"""Paste screenshots side by side into one contact sheet so the user can compare states or viewports in one image.

    sheet.py out.png a.png b.png c.png [--gap 30] [--height 900]

Images are scaled to a common height when --height is given; otherwise pasted at native size, top-aligned.
"""
import sys
from PIL import Image

def main():
    args = sys.argv[1:]
    gap, height = 30, None
    if '--gap' in args:
        i = args.index('--gap'); gap = int(args[i + 1]); del args[i:i + 2]
    if '--height' in args:
        i = args.index('--height'); height = int(args[i + 1]); del args[i:i + 2]
    out, files = args[0], args[1:]
    ims = [Image.open(f).convert('RGB') for f in files]
    if height:
        ims = [im.resize((round(im.width * height / im.height), height)) for im in ims]
    H = max(im.height for im in ims); W = sum(im.width for im in ims) + gap * (len(ims) - 1)
    sheet = Image.new('RGB', (W, H), '#cccccc'); x = 0
    for im in ims:
        sheet.paste(im, (x, 0)); x += im.width + gap
    sheet.save(out); print(out, sheet.size)

if __name__ == '__main__':
    main()
