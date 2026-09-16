# -*- coding: utf-8 -*-
"""Download the Higgsfield renders in jobs.json and convert them to JPEG.

The render file name is hf_<time>_<job id>.png; the time is one of the batch
submission stamps, so each is tried in turn. Openers (h*) keep 2400 px on the
long edge because they print across the sheet; everything else is capped at
1700 px. A contact sheet of all of them is written to out/_photos.jpg.
"""
import json
import os
import urllib.error
import urllib.request

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "photos")
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3EwsnulWFHVE3qogFeo0SoaBqmK/hf_20260915_%s_%s.png"
STAMPS = ["222454", "213425", "211656", "211657", "211724", "211755", "211813", "211825"]


def fetch(job, raw):
    for st in STAMPS:
        try:
            urllib.request.urlretrieve(BASE % (st, job), raw)
            return True
        except urllib.error.HTTPError:
            continue
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = json.load(open(os.path.join(HERE, "jobs.json"), encoding="utf-8"))
    total = 0
    for slug, job in jobs.items():
        dest = os.path.join(OUT, slug + ".jpg")
        if not os.path.exists(dest):
            raw = os.path.join(OUT, "_tmp.png")
            if not fetch(job, raw):
                print("  MISSING", slug)
                continue
            img = Image.open(raw).convert("RGB")
            cap = 2400 if slug.startswith("h") else 1700
            if max(img.size) > cap:
                k = cap / max(img.size)
                img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
            img.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
            os.remove(raw)
            print("  %-12s %5dx%-5d" % (slug, img.width, img.height))
        total += os.path.getsize(dest)
    print("total %.1f MB, %d photographs" % (total / 1048576, len(jobs)))

    tw, th, cols = 300, 225, 8
    rows = (len(jobs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), (240, 236, 228))
    d = ImageDraw.Draw(sheet)
    for i, slug in enumerate(jobs):
        p = os.path.join(OUT, slug + ".jpg")
        if not os.path.exists(p):
            continue
        im = Image.open(p)
        im.thumbnail((tw - 6, th - 6))
        x, y = (i % cols) * tw, (i // cols) * (th + 18)
        sheet.paste(im, (x + 3, y + 3))
        d.text((x + 4, y + th + 2), slug, fill=(20, 40, 45))
    sheet.save(os.path.join(ROOT, "out", "_photos.jpg"), "JPEG", quality=85)


if __name__ == "__main__":
    main()
