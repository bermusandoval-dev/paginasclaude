# -*- coding: utf-8 -*-
"""Drawings computed from the checkpoint data.

Same rule as the first book: nothing here is typed. Every chip, dot, band and
branch arrow comes out of arcs.CHECKPOINT and checkpoints.py, so a chart that
disagrees with the page beside it is a bug the checker can catch rather than a
proofreading job.

The three outlets keep one color each throughout the whole book -- sage for on
track, ochre for stalled, rust for worse -- and nothing else in the book is
allowed those three colors.
"""
import arcs as A
import checkpoints as C
import kit as K

ON, STALL, WORSE = K.SAGE, K.OCHRE, K.RUST
VCOL = {"on": ON, "stalled": STALL, "worse": WORSE}

# The bands on an arc timeline: (colour, opacity). The opacities are the point
# -- below roughly 0.6 these accents wash out to under the chroma the colour
# budget counts, and the page goes grey while the stylesheet still says sage.
BAND = [(K.SAGE_L, 0.80), (K.PLUM_L, 0.80)]


def _svg(inner, x, y, w, h, cls="fig"):
    return (f'<svg class="{cls}" viewBox="{x} {y} {w:.1f} {h:.1f}">'
            + "".join(inner) + "</svg>")


def _t(x, y, s, size=8, fill=None, anchor="middle", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
            f'fill="{fill or K.INK2}" font-family="Spectral"{w}>{s}</text>')


# ------------------------------------------------------------- the arc row ---
# Every timeline is drawn to the same overall width and the same height, so
# the fifteen arc pages have figures of one size. Only the chips change shape:
# a fifteen-session arc gets wide ones, a forty-session arc narrow ones. Scaling
# the whole drawing instead made a short arc's figure two and a half times
# taller than a long arc's, which clipped four pages and told the reader
# nothing.
ROW_W = 446.0


def timeline(key, chip=13.0, gap=2.2):
    """One arc, session by session, with its checkpoints and their branches.

    Checkpoints sit above the row as numbered discs. The branch a stalled
    reading takes is drawn as an arc back (or forward) to the session it lands
    on, which is the only place in the book where that pairing is visible as a
    shape rather than a sentence.
    """
    a = A.BY_KEY[key]
    n = len(a["sessions"])
    cw = (ROW_W + gap) / float(n) - gap        # chip width; the height stays 9
    W = ROW_W
    TOP, BASE = 34.0, 50.0
    cps = {s: (i, A.CHECKPOINT[s]) for i, s, _x, _g in C.schedule(key)}
    branches = {A.CHECKPOINT[s]["stalled"] for s in cps}
    out = []

    def cx(sess):
        return (sess - a["start"]) * (cw + gap) + cw / 2.0

    # Each checkpoint covers the run of sessions up to and including itself.
    # Those runs are banded in the same three accents the first book uses for
    # arc position, at opacities that actually register as colour rather than
    # as a tint: it shows which sessions a reading is about, and it is most of
    # what keeps this book off the page as something other than grey.
    span = {}
    prev = a["start"]
    for i, (_o, sess, _x, _g) in enumerate(C.schedule(key)):
        for m in range(prev, sess + 1):
            span[m] = i
        prev = sess + 1

    for i, (_title, mod) in enumerate(a["sessions"]):
        sess = a["start"] + i
        x = i * (cw + gap)
        if mod == "CLOSE":
            out.append(f'<rect x="{x + 0.4:.1f}" y="{TOP + 0.4:.1f}" width="{cw - 0.8:.1f}" '
                       f'height="{chip - 0.8:.1f}" rx="1.4" fill="none" stroke="{K.INK3}" '
                       f'stroke-width="0.7" stroke-dasharray="1.8 1.4"/>')
            continue
        if sess in cps:
            fill, op = K.INK, 1.0
        elif sess in branches:
            fill, op = STALL, 1.0
        elif sess in span:
            fill, op = BAND[span[sess] % len(BAND)]
        else:
            fill, op = K.RULE, 1.0
        out.append(f'<rect x="{x:.1f}" y="{TOP:.1f}" width="{cw:.1f}" height="{chip}" rx="1.4" '
                   f'fill="{fill}" fill-opacity="{op:.2f}"/>')

    # the branch each stalled reading takes
    for sess, (_ordn, cp) in cps.items():
        x0, x1 = cx(sess), cx(cp["stalled"])
        dip = BASE + 9 + min(9.0, abs(x1 - x0) * 0.09)
        out.append(f'<path d="M{x0:.1f},{BASE:.1f} C{x0:.1f},{dip:.1f} {x1:.1f},{dip:.1f} '
                   f'{x1:.1f},{BASE + 2.4:.1f}" fill="none" stroke="{STALL}" '
                   f'stroke-width="0.9" stroke-dasharray="2.4 1.8"/>')
        d = 1 if x1 > x0 else -1
        out.append(f'<path d="M{x1 - 2.1 * d:.1f},{BASE + 5.4:.1f} L{x1:.1f},{BASE + 1.8:.1f} '
                   f'L{x1 + 2.1 * d:.1f},{BASE + 5.4:.1f}" fill="none" stroke="{STALL}" '
                   f'stroke-width="0.9"/>')

    # the numbered disc above each checkpoint
    for sess, (ordn, _cp) in cps.items():
        x = cx(sess)
        out.append(f'<path d="M{x:.1f},{TOP - 2:.1f} L{x:.1f},{TOP - 9:.1f}" stroke="{K.INK}" '
                   f'stroke-width="0.9"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{TOP - 15:.1f}" r="6.2" fill="{ON}"/>')
        out.append(_t(x, TOP - 12.2, ordn, 8.2, K.PAPER, weight="600"))
        out.append(_t(x, TOP - 23, "S%03d" % sess, 6.6, K.INK2))
    return _svg(out, -8, 0, W + 16, BASE + 24)


def timeline_key():
    return ('<div class="keyrow">'
            '<span class="kk"><i class="sw ink"></i>Checkpoint</span>'
            '<span class="kk"><i class="sw st"></i>Where a stall branches to</span>'
            '<span class="kk"><i class="sw b1"></i><i class="sw b2"></i>'
            'The sessions each reading covers</span>'
            '<span class="kk"><i class="sw cut"></i>The arc&rsquo;s own ending</span>'
            "</div>")


# ------------------------------------------------------------- the chart -----
def chart(key, w=210.0, h=96.0, label=True):
    """The worked case: baseline, then one dot per checkpoint, on the 0-10 goal
    scale. Dot color is the verdict, computed, never chosen."""
    _who, base, rows, _out = C.case(key)
    pts = [(0, base, None)] + [(i, r, v) for i, (_o, _n, r, v, _w) in enumerate(rows, 1)]
    live = [(i, r, v) for i, r, v in pts if r is not None]
    n = len(pts) - 1
    # Top padding has to clear the value printed ABOVE a dot, and a reading of
    # 10 sits on the ceiling; right padding has to clear the widest x label.
    L, R, T, B = 22.0, 26.0, 15.0, 16.0
    pw, ph = w - L - R, h - T - B

    def X(i):
        return L + (pw * i / float(n))

    def Y(v):
        return T + ph * (1 - v / 10.0)

    out = [f'<rect x="{L:.1f}" y="{Y(10):.1f}" width="{pw:.1f}" height="{Y(7) - Y(10):.1f}" '
           f'fill="{ON}" fill-opacity="0.10"/>']
    for v in (0, 5, 10):
        out.append(f'<path d="M{L:.1f},{Y(v):.1f} L{L + pw:.1f},{Y(v):.1f}" stroke="{K.RULE}" '
                   f'stroke-width="0.7"/>')
        out.append(_t(L - 4, Y(v) + 2.6, v, 7.4, K.INK3, "end"))
    out.append(_t(L + pw + 3, Y(8.5) + 2.4, "target", 6.4, K.INK3, "start"))

    d = " ".join(("M" if j == 0 else "L") + "%.1f,%.1f" % (X(i), Y(r))
                 for j, (i, r, _v) in enumerate(live))
    out.append(f'<path d="{d}" fill="none" stroke="{K.INK2}" stroke-width="1.3"/>')
    for i, r, v in pts:
        if r is None:
            out.append(f'<circle cx="{X(i):.1f}" cy="{T + ph / 2:.1f}" r="2.6" fill="none" '
                       f'stroke="{K.INK3}" stroke-width="0.8" stroke-dasharray="1.6 1.4"/>')
            out.append(_t(X(i), h - 5, "not read", 6.4, K.INK3))
            continue
        col = VCOL.get(v, K.INK2)
        out.append(f'<circle cx="{X(i):.1f}" cy="{Y(r):.1f}" r="3.6" fill="{col}"/>')
        out.append(_t(X(i), Y(r) - 6.2, r, 7.6, K.INK, weight="600"))
        if label:
            out.append(_t(X(i), h - 5, "base" if i == 0 else str(i), 6.8, K.INK3))
    return _svg(out, 0, 0, w, h)


def blankchart(w=300.0, h=104.0, cols=5):
    """The plotting grid with nothing plotted on it.

    The worksheet used chart("REL") with its labels switched off, which drew a
    photocopiable sheet carrying one worked case's readings. A blank sheet has
    to actually be blank.
    """
    L, R, T, B = 22.0, 26.0, 15.0, 16.0
    pw, ph = w - L - R, h - T - B
    X = lambda i: L + pw * i / float(cols)
    Y = lambda v: T + ph * (1 - v / 10.0)
    out = [f'<rect x="{L:.1f}" y="{Y(10):.1f}" width="{pw:.1f}" height="{Y(7) - Y(10):.1f}" '
           f'fill="{ON}" fill-opacity="0.10"/>']
    for v in range(0, 11):
        big = v in (0, 5, 10)
        out.append(f'<path d="M{L:.1f},{Y(v):.1f} L{L + pw:.1f},{Y(v):.1f}" '
                   f'stroke="{K.RULE}" stroke-width="{0.7 if big else 0.4}"/>')
        if big:
            out.append(_t(L - 4, Y(v) + 2.6, v, 7.4, K.INK3, "end"))
    out.append(_t(L + pw + 3, Y(8.5) + 2.4, "target", 6.4, K.INK3, "start"))
    for i in range(cols + 1):
        out.append(f'<path d="M{X(i):.1f},{T:.1f} L{X(i):.1f},{T + ph:.1f}" '
                   f'stroke="{K.RULE}" stroke-width="0.5"/>')
        out.append(_t(X(i), h - 5, "base" if i == 0 else str(i), 6.8, K.INK3))
    return _svg(out, 0, 0, w, h)


def chart_key():
    return ('<div class="keyrow">'
            f'<span class="kk"><i class="sw" style="background:{ON}"></i>On track</span>'
            f'<span class="kk"><i class="sw" style="background:{STALL}"></i>Stalled</span>'
            f'<span class="kk"><i class="sw" style="background:{WORSE}"></i>Worse</span>'
            "</div>")


def shape(kind, w=96.0, h=62.0):
    """One of the three shapes, drawn small, for the pages that teach them."""
    series = {"on": [3, 5, 7, 9], "stalled": [3, 4, 4, 5], "worse": [6, 5, 3, 2]}[kind]
    col = VCOL[kind]
    L, R, T, B = 10.0, 6.0, 10.0, 10.0
    pw, ph = w - L - R, h - T - B
    X = lambda i: L + pw * i / 3.0
    Y = lambda v: T + ph * (1 - v / 10.0)
    out = [f'<path d="M{L:.1f},{T + ph:.1f} L{L + pw:.1f},{T + ph:.1f}" stroke="{K.RULE}" '
           f'stroke-width="0.7"/>']
    d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(series))
    out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.7"/>')
    for i, v in enumerate(series):
        out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="2.7" fill="{col}"/>')
    return _svg(out, 0, 0, w, h)


# ------------------------------------------------------------- the tree ------
def tree(w=300.0):
    """The decision rule: one reading in, three ways out.

    Only the stem is drawn. The three outlets are HTML cards under it, because
    each needs a sentence and an SVG cannot wrap one.
    """
    h = 84.0
    mid = w / 2.0
    cols = [w / 6.0, mid, w * 5 / 6.0]
    out = [f'<rect x="{mid - 52:.1f}" y="2" width="104" height="22" rx="3" fill="{K.CARD}" '
           f'stroke="{K.INK2}" stroke-width="0.9"/>',
           _t(mid, 16.4, "Read the number", 9, K.INK, weight="600"),
           f'<path d="M{mid:.1f},24 L{mid:.1f},40" stroke="{K.INK2}" stroke-width="0.9"/>',
           f'<rect x="{mid - 80:.1f}" y="40" width="160" height="20" rx="3" fill="{K.PAPER2}" '
           f'stroke="{K.RULE}" stroke-width="0.8"/>',
           _t(mid, 53.8, "Compare it with the reading before", 8.2, K.INK2),
           f'<path d="M{mid:.1f},60 L{mid:.1f},70 M{cols[0]:.1f},70 L{cols[2]:.1f},70" '
           f'stroke="{K.INK2}" stroke-width="0.9"/>']
    for kind, x in zip(("worse", "stalled", "on"), cols):
        col = VCOL[kind]
        out.append(f'<path d="M{x:.1f},70 L{x:.1f},80" stroke="{col}" stroke-width="1.3"/>')
        out.append(f'<path d="M{x - 3:.1f},75.6 L{x:.1f},80.6 L{x + 3:.1f},75.6" fill="none" '
                   f'stroke="{col}" stroke-width="1.3"/>')
    return _svg(out, 0, 0, w, h)


# ------------------------------------------------ the whole book at a glance --
def spread(w=392.0):
    """Where the fifty checkpoints fall, all fifteen arcs stacked and scaled to
    the same width, so the pattern of the schedule is visible in one look."""
    rowh, lab = 10.4, 92.0
    keys = [a["key"] for a in A.ARCS]
    h = len(keys) * rowh + 10
    out = []
    for r, key in enumerate(keys):
        a = A.BY_KEY[key]
        n = len(a["sessions"])
        y = 8 + r * rowh
        out.append(_t(lab - 6, y + 2.9, a["short"], 6.8, K.INK2, "end"))
        out.append(f'<path d="M{lab:.1f},{y:.1f} L{w - 16:.1f},{y:.1f}" stroke="{K.RULE}" '
                   f'stroke-width="2.6" stroke-linecap="round"/>')
        for _i, sess, idx, _g in C.schedule(key):
            x = lab + (w - 16 - lab) * (idx - 0.5) / float(n)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.1" fill="{ON}"/>')
        out.append(_t(w - 11, y + 3.2, n, 7, K.INK3, "start"))
    return _svg(out, 0, 0, w, h)


# ------------------------------------------------------------- instruments ---
def bandbar(name, w=250.0):
    """An instrument's severity bands drawn to scale, with the target band and
    the step that counts as a real change both marked."""
    m = C.MEASURE[name]
    lo, hi = m["range"]
    # The band names are set in HTML under the bar, not in here: an SVG label
    # cannot wrap, and five of them across one bar collide at any useful size.
    h = 40.0
    L, R = 2.0, 2.0
    pw = w - L - R
    X = lambda v: L + pw * (v - lo) / float(hi - lo)
    out = []
    tgt = m["bands"][-1] if m["dir"] == "up" else m["bands"][0]
    for i, (blo, bhi, nm) in enumerate(m["bands"]):
        x0, x1 = X(blo), X(bhi + 1 if bhi < hi else hi)
        fill = ON if (blo, bhi, nm) == tgt else K.INK2
        op = 0.75 if (blo, bhi, nm) == tgt else 0.10 + 0.06 * i
        out.append(f'<rect x="{x0:.1f}" y="6" width="{max(0.6, x1 - x0):.1f}" height="15" '
                   f'fill="{fill}" fill-opacity="{op:.2f}"/>')
        if i:
            out.append(f'<path d="M{x0:.1f},6 L{x0:.1f},24" stroke="{K.PAPER}" '
                       f'stroke-width="0.8"/>')
            out.append(_t(x0, 30, blo, 6.6, K.INK3))
    out.append(f'<rect x="{L:.1f}" y="6" width="{pw:.1f}" height="15" fill="none" '
               f'stroke="{K.INK2}" stroke-width="0.8"/>')
    out.append(_t(X(lo), 3.4, lo, 7, K.INK3, "start"))
    out.append(_t(X(hi), 3.4, hi, 7, K.INK3, "end"))
    # the step, drawn as a bracket at true width
    sx0, sx1 = X(lo), X(lo + m["step"])
    out.append(f'<path d="M{sx0:.1f},38 L{sx0:.1f},34 L{sx1:.1f},34 L{sx1:.1f},38" fill="none" '
               f'stroke="{K.RUST}" stroke-width="0.9"/>')
    out.append(_t(sx1 + 3, 37.6, "a step of %d" % m["step"], 6.6, K.RUST, "start"))
    return _svg(out, 0, 0, w, h)


def goalbar(w=260.0):
    """The 0-10 goal scale, drawn as the client sees it on the card."""
    h = 34.0
    L, R = 8.0, 8.0
    pw = w - L - R
    out = [f'<path d="M{L:.1f},16 L{L + pw:.1f},16" stroke="{K.INK2}" stroke-width="1"/>']
    for v in range(11):
        x = L + pw * v / 10.0
        tall = v in (0, 5, 10)
        out.append(f'<path d="M{x:.1f},{16 - (5 if tall else 3):.1f} L{x:.1f},'
                   f'{16 + (5 if tall else 3):.1f}" stroke="{K.INK2}" stroke-width="0.9"/>')
        out.append(_t(x, 30, v, 7.4, K.INK if tall else K.INK3))
    out.append(f'<rect x="{L + pw * 0.7:.1f}" y="9" width="{pw * 0.3:.1f}" height="14" '
               f'fill="{ON}" fill-opacity="0.13"/>')
    out.append(_t(L, 6, "not at all", 6.6, K.INK3, "start"))
    out.append(_t(L + pw, 6, "the goal", 6.6, K.INK3, "end"))
    return _svg(out, 0, 0, w, h)


# ----------------------------------------------------- charts that mislead ---
def artifact(kind, w=92.0, h=58.0):
    series = {
        "spike": [3, 3, 8, 3],
        "ceiling": [6, 8, 9, 9],
        "sawtooth": [4, 7, 4, 7],
    }[kind]
    L, R, T, B = 8.0, 6.0, 9.0, 9.0
    pw, ph = w - L - R, h - T - B
    X = lambda i: L + pw * i / 3.0
    Y = lambda v: T + ph * (1 - v / 10.0)
    out = [f'<path d="M{L:.1f},{T + ph:.1f} L{L + pw:.1f},{T + ph:.1f}" stroke="{K.RULE}" '
           f'stroke-width="0.7"/>']
    if kind == "ceiling":
        out.insert(0, f'<rect x="{L:.1f}" y="{Y(10):.1f}" width="{pw:.1f}" '
                      f'height="{Y(7) - Y(10):.1f}" fill="{ON}" fill-opacity="0.12"/>')
    d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(series))
    out.append(f'<path d="{d}" fill="none" stroke="{K.INK2}" stroke-width="1.5"/>')
    for i, v in enumerate(series):
        out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="2.5" fill="{K.INK2}"/>')
    return _svg(out, 0, 0, w, h)


def shortfig(key, w=250.0):
    """The whole schedule against the three readings a short course keeps."""
    ns = A.checkpoints(key)
    keep = set(C.short_course(key))
    # An arc that reads three times is already the short course. Drawing the
    # same row twice says "these differ" when they do not.
    rows = ((13.0, False), (33.0, True)) if len(ns) > 3 else ((16.0, False),)
    h = 44.0 if len(rows) > 1 else 32.0
    L, R = 10.0, 10.0
    pw = w - L - R
    a = A.BY_KEY[key]
    n = len(a["sessions"])
    out = []
    for row, (y, only) in enumerate(rows):
        out.append(f'<path d="M{L:.1f},{y:.1f} L{L + pw:.1f},{y:.1f}" stroke="{K.RULE}" '
                   f'stroke-width="2.4" stroke-linecap="round"/>')
        for s in ns:
            if only and s not in keep:
                continue
            x = L + pw * (s - a["start"] + 0.5) / float(n)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{ON}"/>')
    return _svg(out, 0, 0, w, h)
