# -*- coding: utf-8 -*-
"""
exportar.py — Export maestro del catalogo.

Siempre escribe catalogo_maestro.csv (una fila por plano, resumen vendible).
Si openpyxl esta disponible, tambien escribe catalogo_maestro.xlsx.

Uso:  python exportar.py
"""
import csv
import json

COLUMNAS = [
    "id", "familia", "subcategoria", "titulo", "variante_label", "union",
    "dificultad", "weld", "acabado_label", "desbaste", "n_piezas",
    "n_herrajes", "n_herramientas", "cut_list_barras", "dims", "escena",
]


def fila(p):
    return {
        "id": p["id"],
        "familia": p["familia"],
        "subcategoria": p["subcategoria"],
        "titulo": p["titulo"],
        "variante_label": p["variante_label"],
        "union": p["union"],
        "dificultad": p["dificultad"],
        "weld": "yes" if p["weld"] else "no",
        "acabado_label": p["acabado_label"],
        "desbaste": p["desbaste"],
        "n_piezas": len(p["piezas"]),
        "n_herrajes": len(p["herrajes"]),
        "n_herramientas": len(p["herramientas"]),
        "cut_list_barras": " | ".join(p["cut_list_barras"]),
        "dims": json.dumps(p["dims"], ensure_ascii=False),
        "escena": p["escena"],
    }


def main():
    planes = json.load(open("catalogo.json", encoding="utf-8"))
    filas = [fila(p) for p in planes]

    with open("catalogo_maestro.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)
    print(f"OK  catalogo_maestro.csv  ({len(filas)} filas)")

    try:
        import openpyxl
        from openpyxl.styles import Font
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "MetalMaster"
        ws.append(COLUMNAS)
        for c in ws[1]:
            c.font = Font(bold=True)
        for f in filas:
            ws.append([f[c] for c in COLUMNAS])
        ws.freeze_panes = "A2"
        wb.save("catalogo_maestro.xlsx")
        print(f"OK  catalogo_maestro.xlsx  ({len(filas)} filas)")
    except ImportError:
        print("   (openpyxl no instalado; solo CSV. `pip install openpyxl` para el .xlsx)")


if __name__ == "__main__":
    main()
