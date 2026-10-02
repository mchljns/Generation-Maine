"""Find licensed photographs of the four hero settings on Wikimedia Commons, with their licenses and authors, and download
the candidates at 2560 px for a contact sheet. Only CC BY, CC BY-SA, CC0 and public domain files are kept.

  python3 brand/src/fetch_commons.py            # writes brand/content/photos/commons/<subject>-<n>.jpg and candidates.json
"""
import json
import os
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT

OUT = os.path.join(ROOT, "brand", "content", "photos", "commons")
SUBJECTS = {
    "katahdin": ["Mount Katahdin Knife Edge", "Katahdin from Abol Bridge", "Mount Katahdin Baxter State Park"],
    "cadillac": ["Cadillac Mountain summit Acadia", "Cadillac Mountain view Bar Harbor", "Acadia National Park granite coast Otter Cliffs"],
    "oldport": ["Old Port Portland Maine street", "Commercial Street Portland Maine", "Exchange Street Portland Maine"],
    "aroostook": ["Aroostook County potato field", "Presque Isle Maine farmland", "Fort Fairfield potato harvest"],
    "headlight": ["Portland Head Light", "Portland Head Lighthouse Cape Elizabeth", "Portland Head Light Fort Williams Park"],
    "cadillac2": ["Cadillac Mountain sunrise", "Cadillac Mountain summit panorama", "Frenchman Bay from Cadillac Mountain"],
    # the towns the placeholder creators are from, for the smaller slots on the page
    "belfast": ["Belfast Maine Main Street", "Belfast Maine downtown", "Belfast Maine harbor"],
    "skowhegan": ["Skowhegan Maine downtown", "Skowhegan Maine Water Street", "Skowhegan Maine Kennebec"],
    "lewiston": ["Lisbon Street Lewiston Maine", "Lewiston Maine downtown", "Bates Mill Lewiston"],
    "machias": ["Machias Maine Main Street", "Machias Maine downtown", "Machias River Maine"],
    "sanford": ["Sanford Maine downtown", "Sanford Maine Main Street", "Springvale Maine"],
}
MIN_W = int(os.environ.get("GM_MIN_W", "3000"))  # a full-width hero at 1920 by 1080 with room to pan needs the source wider than that
OK = ("cc by", "cc by-sa", "cc0", "public domain", "pd", "cc-by", "cc-by-sa")


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    import time
    for attempt in range(4):
        out = subprocess.run(["curl", "-s", "--max-time", "40", "-A", "GenerationMaine/1.0 (brand research; contact via repo)", url], capture_output=True).stdout
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            time.sleep(2 + attempt * 3)
    return {}


def search(q, n=8):
    r = api(dict(action="query", format="json", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=n,
                 prop="imageinfo", iiprop="url|size|extmetadata|mime", iiurlwidth=2560, iiextmetadatafilter="LicenseShortName|Artist|ImageDescription|Credit"))
    pages = r.get("query", {}).get("pages", {})
    found = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii or ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not any(k in lic.lower() for k in OK) or "nc" in lic.lower() or "nd" in lic.lower():
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < MIN_W or w / max(1, h) < 1.15:
            continue
        # the thumbnail host is not reachable from here; upload.wikimedia.org serves the same paths
        u = (ii.get("thumburl") or ii["url"]).replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/").split("?")[0]
        found.append(dict(title=p["title"], url=u, page=ii.get("descriptionurl"), w=w, h=h, license=lic,
                          artist=md.get("Artist", {}).get("value", ""), credit=md.get("Credit", {}).get("value", "")))
    return found


def build(only=None):
    os.makedirs(OUT, exist_ok=True)
    picks = json.load(open(os.path.join(OUT, "candidates.json"))) if os.path.exists(os.path.join(OUT, "candidates.json")) else {}
    for key, queries in SUBJECTS.items():
        if only and key not in only:
            continue
        seen, cands = set(), []
        for q in queries:
            for c in search(q):
                if c["title"] not in seen:
                    seen.add(c["title"]); cands.append(c)
            if len(cands) >= 6:
                break
        cands = cands[:6]
        for i, c in enumerate(cands):
            dst = os.path.join(OUT, "%s-%d.jpg" % (key, i + 1))
            r = subprocess.run(["curl", "-s", "-L", "--max-time", "120", "-A", "GenerationMaine/1.0 (brand research; contact via repo)", "-o", dst, "-w", "%{http_code}", c["url"]], capture_output=True, text=True)
            c["http"] = r.stdout.strip()
            c["file"] = os.path.relpath(dst, ROOT)
            print(key, i + 1, c.get("http"), c["license"], "%dx%d" % (c["w"], c["h"]), c["title"][:70])
        picks[key] = cands
    with open(os.path.join(OUT, "candidates.json"), "w") as fh:
        json.dump(picks, fh, indent=1)


if __name__ == "__main__":
    build(sys.argv[1:] or None)
