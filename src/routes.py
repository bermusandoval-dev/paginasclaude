# -*- coding: utf-8 -*-
"""The seven ordering rules and the route builder.

A route is computed, never typed: order the arcs by layer, walk their sessions,
keep a shared module only the first time it appears, keep only the last arc's
ending, and mark the seams. Every figure on a route page is drawn from the
object this file returns, and check_figs.py re-derives the numbers.
"""
import arcs as A

RULES = [
    {"n": 1, "key": "R1", "name": "Stabilize before you explore",
     "short": "Stabilize first",
     "body": "When emotions flood or safety is shaky, nothing else can be learned yet. "
             "Emotion Regulation and Trauma Groundwork lead any route they are part of.",
     "arcs": ["EMO", "TRA"]},
    {"n": 2, "key": "R2", "name": "Body and load before mind",
     "short": "Body and load",
     "body": "A brain that is not sleeping, or a week with no room in it, cannot do cognitive "
             "work well. Sleep and Stress &amp; Burnout come before the thinking arcs.",
     "arcs": ["SLP", "STR"]},
    {"n": 3, "key": "R3", "name": "The loss before what it set off",
     "short": "Loss first",
     "body": "When a loss started the other problems, work on the loss first. Treating the "
             "low mood that grief caused, without the grief, reads to the client as being "
             "asked to move on.",
     "arcs": ["GRF"]},
    {"n": 4, "key": "R4", "name": "Energy before approach",
     "short": "Energy first",
     "body": "Facing a fear or resisting an urge takes effort. If low mood has drained the "
             "tank, get the days moving before asking the client to climb a ladder.",
     "arcs": ["DEP"]},
    {"n": 5, "key": "R5", "name": "Self before others",
     "short": "Self first",
     "body": "A person who is at war with themselves, or whose temper speaks first, brings that "
             "into every relationship. Self-Worth and Anger come before Relationships.",
     "arcs": ["SW", "ANG"]},
    {"n": 6, "key": "R6", "name": "Direction comes last",
     "short": "Direction last",
     "body": "Values and work questions are easier to answer from solid ground, and they give "
             "the route its reason to continue after therapy. Values &amp; Meaning and Work "
             "&amp; Money close a route.",
     "arcs": ["VAL", "WRK"]},
    {"n": 7, "key": "R7", "name": "Teach once, end once",
     "short": "Teach once",
     "body": "A skill is taught the first time it appears and reviewed after that. Only the last "
             "arc keeps its ending. When two arcs sit on the same layer, the one that teaches the "
             "shared skill in more depth goes first.",
     "arcs": []},
]
RULE = {r["key"]: r for r in RULES}

# Position on the ladder. Lower goes first. Ties inside a rule are broken by R7:
# the arc that lends the shared skill goes first (Emotion Regulation lends
# grounding to Trauma Groundwork, Sleep lends wind-down to Stress, Anxiety lends
# the ladder to Habits, Values lends the compass to Work).
LAYER = {"EMO": 1.0, "TRA": 1.5, "SLP": 2.0, "STR": 2.5, "GRF": 3.0, "DEP": 4.0,
         "ANX": 5.0, "CMP": 5.5, "SW": 6.0, "ANG": 6.5, "REL": 7.0, "VAL": 8.0, "WRK": 8.5}
RULE_OF = {"EMO": "R1", "TRA": "R1", "SLP": "R2", "STR": "R2", "GRF": "R3", "DEP": "R4",
           "ANX": None, "CMP": None, "SW": "R5", "ANG": "R5", "REL": None,
           "VAL": "R6", "WRK": "R6"}
LADDER_ROWS = [  # (label, arcs) drawn on the layer ladder, top to bottom
    ("Stabilize", ["EMO", "TRA"]),
    ("Body and load", ["SLP", "STR"]),
    ("Loss", ["GRF"]),
    ("Energy", ["DEP"]),
    ("Approach", ["ANX", "CMP"]),
    ("Self", ["SW", "ANG"]),
    ("Others", ["REL"]),
    ("Direction", ["VAL", "WRK"]),
]


def why_first(a, b):
    """The rule that puts arc a before arc b."""
    ra, rb = RULE_OF[a], RULE_OF[b]
    if ra and ra == rb:
        return "R7"
    if rb == "R6":
        return "R6"
    if ra and ra != "R6":
        return ra
    if a in ("ANX", "CMP") and b in ("ANX", "CMP"):
        return "R7"
    return rb or "R7"


def order(keys):
    return sorted(keys, key=lambda k: LAYER[k])


def build(keys):
    seq = order(keys)
    taught = {}
    items = []
    pending_review = {}  # arc -> list of session numbers whose review folds into its next kept session
    for idx, k in enumerate(seq):
        last = idx == len(seq) - 1
        for n, t, m in A.sessions(k):
            it = {"n": n, "title": t, "module": m, "arc": k, "status": "keep", "ref": None,
                  "reviews": []}
            if m == "CLOSE" and not last:
                it["status"] = "close"
            elif m and m != "CLOSE" and m in taught:
                it["status"] = "repeat"
                it["ref"] = taught[m]
                pending_review.setdefault(k, []).append(taught[m])
            else:
                if m and m != "CLOSE":
                    taught[m] = n
                if pending_review.get(k):
                    it["reviews"] = pending_review.pop(k)
            items.append(it)
    kept = [i for i in items if i["status"] == "keep"]
    seams = []
    for a, b in zip(seq, seq[1:]):
        la = [i for i in kept if i["arc"] == a][-1]
        fb = [i for i in kept if i["arc"] == b][0]
        week = kept.index(fb) + 1
        seams.append({"from": a, "to": b, "last": la, "first": fb, "week": week,
                      "rule": why_first(a, b)})
    by_arc = {k: {"total": len(A.sessions(k)),
                  "kept": sum(1 for i in kept if i["arc"] == k),
                  "repeat": sum(1 for i in items if i["arc"] == k and i["status"] == "repeat"),
                  "close": sum(1 for i in items if i["arc"] == k and i["status"] == "close")}
              for k in seq}
    return {"order": seq, "items": items, "kept": kept, "seams": seams, "by_arc": by_arc,
            "total": sum(len(A.sessions(k)) for k in seq), "length": len(kept),
            "repeats": sum(v["repeat"] for v in by_arc.values()),
            "closes": sum(v["close"] for v in by_arc.values())}


WORK = {"EMO": "the work on strong feelings", "ANX": "the work on the anxiety", "DEP": "the work on low mood",
        "STR": "the work on the load", "SW": "the work on the inner critic", "REL": "the work on relationships",
        "TRA": "the groundwork for safety", "GRF": "the work on the loss", "CMP": "the work on the habit",
        "VAL": "the work on direction", "ANG": "the work on anger", "SLP": "the work on sleep",
        "WRK": "the work on work and money"}


def bridge(seam):
    a, b = A.BY_KEY[seam["from"]], A.BY_KEY[seam["to"]]
    return ("You now have %s. That is what the next part asks for: %s. Next week, in S%03d, we begin %s."
            % (a["builds"], b["needs"], seam["first"]["n"], WORK[seam["to"]]))


if __name__ == "__main__":
    for keys in (["ANX", "DEP"], ["DEP", "SLP", "ANX"], ["REL", "ANG", "EMO"]):
        r = build(keys)
        print(r["order"], r["total"], "->", r["length"], "repeats", r["repeats"], "closes", r["closes"])
        for s in r["seams"]:
            print("   seam week", s["week"], s["rule"], bridge(s))
