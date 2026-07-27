# -*- coding: utf-8 -*-
"""
datos_metal.py — Configuracion maestra del catalogo MetalMaster (MM).

Contiene: familias, subcategorias, acabados, grits, herramientas base,
bloques de seguridad y escenas. NO contiene geometria (eso vive en
arquetipos.py). Todo en ingles porque es lo que va impreso en el PDF
(el comprador es anglo); los comentarios en espanol son para nosotros.

REGLA DE ORO: nada de texto que se imprime cambia por reordenar este
archivo. Las elecciones "aleatorias" siempre se hacen con RNG sembrado
por proyecto/subcategoria (ver catalogo.py), nunca con random global.
"""

MARCA = "MetalMaster"
PROYECTO_SEED = "MM1200"          # cambia esto y NUNCA cambies planos entregados
TOTAL_OBJETIVO = 1200             # 8 familias x 150
SUBCATS_POR_FAMILIA = 15          # 15 subcats x ~10 planos = 150
PLANOS_POR_SUBCAT = 10

# ---------------------------------------------------------------------------
# ACABADOS  (cada acabado arrastra su herramienta y su consumible: asi dos
# "gemelos" con acabado distinto tienen listas de herramientas/herrajes
# distintas por construccion -> el auditor de similitud pasa limpio).
# ---------------------------------------------------------------------------
ACABADOS = [
    {"key": "primer_enamel",
     "label": "Anti-rust primer + gloss enamel topcoat",
     "tool": "Paint brush and mini foam roller",
     "consumable": "Anti-rust primer + enamel (2 coats)"},
    {"key": "powder",
     "label": "Electrostatic powder coating",
     "tool": "Powder coating gun",
     "consumable": "Polyester powder + oven cure"},
    {"key": "clear",
     "label": "Clear lacquer over brushed bare steel",
     "tool": "HVLP spray gun",
     "consumable": "Etch primer + clear lacquer"},
    {"key": "bluing",
     "label": "Cold bluing (gun-blue) + oil",
     "tool": "Applicator pads and gloves",
     "consumable": "Cold-blue solution + machine oil"},
    {"key": "hammered",
     "label": "Hammered-finish direct-to-metal enamel",
     "tool": "Foam roller",
     "consumable": "Hammered enamel (no primer)"},
    {"key": "galv_wax",
     "label": "Cold-galvanising zinc spray + paste wax",
     "tool": "Aerosol can + buffing cloth",
     "consumable": "Zinc-rich spray + clear paste wax"},
]

# Preparacion / lijado-desbaste (equivalente a "lijas" en madera).
DESBASTES = [
    "Flap disc 40 grit, then 80 to blend",
    "Flap disc 60 grit, then 120 to smooth",
    "Sanding disc 80 grit, wire-wheel to deburr",
    "Emery cloth 120 then 240 by hand",
    "Flap disc 80 grit, Scotch-Brite for a satin key",
    "Wire wheel to strip, then 180 emery",
]

# ---------------------------------------------------------------------------
# HERRAMIENTAS  (uso especifico entre parentesis, como en madera).
# ---------------------------------------------------------------------------
HERRAMIENTAS_BASE = [
    {"item": "Angle grinder + cutting and flap discs", "uso": "cut tube to length and deburr every edge"},
    {"item": "Cordless drill + HSS bits", "uso": "drill the bolt and hook holes"},
    {"item": "Combination square", "uso": "mark square ends and check 90 corners"},
    {"item": "Two 150 mm F-clamps", "uso": "hold parts while you fix them"},
    {"item": "Tape measure + fine marker", "uso": "lay out every length from the cut list"},
    {"item": "Centre punch", "uso": "dimple each hole so the bit does not wander"},
    {"item": "Flat file", "uso": "clean burrs off cut ends before assembly"},
]
HERRAMIENTAS_SOLDADURA = [
    {"item": "MIG welder (0.8 mm wire)", "uso": "weld the frame joints"},
    {"item": "Two magnetic welding squares", "uso": "hold parts at a true 90 while tacking"},
    {"item": "Angle grinder wire cup", "uso": "clean paint and mill scale off weld zones"},
]
HERRAMIENTAS_ATORNILLADO = [
    {"item": "M8 tap + tap wrench", "uso": "thread the captive-nut and bolt holes"},
    {"item": "8 mm socket + spanner", "uso": "tighten the button bolts evenly"},
    {"item": "Step drill 4-12 mm", "uso": "open clean bolt clearance holes"},
]
HERRAMIENTAS_CHAPA = [
    {"item": "Bench folder / folding bars", "uso": "bend the sheet panels to the marked lines"},
    {"item": "Aviation tin snips", "uso": "trim the sheet blanks to size"},
]
HERRAMIENTA_REMACHE = {"item": "Lever rivet gun", "uso": "set the 4.8 mm rivets"}

# ---------------------------------------------------------------------------
# SEGURIDAD  (bloque NUEVO respecto a madera: una linea por peligro real).
# ---------------------------------------------------------------------------
SEG_BASE = [
    "Wrap-around safety glasses whenever the grinder or drill is running.",
    "Cut-resistant work gloves for handling raw cut edges.",
    "Ear protection while grinding or cutting.",
    "Full face shield when grinding or cutting off discs.",
]
SEG_SOLDADURA = [
    "Auto-darkening welding helmet, shade 10-11, for every arc.",
    "Leather welding gloves and a flame-resistant long-sleeve.",
    "Weld only in a ventilated bay, clear of anything flammable.",
]
SEG_CHAPA = [
    "Keep fingers clear of the folder pinch line.",
]

# ---------------------------------------------------------------------------
# MATERIALES BASE (perfiles reales). El cut list optimiza barras de 6 m.
# ---------------------------------------------------------------------------
LARGO_BARRA_MM = 6000
KERF_WASTE = 1.05  # 5% de merma/kerf al calcular barras

# ---------------------------------------------------------------------------
# FAMILIAS. Cada familia: clave, nombre EN, arquetipo (geometria en
# arquetipos.py), rango de IDs y 15 subcategorias tematicas + escenas.
# Los IDs son MM-0001..MM-1200 (4 digitos por el total de 1200).
# ---------------------------------------------------------------------------
FAMILIAS = [
    {
        "key": "banco",
        "nombre": "Workbenches & Work Tables",
        "arquetipo": "banco",
        "id_ini": 1, "id_fin": 150,
        "subcats": [
            "Heavy-duty workbench", "Folding utility bench",
            "Compact garage bench", "Starter home bench",
            "Mobile assembly table", "Fabrication work table",
            "Mechanic's bench", "Fold-down wall bench",
            "Kids' maker bench", "Two-station shared bench",
            "Slim balcony bench", "Butcher-block-top bench",
            "Outfeed / packing table", "Tall standing work table",
            "Corner L-shaped bench",
        ],
        "escenas": [
            "in a bright home garage next to a pegboard wall",
            "in a clean two-car garage on a painted concrete floor",
            "in a tidy hobby workshop with daylight from a side window",
            "in a maker space against a plain white wall",
            "in a home garage beside a rolling tool chest",
        ],
    },
    {
        "key": "estanteria",
        "nombre": "Industrial Shelving & Racks",
        "arquetipo": "estanteria",
        "id_ini": 151, "id_fin": 300,
        "subcats": [
            "Garage storage shelving", "Warehouse-style rack",
            "Tall utility shelving", "Steel bookcase unit",
            "Ventilated storage rack", "Heavy tote rack",
            "Narrow pantry shelving", "Corner shelving tower",
            "Under-stairs shelving", "Tyre / wheel rack",
            "Paint & solvent shelving", "Deep tote rack",
            "Open-back display shelving", "Long-stock rack",
            "Wall-anchored garage shelf",
        ],
        "escenas": [
            "in a garage against a bare block wall",
            "in a utility room on a tiled floor",
            "in a basement storage area under soft light",
            "in a clean warehouse corner",
            "in a garage loaded with plain unlabelled boxes",
        ],
    },
    {
        "key": "rack_pared",
        "nombre": "Tool Racks & Wall Organizers",
        "arquetipo": "rack_pared",
        "id_ini": 301, "id_fin": 450,
        "subcats": [
            "Tool wall panel", "Wall storage rail",
            "Garden-tool wall rack", "Small-parts hook board",
            "Workshop peg wall", "Clamp storage rack",
            "Cordless-tool charging wall", "Spray-can shelf rack",
            "Bike-tool wall station", "Wrench & plier rack",
            "Hose & cable hanger", "Screwdriver rack",
            "Fishing-rod wall rack", "Broom & mop rack",
            "Sports-gear entry rack",
        ],
        "escenas": [
            "mounted on a plain garage wall",
            "on a white workshop wall in daylight",
            "on a grey concrete wall above a bench",
            "on a wall beside a closed door",
            "on a bright utility-room wall",
        ],
    },
    {
        "key": "carrito",
        "nombre": "Shop Carts & Trolleys",
        "arquetipo": "carrito",
        "id_ini": 451, "id_fin": 600,
        "subcats": [
            "Two-tier shop cart", "Three-tier trolley",
            "Welder's cart", "Ventilated rolling cart",
            "Service trolley", "Kitchen island cart",
            "Garden potting trolley", "Bar & drinks trolley",
            "Tool-box rolling stand", "Bench-tool cart",
            "Firewood carry trolley", "Laundry rolling cart",
            "Printer / office trolley", "Nursery plant trolley",
            "Heavy-duty parts cart",
        ],
        "escenas": [
            "in a home garage on a smooth floor",
            "in a bright kitchen against a plain wall",
            "in a workshop beside a workbench",
            "on a patio by a plain wall",
            "in a utility room in soft daylight",
        ],
    },
    {
        "key": "soporte",
        "nombre": "Stands & Holders",
        "arquetipo": "soporte",
        "id_ini": 601, "id_fin": 750,
        "subcats": [
            "Bike floor stand", "Ladder plant stand",
            "Firewood log rack", "Compact bike rack",
            "Tiered plant stand", "Vertical bike stand",
            "Log store frame", "Monitor / laptop riser",
            "Instrument stand", "Firewood holder",
            "Umbrella & boot stand", "Kayak / board rack",
            "Speaker floor stand", "Ladder storage stand",
            "Watering-can & hose stand",
        ],
        "escenas": [
            "on a patio against a plain fence",
            "in a bright hallway on a wood floor",
            "in a garden next to a plain wall",
            "in a living room corner in soft light",
            "on a covered porch by a blank wall",
        ],
    },
    {
        "key": "mesa_madera",
        "nombre": "Metal-Frame Tables (Wood Top)",
        "arquetipo": "mesa_madera",
        "id_ini": 751, "id_fin": 900,
        "subcats": [
            "Dining table", "Writing desk",
            "Console table", "Coffee table",
            "Bistro table", "Bedside table",
            "Study desk", "Bench seat",
            "Side table", "TV console",
            "Plant table", "Standing desk",
            "Picnic table", "Kitchen island top",
            "Entry console",
        ],
        "escenas": [
            "in a bright dining room on a wood floor",
            "in a modern living room against a white wall",
            "in a home office by a window",
            "in a Scandinavian-style room in soft daylight",
            "in a hallway against a plain painted wall",
        ],
    },
    {
        "key": "parrilla",
        "nombre": "BBQ, Grills & Fire Pits",
        "arquetipo": "parrilla",
        "id_ini": 901, "id_fin": 1050,
        "subcats": [
            "Charcoal grill", "Brick-style BBQ",
            "Portable firebox", "Square fire pit",
            "Tabletop hibachi grill", "Barrel-style grill",
            "Fire pit with grate", "Santa-maria grill",
            "Camp grill", "Deep fire pit bowl",
            "Chimney fire box", "Picnic grill",
            "Skewer grill", "Mini forge box",
            "Fire pit with tool hooks",
        ],
        "escenas": [
            "on a stone patio at golden hour with unlit charcoal",
            "in a back garden on a gravel bed, cold and unlit",
            "on a wooden deck against a plain fence, unlit",
            "on a patio beside a plain wall in daylight, unlit",
            "on a paved terrace, clean and unlit",
        ],
    },
    {
        "key": "perchero",
        "nombre": "Coat / Shoe Racks & Entry",
        "arquetipo": "perchero",
        "id_ini": 1051, "id_fin": 1200,
        "subcats": [
            "Coat stand", "Hall tree",
            "Coat rack with bench", "Tall coat rack",
            "Coat bar with shelf", "Free-standing shoe rack",
            "Entry bench with hooks", "Industrial coat tree",
            "Slim hallway rack", "Boot & umbrella rack",
            "Bag & scarf rack", "Shoe tower",
            "Mudroom hook rail", "Garment rack",
            "Compact coat rack",
        ],
        "escenas": [
            "in a bright entryway on a wood floor",
            "in a hallway against a plain painted wall",
            "in a mudroom by a plain door",
            "in a modern foyer in soft daylight",
            "against a clean white wall near a doormat",
        ],
    },
]


def familia_por_arquetipo(arq):
    for f in FAMILIAS:
        if f["arquetipo"] == arq:
            return f
    raise KeyError(arq)
