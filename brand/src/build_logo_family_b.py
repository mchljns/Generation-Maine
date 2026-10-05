"""Family B's logo set: the stacked lowercase wordmark inside an open frame, the way Maine Civic Action frames its name.
Frame and second word in the accent. On dark fields the name is Paper and the accent marigold; on light fields the name is
navy and the accent blue.

  python3 brand/src/build_logo_family_b.py   # writes brand/identity/logo-maine/family-b/*.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_family_marks import b_framed, b_two_tone, b_bar

OUT = os.path.join(ROOT, "brand", "identity", "logo-maine", "family-b")
NAVY, BLUE, MG, PAPER = "#112337", "#006CB5", "#EFB443", "#F4F3EE"

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    files = {}
    for suf, fg, acc in (("", NAVY, BLUE), ("-reversed", PAPER, MG), ("-black", "#000000", "#000000"), ("-white", "#FFFFFF", "#FFFFFF")):
        files["lockup-framed" + suf] = b_framed(fg, acc)
        files["lockup-compact" + suf] = b_framed(fg, acc, pad=30, stroke=8)
        files["lockup-two-line" + suf] = b_framed(fg, acc)
        files["wordmark-two-tone" + suf] = b_two_tone(fg, acc)
        files["lockup-bar" + suf] = b_bar(fg, acc)
    for k, v in files.items():
        write(os.path.join(OUT, k + ".svg"), v)
    print("wrote", len(files), "files")
