# -*- coding: utf-8 -*-
"""Every picture and every drawing, next to the words that claim what it is.

It counts the raw <img> and <svg> tags per page first and refuses to report
unless the itemised list accounts for all of them -- answering "do they all
match?" from a list that is quietly short is the same failure being looked for.
It also names frames that were generated and never used.
"""
import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build  # noqa: E402

TAG = re.compile(r"<[^>]+>")
IMG = re.compile(r'<img src="[^"]*/([^"/]+)\.jpg"')
SVG = re.compile(r'<svg class="(fig|truescale)"')


def clean(s, n=110):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", s or ""))).strip()[:n]


def after(h, pos, limit=460):
    seg = h[pos:pos + limit]
    for pat in (r"<h4[^>]*>(.*?)</h4>\s*<p class=\"why\">(.*?)</p>",
                r"<figcaption>(.*?)</figcaption>",
                r"<div class=\"cap\">(.*?)</div>",
                r"<h4[^>]*>(.*?)</h4>"):
        m = re.search(pat, seg, re.S)
        if m:
            return " | ".join(clean(g, 88) for g in m.groups() if g)
    return ""


def main():
    pages = build.render_pages()
    rows, short = [], []
    for i, (kind, h, hl, hr) in enumerate(pages, 1):
        page = "p%02d" % i
        topic = clean(hr or "", 26) or ("opener" if kind in ("hero", "dark") else "")
        imgs = list(IMG.finditer(h))
        svgs = list(SVG.finditer(h))
        for m in imgs:
            slug = m.group(1)
            before = h[max(0, m.start() - 240):m.start()]
            if 'class="shot"' in before[-170:]:
                k = "STEP"
            elif '<div class="hero">' in before[-260:] or 'class="hero"' in before[-260:]:
                k = "HERO"
            else:
                k = "PHOTO"
            claim = after(h, m.end())
            if not claim:
                seg = h[m.start():h.find(">", m.start()) + 1]
                al = re.search(r'alt="([^"]*)"', seg)
                claim = ("NO CAPTION -- alt says: " + clean(al.group(1), 76)) if al and al.group(1) \
                    else "NO CAPTION, NO ALT"
            rows.append((page, topic, k, slug, claim))
        for m in svgs:
            end = h.find("</svg>", m.start())
            rows.append((page, topic, "FIG", "(%s)" % m.group(1), after(h, end + 6, 320)))
        got = len([r for r in rows if r[0] == page])
        if got != len(imgs) + len(svgs):
            short.append((page, len(imgs) + len(svgs), got))
    if short:
        raise SystemExit("inventory is incomplete: %s" % short)

    print("%-5s %-24s %-6s %-20s %s" % ("page", "topic", "kind", "asset", "what it claims to be"))
    for r in rows:
        print("%-5s %-24s %-6s %-20s %s" % r)
    kinds = {}
    for r in rows:
        kinds[r[2]] = kinds.get(r[2], 0) + 1
    print("\ntotal %d assets, all accounted for  %s" % (len(rows), kinds))

    used = [r[3] for r in rows if r[2] != "FIG"]
    dupes = sorted({s for s in used if used.count(s) > 1})
    print("photographs used more than once: %s" % (dupes or "none"))
    mute = [(r[0], r[3]) for r in rows if r[2] not in ("HERO",) and r[4].startswith("NO CAPTION")]
    print("pictures with nothing printed beside them: %d" % len(mute))
    for pgn, slug in mute:
        print("   %s  %s" % (pgn, slug))
    on_disk = {os.path.basename(f)[:-4] for f in glob.glob(os.path.join(ROOT, "assets", "photos", build.BOOK, "*.jpg"))}
    print("generated but not used: %s" % (sorted(on_disk - set(used)) or "none"))


if __name__ == "__main__":
    main()
