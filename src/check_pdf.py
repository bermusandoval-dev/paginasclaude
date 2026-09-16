# -*- coding: utf-8 -*-
"""Audit the rendered PDF for faults that raise no error anywhere.

1. Fonts: every face must be an embedded Type0 Garamond or Georgia. A glyph
   the subset lacks falls back to Segoe UI or Cambria without a word.
2. Side margins: nothing may come within 8 mm of a sheet edge, except the
   full-bleed openers and the dark pages.
3. Page count against the builder's list.
4. Cross-references: every "page NN" must land on the page it names.
"""
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
MM = 72.0 / 25.4
SIDE_SAFE = 8.0 * MM
GOOD = ("Spectral",)
BAD = ("SegoeUI", "ArialMT", "Cambria", "TimesNewRoman", "Arial")

import build  # noqa: E402


def check(paper):
    # XREF is filled in by build.numbers(), which only runs when the book is
    # assembled. Reading build.XREF without calling it compares every
    # cross-reference against an empty dict and reports all of them as
    # unrecorded -- which looks exactly like 29 broken references.
    build.numbers()
    path = build.pdf_path(paper)
    doc = pymupdf.open(path)
    print("=" * 74)
    print(os.path.basename(path), doc.page_count, "pages, %.2f MB"
          % (os.path.getsize(path) / 1048576))
    bad = 0

    if doc.page_count != len(build.PAGES):
        bad += 1
        print("   PAGE COUNT: pdf %d, builder %d" % (doc.page_count, len(build.PAGES)))

    seen, trouble = set(), set()
    for pno in range(doc.page_count):
        for f in doc[pno].get_fonts(full=True):
            seen.add((f[3], f[2]))
            if f[2] == "Type3" or any(b in f[3] for b in BAD):
                trouble.add((f[3], f[2], pno + 1))
    print("\nfonts:")
    for bf, ft in sorted(seen):
        ok = ft in ("Type0", "TrueType") and any(g in bf for g in GOOD)
        print("   %-40s %-8s %s" % (bf, ft, "ok" if ok else "<-- CHECK"))
        if not ok:
            bad += 1
    if trouble:
        bad += 1
        print("   FALLBACK OR TYPE3:", sorted(trouble)[:8])

    print("\nside margins (%.0f mm):" % (SIDE_SAFE / MM))
    bleed = {i for i, p in enumerate(build.PAGES) if p[0] == "hero"}
    worst = []
    for pno in range(doc.page_count):
        if pno in bleed:
            continue
        page = doc[pno]
        pr = page.rect
        for blk in page.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                r = pymupdf.Rect(ln["bbox"])
                m = min(r.x0 - pr.x0, pr.x1 - r.x1, r.y0 - pr.y0, pr.y1 - r.y1)
                if m < SIDE_SAFE:
                    worst.append((round(m / MM, 2), pno + 1,
                                  "".join(s["text"] for s in ln["spans"])[:40]))
    if worst:
        bad += 1
        for m, p, t in sorted(worst)[:8]:
            print("   p%02d %5.2f mm  %s" % (p, m, t.encode("ascii", "replace").decode()))
    else:
        print("   nothing closer than 8 mm to an edge")

    print("\ncross-references:")
    # Whitespace is normalised before matching: a phrase that happens to
    # straddle a line break is still the phrase, and leaving it unnormalised
    # made the checker reject cross-references that were perfectly correct.
    texts = [re.sub(r"\s+", " ", doc[i].get_text()).lower()
             for i in range(doc.page_count)]
    refs = set()
    for i, tx in enumerate(texts):
        for m in re.finditer(r"page\s+(\d{1,2})\b", tx):
            refs.add((i + 1, int(m.group(1))))
    for a, b in sorted(refs):
        want = build.XREF.get(b)
        if want is None:
            print("   p%02d -> page %d  (no expectation recorded)" % (a, b))
            bad += 1
            continue
        ok = want in texts[b - 1]
        print("   p%02d -> page %-2d %s" % (a, b, "ok" if ok else "<-- WRONG (%s)" % want))
        if not ok:
            bad += 1
    doc.close()
    print("\n%s: %d problem group(s)" % (paper, bad))
    return bad


if __name__ == "__main__":
    total = sum(check(p) for p in (sys.argv[1:] or ["A4", "Letter"]))
    sys.exit(1 if total else 0)
