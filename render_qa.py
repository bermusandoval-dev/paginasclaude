# -*- coding: utf-8 -*-
"""
render_qa.py — Rasteriza una pagina SVG a PNG para QA visual.

Uso:  python render_qa.py <MM-XXXX> <pagina 2|3|4> [salida.png]
"""
import json
import sys
import importlib
import cairosvg

GEN = {1: "portada_svg", 2: "materiales_svg", 3: "planos_svg", 4: "armado_svg"}


def plan_por_id(pid):
    for p in json.load(open("catalogo.json", encoding="utf-8")):
        if p["id"] == pid:
            return p
    raise SystemExit(f"no existe {pid}")


def main():
    pid = sys.argv[1]
    page = int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else f"qa_{pid}_p{page}.png"
    plan = plan_por_id(pid)
    svg = importlib.import_module(GEN[page]).render(plan)
    with open(out.replace(".png", ".svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out,
                     output_width=794, output_height=1123, background_color="white")
    print("OK", out)


if __name__ == "__main__":
    main()
