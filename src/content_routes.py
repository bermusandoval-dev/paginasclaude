# -*- coding: utf-8 -*-
"""The thirty route pages: two pages per route.

Page A explains the route: who it tends to fit, the order and why, the whole
route drawn session by session, what to say, the seams and what to watch for.
Page B is the running order itself, one line per session, with a box and a
date line: it is the page that goes in the client's file.
"""
import math
import re

import arcs as A
import figs as F
import kit as K
import routes as R
import routes_text as T

ORDERED = sorted(T.ROUTES, key=lambda r: r["family"])
for _i, _r in enumerate(ORDERED, 1):
    _r["num"] = _i
    _r["build"] = R.build(_r["keys"])
    _r["slug"] = "r-" + re.match(r"(\w+)", _r["who"]).group(1).lower()
    _r["title"] = " + ".join(A.BY_KEY[k]["short"] for k in _r["build"]["order"])

NUM_OF_PAIR = {frozenset(r["keys"]): r["num"] for r in ORDERED if len(r["keys"]) == 2}


def weeks_text(r):
    s = r["say"]
    for i, seam in enumerate(r["build"]["seams"], 1):
        s = s.replace("{w%d}" % i, str(seam["week"]))
    return s


def page_a(r):
    b = r["build"]
    fam, famline = T.FAMILIES[r["family"]]
    n_arcs = len(b["order"])
    seams = "".join(
        f'<div class="seamc"><div class="hd">Seam {i} &middot; week {s["week"]} '
        f'<span>S{s["last"]["n"]:03d} {K.arrow()} S{s["first"]["n"]:03d} &middot; Rule {R.RULE[s["rule"]]["n"]}: '
        f'{R.RULE[s["rule"]]["name"]}</span></div>'
        f'<p>&ldquo;{R.bridge(s)}&rdquo;</p></div>'
        for i, s in enumerate(b["seams"], 1))
    lead = b["order"][0]
    other = b["order"][1]
    first_other = A.sessions(other)[0]
    return f"""<div class="rpage ra">
<div class="rhead">
  <div class="rnum">{r["num"]:02d}</div>
  <div><div class="fam">{fam} &middot; {n_arcs} arcs</div><h2>{r["title"]}</h2></div>
  <div class="rfacts">
    <div><div class="v">{b["length"]}</div><div class="l">Sessions</div></div>
    <div><div class="v">{b["repeats"]}</div><div class="l">Repeats cut</div></div>
    <div><div class="v">{b["closes"]}</div><div class="l">Endings folded</div></div>
  </div>
</div>
<div class="rband">{K.photo(r["slug"], 96, "")}<div class="cap">{famline}</div></div>
<div class="g55">
  <div><h3>Who tends to walk in</h3><p class="rwho">{r["who"]}</p>
    <p class="micro">A composite written for this book, not a case record.</p></div>
  <div class="rsay"><h3>What you tell the client</h3><p class="quote">&ldquo;{weeks_text(r)}&rdquo;</p></div>
</div>
<div><h3>The order, and the rule behind each step</h3>{F.orderline(b)}</div>
<figure class="figbox"><div class="figw">{F.strip(b)}</div>{F.strip_key()}
<figcaption><b>Override</b>If the client named {A.BY_KEY[other]["short"].lower()} as the reason they came, borrow S{first_other[0]:03d}
&ldquo;{first_other[1]}&rdquo; into week 2 (the override, page {K.pg("p_override")}).</figcaption></figure>
{seams}
</div>"""


def page_b(r):
    b = r["build"]
    watch = "".join(f'<div><span class="dot">{i}</span><br>{w}</div>' for i, w in enumerate(r["watch"], 1))
    rows = []
    week = 0
    for i, k in enumerate(b["order"]):
        a = A.BY_KEY[k]
        v = b["by_arc"][k]
        if i:
            s = b["seams"][i - 1]
            rows.append(f'<div class="run seamrow">Seam {i} &middot; week {s["week"]} &middot; new bridge in S{s["last"]["n"]:03d}</div>')
        rows.append(f'<div class="run head h{i + 1}">Arc {i + 1} &middot; {a["short"]} &middot; {v["kept"]} sessions</div>')
        for it in b["items"]:
            if it["arc"] != k:
                continue
            if it["status"] == "keep":
                week += 1
                extra = ""
                if it["reviews"]:
                    extra = " <small>+ " + ", ".join("S%03d" % x for x in it["reviews"]) + "</small>"
                rows.append(f'<div class="run {F.POSCLS[i]}"><span class="cb"></span><span class="s">S{it["n"]:03d}</span>'
                            f'<span class="t">{it["title"]}{extra}</span></div>')
            elif it["status"] == "repeat":
                rows.append(f'<div class="run cut"><span class="cb"></span><span class="s">S{it["n"]:03d}</span>'
                            f'<span class="t"><small>repeat &middot; see S{it["ref"]:03d}</small></span></div>')
            else:
                rows.append(f'<div class="run cut"><span class="cb"></span><span class="s">S{it["n"]:03d}</span>'
                            f'<span class="t"><small>ending folded</small></span></div>')
    # A long route lists its cuts in one line under the order, so the order
    # itself fits three columns without wrapping.
    long_route = len(b["items"]) > 68
    cutline = ""
    if long_route:
        rows = [x for x in rows if 'class="run cut"' not in x]
        cuts = []
        for it in b["items"]:
            if it["status"] == "repeat":
                cuts.append("S%03d (see S%03d)" % (it["n"], it["ref"]))
            elif it["status"] == "close":
                cuts.append("S%03d (ending)" % it["n"])
        cutline = ('<div class="runfoot"><span><b style="font-weight:600;color:#173C42">Cut from this route:</b> '
                   + ", ".join(cuts) + "</span></div>")
    # The footnote that explains the "+ Sxxx" marker has to name a session that
    # is actually on this page. One hardcoded example put a Sleep session on the
    # 26 routes that carry no Sleep arc.
    revs = sorted({x for it in b["items"] for x in it["reviews"]})
    reviewnote = ("<span>&ldquo;+ S%03d&rdquo;: open with a ten-minute review of "
                  "that session&rsquo;s skill.</span>" % revs[0]) if revs else ""
    cols = 3 if len(rows) > 44 else 2
    per = math.ceil(len(rows) / cols)
    return f"""<div class="rpage">
<div class="runhead">
  <div><div class="eyebrow">Route {r["num"]:02d} &middot; the running order</div>
  <h2 style="margin:0;font-size:21px">{r["title"]}</h2></div>
  <div class="rec"><span>Client initials</span><i></i><span>Start</span><i></i></div>
</div>
<div class="runlist" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({per},auto);align-content:stretch">{"".join(rows)}</div>
{cutline}<div class="runfoot"><span><span class="cbx"></span>Tick when done.</span>
<span>Cut sessions are grey: &ldquo;see&rdquo; names the session that already taught the skill.</span>
{reviewnote}</div>
<div><h3>Watch for on this route</h3><div class="watch">{watch}</div></div>
</div>"""


def pages():
    out = []
    for r in ORDERED:
        a = lambda r=r: page_a(r)
        a.__name__ = "ra%02d" % r["num"]
        bb = lambda r=r: page_b(r)
        bb.__name__ = "rb%02d" % r["num"]
        out.append((a, r))
        out.append((bb, r))
    return out
