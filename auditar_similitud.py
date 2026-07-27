# -*- coding: utf-8 -*-
"""
auditar_similitud.py — Antidoto contra "todas las hojas se ven iguales".

Para cada par de GEMELOS (misma subcategoria Y misma variante) verifica que:
  1. NO compartan 2 o mas de {union, acabado, desbaste}.
     (Comparten la union por ser la misma variante -> ergo acabado y desbaste
      DEBEN diferir; el catalogo lo garantiza por construccion, esto lo prueba.)
  2. NO tengan la lista de herrajes Y la de herramientas identicas a la vez.

Tambien reporta metricas globales de variedad.

Uso:  python auditar_similitud.py
"""
import json
import sys
from collections import defaultdict
from itertools import combinations


def firma_herrajes(p):
    return tuple(sorted(h["item"] for h in p["herrajes"]))


def firma_herramientas(p):
    return tuple(sorted(t["item"] for t in p["herramientas"]))


def main():
    planes = json.load(open("catalogo.json", encoding="utf-8"))
    grupos = defaultdict(list)
    for p in planes:
        grupos[(p["subcategoria"], p["variante"])].append(p)

    fallos = []
    pares = 0
    for (subcat, var), gs in grupos.items():
        for a, b in combinations(gs, 2):
            pares += 1
            comparten = 0
            if a["union"] == b["union"]:
                comparten += 1
            if a["acabado"] == b["acabado"]:
                comparten += 1
            if a["desbaste"] == b["desbaste"]:
                comparten += 1
            if comparten >= 2:
                fallos.append((a["id"], b["id"], f"comparten {comparten} de union/acabado/desbaste"))
            if firma_herrajes(a) == firma_herrajes(b) and firma_herramientas(a) == firma_herramientas(b):
                fallos.append((a["id"], b["id"], "herrajes Y herramientas identicos"))

    print(f"Planos: {len(planes)}   Pares de gemelos comprobados: {pares}   Fallos: {len(fallos)}")
    for a, b, m in fallos[:30]:
        print(f"  {a} vs {b}: {m}")

    # metricas de variedad globales
    from collections import Counter
    print("\nVariedad global:")
    print("  Acabados:", dict(Counter(p["acabado"] for p in planes)))
    print("  Variantes distintas:", len(set((p["arquetipo"], p["variante"]) for p in planes)))
    weld = Counter(p["weld"] for p in planes)
    print(f"  Con soldadura: {weld[True]}   Sin soldadura: {weld[False]}")

    if fallos:
        sys.exit(1)
    print("\nAUDITORIA LIMPIA: ningun par de gemelos es intercambiable.")
    sys.exit(0)


if __name__ == "__main__":
    main()
