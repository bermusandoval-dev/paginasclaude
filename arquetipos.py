# -*- coding: utf-8 -*-
"""
arquetipos.py — Geometria de los 8 arquetipos de MetalMaster.

Cada arquetipo expone:
  - DIMS[arq](rng)            -> dict de dimensiones en mm (RNG sembrado)
  - VARIANTES[arq]            -> dict vkey -> metadatos (label, weld, union, vistas)
  - build(arq, d, vkey)       -> dict con:
        piezas       : [{ref,nombre,cantidad,largo,ancho,perfil,nota}]
        posiciones   : [str]  posiciones clave con mm (pagina 3)
        angulos      : [str]  todos los angulos en grados (atan2 real)
        detalle      : {"titulo","desc"} zoom de union dificil (pagina 3)
        herrajes     : [{item,cantidad,para_que}]
        tools_extra  : [{item,uso}]

INVARIANTES GEOMETRICAS: cada build produce piezas que cumplen las
relaciones que validar.py comprueba de forma independiente (leg+top==alto,
span+2*poste==ancho, etc.). Las notas llevan las palabras clave que
disparan los iconos de FORMA REAL en la pagina 3 (tube, mitred, drilled
plate, folded, mesh, threaded rod, round rod, cut at N deg).
"""
import math

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def r5(x):
    return int(round(x / 5.0) * 5)

def r10(x):
    return int(round(x / 10.0) * 10)

def pieza(ref, nombre, cantidad, largo, ancho, perfil, nota):
    return {"ref": ref, "nombre": nombre, "cantidad": int(cantidad),
            "largo": int(round(largo)), "ancho": int(round(ancho)),
            "perfil": perfil, "nota": nota}

def ang_deg(rise, run):
    return round(math.degrees(math.atan2(rise, run)), 1)

def hyp(a, b):
    return math.hypot(a, b)

# hardware helper
def hw(item, cantidad, para_que):
    return {"item": item, "cantidad": int(cantidad), "para_que": para_que}


# ===========================================================================
# 1) BANCO  (workbenches & work tables)
# ===========================================================================
def dims_banco(rng):
    return {
        "length": rng.choice([900, 1000, 1200, 1200, 1500, 1500, 1800]),
        "depth": rng.choice([500, 600, 600, 700, 750]),
        "height": rng.choice([850, 900, 900, 950]),
        "top_thickness": rng.choice([30, 35, 40]),
        "leg_sec": rng.choice([40, 50, 50, 60]),
        "rail_sec": rng.choice([30, 40]),
        "top_mat": rng.choice(["steel", "steel", "wood", "ply"]),
    }

VAR_BANCO = {
    "welded":  {"label": "Welded MIG frame",           "weld": True,  "union": "MIG-welded steel frame", "vistas": ["front", "side"]},
    "bolted":  {"label": "Bolt-together M8 frame",      "weld": False, "union": "Bolt-together M8 frame with corner gussets", "vistas": ["front", "side"]},
    "xbrace":  {"label": "Welded frame, X-braced ends", "weld": True,  "union": "MIG-welded frame with diagonal end bracing", "vistas": ["front", "side"]},
    "shelf":   {"label": "Bolted frame + lower shelf",  "weld": False, "union": "Bolt-together frame with a lower storage shelf", "vistas": ["front", "side"]},
    "rolling": {"label": "Welded rolling bench",        "weld": True,  "union": "MIG-welded frame on lockable castors", "vistas": ["front", "side"]},
}

def build_banco(d, vkey):
    L, P, H, T = d["length"], d["depth"], d["height"], d["top_thickness"]
    ls, rs = d["leg_sec"], d["rail_sec"]
    leg_len = H - T
    top_mat = {"steel": "steel sheet 2 mm", "wood": "solid wood board 30 mm",
               "ply": "18 mm birch ply, doubled"}[d["top_mat"]]
    top_nota = "steel top, edges deburred" if d["top_mat"] == "steel" else "wood top, softened edges"

    P_ = []
    posiciones, angulos = [], []
    detalle = {"titulo": "Corner joint", "desc": ""}

    # legs
    leg_nota = f"square tube {ls}x{ls}, ends squared"
    if vkey == "bolted":
        leg_nota = f"square tube {ls}x{ls}, drilled plate gussets bolt here (4-hole pattern)"
    if vkey == "rolling":
        leg_nota = f"square tube {ls}x{ls}, castor plate welded to the foot"
    P_.append(pieza("A", "Legs", 4, leg_len, ls, f"square tube {ls}x{ls}x2 mm", leg_nota))

    # top rails
    rail_corner = "mitred 45 at the corners" if VAR_BANCO[vkey]["weld"] else "square-cut, bolted to leg brackets"
    P_.append(pieza("B", "Top long rails", 2, L - 2 * ls, rs, f"square tube {rs}x{rs}x2 mm", f"square tube, {rail_corner}"))
    P_.append(pieza("C", "Top short rails", 2, P - 2 * ls, rs, f"square tube {rs}x{rs}x2 mm", f"square tube, {rail_corner}"))

    # top panel
    P_.append(pieza("D", "Work top", 1, L, P, top_mat, top_nota))

    ref_next = "E"
    if vkey == "bolted":
        P_.append(pieza(ref_next, "Corner gussets", 4, 90, 90, "flat plate 4 mm", "drilled plate, 3-hole bolt pattern"))
        detalle = {"titulo": "Bolted corner gusset", "desc": "3 x M8 button bolts through the gusset into captive nuts inside each leg."}
    elif vkey == "xbrace":
        rise = leg_len - rs
        run = P - 2 * ls
        a = ang_deg(rise, run)
        P_.append(pieza(ref_next, "End diagonal braces", 2, hyp(rise, run), rs, f"square tube {rs}x{rs}x2 mm", f"square tube, both ends cut at {a} deg"))
        angulos.append(f"End X-braces run at {a} deg from horizontal")
        detalle = {"titulo": "Welded X-brace toe", "desc": f"Brace toe coped and welded to the leg at {a} deg; full 30 mm weld each side."}
    elif vkey == "shelf":
        sh_h = r10(150 + (H * 0.0))  # shelf near floor
        P_.append(pieza(ref_next, "Lower long rails", 2, L - 2 * ls, rs, f"square tube {rs}x{rs}x2 mm", "square tube, bolted to leg brackets"))
        P_.append(pieza("F", "Lower short rails", 2, P - 2 * ls, rs, f"square tube {rs}x{rs}x2 mm", "square tube, bolted to leg brackets"))
        P_.append(pieza("G", "Lower shelf panel", 1, L - 2 * ls, P - 2 * ls, "steel sheet 1.5 mm", "steel sheet, corners notched around the legs"))
        posiciones.append(f"Lower shelf top face 180 mm above the floor line")
        detalle = {"titulo": "Shelf-to-leg bracket", "desc": "Bolted angle bracket carries the lower shelf rail; M8 into captive nut."}

    # posiciones y angulos comunes
    posiciones.insert(0, f"Work-top surface {H} mm above the floor")
    posiciones.append(f"Rail top face {H - T} mm above the floor (under the top)")
    if not angulos:
        angulos.append("All legs vertical (90 deg to the floor)")
        angulos.append("All top-frame corners square (90 deg)")

    # herrajes
    herr = []
    tools_extra = []
    n_top_fix = max(6, (L // 300) * 2)
    if d["top_mat"] == "steel":
        herr.append(hw("Self-tapping screws 4.2 x 13 mm", n_top_fix, "fix the steel top down from underneath"))
    else:
        herr.append(hw("M6 coach bolts + washers", n_top_fix, "clamp the wood top to the frame"))
    if vkey in ("bolted", "shelf"):
        n_bolts = 12 if vkey == "bolted" else 16
        herr.append(hw("M8 x 20 button-head bolts", n_bolts, "join the frame at each bracket"))
        herr.append(hw("M8 captive nuts", n_bolts, "give the bolts a thread inside the tube"))
    if vkey == "rolling":
        herr.append(hw("75 mm castors, 2 with brakes", 4, "roll the bench and lock it in place"))
    else:
        herr.append(hw("M8 adjustable levelling feet", 4, "level the bench on an uneven floor"))

    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 2) ESTANTERIA (industrial shelving & racks)
# ===========================================================================
def dims_estanteria(rng):
    n = rng.choice([3, 4, 4, 5, 5])
    return {
        "length": rng.choice([600, 750, 900, 900, 1200]),
        "depth": rng.choice([300, 350, 400, 450, 500]),
        "height": rng.choice([1500, 1800, 1800, 2000]),
        "n_shelves": n,
        "post_sec": rng.choice([30, 40, 40, 50]),
        "shelf_mat": rng.choice(["steel", "steel", "wood", "mesh"]),
    }

VAR_ESTANTERIA = {
    "bolted_angle": {"label": "Boltless slotted angle", "weld": False, "union": "Slotted-angle, bolt-together", "vistas": ["front", "side"]},
    "welded":       {"label": "Welded steel frame",     "weld": True,  "union": "MIG-welded frame", "vistas": ["front", "side"]},
    "diagonal":     {"label": "Welded, cross-braced",   "weld": True,  "union": "MIG-welded with diagonal back bracing", "vistas": ["front", "side"]},
    "mesh_shelves": {"label": "Bolted, mesh shelves",   "weld": False, "union": "Bolt-together frame, mesh shelf panels", "vistas": ["front", "side"]},
    "wood_shelves": {"label": "Bolted, wood shelves",   "weld": False, "union": "Bolt-together steel frame, wood shelves", "vistas": ["front", "side"]},
}

def build_estanteria(d, vkey):
    L, P, H, n, ps = d["length"], d["depth"], d["height"], d["n_shelves"], d["post_sec"]
    P_, posiciones, angulos = [], [], []

    post_nota = f"angle iron {ps}x{ps}x3"
    if vkey == "bolted_angle":
        post_nota = f"slotted angle {ps}x{ps}, drilled plate slot pattern the full length"
    P_.append(pieza("A", "Corner posts", 4, H, ps, f"angle {ps}x{ps}x3 mm", post_nota))

    P_.append(pieza("B", "Shelf long rails", 2 * n, L - 2 * ps, ps, f"angle {ps}x{ps}x3 mm",
                    "angle, square-cut" if vkey != "welded" and vkey != "diagonal" else "angle, welded to posts"))
    P_.append(pieza("C", "Shelf short rails", 2 * n, P - 2 * ps, ps, f"angle {ps}x{ps}x3 mm", "angle, square-cut"))

    shelf_mat = {"steel": "steel sheet 1.2 mm", "wood": "18 mm OSB board",
                 "mesh": "welded mesh 50 mm"}[d["shelf_mat"]]
    if vkey == "mesh_shelves":
        shelf_mat = "welded mesh 50 mm"
    if vkey == "wood_shelves":
        shelf_mat = "18 mm OSB board"
    shelf_nota = "welded mesh, edges bound in the frame" if "mesh" in shelf_mat else \
                 ("wood board, dropped into the frame" if "OSB" in shelf_mat else "steel sheet, edges folded 15 mm down")
    P_.append(pieza("D", "Shelf panels", n, L - 2 * ps, P - 2 * ps, shelf_mat, shelf_nota))

    detalle = {"titulo": "Shelf-to-post joint", "desc": ""}
    ref_next = "E"
    if vkey == "diagonal":
        rise = H
        run = L - 2 * ps
        a = ang_deg(rise, run)
        P_.append(pieza(ref_next, "Back diagonal braces", 2, hyp(rise, run), ps, f"angle {ps}x{ps}x3 mm", f"angle, both ends cut at {a} deg"))
        angulos.append(f"Back braces run corner-to-corner at {a} deg")
        detalle = {"titulo": "Welded brace foot", "desc": f"Diagonal foot coped to the post at {a} deg, welded both flanges."}
    if vkey == "bolted_angle":
        detalle = {"titulo": "Slotted-angle bolt", "desc": "M8 cup bolt + square nut through the matching slots; no drilling on site."}

    # shelf heights from floor (posiciones clave)
    top_margin = 60
    usable = H - top_margin
    gap = usable / (n)
    heights = [r10(top_margin + gap * (i + 1)) for i in range(n)]
    for i, hgt in enumerate(heights):
        posiciones.append(f"Shelf {i + 1} top face {hgt} mm above the floor")
    posiciones.append(f"Clear gap between shelves ~ {r10(gap - ps)} mm")
    if not angulos:
        angulos.append("All posts vertical (90 deg)")
        angulos.append("All shelf corners square (90 deg)")

    herr, tools_extra = [], []
    n_bolts = 8 * n
    if vkey in ("bolted_angle", "mesh_shelves", "wood_shelves"):
        herr.append(hw("M8 x 16 cup bolts + nuts", n_bolts, "clamp every shelf rail to the posts"))
    if vkey == "mesh_shelves":
        herr.append(hw("Mesh J-clips", 8 * n, "lock the mesh panels into the frame"))
    if vkey == "wood_shelves":
        herr.append(hw("Rubber shelf buffers", 4 * n, "stop the wood boards from sliding"))
    herr.append(hw("M8 adjustable feet", 4, "level the unit and protect the floor"))
    if H >= 1800:
        herr.append(hw("Anti-tip wall bracket + plug", 2, "anchor the tall unit to the wall"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 3) RACK_PARED (tool racks & wall organizers)
# ===========================================================================
def dims_rack_pared(rng):
    return {
        "width": rng.choice([500, 600, 750, 900, 1000]),
        "height": rng.choice([400, 500, 600, 700]),
        "rail_sec": rng.choice([20, 25, 30]),
        "n_hooks": rng.choice([4, 5, 6, 7, 8]),
        "hook_len": rng.choice([60, 80, 100]),
    }

VAR_RACK = {
    "mesh":        {"label": "Mesh panel + hooks",   "weld": False, "union": "Bolt-together frame, mesh panel", "vistas": ["front", "side"]},
    "slat":        {"label": "French-cleat slats",   "weld": False, "union": "Folded-slat cleat rail, screwed", "vistas": ["front", "side"]},
    "bar_hooks":   {"label": "Welded bar + hooks",   "weld": True,  "union": "MIG-welded bar with formed hooks", "vistas": ["front", "side"]},
    "folded_shelf":{"label": "Folded shelf + hooks", "weld": False, "union": "Folded-sheet shelf, bolted", "vistas": ["front", "side"]},
    "pegboard":    {"label": "Perforated steel board","weld": False,"union": "Drilled steel pegboard, bolted", "vistas": ["front", "side"]},
}

def build_rack_pared(d, vkey):
    W, H, rs, nh, hl = d["width"], d["height"], d["rail_sec"], d["n_hooks"], d["hook_len"]
    P_, posiciones, angulos = [], [], []
    detalle = {"titulo": "Hook detail", "desc": ""}

    P_.append(pieza("A", "Vertical rails", 2, H, rs, f"square tube {rs}x{rs}x2 mm", "square tube, drilled for wall plugs top and bottom"))
    n_h = 3 if H >= 600 else 2
    P_.append(pieza("B", "Horizontal rails", n_h, W - 2 * rs, rs, f"square tube {rs}x{rs}x2 mm",
                    "square tube, welded to the uprights" if vkey == "bar_hooks" else "square tube, bolted to the uprights"))

    ref = "C"
    if vkey == "mesh":
        P_.append(pieza(ref, "Mesh panel", 1, W - 2 * rs, H - 2 * rs, "welded mesh 40 mm", "welded mesh, edges tucked behind the frame"))
        P_.append(pieza("D", "S-hooks", nh, hl, 8, "round rod 6 mm", "round rod, bent into an S-hook"))
        detalle = {"titulo": "Mesh S-hook", "desc": "6 mm rod bent into an S; hangs anywhere on the 40 mm mesh."}
    elif vkey == "slat":
        n_slat = 3
        P_.append(pieza(ref, "Cleat slats", n_slat, W, 60, "folded sheet 1.5 mm", "folded into a 45 deg cleat profile"))
        angulos.append("Cleat face folded at 45 deg to lock the hooks")
        detalle = {"titulo": "45 deg cleat", "desc": "Both slat and hook folded at 45 deg so gravity holds the tool on."}
    elif vkey == "bar_hooks":
        P_.append(pieza(ref, "Formed hooks", nh, hl, 12, "round rod 10 mm", "round rod, bent into a J and welded to the bar"))
        detalle = {"titulo": "Welded J-hook", "desc": "10 mm rod J-hook welded to the front face of the bar, 8 mm fillet."}
    elif vkey == "folded_shelf":
        P_.append(pieza(ref, "Folded shelf", 1, W - 2 * rs, 120, "folded sheet 1.5 mm", "folded into a U-channel shelf with a lip"))
        P_.append(pieza("D", "Screw hooks", nh, hl, 8, "round rod 8 mm", "round rod, threaded end, screws into the rail"))
        detalle = {"titulo": "U-channel shelf", "desc": "Sheet folded twice into a U so small parts do not roll off."}
    elif vkey == "pegboard":
        P_.append(pieza(ref, "Pegboard panel", 1, W - 2 * rs, H - 2 * rs, "steel sheet 2 mm", "drilled plate, 25 mm hole grid (peg pattern)"))
        P_.append(pieza("D", "Peg hooks", nh, hl, 8, "round rod 6 mm", "round rod, bent peg to suit the hole grid"))
        detalle = {"titulo": "Peg-hole grid", "desc": "6 mm holes on a 25 mm grid; pegs move without tools."}

    # hook spacing
    margin = 60
    if nh > 1:
        sp = (W - 2 * margin) / (nh - 1)
        posiciones.append(f"Hooks on a {r10(sp)} mm pitch, first hook {margin} mm from the end")
    posiciones.append(f"Top rail centre {H - rs} mm from the bottom rail; fix to studs at {r10((W - 2 * rs))} mm centres")
    if not angulos:
        angulos.append("Panel mounts flat and plumb (90 deg to the floor)")

    herr, tools_extra = [], []
    herr.append(hw("Wall plugs + 60 mm screws", 4, "anchor the rack to solid wall or studs"))
    if vkey in ("mesh", "folded_shelf", "pegboard"):
        herr.append(hw("M6 x 16 bolts + nuts", 6, "bolt the panel and rails together"))
    if vkey == "slat":
        herr.append(hw("Countersunk wood screws 4 x 40", 8, "screw the cleat slats to the wall"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 4) CARRITO (shop carts & trolleys)
# ===========================================================================
def dims_carrito(rng):
    return {
        "length": rng.choice([600, 700, 750, 800, 900]),
        "depth": rng.choice([400, 450, 500, 550]),
        "post_len": rng.choice([700, 800, 850, 900]),
        "n_shelves": rng.choice([2, 2, 3, 3]),
        "post_sec": rng.choice([25, 30, 30, 40]),
        "caster_h": rng.choice([75, 100, 125]),
    }

VAR_CARRITO = {
    "welded_2shelf": {"label": "Welded, two shelves",  "weld": True,  "union": "MIG-welded frame on castors", "vistas": ["front", "side"]},
    "bolted_3shelf": {"label": "Bolted, three shelves", "weld": False, "union": "Bolt-together frame on castors", "vistas": ["front", "side"]},
    "handle_cart":   {"label": "Welded + push handle", "weld": True, "union": "MIG-welded frame with a bent push handle", "vistas": ["front", "side"]},
    "mesh_shelves":  {"label": "Bolted, mesh shelves", "weld": False, "union": "Bolt-together frame, mesh shelves", "vistas": ["front", "side"]},
    "tray_top":      {"label": "Welded + folded tray top", "weld": True, "union": "MIG-welded frame with a folded lipped tray", "vistas": ["front", "side"]},
}

def build_carrito(d, vkey):
    L, P, PL, n, ps, ch = d["length"], d["depth"], d["post_len"], d["n_shelves"], d["post_sec"], d["caster_h"]
    P_, posiciones, angulos = [], [], []
    weld = VAR_CARRITO[vkey]["weld"]

    P_.append(pieza("A", "Corner posts", 4, PL, ps, f"square tube {ps}x{ps}x2 mm",
                    "square tube, castor plate welded to the foot" if weld else "square tube, drilled for castor bolts"))
    P_.append(pieza("B", "Shelf long rails", 2 * n, L - 2 * ps, ps, f"square tube {ps}x{ps}x2 mm",
                    "square tube, welded to posts" if weld else "square tube, bolted to posts"))
    P_.append(pieza("C", "Shelf short rails", 2 * n, P - 2 * ps, ps, f"square tube {ps}x{ps}x2 mm",
                    "square tube, welded to posts" if weld else "square tube, bolted to posts"))

    shelf_mat = "welded mesh 40 mm" if vkey == "mesh_shelves" else "steel sheet 1.5 mm"
    shelf_nota = "welded mesh, bound in the frame" if vkey == "mesh_shelves" else "steel sheet, edges folded 20 mm down"
    P_.append(pieza("D", "Shelf panels", n, L - 2 * ps, P - 2 * ps, shelf_mat, shelf_nota))

    detalle = {"titulo": "Castor mount", "desc": "Castor top plate sits square under each leg."}
    ref = "E"
    if vkey == "handle_cart":
        P_.append(pieza(ref, "Push handle", 1, L - 2 * ps + 2 * 120, ps, f"round tube {ps} dia x 2 mm", "round tube, two 90 deg bends into a U handle"))
        angulos.append("Handle has two 90 deg bends")
        detalle = {"titulo": "Bent push handle", "desc": "One tube, two 90 deg bends; welded to the top of the back posts."}
    if vkey == "tray_top":
        P_[-1] = pieza("D", "Shelf panels", max(1, n - 1), L - 2 * ps, P - 2 * ps, "steel sheet 1.5 mm", "steel sheet, edges folded 20 mm down")
        P_.append(pieza(ref, "Lipped top tray", 1, L, P, "folded sheet 1.5 mm", "folded into a tray with a 30 mm lip all round"))
        detalle = {"titulo": "Folded tray lip", "desc": "Corners notched and folded so the 30 mm lip meets cleanly."}

    # shelf heights
    heights = [r10(ch + PL * (i + 1) / (n + 0.5)) for i in range(n)]
    for i, hgt in enumerate(heights):
        posiciones.append(f"Shelf {i + 1} top face {hgt} mm above the floor (with castors)")
    posiciones.append(f"Top of cart {ch + PL} mm above the floor")
    if not angulos:
        angulos.append("Posts vertical (90 deg); shelves level")

    herr, tools_extra = [], []
    herr.append(hw(f"{ch} mm castors, 2 with brakes", 4, "roll the cart and lock two wheels"))
    if not weld:
        herr.append(hw("M8 x 20 bolts + captive nuts", 8 * n, "bolt every shelf rail to the posts"))
    if vkey == "mesh_shelves":
        herr.append(hw("Mesh J-clips", 8 * n, "lock the mesh shelves in place"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 5) SOPORTE (stands & holders)  -- geometrias diversas, angulos clave
# ===========================================================================
def dims_soporte(rng):
    return {
        "width": rng.choice([400, 500, 600, 700, 800]),
        "depth": rng.choice([300, 350, 400, 450]),
        "height": rng.choice([500, 700, 900, 1100, 1300]),
        "sec": rng.choice([20, 25, 30]),
        "n_levels": rng.choice([2, 3, 3, 4]),
    }

VAR_SOPORTE = {
    "a_frame":  {"label": "Welded A-frame",        "weld": True,  "union": "MIG-welded A-frame", "vistas": ["front", "side"]},
    "leaning":  {"label": "Bolted leaning ladder", "weld": False, "union": "Bolt-together leaning ladder", "vistas": ["front", "side"]},
    "firewood": {"label": "Bolted rectangular rack", "weld": False, "union": "Bolt-together rectangular rack", "vistas": ["front", "side"]},
    "hoop":     {"label": "Bent-tube hoop",     "weld": True,  "union": "Bent-tube hoop, welded feet", "vistas": ["front", "top"]},
    "tiered":   {"label": "Bolted tiered frame",         "weld": False, "union": "Bolt-together tiered stand", "vistas": ["front", "side"]},
}

def build_soporte(d, vkey):
    W, P, H, s, nl = d["width"], d["depth"], d["height"], d["sec"], d["n_levels"]
    P_, posiciones, angulos = [], [], []
    detalle = {"titulo": "Foot detail", "desc": ""}

    if vkey == "a_frame":
        spread = P
        rise = H
        a = ang_deg(rise, spread / 2)
        leg_len = hyp(rise, spread / 2)
        P_.append(pieza("A", "A-frame legs", 4, leg_len, s, f"round tube {s} dia x 2 mm", f"round tube, feet cut at {round(90 - a,1)} deg"))
        P_.append(pieza("B", "Top ridge rail", 1, W, s, f"round tube {s} dia x 2 mm", "round tube, legs welded each side"))
        P_.append(pieza("C", "Cross ties", 2, spread - 2 * s, s, f"square tube {s}x{s}x2 mm", "square tube, ties the leg pairs"))
        angulos.append(f"Legs splay at {round(90 - a,1)} deg from vertical (apex {round(2*(90-a),1)} deg)")
        posiciones.append(f"Ridge {H} mm above the floor; feet {spread} mm apart")
        detalle = {"titulo": "Welded apex", "desc": f"Four legs meet the ridge; each leg foot cut at {round(90-a,1)} deg to sit flat."}
    elif vkey == "leaning":
        lean = 15  # deg from wall
        rise = H
        run = math.tan(math.radians(lean)) * H
        leg_len = hyp(rise, run)
        P_.append(pieza("A", "Leaning stiles", 2, leg_len, s, f"square tube {s}x{s}x2 mm", f"square tube, top & foot cut at {lean} deg"))
        for i in range(nl):
            P_.append(pieza(chr(ord("B") + i), f"Shelf rung {i+1}", 1, W - 2 * s, s, f"square tube {s}x{s}x2 mm", "square tube, bolted between the stiles"))
        angulos.append(f"Whole frame leans {lean} deg off the wall")
        heights = [r10(H * (i + 1) / (nl + 1)) for i in range(nl)]
        for i, hgt in enumerate(heights):
            posiciones.append(f"Rung {i+1} front edge {hgt} mm above the floor")
        detalle = {"titulo": "Leaning foot", "desc": f"Foot cut at {lean} deg so the full face sits on the floor."}
    elif vkey == "firewood":
        P_.append(pieza("A", "Uprights", 4, H, s, f"square tube {s}x{s}x2 mm", "square tube, drilled for the rail bolts"))
        P_.append(pieza("B", "Long rails", 4, W - 2 * s, s, f"square tube {s}x{s}x2 mm", "square tube, bolted top and bottom"))
        P_.append(pieza("C", "Short rails", 4, P - 2 * s, s, f"square tube {s}x{s}x2 mm", "square tube, bolted top and bottom"))
        P_.append(pieza("D", "Floor bars", 5, W - 2 * s, s, f"round tube {s} dia x 2 mm", "round tube, keeps logs off the ground"))
        posiciones.append(f"Bottom rail {r10(120)} mm above the floor; top rail {H - s} mm")
        posiciones.append(f"Five floor bars on a {r10((W - 2*s)/4)} mm pitch")
        angulos.append("All uprights vertical (90 deg)")
        detalle = {"titulo": "Bolted rail end", "desc": "Rail flattened and bolted to the upright with one M8."}
    elif vkey == "hoop":
        # bent tube hoop
        P_.append(pieza("A", "Bent hoop", 1, math.pi * (W / 2) + 2 * H, s, f"round tube {s} dia x 2 mm", "round tube, cold-bent into an inverted-U hoop"))
        P_.append(pieza("B", "Welded feet", 2, 120, 60, "flat plate 5 mm", "drilled plate, 2-hole foot, welded to the hoop"))
        angulos.append("Hoop top is a 180 deg bend; legs vertical")
        posiciones.append(f"Hoop {H} mm tall, {W} mm wide; foot holes {r10(80)} mm apart")
        detalle = {"titulo": "Hoop-to-foot weld", "desc": "Tube end coped onto the foot plate and welded all round."}
    elif vkey == "tiered":
        for i in range(nl):
            lvl_w = W - i * 80
            P_.append(pieza(chr(ord("A") + i), f"Tier {i+1} frame", 1, 2 * (lvl_w) + 2 * P, s, f"square tube {s}x{s}x2 mm", "square tube, bent/bolted into a tray frame"))
        P_.append(pieza(chr(ord("A") + nl), "Corner links", 4 * (nl - 1), r10(H / nl), s, f"square tube {s}x{s}x2 mm", "square tube, bolts the tiers apart"))
        heights = [r10(H * (i + 1) / nl) for i in range(nl)]
        for i, hgt in enumerate(heights):
            posiciones.append(f"Tier {i+1} {hgt} mm above the floor, each {80} mm narrower going up")
        angulos.append("Tiers stacked square (90 deg links)")
        detalle = {"titulo": "Tier link", "desc": "Short post bolts each tier to the one below with M6."}

    herr, tools_extra = [], []
    if vkey in ("leaning", "firewood", "tiered"):
        herr.append(hw("M8 x 20 bolts + nuts" if vkey != "tiered" else "M6 x 16 bolts + nuts", 8 if vkey != "tiered" else 8 * (nl - 1), "bolt the frame together"))
    herr.append(hw("Rubber end caps", 4 if vkey != "hoop" else 2, "cap the tube feet and protect the floor"))
    if vkey == "hoop":
        herr.append(hw("M8 x 60 anchor bolts", 4, "bolt the feet to the floor"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 6) MESA_MADERA (metal frame, wood top)
# ===========================================================================
def dims_mesa_madera(rng):
    return {
        "length": rng.choice([900, 1000, 1200, 1400, 1600]),
        "depth": rng.choice([450, 500, 600, 700, 800]),
        "height": rng.choice([420, 450, 730, 740, 750]),  # coffee vs dining
        "top_thickness": rng.choice([25, 30, 38]),
        "leg_top_sec": rng.choice([25, 30, 40]),
        "n_planks": rng.choice([3, 4, 5]),
    }

VAR_MESA = {
    "hairpin":        {"label": "Hairpin rod legs",     "weld": True,  "union": "Welded hairpin rod legs, bolted to top", "vistas": ["front", "side"]},
    "straight_bolted":{"label": "Straight bolted legs", "weld": False, "union": "Straight tube legs, bolted top plates", "vistas": ["front", "side"]},
    "trapezoid":      {"label": "Trapezoid A-legs",     "weld": True,  "union": "Welded trapezoid legs", "vistas": ["front", "side"]},
    "box_frame":      {"label": "Welded box frame",     "weld": True,  "union": "Welded box frame under the top", "vistas": ["front", "side"]},
    "cross_x":        {"label": "Bolted X-legs",        "weld": False, "union": "Bolt-together X trestle legs", "vistas": ["front", "side"]},
}

def build_mesa_madera(d, vkey):
    L, P, H, T, ls, npl = d["length"], d["depth"], d["height"], d["top_thickness"], d["leg_top_sec"], d["n_planks"]
    P_, posiciones, angulos = [], [], []
    detalle = {"titulo": "Top fixing", "desc": ""}
    frame_h = H - T

    if vkey == "hairpin":
        rake = 100  # foot offset
        leg_len = hyp(frame_h, rake)
        a = ang_deg(frame_h, rake)
        P_.append(pieza("A", "Hairpin legs (2-rod)", 4, leg_len, 10, "round rod 10 mm", f"round rod, 2 rods per leg, splay {round(90-a,1)} deg, welded top plate"))
        P_.append(pieza("B", "Leg top plates", 4, 120, 120, "flat plate 4 mm", "drilled plate, 3-hole pattern to bolt under the top"))
        angulos.append(f"Hairpin rods splay {round(90 - a,1)} deg from vertical")
        detalle = {"titulo": "Hairpin weld + plate", "desc": "Two rods welded to a drilled plate; plate bolts up into the wood top."}
    elif vkey == "straight_bolted":
        P_.append(pieza("A", "Straight legs", 4, frame_h, ls, f"square tube {ls}x{ls}x2 mm", "square tube, bolt-on top plate drilled for the top"))
        P_.append(pieza("B", "Aprons long", 2, L - 2 * ls - 80, ls, f"square tube {ls}x{ls}x2 mm", "square tube, bolted to the legs"))
        P_.append(pieza("C", "Aprons short", 2, P - 2 * ls - 80, ls, f"square tube {ls}x{ls}x2 mm", "square tube, bolted to the legs"))
        angulos.append("Legs vertical (90 deg)")
        detalle = {"titulo": "Bolted apron", "desc": "Apron bolts to a tab on each leg; two M8 per corner."}
    elif vkey == "trapezoid":
        rake = P * 0.22
        leg_len = hyp(frame_h, rake)
        a = ang_deg(frame_h, rake)
        P_.append(pieza("A", "Trapezoid legs", 2, leg_len, ls, f"square tube {ls}x{ls}x2 mm", f"square tube, inverted-V, ends cut at {round(90-a,1)} deg"))
        P_.append(pieza("B", "Foot bars", 2, P, ls, f"square tube {ls}x{ls}x2 mm", "square tube, welded across the leg feet"))
        P_.append(pieza("C", "Top bars", 2, r10(P * 0.4), ls, f"square tube {ls}x{ls}x2 mm", "square tube, welded top plate for the wood top"))
        P_.append(pieza("D", "Stretcher", 1, L - 300, ls, f"round tube {ls} dia x 2 mm", "round tube, joins the two leg frames"))
        angulos.append(f"Trapezoid legs rake {round(90 - a,1)} deg from vertical")
        detalle = {"titulo": "Welded leg apex", "desc": f"Leg and foot bar meet at {round(90-a,1)} deg, welded both sides."}
    elif vkey == "box_frame":
        P_.append(pieza("A", "Legs", 4, frame_h, ls, f"square tube {ls}x{ls}x2 mm", "square tube, mitred into the box frame"))
        P_.append(pieza("B", "Frame long rails", 2, L - 2 * ls, ls, f"square tube {ls}x{ls}x2 mm", "square tube, mitred 45 at the corners"))
        P_.append(pieza("C", "Frame short rails", 2, P - 2 * ls, ls, f"square tube {ls}x{ls}x2 mm", "square tube, mitred 45 at the corners"))
        angulos.append("Legs vertical; frame corners mitred 45 deg")
        detalle = {"titulo": "Mitred box corner", "desc": "Rails mitred 45 deg and welded; leg tucks inside the corner."}
    elif vkey == "cross_x":
        rise = frame_h
        run = P - 2 * ls
        a = ang_deg(rise, run)
        P_.append(pieza("A", "X-leg bars", 4, hyp(rise, run), ls, f"square tube {ls}x{ls}x2 mm", f"square tube, ends cut at {a} deg, bolt pivot at centre"))
        P_.append(pieza("B", "Top rails", 2, L - 200, ls, f"square tube {ls}x{ls}x2 mm", "square tube, bolted, carries the wood top"))
        P_.append(pieza("C", "Foot rails", 2, P, ls, f"square tube {ls}x{ls}x2 mm", "square tube, bolted across the X feet"))
        angulos.append(f"X-legs cross at {round(2*a,1)} deg (each bar {a} deg)")
        detalle = {"titulo": "X pivot bolt", "desc": "The two bars pivot on one M8 carriage bolt + lock nut at the crossing."}

    # top planks
    plank_w = r5((P - (npl - 1) * 5) / npl)
    P_.append(pieza("Z", "Wood top planks", npl, L, plank_w, "solid wood plank", f"wood board, {npl} planks with 5 mm gaps, softened edges"))
    posiciones.insert(0, f"Table top {H} mm above the floor; wood top {T} mm thick")
    posiciones.append(f"Frame top face {frame_h} mm above the floor")
    if not angulos:
        angulos.append("Legs vertical (90 deg)")

    herr, tools_extra = [], []
    n_top = 4 if vkey in ("hairpin", "straight_bolted") else 6
    herr.append(hw("M6 x 30 coach screws + washers", n_top, "screw the wood top to the frame plates"))
    if vkey in ("straight_bolted", "cross_x"):
        herr.append(hw("M8 x 20 bolts + nuts", 8, "bolt the frame/legs together"))
    if vkey == "cross_x":
        herr.append(hw("M8 x 50 carriage bolt + lock nut", 1, "the X pivots on this bolt"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 7) PARRILLA (BBQ, grills & fire pits)
# ===========================================================================
def dims_parrilla(rng):
    return {
        "width": rng.choice([500, 600, 700, 800]),
        "depth": rng.choice([350, 400, 450, 500]),
        "box_depth": rng.choice([150, 180, 200, 250]),
        "stand_h": rng.choice([0, 700, 750, 800]),  # 0 = tabletop
        "n_bars": rng.choice([6, 7, 8, 9]),
        "sheet_t": rng.choice([2, 3]),
    }

VAR_PARRILLA = {
    "folded_box":  {"label": "Folded-sheet firebox",   "weld": False, "union": "Folded sheet, riveted seams", "vistas": ["front", "top"]},
    "welded_angle":{"label": "Welded angle frame",     "weld": True,  "union": "Welded angle frame + sheet", "vistas": ["front", "side"]},
    "riveted":     {"label": "Riveted portable box",   "weld": False, "union": "Riveted sheet firebox", "vistas": ["front", "top"]},
    "brazier":     {"label": "Welded deep brazier",    "weld": True,  "union": "Welded deep bowl-style firebox", "vistas": ["front", "side"]},
    "wheeled":     {"label": "Welded box on wheels",   "weld": True,  "union": "Welded firebox on a wheeled stand", "vistas": ["front", "side"]},
}

def build_parrilla(d, vkey):
    W, P, bd, sh, nb, st = d["width"], d["depth"], d["box_depth"], d["stand_h"], d["n_bars"], d["sheet_t"]
    P_, posiciones, angulos = [], [], []
    detalle = {"titulo": "Seam detail", "desc": ""}
    tabletop = (sh == 0)
    weld = VAR_PARRILLA[vkey]["weld"]
    joinw = "welded" if weld else "bolted"

    # firebox
    if vkey in ("folded_box", "riveted"):
        P_.append(pieza("A", "Firebox blank (folded)", 1, W + 2 * bd, P + 2 * bd, f"steel sheet {st} mm",
                        "folded into a tray: base + 4 sides, corners riveted"))
        detalle = {"titulo": "Riveted corner", "desc": "Corner tabs folded up and set with two 4.8 mm rivets each."}
    else:
        P_.append(pieza("A", "Firebox side panels", 2, W, bd, f"steel sheet {st} mm", "steel sheet, welded to the frame"))
        P_.append(pieza("B", "Firebox end panels", 2, P - 2 * st, bd, f"steel sheet {st} mm", "steel sheet, welded to the frame"))
        P_.append(pieza("C", "Firebox base", 1, W, P, f"steel sheet {st} mm", "steel sheet, drilled with air holes (hole pattern)"))
        P_.append(pieza("D", "Box frame angles", 4, bd, 25, "angle 25x25x3 mm", "angle, welded box corners"))
        detalle = {"titulo": "Welded box corner", "desc": "Angle uprights welded to the base and side sheet; continuous seam."}

    # grate bars
    ref = "E" if vkey in ("welded_angle", "brazier", "wheeled") else "B"
    P_.append(pieza(ref, "Grate bars", nb, W - 40, 10, "round rod 10 mm", f"round rod, grate bar in a {joinw} frame"))
    grate_frame_ref = chr(ord(ref) + 1)
    P_.append(pieza(grate_frame_ref, "Grate frame", 1, 2 * (W - 40) + 2 * (P - 40), 20, "square bar 10 mm", f"square bar, {joinw} grate frame"))

    # legs / stand
    if not tabletop:
        leg_ref = chr(ord(grate_frame_ref) + 1)
        if vkey == "wheeled":
            P_.append(pieza(leg_ref, "Stand legs", 4, sh, 30, "square tube 30x30x2 mm", "square tube, 2 legs take an axle for wheels"))
            P_.append(pieza(chr(ord(leg_ref) + 1), "Axle", 1, W + 60, 16, "round bar 16 mm", "round bar, wheels on each end"))
        else:
            P_.append(pieza(leg_ref, "Stand legs", 4, sh, 30, "square tube 30x30x2 mm", f"square tube, {joinw} under the box"))
        P_.append(pieza(chr(ord(leg_ref) + (2 if vkey == "wheeled" else 1)), "Stand cross rails", 2, W - 60, 25, "square tube 25x25x2 mm", "square tube, ties the legs"))
        posiciones.append(f"Firebox rim {sh + bd} mm above the floor; grate {sh + bd - 30} mm")
    else:
        posiciones.append(f"Firebox {bd} mm deep; sits on a tabletop")

    # grate bar spacing + air holes
    if nb > 1:
        pitch = (W - 80) / (nb - 1)
        posiciones.append(f"Grate bars on a {r10(pitch)} mm pitch, {r10(pitch - 10)} mm clear gaps")
    posiciones.append(f"Firebox internal {W} x {P} x {bd} mm")
    angulos.append("Firebox sides vertical (90 deg) to the base")
    if vkey == "brazier":
        flare = 8
        angulos.append(f"Brazier walls flare {flare} deg outward")

    herr, tools_extra = [], []
    if vkey in ("folded_box", "riveted"):
        herr.append(hw("4.8 x 10 mm rivets", 12, "set the folded firebox corners"))
    if not tabletop and vkey != "wheeled":
        if vkey in ("folded_box", "riveted"):
            herr.append(hw("M8 x 20 bolts + nuts", 8, "bolt the legs under the firebox"))
    if vkey == "wheeled":
        herr.append(hw(f"{r10(200)} mm steel wheels", 2, "wheel the grill across the patio"))
        herr.append(hw("R-clips", 2, "keep the wheels on the axle"))
    herr.append(hw("High-temp BBQ paint", 1, "protect the firebox from heat and rust"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# 8) PERCHERO (coat / shoe racks & entry)
# ===========================================================================
def dims_perchero(rng):
    return {
        "width": rng.choice([400, 500, 600, 700, 800]),
        "height": rng.choice([1500, 1600, 1700, 1750, 1800]),
        "depth": rng.choice([300, 350, 400]),
        "n_hooks": rng.choice([4, 5, 6, 8]),
        "post_sec": rng.choice([25, 30, 40]),
        "shelf": rng.choice([True, True, False]),
    }

VAR_PERCHERO = {
    "welded_tube": {"label": "Welded tube frame",      "weld": True,  "union": "MIG-welded tube frame", "vistas": ["front", "side"]},
    "bolted_flat": {"label": "Flat-pack bolted",       "weld": False, "union": "Bolt-together flat-pack frame", "vistas": ["front", "side"]},
    "bench_combo": {"label": "Welded frame + bench",   "weld": True,  "union": "MIG-welded frame with a seat bench", "vistas": ["front", "side"]},
    "ladder":      {"label": "Bolted leaning ladder",  "weld": False, "union": "Bolt-together leaning ladder", "vistas": ["front", "side"]},
    "wall_mounted":{"label": "Wall bar + shelf",       "weld": False, "union": "Wall-mounted bar with a shelf", "vistas": ["front", "side"]},
}

def build_perchero(d, vkey):
    W, H, P, nh, ps = d["width"], d["height"], d["depth"], d["n_hooks"], d["post_sec"]
    shelf = d["shelf"]
    P_, posiciones, angulos = [], [], []
    detalle = {"titulo": "Hook mount", "desc": ""}

    if vkey == "wall_mounted":
        H = min(H, 400)  # a wall bar, not a tower
        P_.append(pieza("A", "Wall bar", 1, W, ps, f"square tube {ps}x{ps}x2 mm", "square tube, drilled for wall plugs"))
        P_.append(pieza("B", "Hooks", nh, 90, 10, "round rod 10 mm", "round rod, bent J-hook, screwed to the bar"))
        if shelf:
            P_.append(pieza("C", "Top shelf", 1, W, P, "folded sheet 1.5 mm", "folded into a U-channel shelf with a lip"))
            P_.append(pieza("D", "Shelf brackets", 2, P, 25, "angle 25x25x3 mm", "angle, bolts the shelf to the wall"))
        posiciones.append(f"Bar fixed at hook height; hooks {r10((W - 120)/(max(1,nh-1)))} mm apart")
        detalle = {"titulo": "Wall fixing", "desc": "Bar bolts to studs; hooks screw onto the bar face."}
    elif vkey == "ladder":
        lean = 15
        leg_len = hyp(H, math.tan(math.radians(lean)) * H)
        P_.append(pieza("A", "Leaning stiles", 2, leg_len, ps, f"square tube {ps}x{ps}x2 mm", f"square tube, top & foot cut at {lean} deg"))
        n_rung = 5
        P_.append(pieza("B", "Rungs", n_rung, W - 2 * ps, ps, f"round tube {ps} dia x 2 mm", "round tube, bolted between the stiles (hang over these)"))
        angulos.append(f"Ladder leans {lean} deg off the wall")
        heights = [r10(H * (i + 1) / (n_rung + 1)) for i in range(n_rung)]
        posiciones.append(f"Rungs from {heights[0]} to {heights[-1]} mm up the wall")
        detalle = {"titulo": "Leaning foot", "desc": f"Foot cut at {lean} deg so it sits flat and leans safely."}
    else:
        # tower: welded_tube / bolted_flat / bench_combo
        P_.append(pieza("A", "Uprights", 2, H, ps, f"square tube {ps}x{ps}x2 mm",
                        "square tube, welded to the base" if VAR_PERCHERO[vkey]["weld"] else "square tube, bolted to the base"))
        P_.append(pieza("B", "Top hook bar", 1, W - 2 * ps, ps, f"square tube {ps}x{ps}x2 mm",
                        "square tube, welded across the top" if VAR_PERCHERO[vkey]["weld"] else "square tube, bolted across the top"))
        P_.append(pieza("C", "Hooks", nh, 100, 10, "round rod 10 mm",
                        "round rod, bent double-hook" + (", welded to the bar" if VAR_PERCHERO[vkey]["weld"] else ", screwed to the bar")))
        P_.append(pieza("D", "Feet", 2, P, ps, f"square tube {ps}x{ps}x2 mm", "square tube, T-feet keep the tower upright"))
        ref = "E"
        if shelf or vkey == "bench_combo":
            seat_h = 450 if vkey == "bench_combo" else 300
            P_.append(pieza(ref, "Lower shelf/seat rails", 2, W - 2 * ps, ps, f"square tube {ps}x{ps}x2 mm", "square tube, carries the seat/shelf"))
            P_.append(pieza(chr(ord(ref)+1), "Seat/shelf board", 1, W - 2 * ps, P, "solid wood board 20 mm" if vkey == "bench_combo" else "steel sheet 1.5 mm",
                            "wood seat board" if vkey == "bench_combo" else "steel shelf, edges folded"))
            posiciones.append(f"Seat/shelf {seat_h} mm above the floor")
        posiciones.insert(0, f"Top hook bar {H - ps} mm above the floor")
        if nh > 1:
            posiciones.append(f"Hooks {r10((W - 2*ps - 60)/(nh-1))} mm apart on the top bar")
        angulos.append("Uprights vertical (90 deg); feet square to the floor")
        detalle = {"titulo": "Welded double-hook" if VAR_PERCHERO[vkey]["weld"] else "Screwed hook",
                   "desc": "10 mm rod bent into a double hook, fixed to the top bar."}

    if not posiciones:
        posiciones.append("Mounts plumb and square to the wall")
    if not angulos:
        angulos.append("Bar mounts level (90 deg to the uprights)")

    herr, tools_extra = [], []
    if vkey == "wall_mounted":
        herr.append(hw("Wall plugs + 70 mm screws", 4, "anchor the bar to studs or masonry"))
        herr.append(hw("M6 hook screws", nh, "fix each hook to the bar"))
    elif vkey in ("bolted_flat", "ladder"):
        herr.append(hw("M8 x 20 bolts + nuts", 10, "bolt the flat-pack frame together"))
    if vkey != "wall_mounted":
        herr.append(hw("Rubber floor pads", 4, "protect the floor under the feet"))
    if d.get("shelf") and vkey in ("welded_tube", "bolted_flat"):
        herr.append(hw("Self-tapping screws 4.2 x 13", 6, "fix the lower shelf board"))
    return {"piezas": P_, "posiciones": posiciones, "angulos": angulos,
            "detalle": detalle, "herrajes": herr, "tools_extra": tools_extra}


# ===========================================================================
# Dispatchers
# ===========================================================================
DIMS = {
    "banco": dims_banco, "estanteria": dims_estanteria, "rack_pared": dims_rack_pared,
    "carrito": dims_carrito, "soporte": dims_soporte, "mesa_madera": dims_mesa_madera,
    "parrilla": dims_parrilla, "perchero": dims_perchero,
}
VARIANTES = {
    "banco": VAR_BANCO, "estanteria": VAR_ESTANTERIA, "rack_pared": VAR_RACK,
    "carrito": VAR_CARRITO, "soporte": VAR_SOPORTE, "mesa_madera": VAR_MESA,
    "parrilla": VAR_PARRILLA, "perchero": VAR_PERCHERO,
}
_BUILDERS = {
    "banco": build_banco, "estanteria": build_estanteria, "rack_pared": build_rack_pared,
    "carrito": build_carrito, "soporte": build_soporte, "mesa_madera": build_mesa_madera,
    "parrilla": build_parrilla, "perchero": build_perchero,
}

def build(arq, d, vkey):
    return _BUILDERS[arq](d, vkey)

def deck_variantes(arq):
    """Orden ESTABLE del mazo base (no reordenar: cambia los repartos)."""
    return list(VARIANTES[arq].keys())
