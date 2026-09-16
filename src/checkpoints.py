# -*- coding: utf-8 -*-
"""The arithmetic of The Progress Checkpoints.

Everything the book prints about a checkpoint -- where it falls in its arc, how
far apart they are, what counts as a move, what the worked case decided -- is
computed here from arcs.CHECKPOINT. No page states a number of its own.

The one deliberate simplification: every worked chart in the book plots the
0-10 goal scale, not the instrument. Every arc has a goal scale, only some have
an instrument, and a reader comparing fifteen charts should be comparing the
same axis on all of them.
"""
import arcs as A

# --- what may be reproduced, and what may only be named --------------------
# "free" means the instrument carries an explicit statement that it may be
# reproduced without permission, or is a work of the United States government
# and so in the public domain. Everything else is named and linked, never
# printed: a licence for research use is not a licence to sell inside a PDF.
MEASURE = {
    "PHQ-9": {
        "what": "Depression severity, nine items",
        "range": (0, 27), "step": 5, "dir": "down",
        "bands": [(0, 4, "none-minimal"), (5, 9, "mild"), (10, 14, "moderate"),
                  (15, 19, "moderately severe"), (20, 27, "severe")],
        "free": True,
        "licence": "Carries the statement &ldquo;no permission required to reproduce, "
                   "translate, display or distribute&rdquo;. Reproduced in full on page %s.",
        "source": "Kroenke, Spitzer &amp; Williams (2001), <i>Journal of General Internal "
                  "Medicine</i> 16(9), 606&ndash;613.",
        "risk": 9,
    },
    "GAD-7": {
        "what": "Generalized anxiety severity, seven items",
        "range": (0, 21), "step": 4, "dir": "down",
        "bands": [(0, 4, "minimal"), (5, 9, "mild"), (10, 14, "moderate"),
                  (15, 21, "severe")],
        "free": True,
        "licence": "Carries the same no-permission statement as the PHQ-9. "
                   "Reproduced in full on page %s.",
        "source": "Spitzer, Kroenke, Williams &amp; L&ouml;we (2006), <i>Archives of "
                  "Internal Medicine</i> 166(10), 1092&ndash;1097.",
        "risk": None,
    },
    "PCL-5": {
        "what": "PTSD symptom severity, twenty items",
        "range": (0, 80), "step": 10, "dir": "down",
        "bands": [(0, 30, "below the provisional cut-point"),
                  (31, 80, "at or above the provisional cut-point")],
        "free": True,
        "licence": "A work of the United States government and in the public domain. "
                   "Too long to set here: printed from the National Center for PTSD.",
        "source": "Weathers et al. (2013), National Center for PTSD, ptsd.va.gov.",
        "risk": None,
    },
    "Sleep diary": {
        "what": "Sleep efficiency: time asleep as a percentage of time in bed",
        "range": (0, 100), "step": 10, "dir": "up",
        "bands": [(0, 74, "low"), (75, 84, "approaching"), (85, 100, "at target")],
        "free": True,
        "licence": "Not an instrument and not anyone's property: it is the client's own "
                   "diary from S312, divided one number by another.",
        "source": "The 85 per cent target is the usual working figure in "
                  "cognitive behavioral treatment for insomnia.",
        "risk": None,
    },
    "Goal scale": {
        "what": "The arc's own 0-10 goal-attainment item",
        "range": (0, 10), "step": 2, "dir": "up",
        "bands": [(0, 3, "little"), (4, 6, "some"), (7, 10, "most")],
        "free": True,
        "licence": "Written for this book from the clinical goal of the sessions "
                   "either side of the checkpoint. Yours to copy, and to reword.",
        "source": "The two-point step is this book's working convention, not a "
                  "psychometric statistic. See page %s.",
        "risk": None,
    },
    "Treatment scale": {
        "what": "Whichever instrument ran through treatment, read one last time",
        "range": (0, 0), "step": 0, "dir": "down",
        "bands": [],
        "free": True,
        "licence": "Carries the licence of whichever instrument it is.",
        "source": "Its own. The point of the ending arc is that the last reading is "
                  "comparable with the first.",
        "risk": None,
    },
}

GOAL = MEASURE["Goal scale"]

# --- the three outlets ------------------------------------------------------
OUTLET = {
    "on": ("On track", "Stay on the arc. Say the number out loud and move on."),
    "stalled": ("Stalled", "Branch to the session named on the arc page, then read "
                           "again at the next checkpoint."),
    "worse": ("Worse", "Stop planning the arc and open B8: Pause &amp; Refer."),
}


def at_target(v, m=GOAL):
    """Is this reading already in the band the arc is aiming at?"""
    if not m["bands"]:
        return False
    lo, hi, _name = m["bands"][-1] if m["dir"] == "up" else m["bands"][0]
    return lo <= v <= hi


def verdict(prev, now, m=GOAL):
    """Which of the three outlets a pair of readings points at.

    The ceiling clause is the one that is easy to leave out and wrong to. A
    client who reached the top of the scale cannot move another two points, so
    a rule that only asks "did it move?" marks every good ending as stalled and
    sends the therapist back to re-teach a skill the client already has.
    Holding inside the target band is on track.
    """
    move = (now - prev) if m["dir"] == "up" else (prev - now)
    if move <= -m["step"]:
        return "worse"
    if move >= m["step"]:
        return "on"
    return "on" if at_target(now, m) else "stalled"


def why(prev, now, m=GOAL):
    """"moved" or "held": which clause of the rule produced an on-track verdict."""
    move = (now - prev) if m["dir"] == "up" else (prev - now)
    return "moved" if move >= m["step"] else "held"


# --- where the checkpoints fall --------------------------------------------
def schedule(key):
    """[(ordinal, session, index within the arc, sessions since the last one)]."""
    a = A.BY_KEY[key]
    out, prev = [], a["start"] - 1
    for i, n in enumerate(A.checkpoints(key), 1):
        out.append((i, n, n - a["start"] + 1, n - prev))
        prev = n
    return out


def short_course(key):
    """The three to keep when there are not enough sessions for the whole arc.

    First, middle and last. With four checkpoints the middle one is whichever
    of the two inner checkpoints sits closer to the midpoint of the span, so
    the three kept readings are as evenly spread as the arc allows.
    """
    ns = A.checkpoints(key)
    if len(ns) == 3:
        return list(ns)
    mid = (ns[0] + ns[-1]) / 2.0
    inner = min(ns[1:-1], key=lambda n: abs(n - mid))
    return [ns[0], inner, ns[-1]]


def measures(key):
    """The distinct instruments this arc reads, in the order they appear."""
    out = []
    for n in A.checkpoints(key):
        m = A.CHECKPOINT[n]["measure"]
        if m not in out:
            out.append(m)
    return out


# --- the fifteen worked cases ----------------------------------------------
# A composite for each arc, plotted on the goal scale. The readings are the
# only thing written down: every verdict, every branch and every count printed
# beside them is computed from these by verdict() above, so a case that says
# "stalled" and a chart that rises cannot disagree.
CASE = {
    "INT": ("A man in his fifties, sent by his physician, who is not sure he "
            "wants to be here at all.", 2, (5, 6, 8)),
    "EMO": ("A nurse who can describe the feeling perfectly the next morning "
            "and not at all while it is happening.", 1, (4, 6, 8)),
    "ANX": ("A teacher who has not eaten in a restaurant for two years.",
            2, (4, 4, 7, 9)),
    # The arc that leaves the book. Its fourth checkpoint has no reading
    # because the third one ended the arc: a book of decision rules that only
    # ever shows the comfortable two thirds of its own method is selling a
    # rule it does not mean.
    "DEP": ("A woman six months after redundancy, in bed until noon most days.",
            4, (6, 5, 2)),
    "STR": ("A social worker carrying a caseload of forty and a sick parent.",
            2, (2, 5, 6, 8)),
    "SW": ("A designer who reads one critical comment in a review of thirty.",
           2, (4, 6, 6, 9)),
    "REL": ("A man whose partner has asked him, twice, what he is feeling.",
            3, (5, 6, 8, 10)),
    "TRA": ("A paramedic who is fine on shift and not fine in the car park.",
            2, (5, 7, 9)),
    "GRF": ("A widow eleven months in, who says she should be over it.",
            2, (2, 4, 6)),
    "CMP": ("A student who checks the door lock nine times and knows it is nine.",
            1, (3, 4, 7)),
    "VAL": ("A man who got the promotion and feels nothing about it.",
            3, (6, 8, 10)),
    "ANG": ("A father who has frightened himself twice this month.",
            2, (4, 7, 9)),
    "SLP": ("A shift worker who has not slept through since the baby came.",
            3, (5, 5, 8)),
    "WRK": ("An accountant who has been about to resign for three years.",
            3, (3, 5, 8)),
    "PRG": ("A client of eleven months, four sessions from the end.",
            6, (8, 9, 10)),
}


def case(key):
    """(who, baseline, [(ordinal, session, reading, verdict, why)], outcome).

    A case may carry fewer readings than its arc has checkpoints. That is not
    missing data: a "worse" verdict opens B8, and an arc that has stopped does
    not get read again. Those checkpoints come back with a reading of None.
    """
    who, base, reads = CASE[key]
    sched = schedule(key)
    assert len(reads) <= len(sched), ("case longer than its arc", key)
    rows, prev, stopped = [], base, False
    for i, (ordn, n, _idx, _gap) in enumerate(sched):
        if stopped or i >= len(reads):
            rows.append((ordn, n, None, None, None))
            continue
        r = reads[i]
        v = verdict(prev, r, GOAL)
        rows.append((ordn, n, r, v, why(prev, r, GOAL) if v == "on" else None))
        stopped = v == "worse"
        prev = r
    kinds = [v for _o, _n, _r, v, _w in rows if v]
    assert kinds, ("case with no readings", key)
    assert (len(reads) < len(sched)) == ("worse" in kinds), \
        ("only a worse verdict may cut a case short", key)
    outcome = "worse" if "worse" in kinds else ("stalled" if "stalled" in kinds else "on")
    return who, base, rows, outcome


def counterfactual(key):
    """At the checkpoint that decided the case: what each of the three readings
    would have had to be, and what it would have meant.

    Written out arc by arc because a rule stated once in the abstract is a rule
    a reader believes and cannot apply. The bounds come from the same verdict()
    the charts use, found by trying every reading on the scale rather than by
    restating the arithmetic in a second place where it could drift.
    """
    _who, base, rows, _out = case(key)
    live = [(o, n, r, v) for o, n, r, v, _w in rows if r is not None]
    decisive = next((x for x in live if x[3] != "on"), live[-1])
    ordn, n, _r, _v = decisive
    i = [x[0] for x in live].index(ordn)
    prev = base if i == 0 else live[i - 1][2]
    lo, hi = GOAL["range"]
    got = {}
    for v in range(lo, hi + 1):
        got.setdefault(verdict(prev, v, GOAL), []).append(v)
    out = {}
    for kind, vals in got.items():
        out[kind] = ("%d" % vals[0]) if len(vals) == 1 else ("%d&ndash;%d" % (vals[0], vals[-1]))
    return ordn, n, prev, out


# --- what the front matter says about the whole book ------------------------
def totals():
    every = [(k, A.checkpoints(k)) for k in (a["key"] for a in A.ARCS)]
    counts = [len(ns) for _k, ns in every]
    gaps = [g for k, _ns in every for _i, _n, _x, g in schedule(k)[1:]]
    named = sorted({A.CHECKPOINT[n]["measure"] for _k, ns in every for n in ns}
                   - {"Goal scale", "Treatment scale"})
    outs = [case(k)[3] for k, _ns in every]
    return {
        "arcs": len(every),
        "checkpoints": sum(counts),
        "three": counts.count(3),
        "four": counts.count(4),
        "gap_lo": min(gaps), "gap_hi": max(gaps),
        "gap_avg": sum(gaps) / float(len(gaps)),
        "instruments": named,
        "cases_on": outs.count("on"),
        "cases_stalled": outs.count("stalled"),
        "cases_worse": outs.count("worse"),
    }


def selftest():
    t = totals()
    assert t["checkpoints"] == sum(len(A.checkpoints(a["key"])) for a in A.ARCS)
    assert t["arcs"] == 15
    for a in A.ARCS:
        k = a["key"]
        ns = A.checkpoints(k)
        assert ns == sorted(ns)
        assert len(short_course(k)) == 3
        assert set(short_course(k)) <= set(ns)
        for m in measures(k):
            assert m in MEASURE, (k, m)
        who, base, rows, _out = case(k)
        assert who.strip() and 0 <= base <= 10
        for _i, n, r, v, _w in rows:
            assert n in ns
            assert r is None or (0 <= r <= 10 and v in OUTLET)
    return t


if __name__ == "__main__":
    t = selftest()
    print("%(checkpoints)d checkpoints over %(arcs)d arcs "
          "(%(three)d arcs of three, %(four)d of four)" % t)
    print("gaps between checkpoints: %d to %d sessions, mean %.1f"
          % (t["gap_lo"], t["gap_hi"], t["gap_avg"]))
    print("instruments named: %s" % ", ".join(t["instruments"]))
    print("worked cases: %d on track, %d with a stall, %d that deteriorate"
          % (t["cases_on"], t["cases_stalled"], t["cases_worse"]))
    print()
    for a in A.ARCS:
        k = a["key"]
        who, base, rows, out = case(k)
        print("%-4s %-18s base %2d  %s  -> %s" % (
            k, "/".join(measures(k))[:18], base,
            "  ".join("S%03d %2s %-8s" % (n, r if r is not None else "-", (v or "not reached") + ("/" + w if w else ""))
                      for _i, n, r, v, w in rows), out))
