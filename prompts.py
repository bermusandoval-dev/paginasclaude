# -*- coding: utf-8 -*-
"""
prompts.py — Prompts de imagen (portada + grilla) por plano, en ingles.

Reglas aprendidas (doc seccion 4):
  * Portada: product photography con CONTEOS EXACTOS, material, medidas en cm,
    escena por subcategoria, STRICT RULES (sin texto/cotas/gente).
  * Grilla: 8 paneles 2x4, "metalworker's hands" (posesivo + oficio evita
    falsos positivos NSFW), 8 pasos DISTINTOS, sin texto/numeros/marcos.
"""

def _cm(mm):
    return f"{mm/10:.0f}"


def _dims_cm(plan):
    d, arq = plan["dims"], plan["arquetipo"]
    if arq in ("banco", "estanteria", "mesa_madera"):
        return d["length"], d["depth"], d["height"]
    if arq == "carrito":
        return d["length"], d["depth"], d["post_len"] + d["caster_h"]
    if arq == "rack_pared":
        return d["width"], None, d["height"]
    if arq == "soporte":
        return d["width"], d["depth"], d["height"]
    if arq == "parrilla":
        return d["width"], d["depth"], d["stand_h"] + d["box_depth"]
    if arq == "perchero":
        h = 400 if plan["variante"] == "wall_mounted" else d["height"]
        return d["width"], d["depth"], h
    return d.get("length", 500), d.get("depth", 400), d.get("height", 500)


def _dims_phrase(plan):
    w, dp, h = _dims_cm(plan)
    if dp is None:  # rack de pared
        return f"about {_cm(w)} cm wide and {_cm(h)} cm tall"
    return f"about {_cm(w)} x {_cm(dp)} cm and {_cm(h)} cm tall"


def _material(plan):
    arq, v = plan["arquetipo"], plan["variante"]
    weld = "welded" if plan["weld"] else "bolted"
    if arq == "mesa_madera":
        return f"a {weld} steel frame with a solid wood top"
    if arq == "estanteria":
        base = "steel angle" if "angle" in v else "steel tube"
        return f"{weld} {base}"
    if arq == "parrilla":
        return "welded steel sheet" if plan["weld"] else "folded and riveted steel sheet"
    if arq == "banco":
        top = plan["dims"]["top_mat"]
        top = "a solid wood top" if top == "wood" else ("a plywood top" if top == "ply" else "a steel top")
        return f"a {weld} steel tube frame with {top}"
    return f"{weld} steel tube"


def _counts(plan):
    """Frase 'It ...' con conteos EXACTOS por arquetipo/variante."""
    d, arq, v = plan["dims"], plan["arquetipo"], plan["variante"]
    if arq == "banco":
        c = "It has a flat rectangular work top on four straight legs"
        c += {"xbrace": ", with a single diagonal brace on each of the two ends",
              "shelf": ", with exactly one lower storage shelf",
              "rolling": ", standing on four castors"}.get(v, "")
        return c + "."
    if arq == "estanteria":
        c = f"It has exactly {d['n_shelves']} evenly spaced open shelves - count them"
        if v == "diagonal":
            c += ", plus one diagonal brace across the back"
        return c + "."
    if arq == "rack_pared":
        return f"It is a flat wall-mounted panel with exactly {d['n_hooks']} hooks in a single row."
    if arq == "carrito":
        c = f"It has exactly {d['n_shelves']} shelves and stands on four castors"
        if v == "handle_cart":
            c += ", with one push handle on top"
        return c + "."
    if arq == "soporte":
        return {"a_frame": "It is a simple A-frame stand.",
                "leaning": "It is a free-standing leaning ladder-style rack.",
                "firewood": "It is a low rectangular log rack, open on the long sides.",
                "hoop": "It is a single inverted-U tube hoop on two feet.",
                "tiered": f"It is a tiered stand with {d['n_levels']} levels, each one narrower going up."}[v]
    if arq == "mesa_madera":
        legs = {"hairpin": "thin hairpin rod", "straight_bolted": "straight square-tube",
                "trapezoid": "trapezoid A-shaped", "box_frame": "boxed square-tube",
                "cross_x": "crossed X-shaped"}[v]
        return f"It has a rectangular solid wood top on four {legs} metal legs."
    if arq == "parrilla":
        c = "It is an open rectangular firebox with a removable grate of parallel round bars"
        if v == "wheeled":
            c += ", on a stand with two steel wheels on one side"
        elif d["stand_h"] > 0:
            c += ", raised on four legs"
        else:
            c += ", tabletop size"
        return c + "."
    if arq == "perchero":
        if v == "wall_mounted":
            return f"It is a wall-mounted bar with exactly {d['n_hooks']} hooks."
        if v == "ladder":
            return "It is a leaning ladder coat rack with rungs to hang things over."
        c = f"It is a tall free-standing coat stand with exactly {d['n_hooks']} hooks near the top"
        if v == "bench_combo":
            c += ", and a low seat bench at the base"
        return c + "."
    return "A metal item."


def cover_prompt(plan):
    obj = plan["subcategoria"].lower()
    return (
        f"Professional product photography of a single {obj}. {_counts(plan)} "
        f"Built from {_material(plan)}, {_dims_phrase(plan)}. "
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


# ===========================================================================
# GRILLA: 8 paneles DISTINTOS por arquetipo (weld/bolt-aware).
# ===========================================================================
_CUT = "cutting steel to length with an angle grinder, sparks flying, on a bench"
_PAINT = "brushing the paint and finish onto the completed piece with a roller"


def grid_panels(plan):
    arq, d, v, weld = plan["arquetipo"], plan["dims"], plan["variante"], plan["weld"]
    J = "welding" if weld else "bolting"

    if arq == "banco":
        sig = {"xbrace": "welding a diagonal brace across each end of the frame",
               "shelf": "bolting the lower shelf rails and dropping the shelf panel in",
               "rolling": "bolting a lockable castor under each leg",
               "bolted": "bolting a drilled corner gusset at each frame joint"}.get(
            v, "checking the frame is square with a combination square")
        return [_CUT, "deburring and filing the cut tube ends",
                f"{J} the long and short rails into a rectangular top frame, clamped square",
                f"{J} the four legs to the corners of the top frame",
                sig, "setting the top panel on the frame and fixing it from underneath",
                "threading the levelling feet in and standing the bench up", _PAINT]

    if arq == "estanteria":
        step6 = ("welding the diagonal back brace corner to corner" if v == "diagonal"
                 else "sliding the shelf panels into their frames")
        return [_CUT, "drilling and deburring the shelf-rail ends",
                f"{J} the first shelf frame to the four upright posts",
                f"{J} the middle shelf frames up the posts at their marks",
                f"{J} the top shelf frame, keeping the posts vertical",
                step6, "standing the unit up and levelling the feet", _PAINT]

    if arq == "rack_pared":
        panel = {"mesh": "fitting the mesh panel into the frame",
                 "pegboard": "drilling the peg-hole grid in the steel panel",
                 "slat": "bending the cleat slats to a 45 degree profile",
                 "folded_shelf": "folding the U-channel shelf on a bench folder"}.get(
            v, "fitting the back panel into the frame")
        return [_CUT, f"{J} the rails between the two uprights into a flat panel frame",
                panel, "forming the hooks from steel rod",
                f"fixing exactly {d['n_hooks']} hooks across the bar, evenly spaced",
                "drilling the wall-fixing holes top and bottom",
                "holding the panel to the wall and marking the fixings", _PAINT]

    if arq == "carrito":
        sig = {"handle_cart": "welding the bent push handle to the back posts",
               "tray_top": "folding and fitting the lipped tray top",
               "mesh_shelves": "clipping the mesh shelf panels into the frames"}.get(
            v, "setting the steel shelf panels into the frames")
        return [_CUT, f"{J} the shelf frames square on the bench",
                f"{J} the shelf frames to the four posts at their heights",
                sig, "bolting a castor under each of the four legs",
                "standing the cart up and locking the braked castors",
                "checking the shelves sit level", _PAINT]

    if arq == "soporte":
        seqs = {
            "a_frame": ["marking and cutting the splayed foot angles on the legs",
                        "welding the four legs to the top ridge bar",
                        "welding the cross ties between the leg pairs",
                        "checking the A-frame stands square"],
            "leaning": ["cutting the stile tops and feet at a 15 degree angle",
                        "bolting the rungs between the two stiles",
                        "fitting rubber caps to the feet",
                        "leaning it on the wall to check it sits flat"],
            "firewood": ["bolting the long and short rails between the uprights",
                         "fitting the floor bars to keep logs off the ground",
                         "squaring the rectangular rack up",
                         "checking the bottom rail sits about 120 mm up"],
            "hoop": ["cold-bending the tube into an inverted-U hoop",
                     "welding a drilled foot plate to each leg",
                     "grinding the welds smooth",
                     "marking the floor holes to bolt it down"],
            "tiered": ["assembling each tier tray, narrower going up",
                       "bolting the corner links to space the tiers",
                       "checking each tier sits level",
                       "fitting rubber feet to the base"],
        }[v]
        return [_CUT] + seqs[:3] + [seqs[3], "standing the finished stand up", _PAINT]

    if arq == "mesa_madera":
        sig = {"hairpin": "welding two steel rods into each hairpin leg",
               "straight_bolted": "drilling and bolting the leg top plates",
               "trapezoid": "welding each trapezoid leg pair to its bars",
               "box_frame": "mitring and welding the box frame corners",
               "cross_x": "bolting each pair of bars at the centre X pivot"}[v]
        return [_CUT, sig, f"{J} the two leg assemblies, checking they match",
                f"{J} the legs and rails into the table base",
                "checking the base is square and flat",
                "laying the wood planks on top with even 5 mm gaps",
                "screwing the wood top down from under the frame",
                "sanding and oiling the wood top"]

    if arq == "parrilla":
        if v in ("folded_box", "riveted"):
            body = ["folding the firebox sides up on a bench folder",
                    "riveting the firebox corners with a hand rivet gun"]
        else:
            body = ["tacking the box-frame angles square",
                    "welding the side and base sheet onto the frame"]
        step6 = ("fitting the axle and two wheels to the back legs" if v == "wheeled"
                 else ("bolting the legs under the firebox" if not weld else "welding the legs under the firebox"))
        tail = "brushing high-temp finish onto the completed grill"
        return [_CUT] + body + ["drilling the air holes in the base",
                                 "laying the round bars into the grate frame",
                                 step6, "sitting the grate in and checking the gaps", tail]

    if arq == "perchero":
        if v == "wall_mounted":
            return [_CUT, "drilling the wall bar for the fixings",
                    "forming the hooks from steel rod",
                    f"fixing exactly {d['n_hooks']} hooks along the bar",
                    "fitting the shelf and brackets if used",
                    "marking the wall and drilling the fixings",
                    "mounting the bar level on the wall", _PAINT]
        if v == "ladder":
            return [_CUT, "cutting the stile ends at a 15 degree angle",
                    "bolting the rungs between the two stiles",
                    "checking the frame is flat and square",
                    "fitting rubber feet to the base",
                    "leaning it on the wall to test it",
                    "hanging a coat over the top rung", _PAINT]
        sig = ("fitting the seat board at the base" if v == "bench_combo"
               else "checking the tower stands plumb")
        return [_CUT, f"{J} the top hook bar across the two uprights",
                f"{J} the T-feet to the base of the uprights",
                "forming the hooks from steel rod",
                f"fixing exactly {d['n_hooks']} hooks along the top bar",
                sig, "standing the coat stand up and checking it is stable", _PAINT]

    return [_CUT] + ["assembling the steel frame"] * 6 + [_PAINT]


def grid_prompt(plan):
    obj = plan["subcategoria"].lower()
    panels = grid_panels(plan)[:8]
    lines = "; ".join(f"panel {i+1}: {p}" for i, p in enumerate(panels))
    return (
        "Photorealistic step-by-step build guide as a grid of exactly 8 photo "
        "panels, 2 columns x 4 rows, reading order left to right then top to "
        "bottom, panels running edge to edge separated only by thin white "
        "gutters - no outer border, no frame, no matte, no margin around the "
        f"grid. Each panel shows a metalworker's hands building a {obj} in a "
        f"clean bright metal workshop. {lines}. "
        "STRICT RULES: absolutely no text, no numbers, no letters, no labels, "
        "no arrows, no circles, no number badges, no watermarks in any panel; "
        "no finished-room scenes; every panel is a real construction step photo."
    )
