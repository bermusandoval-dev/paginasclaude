# -*- coding: utf-8 -*-
"""
ensamblar.py — Compone el PDF de 4 paginas (300 dpi) por plano.

Cada pagina se genera como SVG y se rasteriza a un PDF vectorial A4 con
cairosvg (794 px @ 96 dpi -> 210 mm exactos); las 4 se unen con pypdf.
Las imagenes IA embebidas (portada/grilla) van a su resolucion nativa.

Uso:
    python ensamblar.py MM-0751 MM-0155 ...   # ids sueltos
    python ensamblar.py --pilotos             # 1 por familia (mayor score)
    python ensamblar.py --todos               # las 1200 (tandas)
"""
import io
import json
import os
import sys

import cairosvg
from pypdf import PdfWriter, PdfReader

import portada_svg
import materiales_svg
import planos_svg
import armado_svg

OUT_DIR = "pdf"
PAGINAS = [portada_svg, materiales_svg, planos_svg, armado_svg]


def _svg_to_pdf_bytes(svg):
    return cairosvg.svg2pdf(bytestring=svg.encode("utf-8"))


def ensamblar_uno(plan):
    os.makedirs(OUT_DIR, exist_ok=True)
    writer = PdfWriter()
    for mod in PAGINAS:
        svg = mod.render(plan)
        pdf_bytes = _svg_to_pdf_bytes(svg)
        reader = PdfReader(io.BytesIO(pdf_bytes))
        writer.add_page(reader.pages[0])
    out = os.path.join(OUT_DIR, f"{plan['id']}.pdf")
    with open(out, "wb") as fh:
        writer.write(fh)
    return out


def pilotos(planes):
    """1 plano por familia: el de mayor score (mas completo) para probar."""
    best = {}
    for p in planes:
        f = p["familia"]
        if f not in best or p["score"] > best[f]["score"]:
            best[f] = p
    return [best[f] for f in sorted(best)]


def main():
    planes = json.load(open("catalogo.json", encoding="utf-8"))
    by_id = {p["id"]: p for p in planes}
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        return
    if args[0] == "--pilotos":
        objetivo = pilotos(planes)
    elif args[0] == "--todos":
        objetivo = planes
    else:
        objetivo = [by_id[a] for a in args if a in by_id]

    print(f"Ensamblando {len(objetivo)} PDF(s)...")
    for i, plan in enumerate(objetivo, 1):
        out = ensamblar_uno(plan)
        cover = "foto" if os.path.exists(f"hf/{plan['id']}_cover.png") else "placeholder"
        print(f"  [{i}/{len(objetivo)}] {out}  (cover: {cover})")


if __name__ == "__main__":
    main()
