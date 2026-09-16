# -*- coding: utf-8 -*-
"""Put every page on an exact paper box, and stamp the metadata. Chrome
quantises the page box (it wrote 209.89 mm for 210), which is what invites a
printer driver to offer "fit to page"."""
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
MM = 72.0 / 25.4
SIZES = {"A4": (210.0, 297.0), "Letter": (215.9, 279.4)}

import build  # noqa: E402


def finalize(paper):
    src = build.pdf_path(paper)
    W, H = SIZES[paper][0] * MM, SIZES[paper][1] * MM
    old = pymupdf.open(src)
    new = pymupdf.open()
    for page in old:
        p = new.new_page(width=W, height=H)
        r = page.rect
        dx, dy = (W - r.width) / 2.0, (H - r.height) / 2.0
        p.show_pdf_page(pymupdf.Rect(dx, dy, dx + r.width, dy + r.height), old, page.number)
    # Deliberately bland metadata: the file name and properties are what shows
    # in a shared downloads folder or a print queue.
    new.set_metadata({
        "title": build.TITLE,
        "author": "Sando LLC",
        "subject": build.SUBJECT,
        "keywords": "",
        "creator": "Sando LLC",
        "producer": "Sando LLC",
    })
    tmp = src + ".tmp"
    new.save(tmp, garbage=4, deflate=True)
    new.close()
    old.close()
    os.replace(tmp, src)
    doc = pymupdf.open(src)
    sizes = {(round(p.rect.width / MM, 2), round(p.rect.height / MM, 2)) for p in doc}
    print("%-7s %2d pages  %s mm  %.2f MB" % (paper, doc.page_count, sizes,
                                             os.path.getsize(src) / 1048576))
    doc.close()


if __name__ == "__main__":
    for n in sys.argv[1:] or ["A4", "Letter"]:
        finalize(n)
