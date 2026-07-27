# -*- coding: utf-8 -*-
"""
armado_pasos.py — Genera los 8 pasos de construccion (captions pagina 4).

En vez de un dict PASOS_EN de 40 plantillas a mano, generamos los 8 pasos
desde el despiece real: cada caption es "detalle con mm", adaptado a
soldado/atornillado y a la variante, y el paso 8 siempre cierra en el
acabado ("Deburr all welds/edges and apply the finish."). Todo en ingles.
"""


def _refs(plan):
    by_ref = {pz["ref"]: pz for pz in plan["piezas"]}
    return by_ref


def _find(plan, *subs):
    for pz in plan["piezas"]:
        low = pz["nombre"].lower()
        if all(s in low for s in subs):
            return pz
    return None


def _angle_note(plan):
    for a in plan["angulos"]:
        if "deg" in a.lower() and "90" not in a:
            return a[0].lower() + a[1:]
    return None


def pasos_en(plan):
    arq, d, v, weld = plan["arquetipo"], plan["dims"], plan["variante"], plan["weld"]
    R = _refs(plan)
    J = "Weld" if weld else "Bolt"
    j = "weld" if weld else "bolt"
    finish = ("Deburr all welds" if weld else "Deburr every edge") + \
             f", then apply {plan['acabado_label'].lower()}."
    ang = _angle_note(plan)
    steps = []

    if arq == "banco":
        L, P, H = d["length"], d["depth"], d["height"]
        A, Bp, C, Dp = R["A"], R["B"], R["C"], R["D"]
        steps = [
            f"Cut all parts to the list: 4 legs at {A['largo']} mm and the top rails at {Bp['largo']} and {C['largo']} mm.",
            f"Lay the two long and two short rails into a {L} x {P} mm rectangle; check the diagonals are equal.",
            f"{J} the four top-frame corners square at 90 degrees.",
            f"Stand the 4 legs so the top face sits {H} mm off the floor and {j} them to the frame.",
        ]
        if v == "xbrace":
            steps.append(f"Fit the two end diagonals ({ang or 'at the marked angle'}) and {j} both toes.")
        elif v == "shelf":
            steps.append("Bolt the lower rails and drop in the shelf panel 180 mm above the floor.")
        elif v == "rolling":
            steps.append("Bolt a castor plate under each leg - two of the four with brakes.")
        elif v == "bolted":
            steps.append("Add a drilled corner gusset at each top corner with 3 x M8 into the captive nuts.")
        else:
            steps.append("Check the frame is square and twist-free before the joints set.")
        steps += [
            f"Fit the {d['top_mat']} top {L} x {P} mm and fix it down from underneath.",
            ("Lock the two braked castors" if v == "rolling" else "Thread in the four levelling feet") + " and set it dead level.",
            finish,
        ]

    elif arq == "estanteria":
        L, P, H, n = d["length"], d["depth"], d["height"], d["n_shelves"]
        A = R["A"]
        heights = None
        for pos in plan["posiciones_clave"]:
            if "Shelf 1" in pos:
                heights = pos
        steps = [
            f"Cut 4 posts at {A['largo']} mm and the {2*n} long + {2*n} short shelf rails to length.",
            f"Build the {n} shelf frames flat, each {L-2*d['post_sec']} x {P-2*d['post_sec']} mm inside the rails.",
            f"Mark the shelf heights up each post ({heights or 'per the key positions'}).",
            f"{J} the first shelf frame to all four posts, checking the posts stay vertical.",
            f"Work up the posts, {j}ing each remaining shelf frame at its mark.",
        ]
        if v == "diagonal":
            steps.append(f"Add the back diagonal brace corner-to-corner ({ang or ''}) and {j} both ends.")
        elif v in ("mesh_shelves", "wood_shelves", "bolted_angle"):
            steps.append(f"Drop the {n} shelf panels into their frames and clip/bolt them down.")
        else:
            steps.append(f"Drop the {n} steel shelf panels in and fix the edges.")
        steps += [
            "Stand it up, level the feet, and (if tall) anchor the top to the wall.",
            finish,
        ]

    elif arq == "rack_pared":
        W, H, nh = d["width"], d["height"], d["n_hooks"]
        steps = [
            f"Cut 2 uprights at {H} mm and the cross rails at {W-2*d['rail_sec']} mm.",
            f"{J} or bolt the rails between the uprights into a {W} x {H} mm frame.",
            "Check the frame is square and flat against a bench.",
            f"Fit the panel/slats and set out the {nh} hook positions.",
            f"Fix the {nh} hooks on their marks (even pitch across the bar).",
            "Drill the top and bottom fixing holes for the wall.",
            "Mount it plumb on the wall, into studs or with wall plugs.",
            finish,
        ]

    elif arq == "carrito":
        L, P, n = d["length"], d["depth"], d["n_shelves"]
        A = R["A"]
        steps = [
            f"Cut 4 posts at {A['largo']} mm and the {2*n} long + {2*n} short shelf rails.",
            f"Build the {n} shelf frames {L-2*d['post_sec']} x {P-2*d['post_sec']} mm.",
            f"{J} the shelf frames to the posts at their heights, keeping the posts vertical.",
            f"Fit the {n} shelf panels and fix the edges.",
        ]
        if v == "handle_cart":
            steps.append("Fit the bent push handle to the top of the back posts (two 90 degree bends).")
        elif v == "tray_top":
            steps.append("Fold and fit the lipped top tray with a 30 mm lip all round.")
        else:
            steps.append("Check the cart is square and the shelves sit level.")
        steps += [
            f"Bolt a {d['caster_h']} mm castor under each leg - two with brakes.",
            "Roll it, lock the brakes, and confirm it does not rock.",
            finish,
        ]

    elif arq == "soporte":
        steps = [
            "Cut all parts to the list and mark every angled end.",
            f"Set out the main frame and {j} the first joints, checking the key angles.",
            f"{J} or bolt the cross members to tie the frame together.",
        ]
        if v == "a_frame":
            steps += [f"Join the four legs to the top ridge ({ang or 'at the splay angle'}).",
                      "Add the cross ties between the leg pairs.",
                      "Stand it up and check it is stable and does not rock."]
        elif v == "hoop":
            steps += ["Cold-bend the tube into the inverted-U hoop.",
                      "Weld a drilled foot plate to each leg.",
                      "Bolt the feet to the floor on the marked centres."]
        elif v == "leaning":
            steps += [f"Cut the stile tops and feet at {ang or '15 deg'} so they lean and sit flat.",
                      "Bolt the shelf rungs between the stiles at their heights.",
                      "Lean it against the wall and check the feet sit flat."]
        elif v == "firewood":
            steps += ["Bolt the long and short rails between the four uprights.",
                      "Fit the floor bars to keep the logs off the ground.",
                      "Set it level; the bottom rail should sit ~120 mm up."]
        else:  # tiered
            steps += ["Assemble each tier tray, narrowing by 80 mm as you go up.",
                      "Bolt the corner links to space the tiers apart.",
                      "Check every tier sits level."]
        steps.append(finish)

    elif arq == "mesa_madera":
        L, P, H = d["length"], d["depth"], d["height"]
        steps = [
            "Cut the leg parts and mark any angled ends from the drawing.",
            f"Build the two leg assemblies ({j}ed), checking they match.",
        ]
        if v in ("hairpin",):
            steps.append(f"Weld each 2-rod hairpin to its drilled top plate ({ang or ''}).")
        elif v == "cross_x":
            steps.append("Bolt each pair of bars at the centre pivot to form the X.")
        elif v == "trapezoid":
            steps.append(f"Weld the trapezoid legs to their foot and top bars ({ang or ''}).")
        elif v == "box_frame":
            steps.append("Mitre and weld the box frame, then add the legs at the corners.")
        else:
            steps.append("Bolt the aprons to the leg tabs, two M8 per corner.")
        steps += [
            f"Join the two leg frames with the stretcher/aprons into a {L} x {P} mm base.",
            f"Check the frame is square and the top will sit {H} mm off the floor.",
            f"Lay the {d['n_planks']} wood planks on top with 5 mm gaps and screw up from the frame.",
            "Sand and oil the wood top; check it does not wobble.",
            finish,
        ]

    elif arq == "parrilla":
        W, P, bd, nb = d["width"], d["depth"], d["box_depth"], d["n_bars"]
        if v in ("folded_box", "riveted"):
            steps = [
                f"Cut and mark the sheet blank for a {W} x {P} x {bd} mm firebox.",
                "Fold up the four sides on the marked lines.",
                "Rivet the corner tabs (two rivets per corner).",
            ]
        else:
            steps = [
                f"Cut the sheet panels and the box-frame angles for a {W} x {P} x {bd} mm firebox.",
                "Tack the angle frame square, then weld the side and base sheet on.",
                "Drill the air holes in the base.",
            ]
        steps += [
            f"Make the grate: {nb} round bars in their frame, on an even pitch.",
        ]
        if d["stand_h"] > 0:
            steps.append(f"{'Weld' if weld else 'Bolt'} the stand legs under the box so the rim sits {d['stand_h']+bd} mm up.")
            if v == "wheeled":
                steps.append("Fit the axle and two wheels to the back legs.")
            else:
                steps.append("Fit the cross rails to tie the legs and check it stands firm.")
        else:
            steps.append("Check the firebox sits flat and square on a tabletop.")
            steps.append("Fit the grate and confirm it drops in level.")
        steps += [
            "Sit the grate in place and confirm even gaps for airflow.",
            ("Deburr all welds" if weld else "Deburr every edge") + ", then apply the high-temp BBQ finish.",
        ]
        steps = steps[:8]

    elif arq == "perchero":
        W, H, nh = d["width"], d["height"], d["n_hooks"]
        if v == "wall_mounted":
            steps = [
                f"Cut the wall bar at {W} mm and drill it for the wall plugs.",
                f"Set out and fix the {nh} hooks along the bar on an even pitch.",
                "If fitted, bolt the shelf brackets and folded shelf on top.",
                "Mark the wall, drill, and plug the fixing points.",
                "Mount the bar level and plumb on the wall.",
                "Load-test one hook gently before use.",
                "Touch up any drilled edges.",
                finish,
            ]
        elif v == "ladder":
            steps = [
                f"Cut the two stiles and the 5 rungs; cut the ends at 15 deg.",
                "Bolt the rungs between the stiles at their heights.",
                "Check the frame is flat and the lean angle is even.",
                "Add rubber feet so it grips the floor.",
                "Lean it on the wall and confirm it is stable.",
                "Hang a test load over the top rungs.",
                "Deburr every edge and cut end.",
                finish,
            ]
        else:
            steps = [
                f"Cut 2 uprights at {H} mm, the top bar, feet and (if any) shelf rails.",
                f"{J} the top hook bar across the uprights, kept square.",
                f"{J} the T-feet to the base of each upright so it stands plumb.",
                f"Fix the {nh} hooks along the top bar on an even pitch.",
            ]
            if v == "bench_combo":
                steps.append("Fit the seat rails and wood seat board 450 mm off the floor.")
            elif _find(plan, "shelf") or _find(plan, "seat"):
                steps.append("Fit the lower shelf rails and board at their height.")
            else:
                steps.append("Check the tower stands upright without rocking.")
            steps += [
                "Stand it up and confirm it is stable under a hung coat.",
                "Add rubber floor pads under the feet.",
                finish,
            ]

    # normaliza a exactamente 8
    steps = [s for s in steps if s]
    while len(steps) < 8:
        steps.insert(-1, "Check all joints are tight and everything sits square.")
    return steps[:8]
