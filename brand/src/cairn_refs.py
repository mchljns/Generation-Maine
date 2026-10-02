"""Retry rate-limited reference downloads with long pauses, then lay the cairn references out on a contact sheet with credits.
  python3 brand/src/cairn_refs.py
"""
import json, os, subprocess, time, re
from PIL import Image, ImageDraw
D = "brand/content/photos/cairns"
UA = "GenerationMaine/1.0 (brand research; contact via repo)"
res = json.load(open(os.path.join(D, "refs.json")))
items = [it for its in res.values() for it in its if it.get("file")]
for it in items:
    if it.get("http") != "200":
        for a in range(4):
            time.sleep(10)
            code = subprocess.run(["curl", "-s", "-L", "--max-time", "60", "-A", UA, "-o", it["file"], "-w", "%{http_code}", it["url"]], capture_output=True, text=True).stdout.strip()
            it["http"] = code
            if code == "200":
                break
        print(it["file"], it["http"])
json.dump(res, open(os.path.join(D, "refs.json"), "w"), indent=1)
ok = []
for it in items:
    try:
        im = Image.open(it["file"]).convert("RGB"); ok.append((it, im))
    except Exception:
        pass
cols = 6; W = 400; H = 300
sh = Image.new("RGB", (cols * W, ((len(ok) + cols - 1) // cols) * (H + 40)), "white"); d = ImageDraw.Draw(sh)
with open(os.path.join(D, "REFERENCES.md"), "w") as fh:
    fh.write("# Cairn references, Wikimedia Commons\n\nStudy material only; nothing here is reproduced in the mark.\n\n")
    for n, (it, im) in enumerate(ok):
        im.thumbnail((W - 10, H - 10)); x = (n % cols) * W; y = (n // cols) * (H + 40)
        sh.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        d.text((x + 6, y + H + 4), "%02d %s" % (n + 1, it["title"][5:60]), fill="black")
        d.text((x + 6, y + H + 20), "%s, %s" % (re.sub("<[^>]+>", "", it["artist"])[:40], it["license"]), fill="gray")
        fh.write("- %02d. %s. %s, %s. %s\n" % (n + 1, it["title"], re.sub("<[^>]+>", "", it["artist"]).strip(), it["license"], it["page"]))
sh.save(os.path.join(D, "references.png")); print(len(ok), "references on the sheet")
