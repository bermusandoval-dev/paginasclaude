# -*- coding: utf-8 -*-
"""Drawings computed from the route data. Nothing here is typed by hand:
every chip, count and seam comes from routes.build()."""
import arcs as A
import kit as K
import routes as R

POSCLS = ["a1", "a2", "a3"]


def pos_of(route, arc):
    return route["order"].index(arc)


# ------------------------------------------------------------------ strip ---
def strip(route, per_row=32, chip=17.0, gap=3.0, show_cut=True):
    """Every session of every arc on the route, in route order. Kept sessions
    are tinted by arc position; repeats and folded endings are dashed outlines;
    a rust rule marks each seam. Week numbers run under the kept sessions."""
    items = route["items"] if show_cut else route["kept"]
    W = per_row * (chip + gap) - gap
    rowh = chip + 14
    rows = (len(items) + per_row - 1) // per_row
    H = rows * rowh - 4
    out = []
    week = 0
    seam_firsts = {s["first"]["n"] for s in route["seams"]}
    for i, it in enumerate(items):
        r, c = divmod(i, per_row)
        x, y = c * (chip + gap), r * rowh
        p = pos_of(route, it["arc"])
        col, tint = K.POS[p]
        if it["status"] == "keep":
            week += 1
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{chip}" height="{chip}" rx="1.6" '
                       f'fill="{K.POS_FILL[p]}" fill-opacity="0.78" stroke="{col}" stroke-width="0.9"/>')
            if week == 1 or week % 10 == 0:
                out.append(f'<text x="{x + chip / 2:.1f}" y="{y + chip + 10.5:.1f}" text-anchor="middle" '
                           f'font-size="8" fill="{K.INK2}" font-family="Spectral">{week}</text>')
            if it["n"] in seam_firsts:
                out.append(f'<rect x="{x - gap / 2 - 1.1:.1f}" y="{y - 2:.1f}" width="2.2" height="{chip + 4}" '
                           f'fill="{K.RUST}"/>')
        else:
            out.append(f'<rect x="{x + 0.5:.1f}" y="{y + 0.5:.1f}" width="{chip - 1}" height="{chip - 1}" rx="1.6" '
                       f'fill="none" stroke="{K.INK3}" stroke-width="0.8" stroke-dasharray="2 1.6"/>')
            if it["status"] == "close":
                out.append(f'<path d="M{x + 5:.1f},{y + chip / 2:.1f} L{x + chip - 5:.1f},{y + chip / 2:.1f}" '
                           f'stroke="{K.INK3}" stroke-width="0.9"/>')
            else:
                out.append(f'<path d="M{x + 5.5:.1f},{y + 5.5:.1f} L{x + chip - 5.5:.1f},{y + chip - 5.5:.1f} '
                           f'M{x + chip - 5.5:.1f},{y + 5.5:.1f} L{x + 5.5:.1f},{y + chip - 5.5:.1f}" '
                           f'stroke="{K.INK3}" stroke-width="0.9"/>')
    return (f'<svg class="fig" viewBox="-3 -3 {W + 6:.1f} {H + 6:.1f}">' + "".join(out) + "</svg>")


def strip_key():
    return ('<div class="keyrow">'
            f'<span class="kk">{K.swatch("a1")}First arc</span>'
            f'<span class="kk">{K.swatch("a2")}Second arc</span>'
            f'<span class="kk">{K.swatch("a3")}Third arc</span>'
            f'<span class="kk">{K.swatch("seam")}Seam</span>'
            '<span class="kk"><svg width="12" height="12" viewBox="0 0 12 12"><rect x="1" y="1" width="10" height="10" rx="1.4" fill="none" stroke="#9AA4A2" stroke-dasharray="2 1.6"/><path d="M4,4 L8,8 M8,4 L4,8" stroke="#9AA4A2"/></svg>Repeat, cut</span>'
            '<span class="kk"><svg width="12" height="12" viewBox="0 0 12 12"><rect x="1" y="1" width="10" height="10" rx="1.4" fill="none" stroke="#9AA4A2" stroke-dasharray="2 1.6"/><path d="M3.5,6 L8.5,6" stroke="#9AA4A2"/></svg>Ending, folded</span>'
            '<span class="kk">Numbers: week</span></div>')


# ------------------------------------------------------------ order line ---
def orderline(route):
    cells = []
    for i, k in enumerate(route["order"]):
        a = A.BY_KEY[k]
        v = route["by_arc"][k]
        cut = []
        if v["repeat"]:
            cut.append("%d repeat%s" % (v["repeat"], "" if v["repeat"] == 1 else "s"))
        if v["close"]:
            cut.append("ending folded")
        ct = "%d of %d kept" % (v["kept"], v["total"]) + (" &middot; " + ", ".join(cut) if cut else "")
        if i:
            s = route["seams"][i - 1]
            rule = R.RULE[s["rule"]]
            cells.append(f'<div class="join">Rule {rule["n"]}<br>{K.arrow(w=18)}<br>wk {s["week"]}</div>')
        cells.append(f'<div class="arc {POSCLS[i]}"><div class="k">Arc {i + 1} &middot; '
                     f'S{a["start"]:03d}&ndash;S{a["start"] + len(a["sessions"]) - 1:03d}</div>'
                     f'<div class="nm">{a["name"]}</div><div class="ct">{ct}</div></div>')
    return '<div class="orderline">' + "".join(cells) + "</div>"


# ---------------------------------------------------------------- ladder ---
def ladder(highlight=None, compact=False):
    """The eight layers, top to bottom, with the arcs on each. When a route is
    given, its arcs are marked with their position number and the rest fade."""
    rows = []
    for li, (label, keys) in enumerate(R.LADDER_ROWS, 1):
        pills = []
        for k in keys:
            a = A.BY_KEY[k]
            if highlight:
                if k in highlight["order"]:
                    p = highlight["order"].index(k)
                    col, tint = K.POS[p]
                    pills.append(f'<span style="display:inline-flex;align-items:center;gap:5px;background:{tint};'
                                 f'border:0.8px solid {col};padding:1px 7px 1px 2px;margin:1px 5px 1px 0;font-weight:600">'
                                 f'<span class="dot" style="width:14px;height:14px;flex-basis:14px;font-size:8px;background:{col}">{p + 1}</span>'
                                 f'{a["short"]}</span>')
                else:
                    pills.append(f'<span style="color:{K.INK3};margin-right:9px">{a["short"]}</span>')
            else:
                pills.append(f'<span style="display:inline-block;border:0.8px solid {K.INK3};background:{K.CARD};'
                             f'padding:1px 8px;margin:2px 6px 2px 0">{a["short"]}</span>')
        fs = "11px" if compact else "12.4px"
        pad = "1.5px" if compact else "9px"
        rows.append(f'<div style="display:grid;grid-template-columns:{"84px" if compact else "118px"} 1fr;'
                    f'gap:10px;align-items:center;padding:{pad} 0;border-bottom:0.8px solid {K.RULE};font-size:{fs}">'
                    f'<span style="font-size:7.4px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;'
                    f'color:{K.INK2}">{li:02d} &middot; {label}</span><span>{"".join(pills)}</span></div>')
    return "<div>" + "".join(rows) + "</div>"


# ------------------------------------------------------------- stack bars ---
def stack_vs_route(route):
    """Two bars: the arcs stacked exactly as written, and the same arcs as a
    route. Segment widths are session counts on one shared scale."""
    W, bh = 640.0, 30.0
    total = route["total"]
    k = W / total
    out = []
    # stacked as written
    x = 0.0
    y1 = 18
    for i, a in enumerate(route["order"]):
        col, tint = K.POS[i]
        for n, t, m in A.sessions(a):
            it = next(it for it in route["items"] if it["n"] == n)
            fill = tint
            out.append(f'<rect x="{x:.2f}" y="{y1}" width="{k:.2f}" height="{bh}" fill="{fill}" '
                       f'stroke="{col}" stroke-width="0.35"/>')
            if it["status"] != "keep":
                out.append(f'<rect x="{x:.2f}" y="{y1}" width="{k:.2f}" height="{bh}" fill="{K.INK2}" opacity="0.55"/>')
            x += k
    out.append(f'<text x="0" y="11" font-size="10" fill="{K.INK}" font-family="Spectral" font-weight="600" '
               f'letter-spacing="1.2">STACKED AS WRITTEN &#183; {total} SESSIONS</text>')
    # as a route
    y2 = y1 + bh + 34
    x = 0.0
    kept = route["kept"]
    for it in kept:
        p = route["order"].index(it["arc"])
        col, tint = K.POS[p]
        out.append(f'<rect x="{x:.2f}" y="{y2}" width="{k:.2f}" height="{bh}" fill="{K.POS_FILL[p]}" fill-opacity="0.78" stroke="{col}" stroke-width="0.35"/>')
        x += k
    for s in route["seams"]:
        sx = (s["week"] - 1) * k
        out.append(f'<rect x="{sx - 1.2:.2f}" y="{y2 - 4}" width="2.4" height="{bh + 8}" fill="{K.RUST}"/>')
    out.append(f'<text x="0" y="{y2 - 7}" font-size="10" fill="{K.INK}" font-family="Spectral" font-weight="600" '
               f'letter-spacing="1.2">AS A ROUTE &#183; {route["length"]} SESSIONS</text>')
    H = y2 + bh + 4
    return f'<svg class="fig" viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>"


# ----------------------------------------------------------- override ----
def override_fig(route, borrow_arc):
    """The first twelve weeks of a route, and the one session borrowed from a
    later arc into week two."""
    first = A.sessions(borrow_arc)[0]
    kept = route["kept"][:12]
    chipw, gap = 46.0, 5.0
    W = 13 * (chipw + gap)
    out = []
    y = 40
    col0, tint0 = K.POS[0]
    bp = route["order"].index(borrow_arc)
    colb, tintb = K.POS[bp]
    seqn = [kept[0], None] + kept[1:11]
    for i, it in enumerate(seqn):
        x = i * (chipw + gap)
        if it is None:
            out.append(f'<rect x="{x}" y="{y}" width="{chipw}" height="36" rx="2" fill="{K.POS_FILL[bp]}" fill-opacity="0.45" stroke="{colb}" stroke-width="1.1"/>'
                       f'<text x="{x + chipw / 2}" y="{y + 16}" text-anchor="middle" font-size="10.5" font-weight="600" '
                       f'fill="{K.INK}" font-family="Spectral">S{first[0]:03d}</text>'
                       f'<text x="{x + chipw / 2}" y="{y + 29}" text-anchor="middle" font-size="8.5" fill="{K.INK2}" '
                       f'font-family="Spectral">wk 2</text>')
            continue
        out.append(f'<rect x="{x}" y="{y}" width="{chipw}" height="36" rx="2" fill="{tint0}" stroke="{col0}" stroke-width="0.8"/>'
                   f'<text x="{x + chipw / 2}" y="{y + 16}" text-anchor="middle" font-size="10.5" font-weight="600" '
                   f'fill="{K.INK}" font-family="Spectral">S{it["n"]:03d}</text>'
                   f'<text x="{x + chipw / 2}" y="{y + 29}" text-anchor="middle" font-size="8.5" fill="{K.INK2}" '
                   f'font-family="Spectral">wk {i + 1}</text>')
    # arc from its home position (drawn at the far right as a ghost)
    gx = 12 * (chipw + gap)
    out.append(f'<rect x="{gx}" y="{y}" width="{chipw}" height="36" rx="2" fill="none" stroke="{K.INK3}" '
               f'stroke-dasharray="3 2"/>'
               f'<text x="{gx + chipw / 2}" y="{y + 22}" text-anchor="middle" font-size="9" fill="{K.INK3}" '
               f'font-family="Spectral">wk {next(s["week"] for s in route["seams"] if s["to"] == borrow_arc)}</text>')
    x2 = 1 * (chipw + gap) + chipw / 2
    out.append(f'<path d="M{gx + chipw / 2},{y - 3} C{gx - 60},{y - 40} {x2 + 60},{y - 40} {x2},{y - 4}" fill="none" '
               f'stroke="{K.RUST}" stroke-width="1.3"/>'
               f'<path d="M{x2 - 5},{y - 11} L{x2},{y - 3} L{x2 + 6},{y - 10}" fill="none" stroke="{K.RUST}" stroke-width="1.3"/>')
    return f'<svg class="fig" viewBox="-4 -4 {W + 8} {y + 44}">' + "".join(out) + "</svg>"


# ---------------------------------------------------------------- tables ---
def module_matrix():
    keys = A.COMBINABLE
    head = "<th>Shared skill</th>" + "".join(
        f'<th class="c" style="padding-right:0">{k}</th>' for k in keys) + '<th class="c">Arcs</th>'
    rows = []
    for m, name in A.MODULES.items():
        cells = []
        cnt = 0
        for k in keys:
            hit = next((n for n, t, mm in A.sessions(k) if mm == m), None)
            if hit:
                cnt += 1
                cells.append(f'<td class="c" style="padding:5px 0;font-size:9.4px;color:{K.INK};white-space:nowrap">'
                             f'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:{K.INK};'
                             f'vertical-align:1px;margin-right:2px"></span>{hit}</td>')
            else:
                cells.append('<td class="c" style="padding:4px 0"></td>')
        rows.append(f'<tr><td class="lead" style="white-space:nowrap;padding:5px 8px 5px 0">{name}</td>'
                    + "".join(cells) + f'<td class="c" style="padding:4px 0">{cnt}</td></tr>')
    return f'<table class="tbl" style="font-size:11.4px">' \
           f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


ATLAS_TINT = {0: "#FFFCF6", 1: "#EEF1EE", 2: "#DCE3E1", 3: "#C4D0CE", 4: "#A6B6B4"}


def atlas():
    keys = A.COMBINABLE
    head = '<th style="width:118px"></th>' + "".join(
        f'<th class="c" style="padding:0 0 5px;font-size:7.2px;letter-spacing:0.08em">{k}</th>' for k in keys)
    rows = []
    for a in keys:
        cells = []
        for b in keys:
            if a == b:
                cells.append(f'<td class="c" style="background:{K.INK};color:#FBF7EF;font-size:9.6px;padding:0">'
                             f'{len(A.sessions(a))}</td>')
            else:
                v = A.overlap(a, b)
                col = K.INK if v >= 3 else K.INK2
                cells.append(f'<td class="c" style="background:{ATLAS_TINT[v]};color:{col};padding:0;font-size:12px;'
                             f'font-weight:{600 if v >= 3 else 400};border:0.8px solid #FBF7EF">{v if v else "&middot;"}</td>')
        rows.append(f'<tr style="height:41px"><td style="padding:0 8px 0 0;font-size:11.4px;line-height:1.15;border-bottom:0.8px solid #E3DACB">'
                    f'<b style="font-size:7.4px;letter-spacing:0.1em;color:{K.INK2};display:block">{a}</b>'
                    f'{A.BY_KEY[a]["short"]}</td>' + "".join(cells) + "</tr>")
    return (f'<table class="tbl atlas" style="table-layout:fixed">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')


def finder(route_nums):
    """Upper triangle: the route number for each pair in the book."""
    keys = A.COMBINABLE
    head = '<th style="width:118px"></th>' + "".join(
        f'<th class="c" style="padding:0 0 5px;font-size:7.2px;letter-spacing:0.08em">{k}</th>' for k in keys)
    rows = []
    for i, a in enumerate(keys):
        cells = []
        for j, b in enumerate(keys):
            if j <= i:
                cells.append('<td style="padding:0;border:none"></td>')
                continue
            n = route_nums.get(frozenset((a, b)))
            if n:
                cells.append(f'<td class="c" style="background:{K.INK};color:#FBF7EF;font-weight:600;padding:0;'
                             f'border:1px solid #FBF7EF;font-size:11.4px">{n:02d}</td>')
            else:
                cells.append(f'<td class="c" style="background:#F4EEE3;color:{K.INK3};padding:0;border:1px solid #FBF7EF;'
                             f'font-size:9px">{A.overlap(a, b)}</td>')
        rows.append(f'<tr style="height:22px"><td style="padding:0 8px 0 0;font-size:11.2px;border-bottom:0.8px solid #E3DACB">'
                    f'<b style="font-size:7.4px;letter-spacing:0.1em;color:{K.INK2}">{a}</b> {A.BY_KEY[a]["short"]}</td>'
                    + "".join(cells) + "</tr>")
    return (f'<table class="tbl atlas" style="table-layout:fixed">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')
