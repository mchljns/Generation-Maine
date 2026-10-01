"""The lockup variations under the October 1 rule, on one sheet: each in color on Birch and reversed on
Spruce, then the set at working sizes.

  python3 brand/src/build_logo_maine.py && python3 brand/src/sheet_lockups.py
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write

R = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")
ROWS = [
    ("lockup-horizontal", "1. Horizontal. The primary lockup. The state stands taller than the capitals", 150, "A-"),
    ("lockup-horizontal-right", "2. Horizontal, state after the name. The dot and the state sit near each other", 150, "B"),
    ("lockup-compact", "3. Compact. The mid cut inside the cap height, for bylines, bars and footers", 150, "B+"),
    ("lockup-two-line", "4. Two-line. The state beside the name on two lines, as tall as both", 190, "A-"),
    ("lockup-stacked", "5. Stacked left. The state over the two-line name, for narrow spaces", 230, "B+"),
    ("lockup-stacked-centered", "6. Stacked centered. The state over the one-line name, for title cards and print", 230, "B+"),
    ("lockup-endorsed", "7. Endorsed. The horizontal lockup with the disclosure line", 180, "A-"),
    ("lockup-endorsed-stacked", "8. Endorsed, stacked. For the end card and the back of print", 260, "B+"),
    ("wordmark", "9. The wordmark alone", 120, "A-"),
]


def inl(k, cls=""):
    with open(os.path.join(R, k + ".svg")) as fh:
        return fh.read().replace('role="img"', "").replace("<svg ", '<svg class="%s" ' % cls, 1)


def build():
    rows = ""
    for k, lab, h, grade in ROWS:
        rows += ('<div class="row"><p class="lab">%s <b>%s</b></p><div class="g">'
                 '<div class="t bi" style="height:%dpx">%s</div><div class="t sp" style="height:%dpx">%s</div></div></div>'
                 % (lab, grade, h + 60, inl(k), h + 60, inl(k + "-reversed")))
    sizes = ('<div class="row"><p class="lab">At working sizes. Horizontal at 120 px wide, the smallest allowed. Compact at 100 px. Mid cut lockup at 160 px. Marks at 110, 40 and 16 px.</p>'
             '<div class="g wrap"><div class="t w">%s</div><div class="t w">%s</div><div class="t w">%s</div><div class="t w">%s%s%s</div><div class="t w" style="background:#104836">%s%s%s</div></div></div>') % (
        inl("lockup-horizontal").replace("<svg ", '<svg style="width:120px;height:auto" ', 1),
        inl("lockup-compact").replace("<svg ", '<svg style="width:100px;height:auto" ', 1),
        inl("lockup-horizontal-small").replace("<svg ", '<svg style="width:160px;height:auto" ', 1),
        inl("avatar-full").replace("<svg ", '<svg style="width:110px;height:110px;border-radius:50%" ', 1),
        inl("avatar-mid").replace("<svg ", '<svg style="width:40px;height:40px;border-radius:50%" ', 1),
        inl("favicon").replace("<svg ", '<svg style="width:16px;height:16px" ', 1),
        inl("mark-full-reversed").replace("<svg ", '<svg style="height:110px;width:auto" ', 1),
        inl("mark-mid-reversed").replace("<svg ", '<svg style="height:40px;width:auto" ', 1),
        inl("mark-solid-reversed").replace("<svg ", '<svg style="height:16px;width:auto" ', 1))
    with open(os.path.join(ROOT, "brand", "identity", "apply", "apply.html")) as fh:
        css = fh.read().split("<style>")[1].split("</style>")[0]
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Generation Maine, the lockups</title><style>%s\n'
            'body{background:#E9E5DA;padding:28px}\n'
            '.row{margin-bottom:26px}.lab{margin:0 0 8px;font:600 14px Inter;color:#1E2621}.lab b{color:#104836;margin-left:8px}\n'
            '.g{display:flex;gap:16px;align-items:stretch}.g.wrap{flex-wrap:wrap;align-items:center}\n'
            '.t{border-radius:10px;padding:30px 40px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;flex:1}.t svg{display:block;max-height:100%%;width:auto;max-width:100%%}\n'
            '.t.bi{background:#F4F0E6}.t.sp{background:#104836}.t.w{background:#fff;flex:0 0 auto;padding:22px 28px;gap:22px}\n'
            '</style></head><body><h1 style="font:800 30px/1 Bric;letter-spacing:-.02em;margin:0 0 6px">The lockups</h1>'
            '<p style="font:14px/1.4 Inter;color:#5E6A63;margin:0 0 24px;max-width:760px">The state is one color. Marigold is the dot on the i, once per frame. Each row shows color on Birch and reversed on Spruce.</p>%s%s</body></html>') % (css, rows, sizes)
    write("brand/identity/logo-maine/lockups.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), os.path.join(ROOT, "brand", "identity", "logo-maine", "lockups.html"), os.path.join(ROOT, "brand", "identity", "logo-maine", "lockups.png"), "1500"], check=True)


if __name__ == "__main__":
    build()
    print("lockups written")
