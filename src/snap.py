# -*- coding: utf-8 -*-
"""The reduced route page on 'Reading a route page' is a picture of the real
page, taken from the rendered PDF, so it can never disagree with page ra05.
Crops to the 175 x 236 mm live area. Run after render.py; the fitter and a
second render then pick it up."""
import os
import sys

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
MM = 72.0 / 25.4

import build  # noqa: E402


def main():
    build.numbers()
    pno = build.K.PAGENO["ra05"] - 1
    pdf = build.pdf_path("A4")
    doc = pymupdf.open(pdf)
    page = doc[pno]
    mx, my = (210 - 175) / 2 * MM, (297 - 236) / 2 * MM
    clip = pymupdf.Rect(mx, my, mx + 175 * MM, my + 236 * MM)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.thumbnail((1400, 1900), Image.LANCZOS)
    out = os.path.join(ROOT, "assets", "photos", "snap-ra05.jpg")
    img.save(out, "JPEG", quality=90)
    print("snap from page", pno + 1, img.size)


if __name__ == "__main__":
    main()
