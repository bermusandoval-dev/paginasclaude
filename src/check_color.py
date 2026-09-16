# -*- coding: utf-8 -*-
"""The colour budget: how much of the book is saturated colour.

Every page is rasterized at 90 dpi and converted to CIE Lab. A pixel counts as
saturated when its chroma C* = sqrt(a*^2 + b*^2) is 18 or more, and it is not
near black or near white (L* between 18 and 94). On that scale the ink
#173C42 is C* 13, the grey #6B7D7E is 7 and every tint is under 10, so they are
neutral; every accent counts, down to the slate blue #7B91B0 at 19 and the
sage #5F7554 at 22 (rust #B8552F is 55).

Target from the brief: about 2.1% of the whole visual area.
"""
import os
import sys

import numpy as np
import pymupdf
from skimage.color import rgb2lab

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
C_MIN, L_LO, L_HI = 18.0, 18.0, 94.0

import build  # noqa: E402


def main(paper="A4"):
    pdf = build.pdf_path(paper)
    doc = pymupdf.open(pdf)
    tot_px, tot_sat, rows = 0, 0, []
    for p in doc:
        pix = p.get_pixmap(dpi=90)
        rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        lab = rgb2lab(rgb / 255.0)
        c = np.hypot(lab[:, :, 1], lab[:, :, 2])
        sat = (c >= C_MIN) & (lab[:, :, 0] > L_LO) & (lab[:, :, 0] < L_HI)
        n, s = sat.size, int(sat.sum())
        tot_px += n
        tot_sat += s
        rows.append((p.number + 1, 100.0 * s / n))
    doc.close()
    print("saturated area, whole book: %.2f%%  (target about 2.1%%)" % (100.0 * tot_sat / tot_px))
    worst = sorted(rows, key=lambda r: -r[1])[:8]
    print("highest pages: " + ", ".join("p%02d %.1f%%" % r for r in worst))
    return 100.0 * tot_sat / tot_px


if __name__ == "__main__":
    main(*(sys.argv[1:] or []))
