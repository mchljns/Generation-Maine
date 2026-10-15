#!/usr/bin/env python3
"""Zip the WordPress theme for upload: dist/generation-maine.zip (and the copy in generation-maine-dist/).

    python3 brand/src/package_theme.py

Agency-internal notes (PROJECT.md) and local tooling (.wp-env.json) stay out of the zip, and so do two files the theme does
not use: the shell wrapper for the seed script (the README runs bin/seed-creators.php with wp eval-file) and the DM Sans TTF
the brand builders read (the theme loads the WOFF2). Entries are sorted and dated so the same theme always makes the same zip.
"""
import os
import shutil
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP = {".DS_Store", ".wp-env.json", "PROJECT.md", "seed-creators.sh", "dm-sans-var.ttf"}


def main():
    files = sorted(os.path.join(d, f) for d, _, fs in os.walk(os.path.join(ROOT, "generation-maine")) for f in fs if f not in SKIP)
    out = os.path.join(ROOT, "dist", "generation-maine.zip")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(os.path.relpath(f, ROOT), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if f.endswith(".sh") else 0o644) << 16
            with open(f, "rb") as fh:
                z.writestr(info, fh.read())
    os.makedirs(os.path.join(ROOT, "generation-maine-dist"), exist_ok=True)
    shutil.copy(out, os.path.join(ROOT, "generation-maine-dist", "generation-maine.zip"))
    print("%s: %d files, %d bytes" % (os.path.relpath(out, ROOT), len(files), os.path.getsize(out)))


if __name__ == "__main__":
    main()
