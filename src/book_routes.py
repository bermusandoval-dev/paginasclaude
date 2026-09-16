# -*- coding: utf-8 -*-
"""Order bump 01 -- The Combined Routes: which pages, in which order.

A book module names the book and lists its pages. Everything that turns that
list into paper -- the geometry, the fitter, the renderer, the checkers --
lives elsewhere and is shared, so a second book is a second list, not a second
pipeline.
"""
TITLE = "The Combined Routes"
NAME = "Session-Arc-The-Combined-Routes"
SLUG = "routes"
SUBJECT = "Session Arc - companion 01"


import content_front as C  # noqa: E402
import content_routes as CR  # noqa: E402
import kit as K  # noqa: E402
import routes_text as T  # noqa: E402

P1, P2 = "Part One &middot; The method", "Part Two &middot; The Overlap Atlas"

PAGES = [
    ("hero", C.p_cover, None, None),
    ("std", C.p_fits, "Start here", "Where this book sits"),
    ("std", C.p_contents, "Start here", "Contents"),
    ("std", C.p_problem, "Start here", "One client, three arcs"),
    ("std", C.p_build, "Start here", "How a route is built"),
    ("hero", C.p_op1, None, None),
    ("std", C.p_choose, P1, "Choosing the route"),
    ("std", C.p_rules1, P1, "Rules one to four"),
    ("std", C.p_rules2, P1, "Rules five to seven"),
    ("std", C.p_override, P1, "The override"),
    ("std", C.p_modules, P1, "Shared skills"),
    ("std", C.p_cut, P1, "Cutting a repeat"),
    ("std", C.p_seams, P1, "Seams"),
    ("std", C.p_talk, P1, "The order conversation"),
    ("std", C.p_reading, P1, "Reading a route page"),
    ("std", C.p_stop, P1, "When it stops fitting"),
    ("hero", C.p_op2, None, None),
    ("std", C.p_atlas, P2, "The atlas"),
    ("std", C.p_atlas_read, P2, "Reading the atlas"),
    ("std", C.p_own, P2, "Building your own"),
    ("std", C.p_finder, P2, "Route finder"),
    ("hero", C.p_op3, None, None),
]
for _fn, _r in CR.pages():
    _fam = T.FAMILIES[_r["family"]][0]
    _side = "Explained" if _fn.__name__.startswith("ra") else "Running order"
    PAGES.append(("std", _fn, "Route %02d &middot; %s" % (_r["num"], _fam), _side))
PAGES += [
    ("work", C.p_sheet1, "Sheet 1", "Route builder"),
    ("work", C.p_sheet2, "Sheet 2", "Seam planner"),
    ("std", C.p_scope, "Scope", "Referral and sources"),
    ("hero", C.p_back, None, None),
]


XREF_PHRASES = {
    "p_override": "the first visible win",
    "p_rules1": "the layer ladder",
    "p_talk": "the order conversation",
    "p_stop": "stops fitting",
    "p_modules": "the fifteen shared skills",
    "ra05": "sleep + depression + anxiety",
    "p_reading": "reading a route page",
    "p_sheet2": "seam planner",
}
