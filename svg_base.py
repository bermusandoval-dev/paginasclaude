# -*- coding: utf-8 -*-
"""
svg_base.py — Lienzo A4 y primitivas compartidas para las paginas vectoriales.

Identidad visual MetalMaster: fondo blanco, acento naranja #FF7A1A, texto
carbon, sans limpia, franja naranja de 10 px al pie y footer
"MetalMaster    MM-XXXX  ·  Page N of 4".

A4 = 794 x 1123 px (96 dpi). El PDF final se rasteriza a 300 dpi en
ensamblar.py; aqui trabajamos en unidades de usuario = px de A4@96.
"""

PAGE_W = 794
PAGE_H = 1123
MARGIN = 44

# --- paleta ---
WHITE = "#FFFFFF"
ORANGE = "#FF7A1A"
ORANGE_DK = "#C85A08"
CARBON = "#20201E"
INK_SOFT = "#615C55"
INK_FAINT = "#9A938A"
LINE = "#E4E0D8"
LINE_STRONG = "#C7C1B6"
STEEL = "#4F5B68"
PANEL = "#F7F5F1"

FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Liberation Mono, monospace"

BRAND = "MetalMaster"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def t(x, y, s, size=12, weight="normal", fill=CARBON, anchor="start",
      font=FONT, spacing=None, italic=False, opacity=None):
    extra = ""
    if spacing is not None:
        extra += f' letter-spacing="{spacing}"'
    if italic:
        extra += ' font-style="italic"'
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1, rx=0, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')


def line(x1, y1, x2, y2, stroke=LINE_STRONG, sw=1, dash=None, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')


def circle(cx, cy, r, fill="none", stroke=CARBON, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def polyline(pts, fill="none", stroke=CARBON, sw=1, dash=None, closed=False):
    tag = "polygon" if closed else "polyline"
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def wrap(text, maxchars):
    """Envuelve por palabras a <= maxchars por linea."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= maxchars:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, size=11, maxchars=60, lh=15, fill=CARBON, weight="normal",
         bullet=None, max_lines=None):
    """Bloque de texto con wrap. Devuelve (svg, y_final)."""
    lines = wrap(text, maxchars)
    if max_lines:
        lines = lines[:max_lines]
    out = []
    for i, ln in enumerate(lines):
        pref = ""
        xx = x
        if bullet and i == 0:
            out.append(f'<circle cx="{x-8:.1f}" cy="{y-4:.1f}" r="1.7" fill="{ORANGE}"/>')
        elif bullet:
            xx = x
        out.append(t(xx, y, ln, size=size, weight=weight, fill=fill))
        y += lh
    return "\n".join(out), y


# --------------------------------------------------------------------------
def header(page_title, plan):
    """Banda superior: titulo de pagina + wordmark + id + tira fina naranja."""
    s = []
    s.append(t(MARGIN, 50, page_title, size=25, weight="bold", fill=CARBON))
    # subtitulo: titulo del plano
    s.append(t(MARGIN, 72, plan["titulo"], size=11.5, fill=INK_SOFT))
    # wordmark derecha
    s.append(t(PAGE_W - MARGIN, 40, BRAND, size=15, weight="bold",
               fill=ORANGE, anchor="end"))
    s.append(t(PAGE_W - MARGIN, 57, plan["id"], size=11, fill=INK_SOFT,
               anchor="end", font=MONO))
    s.append(t(PAGE_W - MARGIN, 72, plan["dificultad"], size=10, fill=STEEL,
               anchor="end", font=MONO))
    s.append(line(MARGIN, 84, PAGE_W - MARGIN, 84, stroke=CARBON, sw=1.5))
    return "\n".join(s)


def footer(plan, page_no):
    s = []
    fy = PAGE_H - 26
    s.append(t(MARGIN, fy, BRAND, size=10, weight="bold", fill=INK_SOFT))
    s.append(t(PAGE_W - MARGIN, fy, f"{plan['id']}  ·  Page {page_no} of 4",
               size=10, fill=INK_SOFT, anchor="end", font=MONO))
    # franja naranja 10 px al pie
    s.append(rect(0, PAGE_H - 10, PAGE_W, 10, fill=ORANGE))
    return "\n".join(s)


def section_title(x, y, label):
    """Encabezado de seccion en naranja con regla fina."""
    s = [t(x, y, label.upper(), size=12, weight="bold", fill=ORANGE_DK,
           spacing="1.2")]
    return "\n".join(s)


def document(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" '
            f'height="{PAGE_H}" viewBox="0 0 {PAGE_W} {PAGE_H}">\n'
            f'{rect(0,0,PAGE_W,PAGE_H,fill=WHITE)}\n{body}\n</svg>')
