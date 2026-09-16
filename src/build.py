# -*- coding: utf-8 -*-
"""Assemble The Combined Routes into one HTML file per paper size.

A 175 x 236 mm content block, centred, identical on A4 and US Letter. Page
numbers are handed out before any page renders, so every reference goes
through kit.pg()."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import content_front as C  # noqa: E402
import content_routes as CR  # noqa: E402
import kit as K  # noqa: E402
import routes_text as T  # noqa: E402

LIVE_W, LIVE_H = 175.0, 236.0
PAPERS = {"A4": (210.0, 297.0), "Letter": (215.9, 279.4)}
TITLE = "The Combined Routes"
P1, P2 = "Part One &middot; The method", "Part Two &middot; The Overlap Atlas"

PAGES = [
    ("hero", C.p_cover, None, None),
    ("std", C.p_fits, "Start here", "Where this book sits"),
    ("std", C.p_contents, "Start here", "Contents"),
    ("std", C.p_problem, "Start here", "One client, three arcs"),
    ("std", C.p_build, "Start here", "How a route is built"),
    ("hero", C.p_op1, None, None),
    ("std", C.p_choose, P1, "Choosing the route"),
    ("std", C.p_rules1, P1, "Rules one to four"),
    ("std", C.p_rules2, P1, "Rules five to seven"),
    ("std", C.p_override, P1, "The override"),
    ("std", C.p_modules, P1, "Shared skills"),
    ("std", C.p_cut, P1, "Cutting a repeat"),
    ("std", C.p_seams, P1, "Seams"),
    ("std", C.p_talk, P1, "The order conversation"),
    ("std", C.p_reading, P1, "Reading a route page"),
    ("std", C.p_stop, P1, "When it stops fitting"),
    ("hero", C.p_op2, None, None),
    ("std", C.p_atlas, P2, "The atlas"),
    ("std", C.p_atlas_read, P2, "Reading the atlas"),
    ("std", C.p_own, P2, "Building your own"),
    ("std", C.p_finder, P2, "Route finder"),
    ("hero", C.p_op3, None, None),
]
for _fn, _r in CR.pages():
    _fam = T.FAMILIES[_r["family"]][0]
    _side = "Explained" if _fn.__name__.startswith("ra") else "Running order"
    PAGES.append(("std", _fn, "Route %02d &middot; %s" % (_r["num"], _fam), _side))
PAGES += [
    ("work", C.p_sheet1, "Sheet 1", "Route builder"),
    ("work", C.p_sheet2, "Sheet 2", "Seam planner"),
    ("std", C.p_scope, "Scope", "Referral and sources"),
    ("hero", C.p_back, None, None),
]


XREF_PHRASES = {
    "p_override": "the first visible win",
    "p_rules1": "the layer ladder",
    "p_talk": "the order conversation",
    "p_stop": "stops fitting",
    "p_modules": "the fifteen shared skills",
    "ra05": "sleep + depression + anxiety",
    "p_reading": "reading a route page",
    "p_sheet2": "seam planner",
}
XREF = {}


def numbers():
    K.PAGENO.clear()
    for i, (_k, fn, _l, _r) in enumerate(PAGES, 1):
        K.PAGENO[fn.__name__] = i
    XREF.clear()
    for name, phrase in XREF_PHRASES.items():
        XREF[K.PAGENO[name]] = phrase


def render_pages():
    numbers()
    return [(k, fn(), hl, hr) for k, fn, hl, hr in PAGES]


def page_html(kind, inner, hl, hr, num):
    if kind == "hero":
        return f'<div class="sheet bleed"><div class="page">{inner}</div></div>'
    foot = f'<span>&copy; Sando LLC &middot; {TITLE}</span>'
    return f"""<div class="sheet"><div class="page">
<header class="ph"><span>{hl}</span><span class="r">{hr}</span></header>
<div class="body">{inner}</div>
<footer class="pf">{foot}<span class="n">{num}</span></footer>
</div></div>"""


def build(paper, pages=None):
    pw, ph = PAPERS[paper]
    mx = round((pw - LIVE_W) / 2, 3)
    my = round((ph - LIVE_H) / 2, 3)
    fonts = open(os.path.join(ROOT, "fonts", "fonts.css"), encoding="utf-8").read()
    style = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    geom = f"""
@page {{ size: {pw}mm {ph}mm; margin: 0; }}
.sheet {{ width: {pw}mm; height: {ph}mm; padding: {my}mm {mx}mm; overflow: hidden; }}
.page {{ width: {LIVE_W}mm; height: {LIVE_H}mm; }}
"""
    if pages is None:
        pages = render_pages()
    body = [page_html(k, inner, hl, hr, i) for i, (k, inner, hl, hr) in enumerate(pages, 1)]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{TITLE} &mdash; {paper}</title>
<style>{fonts}</style>
<style>{style}</style>
<style>{geom}</style>
</head><body>
{''.join(body)}
</body></html>"""


def main():
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    for paper in PAPERS:
        html = build(paper)
        if html.count("<div") != html.count("</div>"):
            raise SystemExit("unbalanced divs in %s: %d open, %d close"
                             % (paper, html.count("<div"), html.count("</div>")))
        path = os.path.join(ROOT, "out", "routes-%s.html" % paper)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("%-7s %2d pages  %6.1f KB" % (paper, len(PAGES), len(html) / 1024))


if __name__ == "__main__":
    main()
