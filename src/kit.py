# -*- coding: utf-8 -*-
"""Page furniture. A picture never carries a fixed height unless it is a
photograph; labels live in HTML beside a drawing, not inside it; and every
photograph has a line of type that says what the page is doing."""

PHOTO = "../assets/photos/%s.jpg"
PAGENO = {}

INK, INK2, INK3 = "#173C42", "#6B7D7E", "#9AA4A2"
PAPER, PAPER2, CARD, RULE = "#FBF7EF", "#F4EEE3", "#FFFCF6", "#E3DACB"
RUST, SAGE, PLUM, BLUE, OCHRE = "#B8552F", "#5F7554", "#6F5F80", "#7B91B0", "#D3A44C"
SAGE_T, PLUM_T, BLUE_T, RUST_T = "#ECEEE4", "#EFEBF2", "#EBEFF4", "#F7EBE3"
POS = [(SAGE, SAGE_T), (PLUM, PLUM_T), (BLUE, BLUE_T)]
# the filled chips of a route strip: the light accent of each arc position
POS_FILL = ["#859159", "#9574AD", "#7B91B0"]


def pg(name):
    return PAGENO.get(name, 0)


def photo(slug, h, alt="", pos=None):
    op = f' style="object-position:{pos}"' if pos else ""
    return (f'<div class="photo" style="height:{h}pt">'
            f'<img src="{PHOTO % slug}"{op} alt="{alt}"></div>')


def capt(slug, h, text, pos=None):
    return ('<figure class="pcap">' + photo(slug, h, text, pos)
            + f'<figcaption>{text}</figcaption></figure>')


def figbox(inner, caption=None, cls="", width=None):
    w = f' style="width:{width}%"' if width else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="figbox {cls}"><div class="figw"{w}>{inner}</div>{cap}</figure>'


def legend(items, cols=1, start=1, rust=()):
    c = {1: "", 2: " c2", 3: " c3"}[cols]
    out = []
    for i, (title, body) in enumerate(items, start):
        r = " r" if i in rust else ""
        out.append(f'<li><span class="dot{r}">{i}</span><span><b>{title}</b>{body}</span></li>')
    return f'<ul class="legend{c}">' + "".join(out) + "</ul>"


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><div>{t}</div></li>" for t in items) + "</ol>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li><span>{t}</span></li>" for t in items) + "</ul>"


def table(head, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="tbl {cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def card(inner, cls=""):
    return f'<div class="card {cls}">{inner}</div>'


def seq(items, h=150, start=1):
    cells = []
    for i, (slug, title, why) in enumerate(items, start):
        cells.append(
            f'<figure class="sc"><div class="shot" style="height:{h}pt">'
            f'<img src="{PHOTO % slug}" alt="{title}"><span class="tagn">Step {i}</span></div>'
            f'<h4>{title}</h4><p class="why">{why}</p></figure>')
    return f'<div class="seq n{len(items)}">' + "".join(cells) + "</div>"


def stat(v, label):
    return f'<div class="stat"><div class="v">{v}</div><div class="l">{label}</div></div>'


def src(text):
    return f'<p class="src"><b>Sources</b>{text}</p>'


def arrow(direction="right", w=13):
    if direction == "down":
        return (f'<svg class="arw" viewBox="0 0 10 14" width="9" height="13"><path d="M5,1 L5,12 M1.5,8.5 L5,12 '
                f'L8.5,8.5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
    return (f'<svg class="arw" viewBox="0 0 14 10" width="{w}" height="9"><path d="M1,5 L12,5 M8,1.5 L12,5 '
            f'L8,8.5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')


def swatch(cls):
    return f'<span class="sw {cls}"></span>'
