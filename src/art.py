# -*- coding: utf-8 -*-
"""The forty-six plates of The Progress Checkpoints, drawn here.

These occupy the slots the Higgsfield renders were written for. The renders
exist in the account that ordered them, but they are served from a host this
build environment's egress policy blocks, and no tool available here returns
their bytes -- so the book could not be finished with them. Rather than ship a
book with forty-six empty frames, the same compositions are drawn as vector
plates and rasterised into the same files the build already expects.

Nothing downstream knows the difference: make_plates.py writes
assets/photos/checkpoints/<slug>.jpg, and dropping real photographs over those
files is all it would take to swap them back.

The rules the photographs were held to are the rules here. Warm oak and cream,
muted neutrals, one small accent at most. No lettering anywhere -- writing is
ruled strokes, the way it reads from across a desk.
"""
import math

# ------------------------------------------------------------------ palette --
# Chroma matters here, not taste alone: check_color counts any pixel at
# C* 18 or more, and the desk covers whole pages on the five openers. At
# #DDCBA9 it measured 19.3 and took the book to 5.95 per cent against a brief
# of about two. Every large area below is under that line on purpose.
OAK = "#DED4C2"
OAK_D = "#C9BCA3"
OAK_L = "#E8E0D1"
PAPER = "#FFFCF6"
PAPER_D = "#EFE5D3"

SHADOW = "rgba(90,70,45,0.16)"
RULE = "#CFC1A6"
GRAPH = "#DCCFB4"
LEAD = "#5C5A55"
INK = "#173C42"
INK2 = "#6B7D7E"
LINEN = "#DCD2BC"
RUST = "#B8552F"
SAGE = "#5F7554"
OCHRE = "#D3A44C"
PLUM = "#6F5F80"
SKIN = "#E2C4A8"
SKIN_D = "#CBA98A"
SLEEVE = "#EDE7DC"


def _defs():
    return (
        '<defs>'
        '<linearGradient id="lt" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>'
        f'<stop offset="0.58" stop-color="#FFFFFF" stop-opacity="0.02"/>'
        f'<stop offset="1" stop-color="#6B5432" stop-opacity="0.16"/>'
        '</linearGradient>'
        '<filter id="sh" x="-30%" y="-30%" width="170%" height="170%">'
        '<feDropShadow dx="0" dy="3" stdDeviation="3.4" flood-color="#5A4426" flood-opacity="0.30"/>'
        '</filter>'
        '<filter id="shs" x="-40%" y="-40%" width="190%" height="190%">'
        '<feDropShadow dx="0" dy="1.6" stdDeviation="1.8" flood-color="#5A4426" flood-opacity="0.32"/>'
        '</filter>'
        '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur stdDeviation="7"/></filter>'
        '</defs>')


def svg(w, h, body, bg=OAK):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{_defs()}'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>'
            f'{grain(w, h)}{body}'
            f'<rect width="{w}" height="{h}" fill="url(#lt)"/></svg>')


def grain(w, h):
    """The wood, as a few long soft strokes rather than a texture fill."""
    out = []
    for i in range(9):
        y = h * (i + 0.4) / 9.0
        amp = 5 + (i % 3) * 3
        d = "M0,%.1f " % y + " ".join(
            "Q%.0f,%.1f %.0f,%.1f" % (x + w / 16.0, y + (amp if (x // (w / 8.0)) % 2 else -amp),
                                      x + w / 8.0, y)
            for x in [w * k / 8.0 for k in range(8)])
        out.append(f'<path d="{d}" fill="none" stroke="{OAK_D}" stroke-width="{1.3 + (i % 2) * 0.9}" '
                   f'stroke-opacity="0.55"/>')
    out.append(f'<ellipse cx="{w * 0.22:.0f}" cy="{h * 0.12:.0f}" rx="{w * 0.44:.0f}" '
               f'ry="{h * 0.4:.0f}" fill="#FFFFFF" fill-opacity="0.17" filter="url(#soft)"/>')
    return "".join(out)


# --------------------------------------------------------------- primitives --
def sheet(x, y, w, h, rot=0, fill=PAPER, r=2):
    t = f' transform="rotate({rot} {x + w / 2:.1f} {y + h / 2:.1f})"' if rot else ""
    return (f'<g{t}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" filter="url(#sh)"/></g>')


def ruled(x, y, w, n, gap, col=RULE, sw=2.0, jitter=True):
    out = []
    for i in range(n):
        ww = w * (0.72 + 0.28 * ((i * 7 % 5) / 4.0)) if jitter else w
        out.append(f'<rect x="{x:.1f}" y="{y + i * gap:.1f}" width="{ww:.1f}" height="{sw}" '
                   f'rx="{sw / 2:.1f}" fill="{col}"/>')
    return "".join(out)


def grid(x, y, w, h, cols, rows, col=GRAPH, sw=1.2):
    out = []
    for c in range(cols + 1):
        gx = x + w * c / cols
        out.append(f'<rect x="{gx:.1f}" y="{y:.1f}" width="{sw}" height="{h:.1f}" fill="{col}"/>')
    for r in range(rows + 1):
        gy = y + h * r / rows
        out.append(f'<rect x="{x:.1f}" y="{gy:.1f}" width="{w:.1f}" height="{sw}" fill="{col}"/>')
    return "".join(out)


def pencil(x, y, ln, ang=0, col=LEAD):
    """A pencil lying on the desk, tip first."""
    body = ln * 0.82
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang})" filter="url(#shs)">'
            f'<rect x="0" y="-5" width="{body:.1f}" height="10" rx="2" fill="{col}"/>'
            f'<rect x="{body:.1f}" y="-5" width="{ln * 0.10:.1f}" height="10" fill="#C9A227"/>'
            f'<rect x="{body + ln * 0.10:.1f}" y="-5" width="{ln * 0.08:.1f}" height="10" rx="2" '
            f'fill="#D98C7A"/>'
            f'<path d="M0,-5 L{-ln * 0.075:.1f},0 L0,5 Z" fill="#E8D9BE"/>'
            f'<path d="M{-ln * 0.045:.1f},-2 L{-ln * 0.075:.1f},0 L{-ln * 0.045:.1f},2 Z" '
            f'fill="#3A3733"/></g>')


def line_path(pts, col=LEAD, sw=3.0, dash=None):
    d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % p for i, p in enumerate(pts))
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def dot(x, y, r=6, col=LEAD, ring=False):
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'
    if ring:
        s += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 5}" fill="none" stroke="{col}" '
              f'stroke-width="2" stroke-opacity="0.65"/>')
    return s


def mug(x, y, r=34):
    return (f'<g filter="url(#sh)">'
            f'<ellipse cx="{x + r * 1.5:.0f}" cy="{y:.0f}" rx="{r * 0.42:.0f}" ry="{r * 0.5:.0f}" '
            f'fill="none" stroke="{PAPER_D}" stroke-width="7"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{PAPER_D}"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 0.78:.0f}" fill="#EFE7DA"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 0.62:.0f}" fill="#E4D9C6"/></g>')


def clipboard(x, y, w, h):
    return (f'<g filter="url(#sh)">'
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="7" fill="#BFAE95"/>'
            f'<rect x="{x + w * 0.05:.0f}" y="{y + h * 0.055:.0f}" width="{w * 0.90:.0f}" '
            f'height="{h * 0.90:.0f}" rx="2" fill="{PAPER}"/>'
            f'<rect x="{x + w * 0.33:.0f}" y="{y - h * 0.022:.0f}" width="{w * 0.34:.0f}" '
            f'height="{h * 0.055:.0f}" rx="4" fill="#9BA0A4"/></g>')


def stem(x, y, ln, ang, col="#C2B79B"):
    out = [f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang})">',
           f'<path d="M0,0 Q{ln * 0.5:.0f},{-ln * 0.06:.0f} {ln:.0f},0" fill="none" '
           f'stroke="{col}" stroke-width="3"/>']
    for i in range(6):
        px = ln * (0.25 + i * 0.13)
        s = 1 if i % 2 else -1
        out.append(f'<ellipse cx="{px:.0f}" cy="{s * 9:.0f}" rx="13" ry="6" fill="{col}" '
                   f'fill-opacity="0.85" transform="rotate({s * 22} {px:.0f} {s * 9:.0f})"/>')
    out.append("</g>")
    return "".join(out)


def hand(x, y, ang=0, scale=1.0, holding=False):
    """A hand from the wrist, seen from above. Simplified on purpose: the
    photographs showed hands and the plates should not pretend otherwise."""
    g = [f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang}) scale({scale})" filter="url(#sh)">',
         f'<rect x="-30" y="-150" width="128" height="150" rx="34" fill="{SLEEVE}"/>',
         f'<path d="M-18,-16 Q-24,44 14,66 Q56,86 92,58 Q116,38 112,-8 L112,-24 Q60,-40 -18,-28 Z" '
         f'fill="{SKIN}"/>']
    for i, (fx, fy, fl, fa) in enumerate(((6, 40, 74, -6), (36, 52, 84, 2),
                                          (66, 48, 78, 10), (92, 34, 62, 20))):
        g.append(f'<rect x="{fx}" y="{fy}" width="26" height="{fl}" rx="13" fill="{SKIN}" '
                 f'transform="rotate({fa} {fx + 13} {fy})"/>')
    g.append(f'<rect x="-30" y="2" width="30" height="62" rx="15" fill="{SKIN}" '
             f'transform="rotate(-28 -15 2)"/>')
    g.append(f'<path d="M-18,-16 Q-24,44 14,66" fill="none" stroke="{SKIN_D}" stroke-width="2" '
             f'stroke-opacity="0.6"/>')
    g.append("</g>")
    return "".join(g)


def chair(x, y, w, h, turn=0):
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({turn})" filter="url(#sh)">'
            f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" rx="18" fill="#DCD3C2"/>'
            f'<rect x="{w * 0.10:.0f}" y="{h * 0.10:.0f}" width="{w * 0.80:.0f}" '
            f'height="{h * 0.52:.0f}" rx="12" fill="#E6DED0"/>'
            f'<rect x="{-w * 0.06:.0f}" y="{h * 0.20:.0f}" width="{w * 0.12:.0f}" '
            f'height="{h * 0.5:.0f}" rx="8" fill="#D2C8B6"/>'
            f'<rect x="{w * 0.94:.0f}" y="{h * 0.20:.0f}" width="{w * 0.12:.0f}" '
            f'height="{h * 0.5:.0f}" rx="8" fill="#D2C8B6"/></g>')


# ------------------------------------------------------------------- plates --
# Each returns an SVG string. Sizes are the aspect the page asks for.
W43, H43 = 1600, 1200          # 4:3
W32, H32 = 1600, 1067          # 3:2
W23, H23 = 1067, 1600          # 2:3
W169, H169 = 1600, 900         # 16:9


def _chartsheet(x, y, w, h, series, ring=None, spike=False, blank=False):
    """A sheet of graph paper with a plotted pencil line."""
    out = [sheet(x, y, w, h), grid(x + w * 0.09, y + h * 0.13, w * 0.82, h * 0.68, 8, 5)]
    px, py = x + w * 0.09, y + h * 0.13
    pw, ph = w * 0.82, h * 0.68
    if not blank:
        pts = [(px + pw * i / float(len(series) - 1), py + ph * (1 - v / 10.0))
               for i, v in enumerate(series)]
        out.append(line_path(pts, LEAD, 3.4))
        for i, p in enumerate(pts):
            out.append(dot(p[0], p[1], 7, LEAD, ring=(ring is not None and i == ring)))
    out.append(ruled(px, y + h * 0.88, pw * 0.5, 2, h * 0.05, RULE, 2.4))
    return "".join(out)


def p_h0_cover():
    b = [_chartsheet(210, 170, 830, 830, [8, 6, 4, 2]),
         pencil(1130, 760, 250, -14),
         mug(1330, 320, 74),
         sheet(1180, 940, 380, 300, 8, LINEN, 6),
         stem(120, 1050, 300, -8)]
    return svg(W43, H43, "".join(b))


def p_h1_method():
    b = []
    for i in range(4):
        b.append(sheet(170 + i * 330, 430, 250, 360, -2 + i * 1.4))
        b.append(ruled(205 + i * 330, 500, 180, 3, 34))
    b.append(pencil(700, 900, 260, -22))
    b.append(f'<circle cx="255" cy="470" r="15" fill="{RUST}" fill-opacity="0.8"/>')
    return svg(W43, H43, "".join(b))


def p_h2_arcs():
    b = []
    for r in range(3):
        for c in range(5):
            x, y = 130 + c * 280, 260 + r * 300
            lift = -6 if (r, c) == (1, 2) else 0
            b.append(sheet(x, y + lift, 235, 215, -1.5 + c * 0.8))
            b.append(f'<rect x="{x + 22}" y="{y + 26 + lift}" width="190" height="16" rx="8" '
                     f'fill="{RULE}"/>')
            b.append(ruled(x + 22, y + 70 + lift, 170, 3, 30))
    return svg(W43, H43, "".join(b))


def p_h3_sheets():
    b = [clipboard(360, 150, 780, 950),
         grid(470, 400, 570, 470, 7, 5),
         ruled(470, 300, 400, 2, 40, RULE, 3),
         pencil(1230, 700, 250, -80),
         f'<rect x="1210" y="330" width="120" height="44" rx="22" fill="{PAPER_D}"/>',
         stem(250, 1080, 320, -12)]
    return svg(W43, H43, "".join(b))


def p_h9_back():
    """A closed folder, tied, at the end of the day.

    Drawn directly rather than through sheet(): the helper's drop shadow over a
    mid-tone fill washed the folder out until it read as a placeholder box.
    """
    b = [f'<g transform="rotate(-3 750 640)" filter="url(#sh)">',
         f'<rect x="270" y="300" width="960" height="680" rx="14" fill="#A8977A"/>',
         f'<rect x="270" y="300" width="960" height="660" rx="14" fill="#C2B090"/>',
         f'<rect x="292" y="322" width="916" height="616" rx="9" fill="#CFC4B0"/>',
         f'<rect x="292" y="322" width="916" height="96" rx="9" fill="#C4B9A4"/>',
         f'<rect x="292" y="414" width="916" height="7" fill="#B6A483"/>',
         # the tie: one band across the short edge, and its knot
         f'<rect x="940" y="288" width="40" height="704" fill="#8F7F63"/>',
         f'<rect x="940" y="288" width="40" height="704" fill="#9C9282" opacity="0.55"/>',
         f'<ellipse cx="960" cy="640" rx="34" ry="24" fill="#8A7A5E"/>',
         "</g>",
         mug(1350, 1040, 70),
         pencil(230, 1100, 250, -7),
         stem(250, 180, 330, 7)]
    return svg(W43, H43, "".join(b))


def p_c1_months():
    b = [sheet(120, 150, 1360, 780, 0, PAPER, 4),
         f'<rect x="790" y="150" width="14" height="780" fill="{PAPER_D}"/>']
    for side in (0, 1):
        ox = 175 + side * 660
        for r in range(4):
            for c in range(4):
                x, y = ox + c * 140, 250 + r * 160
                b.append(f'<rect x="{x}" y="{y}" width="120" height="130" rx="4" fill="none" '
                         f'stroke="{RULE}" stroke-width="2.4"/>')
                if (r + c + side) % 3 != 2:
                    b.append(line_path([(x + 30, y + 78), (x + 48, y + 98), (x + 92, y + 46)],
                                       RULE, 4.5))
    b.append(pencil(770, 980, 230, -84))
    return svg(W32, H32, "".join(b))


def p_c2_anatomy():
    x, y, w, h = 300, 190, 1000, 690
    b = [sheet(x, y, w, h, -1)]
    for i, frac in enumerate((0.18, 0.30, 0.22, 0.18)):
        top = y + 70 + sum((0.18, 0.30, 0.22, 0.18)[:i]) * (h - 150)
        b.append(f'<rect x="{x + 60}" y="{top:.0f}" width="{w - 120}" '
                 f'height="{frac * (h - 150) - 18:.0f}" rx="6" fill="none" stroke="{RULE}" '
                 f'stroke-width="3"/>')
        b.append(ruled(x + 90, top + 22, w - 220, 2, 26))
    b.append(pencil(1360, 560, 250, 90))
    b.append(f'<circle cx="{x + w - 58}" cy="{y + 46}" r="17" fill="{RUST}" fill-opacity="0.85"/>')
    return svg(W32, H32, "".join(b))


def p_c3_three():
    b = []
    for i, (dx, rot) in enumerate(((-360, -20), (0, 0), (360, 20))):
        x = 800 + dx - 190
        b.append(sheet(x, 300, 380, 520, rot, LINEN if i != 1 else PAPER, 6))
        if i == 1:
            b.append(sheet(x + 24, 268, 330, 470, rot, PAPER))
            b.append(ruled(x + 60, 330, 250, 4, 38))
    b.append(f'<rect x="1178" y="300" width="70" height="26" rx="8" fill="{RUST}" '
             f'fill-opacity="0.85" transform="rotate(20 1213 313)"/>')
    return svg(W32, H32, "".join(b))


def p_k1_ontrack():
    return svg(W43, H43, _chartsheet(160, 150, 1280, 900, [8, 6, 4, 2])
               + pencil(1250, 1090, 240, -10))


def p_k2_stalled():
    return svg(W43, H43, _chartsheet(160, 150, 1280, 900, [5, 5.4, 4.8, 5.2])
               + pencil(300, 1110, 230, 4)
               + f'<rect x="1210" y="1060" width="120" height="70" rx="12" fill="{PAPER_D}" '
                 f'filter="url(#shs)"/>')


def p_k3_worse():
    return svg(W43, H43, _chartsheet(160, 150, 1280, 900, [2, 4, 6, 8.6], ring=3))


def p_m1_choose():
    b = [sheet(110, 180, 660, 900),
         ruled(170, 270, 520, 9, 82, RULE, 3)]
    for i in range(9):
        for k in range(4):
            b.append(f'<rect x="{560 + k * 44}" y="{262 + i * 82}" width="30" height="30" rx="4" '
                     f'fill="none" stroke="{RULE}" stroke-width="2.4"/>')
    b.append(sheet(880, 430, 620, 330))
    b.append(ruled(930, 490, 460, 1, 0, RULE, 3))
    b.append(f'<rect x="930" y="620" width="520" height="7" rx="3.5" fill="{INK2}" '
             f'fill-opacity="0.55"/>')
    for k in range(11):
        b.append(f'<rect x="{930 + k * 52}" y="{608 - (7 if k % 5 == 0 else 0)}" width="5" '
                 f'height="{31 if k % 5 == 0 else 17}" rx="2.5" fill="{INK2}" fill-opacity="0.55"/>')
    b.append(pencil(800, 900, 240, -66))
    return svg(W32, H32, "".join(b))


def p_l1_licence():
    b = []
    for i in range(5):
        b.append(sheet(300 + i * 36, 210 + i * 34, 900, 620, -4 + i * 1.6))
    b.append(ruled(420, 330, 620, 7, 62))
    b.append(f'<circle cx="1130" cy="300" r="34" fill="none" stroke="{RUST}" stroke-width="7" '
             f'stroke-opacity="0.75"/>')
    b.append(f'<rect x="1096" y="288" width="68" height="24" rx="6" fill="{RUST}" '
             f'fill-opacity="0.55"/>')
    return svg(W32, H32, "".join(b))


def _form_plate(rows):
    b = [clipboard(120, 120, 830, 1370)]
    b.append(f'<rect x="200" y="290" width="680" height="24" rx="12" fill="{RULE}"/>')
    gap = min(96, 1000 / float(rows))
    for i in range(rows):
        y = 400 + i * gap
        b.append(ruled(200, y, 430, 1, 0, RULE, 3))
        for k in range(4):
            b.append(f'<rect x="{660 + k * 58}" y="{y - 13}" width="34" height="34" rx="5" '
                     f'fill="none" stroke="{RULE}" stroke-width="2.6"/>')
    b.append(pencil(230, 400 + rows * gap + 90, 380, -6))
    return svg(W23, H23, "".join(b))


def p_q1_phq():
    return _form_plate(9)


def p_q2_gad():
    return _form_plate(7)


def _card_scale(x, y, w, h, mark=None):
    b = [sheet(x, y, w, h), ruled(x + 40, y + 52, w - 150, 1, 0, RULE, 3)]
    by = y + h * 0.62
    b.append(f'<rect x="{x + 40}" y="{by}" width="{w - 80}" height="6" rx="3" fill="{INK2}" '
             f'fill-opacity="0.5"/>')
    for k in range(11):
        gx = x + 40 + (w - 80) * k / 10.0
        b.append(f'<rect x="{gx - 2}" y="{by - (10 if k % 5 == 0 else 6)}" width="4.5" '
                 f'height="{26 if k % 5 == 0 else 18}" rx="2" fill="{INK2}" fill-opacity="0.5"/>')
    if mark is not None:
        gx = x + 40 + (w - 80) * mark
        b.append(f'<rect x="{gx - 4}" y="{by - 24}" width="8" height="54" rx="4" fill="{LEAD}"/>')
    return "".join(b)


def p_r1_hand():
    """Step one: the card is halfway across the desk, still moving."""
    b = [sheet(150, 250, 520, 700, -4, PAPER_D),
         _card_scale(620, 380, 760, 440),
         f'<path d="M560,600 L610,600" stroke="{LEAD}" stroke-width="5" stroke-opacity="0.35" '
         f'stroke-linecap="round"/>',
         f'<path d="M500,600 L545,600" stroke="{LEAD}" stroke-width="5" stroke-opacity="0.18" '
         f'stroke-linecap="round"/>',
         pencil(1240, 1030, 230, -8)]
    return svg(W43, H43, "".join(b))


def p_r2_mark():
    """Step two: the mark has just been made and the pencil is still on it."""
    b = [_card_scale(300, 330, 1000, 540, mark=0.66),
         pencil(966, 1012, 330, -118),
         f'<circle cx="960" cy="700" r="62" fill="{LEAD}" fill-opacity="0.07"/>']
    return svg(W43, H43, "".join(b))


def p_r3_plot():
    """Step three: the fourth dot is new, and the line to it not yet inked."""
    b = [_chartsheet(150, 160, 1100, 880, [7, 5.4, 4]),
         dot(1042, 764, 9, LEAD, ring=True),
         pencil(1112, 1010, 330, -124)]
    return svg(W43, H43, "".join(b))


def p_r4_compare():
    """Step four: the two sheets side by side, read against one another."""
    b = [_chartsheet(90, 230, 800, 730, [7, 5, 3.4, 2]),
         _card_scale(960, 400, 560, 380, mark=0.6),
         f'<path d="M900,600 L950,600" stroke="{LEAD}" stroke-width="4" '
         f'stroke-dasharray="14 12" stroke-opacity="0.45"/>']
    return svg(W43, H43, "".join(b))


def p_r5_decide():
    b = []
    for i, rot in enumerate((-13, 0, 13)):
        b.append(sheet(300 + i * 400, 340, 360, 480, rot))
        b.append(ruled(340 + i * 400, 410, 250, 3, 42))
    b.append(pencil(700, 660, 330, -8))
    return svg(W43, H43, "".join(b))


def _place(x, y, flip=False):
    """One person's place at the table: a mug and a pencil, no person."""
    d = -1 if flip else 1
    return mug(x, y, 62) + pencil(x + d * 40, y + 150, 190, 8 * d)


def p_t1_script():
    """The sheet on the table between the two of them, and both pencils down."""
    b = [f'<ellipse cx="800" cy="560" rx="620" ry="330" fill="#C9BCA1"/>',
         f'<ellipse cx="800" cy="548" rx="588" ry="306" fill="#D9CDB4"/>',
         _chartsheet(600, 380, 400, 330, [7, 5.2, 3.6]),
         _place(300, 430), _place(1300, 430, True)]
    return svg(W32, H32, "".join(b), bg="#CFC5B4")


def p_t2_words():
    """The same table with the sheet turned face down and set to one side."""
    b = [f'<ellipse cx="800" cy="560" rx="620" ry="330" fill="#C9BCA1"/>',
         f'<ellipse cx="800" cy="548" rx="588" ry="306" fill="#D9CDB4"/>',
         sheet(640, 400, 380, 300, 5, PAPER_D),
         f'<rect x="700" y="470" width="260" height="8" rx="4" fill="{RULE}" '
         f'transform="rotate(5 830 474)"/>',
         _place(300, 430), _place(1300, 430, True)]
    return svg(W32, H32, "".join(b), bg="#CFC5B4")


def p_n1_note():
    b = [f'<rect x="120" y="120" width="760" height="520" rx="16" fill="#C9C3B8" '
         f'filter="url(#sh)"/>',
         f'<rect x="150" y="150" width="700" height="460" rx="10" fill="#D8D2C6"/>',
         sheet(950, 300, 520, 640, 4),
         ruled(1000, 390, 400, 7, 62),
         pencil(1105, 1020, 320, -122),
         _chartsheet(300, 700, 560, 420, [6, 4.6, 3], blank=False)]
    return svg(W32, H32, "".join(b))


def p_b1_stop():
    b = [sheet(300, 260, 1000, 600, -3, PAPER_D),
         sheet(520, 400, 620, 360, 2),
         f'<rect x="520" y="400" width="26" height="360" rx="4" fill="{RUST}" fill-opacity="0.85"/>',
         pencil(240, 950, 260, -6)]
    return svg(W32, H32, "".join(b))


def p_p1_chart():
    b = [_chartsheet(120, 120, 1140, 800, [7, 5.2, 3.6]),
         f'<rect x="1075" y="780" width="5" height="46" rx="2.5" fill="{LEAD}"/>',
         pencil(1160, 960, 320, -124)]
    return svg(W32, H32, "".join(b))


def p_p2_lies():
    b = [_chartsheet(150, 150, 1300, 780, [3, 3.2, 8.6, 3.1])]
    b.append(f'<path d="M1180,300 q64,-44 92,4 q22,42 -34,72 q-30,16 -30,44" fill="none" '
             f'stroke="{RUST}" stroke-width="11" stroke-linecap="round" stroke-opacity="0.85"/>')
    b.append(f'<circle cx="1206" cy="474" r="9" fill="{RUST}" fill-opacity="0.85"/>')
    return svg(W32, H32, "".join(b))


def p_s1_short():
    b = [sheet(150, 330, 1300, 420)]
    y = 540
    b.append(f'<rect x="270" y="{y - 3}" width="1060" height="6" rx="3" fill="{RULE}"/>')
    for k in (0, 0.5, 1.0):
        b.append(dot(270 + 1060 * k, y, 15, LEAD, ring=True))
    return svg(W32, H32, "".join(b))


def p_x1_reading():
    b = [f'<rect x="60" y="300" width="947" height="1010" rx="8" fill="{PAPER_D}" '
         f'filter="url(#sh)"/>',
         sheet(80, 320, 440, 970), sheet(546, 320, 440, 970),
         ruled(130, 400, 320, 3, 42, RULE, 4),
         grid(130, 570, 340, 250, 6, 4),
         ruled(130, 880, 320, 7, 44),
         ruled(596, 400, 320, 2, 42, RULE, 4),
         ruled(596, 520, 340, 12, 44),
         f'<rect x="520" y="320" width="28" height="970" fill="#E6DCC9"/>',
         pencil(534, 900, 190, 90)]
    return svg(W23, H23, "".join(b))


# ---- the fifteen arc emblems ------------------------------------------------
def _arc(body):
    return svg(W169, H169, body)


def p_a_int():
    """One blank sheet, one ruled line, a sharpened pencil. The record starts."""
    return _arc(sheet(390, 150, 780, 600)
                + ruled(470, 250, 420, 1, 0, RULE, 5)
                + pencil(1255, 620, 260, -14)
                + f'<rect x="250" y="640" width="180" height="120" rx="10" fill="{PAPER_D}" '
                  f'filter="url(#shs)"/>')


def p_a_emo():
    """A shallow bowl of water, the ripples still moving."""
    b = [f'<circle cx="1010" cy="450" r="258" fill="#B9AE98" filter="url(#sh)"/>',
         f'<circle cx="1010" cy="450" r="228" fill="#CFC8B6"/>',
         f'<circle cx="1010" cy="450" r="206" fill="#C3C9C4"/>']
    for r, op in ((66, 0.9), (118, 0.7), (172, 0.5)):
        b.append(f'<circle cx="1010" cy="450" r="{r}" fill="none" stroke="#FFFFFF" '
                 f'stroke-width="7" stroke-opacity="{op}"/>')
    b.append(f'<path d="M846,300 Q1010,236 1174,300" fill="none" stroke="#FFFFFF" '
             f'stroke-width="10" stroke-opacity="0.5"/>')
    b.append(sheet(270, 290, 400, 320, -5))
    b.append(ruled(310, 350, 300, 3, 44))
    return _arc("".join(b))


def p_a_anx():
    b = [sheet(1120, 330, 340, 270, 3)]
    for i in range(5):
        h = 90 + i * 66
        b.append(f'<rect x="{240 + i * 150}" y="{740 - h}" width="126" height="{h}" rx="8" '
                 f'fill="#D5CAB4" filter="url(#shs)"/>')
        b.append(f'<rect x="{240 + i * 150}" y="{740 - h}" width="126" height="16" rx="8" '
                 f'fill="#E4DCCB"/>')
    return _arc("".join(b))


def p_a_dep():
    b = [sheet(280, 190, 1040, 520)]
    for c in range(7):
        x = 340 + c * 138
        b.append(f'<rect x="{x}" y="250" width="112" height="400" rx="6" fill="none" '
                 f'stroke="{RULE}" stroke-width="3"/>')
        if c in (1, 4):
            b.append(line_path([(x + 28, 440), (x + 48, 468), (x + 88, 396)], LEAD, 6))
    b.append(pencil(360, 760, 260, -4))
    return _arc("".join(b))


def p_a_str():
    b = []
    for i in range(5):
        b.append(f'<rect x="{170 + i * 8}" y="{640 - i * 108}" width="520" height="96" rx="10" '
                 f'fill="{"#E4DAC7" if i % 2 else "#EDE4D3"}" filter="url(#shs)"/>')
    b.append(f'<rect x="900" y="200" width="7" height="520" fill="{RULE}"/>')
    return _arc("".join(b))


def p_a_sw():
    """A small round mirror, face up, catching a corner of the sheet beside it."""
    b = [sheet(240, 250, 420, 420, -6),
         f'<circle cx="1010" cy="450" r="262" fill="#BCB3A0" filter="url(#sh)"/>',
         f'<circle cx="1010" cy="450" r="232" fill="#CFCFCB"/>',
         f'<circle cx="1010" cy="450" r="214" fill="#DEDED9"/>',
         f'<path d="M830,286 Q1010,214 1190,286 Q1080,392 830,286 Z" fill="#FFFFFF" '
         f'fill-opacity="0.75"/>',
         f'<path d="M796,520 L900,470 L920,640 L816,672 Z" fill="{PAPER}" fill-opacity="0.55"/>',
         pencil(1310, 700, 230, -22)]
    return _arc("".join(b))


def p_a_rel():
    return _arc(sheet(360, 230, 500, 440, -6) + sheet(740, 300, 500, 440, 5)
                + f'<rect x="845" y="300" width="7" height="370" fill="{RULE}"/>')


def p_a_tra():
    """A folded wool blanket with a card and a grounding stone resting on it."""
    b = [f'<rect x="250" y="300" width="1000" height="430" rx="30" fill="#BFB19A" '
         f'filter="url(#sh)"/>']
    for i in range(4):
        y = 330 + i * 100
        b.append(f'<rect x="270" y="{y}" width="960" height="86" rx="22" '
                 f'fill="{"#D3C6AE" if i % 2 else "#C7B89E"}"/>')
        b.append(f'<rect x="270" y="{y + 80}" width="960" height="7" fill="#B2A48C"/>')
    b.append(sheet(520, 250, 400, 300, -4))
    b.append(f'<ellipse cx="1060" cy="330" rx="92" ry="66" fill="#8E8A84" filter="url(#shs)"/>')
    b.append(f'<ellipse cx="1040" cy="310" rx="52" ry="32" fill="#A7A29A"/>')
    return _arc("".join(b))


def p_a_grf():
    return _arc(sheet(330, 170, 940, 570, -2) + stem(430, 620, 760, -26)
                + f'<ellipse cx="1130" cy="690" rx="30" ry="14" fill="#C2B79B" '
                  f'fill-opacity="0.9" transform="rotate(18 1130 690)"/>')


def p_a_cmp():
    b = [sheet(420, 220, 760, 520, 2),
         f'<circle cx="790" cy="470" r="185" fill="none" stroke="#C9BFA8" stroke-width="17"/>',
         f'<path d="M958,398 Q1130,320 1250,430" fill="none" stroke="#C9BFA8" stroke-width="17" '
         f'stroke-linecap="round"/>']
    return _arc("".join(b))


def p_a_val():
    b = [sheet(390, 180, 820, 590, -2),
         f'<circle cx="800" cy="470" r="150" fill="#C0B394" filter="url(#sh)"/>',
         f'<circle cx="800" cy="470" r="124" fill="#EFE7D4"/>',
         f'<circle cx="800" cy="470" r="104" fill="#E3D9C2"/>',
         f'<path d="M800,380 L832,470 L800,560 L768,470 Z" fill="{RUST}" fill-opacity="0.8"/>',
         f'<circle cx="800" cy="470" r="14" fill="#C0B394"/>']
    return _arc("".join(b))


def p_a_ang():
    b = [f'<ellipse cx="880" cy="600" rx="230" ry="88" fill="#DCD3C0" filter="url(#sh)"/>',
         f'<ellipse cx="880" cy="588" rx="196" ry="70" fill="#E9E2D3"/>',
         f'<g transform="rotate(-16 880 570)">'
         f'<rect x="700" y="556" width="360" height="17" rx="8" fill="#D8C7A8"/>'
         f'<circle cx="1064" cy="564" r="24" fill="#3E3A35"/></g>',
         f'<path d="M1074,520 q42,-70 -8,-124 q64,44 32,124" fill="#FFFFFF" fill-opacity="0.5"/>',
         sheet(280, 250, 380, 300, -5)]
    return _arc("".join(b))


def p_a_slp():
    b = [sheet(280, 180, 940, 560)]
    for c in range(7):
        x = 340 + c * 124
        b.append(f'<rect x="{x}" y="240" width="100" height="440" rx="5" fill="none" '
                 f'stroke="{RULE}" stroke-width="3"/>')
        b.append(ruled(x + 14, 290, 70, 4, 96, GRAPH, 5, jitter=False))
    b.append(f'<circle cx="1360" cy="470" r="118" fill="#C0B394" filter="url(#sh)"/>')
    b.append(f'<circle cx="1360" cy="470" r="96" fill="#D9CEB6"/>')
    return _arc("".join(b), )


def p_a_wrk():
    b = [f'<rect x="330" y="300" width="940" height="380" rx="22" fill="#C9C3B8" '
         f'filter="url(#sh)"/>',
         f'<rect x="366" y="336" width="868" height="308" rx="14" fill="#D8D2C6"/>',
         sheet(640, 250, 420, 300, -4), pencil(690, 400, 300, -8)]
    return _arc("".join(b))


def p_a_prg():
    b = []
    for i in range(9):
        b.append(f'<rect x="{430 - i * 3}" y="{640 - i * 36}" width="700" height="60" rx="8" '
                 f'fill="{"#EFE6D5" if i % 2 else "#E7DDC9"}" filter="url(#shs)"/>')
    b.append(f'<rect x="700" y="300" width="26" height="400" rx="8" fill="#D4C7AC"/>')
    b.append(sheet(760, 200, 420, 240, 6))
    return _arc("".join(b))


# ---- the three worksheets ---------------------------------------------------
def p_w1_sheet():
    b = [clipboard(90, 110, 890, 1400),
         ruled(190, 330, 500, 2, 52, RULE, 4),
         grid(190, 500, 700, 720, 6, 8),
         pencil(250, 1330, 400, -5)]
    return svg(W23, H23, "".join(b))


def p_w2_goal():
    b = [sheet(90, 150, 890, 1330, -1),
         ruled(180, 330, 660, 5, 96, RULE, 4)]
    by = 1130
    b.append(f'<rect x="180" y="{by}" width="700" height="7" rx="3.5" fill="{INK2}" '
             f'fill-opacity="0.5"/>')
    for k in range(11):
        gx = 180 + 700 * k / 10.0
        b.append(f'<rect x="{gx - 2.5}" y="{by - (11 if k % 5 == 0 else 7)}" width="5.5" '
                 f'height="{30 if k % 5 == 0 else 20}" rx="2.5" fill="{INK2}" fill-opacity="0.5"/>')
    b.append(pencil(230, 1300, 380, -6))
    b.append(f'<rect x="700" y="1270" width="150" height="66" rx="14" fill="{PAPER_D}" '
             f'filter="url(#shs)"/>')
    return svg(W23, H23, "".join(b))


def p_w3_caseload():
    b = [sheet(90, 150, 890, 1330, 1), grid(170, 300, 730, 1030, 5, 11),
         pencil(560, 240, 330, 6)]
    return svg(W23, H23, "".join(b))


PLATES = {
    "h0-cover": p_h0_cover, "h1-method": p_h1_method, "h2-arcs": p_h2_arcs,
    "h3-sheets": p_h3_sheets, "h9-back": p_h9_back,
    "c1-months": p_c1_months, "c2-anatomy": p_c2_anatomy, "c3-three": p_c3_three,
    "k1-ontrack": p_k1_ontrack, "k2-stalled": p_k2_stalled, "k3-worse": p_k3_worse,
    "m1-choose": p_m1_choose, "l1-licence": p_l1_licence,
    "q1-phq": p_q1_phq, "q2-gad": p_q2_gad,
    "r1-hand": p_r1_hand, "r2-mark": p_r2_mark, "r3-plot": p_r3_plot,
    "r4-compare": p_r4_compare, "r5-decide": p_r5_decide,
    "t1-script": p_t1_script, "t2-words": p_t2_words,
    "n1-note": p_n1_note, "b1-stop": p_b1_stop,
    "p1-chart": p_p1_chart, "p2-lies": p_p2_lies, "s1-short": p_s1_short,
    "x1-reading": p_x1_reading,
    "a-int": p_a_int, "a-emo": p_a_emo, "a-anx": p_a_anx, "a-dep": p_a_dep,
    "a-str": p_a_str, "a-sw": p_a_sw, "a-rel": p_a_rel, "a-tra": p_a_tra,
    "a-grf": p_a_grf, "a-cmp": p_a_cmp, "a-val": p_a_val, "a-ang": p_a_ang,
    "a-slp": p_a_slp, "a-wrk": p_a_wrk, "a-prg": p_a_prg,
    "w1-sheet": p_w1_sheet, "w2-goal": p_w2_goal, "w3-caseload": p_w3_caseload,
}
