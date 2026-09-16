# -*- coding: utf-8 -*-
"""The Higgsfield prompt for every photograph in The Progress Checkpoints.

Kept in the repo because the prompt is the only reproducible part of a
render: the job ids in jobs_cp.json point at images that cannot be
regenerated identically, so if one has to be remade this is what it was
asked for.

Two rules run through all of them and both were learned the hard way on the
first book. Generated lettering always comes out as garbled pseudo-text, so
nothing in frame may carry words -- handwriting and printed type are asked
for as faint grey strokes and rule-lines instead. And the saturated-colour
budget is about 2 per cent of the whole book, so the photographs have to be
neutral: warm oak, cream paper, soft greys, with at most one small muted
accent each.
"""

STYLE = ("Soft natural window daylight with gentle directional shadows. Pale warm "
         "oak desk surface, cream and off-white paper, muted neutral palette of "
         "warm greys and soft beige. Calm, premium, editorial therapeutic "
         "stationery photography, shallow depth of field, fine detail, "
         "no harsh contrast, no saturated colour. "
         "ABSOLUTELY NO letters, NO numbers, NO words, NO readable text anywhere: "
         "any writing is only faint indistinct grey pencil strokes and ruled lines "
         "suggesting handwriting from a distance.")

HANDS = ("Adult hands only, no face, natural skin, plain neutral long sleeve. ")

# slug -> (aspect ratio, subject)
SHOTS = {
    # ---- openers -----------------------------------------------------------
    "h0-cover": ("4:3",
        "Top-down flat lay. One sheet of cream paper carries a simple hand-drawn line "
        "graph in soft graphite: a horizontal baseline, and a line that steps clearly "
        "DOWNWARD from upper left to lower right in three stages. Three small circled "
        "dots sit on the line where it changes. A dark grey pencil rests beside the "
        "sheet, a pale ceramic mug and a linen notebook at the frame edge."),
    "h1-method": ("4:3",
        "Top-down flat lay. Four identical small cream index cards laid in a row across "
        "the oak desk, evenly spaced, each ruled with three faint grey lines. A pencil "
        "lies diagonally across the gap between the second and third card. One small "
        "muted terracotta paperclip on the first card."),
    "h2-arcs": ("4:3",
        "Top-down flat lay. Fifteen slim cream file cards fanned in three neat rows "
        "across the desk like a card index, each with a faint grey ruled header band. "
        "Soft shadow across the lower third. One card lifted slightly proud of the rest."),
    "h3-sheets": ("4:3",
        "Top-down flat lay. A blank cream worksheet on a wooden clipboard, ruled with a "
        "faint grey grid and an empty plotting area, a sharpened pencil and a soft "
        "eraser beside it, a single dried stem laid along the top edge."),
    "h9-back": ("4:3",
        "Top-down flat lay. A closed linen-bound folder on the oak desk, a pencil and a "
        "pale ceramic cup beside it, low warm late-afternoon light raking across from "
        "the left, most of the frame quiet empty wood."),

    # ---- the problem, the anatomy, the three outlets ------------------------
    "c1-months": ("3:2",
        "Top-down. An open paper desk diary showing many small ruled week boxes across "
        "two pages, most boxes marked only with faint grey pencil ticks, no legible "
        "writing. A pencil rests in the gutter. The impression is of months passing "
        "with nothing recorded that says whether anything improved."),
    "c2-anatomy": ("3:2",
        "Top-down close-up of a single cream index card on oak, ruled into four faint "
        "grey zones of different heights, a pencil laid along its right edge, a small "
        "muted terracotta dot in the top corner. Clean, diagrammatic, generous space "
        "around the card."),
    "c3-three": ("3:2",
        "Top-down. Three cream folders spread on the oak desk so they fan out from a "
        "single point at the bottom of the frame into three separate directions. The "
        "left folder is closed, the middle one slightly open, the right one turned "
        "away. One small muted terracotta tab on the right folder."),

    # ---- reading the number ------------------------------------------------
    "k1-ontrack": ("4:3",
        "Top-down close-up of a sheet of cream graph paper with a faint grey grid. A "
        "single pencil line plotted across it descends steadily from upper left to "
        "lower right through four dotted points. Pencil resting at the lower right end "
        "of the line."),
    "k2-stalled": ("4:3",
        "Top-down close-up of a sheet of cream graph paper with a faint grey grid. A "
        "single pencil line plotted across it runs almost perfectly FLAT and level from "
        "left to right through four dotted points, with only tiny wobbles. A pencil "
        "rests beside it and an eraser sits at the right edge."),
    "k3-worse": ("4:3",
        "Top-down close-up of a sheet of cream graph paper with a faint grey grid. A "
        "single pencil line plotted across it climbs clearly UPWARD from lower left to "
        "upper right through four dotted points. A small muted terracotta circle is "
        "drawn around the highest final point."),
    "m1-choose": ("3:2",
        "Top-down. Two paper forms lying side by side on oak: the left one long, ruled "
        "with many faint grey question rows and small empty response boxes; the right "
        "one a single small cream card with one ruled line and a long empty scale bar "
        "printed across it. A pencil lies between them, not yet touching either."),
    "l1-licence": ("3:2",
        "Top-down. A neat stack of four or five loose paper forms slightly offset from "
        "one another on the oak desk, each ruled with faint grey lines, the top one "
        "carrying a small muted terracotta stamp mark in the corner. Quiet, archival, "
        "orderly."),
    "q1-phq": ("2:3",
        "Three-quarter view of a wooden clipboard on oak holding a single-page paper "
        "form: a faint grey ruled header band, then nine evenly spaced question rows "
        "each with four small empty tick boxes to the right. A dark pencil lies across "
        "the lower half of the sheet."),
    "q2-gad": ("2:3",
        "Three-quarter view of a wooden clipboard on oak holding a short paper form: a "
        "faint grey ruled header band, then seven evenly spaced question rows each with "
        "four small empty tick boxes to the right. Noticeably shorter than a full page, "
        "with clear cream space below the last row."),

    # ---- running the checkpoint: the five-step sequence --------------------
    "r1-hand": ("4:3", HANDS +
        "Top-down. One hand slides a single small cream card with a long empty scale "
        "bar across the oak desk toward the far side of frame, offering it."),
    "r2-mark": ("4:3", HANDS +
        "Top-down close-up. A hand holding a pencil makes one small mark on the empty "
        "scale bar of the cream card, roughly two thirds along its length."),
    "r3-plot": ("4:3", HANDS +
        "Top-down close-up. A hand plots a single dot onto a sheet of cream graph paper "
        "that already carries three earlier dots joined by a descending pencil line."),
    "r4-compare": ("4:3", HANDS +
        "Top-down. Two hands hold the graph sheet flat while the small scale card lies "
        "beside it, the two sheets clearly being read against one another."),
    "r5-decide": ("4:3", HANDS +
        "Top-down. A hand rests a pencil on one of three cream cards fanned on the desk, "
        "having chosen the middle one. The other two cards sit untouched."),

    # ---- the conversation ---------------------------------------------------
    "t1-script": ("3:2",
        "Wide, from behind and to one side, softly out of focus: two people seated "
        "facing each other in a calm neutral consulting room with a low table between "
        "them holding a single cream sheet and a pencil. Warm daylight from a window to "
        "the left. No faces readable, no text, muted oatmeal and soft grey upholstery."),
    "t2-words": ("3:2",
        "Two empty armchairs in a calm neutral consulting room, angled slightly toward "
        "each other, a small side table between them with one cream sheet of paper and a "
        "pencil on it. Soft window daylight, muted oatmeal fabric, a single plant out of "
        "focus at the edge."),
    "n1-note": ("3:2", HANDS +
        "Top-down. A hand writes on a small ruled notepad beside a closed laptop, the "
        "graph sheet visible at the top edge of frame. Only faint grey pencil strokes, "
        "no legible words. Quiet end-of-day desk light."),
    "b1-stop": ("3:2",
        "Top-down. A cream sheet on the oak desk is turned face down, and a second, "
        "smaller card with a single muted terracotta edge stripe is laid squarely on top "
        "of it. A pencil is set down to one side, clearly put aside rather than in use."),

    # ---- charting -----------------------------------------------------------
    "p1-chart": ("3:2", HANDS +
        "Top-down close-up of a hand drawing a short vertical tick onto the baseline of "
        "a cream graph sheet, marking a new column, three plotted dots already present "
        "to the left."),
    "p2-lies": ("3:2",
        "Top-down close-up of a cream graph sheet where the plotted pencil line runs "
        "low and steady but has one single sharp spike shooting up and straight back "
        "down at one point. A small muted terracotta question mark shape, drawn as a "
        "simple curved pencil stroke, sits beside the spike."),
    "s1-short": ("3:2",
        "Top-down. A short strip of cream card on the oak desk carries just three small "
        "circled pencil dots: one at the far left, one in the middle, one at the far "
        "right, joined by a light ruled line. Plenty of empty card around them."),
    "x1-reading": ("2:3",
        "Three-quarter view of an open printed booklet lying flat on the oak desk, its "
        "two visible pages laid out as faint grey blocks, rule-lines and an empty "
        "plotting grid, no readable text. A pencil rests in the gutter between pages."),

    # ---- the fifteen arcs ---------------------------------------------------
    "a-int": ("16:9",
        "Top-down. A single fresh cream sheet, entirely blank except for one faint grey "
        "ruled line near the top, a sharpened pencil laid beside it, morning light. The "
        "beginning of a record."),
    "a-emo": ("16:9",
        "Top-down. A cream card on oak beside a shallow ceramic bowl of water catching "
        "the window light, a few concentric ripples still moving across it."),
    "a-anx": ("16:9",
        "Top-down. A small wooden step-ladder toy or a set of five ascending wooden "
        "blocks arranged as a rising staircase on the oak desk, a cream card beside "
        "them."),
    "a-dep": ("16:9",
        "Top-down. A cream weekly planner card ruled into seven faint grey columns, with "
        "small pencil ticks appearing in only two of them, a pencil resting across it."),
    "a-str": ("16:9",
        "Top-down. A stack of paper trays or folders piled high on one side of the oak "
        "desk and a completely clear space on the other, the boundary between them "
        "sharp."),
    "a-sw": ("16:9",
        "Top-down. A small round mirror lying face up on the oak desk reflecting only "
        "soft ceiling light and a corner of cream paper, a pencil beside it."),
    "a-rel": ("16:9",
        "Top-down. Two cream cards on the oak desk, overlapping slightly at one corner, "
        "a single pencil line drawn on the desk paper between them."),
    "a-tra": ("16:9",
        "Top-down. A folded soft wool blanket in muted oatmeal on the corner of the oak "
        "desk with a cream card and a smooth grounding stone resting on top of it."),
    "a-grf": ("16:9",
        "Top-down. A single dried flower stem laid diagonally across a cream sheet on "
        "the oak desk, one pressed petal fallen beside it, very soft light."),
    "a-cmp": ("16:9",
        "Top-down. A loop of fine cord laid on the oak desk in a closed circle with one "
        "end pulled clear of the loop, a cream card beneath."),
    "a-val": ("16:9",
        "Top-down. A small brass compass lying on a cream sheet on the oak desk, its "
        "face catching the light, no readable markings."),
    "a-ang": ("16:9",
        "Top-down. A struck match, already extinguished, resting on a small ceramic dish "
        "beside a cream card on the oak desk, a thin wisp of smoke still rising."),
    "a-slp": ("16:9",
        "Top-down. A cream sleep-diary card ruled into a faint grey grid of seven narrow "
        "columns, a small brass alarm clock face-down beside it, early blue-grey dawn "
        "light."),
    "a-wrk": ("16:9",
        "Top-down. A closed laptop on the oak desk with a single cream card resting on "
        "its lid and a pencil across the card, end of the working day light."),
    "a-prg": ("16:9",
        "Top-down. A neat closed stack of many cream cards bound with a simple cotton "
        "tie on the oak desk, one card slipped out and laid on top, late warm light."),

    # ---- the worksheets -----------------------------------------------------
    "w1-sheet": ("2:3",
        "Three-quarter view of a blank cream chart sheet on a wooden clipboard: an empty "
        "faint grey plotting grid filling most of the page with a ruled header band "
        "above it, a sharpened pencil resting on the clip."),
    "w2-goal": ("2:3",
        "Three-quarter view of a blank cream worksheet on oak ruled with a few widely "
        "spaced faint grey lines and one long empty horizontal scale bar across the "
        "lower third, a pencil and eraser beside it."),
    "w3-caseload": ("2:3",
        "Three-quarter view of a blank cream grid sheet on oak ruled into many small "
        "empty boxes in rows and columns, like a class register, a pencil laid across "
        "the top right corner."),
}


def prompt(slug):
    _ar, subject = SHOTS[slug]
    return subject + " " + STYLE


def aspect(slug):
    return SHOTS[slug][0]
