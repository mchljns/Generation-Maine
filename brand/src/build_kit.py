"""Brand kit: the master brand plus Route A ("In their words") and Route B ("Hometown"),
each shown on the real-use mockups named in brand/00-platform.md.

  python3 brand/src/build_kit.py     # logo files and brand/kit/kit.html
  node brand/src/render_kit.mjs      # exports every artboard to PNG, runs checks

Sample lines and sample towns are for layout only. Real lines and towns come from the creators.
"""
import base64
import os

from gmlib import ROOT, write
from build_v4 import wordmark_one_line, wordmark_stacked, g_icon, placed, rect, text, svg, f
from build_v6 import C, ratio
import build_kit_d

OUT = "brand/kit"
MPI = "An initiative of Maine Policy Institute"

TOWNS = ["Rumford", "Presque Isle", "Biddeford", "Machias", "Lewiston", "Skowhegan", "Belfast", "Fort Kent", "Sanford"]
LINES = ["I want to buy a house in my hometown", "My shop opened in May", "Most of my friends moved away",
         "I drive 40 minutes to work", "I came back after college", "I live with my parents for now",
         "I work two jobs to stay", "I love it here and I am doing the math", "I fix boats all winter"]
TOPICS = ["Finding a place", "Starting a shop", "Who stays", "The commute", "Coming home", "Moving out", "Two jobs", "Doing the math", "Winter work"]


# ------------------------------------------------------------------ master brand files
def build_logos():
    m = {}
    for suf, fg in (("", C["spruce"]), ("-reversed", C["birch"]), ("-black", "#000000"), ("-white", "#FFFFFF")):
        dot = C["marigold"] if suf in ("", "-reversed") else fg
        b, w, h = wordmark_one_line(fg, dot, "circle")
        m["wordmark" + suf] = svg(w, h, b, "Generation Maine")
        b, w, h = wordmark_stacked(fg, dot, "circle")
        m["stacked" + suf] = svg(w, h, b, "Generation Maine")
    m["icon"] = svg(200, 200, g_icon(0, 0, 200, C["spruce"], C["birch"], C["marigold"], "circle", 0), "Generation Maine")
    m["icon-light"] = svg(200, 200, g_icon(0, 0, 200, C["birch"], C["spruce"], C["marigold"], "circle", 0), "Generation Maine")
    m["icon-marigold"] = svg(200, 200, g_icon(0, 0, 200, C["marigold"], C["ink"], C["spruce"], "circle", 0), "Generation Maine")
    m["icon-bare"] = svg(200, 200, g_icon(0, 0, 200, None, C["birch"], C["marigold"], "circle", 0), "Generation Maine")
    # Endorsement lockup: the wordmark with the institute line, one rule between.
    for suf, fg in (("", C["spruce"]), ("-reversed", C["birch"])):
        b, w, h = wordmark_one_line(fg, C["marigold"], "circle")
        body = b + rect(0, h + 22, w, 2, fg) + text(0, h + 62, MPI, 30, fg, weight=600)
        m["endorsed" + suf] = svg(w, h + 76, body, "Generation Maine, an initiative of Maine Policy Institute")
    for k, v in m.items():
        write("%s/assets/logo/%s.svg" % (OUT, k), v)
    return m


# ------------------------------------------------------------------ kit page
def font64(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def inl(s, cls=""):
    return s.replace("<svg ", '<svg class="%s" aria-hidden="true" ' % cls, 1).replace(' role="img"', "")


def ui_overlay(handle="@creator.handle", cap="[Caption from the creator]"):
    """Generic short-video app chrome, so we see what the platform covers."""
    rail = "".join('<i class="ic"></i>' for _ in range(4))
    return ('<div class="ui"><div class="tabs"><span>Following</span><b>For You</b></div>'
            '<div class="rail"><i class="av"></i>%s</div>'
            '<div class="meta"><b>%s</b><span>%s</span><span class="snd">original sound</span></div>'
            '<div class="nav"><i></i><i></i><i class="plus"></i><i></i><i></i></div></div>') % (rail, handle, cap)


def bug(icon):
    return '<div class="bug">%s<span>Generation Maine</span></div>' % icon


def say(line, cls=""):
    """Route A caption: the sentence set in Birch blocks, ending on the Marigold dot."""
    head, _, last = line.rpartition(" ")
    body = (head + " " if head else "") + '<b class="nw">%s<i class="d"></i></b>' % last
    return '<p class="say %s"><span>%s</span></p>' % (cls, body)


def who(name="[Creator name]", town="[Hometown]"):
    return '<p class="who"><b>%s</b> · %s, Maine</p>' % (name, town)


def town(t, cls="", width=None):
    """Town in condensed capitals. width= fits the longest word to that many px."""
    style = ""
    if width:
        longest = max(len(w) for w in t.split())
        style = ' style="font-size:%dpx"' % min(40, int(width / (longest * 0.47)))
    return '<p class="town %s"%s>%s</p>' % (cls, style, t)


def artboard(aid, cls, inner, cap, w, h):
    return ('<figure class="card"><div id="%s" class="ab %s" style="width:%dpx;height:%dpx">%s</div>'
            '<figcaption>%s</figcaption></figure>' % (aid, cls, w, h, inner, cap))


def route_mockups(r, m):
    icon = inl(m["icon-bare"], "gi")
    wm_rev = inl(m["wordmark-reversed"], "wm")
    wm = inl(m["wordmark"], "wm")
    out = []
    if r == "a":
        first = '<div class="foot"></div>%s<div class="open">%s%s</div>%s' % (bug(icon), say(LINES[3], "lg"), who(town="Skowhegan"), ui_overlay())
        lower = '<div class="foot"></div>%s<div class="l3a">%s%s</div>%s' % (bug(icon), say("I leave before sunrise all winter", "md"), who(town="Skowhegan"), ui_overlay())
        end = ('<div class="endc">%s<div class="endmid">%s<ul class="hl"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
               '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul></div><p class="mpi">%s</p></div>') % (wm_rev, say("Follow along", "lg"), MPI)
        covers = ""
        bgs = ["sp", "bi", "pi"]
        for i in range(9):
            covers += '<div class="cov %s">%s<p class="cn">%s, Maine</p></div>' % (bgs[i % 3], say(LINES[i], "sm"), TOWNS[i])
        sub_mid = '<div class="subq">%s%s</div>' % (say("I came back after college. Here is why", "md"), who(town="Belfast"))
        hero_side = '<div class="hside">%s%s%s%s%s%s</div>' % (say(LINES[0], "md"), who(town="Lewiston"), say(LINES[1], "md"), who(town="Belfast"), say(LINES[6], "md"), who(town="Fort Kent"))
        post = '<div class="pimg"><div class="foot"></div>%s<div class="pcap">%s</div></div>' % (bug(icon), say(LINES[5], "md"))
    else:
        first = '<div class="foot"></div>%s<div class="open b">%s%s</div>%s' % (bug(icon), '<p class="lives">[Creator name] lives in</p>', town("Skowhegan", "xl"), ui_overlay())
        lower = '<div class="foot"></div>%s<div class="l3b"><p class="t">Skowhegan</p><p class="n">[Creator name]<span>Episode 04 · The commute</span></p></div>%s' % (bug(icon), ui_overlay())
        wall = "".join('<span>%s</span>' % t for t in TOWNS)
        end = ('<div class="endc b"><div class="wall">%s</div>%s<div class="endmid"><p class="fa">Follow along</p><ul class="hl"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
               '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul></div><p class="mpi">%s</p></div>') % (wall, wm_rev, MPI)
        covers = ""
        bgs = ["sp", "mg", "bi"]
        for i in range(9):
            covers += '<div class="cov b %s"><p class="ep">EP %02d</p>%s<p class="cn">%s</p></div>' % (bgs[i % 3], i + 1, town(TOWNS[i], "cv", width=104), TOPICS[i])
        sub_mid = '<p class="dateline">Belfast, Maine</p>'
        hero_side = '<div class="hwall">%s</div>' % "".join('<span class="%s">%s</span>' % ("on" if i == 5 else "", t) for i, t in enumerate(TOWNS + TOWNS[:3]))
        post = '<div class="pimg"><div class="foot"></div>%s<div class="ptown">%s<p>[Creator name]</p></div></div>' % (bug(icon), town("Machias", "md"))

    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9 %s">%s</div></div>') % (inl(m["icon"], "pa"), MPI, r, covers)
    substack = ('<div class="subst %s"><div class="sh">%s</div>%s<div class="sb"><p class="kick">Episode 06</p><h3>[Post title in plain words]</h3>'
                '<p class="by">[Creator name] · [Hometown], Maine</p><p>Short videos and this newsletter are made by young Maine creators about the rules that shape their lives.</p>'
                '%s<p>[Body of the post continues in the creator\'s own words.]</p></div><p class="sfoot">%s</p></div>') % (
        r, wm_rev if r == "a" else '%s<p class="shtown">Belfast</p>' % wm_rev, "", sub_mid, MPI)
    hero = ('<div class="web %s"><div class="wn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<div class="wh"><div><p class="wl">%s</p><h1>Young Mainers on building a life here<i class="d"></i></h1>'
            '<p class="wlede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="wbtn"><span class="b1">Meet the creators</span><span class="b2">Follow along</span></p></div>%s</div></div>') % (r, wm_rev, MPI, hero_side)
    collab = ('<div class="feed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post

    ra = r.upper()
    out.append(artboard("%s-first" % r, "ph9", first, "%s1 · Video, first seconds, with the app's buttons on top" % ra, 360, 640))
    out.append(artboard("%s-lower" % r, "ph9", lower, "%s2 · Lower third, mid-video" % ra, 360, 640))
    out.append(artboard("%s-end" % r, "ph9", end, "%s3 · End card" % ra, 360, 640))
    out.append(artboard("%s-grid" % r, "ph9 light", grid, "%s4 · Profile grid of nine covers" % ra, 360, 640))
    out.append(artboard("%s-substack" % r, "light", substack, "%s6 · Substack header and email" % ra, 480, 640))
    out.append(artboard("%s-collab" % r, "ph9 light", collab, "%s8 · Collab post on a creator's own account" % ra, 360, 640))
    web = artboard("%s-web" % r, "", hero, "%s7 · Website hero, no photo" % ra, 1200, 680)
    return "".join(out), web


def ttl(t, cls=""):
    """Signature headline: big, tight, sentence case, ending on the Marigold dot."""
    head, _, last = t.rpartition(" ")
    return '<p class="ttl %s">%s<b class="nw">%s<i class="d"></i></b></p>' % (cls, (head + " ") if head else "", last)


def plain(name="[Creator name]", town="[Hometown]"):
    return '<p class="plain"><b>%s</b><span>%s, Maine</span></p>' % (name, town)


def quiet_mockups(m):
    icon = inl(m["icon-bare"], "gi")
    wm_rev = inl(m["wordmark-reversed"], "wm")
    wm = inl(m["wordmark"], "wm")
    first = '<div class="foot"></div>%s%s' % (bug(icon), ui_overlay())
    lower = '<div class="foot"></div>%s<div class="ql3">%s</div>%s' % (bug(icon), plain(town="Skowhegan"), ui_overlay())
    end = ('<div class="qend"><p class="qk">Generation Maine</p>%s<ul class="hl q"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
           '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul><p class="mpi">%s</p></div>') % (ttl("Follow along", "xl"), MPI)
    fields = ["sp", "bi", "pi", "bi", "sp", "mg", "pi", "sp", "bi"]
    covers = "".join('<div class="cov q %s"><p class="ep">EP %02d</p>%s<p class="cn">%s</p></div>' % (fields[i], i + 1, ttl(TOPICS[i], "cv"), "[Creator name]")
                     for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9">%s</div></div>') % (inl(m["icon"], "pa"), MPI, covers)
    substack = ('<div class="subst q"><div class="qsh">%s</div><div class="sb"><p class="kick">Episode 06</p><h3>[Post title in plain words]</h3>'
                '<p class="by">[Creator name] · [Hometown], Maine</p><p>Short videos and this newsletter are made by young Maine creators about the rules that shape their lives.</p>'
                '<p>[Body of the post continues in the creator\'s own words.]</p><p>[Body continues.]</p></div><p class="sfoot">%s</p></div>') % (wm, MPI)
    hero = ('<div class="web q"><div class="wn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<div class="qh"><p class="wl">%s</p><h1>Young Mainers on building a life here<i class="d"></i></h1>'
            '<div class="qrow"><p class="wlede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="wbtn"><span class="b1">Meet the creators</span><span class="b2">Follow along</span></p></div></div>'
            '<div class="qnext"><span>01</span> What it is</div></div>') % (wm_rev, MPI)
    post = '<div class="pimg"><div class="foot"></div>%s<div class="ql3 p">%s</div></div>' % (bug(icon), plain(town="Machias"))
    collab = ('<div class="feed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    out = [artboard("q-first", "ph9", first, "S1 · Video, first seconds. Only the bug.", 360, 640),
           artboard("q-lower", "ph9", lower, "S2 · Name and town, plain", 360, 640),
           artboard("q-end", "ph9", end, "S3 · End card", 360, 640),
           artboard("q-grid", "ph9 light", grid, "S4 · Profile grid of nine covers", 360, 640),
           artboard("q-substack", "light", substack, "S6 · Substack header and email", 480, 640),
           artboard("q-collab", "ph9 light", collab, "S8 · Collab post on a creator's own account", 360, 640)]
    return out, artboard("q-web", "", hero, "S7 · Website hero, no photo", 1200, 680)


# ------------------------------------------------------------------ Signature, round two
# Changes from the pressure test (brand/03-pressure-test.md):
#  - one margin unit M = frame width / 15; headline baseline sits on the bottom safe line
#  - the bug is the wordmark alone, so there is one lockup to learn
#  - covers carry one headline and one plain credit line, no episode numbers
#  - field order is Spruce, Birch, Pine; every ninth post Marigold takes Pine's place
#  - outside the wordmark, Marigold appears once: the headline dot or the Marigold field
#  - labels are sentence case, Inter 400 and 600 only; Bricolage 800 only
#  - the disclosure sentence never changes and sits in the same place on every surface
ORDER = ["sp", "bi", "pi", "sp", "bi", "pi", "sp", "bi", "mg"]


def sbug(m):
    return '<div class="sbug">%s</div>' % inl(m["wordmark-reversed"], "wm")


def credit(name="[Creator name]", town="[Hometown]", cls=""):
    return '<p class="credit %s"><b>%s</b> %s, Maine</p>' % (cls, name, town)


def sig_mockups(m):
    wm_rev = inl(m["wordmark-reversed"], "wm")
    first = '<div class="foot"></div>%s%s' % (sbug(m), ui_overlay())
    lower = '<div class="foot"></div>%s<div class="sl3">%s</div>%s' % (sbug(m), credit(town="Skowhegan", cls="lg"), ui_overlay())
    end = ('<div class="send">%s<div class="slow">%s<ul class="hl s"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
           '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul></div><p class="disc">%s</p></div>') % (wm_rev, ttl("Follow along", "xl"), MPI)
    covers = "".join('<div class="cov s %s">%s%s</div>' % (ORDER[i], credit(town=TOWNS[i], cls="cv"), ttl(TOPICS[i], "cv"))
                     for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9">%s</div></div>') % (inl(m["icon"], "pa"), MPI, covers)
    substack = ('<div class="subst s"><div class="ssh">%s</div><p class="sdisc">%s</p><div class="sb"><h3>[Post title in plain words]</h3>'
                '%s<p>[First paragraph in the creator\'s own words.]</p>'
                '<p>[Body continues.]</p><p>[Body continues.]</p></div>'
                '<p class="sfoot">Short videos and this newsletter are made by young Maine creators. %s.</p></div>') % (
        wm_rev, MPI, credit(town="Belfast", cls="by"), MPI)
    hero = ('<div class="web s"><div class="wn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<p class="sdisc w">%s</p>'
            '<div class="sh1"><h1>Young Mainers on building a life here<i class="d"></i></h1>'
            '<div class="sside"><p class="wlede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="wbtn"><span class="b1">Meet the creators</span><span class="b2">Follow along</span></p></div></div>'
            '<div class="qnext s">What it is</div></div>') % (wm_rev, MPI)
    post = '<div class="pimg"><div class="foot"></div>%s<div class="sl3 p">%s</div></div>' % (sbug(m), credit(town="Machias", cls="lg"))
    collab = ('<div class="feed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    out = [artboard("s-first", "ph9", first, "S1 · Video, first seconds. The wordmark is the bug.", 360, 640),
           artboard("s-lower", "ph9", lower, "S2 · Name and town, plain, on the safe line", 360, 640),
           artboard("s-end", "ph9", end, "S3 · End card", 360, 640),
           artboard("s-grid", "ph9 light", grid, "S4 · Profile grid of nine covers", 360, 640),
           artboard("s-substack", "light", substack, "S6 · Substack header and email", 480, 640),
           artboard("s-collab", "ph9 light", collab, "S8 · Collab post on a creator's own account", 360, 640)]
    return out, artboard("s-web", "", hero, "S7 · Website hero, no photo", 1200, 680)


CHANGES = [
    ("Video, first seconds", "Before: a G icon plus spaced capitals, a third lockup to learn. After: the wordmark alone, one margin in from the left."),
    ("Lower third", "Before: a Bricolage name over tracked capitals. After: name in Inter SemiBold, town in sentence case, on the safe line above the app's captions."),
    ("End card", "Before: the name in small capitals and no wordmark. After: the wordmark at half the frame width, top left. Headline and handles sit low left. The disclosure sits on the bottom margin."),
    ("Profile grid", "Before: episode numbers and a loose color order. After: Spruce, Birch and Pine fall into columns. Marigold takes the ninth slot. One credit line top left, one headline low left."),
    ("Substack", "Before: a white header, with the disclosure only at the foot. After: a Spruce masthead with the wordmark low left and the disclosure right under it. The byline sits above the text on a hairline."),
    ("Collab post", "After: the wordmark bug and the sentence-case credit, the same as in the video."),
]


def before_after(q, s):
    rows = ""
    for (title, note), a, b in zip(CHANGES, q, s):
        rows += ('<div class="pair"><div class="pn"><p class="k">%s</p><p>%s</p></div><div class="cards tight">%s%s</div></div>'
                 % (title, note, a.replace("<figcaption>", "<figcaption>Before · "), b.replace("<figcaption>", "<figcaption>After · ")))
    return rows


# ------------------------------------------------------------------ Concept C: Offset
# Every frame breaks at the same height, two thirds down. Above: footage, or a field in the
# order Spruce, Moss, Pine, with Marigold every ninth post. Below: a Birch band, always, which
# carries the plain credit. In a three-across grid the bands line up into one stripe.
O_ORDER = ["sp", "mo", "pi", "sp", "mo", "pi", "sp", "mo", "mg"]


def offset_mockups(m):
    wm_rev = inl(m["wordmark-reversed"], "wm")
    wm = inl(m["wordmark"], "wm")
    first = '<div class="foot"></div>%s%s' % (sbug(m), ui_overlay())
    lower = '<div class="foot"></div>%s<div class="ol3">%s</div>%s' % (sbug(m), credit(town="Skowhegan", cls="lg"), ui_overlay())
    end = ('<div class="oend"><div class="otop sp">%s%s</div><div class="oband"><ul class="hl o"><li><b>Instagram</b>[@handle]</li><li><b>TikTok</b>[@handle]</li>'
           '<li><b>YouTube</b>[@handle]</li><li><b>Substack</b>[name].substack.com</li></ul><p class="disc o">%s</p></div></div>') % (wm_rev, ttl("Follow along", "xl"), MPI)
    covers = "".join('<div class="cov o"><div class="otop %s">%s</div><div class="oband">%s</div></div>' % (O_ORDER[i], ttl(TOPICS[i], "cv"), credit(town=TOWNS[i], cls="cv"))
                     for i in range(9))
    grid = ('<div class="prof"><div class="ph"><span class="pav">%s</span><div><b>Generation Maine</b><span>[@handle]</span></div></div>'
            '<p class="bio">Young Mainers on building a life here. %s.</p><div class="grid9 o">%s</div></div>') % (inl(m["icon"], "pa"), MPI, covers)
    substack = ('<div class="subst o"><div class="osh"><div class="otop sp">%s</div><div class="oband"><p>%s</p></div></div><div class="sb"><h3>[Post title in plain words]</h3>'
                '%s<p>[First paragraph in the creator\'s own words.]</p><p>[Body continues.]</p><p>[Body continues.]</p></div>'
                '<p class="sfoot">%s</p></div>') % (wm_rev, MPI, credit(town="Belfast", cls="by"), MPI)
    hero = ('<div class="web o"><div class="otop sp"><div class="wn">%s<nav><span>About</span><span>Creators</span><span>Follow</span></nav></div>'
            '<h1>Young Mainers on building a life here<i class="d"></i></h1></div>'
            '<div class="oband"><p class="wlede">Short videos by young Maine creators about the rules that shape their lives.</p>'
            '<p class="wbtn"><span class="b1">Meet the creators</span><span class="b2">Follow along</span></p><p class="disc o">%s</p></div></div>') % (wm_rev, MPI)
    post = ('<div class="pimg o"><div class="otop"><div class="foot"></div></div><div class="oband">%s%s</div></div>'
            % (credit(town="Machias", cls="md"), inl(m["wordmark"], "wm")))
    collab = ('<div class="feed"><div class="fh"><i class="cav">C</i><div><b>[creator.handle] and generationmaine</b><span>Paid partnership with Generation Maine</span></div></div>'
              '%s<div class="fa"><i></i><i></i><i></i></div><p class="fc"><b>[creator.handle]</b> [Caption in the creator\'s words]</p></div>') % post
    out = [artboard("o-first", "ph9", first, "C1 · Video, first seconds. Only the wordmark.", 360, 640),
           artboard("o-lower", "ph9", lower, "C2 · Name and town sit on the two-thirds line", 360, 640),
           artboard("o-end", "ph9", end, "C3 · End card", 360, 640),
           artboard("o-grid", "ph9 light", grid, "C4 · Profile grid: the bands line up", 360, 640),
           artboard("o-substack", "light", substack, "C6 · Substack header and email", 480, 640),
           artboard("o-collab", "ph9 light", collab, "C8 · Collab post: the creator's photo over the band", 360, 640)]
    return out, artboard("o-web", "", hero, "C7 · Website hero, no photo", 1200, 680)


O_SCORE = """<p class="k" style="margin-top:34px">Against the test, first pass</p>
  <table class="checks"><tr><th>Criterion</th><th>Signature, round two</th><th>Offset</th></tr>
  <tr><td>1 Signs, does not cover</td><td>Pass</td><td>Pass in video, which is the same as Signature. Watch the collab post: the band takes a third of the creator's photo.</td></tr>
  <tr><td>2 Survives the crop</td><td>Pass</td><td>Pass. Same avatar.</td></tr>
  <tr><td>3 Carries a person</td><td>Pass</td><td>Pass, and the strongest yet. Every cover and post gives the name its own band.</td></tr>
  <tr><td>4 Neutral</td><td>Pass</td><td>Pass. Photo over a light band can drift toward an instant-photo look. Square corners and a full-bleed band keep it modern.</td></tr>
  <tr><td>5 Both audiences</td><td>Pass</td><td>Pass. The site and Substack read as editorial. Covers read as a set.</td></tr>
  <tr><td>6 Stands without photos</td><td>Pass</td><td>Pass. Field and band carry every surface.</td></tr>
  <tr><td>7 Ownable</td><td>Partial</td><td>Partial, and the closest yet. The stripe across the grid is unusual and visible at thumbnail size. A layout habit can still be copied.</td></tr>
  <tr><td>8 Easy to make</td><td>Pass</td><td>Pass. Two boxes in one template: field and band.</td></tr>
  </table>
  <p class="note" style="margin-top:14px">Grade so far: Signature B, Offset B plus. Offset keeps every Signature type rule and adds one structural habit. It costs a third of every cover and photo, and headlines get less room.</p>"""


def overlays(m):
    icon = inl(m["icon-bare"], "gi")
    o = []
    o.append(artboard("ov-bug", "clear", bug(icon), "Video bug, top left, transparent", 360, 640))
    o.append(artboard("ov-a-lower", "clear", '<div class="l3a">%s%s</div>' % (say("[One line in the creator's words]", "md"), who()), "Route A lower third, transparent", 360, 640))
    o.append(artboard("ov-b-lower", "clear", '<div class="l3b"><p class="t">[Hometown]</p><p class="n">[Creator name]<span>Episode 00 · [Topic]</span></p></div>', "Route B lower third, transparent", 360, 640))
    return "".join(o)


def sig_overlays(m):
    return (artboard("ov-s-bug", "clear", sbug(m), "Round two bug: the wordmark, transparent", 360, 640)
            + artboard("ov-s-lower", "clear", '<div class="sl3">%s</div>' % credit(cls="lg"), "Round two name and town, transparent", 360, 640))


def avatars(m):
    others = [("#7A4E9E", "RJ"), ("#2F6FA3", "MB"), ("#B4532A", "TK")]
    big = "".join('<span class="oav" style="background:%s">%s</span>' % (c, t) for c, t in others[:2])
    big = big[:len(big) // 2] + '<span class="gav">%s</span>' % inl(m["icon"], "") + big[len(big) // 2:]
    rows = "".join('<li><span class="oav s" style="background:%s">%s</span><b>Account name</b><span class="fb">Follow</span></li>' % (c, t) for c, t in others)
    rows = rows.replace("<li>", '<li><span class="gav s">%s</span><b>Generation Maine</b><span class="fb">Follow</span></li><li>' % inl(m["icon"], ""), 1)
    tab = '<div class="tabbar"><span class="tab on"><i>%s</i>Generation Maine</span><span class="tab"><i class="g"></i>Other site</span></div>' % inl(m["icon"], "")
    inner = '<div class="avs"><p class="k">Profile size, 110 px</p><div class="row3">%s</div><p class="k">List size, 40 px</p><ul class="sugg">%s</ul><p class="k">Browser tab, 16 px</p>%s</div>' % (big, rows, tab)
    return artboard("m-avatar", "light", inner, "5 · Avatar among other accounts (shared by both routes)", 480, 640)


CSS = r"""
@font-face{font-family:Bric;src:url(data:font/woff2;base64,{{F800}}) format('woff2');font-weight:800}
@font-face{font-family:Bric;src:url(data:font/woff2;base64,{{F700}}) format('woff2');font-weight:700}
@font-face{font-family:Cond;src:url(data:font/woff2;base64,{{FCOND}}) format('woff2');font-weight:800}
@font-face{font-family:Inter;src:url(data:font/woff2;base64,{{FINTER}}) format('woff2');font-weight:400 700}
:root{--sp:{{spruce}};--pine:{{pine}};--bi:{{birch}};--ink:{{ink}};--mg:{{marigold}};--sage:{{sage}};--moss:{{moss}};--stone:{{stone}}}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 Inter,system-ui,sans-serif;color:var(--ink);background:#E9E5DA;-webkit-font-smoothing:antialiased}
.w{max-width:1320px;margin:0 auto;padding:0 32px}
header.top{background:var(--sp);color:var(--bi);padding:64px 0 56px}
header.top h1{font:800 64px/1 Bric;letter-spacing:-.03em;margin:14px 0 18px}
header.top p{max-width:70ch;margin:0 0 10px;color:#E2E2D8}
.k{font:600 12px/1.3 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--moss);margin:0 0 10px}
section{padding:56px 0;border-bottom:1px solid #D6D0C2}
section h2{font:700 40px/1.05 Bric;letter-spacing:-.02em;margin:6px 0 10px}
section>.w>p{max-width:70ch}
.cards{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start;margin-top:26px}
.card{margin:0}
figcaption{font:600 12px/1.4 Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--stone);margin-top:10px;max-width:360px}
.ab{position:relative;overflow:hidden;background:#56625B;color:var(--bi);border-radius:14px;box-shadow:0 18px 40px -26px rgba(11,43,33,.6)}
.ab.light{background:#fff;color:var(--ink)}
.ab.clear{background:repeating-conic-gradient(#d9d9d9 0 25%,#f2f2f2 0 50%) 0 0/16px 16px;border-radius:0}
.foot{position:absolute;inset:0;background:#56625B}
.foot::after{content:"Creator footage";position:absolute;left:0;right:0;top:46%;text-align:center;font:600 11px Inter;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.28)}
/* generic app chrome */
.ui{position:absolute;inset:0;pointer-events:none;color:#fff}
.ui .tabs{position:absolute;top:14px;left:0;right:0;text-align:center;font:600 13px Inter;opacity:.9}
.ui .tabs span{opacity:.6;margin-right:14px}
.ui .rail{position:absolute;right:10px;bottom:120px;display:flex;flex-direction:column;gap:16px;align-items:center}
.ui .rail i{display:block;width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.85)}
.ui .rail i.av{width:40px;height:40px;background:#A7B1AB;border:2px solid #fff}
.ui .meta{position:absolute;left:12px;right:64px;bottom:62px;font:13px/1.35 Inter;display:flex;flex-direction:column;gap:3px;text-shadow:0 1px 2px rgba(0,0,0,.4)}
.ui .meta .snd{font-size:11px;opacity:.8}
.ui .nav{position:absolute;left:0;right:0;bottom:0;height:48px;background:#000;display:flex;justify-content:space-around;align-items:center}
.ui .nav i{width:20px;height:20px;border-radius:5px;background:#666}
.ui .nav i.plus{width:36px;height:24px;background:#fff}
/* master: bug */
.bug{position:absolute;top:44px;left:12px;display:flex;align-items:center;gap:6px;font:700 10px/1 Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--bi);text-shadow:0 1px 3px rgba(0,0,0,.35)}
.bug .gi{width:26px;height:26px;filter:drop-shadow(0 1px 2px rgba(0,0,0,.3))}
/* Route A: caption */
.say{margin:0;font:800 22px/1.32 Bric;letter-spacing:-.01em;color:var(--ink)}
.say span{background:var(--bi);padding:.1em .34em;-webkit-box-decoration-break:clone;box-decoration-break:clone;border-radius:3px}
.say .nw{font-weight:inherit;white-space:nowrap}
.say .d{display:inline-block;width:.3em;height:.3em;border-radius:50%;background:var(--mg);margin-left:.08em;vertical-align:baseline}
.say.lg{font-size:28px}.say.md{font-size:21px}.say.sm{font-size:15px;line-height:1.34}
.who{margin:8px 0 0;font:600 11px/1.3 Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--bi);text-shadow:0 1px 2px rgba(0,0,0,.35)}
.who b{font-weight:700}
.open{position:absolute;left:14px;right:70px;top:170px}
.l3a{position:absolute;left:14px;right:70px;bottom:196px}
.cov .say{position:absolute;left:8px;right:8px;top:12px}
/* Route B: town */
.town{margin:0;font:800 64px/.86 Cond;text-transform:uppercase;letter-spacing:-.005em;color:var(--mg)}
.town.xl{font-size:72px;color:var(--bi);text-shadow:0 2px 12px rgba(0,0,0,.25)}
.town.md{font-size:44px;color:var(--bi)}
.open.b{top:150px}
.lives{margin:0 0 6px;font:600 12px Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--bi);text-shadow:0 1px 2px rgba(0,0,0,.35)}
.l3b{position:absolute;left:0;bottom:196px;max-width:290px}
.l3b .t{margin:0;background:var(--sp);color:var(--bi);font:800 34px/1 Cond;text-transform:uppercase;padding:9px 14px 7px 14px;display:inline-block;border-left:6px solid var(--mg)}
.l3b .n{margin:0;background:var(--bi);color:var(--ink);font:700 15px/1.2 Bric;padding:7px 14px;display:block}
.l3b .n span{display:block;font:600 10px/1.4 Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--stone)}
/* end cards */
.endc{position:absolute;inset:0;background:var(--sp);padding:48px 24px 28px;display:flex;flex-direction:column;justify-content:space-between}
.endc .wm{width:210px;height:auto;position:relative}
.endmid{position:relative}
.hl{list-style:none;margin:18px 0 0;padding:0;font:14px/1 Inter;color:var(--bi)}
.hl li{display:flex;gap:14px;padding:11px 0;border-bottom:1px solid #2E6450}
.hl b{width:84px}
.mpi{margin:0;font:600 13px/1.3 Inter;color:var(--bi);position:relative}
.fa{margin:0;font:800 38px/1 Bric;letter-spacing:-.02em;color:var(--mg)}
.wall{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 10px;font:800 58px/.88 Cond;text-transform:uppercase;color:#154F3C;overflow:hidden;white-space:nowrap}
/* grid */
.prof{position:absolute;inset:0;padding:40px 10px 0;background:#fff}
.ph{display:flex;gap:12px;align-items:center}
.pav svg{width:62px;height:62px;border-radius:50%;display:block}
.ph b{display:block;font:700 15px Inter}.ph span{font-size:12px;color:var(--stone)}
.bio{font-size:12px;line-height:1.45;margin:10px 0 12px;color:#34413A}
.grid9{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}
.cov{position:relative;aspect-ratio:3/4;overflow:hidden}
.cov.sp{background:var(--sp)}.cov.bi{background:var(--bi)}.cov.pi{background:var(--pine)}.cov.mg{background:var(--mg)}
.cov.bi .say span{background:var(--sp);color:var(--bi)}
.cn{position:absolute;left:8px;bottom:7px;margin:0;font:600 8px/1.2 Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--bi)}
.cov.bi .cn,.cov.mg .cn{color:var(--ink)}
.cov.b .town{position:absolute;left:7px;right:4px;bottom:22px;line-height:.86}
.cov.b.sp .town{color:var(--mg)}.cov.b.mg .town{color:var(--ink)}.cov.b.bi .town{color:var(--sp)}
.ep{position:absolute;left:8px;top:8px;margin:0;font:700 8px Inter;letter-spacing:.08em;color:inherit}
.cov.b.sp .ep{color:var(--bi)}.cov.b.mg .ep,.cov.b.bi .ep{color:var(--ink)}
/* substack */
.subst{position:absolute;inset:0;background:#fff}
.sh{background:var(--sp);height:140px;display:flex;align-items:center;padding:0 32px;position:relative;overflow:hidden}
.sh .wm{width:250px;height:auto;position:relative;z-index:1}
.shtown{position:absolute;right:-4px;bottom:-12px;margin:0;font:800 84px/1 Cond;text-transform:uppercase;color:#1B5642}
.sb{padding:26px 32px 0;font-size:14px;line-height:1.6;color:#2A332E}
.sb .kick{margin:0;font:600 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--moss)}
.sb h3{font:700 27px/1.1 Bric;letter-spacing:-.015em;margin:8px 0 8px;color:var(--ink)}
.sb .by{margin:0 0 14px;font:600 12px Inter;color:var(--stone)}
.subq{background:var(--sp);padding:18px 18px 16px;margin:6px 0 14px;border-radius:4px}
.dateline{margin:0 0 12px;font:800 26px/1 Cond;text-transform:uppercase;color:var(--sp);border-top:4px solid var(--sp);padding-top:10px}
.sfoot{position:absolute;left:32px;bottom:14px;margin:0;font:600 11px Inter;color:var(--stone)}
/* website */
.web{position:absolute;inset:0;background:var(--sp);color:var(--bi);overflow:hidden}
.wn{display:flex;justify-content:space-between;align-items:center;padding:24px 56px;position:relative;z-index:2}
.wn .wm{height:24px;width:auto}
.wn nav{display:flex;gap:28px;font:600 15px Inter}
.wh{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;padding:56px 56px 0;position:relative;z-index:2}
.wl{margin:0;font:600 12px Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--mg)}
.web h1{font:800 84px/.94 Bric;letter-spacing:-.03em;margin:18px 0 22px}
.web h1 .d{display:inline-block;width:.19em;height:.19em;border-radius:50%;background:var(--mg);margin-left:.04em}
.wlede{font-size:19px;color:#E6E4DA;max-width:34ch;margin:0 0 26px}
.wbtn{display:flex;gap:12px;margin:0}
.wbtn span{padding:14px 22px;font-weight:700;border-radius:3px}
.b1{background:var(--mg);color:var(--ink)}.b2{box-shadow:inset 0 0 0 1.5px #9DB5A9}
.hside{display:flex;flex-direction:column;gap:4px;padding-top:30px}
.hside .who{margin:6px 0 18px}
.hwall{position:absolute;right:-40px;top:8px;height:640px;width:440px;display:flex;flex-direction:column;justify-content:flex-start;font:800 76px/.86 Cond;text-transform:uppercase;color:#1B5642;white-space:nowrap;z-index:-1}
.hwall .on{color:var(--mg)}
.web.b .wh{grid-template-columns:1fr}
.web.b .wh>div:first-child{max-width:600px;position:relative;z-index:3}
.web.b h1{font-size:76px}
/* collab feed */
.feed{position:absolute;inset:0;background:#fff;padding-top:36px}
.fh{display:flex;gap:10px;align-items:center;padding:0 12px 10px}
.cav{width:34px;height:34px;border-radius:50%;background:#A7B1AB;display:grid;place-items:center;font:700 13px Inter;color:#fff;font-style:normal}
.fh b{display:block;font:700 12.5px Inter}.fh span{font-size:11px;color:var(--stone)}
.pimg{position:relative;width:360px;height:450px;overflow:hidden}
.pcap{position:absolute;left:14px;right:40px;bottom:22px}
.ptown{position:absolute;left:14px;bottom:18px}
.ptown p:last-child{margin:6px 0 0;font:700 13px Bric;color:var(--bi)}
.fa{}
.feed .fa{display:flex;gap:14px;padding:10px 12px}
.feed .fa i{width:22px;height:22px;border-radius:6px;box-shadow:inset 0 0 0 2px #222}
.fc{margin:0 12px;font-size:12.5px;line-height:1.4}
/* avatars */
.avs{position:absolute;inset:0;padding:28px}
.row3{display:flex;gap:18px;margin-bottom:26px}
.oav,.gav{width:110px;height:110px;border-radius:50%;display:grid;place-items:center;font:700 30px Inter;color:#fff;overflow:hidden;flex:none}
.gav svg{width:100%;height:100%;display:block}
.oav.s,.gav.s{width:40px;height:40px;font-size:13px}
.sugg{list-style:none;margin:0 0 26px;padding:0}
.sugg li{display:flex;align-items:center;gap:12px;padding:7px 0;font-size:14px}
.sugg .fb{margin-left:auto;background:#E8E4DA;padding:5px 12px;border-radius:6px;font:600 12px Inter}
.tabbar{display:flex;gap:2px;background:#DAD6CC;padding:8px 8px 0;border-radius:8px 8px 0 0}
.tab{display:flex;gap:8px;align-items:center;background:#ECE9E1;padding:8px 12px;border-radius:8px 8px 0 0;font-size:12px}
.tab.on{background:#fff}
.tab i{width:16px;height:16px;display:block}.tab i svg{width:16px;height:16px;display:block}
.tab i.g{background:#999;border-radius:3px}
/* master sheet */
.sheet{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}
.tile{background:#fff;border-radius:14px;padding:28px;display:flex;align-items:center;justify-content:center;min-height:180px}
.tile.sp{background:var(--sp)}.tile.mg{background:var(--mg)}
.tile svg{max-width:100%;height:auto}
.tile.wide{grid-column:span 2}
.checks{width:100%;border-collapse:collapse;margin-top:18px;font-size:14px}
.checks td,.checks th{border-bottom:1px solid #D6D0C2;padding:9px 8px;text-align:left;vertical-align:top}
.checks th{font:600 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--stone)}
.note{font-size:13px;color:var(--stone)}

/* Signature */
.ttl{margin:0;font:800 30px/.95 Bric;letter-spacing:-.03em;color:var(--bi)}
.ttl .nw{font-weight:inherit;white-space:nowrap}
.ttl .d{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--mg);margin-left:.05em}
.ttl.xl{font-size:74px;line-height:.9}
.plain{margin:0;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.45)}
.plain b{display:block;font:700 19px/1.15 Bric;letter-spacing:-.01em}
.plain span{display:block;font:600 11px/1.5 Inter;letter-spacing:.06em;text-transform:uppercase;opacity:.92}
.ql3{position:absolute;left:14px;bottom:196px}
.ql3.p{bottom:18px}
.qend{position:absolute;inset:0;background:var(--sp);padding:48px 24px 28px;display:flex;flex-direction:column;justify-content:flex-end}
.qend .qk{position:absolute;top:48px;left:24px;margin:0;font:600 11px Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--sage)}
.qend .ttl{margin-bottom:22px}
.hl.q li{border-color:#2A5F4B}
.qend .mpi{margin-top:26px}
.cov.q .ttl{position:absolute;left:8px;right:6px;bottom:22px;font-size:21px}
.cov.q.bi .ttl{color:var(--sp)}.cov.q.mg .ttl{color:var(--ink)}.cov.q.mg .ttl .d{background:var(--ink)}
.cov.q.sp .ep,.cov.q.pi .ep{color:var(--sage)}.cov.q.bi .ep,.cov.q.mg .ep{color:var(--ink)}
.cov.q.pi{background:var(--pine)}
.qsh{padding:30px 32px 22px;border-bottom:1px solid #E1DBCC}
.qsh .wm{width:230px;height:auto;display:block}
.subst.q .sb h3{font:800 32px/1 Bric;letter-spacing:-.025em}
.web.q .qh{padding:70px 56px 0;position:relative;z-index:2}
.web.q h1{font-size:112px;line-height:.9;max-width:11ch;margin:18px 0 34px}
.qrow{display:flex;justify-content:space-between;align-items:flex-end;gap:40px}
.qrow .wlede{margin:0}
.qnext{position:absolute;left:0;right:0;bottom:0;height:64px;background:var(--bi);color:var(--moss);font:600 12px Inter;letter-spacing:.08em;text-transform:uppercase;padding:24px 56px}
.qnext span{color:var(--stone);margin-right:8px}


.pair{display:grid;grid-template-columns:260px 1fr;gap:28px;padding:26px 0;border-top:1px solid #D6D0C2}
.pair .pn p:last-child{font-size:14px;color:#34413A;margin:0}
.cards.tight{margin-top:0}
.find{width:100%;border-collapse:collapse;margin-top:18px;font-size:14px}
.find td,.find th{border-bottom:1px solid #D6D0C2;padding:9px 8px;text-align:left;vertical-align:top}
.find th{font:600 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--stone)}
.rules{margin:18px 0 0;padding-left:22px;max-width:80ch}.rules li{margin:0 0 8px}


/* Concept C: Offset. The break is always at two thirds of the height. */
.otop{position:relative}
.otop.sp{background:var(--sp)}.otop.mo{background:var(--moss)}.otop.pi{background:var(--pine)}.otop.mg{background:var(--mg)}
.oband{background:var(--bi);color:var(--ink)}
.ol3{position:absolute;left:var(--M);top:calc(66.667% - 52px)}
.oend{position:absolute;inset:0;display:grid;grid-template-rows:2fr 1fr}
.oend .otop{padding:44px var(--M) 22px;display:flex;flex-direction:column;justify-content:space-between}
.oend .wm{width:180px;height:auto;display:block}
.oend .oband{padding:12px var(--M) var(--M);display:flex;flex-direction:column;justify-content:space-between}
.hl.o{margin:0;color:var(--ink);font-size:13px}.hl.o li{padding:7px 0;border-color:#DDD6C6}
.disc.o{color:var(--ink)}
.grid9.o{gap:2px 2px}
.cov.o{display:grid;grid-template-rows:2fr 1fr;background:var(--bi)}
.cov.o .otop{position:relative}
.cov.o .ttl{position:absolute;left:8px;right:6px;bottom:8px;font-size:19px}
.cov.o .otop.mg .ttl{color:var(--pine)}.cov.o .otop.mg .ttl .d{background:var(--pine)}
.cov.o .oband{padding:7px 8px}
.cov.o .credit{font-size:8px;line-height:1.3;color:var(--ink)}.cov.o .credit b{display:block}
.osh{height:180px;display:grid;grid-template-rows:2fr 1fr}
.osh .otop{display:flex;align-items:flex-end;padding:0 32px 16px}
.osh .wm{width:220px;height:auto;display:block}
.osh .oband{display:flex;align-items:center;padding:0 32px}
.osh .oband p{margin:0;font:600 12px Inter;color:var(--ink)}
.subst.o .sb{padding-top:26px}
.subst.o .sb h3{font:800 34px/.98 Bric;letter-spacing:-.03em;margin:0 0 14px}
.web.o{display:grid;grid-template-rows:2fr 1fr;background:var(--bi)}
.web.o .otop{padding:0 56px 34px;display:flex;flex-direction:column;justify-content:space-between}
.web.o .wn{padding:24px 0}
.web.o h1{font:800 104px/.9 Bric;letter-spacing:-.03em;margin:0;max-width:12ch}
.web.o .oband{display:grid;grid-template-columns:1fr auto;grid-template-rows:1fr auto;column-gap:40px;padding:30px 56px 22px}
.web.o .wlede{color:var(--ink);margin:0;font-size:19px;max-width:36ch}
.web.o .wbtn{align-self:start}.web.o .wbtn span{white-space:nowrap}
.web.o .b1{background:var(--sp);color:var(--bi)}.web.o .b2{box-shadow:inset 0 0 0 1.5px var(--sp);color:var(--sp)}
.web.o .disc{grid-column:1/-1;font-size:13px;color:var(--stone)}
.pimg.o{display:grid;grid-template-rows:2fr 1fr;background:var(--bi)}
.pimg.o .oband{padding:16px 16px;display:flex;justify-content:space-between;align-items:flex-start}
.credit.md{font-size:13px;color:var(--ink)}.credit.md b{display:block;font-size:18px;letter-spacing:-.005em}
.pimg.o .wm{width:110px;height:auto;margin-top:4px}

/* Signature, round two. M = frame width / 15 (24 px on a 360 px frame, 72 px at 1080). */
.ab{--M:24px}
.sbug{position:absolute;top:44px;left:var(--M)}
.sbug .wm{width:118px;height:auto;display:block;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
.credit{margin:0;font:400 11px/1.35 Inter;color:inherit}
.credit b{font-weight:600}
.credit.lg{font-size:15px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.45)}
.credit.lg b{display:block;font-size:20px;line-height:1.2;letter-spacing:-.005em}
.sl3{position:absolute;left:var(--M);bottom:196px}
.sl3.p{bottom:var(--M)}
.send{position:absolute;inset:0;background:var(--sp);padding:44px var(--M) var(--M);display:flex;flex-direction:column;justify-content:space-between}
.send .wm{width:180px;height:auto;display:block}
.send .ttl{margin-bottom:20px}
.hl.s{margin:0}.hl.s li{border-color:#2A5F4B}
.disc{margin:0;font:600 13px/1.35 Inter;color:var(--bi)}
.cov.s{color:var(--bi)}
.cov.s.bi{color:var(--ink)}.cov.s.mg{color:var(--ink)}
.cov.s .credit{position:absolute;left:8px;top:8px;right:6px;font-size:7.5px;line-height:1.3}
.cov.s .credit b{display:block}
.cov.s .ttl{position:absolute;left:8px;right:6px;bottom:9px;font-size:21px}
.cov.s.bi .ttl{color:var(--sp)}.cov.s.mg .ttl{color:var(--pine)}.cov.s.mg .ttl .d{background:var(--pine)}
.subst.s{background:#fff}
.ssh{background:var(--sp);height:128px;padding:0 32px 22px;display:flex;align-items:flex-end}
.ssh .wm{width:220px;height:auto;display:block}
.sdisc{margin:0;padding:10px 32px;font:600 12px/1.3 Inter;color:var(--moss);background:var(--bi)}
.subst.s .sb{padding-top:28px}
.subst.s .sb h3{font:800 34px/.98 Bric;letter-spacing:-.03em;margin:0 0 14px}
.credit.by{font-size:13px;color:var(--stone);margin:0 0 18px;padding-bottom:14px;border-bottom:1px solid #E1DBCC}
.credit.by b{color:var(--ink)}
.subst.s .sfoot{right:32px;line-height:1.4}
.web.s .wn{padding:24px 56px}
.sdisc.w{background:none;padding:0 56px;color:var(--sage);position:relative;z-index:2}
.sh1{position:absolute;left:56px;right:56px;bottom:112px;display:flex;justify-content:space-between;align-items:flex-end;gap:40px}
.web.s h1{font:800 112px/.9 Bric;letter-spacing:-.03em;margin:0;max-width:11ch}
.sside{flex:none;width:380px;padding-bottom:10px}
.web.s .wbtn span{white-space:nowrap}
.sside .wlede{margin:0 0 22px;font-size:18px}
.web.s .b1{background:var(--bi);color:var(--ink)}
.qnext.s{color:var(--stone);letter-spacing:0;text-transform:none;font:600 14px Inter;padding:22px 56px;border-top:0}
"""


PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generation Maine Brand Kit</title><style>{{CSS}}</style></head><body>
<header class="top"><div class="w">
  <p class="k" style="color:var(--mg)">Generation Maine · Brand kit, round one</p>
  <h1>The brand, where it will actually live</h1>
  <p>One master brand, shared by both routes. Two ways to make the creator frame ownable, each shown on the real places people will meet it: inside a creator's video, in a profile grid, in a Substack email and on the website.</p>
  <p>Sample lines and sample towns are for layout only. Real lines and towns come from the creators.</p>
</div></header>

<section><div class="w">
  <p class="k">Master brand, shared by both routes</p>
  <h2>Quiet on purpose</h2>
  <p>The wordmark from Spruce &amp; Signal, drawn in Bricolage ExtraBold, with the dot on the i in Marigold. The G and dot is the avatar and favicon. It signs the work. It never covers it.</p>
  <div class="sheet">
    <div class="tile wide">{{WM}}</div><div class="tile sp">{{ICON_BARE}}</div>
    <div class="tile sp wide">{{WM_REV}}</div><div class="tile">{{ICON_L}}</div>
    <div class="tile">{{ST}}</div><div class="tile sp">{{ENDORSED_REV}}</div><div class="tile mg">{{ICON_M}}</div>
  </div>
  <div class="cards">{{AVATARS}}{{OVERLAYS}}</div>
</div></section>

<section><div class="w">
  <p class="k">Recommended direction, round two</p>
  <h2>Signature, tightened</h2>
  <p>We checked round one against two sets of real screens on Refero. The first set was editorial and creator-led media. The second was quiet, mission-led brands. Refero has few true nonprofits, so the second set leans on civic-minded companies and impact reports. We borrowed principles, not looks. The full notes are in <code>brand/03-pressure-test.md</code>.</p>
  <table class="find"><tr><th>What we saw</th><th>Where</th><th>What Signature does with it</th></tr>
  <tr><td>Covers in a series vary, but the title and the brand tag sit in the same place every time</td><td>The Athletic podcast grid</td><td>Fixed slots. One credit line top left, one headline low left, nothing else. Episode numbers come off the covers.</td></tr>
  <tr><td>The byline sits in the same place and style on every story</td><td>The New Yorker, The New York Times</td><td>Name and town are one plain line in the same spot on every surface, in sentence case.</td></tr>
  <tr><td>One accent color with one job</td><td>The New Yorker's labels, Anthropic's single dark button</td><td>Marigold has two jobs only: the dot and the ninth field. Buttons and labels lose it.</td></tr>
  <tr><td>Premium comes from space and hairlines, not decoration</td><td>Wealthsimple Magazine, Anthropic, Aesop</td><td>Hairline under the byline. Plain labels. No boxes around text.</td></tr>
  <tr><td>Contact or disclosure sits right under the title</td><td>Handshake newsroom</td><td>"An initiative of Maine Policy Institute" sits under the masthead on Substack and under the nav on the site, as well as in the footer.</td></tr>
  <tr><td>Big, tight, low-left sans on a full field is common</td><td>Dopper impact report, Bloomberg Businessweek</td><td>The anchor alone is not ownable. The dot, the column order and the credit line together have to carry it.</td></tr>
  <tr><td>Trend shapes, mascots and hand lettering</td><td>The Leap, Duolingo, Mailchimp</td><td>Kept out. They date fast and read as marketing.</td></tr>
  </table>
  <p class="k" style="margin-top:34px">The five rules, now measurable</p>
  <ol class="rules">
    <li>One idea per frame. A cover carries one headline of four words or fewer and one credit line.</li>
    <li>Big, tight type anchored low left. Bricolage ExtraBold, line height 0.9, tracking minus 3 percent, three lines at most. The margin is one fifteenth of the frame width, 72 px on a 1080 px frame.</li>
    <li>Full color fields in a fixed order: Spruce, Birch, Pine, then again. Every ninth post, Marigold takes Pine's place. In a three-across grid the colors fall into columns.</li>
    <li>Marigold once per frame, outside the wordmark. It is the dot that ends the headline, or it is the field. On a Marigold field the dot turns Pine.</li>
    <li>The creator's name and town are one plain line: name in Inter SemiBold, town in Inter Regular, sentence case. In video it sits on the safe line, 30 percent up from the bottom.</li>
  </ol>
  <p class="note">Type is Bricolage ExtraBold for headlines and the wordmark, and Inter Regular and SemiBold for everything else. The bug is the wordmark alone. The dot stays round, flat and still. It never winks, bounces or changes shape.</p>
  {{PAIRS}}
  <div class="pair"><div class="pn"><p class="k">Website hero</p><p>Before: Marigold in the label, the dot and the button, and a headline floating mid-frame. After: Marigold only in the dot and the logo. The button is Birch. The headline sits on the bottom margin. The disclosure sits in sentence case under the nav.</p></div><div>{{S_WEB_BEFORE}}<div style="height:24px"></div>{{S_WEB}}</div></div>
  <div class="pair"><div class="pn"><p class="k">Overlays</p><p>Transparent files for CapCut and Canva, built to the new rules.</p></div><div class="cards tight">{{SOVER}}</div></div>
  <p class="k" style="margin-top:34px">Against the test, round two</p>
  <table class="checks"><tr><th>Criterion</th><th>Round one</th><th>Round two</th></tr>
  <tr><td>1 Signs, does not cover</td><td>Pass</td><td>Pass. The bug is the wordmark at a third of the frame width, in the top left, and nothing else.</td></tr>
  <tr><td>2 Survives the crop</td><td>Pass</td><td>Pass. The avatar is unchanged.</td></tr>
  <tr><td>3 Carries a person</td><td>Pass</td><td>Pass, and stronger. Every cover now names the creator and the town.</td></tr>
  <tr><td>4 Neutral</td><td>Pass</td><td>Pass. No device, no claim, no red or blue.</td></tr>
  <tr><td>5 Both audiences</td><td>Pass</td><td>Pass, and stronger on Substack. The masthead, the disclosure and the byline read as editorial.</td></tr>
  <tr><td>6 Stands without photos</td><td>Pass</td><td>Pass. Type and color fields carry every surface.</td></tr>
  <tr><td>7 Ownable</td><td>Partial</td><td>Partial, but closer. The low-left anchor is common on its own. The dot period, the column order and the credit line are ours together. This becomes a pass only after a season of consistent use.</td></tr>
  <tr><td>8 Easy to make</td><td>Pass</td><td>Pass, and fewer choices. No episode numbers, one bug file, and the color order is written down.</td></tr>
  </table>
</div></section>

{{DSECTION}}
<section><div class="w">
  <p class="k">New concept, in progress</p>
  <h2>Concept C: Offset</h2>
  <p>Signature's weak spot is ownability. Its most ownable moment was an accident: in round two, the grid colors fell into columns. Offset makes a structural habit like that deliberate. It adds no symbol and no metaphor, and it keeps the master brand.</p>
  <p>The test sentence: every frame breaks at the same height, so the grid lines up. It says nothing about youth, Maine or economics.</p>
  <ol class="rules">
    <li>Every frame breaks at two thirds of its height. On a 1080 by 1350 cover, the line sits at 900 px.</li>
    <li>Above the line: the creator's footage or photo, or a field in the order Spruce, Moss, Pine. Every ninth post, Marigold takes Pine's place.</li>
    <li>Below the line: a Birch band, always. It carries the creator's name and town as one plain line.</li>
    <li>Marigold once per frame, outside the wordmark: the headline dot or the field.</li>
    <li>Inside a video, nothing covers the footage. The name and town sit on the two-thirds line, and the line itself stays invisible.</li>
  </ol>
  <div class="cards">{{O}}</div>
  <div class="cards">{{O_WEB}}</div>
  {{O_SCORE}}
</div></section>

<section><div class="w">
  <p class="k">Round one, kept for the record</p>
  <h2>Signature, round one</h2>
  <p>No metaphor. The name already says young and Maine, so the look adds confidence instead of repeating it. Five rules carry everything: one idea per frame; big, tight type anchored low left; full color fields in a fixed order; Marigold once per frame, usually as the dot that ends a headline; and the creator's name and town as plain information, never a device.</p>
  <div class="cards">{{Q}}</div>
  <div class="cards">{{Q_WEB}}</div>
</div></section>

<section><div class="w">
  <p class="k">Tested and set aside: Route A</p>
  <h2>In their words</h2>
  <p>The creator's own sentence is the graphic element. It is set in Birch caption blocks, like the captions people already read on short video, and every sentence ends on the Marigold dot from the wordmark. The brand looks like people talking.</p>
  <div class="cards">{{A}}</div>
  <div class="cards">{{A_WEB}}</div>
</div></section>

<section><div class="w">
  <p class="k">Tested and set aside: Route B</p>
  <h2>Hometown</h2>
  <p>The creator's town is the graphic element, set big in condensed capitals, the way a jersey carries a city. A season becomes a list of real Maine towns. With no photos, the list itself is the texture.</p>
  <div class="cards">{{B}}</div>
  <div class="cards">{{B_WEB}}</div>
</div></section>

<section><div class="w">
  <p class="k">Against the test</p>
  <h2>How each route scores</h2>
  <table class="checks"><tr><th>Criterion</th><th>Signature</th><th>Route A: In their words</th><th>Route B: Hometown</th></tr>
  <tr><td>1 Signs, does not cover</td><td>Pass. The bug is the only mark on footage.</td><td>Pass. The bug is 26 px in the top corner.</td><td>Pass. Same bug.</td></tr>
  <tr><td>2 Survives the crop</td><td>Pass. Shared avatar.</td><td>Pass. Shared G and dot avatar.</td><td>Pass. Shared avatar.</td></tr>
  <tr><td>3 Carries a person</td><td>Pass. Name and town are the only words on their video.</td><td>Pass. Their sentence is the biggest thing on screen.</td><td>Partial. Their town is the biggest thing; their name comes second.</td></tr>
  <tr><td>4 Neutral</td><td>Pass. No device, no claim.</td><td>Depends on the lines chosen. Needs an editing rule.</td><td>Pass. A town name takes no side.</td></tr>
  <tr><td>5 Both audiences</td><td>Pass. Reads as editorial on Substack, confident on TikTok.</td><td>Strong on TikTok. Needs the dateline on Substack to feel editorial.</td><td>Strong on both. Towns read as local news and as hometown pride.</td></tr>
  <tr><td>6 Stands without photos</td><td>Pass. Type and color fields carry the page.</td><td>Pass. Sentences fill covers and the hero.</td><td>Pass. The list of towns is the texture.</td></tr>
  <tr><td>7 Ownable</td><td>Partial. Owned through consistency over time, not a device. The dot period helps.</td><td>Partial. Caption blocks are common; the dot period helps.</td><td>Pass. A season of Maine town names belongs to this project.</td></tr>
  <tr><td>8 Easy to make</td><td>Pass. One title, one color field, one rule.</td><td>Pass. One text box with a highlight.</td><td>Pass. One text box in one font.</td></tr>
  </table>
  <p class="note" style="margin-top:14px">Recommendation: Signature. Routes A and B both restate the brief, which is what made them feel on the nose. Signature gives up a clever device and wins on restraint, which is also what makes creators comfortable posting it. Its one partial, ownability, comes from using the same rules every time. Caption blocks from Route A stay available inside videos as a content tool, not as the brand.</p>
</div></section>
</body></html>"""


def build_kit(m):
    a, a_web = route_mockups("a", m)
    b, b_web = route_mockups("b", m)
    q, q_web = quiet_mockups(m)
    sg, s_web = sig_mockups(m)
    oc, o_web = offset_mockups(m)
    dm = build_kit_d.build_logos()
    dc, d_web = build_kit_d.mockups(dm, {"inl": inl, "artboard": artboard, "ui_overlay": ui_overlay, "MPI": MPI, "TOWNS": TOWNS, "TOPICS": TOPICS})
    css = CSS
    for k, v in {"{{F800}}": font64("generation-maine/assets/fonts/bricolage-grotesque-800.woff2"),
                 "{{F700}}": font64("brand/v6/fonts-web/bricolage-grotesque-700.woff2"),
                 "{{FCOND}}": font64("brand/v4/fonts-web/bricolage-condensed-800.woff2"),
                 "{{FINTER}}": font64("generation-maine/assets/fonts/inter-var.woff2")}.items():
        css = css.replace(k, v)
    for k, v in C.items():
        css = css.replace("{{%s}}" % k, v)
    html = PAGE.replace("{{DSECTION}}", build_kit_d.SECTION).replace("{{CSS}}", css + build_kit_d.css())
    rep = {"{{WM}}": m["wordmark"], "{{WM_REV}}": m["wordmark-reversed"], "{{ST}}": m["stacked"], "{{ICON_BARE}}": inl(m["icon-bare"]),
           "{{ICON_L}}": m["icon-light"], "{{ICON_M}}": m["icon-marigold"], "{{ENDORSED_REV}}": m["endorsed-reversed"],
           "{{AVATARS}}": avatars(m), "{{OVERLAYS}}": overlays(m), "{{A}}": a, "{{A_WEB}}": a_web, "{{B}}": b, "{{B_WEB}}": b_web, "{{Q}}": "".join(q), "{{Q_WEB}}": q_web,
           "{{PAIRS}}": before_after(q, sg), "{{S_WEB_BEFORE}}": q_web.replace("q-web", "q-web-b").replace("<figcaption>", "<figcaption>Before · "),
           "{{S_WEB}}": s_web.replace("<figcaption>", "<figcaption>After · "), "{{SOVER}}": sig_overlays(m), "{{O}}": "".join(oc), "{{O_WEB}}": o_web, "{{O_SCORE}}": O_SCORE, "{{D}}": "".join(dc), "{{D_WEB}}": d_web}
    for k, v in rep.items():
        html = html.replace(k, v)
    write(OUT + "/kit.html", html)


if __name__ == "__main__":
    logos = build_logos()
    build_kit(logos)
    print("kit written; contrast Marigold on Spruce %.2f, Ink on Birch %.2f" % (ratio(C["marigold"], C["spruce"]), ratio(C["ink"], C["birch"])))
