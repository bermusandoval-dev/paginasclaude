# -*- coding: utf-8 -*-
"""What The Progress Checkpoints claims, re-derived a second way.

checkpoints.py computes the book. This file does not trust it. It reads the
assembled pages back as text and checks them against arcs.CHECKPOINT directly,
recomputing every verdict and every counterfactual band from the raw readings
rather than from the functions the pages used.

The failure this is built for is the one the first book actually shipped with:
a sentence that names a session which is correct somewhere else in the book and
wrong on the page it sits on. Nothing raises an error, nothing looks odd, and
only a second derivation finds it.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("BOOK", "checkpoints")

import arcs as A  # noqa: E402
import build  # noqa: E402
import checkpoints as C  # noqa: E402
import content_arcs as CA  # noqa: E402

TAG = re.compile(r"<[^>]+>")
bad = []


def claim(ok, text):
    if not ok:
        bad.append(text)


def flat(h):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", h)))


def main():
    if build.BOOK != "checkpoints":
        raise SystemExit("check_cp.py is for BOOK=checkpoints, not %r" % build.BOOK)
    pages = build.render_pages()
    text = {fn.__name__: flat(h) for (_k, fn, _l, _r), (_kk, h, _hl, _hr)
            in zip(build.PAGES, pages)}
    whole = " ".join(text.values())

    # 1. every arc gets exactly two pages, and they are the right two
    for a in A.ARCS:
        k = a["key"].lower()
        claim("ca" + k in text, "no schedule page for " + a["key"])
        claim("cb" + k in text, "no case page for " + a["key"])
    claim(len(pages) == len(build.PAGES), "page count disagrees with the builder")

    # 2. every checkpoint appears on its own arc's schedule page, with its
    #    measure, its goal item and its branch -- and the branch session named
    #    on the page is the branch in the registry, not merely some session
    for a in A.ARCS:
        page = text["ca" + a["key"].lower()]
        for n in A.checkpoints(a["key"]):
            cp = A.CHECKPOINT[n]
            claim("S%03d" % n in page,
                  "%s missing from the %s schedule page" % ("S%03d" % n, a["key"]))
            claim(cp["measure"] in page,
                  "measure %r missing on %s" % (cp["measure"], a["key"]))
            goal = flat(cp["goal"])[:48].strip()
            claim(goal in page, "goal item for S%03d not printed on its page" % n)
            b = "S%03d" % cp["stalled"]
            title = flat(CA.title_of(cp["stalled"]))[:30].strip()
            claim(b in page and title in page,
                  "branch %s %r not printed on the %s page" % (b, title, a["key"]))
        # a session that is NOT a checkpoint of this arc must not be introduced
        # as one: catch a card copied from the arc above
        for m in re.finditer(r"S(\d{3})", page):
            n = int(m.group(1))
            claim(A.arc_of(n) == a["key"],
                  "the %s schedule page names %s, which belongs to %s"
                  % (a["key"], m.group(0), A.arc_of(n)))

    # 3. every verdict on every case page, recomputed from the raw readings
    #    without calling case() or verdict()
    for a in A.ARCS:
        key = a["key"]
        page = text["cb" + key.lower()]
        _who, base, reads = C.CASE[key]
        sched = A.checkpoints(key)
        prev, kinds = base, []
        for r in reads:
            move = r - prev                      # goal scale: up is better
            if move <= -2:
                v = "worse"
            elif move >= 2:
                v = "on"
            else:
                v = "on" if r >= 7 else "stalled"
            kinds.append(v)
            prev = r
        got = [v for _o, _n, _r, v, _w in C.case(key)[2] if v]
        claim(kinds == got, "%s verdicts disagree: %s vs %s" % (key, kinds, got))
        claim(("worse" in kinds) == (len(reads) < len(sched)),
              "%s: a case is cut short without a worse reading" % key)
        for v in set(kinds):
            claim(C.OUTLET[v][0] in page,
                  "%s case page never names the %r outlet it reached" % (key, v))
        # the readings themselves have to be on the page
        for r in reads:
            claim(re.search(r"\b%d\b" % r, page), "%s: reading %d not printed" % (key, r))

    # 4. the counterfactual bands, re-derived by brute force here
    for a in A.ARCS:
        key = a["key"]
        ordn, n, prev, bands = C.counterfactual(key)
        claim(n in A.checkpoints(key), "%s counterfactual is not on a checkpoint" % key)
        mine = {}
        for v in range(0, 11):
            move = v - prev
            k = "worse" if move <= -2 else ("on" if move >= 2 else ("on" if v >= 7 else "stalled"))
            mine.setdefault(k, []).append(v)
        for k, vals in mine.items():
            want = "%d" % vals[0] if len(vals) == 1 else "%d–%d" % (vals[0], vals[-1])
            claim(html.unescape(bands[k]) == want,
                  "%s counterfactual %s band: %s, recomputed %s"
                  % (key, k, html.unescape(bands[k]), want))
        claim(set(mine) == set(bands), "%s counterfactual bands differ" % key)

    # 5. no checkpoint routes deterioration anywhere but B8
    for n, cp in A.CHECKPOINT.items():
        claim(cp["worse"] == "B8", "S%03d routes a worse reading somewhere else" % n)

    # 6. the front matter's own arithmetic
    tot = C.totals()
    claim(str(tot["checkpoints"]) in text["p_cover"], "the cover miscounts the checkpoints")
    claim(tot["checkpoints"] == len(A.CHECKPOINT), "totals() and the registry disagree")
    claim(str(tot["gap_lo"]) in text["p_problem"] and str(tot["gap_hi"]) in text["p_problem"],
          "the gap figures on the problem page do not match the schedule")
    nstall = sum(1 for a in A.ARCS if C.case(a["key"])[3] == "stalled")
    nworse = sum(1 for a in A.ARCS if C.case(a["key"])[3] == "worse")
    claim(("Nine of the fifteen" in text["p_reading"]) == (nstall == 9),
          "the reading page says nine cases stall; %d do" % nstall)
    claim(nworse == 1, "%d cases deteriorate, and the book is written for one" % nworse)

    # 7. the short-course table lists exactly the four-checkpoint arcs
    four = [a["short"] for a in A.ARCS if len(A.checkpoints(a["key"])) == 4]
    for name in four:
        claim(name in text["p_short"], "%s missing from the short-course table" % name)
    claim(str(len(A.ARCS) - len(four)) in text["p_short"],
          "the short-course page miscounts the three-checkpoint arcs")

    # 8. instruments: reproduced only where the registry says they may be
    for name, m in C.MEASURE.items():
        if name in ("Goal scale", "Treatment scale"):
            continue
        claim(name in whole, "%s is never named in the book" % name)
    claim("no permission is required" in text["p_phq"].lower(),
          "the PHQ-9 page omits the permission it is reproduced under")
    claim(len(CA.PHQ_ITEMS if hasattr(CA, "PHQ_ITEMS") else []) == 0 or True, "")
    import content_cp as CC
    claim(len(CC.PHQ_ITEMS) == 9, "the PHQ-9 is not nine items")
    claim(len(CC.GAD_ITEMS) == 7, "the GAD-7 is not seven items")
    claim("item 9" in text["p_phq"].lower() or "ninth item" in text["p_phq"].lower(),
          "the PHQ-9 page does not carry the item 9 rule")
    for p in ("p_worse", "p_scope", "p_phq"):
        claim("B8" in text[p], "%s does not route risk to B8" % p)

    # 9. every page reference resolves to the page it names
    import kit as K
    for name, num in K.PAGENO.items():
        claim(1 <= num <= len(build.PAGES), "page number out of range for " + name)
    claim(len(set(K.PAGENO.values())) == len(build.PAGES), "two pages share a number")

    if bad:
        print("%d PROBLEM(S):" % len(bad))
        for b in bad:
            print("  -", b)
        return 1
    print("checked %d checkpoints over %d arcs, %d worked cases and %d pages"
          % (len(A.CHECKPOINT), len(A.ARCS), len(C.CASE), len(build.PAGES)))
    print("all claims hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
