# -*- coding: utf-8 -*-
"""
armado_svg.py — Pagina 4: Assembly (SVG que embebe la foto-grilla).

Estructura:
  * Grilla de 8 pasos (2 columnas x 4 filas). Si existe la foto-grilla
    (hf/<id>_grid.png) se embebe como PNG base64; si no, placeholder.
  * Numeros de paso dibujados por el SVG (badge naranja), NUNCA por la
    imagen -> asi Nano Banana no tiene que escribir numeros.
  * 8 captions tipografiados (2 col x 4 fil), "detalle con mm", wrap 3 lineas.
    El paso 8 cierra en el acabado.

Todo en ingles, medidas en mm.
"""
import base64
import os
import svg_base as B
import armado_pasos


def _grid_datauri(plan):
    for path in (f"hf/{plan['id']}_grid.png", f"hf/{plan['id']}_grid.jpg"):
        if os.path.exists(path):
            mime = "image/png" if path.endswith("png") else "image/jpeg"
            with open(path, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return None


def _badge(cx, cy, n):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="{B.ORANGE}" '
            f'stroke="{B.WHITE}" stroke-width="1.5"/>'
            f'{B.t(cx, cy+4, str(n), size=12.5, weight="bold", fill=B.WHITE, anchor="middle")}')


def render(plan, grid_uri=None):
    s = [B.header("Assembly", plan)]
    steps = armado_pasos.pasos_en(plan)
    if grid_uri is None:
        grid_uri = _grid_datauri(plan)

    # --- grilla 2x4 ---
    gx, gy = B.MARGIN, 100
    gw = B.PAGE_W - 2 * B.MARGIN
    gh = 516
    cols, rows = 2, 4
    cw, ch = gw / cols, gh / rows

    if grid_uri:
        s.append(f'<clipPath id="gc"><rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="3"/></clipPath>')
        s.append(f'<image href="{grid_uri}" x="{gx}" y="{gy}" width="{gw}" height="{gh}" '
                 f'preserveAspectRatio="xMidYMid slice" clip-path="url(#gc)"/>')
    else:
        # placeholder: hatch + faint number
        for i in range(8):
            r, c = divmod(i, cols)
            px, py = gx + c * cw, gy + r * ch
            s.append(B.rect(px, py, cw, ch, fill=(B.PANEL if (i % 2 == 0) else "#F1EEE9"), stroke="none"))
            s.append(B.t(px + cw / 2, py + ch / 2 + 14, str(i + 1), size=44, weight="bold",
                         fill="#E4DED4", anchor="middle"))
            s.append(B.t(px + cw / 2, py + ch - 14, "step photo pending", size=9,
                         fill=B.INK_FAINT, anchor="middle", font=B.MONO))

    # gutters + border + badges (siempre por SVG)
    s.append(B.rect(gx, gy, gw, gh, fill="none", stroke=B.WHITE if grid_uri else B.LINE, sw=3, rx=3))
    for c in range(1, cols):
        s.append(B.line(gx + c * cw, gy, gx + c * cw, gy + gh, stroke=B.WHITE, sw=3))
    for r in range(1, rows):
        s.append(B.line(gx, gy + r * ch, gx + gw, gy + r * ch, stroke=B.WHITE, sw=3))
    for i in range(8):
        r, c = divmod(i, cols)
        s.append(_badge(gx + c * cw + 20, gy + r * ch + 20, i + 1))

    # --- captions 2x4 ---
    cap_top = gy + gh + 22
    s.append(B.section_title(gx, cap_top - 6, "Build steps"))
    cap_top += 10
    col_w = gw / 2
    row_h = (B.PAGE_H - 40 - cap_top) / 4
    for i, step in enumerate(steps):
        r, c = divmod(i, 2)   # 1-2 fila0, ... llena por filas: 1|2 / 3|4 ...
        cx = gx + c * col_w
        cy = cap_top + r * row_h
        s.append(_badge(cx + 12, cy + 10, i + 1))
        yy = cy + 6
        for ln in B.wrap(step, 44)[:3]:
            s.append(B.t(cx + 32, yy, ln, size=9.6, fill=B.CARBON))
            yy += 13

    s.append(B.footer(plan, 4))
    return B.document("\n".join(s))
