"""Bark & Sky for a Gen Z, masculine-leaning audience, still understated. Three treatments on the same four surfaces.

The brief: appeal to Gen Z, skew masculine, keep the quiet. The cues that do that without shouting: a cooler, duller sky (steel, not
baby blue), paper that is bone rather than white, a grid that sits left, labels and numbers set in a monospace like gear tags and
camera overlays, index numbers and timestamps as a design element, the horizon mark as the badge. What is not used: heavy weights,
black, neon, distressed textures, camo, anything that looks like a sneaker drop.

  python3 brand/src/build_field_barksky.py   # writes brand/identity/marks-bark-sky/field/field.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
from build_v4 import svg, f
import build_kit as K
import build_explore2_barksky as E

OUT = "brand/identity/marks-bark-sky/field"

TREATMENTS = [
    dict(key="a", name="A. Slate", sub="the palette shift alone", sky="#B9C9D3", ground="#26201C", paper="#F4F3EE", mist="#E4E8E6", clay="#5B544C", link="#2B4760",
         display="HS", label="HSans", mono=False, align="left",
         note="Sky goes to steel, Paper to bone, Bark to peat. The serif and the lowercase stay. Already less soft; the pastel was most of the problem."),
    dict(key="b", name="B. Field notes", sub="slate, plus a monospace for every label", sky="#B9C9D3", ground="#26201C", paper="#F4F3EE", mist="#E4E8E6", clay="#5B544C", link="#2B4760",
         display="HS", label="Mono", mono=True, align="left",
         note="The serif keeps the names and headlines human. IBM Plex Mono takes the kickers, the counters, the towns and the timestamps, like a gear tag or a camera overlay. Index numbers become a design element. The horizon mark is the badge."),
    dict(key="c", name="C. Utility", sub="the serif goes, a grotesk comes in", sky="#B9C9D3", ground="#26201C", paper="#F4F3EE", mist="#E4E8E6", clay="#5B544C", link="#2B4760",
         display="Sans", label="Mono", mono=True, align="left",
         note="Instrument Sans at medium for headlines and names, Plex Mono for labels. The most Gen Z and the most masculine, and the least this identity. It is a different concept wearing the horizon."),
]


def fonts():
    return ("@font-face{font-family:HS;src:url(data:font/ttf;base64,%s) format('truetype')}"
            "@font-face{font-family:HSans;src:url(data:font/ttf;base64,%s) format('truetype')}"
            "@font-face{font-family:Mono;src:url(data:font/ttf;base64,%s) format('truetype')}"
            "@font-face{font-family:Sans;src:url(data:font/ttf;base64,%s) format('truetype');font-weight:500}"
            % (K.font64("brand/fonts/d/HedvigLettersSerif-24.ttf"), K.font64("brand/fonts/d/HedvigLettersSans-Regular.ttf"),
               K.font64("brand/fonts/alt/IBMPlexMono-Medium.ttf"), K.font64("brand/fonts/v2/InstrumentSans-Medium.ttf")))


def mark(t, size=240):
    return E.rising(t["sky"], t["ground"], t["paper"], y_frac=0.64, h=190, base=0.7, through=True, size=size)


def row(t):
    sky, gr, pa, mi, cl, lk = t["sky"], t["ground"], t["paper"], t["mist"], t["clay"], t["link"]
    disp = "font-family:%s" % t["display"]
    lab = "font-family:%s;%s" % (t["label"], "text-transform:uppercase;letter-spacing:.06em;font-size:11px" if t["mono"] else "letter-spacing:.08em;font-size:12px")
    mk = '<svg viewBox="0 0 240 240" style="width:%dpx;height:%dpx;display:block">%s</svg>'
    # the hero, left grid, index line
    hero = ('<div class="hero" style="background:%s;color:%s">'
            '<div class="bar"><span class="lk">%s<b style="%s">generation maine</b></span><span class="meta" style="%s">about · creators · follow</span></div>'
            '<div class="hb"><p class="idx" style="%s">nine towns · 2026</p><p class="h1" style="%s">young mainers on building a life here</p>'
            '<p class="lede">Young Mainers film the rules that shape their lives. What rent costs, what a license costs, what it takes to stay.</p>'
            '<p><span class="btn" style="background:%s;color:%s">watch the stories</span><span class="tl" style="border-color:%s">get the newsletter</span></p></div></div>'
            % (sky, gr, mk % (22, 22, mark(t)), disp, lab, lab, disp, gr, pa, gr))
    # a creator panel on bone paper, with the index and the town as a tag
    panel = ('<div class="panel" style="background:%s;color:%s"><p class="tag" style="%s;color:%s">04 / 09 &nbsp; machias, maine &nbsp; 0:58</p>'
             '<p class="nm" style="%s">cole</p><p class="bio">Forty minutes each way to a job that pays the rent, barely. I mount the phone on the dash and talk through the math while I drive.</p>'
             '<p class="soc" style="%s;color:%s">instagram &nbsp; tiktok &nbsp; youtube</p></div>' % (pa, gr, lab, cl, disp, lab, lk))
    # a cover on ground, 3:4, the way it would sit in a grid
    cover = ('<div class="cover" style="background:%s;color:%s"><p class="ctag" style="%s;color:%s">ep 04 · machias</p><p class="ct" style="%s">the commute</p>'
             '<p class="cby" style="%s;color:%s">cole · 0:58</p></div>' % (gr, sky, lab, sky, disp, lab, sky))
    # the end card, 9:16, on ground with the horizon field running edge to edge
    end = ('<div class="end" style="background:%s;color:%s"><div class="field" style="background:%s;border-bottom:3px solid %s"><svg viewBox="0 0 240 150" style="width:100%%;height:100%%;display:block">%s</svg></div>'
           '<div class="eb" style="background:%s"><p class="et" style="%s">follow along</p><p class="el" style="%s">instagram &nbsp;&nbsp;@handle<br>tiktok &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@handle<br>youtube &nbsp;&nbsp;&nbsp;@handle<br>substack &nbsp;&nbsp;[name].substack.com</p>'
           '<p class="ed">An initiative of Maine Policy Institute</p></div></div>'
           % (gr, sky, sky, pa, E.rising(sky, gr, pa, y_frac=0.985, h=150, base=0.9, through=False, container="none", size=240).replace('height="3"', 'height="0"'), gr, disp, lab))
    avs = ('<div class="avs"><div style="display:flex;gap:14px;align-items:center">%s%s%s</div><div class="sw">%s</div></div>'
           % (mk % (96, 96, mark(t)), mk % (40, 40, mark(t)), mk % (16, 16, mark(t)),
              "".join('<i style="background:%s"></i>' % c for c in (sky, gr, pa, mi, cl, lk))))
    return ('<div class="row"><div class="lab"><b style="font-family:HS">%s</b><span>%s</span><p>%s</p></div>%s%s%s%s%s</div>'
            % (t["name"], t["sub"], t["note"], hero, panel, cover, end, avs))


def build():
    rows = "".join(row(t) for t in TREATMENTS)
    page = ('<!doctype html><html><head><meta charset="utf-8"><title>Bark &amp; Sky, field</title><style>%s'
            'body{margin:0;background:#E9E5DA;padding:36px;font-family:HSans,sans-serif;color:#26201C}h1{font:400 30px HS;margin:0 0 6px}.intro{font:14px/1.45 HSans;color:#5B544C;max-width:900px;margin:0 0 26px}'
            '.row{display:grid;grid-template-columns:260px 520px 250px 190px 200px 1fr;gap:16px;align-items:stretch;margin-bottom:22px}'
            '.lab b{display:block;font-size:19px}.lab span{display:block;font:12px HSans;color:#5B544C;margin:2px 0 8px}.lab p{margin:0;font:12.5px/1.45 HSans;color:#5B544C}'
            '.hero{border-radius:10px;padding:18px 22px 22px;display:flex;flex-direction:column;justify-content:space-between;min-height:340px}'
            '.bar{display:flex;justify-content:space-between;align-items:center}.lk{display:flex;gap:8px;align-items:center}.lk b{font-weight:400;font-size:16px}.meta{opacity:.85}'
            '.hb{max-width:380px}.idx{margin:0 0 10px;opacity:.75}.h1{font-size:40px;line-height:1.0;letter-spacing:-.02em;margin:0 0 12px;font-weight:500}.lede{font:13px/1.45 HSans;margin:0 0 16px;max-width:40ch}'
            '.btn{display:inline-block;padding:10px 16px;border-radius:999px;font:13px HSans;margin-right:14px}.tl{font:13px HSans;border-bottom:1.5px solid;padding-bottom:1px}'
            '.panel{border-radius:10px;padding:20px}.tag{margin:0 0 14px}.nm{font-size:44px;line-height:1;margin:0 0 12px;font-weight:500}.bio{font:14px/1.45 HSans;margin:0 0 16px}.soc{margin:0}'
            '.cover{border-radius:10px;padding:16px;aspect-ratio:3/4;display:flex;flex-direction:column}.ctag{margin:0}.ct{font-size:28px;line-height:1.02;margin:auto 0 0;font-weight:500}.cby{margin:10px 0 0}'
            '.end{border-radius:10px;overflow:hidden;aspect-ratio:9/16;display:flex;flex-direction:column}.field{height:38%%}.eb{flex:1;padding:16px 14px;display:flex;flex-direction:column}.et{font-size:26px;margin:0 0 12px;font-weight:500}.el{margin:0;line-height:1.7}.ed{margin:auto 0 0;font:10px HSans;opacity:.8}'
            '.avs{border-radius:10px;background:#fff;padding:18px;display:flex;flex-direction:column;justify-content:space-between}.avs svg{border-radius:50%%}.sw{display:flex;gap:6px}.sw i{display:block;width:22px;height:22px;border-radius:50%%;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}'
            '</style></head><body><h1>Bark &amp; Sky, for a Gen Z audience that leans masculine</h1>'
            '<p class="intro">Same concept, same mark, same quiet. The brief is appeal to young men without losing the understatement. The cues used: a steel sky instead of a pastel one, bone paper instead of white, a grid that sits left, a monospace for labels and numbers the way gear tags and camera overlays use one, and index numbers and timestamps as a design element. Not used: heavy weights, black, neon, texture, camo, anything that looks like a drop. Each row: the hero, a creator panel, a cover in the grid, the end card, the avatar at three sizes.</p>%s</body></html>') % (fonts(), rows)
    write(OUT + "/field.html", page)
    subprocess.run(["node", os.path.join(ROOT, "brand", "src", "shot.mjs"), os.path.join(ROOT, OUT, "field.html"), os.path.join(ROOT, OUT, "field.png"), "1700"], check=True)


if __name__ == "__main__":
    build()
    print("field sheet written")
