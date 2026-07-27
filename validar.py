# -*- coding: utf-8 -*-
"""
validar.py — Cierres geometricos independientes por arquetipo/variante.

No re-ejecuta el generador: comprueba INVARIANTES FISICAS sobre las piezas
y las dimensiones guardadas en catalogo.json. Si una variante produjese un
despiece que no "cierra" (p.ej. rieles que se pasan del largo, paneles que
no cuadran con la seccion de poste), aqui salta.

META: 0 fallos en todo el catalogo antes de producir una sola imagen.

Uso:  python validar.py
"""
import json
import sys

TOL = 1.5        # mm, redondeo normal
TOL_DIAG = 14.0  # mm, voladizos / diagonales / tablones con juntas


def _idx(piezas):
    by_ref, by_name = {}, {}
    for p in piezas:
        by_ref[p["ref"]] = p
        by_name.setdefault(p["nombre"].lower(), p)
    return by_ref, by_name


def _find(piezas, *subs):
    for p in piezas:
        low = p["nombre"].lower()
        if all(s in low for s in subs):
            return p
    return None


def chk(cond, msg, fails):
    if not cond:
        fails.append(msg)


def eq(a, b, tol=TOL):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
def val_banco(p, F):
    d = p["dims"]; L, P, H, T, ls = d["length"], d["depth"], d["height"], d["top_thickness"], d["leg_sec"]
    R, _ = _idx(p["piezas"])
    chk(eq(R["A"]["largo"] + T, H), f"legs {R['A']['largo']}+top {T} != height {H}", F)
    chk(eq(R["B"]["largo"] + 2 * ls, L), f"long rail {R['B']['largo']}+2*{ls} != length {L}", F)
    chk(eq(R["C"]["largo"] + 2 * ls, P), f"short rail {R['C']['largo']}+2*{ls} != depth {P}", F)
    chk(eq(R["D"]["largo"], L) and eq(R["D"]["ancho"], P), "work top != length x depth", F)
    if p["variante"] == "shelf":
        lr = _find(p["piezas"], "lower long")
        chk(lr is not None and eq(lr["largo"] + 2 * ls, L), "lower shelf long rail mismatch", F)


def val_estanteria(p, F):
    d = p["dims"]; L, P, H, n, ps = d["length"], d["depth"], d["height"], d["n_shelves"], d["post_sec"]
    R, _ = _idx(p["piezas"])
    chk(eq(R["A"]["largo"], H), f"posts {R['A']['largo']} != height {H}", F)
    chk(eq(R["B"]["largo"] + 2 * ps, L), f"shelf long {R['B']['largo']}+2*{ps} != length {L}", F)
    chk(eq(R["C"]["largo"] + 2 * ps, P), f"shelf short {R['C']['largo']}+2*{ps} != depth {P}", F)
    chk(R["B"]["cantidad"] == 2 * n and R["C"]["cantidad"] == 2 * n, "shelf rail count != 2*n_shelves", F)
    chk(R["D"]["cantidad"] == n, f"panels {R['D']['cantidad']} != n_shelves {n}", F)


def val_rack_pared(p, F):
    d = p["dims"]; W, H, rs, nh = d["width"], d["height"], d["rail_sec"], d["n_hooks"]
    R, _ = _idx(p["piezas"])
    chk(eq(R["A"]["largo"], H), f"verticals {R['A']['largo']} != height {H}", F)
    chk(eq(R["B"]["largo"] + 2 * rs, W), f"horizontal {R['B']['largo']}+2*{rs} != width {W}", F)
    hook = _find(p["piezas"], "hook") or _find(p["piezas"], "peg")
    if hook is not None:
        chk(hook["cantidad"] == nh, f"hook count {hook['cantidad']} != n_hooks {nh}", F)


def val_carrito(p, F):
    d = p["dims"]; L, P, PL, n, ps = d["length"], d["depth"], d["post_len"], d["n_shelves"], d["post_sec"]
    R, _ = _idx(p["piezas"])
    chk(eq(R["A"]["largo"], PL), f"posts {R['A']['largo']} != post_len {PL}", F)
    chk(eq(R["B"]["largo"] + 2 * ps, L), f"shelf long {R['B']['largo']}+2*{ps} != length {L}", F)
    chk(eq(R["C"]["largo"] + 2 * ps, P), f"shelf short {R['C']['largo']}+2*{ps} != depth {P}", F)
    panels = _find(p["piezas"], "shelf", "panel")
    if panels is not None:
        esperado = n - 1 if p["variante"] == "tray_top" else n
        chk(panels["cantidad"] == esperado, f"panels {panels['cantidad']} != {esperado}", F)


def val_soporte(p, F):
    d = p["dims"]; W, P, H, s = d["width"], d["depth"], d["height"], d["sec"]
    v = p["variante"]
    R, _ = _idx(p["piezas"])
    if v == "firewood":
        lr = _find(p["piezas"], "long rail"); sr = _find(p["piezas"], "short rail")
        up = _find(p["piezas"], "upright")
        chk(up is not None and eq(up["largo"], H), "firewood uprights != height", F)
        chk(lr is not None and eq(lr["largo"] + 2 * s, W), "firewood long rail mismatch", F)
        chk(sr is not None and eq(sr["largo"] + 2 * s, P, TOL_DIAG), "firewood short rail mismatch", F)
    elif v == "a_frame":
        ridge = _find(p["piezas"], "ridge")
        legs = _find(p["piezas"], "leg")
        chk(ridge is not None and eq(ridge["largo"], W), "a-frame ridge != width", F)
        chk(legs is not None and legs["largo"] >= H - TOL_DIAG, "a-frame legs shorter than height (should be diagonal)", F)
    elif v == "leaning":
        st = _find(p["piezas"], "stile")
        chk(st is not None and st["largo"] >= H - TOL_DIAG, "leaning stiles shorter than height", F)
    elif v == "hoop":
        chk(_find(p["piezas"], "hoop") is not None and _find(p["piezas"], "feet") is not None, "hoop pieces missing", F)
    elif v == "tiered":
        chk(len(p["piezas"]) >= d["n_levels"], "tiered: too few pieces", F)


def val_mesa_madera(p, F):
    d = p["dims"]; L, P, H, T, ls, npl = d["length"], d["depth"], d["height"], d["top_thickness"], d["leg_top_sec"], d["n_planks"]
    v = p["variante"]
    R, _ = _idx(p["piezas"])
    frame_h = H - T
    if v in ("straight_bolted", "box_frame"):
        chk(eq(R["A"]["largo"], frame_h), f"legs {R['A']['largo']} != frame_h {frame_h}", F)
    if v == "box_frame":
        chk(eq(R["B"]["largo"] + 2 * ls, L), "box frame long rail mismatch", F)
        chk(eq(R["C"]["largo"] + 2 * ls, P), "box frame short rail mismatch", F)
    if v in ("hairpin", "trapezoid", "cross_x"):
        chk(R["A"]["largo"] >= frame_h - TOL_DIAG, f"{v}: legs shorter than frame height (should be diagonal)", F)
    planks = _find(p["piezas"], "plank")
    chk(planks is not None and eq(planks["largo"], L), "top planks length != table length", F)
    if planks is not None:
        ancho_total = planks["cantidad"] * planks["ancho"] + (planks["cantidad"] - 1) * 5
        chk(eq(ancho_total, P, TOL_DIAG), f"planks span {ancho_total} != depth {P}", F)


def val_parrilla(p, F):
    d = p["dims"]; W, P, bd, nb = d["width"], d["depth"], d["box_depth"], d["n_bars"]
    v = p["variante"]
    R, _ = _idx(p["piezas"])
    if v in ("welded_angle", "brazier", "wheeled"):
        side = _find(p["piezas"], "side panel"); base = _find(p["piezas"], "base")
        chk(side is not None and eq(side["largo"], W), "firebox side != width", F)
        chk(base is not None and eq(base["largo"], W) and eq(base["ancho"], P), "firebox base != W x P", F)
    else:
        chk(_find(p["piezas"], "blank") is not None, "folded firebox blank missing", F)
    bars = _find(p["piezas"], "grate bar")
    chk(bars is not None and bars["cantidad"] == nb, f"grate bars != n_bars {nb}", F)
    chk(bars is not None and eq(bars["largo"], W - 40), "grate bar length != W-40", F)


def val_perchero(p, F):
    d = p["dims"]; W, H, nh, ps = d["width"], d["height"], d["n_hooks"], d["post_sec"]
    v = p["variante"]
    R, _ = _idx(p["piezas"])
    if v == "wall_mounted":
        bar = _find(p["piezas"], "wall bar")
        chk(bar is not None and eq(bar["largo"], W), "wall bar != width", F)
        hook = _find(p["piezas"], "hook")
        chk(hook is not None and hook["cantidad"] == nh, "wall hooks != n_hooks", F)
    elif v == "ladder":
        st = _find(p["piezas"], "stile")
        chk(st is not None and st["largo"] >= H - TOL_DIAG, "ladder stiles shorter than height", F)
    else:
        chk(eq(R["A"]["largo"], H), f"uprights {R['A']['largo']} != height {H}", F)
        bar = _find(p["piezas"], "hook bar")
        chk(bar is not None and eq(bar["largo"] + 2 * ps, W), "top bar mismatch", F)
        hook = _find(p["piezas"], "hooks")
        chk(hook is not None and hook["cantidad"] == nh, "hooks != n_hooks", F)


VALIDADORES = {
    "banco": val_banco, "estanteria": val_estanteria, "rack_pared": val_rack_pared,
    "carrito": val_carrito, "soporte": val_soporte, "mesa_madera": val_mesa_madera,
    "parrilla": val_parrilla, "perchero": val_perchero,
}


def validar_uno(p):
    F = []
    # chequeos genericos
    for pz in p["piezas"]:
        if pz["largo"] <= 0 or pz["ancho"] <= 0 or pz["cantidad"] <= 0:
            F.append(f"pieza {pz['ref']} con medida/cantidad <= 0")
    VALIDADORES[p["arquetipo"]](p, F)
    return F


def main():
    planes = json.load(open("catalogo.json", encoding="utf-8"))
    total_fail = 0
    ejemplos = []
    for p in planes:
        F = validar_uno(p)
        if F:
            total_fail += 1
            if len(ejemplos) < 25:
                ejemplos.append((p["id"], p["arquetipo"], p["variante"], F))
    print(f"Planos: {len(planes)}   Con fallos: {total_fail}")
    for pid, arq, v, F in ejemplos:
        print(f"  {pid} [{arq}/{v}]")
        for f in F:
            print(f"      - {f}")
    if total_fail == 0:
        print("VALIDACION LIMPIA: 0 fallos.")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
