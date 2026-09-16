# -*- coding: utf-8 -*-
"""Contact sheet of the rendered PDF. Measurements never catch everything: an
unbalanced grid, a caption sitting on a drawing, or a page that is simply ugly
only show up by looking at the sheets."""
import os
import sys

import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sheet(pdf, out, cols=6, tw=330, first=0, last=None):
    doc = pymupdf.open(pdf)
    pages = list(range(first, last if last is not None else doc.page_count))
    r0 = doc[pages[0]].rect
    th = int(tw * r0.height / r0.width)
    rows = (len(pages) + cols - 1) // cols
    lab = 16
    img = Image.new("RGB", (cols * tw, rows * (th + lab)), (222, 216, 202))
    for i, pno in enumerate(pages):
        page = doc[pno]
        k = tw / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(k, k))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((tw, th), Image.LANCZOS)
        img.paste(im, ((i % cols) * tw, (i // cols) * (th + lab) + lab))
    img.save(out, "JPEG", quality=86)
    doc.close()
    print(out, img.size, len(pages), "pages")


if __name__ == "__main__":
    pdf = os.path.join(ROOT, "out", sys.argv[1] if len(sys.argv) > 1 else "Session-Arc-The-Combined-Routes-A4.pdf")
    out = os.path.join(ROOT, "out", sys.argv[2] if len(sys.argv) > 2 else "_sheet.jpg")
    kw = {}
    if len(sys.argv) > 3:
        kw["first"] = int(sys.argv[3])
    if len(sys.argv) > 4:
        kw["last"] = int(sys.argv[4])
    if len(sys.argv) > 5:
        kw["cols"] = int(sys.argv[5])
    if len(sys.argv) > 6:
        kw["tw"] = int(sys.argv[6])
    sheet(pdf, out, **kw)
