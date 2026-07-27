# -*- coding: utf-8 -*-
"""
planos_svg.py — Pagina 3: Technical Drawing & Cut List (SVG a escala honesta).

Contiene:
  * DOS vistas (front + side/top) con cotas reales, escala 1:X honesta.
  * Cut list completa (ref, part, qty, size, profile).
  * PARTS AS CUT · TRUE SHAPES: un icono por pieza con su forma real,
    inferida por palabras clave de la nota/perfil (tube, angle, folded,
    mesh, drilled plate, round rod, mitred / cut at N deg...).
  * KEY POSITIONS & ANGLES: posiciones en mm y todos los angulos.
  * Detalle ampliado de la union dificil.

Todo en ingles, medidas en mm. A4 794x1123.
"""
import math
import svg_base as B

# ---- estilos de linea para el dibujo ----
def _style(kind):
    return {
        "solid":  (B.CARBON, 1.3, None),
        "thick":  (B.CARBON, 2.0, None),
        "thin":   (B.INK_SOFT, 0.8, None),
        "dash":   (B.CARBON, 1.0, "5,3"),
        "hidden": (B.INK_FAINT, 0.8, "3,3"),
    }[kind]


# ===========================================================================
# Vistas por arquetipo -> dict {w_mm, h_mm, prim[], extra[]}
#   prim: ("rect",x,y,w,h,style) | ("line",x1,y1,x2,y2,style) |
#         ("circ",cx,cy,r,style) | ("pl",[(x,y)..],closed,style)
#   coordenadas en mm, origen abajo-izquierda, y hacia ARRIBA.
#   extra: cotas custom ("h",x_mm,y0,y1,label) o ("w",y_mm,x0,x1,label)
# ===========================================================================
def _rect(x, y, w, h, st="solid"):
    return ("rect", x, y, w, h, st)


def _shelf_heights(H, n, top_margin=60):
    gap = (H - top_margin) / n
    return [round(top_margin + gap * (i + 1)) for i in range(n)]


def vistas(plan):
    arq, d, v = plan["arquetipo"], plan["dims"], plan["variante"]
    F = {"prim": [], "extra": []}
    S = {"prim": [], "extra": []}

    if arq == "banco":
        L, P, H, T, ls, rs = d["length"], d["depth"], d["height"], d["top_thickness"], d["leg_sec"], d["rail_sec"]
        F.update(w_mm=L, h_mm=H, title="Front elevation")
        F["prim"] += [_rect(0, H - T, L, T, "solid"), _rect(0, 0, ls, H - T), _rect(L - ls, 0, ls, H - T)]
        if v == "shelf":
            F["prim"].append(_rect(ls, 180, L - 2 * ls, rs))
            F["extra"].append(("h", -1, 0, 180, "180"))
        S.update(w_mm=P, h_mm=H, title="Side elevation")
        S["prim"] += [_rect(0, H - T, P, T, "solid"), _rect(0, 0, ls, H - T), _rect(P - ls, 0, ls, H - T)]
        if v == "xbrace":
            S["prim"] += [("line", ls, 0, P - ls, H - T, "solid"), ("line", P - ls, 0, ls, H - T, "solid")]

    elif arq == "estanteria":
        L, P, H, n, ps = d["length"], d["depth"], d["height"], d["n_shelves"], d["post_sec"]
        F.update(w_mm=L, h_mm=H, title="Front elevation")
        F["prim"] += [_rect(0, 0, ps, H), _rect(L - ps, 0, ps, H)]
        for h in _shelf_heights(H, n):
            F["prim"].append(_rect(ps, h - ps, L - 2 * ps, ps, "thick"))
            if h < H * 0.97:   # el estante superior coincide con la cota de alto total
                F["extra"].append(("h", -1, 0, h, str(h)))
        S.update(w_mm=P, h_mm=H, title="Side elevation")
        S["prim"] += [_rect(0, 0, ps, H), _rect(P - ps, 0, ps, H)]
        for h in _shelf_heights(H, n):
            S["prim"].append(("line", 0, h, P, h, "thick"))
        if v == "diagonal":
            S["prim"].append(("line", ps, 0, P - ps, H, "solid"))

    elif arq == "rack_pared":
        W, H, rs, nh = d["width"], d["height"], d["rail_sec"], d["n_hooks"]
        F.update(w_mm=W, h_mm=H, title="Front elevation")
        F["prim"] += [_rect(0, 0, rs, H), _rect(W - rs, 0, rs, H),
                      _rect(rs, H - rs, W - 2 * rs, rs, "thick"), _rect(rs, 0, W - 2 * rs, rs, "thick")]
        margin = 60
        for i in range(nh):
            hx = margin + (0 if nh == 1 else (W - 2 * margin) * i / (nh - 1))
            F["prim"].append(("line", hx, rs, hx, rs - 22, "thick"))
        S.update(w_mm=90, h_mm=H, title="Side view")
        S["prim"] += [_rect(0, 0, rs, H)]
        for i in range(min(nh, 4)):
            yy = H * (i + 1) / (min(nh, 4) + 1)
            S["prim"].append(("pl", [(rs, yy), (70, yy), (70, yy - 24)], False, "thick"))

    elif arq == "carrito":
        L, P, PL, n, ps, ch = d["length"], d["depth"], d["post_len"], d["n_shelves"], d["post_sec"], d["caster_h"]
        F.update(w_mm=L, h_mm=PL + ch, title="Front elevation")
        F["prim"] += [_rect(0, ch, ps, PL), _rect(L - ps, ch, ps, PL)]
        for i in range(n):
            hy = ch + PL * (i + 1) / (n + 0.5)
            F["prim"].append(_rect(ps, hy, L - 2 * ps, ps, "thick"))
            F["extra"].append(("h", -1, 0, round(hy), str(round(hy))))
        F["prim"] += [("circ", ps, ch / 2, ch / 2, "solid"), ("circ", L - ps, ch / 2, ch / 2, "solid")]
        if v == "handle_cart":
            F["prim"].append(("pl", [(0, ch + PL), (0, ch + PL + 120), (L, ch + PL + 120), (L, ch + PL)], False, "solid"))
            F["h_mm"] = PL + ch + 120
        S.update(w_mm=P, h_mm=PL + ch, title="Side elevation")
        S["prim"] += [_rect(0, ch, ps, PL), _rect(P - ps, ch, ps, PL),
                      ("circ", ps, ch / 2, ch / 2, "solid"), ("circ", P - ps, ch / 2, ch / 2, "solid")]

    elif arq == "soporte":
        W, P, H, s = d["width"], d["depth"], d["height"], d["sec"]
        if v == "a_frame":
            F.update(w_mm=W, h_mm=H, title="End (gable)")
            F["prim"] += [("pl", [(0, 0), (W / 2, H), (W, 0)], False, "solid"),
                          ("line", W * 0.25, H / 2, W * 0.75, H / 2, "solid")]
            S.update(w_mm=P, h_mm=H, title="Side")
            S["prim"] += [("pl", [(0, 0), (P / 2, H), (P, 0)], False, "solid")]
        elif v == "leaning":
            off = math.tan(math.radians(15)) * H
            F.update(w_mm=W + off, h_mm=H, title="Front")
            F["prim"] += [("line", 0, 0, off, H, "solid"), ("line", W, 0, W + off, H, "solid")]
            for hh in _shelf_heights(H, d["n_levels"], 0)[:d["n_levels"]]:
                xx = off * hh / H
                F["prim"].append(("line", xx, hh, W + xx, hh, "thick"))
            S.update(w_mm=off + 40, h_mm=H, title="Side")
            S["prim"] += [("line", 0, 0, off, H, "solid")]
        elif v == "firewood":
            F.update(w_mm=W, h_mm=H, title="Front")
            F["prim"] += [_rect(0, 0, s, H), _rect(W - s, 0, s, H),
                          _rect(s, H - s, W - 2 * s, s, "thick"), _rect(s, 120, W - 2 * s, s, "thick")]
            for i in range(5):
                xx = s + (W - 2 * s) * i / 4
                F["prim"].append(("line", xx, 120, xx, 120 + 40, "thin"))
            S.update(w_mm=P, h_mm=H, title="Side")
            S["prim"] += [_rect(0, 0, s, H), _rect(P - s, 0, s, H)]
        elif v == "hoop":
            F.update(w_mm=W, h_mm=H, title="Front")
            F["prim"] += [("line", 0, 0, 0, H - W / 2, "solid"), ("line", W, 0, W, H - W / 2, "solid"),
                          ("pl", [(0, H - W / 2), (W * 0.15, H), (W * 0.85, H), (W, H - W / 2)], False, "solid"),
                          _rect(-30, -10, 60, 12, "fill" if False else "thick"), _rect(W - 30, -10, 60, 12, "thick")]
            S.update(w_mm=P, h_mm=H, title="Side")
            S["prim"] += [("line", P / 2, 0, P / 2, H, "solid")]
        else:  # tiered
            nl = d["n_levels"]
            F.update(w_mm=W, h_mm=H, title="Front")
            for i in range(nl):
                lw = W - i * 80
                yy = H * (i + 1) / nl
                F["prim"].append(_rect((W - lw) / 2, yy - s, lw, s, "thick"))
            F["prim"] += [("line", 10, 0, 10, H, "thin"), ("line", W - 10, 0, W - 10, H, "thin")]
            S.update(w_mm=P, h_mm=H, title="Side")
            for i in range(nl):
                yy = H * (i + 1) / nl
                S["prim"].append(("line", 0, yy, P, yy, "thick"))

    elif arq == "mesa_madera":
        L, P, H, T, ls = d["length"], d["depth"], d["height"], d["top_thickness"], d["leg_top_sec"]
        fh = H - T
        F.update(w_mm=L, h_mm=H, title="Front elevation")
        F["prim"].append(_rect(0, fh, L, T, "solid"))
        if v == "hairpin":
            F["prim"] += [("line", 40, fh, 0, 0, "solid"), ("line", 60, fh, 120, 0, "solid"),
                          ("line", L - 40, fh, L, 0, "solid"), ("line", L - 60, fh, L - 120, 0, "solid")]
        elif v == "trapezoid":
            F["prim"] += [("line", L * 0.32, fh, L * 0.12, 0, "solid"), ("line", L * 0.68, fh, L * 0.88, 0, "solid"),
                          ("line", L * 0.12, 0, L * 0.32, fh, "hidden")]
        elif v == "cross_x":
            F["prim"] += [("line", 40, 0, L * 0.45, fh, "solid"), ("line", L * 0.45, 0, 40, fh, "solid"),
                          ("line", L - 40, 0, L * 0.55, fh, "solid"), ("line", L * 0.55, 0, L - 40, fh, "solid")]
        elif v == "box_frame":
            F["prim"] += [_rect(0, fh - ls, L, ls, "solid"), _rect(0, 0, ls, fh), _rect(L - ls, 0, ls, fh)]
        else:  # straight_bolted
            F["prim"] += [_rect(40, 0, ls, fh), _rect(L - 40 - ls, 0, ls, fh)]
        S.update(w_mm=P, h_mm=H, title="Side elevation")
        S["prim"].append(_rect(0, fh, P, T, "solid"))
        S["prim"] += [_rect(20, 0, ls, fh), _rect(P - 20 - ls, 0, ls, fh)]

    elif arq == "parrilla":
        W, P, bd, sh, nb = d["width"], d["depth"], d["box_depth"], d["stand_h"], d["n_bars"]
        F.update(w_mm=W, h_mm=sh + bd, title="Front elevation")
        F["prim"].append(_rect(0, sh, W, bd, "solid"))
        F["prim"].append(("line", 3, sh + bd - 25, W - 3, sh + bd - 25, "thick"))
        if sh > 0:
            F["prim"] += [_rect(6, 0, 30, sh), _rect(W - 36, 0, 30, sh)]
            F["extra"].append(("h", -1, 0, sh, str(sh)))
        S.update(w_mm=P, h_mm=sh + bd, title="Top view (grate)")
        S["prim"].append(_rect(0, sh, P, bd, "solid"))
        for i in range(nb):
            xx = 20 + (P - 40) * i / (nb - 1) if nb > 1 else P / 2
            S["prim"].append(("line", xx, sh + 3, xx, sh + bd - 3, "thick"))

    elif arq == "perchero":
        W, H, P, nh, ps = d["width"], d["height"], d["depth"], d["n_hooks"], d["post_sec"]
        if v == "wall_mounted":
            H2 = min(H, 400)
            F.update(w_mm=W, h_mm=H2, title="Front")
            F["prim"].append(_rect(0, H2 - ps, W, ps, "thick"))
            for i in range(nh):
                hx = 60 + (W - 120) * i / (nh - 1) if nh > 1 else W / 2
                F["prim"].append(("line", hx, H2 - ps, hx, H2 - ps - 26, "thick"))
            if d.get("shelf"):
                F["prim"].append(_rect(0, H2 - 6, W, 6, "solid"))
            S.update(w_mm=P, h_mm=H2, title="Side")
            S["prim"].append(("line", 0, H2 - ps, P, H2 - ps, "thick"))
        elif v == "ladder":
            off = math.tan(math.radians(15)) * H
            F.update(w_mm=W + off, h_mm=H, title="Front")
            F["prim"] += [("line", 0, 0, off, H, "solid"), ("line", W, 0, W + off, H, "solid")]
            for i in range(5):
                hh = H * (i + 1) / 6
                xx = off * hh / H
                F["prim"].append(("line", xx, hh, W + xx, hh, "thick"))
            S.update(w_mm=off + 40, h_mm=H, title="Side")
            S["prim"].append(("line", 0, 0, off, H, "solid"))
        else:
            F.update(w_mm=W, h_mm=H, title="Front elevation")
            F["prim"] += [_rect(0, 0, ps, H), _rect(W - ps, 0, ps, H),
                          _rect(ps, H - ps, W - 2 * ps, ps, "thick")]
            for i in range(nh):
                hx = ps + 30 + (W - 2 * ps - 60) * i / (nh - 1) if nh > 1 else W / 2
                F["prim"].append(("line", hx, H - ps, hx, H - ps - 26, "thick"))
            F["prim"] += [("pl", [(-P * 0.15, 0), (ps + P * 0.15, 0)], False, "thick"),
                          ("pl", [(W - ps - P * 0.15, 0), (W + P * 0.15, 0)], False, "thick")]
            S.update(w_mm=P, h_mm=H, title="Side elevation")
            S["prim"] += [_rect(P / 2 - ps / 2, 0, ps, H), _rect(0, 0, P, ps, "thick")]

    else:
        F.update(w_mm=d.get("length", 500), h_mm=d.get("height", 500), title="Front")
        S.update(w_mm=d.get("depth", 400), h_mm=d.get("height", 500), title="Side")
    return F, S


# ---- eleccion de escala honesta 1:X ----
_CAND = [5, 8, 10, 12, 15, 20, 25, 30, 40]
_PAPER_MM_PER_PX = 210.0 / B.PAGE_W  # A4 ancho 210 mm


def escala(real_max_mm, avail_px):
    for X in _CAND:
        ppm = 1.0 / (X * _PAPER_MM_PER_PX)   # px por mm a esa escala
        if real_max_mm * ppm <= avail_px:
            return X, ppm
    X = _CAND[-1]
    return X, 1.0 / (X * _PAPER_MM_PER_PX)


# ---- dibujo de una vista ----
def draw_view(cx, cy, cw, ch, view, ppm):
    """Dibuja la vista centrada en la celda (cx,cy,cw,ch). Cotas W y H auto."""
    s = []
    w_px = view["w_mm"] * ppm
    h_px = view["h_mm"] * ppm
    pad_l, pad_b, pad_t = 34, 30, 20
    ox = cx + pad_l + max(0, (cw - pad_l - w_px) / 2)
    baseline = cy + ch - pad_b - max(0, (ch - pad_t - pad_b - h_px) / 2)

    def X(mm): return ox + mm * ppm
    def Y(mm): return baseline - mm * ppm

    s.append(B.t(cx + cw / 2, cy + 12, view.get("title", ""), size=9.5,
                 weight="bold", fill=B.STEEL, anchor="middle", font=B.MONO))

    for pr in view["prim"]:
        kind = pr[0]
        if kind == "rect":
            _, x, y, w, h, st = pr
            col, sw, dash = _style(st)
            fill = B.PANEL if st in ("solid", "thick") else "none"
            s.append(B.rect(X(x), Y(y + h), w * ppm, h * ppm, fill=fill, stroke=col, sw=sw, dash=dash))
        elif kind == "line":
            _, x1, y1, x2, y2, st = pr
            col, sw, dash = _style(st)
            s.append(B.line(X(x1), Y(y1), X(x2), Y(y2), stroke=col, sw=sw, dash=dash))
        elif kind == "circ":
            _, ccx, ccy, r, st = pr
            col, sw, dash = _style(st)
            s.append(B.circle(X(ccx), Y(ccy), r * ppm, stroke=col, sw=sw))
        elif kind == "pl":
            _, pts, closed, st = pr
            col, sw, dash = _style(st)
            s.append(B.polyline([(X(a), Y(b)) for a, b in pts], stroke=col, sw=sw, closed=closed, dash=dash))

    # cota ancho (abajo)
    dy = baseline + 15
    s.append(_dim_h(ox, X(view["w_mm"]), dy, f"{view['w_mm']}"))
    # cota alto (izquierda)
    dx = ox - 16
    s.append(_dim_v(dx, baseline, Y(view["h_mm"]), f"{view['h_mm']}"))
    # cotas custom
    for e in view.get("extra", []):
        if e[0] == "h":
            _, _, y0, y1, lab = e
            s.append(_dim_v(ox - 30, Y(y0), Y(y1), lab, minor=True))
    return "\n".join(s)


def _dim_h(x0, x1, y, label):
    s = [B.line(x0, y, x1, y, stroke=B.STEEL, sw=0.8),
         B.line(x0, y - 4, x0, y + 4, stroke=B.STEEL, sw=0.8),
         B.line(x1, y - 4, x1, y + 4, stroke=B.STEEL, sw=0.8),
         B.rect((x0 + x1) / 2 - 20, y - 6, 40, 12, fill=B.WHITE),
         B.t((x0 + x1) / 2, y + 3.5, label, size=9, fill=B.STEEL, anchor="middle", font=B.MONO)]
    return "\n".join(s)


def _dim_v(x, y0, y1, label, minor=False):
    col = B.INK_FAINT if minor else B.STEEL
    s = [B.line(x, y0, x, y1, stroke=col, sw=0.8),
         B.line(x - 4, y0, x + 4, y0, stroke=col, sw=0.8),
         B.line(x - 4, y1, x + 4, y1, stroke=col, sw=0.8),
         f'<g transform="translate({x-4:.1f},{(y0+y1)/2:.1f}) rotate(-90)">'
         f'{B.rect(-16,-6,32,12,fill=B.WHITE)}'
         f'{B.t(0,3.5,label,size=8.5,fill=col,anchor="middle",font=B.MONO)}</g>']
    return "\n".join(s)


# ===========================================================================
# TRUE SHAPES: icono por pieza segun palabras clave
# ===========================================================================
def true_shape_icon(x, y, w, h, pieza):
    """Dibuja el icono de forma real dentro de (x,y,w,h). Devuelve svg."""
    nota = (pieza["nota"] + " " + pieza["perfil"]).lower()
    cx, cy = x + w / 2, y + h / 2
    s = []
    col = B.CARBON

    def bar(bevel_l=False, bevel_r=False, angle_txt=None):
        bw, bh = w * 0.7, h * 0.34
        x0, y0 = cx - bw / 2, cy - bh / 2
        pts = [(x0 + (bh if bevel_l else 0), y0), (x0 + bw - (bh if bevel_r else 0), y0),
               (x0 + bw, y0 + bh), (x0, y0 + bh)]
        return B.polyline(pts, stroke=col, sw=1.3, closed=True, fill=B.PANEL)

    if "angle" in nota:
        # perfil en L (seccion)
        L = min(w, h) * 0.6
        x0, y0 = cx - L / 2, cy - L / 2
        s.append(B.polyline([(x0, y0), (x0, y0 + L), (x0 + L, y0 + L), (x0 + L, y0 + L - L * 0.28),
                             (x0 + L * 0.28, y0 + L * 0.72), (x0 + L * 0.28, y0)], stroke=col, sw=1.3, closed=True, fill=B.PANEL))
    elif "u-channel" in nota or ("folded" in nota and "u" in nota):
        L = min(w, h) * 0.6
        x0, y0 = cx - L / 2, cy - L / 2
        s.append(B.polyline([(x0, y0), (x0, y0 + L), (x0 + L, y0 + L), (x0 + L, y0),
                             (x0 + L - L * 0.24, y0), (x0 + L - L * 0.24, y0 + L - L * 0.24),
                             (x0 + L * 0.24, y0 + L - L * 0.24), (x0 + L * 0.24, y0)], stroke=col, sw=1.3, closed=True, fill=B.PANEL))
    elif "l-profile" in nota:
        L = min(w, h) * 0.6
        x0, y0 = cx - L / 2, cy - L / 2
        s.append(B.polyline([(x0, y0), (x0, y0 + L), (x0 + L, y0 + L), (x0 + L, y0 + L - L * 0.24),
                             (x0 + L * 0.24, y0 + L - L * 0.24), (x0 + L * 0.24, y0)], stroke=col, sw=1.3, closed=True, fill=B.PANEL))
    elif "mesh" in nota:
        gw = w * 0.62
        x0, y0 = cx - gw / 2, cy - gw / 2
        s.append(B.rect(x0, y0, gw, gw, fill=B.PANEL, stroke=col, sw=1.2))
        for i in range(1, 4):
            s.append(B.line(x0 + gw * i / 4, y0, x0 + gw * i / 4, y0 + gw, stroke=B.INK_SOFT, sw=0.7))
            s.append(B.line(x0, y0 + gw * i / 4, x0 + gw, y0 + gw * i / 4, stroke=B.INK_SOFT, sw=0.7))
    elif "drilled plate" in nota or "hole pattern" in nota or "peg" in nota or "hole grid" in nota:
        pw, ph = w * 0.7, h * 0.4
        x0, y0 = cx - pw / 2, cy - ph / 2
        s.append(B.rect(x0, y0, pw, ph, fill=B.PANEL, stroke=col, sw=1.2))
        for i in range(3):
            hx = x0 + pw * (i + 1) / 4
            s.append(B.circle(hx, cy, 2.6, stroke=B.STEEL, sw=1, dash="2,1.5"))
    elif "threaded" in nota:
        s.append(bar())
        bw = w * 0.7
        for i in range(6):
            hx = cx - bw / 2 + bw * i / 6 + 3
            s.append(B.line(hx, cy - h * 0.15, hx + 6, cy + h * 0.15, stroke=B.INK_SOFT, sw=0.8))
    elif "round rod" in nota or "round tube" in nota or "round bar" in nota:
        s.append(bar())
        s.append(B.circle(cx + w * 0.28, cy, h * 0.16, stroke=col, sw=1.1, fill=B.WHITE))
        if "bent" in nota or "hook" in nota:
            s.append(B.polyline([(cx - w * 0.3, cy + h * 0.16), (cx + w * 0.28, cy + h * 0.16),
                                (cx + w * 0.32, cy), (cx + w * 0.24, cy - h * 0.1)], stroke=col, sw=1.3))
    elif "sheet" in nota or "plate" in nota:
        s.append(B.rect(cx - w * 0.35, cy - h * 0.1, w * 0.7, h * 0.2, fill=B.PANEL, stroke=col, sw=1.2))
    elif "board" in nota or "plank" in nota or "wood" in nota:
        s.append(B.rect(cx - w * 0.35, cy - h * 0.22, w * 0.7, h * 0.44, fill="#F3ECE0", stroke=col, sw=1.2))
        for i in range(1, 3):
            s.append(B.line(cx - w * 0.35, cy - h * 0.22 + h * 0.44 * i / 3, cx + w * 0.35, cy - h * 0.22 + h * 0.44 * i / 3, stroke="#D8C9B0", sw=0.7))
    else:  # square tube (default) — bisel si mitred / cut at N deg
        bl = "mitred" in nota or "cut at" in nota or "deg" in nota
        s.append(bar(bevel_l=bl, bevel_r="mitred" in nota))
        # seccion cuadrada al extremo
        sq = h * 0.26
        s.append(B.rect(cx + w * 0.24, cy - sq / 2, sq, sq, stroke=col, sw=1.1, fill=B.WHITE))

    # etiqueta
    dim = f"{pieza['largo']}x{pieza['ancho']}"
    label = f"{pieza['ref']} x{pieza['cantidad']} · {dim}"
    s.append(B.t(cx, y + h + 12, label, size=8.5, fill=B.INK_SOFT, anchor="middle", font=B.MONO))
    return "\n".join(s)


# ===========================================================================
def render(plan):
    d = plan["dims"]
    s = [B.header("Technical Drawing & Cut List", plan)]

    # --- zona de dibujo ---
    draw_top, draw_h = 96, 372
    box_x, box_w = B.MARGIN, B.PAGE_W - 2 * B.MARGIN
    s.append(B.rect(box_x, draw_top, box_w, draw_h, fill=B.WHITE, stroke=B.LINE, sw=1, rx=3))

    F, Sd = vistas(plan)
    real_max = max(F.get("w_mm", 1), F.get("h_mm", 1), Sd.get("w_mm", 1), Sd.get("h_mm", 1))
    X, ppm = escala(real_max, draw_h - 70)

    half = box_w / 2
    s.append(draw_view(box_x, draw_top, half, draw_h, F, ppm))
    s.append(draw_view(box_x + half, draw_top, half, draw_h, Sd, ppm))
    s.append(B.line(box_x + half, draw_top + 14, box_x + half, draw_top + draw_h - 14, stroke=B.LINE))

    # etiqueta de escala
    s.append(B.rect(box_x + box_w - 118, draw_top + 8, 110, 22, fill=B.PANEL, stroke=B.LINE, sw=1, rx=3))
    s.append(B.t(box_x + box_w - 108, draw_top + 23, f"SCALE  1:{X}", size=11, weight="bold", fill=B.ORANGE_DK, font=B.MONO))
    s.append(B.t(box_x + 10, draw_top + 23, "All dimensions in mm", size=9, fill=B.INK_FAINT, font=B.MONO))

    # --- detalle ampliado (inset) ---
    det = plan["detalle_ampliado"]
    ins_w, ins_h = 190, 96
    ins_x, ins_y = box_x + box_w - ins_w - 8, draw_top + draw_h - ins_h - 8
    s.append(B.rect(ins_x, ins_y, ins_w, ins_h, fill="#FFFDFA", stroke=B.ORANGE, sw=1, rx=3))
    s.append(B.t(ins_x + 10, ins_y + 16, "DETAIL", size=8.5, weight="bold", fill=B.ORANGE_DK, font=B.MONO, spacing="0.8"))
    s.append(B.t(ins_x + 10, ins_y + 31, det["titulo"], size=10, weight="bold", fill=B.CARBON))
    yy = ins_y + 45
    for ln in B.wrap(det["desc"], 32)[:4]:
        s.append(B.t(ins_x + 10, yy, ln, size=8.7, fill=B.INK_SOFT))
        yy += 12

    # --- CUT LIST ---
    ct_top = draw_top + draw_h + 20
    s.append(B.section_title(box_x, ct_top, "Cut list"))
    s.append(B.t(B.PAGE_W - B.MARGIN, ct_top, " | ".join(plan["cut_list_barras"]),
                 size=9, fill=B.STEEL, anchor="end", font=B.MONO))
    ty = ct_top + 16
    cols = [(box_x + 4, "REF"), (box_x + 42, "PART"), (box_x + 250, "QTY"),
            (box_x + 300, "SIZE (mm)"), (box_x + 410, "PROFILE / NOTE")]
    s.append(B.rect(box_x, ty, box_w, 18, fill=B.PANEL, stroke="none", rx=2))
    for cxp, lab in cols:
        s.append(B.t(cxp, ty + 13, lab, size=8.5, weight="bold", fill=B.INK_FAINT, font=B.MONO, spacing="0.5"))
    ry = ty + 18
    for pz in plan["piezas"]:
        s.append(B.t(cols[0][0], ry + 13, pz["ref"], size=10, weight="bold", fill=B.ORANGE_DK, font=B.MONO))
        s.append(B.t(cols[1][0], ry + 13, pz["nombre"], size=10, fill=B.CARBON))
        s.append(B.t(cols[2][0], ry + 13, f"x{pz['cantidad']}", size=10, fill=B.CARBON, font=B.MONO))
        s.append(B.t(cols[3][0], ry + 13, f"{pz['largo']} x {pz['ancho']}", size=10, fill=B.CARBON, font=B.MONO))
        note = B.wrap(pz["perfil"] + " · " + pz["nota"], 44)[0]
        s.append(B.t(cols[4][0], ry + 13, note, size=8.8, fill=B.INK_SOFT))
        s.append(B.line(box_x, ry + 19, box_x + box_w, ry + 19, stroke=B.LINE, sw=0.7))
        ry += 20

    # --- banda inferior: TRUE SHAPES (izq) + KEY POSITIONS (der) ---
    band_top = max(ry + 18, 740)
    band_top = min(band_top, 748)
    colb = box_x + box_w * 0.52

    # TRUE SHAPES
    s.append(B.section_title(box_x, band_top, "Parts as cut · true shapes"))
    piezas = plan["piezas"][:8]
    icols = 4
    icw, ich = (box_w * 0.52 - 10) / icols, 74
    for i, pz in enumerate(piezas):
        r, c = divmod(i, icols)
        ix = box_x + c * icw
        iy = band_top + 16 + r * (ich + 8)
        s.append(true_shape_icon(ix + 6, iy, icw - 12, ich - 22, pz))

    # KEY POSITIONS & ANGLES
    s.append(B.section_title(colb, band_top, "Key positions & angles"))
    ky = band_top + 20
    s.append(B.t(colb, ky, "POSITIONS", size=8.5, weight="bold", fill=B.STEEL, font=B.MONO, spacing="0.6"))
    ky += 15
    for pos in plan["posiciones_clave"]:
        for j, ln in enumerate(B.wrap(pos, 46)):
            if j == 0:
                s.append(f'<circle cx="{colb+3:.1f}" cy="{ky-3.5:.1f}" r="1.7" fill="{B.ORANGE}"/>')
            s.append(B.t(colb + 12, ky, ln, size=9.2, fill=B.CARBON if j == 0 else B.INK_SOFT))
            ky += 13
        ky += 2
    ky += 6
    s.append(B.t(colb, ky, "ANGLES", size=8.5, weight="bold", fill=B.STEEL, font=B.MONO, spacing="0.6"))
    ky += 15
    for a in plan["angulos"]:
        for j, ln in enumerate(B.wrap(a, 46)):
            if j == 0:
                s.append(f'<rect x="{colb:.1f}" y="{ky-8:.1f}" width="6" height="6" fill="{B.STEEL}"/>')
            s.append(B.t(colb + 12, ky, ln, size=9.2, fill=B.CARBON if j == 0 else B.INK_SOFT))
            ky += 13
        ky += 2

    s.append(B.footer(plan, 3))
    return B.document("\n".join(s))
