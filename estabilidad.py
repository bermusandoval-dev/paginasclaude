# -*- coding: utf-8 -*-
"""
estabilidad.py — Snapshot + diff de estabilidad (REGLA DURA del proyecto).

Antes de tocar catalogo.py cuando ya hay planos ENTREGADOS:
    1) python estabilidad.py snapshot X      -> guarda _catalogo_pre_X.json
    2) (editas catalogo.py y regeneras)
    3) python estabilidad.py diff X          -> verifica 0 cambios criticos

Campos criticos (si cambian en un plano ya entregado, hay que re-ensamblar
y re-subir ese PDF): dims, piezas, variante, titulo, familia, subcategoria.
La DIFICULTAD puede moverse por el re-ranking global: se reporta aparte
(no es fallo, pero lista los IDs afectados para re-ensamblar su footer).

Uso:
    python estabilidad.py snapshot <etiqueta>
    python estabilidad.py diff <etiqueta> [id_ini id_fin]
"""
import json
import sys
import hashlib

CRITICOS = ("dims", "piezas", "variante", "titulo", "familia", "subcategoria")


def cargar(path):
    return {p["id"]: p for p in json.load(open(path, encoding="utf-8"))}


def huella(plan):
    payload = {k: plan[k] for k in CRITICOS}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def cmd_snapshot(etiqueta):
    data = json.load(open("catalogo.json", encoding="utf-8"))
    out = f"_catalogo_pre_{etiqueta}.json"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Snapshot guardado: {out}  ({len(data)} planos)")


def cmd_diff(etiqueta, rango=None):
    snap = cargar(f"_catalogo_pre_{etiqueta}.json")
    cur = cargar("catalogo.json")
    ids = sorted(snap.keys())
    if rango:
        lo, hi = rango
        ids = [i for i in ids if lo <= int(i.split("-")[1]) <= hi]

    criticos, dif_movida, faltantes = [], [], []
    for pid in ids:
        if pid not in cur:
            faltantes.append(pid)
            continue
        if huella(snap[pid]) != huella(cur[pid]):
            campos = [k for k in CRITICOS if snap[pid][k] != cur[pid][k]]
            criticos.append((pid, campos))
        if snap[pid].get("dificultad") != cur[pid].get("dificultad"):
            dif_movida.append((pid, snap[pid].get("dificultad"), cur[pid].get("dificultad")))

    print(f"Comprobados {len(ids)} planos entregados.")
    print(f"  Cambios CRITICOS: {len(criticos)}")
    for pid, campos in criticos[:40]:
        print(f"    {pid}: {campos}")
    if faltantes:
        print(f"  IDs que DESAPARECIERON: {len(faltantes)} -> {faltantes[:20]}")
    print(f"  Dificultad re-rankeada (re-ensamblar footer): {len(dif_movida)}")
    for pid, a, b in dif_movida[:40]:
        print(f"    {pid}: {a} -> {b}")

    if criticos or faltantes:
        print("\nFALLO: hay cambios criticos en planos entregados. NO subir hasta resolver.")
        sys.exit(1)
    print("\nOK: 0 cambios criticos en el rango entregado.")
    sys.exit(0)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    modo, etiqueta = sys.argv[1], sys.argv[2]
    if modo == "snapshot":
        cmd_snapshot(etiqueta)
    elif modo == "diff":
        rango = None
        if len(sys.argv) >= 5:
            rango = (int(sys.argv[3]), int(sys.argv[4]))
        cmd_diff(etiqueta, rango)
    else:
        print("modo desconocido:", modo)
        sys.exit(2)


if __name__ == "__main__":
    main()
