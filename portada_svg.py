# -*- coding: utf-8 -*-
"""
portada_svg.py — Pagina 1: Cover (foto a sangre + banda de identidad).

Embebe la portada IA (hf/<id>_cover.png) a sangre; una banda blanca al pie
lleva el titulo, la marca, el ID y "4-page build plan", con la franja
naranja de 10 px. Si no hay foto, placeholder limpio.
"""
import base64
import os
import svg_base as B


def _cover_datauri(plan):
    for path in (f"hf/{plan['id']}_cover.png", f"hf/{plan['id']}_cover.jpg"):
        if os.path.exists(path):
            mime = "image/png" if path.endswith("png") else "image/jpeg"
            with open(path, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return None


def render(plan, cover_uri=None):
    if cover_uri is None:
        cover_uri = _cover_datauri(plan)
    band_h = 96
    photo_h = B.PAGE_H - band_h
    s = []

    if cover_uri:
        s.append(f'<clipPath id="cc"><rect x="0" y="0" width="{B.PAGE_W}" height="{photo_h}"/></clipPath>')
        s.append(f'<image href="{cover_uri}" x="0" y="0" width="{B.PAGE_W}" height="{photo_h}" '
                 f'preserveAspectRatio="xMidYMid slice" clip-path="url(#cc)"/>')
    else:
        s.append(B.rect(0, 0, B.PAGE_W, photo_h, fill=B.PANEL))
        s.append(B.t(B.PAGE_W / 2, photo_h / 2 - 6, "COVER PHOTO", size=20, weight="bold",
                     fill="#D8D2C8", anchor="middle", font=B.MONO))
        s.append(B.t(B.PAGE_W / 2, photo_h / 2 + 18, "3:4 · 4K · Nano Banana Pro", size=11,
                     fill=B.INK_FAINT, anchor="middle", font=B.MONO))

    # tag superior
    s.append(B.rect(B.MARGIN, 30, 118, 26, fill=B.ORANGE, rx=2))
    s.append(B.t(B.MARGIN + 12, 47, "BUILD PLAN", size=12, weight="bold", fill=B.WHITE, font=B.MONO, spacing="1"))

    # banda de identidad al pie
    by = photo_h
    s.append(B.rect(0, by, B.PAGE_W, band_h, fill=B.WHITE))
    s.append(B.line(0, by, B.PAGE_W, by, stroke=B.LINE, sw=1))
    # titulo (2 lineas max)
    title_lines = B.wrap(plan["titulo"], 44)[:2]
    ty = by + 34 if len(title_lines) == 2 else by + 42
    for ln in title_lines:
        s.append(B.t(B.MARGIN, ty, ln, size=17, weight="bold", fill=B.CARBON))
        ty += 21
    s.append(B.t(B.MARGIN, by + band_h - 16, f"{plan['familia']}  ·  {plan['dificultad']}",
                 size=10.5, fill=B.INK_SOFT))
    # derecha: marca + id
    s.append(B.t(B.PAGE_W - B.MARGIN, by + 32, B.BRAND, size=18, weight="bold",
                 fill=B.ORANGE, anchor="end"))
    s.append(B.t(B.PAGE_W - B.MARGIN, by + 52, plan["id"], size=12, fill=B.INK_SOFT,
                 anchor="end", font=B.MONO))
    s.append(B.t(B.PAGE_W - B.MARGIN, by + band_h - 16, "4-page build plan · A4 · 300 dpi",
                 size=10, fill=B.INK_FAINT, anchor="end", font=B.MONO))
    # franja naranja
    s.append(B.rect(0, B.PAGE_H - 10, B.PAGE_W, 10, fill=B.ORANGE))
    return B.document("\n".join(s))
