"""Builds brand/grades/scorecard.html: every identity side by side with a graded scorecard.

Run from the repo root: python3 brand/src/build_scorecard.py
"""
import base64
import os

from gmlib import ROOT, write
from v2marks import A2, a2_symbol, gm_wordmark

OUT = "brand/grades"

# ---- extra assets for the G-sunrise alternate (it has no lockup of its own after italics were removed)
sym = a2_symbol(0, 0, 112, A2["spruce"], A2["lupine"])
wm, ww = gm_wordmark(146, 84, 100, A2["granite"])
write(OUT + "/assets/g-sunrise-lockup.svg",
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 112" width="%d" height="112">%s%s</svg>' % (146 + ww, 146 + ww, sym, wm))
write(OUT + "/assets/g-sunrise-avatar.svg",
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200"><rect width="200" height="200" fill="%s"/>%s</svg>'
      % (A2["spruce"], a2_symbol(38, 38, 124, A2["fog"], A2["lupine"])))

CRITERIA = [
    ("Idea", 15, "Does the mark carry a story in one look?"),
    ("Distinct", 20, "Clear of 76crew, Green Falls and Baxter Brewing"),
    ("Small size", 15, "Reads as a 32 px avatar and 16 px favicon"),
    ("Premium", 15, "Polish, restraint, craft"),
    ("Fit", 15, "Transparent about Maine Policy; lets creators lead"),
    ("Ease", 10, "A small team can repeat it in Canva and CapCut"),
    ("System", 10, "Devices, motion and creator assets beyond the logo"),
]

IDS = [
    {
        "key": "first-light", "name": "First Light", "tag": "v2 · Direction A", "rec": True,
        "logo": "../v2/first-light/logo/horizontal.svg", "logo_bg": "#FFFFFF",
        "avatar": "../v2/first-light/social/avatar-1080.png", "small": "../v2/first-light/logo/symbol.svg",
        "end": "../v2/first-light/social/end-card-1080x1920.png",
        "scores": [8, 6, 9, 8, 8, 9, 8],
        "plus": ["One shape that reads at 16 px", "Pink is unclaimed by any neighbor", "Horizon rule and motion give it a system"],
        "minus": ["Maine silhouette is also on Baxter cans and is common in general", "Sun-in-a-disc still nods to Baxter's sun, even in pink"],
        "path": "Redraw the outline by hand as a simplified, geometric Maine the brand owns, instead of map data. That lifts Distinct to 8 and the grade to A-.",
    },
    {
        "key": "g-sunrise", "name": "G-Sunrise", "tag": "v2 · First Light alternate", "rec": False,
        "logo": "assets/g-sunrise-lockup.svg", "logo_bg": "#FFFFFF",
        "avatar": "assets/g-sunrise-avatar.svg", "small": "../v2/first-light/logo/alt-g-sunrise.svg",
        "end": None,
        "scores": [7, 7, 8, 7, 8, 8, 7],
        "plus": ["No state outline, so no Baxter overlap there", "Geometric and easy to reproduce"],
        "minus": ["Letter-plus-dot marks are common (a G with a dot recalls big tech)", "The sun on a horizon still echoes Baxter's sun, more faintly"],
        "path": "Make the G unmistakably custom (a unique terminal or cut) so it cannot be mistaken for a generic G.",
    },
    {
        "key": "postmark", "name": "Postmark", "tag": "v2 · Direction B", "rec": False,
        "logo": "../v2/postmark/logo/lockup.svg", "logo_bg": "#ECECE6",
        "avatar": "../v2/postmark/social/avatar-1080.png", "small": "../v2/postmark/logo/small.svg",
        "end": "../v2/postmark/social/end-card-1080x1920.png",
        "scores": [8, 5, 7, 6, 7, 7, 9],
        "plus": ["Best creator system: a stamp per town", "ME reads as Maine and as first person", "Blueberry violet is unclaimed"],
        "minus": ["Round badge with ring text reads craft brewery", "Anton looks like Baxter's Knockout; yellow near Baxter's Pale Ale can", "Also uses the Maine silhouette"],
        "path": "Swap Anton for a wide or rounded face, drop the yellow for a second ink color, and keep the badge flat and minimal.",
    },
    {
        "key": "spruce-lupine", "name": "Spruce & Lupine", "tag": "v1 · Direction A (live site)", "rec": False,
        "logo": "../logo/primary.svg", "logo_bg": "#FFFFFF",
        "avatar": "../social/avatar-1080.png", "small": "../logo/icon.svg",
        "end": "../social/end-card-1080x1920.png",
        "scores": [5, 7, 7, 5, 8, 9, 6],
        "plus": ["Calm and credible", "Simplest to use", "Already built into the site"],
        "minus": ["A styled font, not a brandmark", "Bricolage Grotesque is a popular trend face", "Contour lines are a common stock motif"],
        "path": "Superseded by First Light, which keeps its colors and adds a real mark.",
    },
    {
        "key": "paper-route", "name": "Paper Route", "tag": "v1 · Direction B", "rec": False,
        "logo": "assets/paper-route-logo.png", "logo_bg": "#ECECE6",
        "avatar": "assets/paper-route-avatar.png", "small": "assets/paper-route-avatar.png",
        "end": "assets/paper-route-endcard.png",
        "scores": [5, 5, 5, 4, 4, 7, 5],
        "plus": ["Energetic and youthful", "Easy to imitate in Canva"],
        "minus": ["Zine styling is common and dates fast", "Can read as a costume next to a think tank", "Condensed caps and yellow echo Baxter cans"],
        "path": "Superseded by Postmark, which keeps the handmade spirit with more structure.",
    },
]

LETTERS = [(8.5, "A"), (8.0, "A-"), (7.5, "B+"), (7.0, "B"), (6.5, "B-"), (6.0, "C+"), (5.5, "C"), (5.0, "C-"), (0, "D")]


def overall(scores):
    return sum(s * w for s, (_, w, _) in zip(scores, CRITERIA)) / 100.0


def letter(v):
    for cut, l in LETTERS:
        if v >= cut:
            return l
    return "D"


def b64(path):
    p = os.path.join(ROOT, OUT, path)
    ext = "svg+xml" if p.endswith(".svg") else "png"
    with open(p, "rb") as fh:
        return "data:image/%s;base64,%s" % (ext, base64.b64encode(fh.read()).decode())


def font64(name):
    with open(os.path.join(ROOT, "brand/v2/fonts-web", name), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def build():
    ids = sorted(IDS, key=lambda d: -overall(d["scores"]))
    cols = ""
    for d in ids:
        ov = overall(d["scores"])
        bars = "".join(
            '<div class="row"><span>%s</span><i><b style="width:%d%%"></b></i><em>%d</em></div>' % (c[0], s * 10, s)
            for s, c in zip(d["scores"], CRITERIA))
        end = ('<img class="end" src="%s" alt="%s end card">' % (b64(d["end"]), d["name"])) if d["end"] else \
            '<div class="end none">Uses the First Light end card with this mark</div>'
        cols += """
<article class="col%s">
  <header><span class="tag">%s</span><h2>%s</h2>
    <div class="grade"><strong>%s</strong><span>%.1f / 10</span></div>%s</header>
  <div class="logo" style="background:%s"><img src="%s" alt="%s logo"></div>
  <div class="sizes"><img class="av" src="%s" alt=""><img src="%s" width="32" height="32" alt=""><img src="%s" width="16" height="16" alt=""></div>
  %s
  <div class="bars">%s</div>
  <ul class="plus">%s</ul>
  <ul class="minus">%s</ul>
  <p class="path"><b>Path up:</b> %s</p>
</article>""" % (
            " rec" if d["rec"] else "", d["tag"], d["name"], letter(ov), ov,
            '<span class="pill">Recommended</span>' if d["rec"] else "",
            d["logo_bg"], b64(d["logo"]), d["name"], b64(d["avatar"]), b64(d["small"]), b64(d["small"]),
            end, bars,
            "".join("<li>%s</li>" % x for x in d["plus"]), "".join("<li>%s</li>" % x for x in d["minus"]), d["path"])

    crit = "".join("<li><b>%s</b> %d%%<span>%s</span></li>" % c for c in CRITERIA)
    html = TEMPLATE.replace("{{COLS}}", cols).replace("{{CRIT}}", crit).replace("{{F}}", font64("instrument-sans.woff2"))
    write(OUT + "/scorecard.html", html)
    for d in ids:
        print("%-16s %.2f %s" % (d["name"], overall(d["scores"]), letter(overall(d["scores"]))))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine brand scorecard</title>
<style>
@font-face{font-family:IS;src:url(data:font/woff2;base64,{{F}}) format("woff2");font-weight:400 700}
*{box-sizing:border-box}
body{margin:0;background:#F4F5F7;color:#121417;font:14px/1.45 IS,system-ui,sans-serif}
.top{padding:36px 32px 12px;max-width:1900px;margin:0 auto}
h1{font:700 40px/1 IS;letter-spacing:-.02em;margin:0 0 10px}
.top p{margin:0;max-width:90ch;color:#4A515C}
.crit{display:flex;flex-wrap:wrap;gap:8px 20px;list-style:none;padding:0;margin:16px 0 0;font-size:12px}
.crit span{color:#6B7380;margin-left:6px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(260px,1fr));gap:16px;padding:20px 32px 40px;max-width:1900px;margin:0 auto;overflow-x:auto}
.col{background:#fff;border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:14px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.col.rec{outline:3px solid #F0509A;outline-offset:-3px}
header .tag{font:600 11px/1 IS;letter-spacing:.12em;text-transform:uppercase;color:#6B7380}
header h2{font:700 24px/1.1 IS;margin:6px 0 8px;letter-spacing:-.01em}
.grade{display:flex;align-items:baseline;gap:10px}
.grade strong{font:700 44px/1 IS;letter-spacing:-.02em}
.grade span{color:#6B7380;font-weight:600}
.pill{display:inline-block;margin-top:8px;background:#F0509A;color:#121417;font:700 10px/1 IS;letter-spacing:.12em;text-transform:uppercase;padding:6px 9px;border-radius:99px}
.logo{border-radius:12px;height:120px;display:grid;place-items:center;padding:16px;border:1px solid #E6E8EC}
.logo img{max-width:100%;max-height:88px}
.sizes{display:flex;align-items:flex-end;gap:14px}
.sizes .av{width:96px;height:96px;border-radius:50%;object-fit:cover}
.sizes img:not(.av){border-radius:50%}
.end{width:100%;max-width:170px;aspect-ratio:9/16;object-fit:cover;border-radius:10px;align-self:center;box-shadow:0 8px 24px -12px rgba(0,0,0,.4)}
.end.none{display:grid;place-items:center;text-align:center;background:#F4F5F7;color:#6B7380;font-size:12px;padding:12px;box-shadow:none;border:1px dashed #C9CED6}
.bars .row{display:grid;grid-template-columns:78px 1fr 18px;align-items:center;gap:8px;font-size:12px;margin:3px 0}
.bars i{display:block;height:8px;background:#EEF0F3;border-radius:99px;overflow:hidden}
.bars b{display:block;height:100%;background:#0B4A34;border-radius:99px}
.bars em{font-style:normal;font-weight:700;text-align:right}
ul{margin:0;padding-left:18px;font-size:12.5px}
.plus li::marker{content:"+  ";color:#0B4A34;font-weight:700}
.minus li::marker{content:"-  ";color:#AD1F62;font-weight:700}
.path{margin:auto 0 0;font-size:12.5px;background:#F4F5F7;border-radius:10px;padding:10px 12px}
</style></head><body>
<section class="top">
  <h1>Brand scorecard</h1>
  <p>All five Generation Maine identities, graded on the same criteria after the Green Falls, Baxter Brewing and no-italics changes. Scores are 1 to 10; the grade is the weighted average (A 8.5+, A- 8.0, B+ 7.5, B 7.0, B- 6.5, C+ 6.0, C 5.5, C- 5.0, D below). Sorted best first. Scores are a design judgment, not a survey.</p>
  <ul class="crit">{{CRIT}}</ul>
</section>
<main class="grid">{{COLS}}</main>
</body></html>
"""

if __name__ == "__main__":
    build()
