"""The yellow question on one sheet: each placement on the lockup at 96 and 44 px, reversed, and the
avatar on a light field, then the end card for A and B.

  python3 brand/src/sheet_gold.py   # writes brand/identity/gold/yellow-options.html and .png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_kit as K
from build_apply import mural, logo
from gmlib import ROOT, write

R = os.path.join(ROOT, "brand", "identity", "gold")
NAMES = {
    "A": "A. The stripe: the widest line is Marigold. Current.",
    "B": "B. The dot: the state is one color. Marigold is the dot on the i, as in every headline.",
    "C": "C. The thread: the widest line runs out of the state and reaches the name.",
    "D": "D. The baseline: no gold in the state. A Marigold rule under the name is the line the state stands on.",
}


def inl(k):
    with open(os.path.join(R, k + ".svg")) as fh:
        return fh.read().replace('role="img"', "")


def box(k, h, bg="#fff"):
    return '<div class="t" style="background:%s">%s</div>' % (bg, inl(k).replace("<svg ", '<svg style="height:%dpx;width:auto" ' % h, 1))


def endcard(variant):
    gold_line = variant == "A"
    mur = mural(300, "#F4F0E6", "#EFB443" if gold_line else "#F4F0E6", n=48)
    head = '<p class="ttl xl">Follow along.</p>' if gold_line else K.ttl("Follow along", "xl")
    lk = logo("lockup-horizontal-reversed", "lk") if gold_line else inl("lockup-B-reversed").replace("<svg ", '<svg class="lk" ', 1)
    return ('<div class="ab ph9" style="width:360px;height:640px"><div class="lend">%s<div class="lmur">%s</div><div class="lbot">%s'
            '<ul class="hl s"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li><li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul>'
            '<p class="disc">%s</p></div></div></div>') % (lk, mur, head, K.MPI)


def build():
    rows = ""
    for v in "ABCD":
        rows += '<div class="row"><p class="lab">%s</p><div class="g">%s%s%s%s</div></div>' % (
            NAMES[v], box("lockup-" + v, 96), box("lockup-" + v, 44), box("lockup-%s-reversed" % v, 96, "#104836"), box("avatar-light-" + v, 110, "#F2EFE8"))
    with open(os.path.join(ROOT, "brand", "identity", "apply", "apply.html")) as fh:
        css = fh.read().split("<style>")[1].split("</style>")[0]
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Generation Maine, where the yellow goes</title><style>%s\n'
            'body{background:#E9E5DA;padding:28px}\n'
            '.row{margin-bottom:22px}.lab{margin:0 0 8px;font:600 14px Inter;color:#1E2621}\n'
            '.g{display:flex;gap:14px;align-items:center;flex-wrap:wrap}\n'
            '.t{background:#fff;border-radius:8px;padding:16px 22px;display:flex;align-items:center}.t svg{display:block}\n'
            '.ends{display:flex;gap:24px;align-items:flex-start;margin-top:10px}.ends .ab{border-radius:14px}\n'
            '.lend .lk{width:150px}\n</style></head><body>%s'
            '<p class="lab" style="margin-top:30px">End card, A and B. In A the widest line is the frame\'s Marigold and the headline ends in a plain period. In B the mural is Birch and the headline gets its dot back.</p>'
            '<div class="ends">%s%s</div></body></html>') % (css, rows, endcard("A"), endcard("B"))
    write("brand/identity/gold/yellow-options.html", page)
    shot = os.path.join(ROOT, "brand", "src", "shot.mjs")
    if os.path.exists(shot):
        subprocess.run(["node", shot, os.path.join(R, "yellow-options.html"), os.path.join(R, "yellow-options.png")], check=True)


if __name__ == "__main__":
    build()
    print("yellow-options written")
