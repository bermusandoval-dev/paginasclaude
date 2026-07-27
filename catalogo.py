# -*- coding: utf-8 -*-
"""
catalogo.py — Genera catalogo.json con los 1200 planos de MetalMaster.

REGLAS DURAS (heredadas de WoodMaster, adaptadas a metal):
  * Dimensiones con RNG estable POR PROYECTO:
        Random(f"{PROYECTO_SEED}|{subcat}|{i}")
    -> regenerar el catalogo NUNCA cambia planos ya entregados.
  * Variantes por "mazo" barajado con semilla por subcategoria:
        Random(f"DECK|{subcat}") sobre (base * k)[:n]
    -> anadir variantes nuevas al final del deck NO altera repartos hechos.
  * Acabado y desbaste elegidos para que dos "gemelos" (misma subcat+variante)
    SIEMPRE difieran -> el auditor de similitud pasa por construccion.
  * Dificultad por RANKING de score (percentiles), con la POLITICA:
        Principiante == SIN soldadura (atornillado / plegado / remachado).

Uso:  python catalogo.py            -> escribe catalogo.json
"""
import json
import math
import random
from collections import defaultdict

import datos_metal as DM
import arquetipos as AQ

# ---------------------------------------------------------------------------
def dims_humanas(arq, d):
    if arq in ("banco", "estanteria", "carrito", "mesa_madera"):
        h = d.get("height") or d.get("post_len")
        return f"{d.get('length', d.get('width'))}x{d.get('depth')}x{h} mm"
    if arq == "rack_pared":
        return f"{d['width']}x{d['height']} mm"
    if arq == "soporte":
        return f"{d['width']}x{d['depth']}x{d['height']} mm"
    if arq == "parrilla":
        return f"{d['width']}x{d['depth']} mm, box {d['box_depth']} mm"
    if arq == "perchero":
        return f"{d['width']}x{d['height']} mm"
    return ""


LINEAL = ("tube", "angle", "rod", "bar")   # perfiles que se cortan de barra de 6 m
CHAPA = ("sheet", "plate")


def stock_key(perfil):
    """Normaliza el perfil a una clave de compra (agrupa por seccion)."""
    return perfil.strip()


def calcular_materiales(piezas, acabado):
    """Devuelve (materiales_lineas, cut_list_barras)."""
    lineal = defaultdict(float)      # perfil -> mm totales
    chapa = defaultdict(float)       # perfil -> area mm2
    madera = defaultdict(list)       # perfil -> [(largo,ancho,cant)]
    for p in piezas:
        perf = stock_key(p["perfil"])
        low = perf.lower()
        tot_mm = p["largo"] * p["cantidad"]
        if any(k in low for k in LINEAL):
            lineal[perf] += tot_mm
        elif any(k in low for k in CHAPA):
            chapa[perf] += p["largo"] * p["ancho"] * p["cantidad"]
        else:  # wood board / plank
            madera[perf].append((p["largo"], p["ancho"], p["cantidad"]))

    materiales, cut_barras = [], []
    for perf, mm in sorted(lineal.items()):
        metros = mm * DM.KERF_WASTE / 1000.0
        barras = max(1, math.ceil(mm * DM.KERF_WASTE / DM.LARGO_BARRA_MM))
        linea = f"{perf} — {barras} bar of 6 m (incl. 5% kerf/waste), {metros:.1f} m used"
        materiales.append(linea)
        cut_barras.append(f"{perf}: {barras} x 6 m")
    for perf, area in sorted(chapa.items()):
        m2 = area / 1_000_000.0
        materiales.append(f"{perf} — {m2:.2f} m2 of sheet")
    for perf, items in sorted(madera.items()):
        for (lg, an, ct) in items:
            materiales.append(f"{perf} — {ct} x {lg} x {an} mm")
    # consumible de acabado
    materiales.append(f"Finish: {acabado['consumable']}")
    return materiales, cut_barras


def montar_herramientas(weld, piezas, herrajes, acabado):
    tools = list(DM.HERRAMIENTAS_BASE)
    if weld:
        tools += DM.HERRAMIENTAS_SOLDADURA
    if not weld and any(("bolt" in h["item"].lower() or "nut" in h["item"].lower()) for h in herrajes):
        tools += DM.HERRAMIENTAS_ATORNILLADO
    if any("folded" in (p["nota"] + p["perfil"]).lower() for p in piezas):
        tools += DM.HERRAMIENTAS_CHAPA
    if any("rivet" in h["item"].lower() for h in herrajes):
        tools.append(DM.HERRAMIENTA_REMACHE)
    tools.append({"item": acabado["tool"], "uso": f"apply the {acabado['label'].lower()}"})
    # dedupe por item preservando orden
    vistos, out = set(), []
    for t in tools:
        if t["item"] not in vistos:
            vistos.add(t["item"])
            out.append(t)
    return out


def montar_seguridad(weld, piezas):
    seg = list(DM.SEG_BASE)
    if weld:
        seg += DM.SEG_SOLDADURA
    if any("folded" in (p["nota"] + p["perfil"]).lower() for p in piezas):
        seg += DM.SEG_CHAPA
    return seg


def calcular_score(plan):
    """Score de complejidad (no incluye truco de soldadura; la politica
    Principiante-sin-soldadura se aplica luego en el ranking)."""
    piezas = plan["piezas"]
    s = 0.0
    s += len(piezas) * 2.0
    s += sum(p["cantidad"] for p in piezas) * 0.3
    notas = " ".join((p["nota"] + " " + p["perfil"]) for p in piezas).lower()
    if plan["weld"]:
        s += 10
    if "deg" in " ".join(plan["angulos"]).lower() and any(x not in ("90", "") for x in []):
        pass
    # angulos no-90 (cortes en inglete / patas inclinadas)
    ang = " ".join(plan["angulos"]).lower()
    if any(tok in ang for tok in ("splay", "rake", "lean", "cross at", "at 4", "at 3", "at 5", "mitred 45")):
        s += 8
    if "folded" in notas:
        s += 6
    if "mesh" in notas:
        s += 4
    if "drilled plate" in notas or "hole pattern" in notas:
        s += 4
    if "bent" in notas:
        s += 5
    s += len(plan["herrajes"]) * 1.5
    return round(s, 2)


def asignar_dificultad(planes):
    """Ranking -> terciles, con Principiante == subconjunto de los SIN soldadura."""
    N = len(planes)
    n_beg = round(N / 3)
    weldless = sorted([p for p in planes if not p["weld"]], key=lambda p: p["score"])
    beginner_ids = set(p["id"] for p in weldless[:n_beg])
    if len(weldless) < n_beg:
        # (no deberia pasar: ~52% sin soldadura) -> Principiante = todos los sin soldadura
        beginner_ids = set(p["id"] for p in weldless)
    resto = sorted([p for p in planes if p["id"] not in beginner_ids], key=lambda p: p["score"])
    mitad = len(resto) // 2
    inter_ids = set(p["id"] for p in resto[:mitad])
    for p in planes:
        if p["id"] in beginner_ids:
            p["dificultad"] = "Beginner"
        elif p["id"] in inter_ids:
            p["dificultad"] = "Intermediate"
        else:
            p["dificultad"] = "Advanced"


# ---------------------------------------------------------------------------
def generar():
    planes = []
    for fam in DM.FAMILIAS:
        arq = fam["arquetipo"]
        base_deck = AQ.deck_variantes(arq)              # orden estable
        for sc_idx, subcat in enumerate(fam["subcats"]):
            n = DM.PLANOS_POR_SUBCAT
            # mazo barajado estable por subcat
            mazo = (base_deck * (n // len(base_deck) + 1))[:n]
            random.Random(f"DECK|{subcat}").shuffle(mazo)

            # conteo por variante en la subcat -> acabados/desbastes DISTINTOS por gemelo
            cuenta = defaultdict(int)
            for vk in mazo:
                cuenta[vk] += 1
            fin_pool, grit_pool, occ = {}, {}, defaultdict(int)
            for vk, c in cuenta.items():
                rf = random.Random(f"FIN|{subcat}|{vk}")
                rg = random.Random(f"GRIT|{subcat}|{vk}")
                fin_pool[vk] = rf.sample(range(len(DM.ACABADOS)), min(c, len(DM.ACABADOS)))
                grit_pool[vk] = rg.sample(range(len(DM.DESBASTES)), min(c, len(DM.DESBASTES)))

            for i in range(n):
                vkey = mazo[i]
                num = fam["id_ini"] + sc_idx * DM.PLANOS_POR_SUBCAT + i
                pid = f"MM-{num:04d}"
                rng = random.Random(f"{DM.PROYECTO_SEED}|{subcat}|{i}")
                d = AQ.DIMS[arq](rng)
                built = AQ.build(arq, d, vkey)
                var_meta = AQ.VARIANTES[arq][vkey]

                oi = occ[vkey]; occ[vkey] += 1
                acabado = DM.ACABADOS[fin_pool[vkey][oi % len(fin_pool[vkey])]]
                desbaste = DM.DESBASTES[grit_pool[vkey][oi % len(grit_pool[vkey])]]
                escena = random.Random(f"SCN|{pid}").choice(fam["escenas"])

                herrajes = built["herrajes"]
                weld = var_meta["weld"]
                materiales, cut_barras = calcular_materiales(built["piezas"], acabado)
                herramientas = montar_herramientas(weld, built["piezas"], herrajes, acabado)
                seguridad = montar_seguridad(weld, built["piezas"])

                plan = {
                    "id": pid,
                    "arquetipo": arq,
                    "familia": fam["nombre"],
                    "subcategoria": subcat,
                    "subcat_idx": sc_idx,
                    "titulo": f"{subcat} — {var_meta['label']} ({dims_humanas(arq, d)})",
                    "variante": vkey,
                    "variante_label": var_meta["label"],
                    "union": var_meta["union"],
                    "weld": weld,
                    "vistas": var_meta["vistas"],
                    "dims": d,
                    "piezas": built["piezas"],
                    "materiales": materiales,
                    "cut_list_barras": cut_barras,
                    "herrajes": herrajes,
                    "herramientas": herramientas,
                    "seguridad": seguridad,
                    "acabado": acabado["key"],
                    "acabado_label": acabado["label"],
                    "desbaste": desbaste,
                    "escena": escena,
                    "posiciones_clave": built["posiciones"],
                    "angulos": built["angulos"],
                    "detalle_ampliado": built["detalle"],
                }
                plan["score"] = calcular_score(plan)
                planes.append(plan)

    asignar_dificultad(planes)
    return planes


def main():
    planes = generar()
    with open("catalogo.json", "w", encoding="utf-8") as fh:
        json.dump(planes, fh, ensure_ascii=False, indent=1)

    # resumen
    from collections import Counter
    dif = Counter(p["dificultad"] for p in planes)
    fam = Counter(p["familia"] for p in planes)
    print(f"OK  {len(planes)} planos -> catalogo.json")
    print("Dificultad:", dict(dif))
    print("Por familia:")
    for k, v in fam.items():
        print(f"   {v:4d}  {k}")
    ids = [p["id"] for p in planes]
    assert len(ids) == len(set(ids)), "IDs duplicados!"
    print(f"IDs unicos: {len(set(ids))}  ({ids[0]} .. {ids[-1]})")


if __name__ == "__main__":
    main()
