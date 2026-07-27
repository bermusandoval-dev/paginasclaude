# -*- coding: utf-8 -*-
"""
prompts.py — Prompts de imagen (portada + grilla) por plano, en ingles.

Reglas aprendidas (doc seccion 4):
  * Portada: product photography con CONTEOS EXACTOS, material, medidas en cm,
    escena por subcategoria, y STRICT RULES (sin texto/cotas/gente).
  * Grilla: 8 paneles 2x4, "metalworker's hands" (posesivo + oficio evita
    falsos positivos NSFW), conteos enumerados, sin texto/numeros/marcos.
"""

def _cm(mm):
    return f"{mm/10:.0f}"


def _material(plan):
    arq, v = plan["arquetipo"], plan["variante"]
    weld = "welded" if plan["weld"] else "bolted"
    if arq == "mesa_madera":
        return f"a {weld} steel frame with a solid wood top"
    if arq == "estanteria":
        base = "steel angle" if "angle" in v or v == "bolted_angle" else "steel tube"
        return f"{weld} {base}"
    if arq == "parrilla":
        return "welded and folded steel sheet" if plan["weld"] else "folded and riveted steel sheet"
    if arq == "banco":
        top = plan["dims"]["top_mat"]
        top = "a solid wood top" if top == "wood" else ("a plywood top" if top == "ply" else "a steel top")
        return f"a {weld} steel tube frame with {top}"
    return f"{weld} steel tube"


def _counts(plan):
    """Clausula con conteos EXACTOS por arquetipo/variante."""
    d, arq, v = plan["dims"], plan["arquetipo"], plan["variante"]
    if arq == "banco":
        c = "a flat rectangular work top on four straight legs"
        if v == "xbrace":
            c += ", with a single diagonal brace on each of the two ends"
        elif v == "shelf":
            c += ", with exactly one lower shelf"
        elif v == "rolling":
            c += ", standing on four castors"
        return c
    if arq == "estanteria":
        c = f"with exactly {d['n_shelves']} evenly spaced shelves - count them"
        if v == "diagonal":
            c += ", and one diagonal brace across the back"
        return c
    if arq == "rack_pared":
        return f"a wall-mounted panel with exactly {d['n_hooks']} hooks in a row"
    if arq == "carrito":
        c = f"with exactly {d['n_shelves']} shelves and four castors"
        if v == "handle_cart":
            c += ", and one push handle on top"
        return c
    if arq == "soporte":
        return {"a_frame": "a simple A-frame stand",
                "leaning": "a leaning ladder-style stand resting against nothing, free-standing",
                "firewood": "a rectangular log rack, open on the long sides",
                "hoop": "a single inverted-U tube hoop on two feet",
                "tiered": f"a tiered stand with {d['n_levels']} levels, each narrower going up"}[v]
    if arq == "mesa_madera":
        legs = {"hairpin": "thin hairpin rod", "straight_bolted": "straight square",
                "trapezoid": "trapezoid A-shaped", "box_frame": "boxed square",
                "cross_x": "crossed X"}[v]
        return f"a rectangular solid wood top on four {legs} metal legs"
    if arq == "parrilla":
        c = "an open rectangular firebox with a removable grate of parallel round bars"
        if v == "wheeled":
            c += ", on a stand with two steel wheels on one side"
        elif d["stand_h"] > 0:
            c += ", raised on four legs"
        else:
            c += ", tabletop size"
        return c
    if arq == "perchero":
        if v == "wall_mounted":
            return f"a wall-mounted bar with exactly {d['n_hooks']} hooks"
        if v == "ladder":
            return "a leaning ladder coat rack with rungs to hang from"
        c = f"a tall free-standing coat stand with exactly {d['n_hooks']} hooks near the top"
        if v == "bench_combo":
            c += ", and a low seat bench at the base"
        return c
    return "a metal item"


def cover_prompt(plan):
    d = plan["dims"]
    L = d.get("length") or d.get("width")
    P = d.get("depth", d.get("width", 400))
    H = d.get("height") or (d.get("stand_h", 0) + d.get("box_depth", 200)) or d.get("post_len", 800)
    obj = plan["subcategoria"].lower()
    return (
        f"Professional product photography of {_counts(plan)}. "
        f"It is a {obj}, built from {_material(plan)}, "
        f"about {_cm(L)} x {_cm(P)} cm and {_cm(H)} cm tall. "
        f"Finished in {plan['acabado_label'].lower()}. "
        f"Placed {plan['escena']}. "
        "Vertical 3:4 composition, photorealistic, sharp focus, soft daylight, "
        "gentle shadows, warm neutral palette. "
        "STRICT RULES: no people, no text, no letters, no numbers, no logos, "
        "no watermarks, no labels anywhere; absolutely NO dimension lines, NO "
        "measurement arrows, NO size annotations drawn on or near the object; "
        "show EXACTLY the counts described - do not add or remove shelves, "
        "hooks, bars, legs, castors or parts."
    )


# --- grilla: transforma cada paso en un panel visual (diverso y preciso) ---
def _panel(step, weld):
    s = step.lower()
    jverb = "welding" if weld else "bolting"
    # 1) acabado SIEMPRE primero (el paso 8 dice "deburr all welds..." -> no es soldar)
    if any(k in s for k in ("deburr", "apply", "finish", "sand and oil", " oil", "paint")):
        return "brushing paint and finish onto the completed metal item with a foam roller"
    if s.startswith("cut"):
        return "cutting steel tube to length with an angle grinder, sparks flying, on a bench"
    if "rivet" in s:
        return "setting rivets into a folded steel corner with a hand rivet gun"
    if "fold" in s:
        return "folding a flat steel sheet panel on a bench folder"
    if "castor" in s or "wheel" in s or "axle" in s:
        return "fitting a castor wheel to the underside of the frame with a spanner"
    # 2) uniones diferenciadas por el sustantivo del paso
    if any(k in s for k in ("weld", "bolt", "join", "tack", "attach")) or s.startswith(("stand the", "build the")):
        if "corner" in s:
            return f"{jverb} the top-frame corners square with clamps holding the joint"
        if "leg" in s:
            return f"{jverb} the legs onto the frame, the piece clamped upright"
        if "diagonal" in s or "brace" in s:
            return f"{jverb} a diagonal brace between the frame members"
        if "gusset" in s:
            return "bolting a drilled corner gusset onto the frame"
        if "apron" in s:
            return "bolting the aprons to the leg tabs with a spanner"
        if "rung" in s:
            return f"{jverb} a rung between the two side stiles"
        if "shelf frame" in s or "rail" in s or "frame" in s:
            return f"{jverb} a rectangular frame flat on the bench, checking it is square"
        return f"{jverb} two steel parts together"
    if "hook" in s:
        return "fixing a row of steel hooks onto the top bar"
    if "grate" in s or ("bar" in s and "cross" not in s):
        return "laying parallel round bars into the grate frame"
    if any(k in s for k in ("shelf", "panel", "plank", "top", "tray", "board", "seat")):
        return "dropping a shelf, panel or top into place in the frame"
    if any(k in s for k in ("level", "feet", "stand it", "mount", "lean it", "pad", "anchor")):
        return "standing the finished frame up and levelling the feet on the floor"
    return "checking the assembled steel frame is square with a combination square"


def grid_prompt(plan):
    steps = _pasos(plan)
    obj = plan["subcategoria"].lower()
    panels = [f"panel {i+1}: {_panel(st, plan['weld'])}" for i, st in enumerate(steps)]
    setting = "a clean bright metal workshop"
    return (
        "Photorealistic step-by-step build guide as a grid of exactly 8 photo "
        "panels, 2 columns x 4 rows, reading order left to right then top to "
        "bottom, panels running edge to edge separated only by thin white "
        "gutters - no outer border, no frame, no matte, no margin around the "
        f"grid. Each panel shows a metalworker's hands building a {obj} in {setting}. "
        + "; ".join(panels) + ". "
        "STRICT RULES: absolutely no text, no numbers, no letters, no labels, "
        "no arrows, no circles, no number badges, no watermarks in any panel; "
        "no finished-room scenes; every panel is a real construction step photo."
    )


def _pasos(plan):
    import armado_pasos
    return armado_pasos.pasos_en(plan)
