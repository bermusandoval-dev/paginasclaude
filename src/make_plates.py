# -*- coding: utf-8 -*-
"""Rasterise art.py's plates into the files the build expects.

Writes assets/photos/<book>/<slug>.jpg at the same sizes fetch_photos.py would
have written: 2400 px on the long edge for the openers, 1700 px for everything
else. The rest of the pipeline cannot tell the difference, and a real
photograph dropped over any of these files replaces it with no code change.

Chrome does the rasterising because it is already a dependency and it renders
SVG filters -- the drop shadows and the soft window light -- which the pure
Python rasterisers available here do not.
"""
import glob
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
from browser import CHROME, FLAGS  # noqa: E402

import art  # noqa: E402

OUT = os.path.join(ROOT, "assets", "photos", "checkpoints")
TMP = os.path.join(ROOT, "out", "_plates")


def render(slug, fn):
    svg = fn()
    w = int(svg.split('width="')[1].split('"')[0])
    h = int(svg.split('height="')[1].split('"')[0])
    scale = (2400.0 if slug.startswith("h") else 1700.0) / max(w, h)
    pw, ph = int(round(w * scale)), int(round(h * scale))
    src = os.path.join(TMP, slug + ".html")
    png = os.path.join(TMP, slug + ".png")
    with open(src, "w", encoding="utf-8") as fh:
        fh.write("<!doctype html><meta charset=utf-8>"
                 "<style>html,body{margin:0;padding:0;background:#fff}"
                 "svg{display:block;width:100vw;height:100vh}</style>" + svg)
    if os.path.exists(png):
        os.remove(png)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    "--window-size=%d,%d" % (pw, ph),
                    "--screenshot=" + png, *FLAGS,
                    "file:///" + src.replace("\\", "/").lstrip("/")],
                   capture_output=True)
    if not os.path.exists(png):
        raise SystemExit("chrome produced nothing for " + slug)
    img = Image.open(png).convert("RGB")
    dest = os.path.join(OUT, slug + ".jpg")
    img.save(dest, "JPEG", quality=90, optimize=True, progressive=True)
    os.remove(png)
    return img.size, os.path.getsize(dest)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    total = 0
    for slug, fn in art.PLATES.items():
        size, n = render(slug, fn)
        total += n
        print("  %-12s %5dx%-5d %6.0f KB" % (slug, size[0], size[1], n / 1024.0))
    for f in glob.glob(os.path.join(TMP, "*.html")):
        os.remove(f)
    print("%d plates, %.1f MB" % (len(art.PLATES), total / 1048576.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
