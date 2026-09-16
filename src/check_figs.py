# -*- coding: utf-8 -*-
"""What the pages claim, re-derived a second way.

The route builder produces every number in the book. This file does not trust
it: it recomputes route lengths from the Overlap Atlas arithmetic that page 19
teaches, re-reads the seam weeks out of the running order, checks each
"taught in X" sentence in the watch-for boxes against the session data, and
checks the counts printed in Part One against the worked route.
"""
import re
import sys

import arcs as A
import content_front as CF
import content_routes as CR
import routes as R
import routes_text as T

bad = []


def claim(ok, text):
    if not ok:
        bad.append(text)


# 1. Route length by the atlas arithmetic, independently of routes.build()
for r in CR.ORDERED:
    b = r["build"]
    keys = b["order"]
    total = sum(len(A.sessions(k)) for k in keys)
    from collections import Counter
    c = Counter(m for k in keys for m in A.modules(k))
    dup = sum(v - 1 for v in c.values())
    expect = total - dup - 2 * (len(keys) - 1)
    claim(b["length"] == expect, "route %02d length %d, atlas arithmetic %d" % (r["num"], b["length"], expect))
    claim(b["repeats"] == dup, "route %02d repeats %d vs %d" % (r["num"], b["repeats"], dup))
    if len(keys) == 2:
        claim(dup == A.overlap(*keys), "route %02d repeats differ from the atlas cell" % r["num"])
    # 2. seam weeks from the running order
    week = 0
    firsts = {}
    for it in b["items"]:
        if it["status"] == "keep":
            week += 1
            firsts.setdefault(it["arc"], week)
    for s in b["seams"]:
        claim(firsts[s["to"]] == s["week"], "route %02d seam week %d vs %d" % (r["num"], s["week"], firsts[s["to"]]))
    said = CR.weeks_text(r)
    for s in b["seams"]:
        claim(str(s["week"]) in said, "route %02d: the client line does not name week %d" % (r["num"], s["week"]))
    claim("{w" not in said, "route %02d: unfilled week placeholder" % r["num"])
    # 3. "taught in X" in watch-for: X must be an arc on the route that teaches a
    #    module which a later arc on the route has cut
    names = {A.BY_KEY[k]["short"].lower(): k for k in keys}
    names.update({A.BY_KEY[k]["name"].lower(): k for k in keys})
    cut_from = {it["ref"] for it in b["items"] if it["status"] == "repeat"}
    teachers = {A.arc_of(n) for n in cut_from}
    for w in r["watch"]:
        m = re.search(r"taught (?:once, )?in (?:the )?([A-Z][\w &;]+?)(?: arc| and|[;.,])", w)
        if not m:
            continue
        nm = m.group(1).replace("&amp;", "&").strip().lower()
        hit = next((k for n, k in names.items() if n.startswith(nm) or nm.startswith(n) or n.endswith(nm)), None)
        claim(hit is not None, "route %02d: 'taught in %s' names an arc not on the route" % (r["num"], nm))
        claim(hit in teachers, "route %02d: 'taught in %s' but that arc teaches no cut skill" % (r["num"], nm))
    # 4. the override names the first session of the second arc
    first = A.sessions(keys[1])[0]
    claim(first[0] == A.BY_KEY[keys[1]]["start"], "route %02d override session" % r["num"])

# 5. Part One numbers
J = CF.JB
claim(J["total"] == 95 and J["length"] == 85, "Route 05 totals changed: %d / %d" % (J["total"], J["length"]))
claim([s["week"] for s in J["seams"]] == [14, 51], "Route 05 seam weeks %s" % [s["week"] for s in J["seams"]])
claim(any(i["n"] == 83 and i["ref"] == 319 for i in J["items"]), "S083 is no longer a repeat of S319")
claim(any(i["n"] == 84 and 319 in i["reviews"] for i in J["items"]), "S084 no longer opens with the S319 review")
claim(any(i["n"] == 49 and i["reviews"] == [90, 91] for i in J["items"]), "S049 no longer folds S090 and S091")
own = CF.OWN
claim(own["order"] == ["GRF", "ANX"] and own["seams"][0]["rule"] == "R3", "Grief + Anxiety order or rule changed")
claim(A.overlap("GRF", "ANX") == 1, "Grief + Anxiety atlas cell is not 1")

# 6. atlas and finder
for a in A.COMBINABLE:
    for b2 in A.COMBINABLE:
        claim(A.overlap(a, b2) == A.overlap(b2, a), "atlas not symmetric at %s %s" % (a, b2))
claim(len(CR.NUM_OF_PAIR) == 22, "pairs in the finder: %d" % len(CR.NUM_OF_PAIR))
claim(sum(1 for r in CR.ORDERED if len(r["keys"]) == 3) == 8, "trios: not eight")
claim(len({r["slug"] for r in CR.ORDERED}) == 30, "a route photo is used twice")

# 7. every route's arcs appear in ladder order and families are contiguous
for r in CR.ORDERED:
    lay = [R.LAYER[k] for k in r["build"]["order"]]
    claim(lay == sorted(lay), "route %02d not in ladder order" % r["num"])
fams = [r["family"] for r in CR.ORDERED]
claim(fams == sorted(fams), "families are not contiguous")

print("checked 30 routes, Part One and the atlas")
if bad:
    print("%d FALSE CLAIM(S):" % len(bad))
    for x in bad:
        print("   " + x)
    sys.exit(1)
print("all claims hold")
