# -*- coding: utf-8 -*-
"""Order bump 02 -- The Progress Checkpoints: which pages, in which order.

Part Two is generated rather than listed: content_arcs.pages() yields both
pages of every arc in registry order, so an arc cannot be left out of the
book by forgetting a line here.
"""
TITLE = "The Progress Checkpoints"
NAME = "Session-Arc-The-Progress-Checkpoints"
SLUG = "checkpoints"
SUBJECT = "Session Arc - companion 02"

import content_arcs as CA  # noqa: E402
import content_cp as C  # noqa: E402

P1 = "Part One &middot; Reading the number"
P3 = "Part Three &middot; Sheets"

PAGES = [
    ("hero", C.p_cover, None, None),
    ("std", C.p_fits, "Start here", "What this book answers"),
    ("std", C.p_contents, "Start here", "Contents"),
    ("std", C.p_problem, "Start here", "Four months in"),
    ("std", C.p_anatomy, "Start here", "What a checkpoint is"),
    ("hero", C.p_op1, None, None),
    ("std", C.p_three, P1, "One reading, three ways out"),
    ("std", C.p_ontrack, P1, "On track"),
    ("std", C.p_stalled, P1, "Stalled"),
    ("std", C.p_worse, P1, "Worse"),
    ("std", C.p_choose, P1, "Choosing the measure"),
    ("std", C.p_goal, P1, "Writing a goal scale"),
    ("std", C.p_licence, P1, "What you may reproduce"),
    ("std", C.p_phq, P1, "The PHQ-9"),
    ("std", C.p_gad, P1, "The GAD-7"),
    ("std", C.p_run, P1, "Running a checkpoint"),
    ("std", C.p_script, P1, "The review script"),
    ("std", C.p_words, P1, "When it is not good news"),
    ("std", C.p_chart, P1, "Plotting it"),
    ("std", C.p_lies, P1, "Charts that mislead"),
    ("std", C.p_short, P1, "Short courses"),
    ("std", C.p_note, P1, "The checkpoint and the note"),
    ("std", C.p_stop, P1, "When not to measure"),
    ("std", C.p_reading, P1, "Reading an arc spread"),
    ("hero", C.p_op2, None, None),
]
for _fn, _a in CA.pages():
    _side = "The schedule" if _fn.__name__.startswith("ca") else "One worked case"
    PAGES.append(("std", _fn, "Arc %d &middot; %s" % (CA.NUM[_a["key"]], _a["short"]), _side))
PAGES += [
    ("hero", C.p_op3, None, None),
    ("work", C.p_sheet1, "Sheet 1", "The chart sheet"),
    ("work", C.p_sheet2, "Sheet 2", "The goal-scale sheet"),
    ("work", C.p_sheet3, "Sheet 3", "The caseload sheet"),
    ("std", C.p_scope, "Scope", "Referral and sources"),
    ("hero", C.p_back, None, None),
]

# check_pdf verifies each "page NN" lands on a page containing these words. Two
# rules follow from how it looks: it lowercases the page text, so every phrase
# here is lowercase; and an h3 is set as letter-spaced small caps that extracts
# as "I T H E L D, AT TA R G E T", so every phrase is body text, never a
# heading.
XREF_PHRASES = {
    "p_three": "three ways out",
    "p_ontrack": "target band",
    "p_worse": "in the wrong direction",
    "p_goal": "writing a goal scale",
    "p_licence": "what you may reproduce",
    "p_phq": "item 9",
    "p_sheet1": "the first column is the baseline",
    "p_choose": "three questions, in this order",
    "p_words": "doing real work",
    "p_gad": "four points is the figure",
    "p_sheet3": "one line per client",
    "p_fits": "screening and monitoring",
}
