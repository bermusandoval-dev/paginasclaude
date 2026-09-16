# -*- coding: utf-8 -*-
"""Assemble a book into one HTML file per paper size.

A 175 x 236 mm content block, centred, identical on A4 and US Letter. Page
numbers are handed out before any page renders, so every reference goes
through kit.pg().

Which book is assembled comes from the BOOK environment variable and defaults
to the first one: `BOOK=checkpoints python make.py`. Everything downstream --
fit, snap, render, finalize, every checker -- reads the book's identity from
here rather than carrying its own copy of the file names.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

BOOK = os.environ.get("BOOK", "routes")
SPEC = importlib.import_module("book_" + BOOK)

import kit as K  # noqa: E402

TITLE, NAME, SLUG, SUBJECT = SPEC.TITLE, SPEC.NAME, SPEC.SLUG, SPEC.SUBJECT
PAGES = SPEC.PAGES
XREF_PHRASES = SPEC.XREF_PHRASES

LIVE_W, LIVE_H = 175.0, 236.0
PAPERS = {"A4": (210.0, 297.0), "Letter": (215.9, 279.4)}
XREF = {}


def html_path(paper):
    return os.path.join(ROOT, "out", "%s-%s.html" % (SLUG, paper))


def pdf_path(paper):
    return os.path.join(ROOT, "out", "%s-%s.pdf" % (NAME, paper))


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
        path = html_path(paper)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("%-7s %2d pages  %6.1f KB" % (paper, len(PAGES), len(html) / 1024))


if __name__ == "__main__":
    main()
