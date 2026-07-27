# -*- coding: utf-8 -*-
"""
materiales_svg.py — Pagina 2: Materials, Hardware, Tools & Safety (SVG).

Data-driven: sirve para los 1200 planos. Todo en ingles, medidas en mm.
"""
import svg_base as B


def _list(x, y, chars, items, size=11, lh=15.5, gap=4, fill=B.CARBON):
    """Renderiza items (strings) con bullet naranja y wrap. -> (svg, y)."""
    out = []
    for it in items:
        lines = B.wrap(it, chars)
        out.append(f'<circle cx="{x-9:.1f}" cy="{y-3.5:.1f}" r="1.9" fill="{B.ORANGE}"/>')
        for j, ln in enumerate(lines):
            out.append(B.t(x, y, ln, size=size, fill=fill if j == 0 else B.INK_SOFT))
            y += lh
        y += gap
    return "\n".join(out), y


def _hardware_items(plan):
    out = []
    for h in plan["herrajes"]:
        q = f"  x{h['cantidad']}" if h.get("cantidad") else ""
        out.append(f"{h['item']}{q}  ({h['para_que']})")
    return out


def _tools_items(plan):
    return [f"{t['item']} — {t['uso']}" for t in plan["herramientas"]]


def render(plan):
    s = [B.header("Materials & Tools", plan)]

    # --- info strip ---
    iy = 108
    d = plan["dims"]
    info = [
        ("Join method", plan["union"]),
        ("Finish", plan["acabado_label"]),
        ("Surface prep", plan["desbaste"]),
    ]
    s.append(B.rect(B.MARGIN, iy - 18, B.PAGE_W - 2 * B.MARGIN, 58,
                    fill=B.PANEL, stroke=B.LINE, sw=1, rx=3))
    colw = (B.PAGE_W - 2 * B.MARGIN) / 3
    for i, (k, v) in enumerate(info):
        cx = B.MARGIN + 14 + i * colw
        s.append(B.t(cx, iy, k.upper(), size=8.5, weight="bold",
                     fill=B.INK_FAINT, font=B.MONO, spacing="0.8"))
        for j, ln in enumerate(B.wrap(v, 34)[:2]):
            s.append(B.t(cx, iy + 16 + j * 13, ln, size=10.5, fill=B.CARBON))

    # --- two columns ---
    col_l = B.MARGIN
    col_r = B.PAGE_W / 2 + 12
    top = 196

    # LEFT: Materials + Hardware
    y = top
    s.append(B.section_title(col_l, y, "Materials  ·  cut from 6 m bar stock"))
    s.append(B.line(col_l, y + 8, B.PAGE_W / 2 - 12, y + 8, stroke=B.LINE))
    svg, y = _list(col_l + 10, y + 30, 44, plan["materiales"])
    s.append(svg)

    y += 14
    s.append(B.section_title(col_l, y, "Hardware  ·  what each part is for"))
    s.append(B.line(col_l, y + 8, B.PAGE_W / 2 - 12, y + 8, stroke=B.LINE))
    svg, y = _list(col_l + 10, y + 30, 44, _hardware_items(plan))
    s.append(svg)

    # RIGHT: Tools + Safety
    y = top
    s.append(B.section_title(col_r, y, "Tools  ·  what each one does"))
    s.append(B.line(col_r, y + 8, B.PAGE_W - B.MARGIN, y + 8, stroke=B.LINE))
    svg, y = _list(col_r + 10, y + 30, 42, _tools_items(plan))
    s.append(svg)

    y += 14
    # Safety block: caja con acento
    s.append(B.section_title(col_r, y, "Safety  ·  read before you start"))
    box_y = y + 16
    svg, y2 = _list(col_r + 10, box_y + 18, 42, plan["seguridad"], size=10.5, lh=15)
    box_h = (y2 - box_y) + 6
    s.append(B.rect(col_r - 4, box_y - 2, B.PAGE_W - B.MARGIN - col_r + 8, box_h,
                    fill="#FFF6EE", stroke=B.ORANGE, sw=1, rx=3))
    s.append(B.rect(col_r - 4, box_y - 2, 3, box_h, fill=B.ORANGE))
    s.append(svg)

    s.append(B.footer(plan, 2))
    return B.document("\n".join(s))
