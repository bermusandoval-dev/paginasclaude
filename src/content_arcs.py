# -*- coding: utf-8 -*-
"""Part Two: the fifteen arc spreads, two pages each.

The left page is the schedule -- where the checkpoints fall, what each one
reads, and the three ways out of each. The right page is one worked case for
that arc, charted, with the cautions that apply when you read its numbers.

Both pages are generated from the same loop, so an arc cannot be given a
checkpoint on one page and not the other, and no arc can be quietly skipped.
"""
import arcs as A
import checkpoints as C
import cp_text as X
import figs_cp as G
import kit as K

ARC_PHOTO = {a["key"]: "a-" + a["key"].lower() for a in A.ARCS}
NUM = {a["key"]: i for i, a in enumerate(A.ARCS, 1)}


def sid(n):
    return "S%03d" % n


def title_of(n):
    a = A.BY_KEY[A.arc_of(n)]
    return a["sessions"][n - a["start"]][0]


def _next_session(key, n):
    """Where 'stay on the arc' actually goes, so the card can name it."""
    a = A.BY_KEY[key]
    last = a["start"] + len(a["sessions"]) - 1
    return n + 1 if n < last else None


def checkpoint_card(key, ordn, n):
    cp = A.CHECKPOINT[n]
    nxt = _next_session(key, n)
    on = ("Stay on the arc: %s &ldquo;%s&rdquo;." % (sid(nxt), title_of(nxt))) if nxt \
        else "Stay on the arc and close it as written."
    return f"""<div class="cp">
  <div class="hd"><span class="n">{ordn}</span><span class="s">{sid(n)}</span>
    <span class="ti">{title_of(n)}</span><span class="m">{cp["measure"]}</span></div>
  <p class="ask">&ldquo;{cp["goal"]}&rdquo;</p>
  <div class="outs">
    <div class="o"><i></i><span><b>On track</b> &middot; {on}</span></div>
    <div class="s"><i></i><span><b>Stalled</b> &middot; go to {sid(cp["stalled"])}
      &ldquo;{title_of(cp["stalled"])}&rdquo;, then read again here next time.</span></div>
    <div class="w"><i></i><span><b>Worse</b> &middot; stop the arc and open B8.</span></div>
  </div>
</div>"""


def measure_cards(key):
    """What this arc reads, and on what terms. One card per distinct measure,
    plus the card that is the same on all fifteen pages and is the one a
    reader most needs not to have to look up."""
    out = []
    for name in C.measures(key):
        m = C.MEASURE[name]
        step = ("A step is <b>%s</b>." % m["step"]) if m["step"] else \
            "Its step is whichever instrument it turns out to be."
        out.append(f'''<div class="card tint"><h3>{name}</h3>
        <p class="micro">{m["what"]}. {step} {m["licence"].split(".")[0]}.</p></div>''')
    out.append('''<div class="card rust"><h3>Two stalls in a row</h3>
    <p class="micro">A second stalled reading straight after taking the branch means the arc
    is not the problem the client has. Go back to the formulation before you branch
    again.</p></div>''')
    out.append('''<div class="card"><h3>The first reading</h3>
    <p class="micro">Take a baseline at the arc&rsquo;s opening session, using the same item
    as checkpoint 1. It is not a checkpoint and gets no verdict, but without it the first
    comparison has nothing to stand on.</p></div>''')
    return "".join(out)


def page_a(key):
    a = A.BY_KEY[key]
    sched = C.schedule(key)
    ms = C.measures(key)
    cards = "".join(checkpoint_card(key, i, n) for i, n, _x, _g in sched)
    gaps = [g for _i, _n, _x, g in sched[1:]]
    cols = min(3, len(ms) + 2)
    return f"""
<div class="eyebrow">Part Two &middot; arc {NUM[key]} of {len(A.ARCS)} &middot; {sid(a["start"])}&ndash;{sid(a["start"] + len(a["sessions"]) - 1)}</div>
<h2>{a["name"]}</h2>
<p class="lede">{"Builds " + a["builds"] + "." if a.get("builds") else
                 "The frame around the fifteen: what is measured here is whether the work has started, not whether it has worked."}</p>
<figure class="figbox"><div class="figw">{G.timeline(key)}</div>{G.timeline_key()}
<figcaption><b>{len(a["sessions"])} sessions &middot; {len(sched)} readings &middot; first at
{sid(sched[0][1])} &middot; {min(gaps)}&ndash;{max(gaps)} sessions apart &middot; reads
{", ".join(ms).lower()}</b>The ochre squares are the sessions a stalled reading sends the
client back to, and the dashed arrow shows which checkpoint sends them there.</figcaption></figure>
<div class="cps">{cards}</div>
<div class="g{cols}">{measure_cards(key)}</div>
"""


def page_b(key):
    a = A.BY_KEY[key]
    who, base, rows, outcome = C.case(key)
    cells = [f'<div><div class="v">{base}</div><div class="l">Baseline<br>{sid(a["start"])}</div></div>']
    for ordn, n, r, v, w in rows:
        if r is None:
            cells.append(f'<div class="none"><div class="v">&mdash;</div>'
                         f'<div class="l">Checkpoint {ordn}<br>not read</div></div>')
            continue
        lab = C.OUTLET[v][0] + (" (held)" if w == "held" else "")
        cells.append(f'<div class="{v}"><div class="v">{r}</div>'
                     f'<div class="l">Checkpoint {ordn} &middot; {sid(n)}<br>{lab}</div></div>')
    # the branches this case actually took, named from the registry
    took = [A.CHECKPOINT[n]["stalled"] for _o, n, _r, v, _w in rows if v == "stalled"]
    branch = ("It branched to " + ", ".join("%s &ldquo;%s&rdquo;" % (sid(b), title_of(b)) for b in took)
              + ".") if took else ""
    watch = X.WATCH[key]
    watch = [t % K.pg("p_ontrack") if "%s" in t else t for t in watch]
    watchhtml = "".join(f'<div><span class="dot">{i}</span><br>{t}</div>'
                        for i, t in enumerate(watch, 1))
    short = C.short_course(key)
    cf_ord, cf_n, cf_prev, cf = C.counterfactual(key)
    cf_cp = A.CHECKPOINT[cf_n]
    means = {
        "on": "Stay on the arc.",
        "stalled": "Go to %s &ldquo;%s&rdquo;." % (sid(cf_cp["stalled"]), title_of(cf_cp["stalled"])),
        "worse": "Stop the arc and open B8.",
    }
    cf_rows = [[f'<b>{cf[k]}</b>', C.OUTLET[k][0], means[k]]
               for k in ("on", "stalled", "worse") if k in cf]
    cf_note = ("There is no stalled band here at all: the previous reading of %d is already "
               "inside the target band, so anything that has not fallen by a step is on "
               "track. That is the ceiling clause on page %s doing its work."
               % (cf_prev, K.pg("p_ontrack"))) if "stalled" not in cf else \
        ("Read against the reading before it, never against the baseline of %d."
         % C.CASE[key][1])
    return f"""
<div class="eyebrow">Arc {NUM[key]} &middot; {a["short"]} &middot; one worked case</div>
<div class="rband">{K.photo(ARC_PHOTO[key], 92, a["short"])}
<div class="cap">{who}</div></div>
<div class="g55">
  <div class="stack">
    <h2 style="font-size:23px">{"A case that " + {"on": "ran clean", "stalled": "stalled once", "worse": "left the book"}[outcome]}</h2>
    <p class="micro">A composite written for this book, not a case record. Every verdict
    below is computed from the readings by the rule on page {K.pg("p_three")}, not chosen
    to make a point.</p>
    <p>{X.CASE_NOTE[key]} {branch}</p>
    <div class="card tint"><h3>At checkpoint {cf_ord} &middot; {sid(cf_n)}, against {cf_prev}</h3>
    {K.table(["Reading", "Outlet", "Which means"], cf_rows, cls="tight")}
    <p class="micro" style="margin-top:5px">{cf_note}</p></div>
  </div>
  <div class="stack">
    <figure class="figbox bare"><div class="figw">{G.chart(key)}</div>{G.chart_key()}</figure>
    <div class="case">{"".join(cells)}</div>
    <figure class="figbox tint"><div class="figw">{G.shortfig(key)}</div>
    <figcaption><b>Short course</b>Keep the first, the middle and the last:
    {", ".join(sid(n) for n in short)}.</figcaption></figure>
  </div>
</div>
<div><h3>What to watch when you read this arc</h3><div class="watch">{watchhtml}</div></div>
"""


def pages():
    """[(fn, arc key)] -- both pages of every arc, in registry order."""
    out = []
    for a in A.ARCS:
        key = a["key"]
        fa = lambda key=key: page_a(key)
        fa.__name__ = "ca" + key.lower()
        fb = lambda key=key: page_b(key)
        fb.__name__ = "cb" + key.lower()
        out.append((fa, a))
        out.append((fb, a))
    return out
