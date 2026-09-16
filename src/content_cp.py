# -*- coding: utf-8 -*-
"""Front matter, Part One (reading the number), Part Three (the sheets),
scope and the back cover of The Progress Checkpoints.

The worked example that runs through Part One is the Anxiety arc, computed
live from the registry, so the sessions named in the method cannot drift from
the sessions printed on the arc pages.
"""
import arcs as A
import checkpoints as C
import content_arcs as CA
import figs_cp as G
import kit as K

W = "ANX"          # the arc Part One teaches on
WA = A.BY_KEY[W]
WS = C.schedule(W)


def sid(n):
    return "S%03d" % n


def t(n):
    return CA.title_of(n)


def opener(img, num, title, sub, inside):
    items = "".join(f"<li>{x}</li>" for x in inside)
    return f"""<div class="opener">
<div class="img"><img src="{K.PHOTO % img}" alt=""></div>
<div class="txt" style="padding:12mm 17.5mm 16mm">
  <div><div class="chno">{num}</div><h1>{title}</h1><div class="rulec"></div><p class="sub">{sub}</p></div>
  <div class="inside"><h3>Inside</h3><ol>{items}</ol></div>
</div></div>"""


def outlets(extra=None):
    """The three outlet cards. Wording lives here, not inside the drawing."""
    extra = extra or {}
    d = {
        "w": ("Worse", "The reading moved away from the goal by a step or more. Stop "
                       "planning the arc and open B8: Pause &amp; Refer."),
        "s": ("Stalled", "It moved less than a step, either way. Branch to the session "
                         "named on the arc page, then read again at the next checkpoint."),
        "o": ("On track", "It moved toward the goal by a step or more &mdash; or it is "
                          "already inside the target band and has not fallen. Stay on the arc."),
    }
    d.update(extra)
    return ('<div class="outlet">'
            + "".join(f'<div class="{k}"><div class="t">{d[k][0]}</div><p>{d[k][1]}</p></div>'
                      for k in ("w", "s", "o"))
            + "</div>")


# ================================================================== front ===
def p_cover():
    tot = C.totals()
    return f"""<div class="opener cover">
<div class="img" style="flex-basis:60%"><img src="{K.PHOTO % 'h0-cover'}" alt=""></div>
<div style="padding:11mm 17.5mm 14mm;flex:1 1 auto;display:flex;flex-direction:column">
  <div class="brand">Session Arc &middot; Companion 02</div>
  <h1>The Progress Checkpoints</h1>
  <p class="sub" style="max-width:128mm">Fifty check-in points built into the fifteen arcs &mdash;
  what to measure, when to measure it, and which branch to take when the numbers stop moving.</p>
  <div class="facts">
    <div><div class="v">{tot["checkpoints"]}</div><div class="l">Checkpoints</div></div>
    <div><div class="v">{tot["arcs"]}</div><div class="l">Arcs covered</div></div>
    <div><div class="v">3</div><div class="l">Ways out of each</div></div>
    <div><div class="v">15</div><div class="l">Worked cases</div></div>
  </div>
  <div style="margin-top:auto;font-size:8px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#6B7D7E">
  For licensed mental health professionals &middot; &copy; Sando LLC</div>
</div></div>"""


def p_fits():
    return f"""
<div class="eyebrow">Start here</div>
<h2>What this book <em>answers</em></h2>
<p class="lede">The Arc Maps say where to go next. They do not say whether you are getting
there. This book puts a reading at fixed points in every arc, and gives each one exactly
three ways out.</p>
<div class="g2">
  <div class="card sage"><h3>It answers</h3><ul class="ticks">
    <li><span>Where in this arc do I stop and take a reading?</span></li>
    <li><span>What do I measure, when there is no free instrument for it?</span></li>
    <li><span>How much movement counts as movement?</span></li>
    <li><span>The number has not moved &mdash; which session do I go back to?</span></li>
    <li><span>How do I say all of this to the client in three minutes?</span></li>
  </ul></div>
  <div class="card"><h3>It does not answer</h3><ul class="ticks">
    <li><span>Whether a client is safe. No checkpoint assesses risk; all of them hand it to
    <b>B8 &middot; Pause &amp; Refer</b> and your local protocol.</span></li>
    <li><span>What the diagnosis is. Screening and monitoring are not diagnosis.</span></li>
    <li><span>Where the client is in the arc &mdash; that is the Dashboard.</span></li>
    <li><span>How to write the note. That is <b>B5</b>.</span></li>
  </ul></div>
</div>
<div><h3>How it sits against the rest of the shelf</h3>
{K.table(["Piece", "Its question", "Where the line falls"], [
    ["<b>Arc Maps</b>", "Where next?", "They branch on your impression. A checkpoint branches on a number, and names the same kind of session."],
    ["<b>Companion 01</b><br>The Combined Routes", "Which arc first?", "Routes plans the order at intake. Checkpoints reads what happened after, inside whichever arc runs."],
    ["<b>B5</b> Progress notes", "How do I write it up?", "B5 shapes the note. This book supplies the figure the note cites."],
    ["<b>B8</b> Pause &amp; Refer", "Should this stop?", "Every third outlet ends at B8. Nothing here decides a referral; it decides when to go and read that page."],
])}</div>
<div class="g3">
  <div class="card"><h3>If you already measure</h3><p class="micro">Keep your instrument and
  take the schedule. What this adds is the decision: a step that counts, three outlets, and a
  named session at the end of the middle one.</p></div>
  <div class="card"><h3>If you never have</h3><p class="micro">Start with the goal scale and
  one arc &mdash; one question, three or four times in a course of treatment.</p></div>
  <div class="card"><h3>If your service requires it</h3><p class="micro">This gives you the
  measure, the schedule, and the sentence for the note.</p></div>
</div>
<p class="micro">Throughout, a session is named by its number and title &mdash; {sid(WS[0][1])}
&ldquo;{t(WS[0][1])}&rdquo; &mdash; so the book can be used beside the arcs without
cross-referencing anything by hand.</p>
"""


def p_contents():
    """The contents, as a table.

    .toc is a table in the stylesheet -- .toc td, .toc .pg, .toc .d. Written as
    a <ul> it inherited none of that and every line came out as
    "26Intake3 checkpoints" with nothing between the parts.
    """
    def rows(items, cls="toc"):
        out = []
        for kind, title, fn, sub in items:
            if kind == "part":
                out.append(f'<tr class="part"><td colspan="3">{title}</td></tr>')
                continue
            out.append(f'<tr><td>{title}</td><td class="d">{sub}</td>'
                       f'<td class="pg">{K.pg(fn)}</td></tr>')
        return f'<table class="{cls}">' + "".join(out) + "</table>"

    left = rows([
        ("part", "Start here", "", ""),
        ("", "What this book answers", "p_fits", "and the four things it does not"),
        ("", "Four months in", "p_problem", "the question this book exists for"),
        ("", "What a checkpoint is", "p_anatomy", "the five parts of one"),
        ("part", "Part One &middot; Reading the number", "", ""),
        ("", "One reading, three ways out", "p_three", "the rule, whole"),
        ("", "On track", "p_ontrack", "including the clause about ceilings"),
        ("", "Stalled", "p_stalled", "and what a branch is for"),
        ("", "Worse", "p_worse", "and the three things that skip the rule"),
        ("", "Choosing the measure", "p_choose", "instrument, diary or goal scale"),
        ("", "Writing a goal scale", "p_goal", "in four steps, worked"),
        ("", "What you may reproduce", "p_licence", "instrument by instrument"),
        ("", "The PHQ-9", "p_phq", "in full, with the item&nbsp;9 rule"),
        ("", "The GAD-7", "p_gad", "in full, and scoring worked"),
        ("", "Running a checkpoint", "p_run", "five steps, about three minutes"),
        ("", "The review script", "p_script", "word for word"),
        ("", "When it is not good news", "p_words", "two more scripts"),
        ("", "Plotting it", "p_chart", "one sheet per client"),
        ("", "Charts that mislead", "p_lies", "three shapes to distrust"),
        ("", "Short courses", "p_short", "first, middle, last"),
        ("", "The checkpoint and the note", "p_note", "what to write, what not to"),
        ("", "When measuring is the wrong move", "p_stop", "four times to put it down"),
        ("", "Reading an arc spread", "p_reading", "how Part Two is laid out"),
    ], "toc sm")
    arcs = '<table class="toc sm">' + '<tr class="part"><td colspan="3">Part Two &middot; '
    arcs += 'The fifteen arcs</td></tr>'
    for i, a in enumerate(A.ARCS, 1):
        ns = A.checkpoints(a["key"])
        arcs += (f'<tr><td><span class="sid">{i:02d}</span>&nbsp;&nbsp;{a["name"]}</td>'
                 f'<td class="d">{len(ns)} &middot; {", ".join(C.measures(a["key"]))}</td>'
                 f'<td class="pg">{K.pg("ca" + a["key"].lower())}</td></tr>')
    arcs += "</table>"
    three = rows([
        ("part", "Part Three &middot; Sheets", "", ""),
        ("", "The chart sheet", "p_sheet1", "one client, one measure, one page"),
        ("", "The goal-scale sheet", "p_sheet2", "write the item in session"),
        ("", "The caseload sheet", "p_sheet3", "who is due a reading, and when"),
        ("", "Scope, referral and sources", "p_scope", ""),
    ], "toc sm")
    return f"""
<div class="eyebrow">Start here</div>
<h2>Contents</h2>
<p class="lede">Three parts. The method, the fifteen arcs, and three sheets to copy.</p>
<div class="g2">
  <div>{left}</div>
  <div class="stack">{arcs}{three}</div>
</div>
"""


def p_problem():
    tot = C.totals()
    return f"""
<div class="eyebrow">Start here</div>
<h2>&ldquo;Four months in, and I honestly <em>cannot tell</em> if it is helping.&rdquo;</h2>
<div class="g55">
  <div class="stack">
    <p class="lede">It is not a failure of attention. It is that nothing in the week asks
    the question in a form that can be answered.</p>
    <p>Sessions go well or badly. A client arrives lighter, or does not. Six weeks on, the
    impression is of movement &mdash; built out of the sessions you remember, which are the
    memorable ones. Meanwhile the client has begun to wonder the same thing, privately, and
    will not raise it.</p>
    <p>The fix is not more sensitivity. It is a fixed point, agreed in advance, where one
    short question is asked and the answer written down. Not every session: that turns the
    work into an audit. {tot["checkpoints"]} points across {tot["arcs"]} arcs, between
    {tot["gap_lo"]} and {tot["gap_hi"]} sessions apart.</p>
    <div class="card line"><p>Two readings are an anecdote. Three are a direction.</p></div>
  </div>
  <div class="stack">
    {K.capt("c1-months", 168, "Sixteen weeks of sessions, and nothing in the record that answers the question.")}
    <div class="card tint"><h3>What it replaces</h3>
    <p class="micro">Not your judgment &mdash; your memory. The reading is taken in the
    room, in front of the client, and written where you will both see it next time.</p></div>
  </div>
</div>
<figure class="figbox"><div class="figw">{G.spread()}</div>
<figcaption><b>Every checkpoint in the book</b>Each arc drawn to the same width; the figure
on the right is how many sessions it holds. Longer arcs get four readings, shorter ones
three.</figcaption></figure>
"""


def p_anatomy():
    n = WS[1][1]
    cp = A.CHECKPOINT[n]
    return f"""
<div class="eyebrow">Start here</div>
<h2>What a <em>checkpoint</em> is</h2>
<p class="lede">Five parts, all fixed before the client arrives. That is the point: what you
decide about a stalled client should not depend on the kind of day you are having.</p>
<div class="g55">
  <div class="stack">
    {K.legend([
        ("A session, not a week.&nbsp;", "Checkpoints sit on numbered sessions, so a client who misses three weeks still gets their second reading in the right place in the work."),
        ("A measure.&nbsp;", "An instrument where one may lawfully be reproduced, the client&rsquo;s own diary where the arc already collects one, and the arc&rsquo;s 0&ndash;10 goal item in every case."),
        ("A step.&nbsp;", "The smallest change that counts as change. Different for each measure, and printed beside it."),
        ("Three ways out.&nbsp;", "On track, stalled, worse. No fourth, and no &ldquo;wait and see&rdquo; &mdash; waiting is what the book is for."),
        ("A named branch.&nbsp;", "Stalled does not mean try harder. It means go to one particular session, which is printed on the arc page."),
    ], cols=1)}
  </div>
  <div class="stack">{K.capt("c2-anatomy", 150, "One checkpoint, before anyone has written on it.")}</div>
</div>
<div class="card tint"><div class="eyebrow">Worked, on {WA["name"]}</div>
<div class="g3">
  <div><h3>The session</h3><p class="micro">{sid(n)} &ldquo;{t(n)}&rdquo;, the
  {WS[1][0]}nd of {len(WS)} readings in this arc.</p></div>
  <div><h3>The measure</h3><p class="micro">{cp["measure"]}, plus the goal item:
  &ldquo;{cp["goal"]}&rdquo;</p></div>
  <div><h3>The branch</h3><p class="micro">A stalled reading here goes to
  {sid(cp["stalled"])} &ldquo;{t(cp["stalled"])}&rdquo; &mdash; the session this arc
  already contains for exactly this.</p></div>
</div></div>
<div class="g2">
  <div><h3>Why these sessions</h3>
  <p>Three rules placed all fifty. Never an arc&rsquo;s opening session, with nothing to
  compare against. Never one of its closing sessions, because an arc that is ending does not
  branch. And where the arc already holds a review, the checkpoint goes there.</p></div>
  <div><h3>Why three or four, and not eight</h3>
  <p>Longer arcs get four readings, shorter ones three, which puts them
  {C.totals()["gap_lo"]}&ndash;{C.totals()["gap_hi"]} sessions apart. Closer and you read
  noise: the same person asked two weeks running moves a point for reasons that are nothing
  to do with treatment. Further apart and a stalled arc runs a month unnoticed.</p></div>
</div>
<p class="micro">The branch is what makes these checkpoints yours rather than generic. It is
not advice in general terms; it is a session number in a book you already own.</p>
"""


def p_op1():
    return opener("h1-method", "Part One", "Reading the number",
                  "One rule, three outlets, and the dozen ways a true number can still lead "
                  "you somewhere wrong. This part is the whole method; Part Two is that "
                  "method applied, arc by arc.",
                  ["One reading, three ways out", "On track, stalled, worse",
                   "Choosing the measure", "Writing a goal scale",
                   "What you may reproduce", "The PHQ-9 and the GAD-7",
                   "Running a checkpoint", "The review script",
                   "Plotting it, and charts that mislead", "Short courses",
                   "The note, and when to stop measuring"])


# ================================================== part one: the rule ======
def p_three():
    return f"""
<div class="eyebrow">Part One &middot; the rule</div>
<h2>One reading, <em>three ways out</em></h2>
<p class="lede">Every checkpoint in this book runs the same rule. Learn it here and you can
read any of the {2 * len(A.ARCS)} arc pages without looking anything up.</p>
<figure class="figbox bare"><div class="figw">{G.tree()}</div></figure>
{outlets()}
<div class="g64">
  <div class="stack">
    <div><h3>What a step is</h3>
    <p>Each measure carries its own step, because four points on the GAD-7 and four points
    on a 0&ndash;10 scale are not the same distance. They are tabulated on page
    {K.pg("p_choose")} and repeated beside every instrument. On the goal scale the step is
    <b>two points</b>.</p></div>
    <div><h3>Which reading you compare with</h3>
    <p>Always the one before. Not the baseline &mdash; a client who improved a great deal by
    checkpoint 2 and then slid back would go on reading as &ldquo;better than baseline&rdquo;
    for months while getting worse every week. The first checkpoint is the only one that
    compares with baseline, because it has nothing else.</p></div>
  </div>
  <div class="card ochre"><h3>The rule is a floor, not a ceiling</h3>
  <p class="micro">If the number says on track and everything you can see says otherwise,
  the number is wrong and you are right. Write down what you saw, keep the reading, and
  read them together next time. What the rule removes is not your judgment; it is the
  option of never asking.</p></div>
</div>
{K.capt("c3-three", 96, "Three ways out, and the arc page names which session each one leads to.")}
"""


def p_ontrack():
    m = C.MEASURE["Goal scale"]
    return f"""
<div class="eyebrow">Part One &middot; outlet one</div>
<h2><em>On track</em></h2>
<p class="lede">Two different readings earn this outlet, and the second is the one most
rules forget.</p>
<div class="g2">
  <div class="card sage"><h3>It moved</h3>
  <p class="micro">The reading came toward the goal by at least one step since the last
  checkpoint. On the goal scale that is two points; on the PHQ-9, five.</p>
  <div class="figw" style="margin-top:8px">{G.shape("on")}</div></div>
  <div class="card sage"><h3>It held, at target</h3>
  <p class="micro">The reading is inside the target band &mdash; {m["bands"][-1][0]} or more
  on the goal scale &mdash; and has not fallen by a step. A client at nine cannot move two
  more points, and a rule that only asks &ldquo;did it move?&rdquo; would mark every good
  ending as a stall and send them back to relearn a skill they already have.</p>
  <div class="figw" style="margin-top:8px">{G.artifact("ceiling")}</div></div>
</div>
<div class="g46">
  <div class="stack">
    <div><h3>What you do</h3>
    <p>Say the number out loud, say which way it went, and carry on with the session you had
    planned. An on-track reading is not an occasion to review the treatment; it is permission
    to stop wondering.</p></div>
    <div><h3>What it does not mean</h3>
    <ul class="ticks">
      <li><span>That the treatment caused it. A good fortnight, a new job and a change of
      medication all move a reading.</span></li>
      <li><span>That the client is well. The item asks about one goal and is silent about
      everything else.</span></li>
      <li><span>That you can stop measuring at the next checkpoint.</span></li>
    </ul></div>
    <div class="card line"><p class="micro"><b>Do not celebrate the number.</b> A client who
    learns that high numbers please you will give you high numbers.</p></div>
  </div>
  {K.capt("k1-ontrack", 150, "Four readings, each a step better than the last: the shape you are hoping for, and the least interesting one to read.")}
</div>
"""


def p_stalled():
    n = WS[1][1]
    cp = A.CHECKPOINT[n]
    return f"""
<div class="eyebrow">Part One &middot; outlet two</div>
<h2><em>Stalled</em></h2>
<p class="lede">The number moved less than a step, either way. This is the outlet that earns
the book &mdash; the one that would otherwise read as &ldquo;early days&rdquo; for another
two months.</p>
<div class="g46">
  {K.capt("k2-stalled", 154, "Four readings that go nowhere. Without a fixed point to read them at, this shape is invisible from inside the work.")}
  <div class="stack">
    <div><h3>What it is not</h3>
    <p>Not a verdict on the client, and not a signal to work harder at the same thing. A
    stall almost always means a step was too large, a foundation was skipped, or the arc is
    treating something the client did not come for.</p></div>
    <div><h3>What you do: take the named branch</h3>
    <p>Every checkpoint in Part Two names one session to go to &mdash; not advice, a session
    number. At {sid(n)} in {WA["short"]}, a stalled reading goes to {sid(cp["stalled"])}
    &ldquo;{t(cp["stalled"])}&rdquo;, the session that arc already holds for a ladder that
    has stopped moving.</p></div>
    <div class="card tint"><h3>Then read again, in the same place</h3>
    <p class="micro">Take the branch, and take the next reading at the next scheduled
    checkpoint &mdash; not sooner. Reading again in two weeks to see whether the branch
    worked turns the measure into a mood thermometer.</p></div>
  </div>
</div>
<div><h3>Four reasons a number stops moving</h3>
{K.table(["What happened", "What it looks like", "What to do about it"], [
  ["<b>The step was too big</b>", "They can describe the task and have not attempted it, or tried once and stopped.",
   "Halve it. The commonest cause by some distance."],
  ["<b>A foundation is missing</b>", "The exercise needs a skill from earlier in the arc that never quite landed.",
   "Usually where the branch goes. One session to re-teach, six saved."],
  ["<b>It is the wrong problem</b>", "Compliant, pleasant, and somewhere else. Homework done, nothing changes.",
   "Ask the question in the script on page " + str(K.pg("p_words")) + "."],
  ["<b>The item is wrong</b>", "The work is plainly going well and only the number is flat.",
   "Rewrite it, and note on the chart that you did."],
])}</div>
<div><h3>Two stalls in a row</h3>
<p>A second stalled reading straight after taking the branch means the arc is not the problem
the client has. Go back to the formulation &mdash; and if they arrived with more than one
problem, Companion 01 decides which arc should have gone first.</p></div>
"""


def p_worse():
    return f"""
<div class="eyebrow">Part One &middot; outlet three</div>
<h2><em>Worse</em></h2>
<p class="lede">The reading moved away from the goal by a step or more. The arc stops being
the plan, today, in this session.</p>
<div class="g55">
  <div class="stack">
    <div><h3>What you do</h3>
    <p>Stop planning the arc and open <b>B8 &middot; Pause &amp; Refer</b>. That page decides
    what happens next &mdash; a referral, a medical review, a change in level of care, or a
    conversation that ends with the same arc resuming next week. All this book decides is
    that B8 gets opened.</p></div>
    <div class="card rust"><h3>Never branch inside the arc on a worse reading</h3>
    <p class="micro">Not once in the fifty checkpoints does a deteriorating reading send the
    client to another session of the same arc. A client getting worse inside a plan does not
    need a different part of that plan.</p></div>
    <div><h3>One reading, not a trend</h3>
    <p>You do not wait for two. A single step in the wrong direction is enough, because the
    cost of opening B8 unnecessarily is a conversation, and the cost of waiting is a month.</p></div>
    <div class="card line"><p class="micro"><b>Worse is not the same as distressed.</b> A
    client can have a terrible fortnight and read on track. The outlet follows the number,
    and where the number and the room disagree, you open B8 and say so there.</p></div>
  </div>
  {K.capt("k3-worse", 168, "A line moving the wrong way. One step is enough; there is nothing to be gained by confirming it.")}
</div>
<div class="scope r"><h3>Three things that skip the rule entirely</h3>
<p>These are not checkpoint outcomes and they are not weighed against a step. If any of them
appears &mdash; at a checkpoint or at any other moment &mdash; the measuring stops there and
your local protocol starts.</p>
<ul class="ticks">
  <li><span><b>Any indication of suicidal thinking or self-harm.</b> Including a non-zero
  answer to item 9 of the PHQ-9, which is why that item is handled on page
  {K.pg("p_phq")} and not counted here.</span></li>
  <li><span><b>A disclosure of abuse</b>, current or historical, that carries a reporting
  duty where you practice.</span></li>
  <li><span><b>Current violence</b>, to the client or by them.</span></li>
</ul>
<p class="micro">A checkpoint is a question about whether a treatment is working. None of
these three is that question, and no number on a chart changes what you do about them.</p>
</div>
"""


NAMED = ("PHQ-9", "GAD-7", "PCL-5")
WORDS = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
         6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
         11: "Eleven", 12: "Twelve"}


def _by_measure():
    """(arcs with a reproducible instrument, with a diary, on the goal item
    alone, inheriting whatever ran through treatment). Counted rather than
    typed: the sentence on the page said four when it was three."""
    inst, diary, goal, inherit = [], [], [], []
    for a in A.ARCS:
        ms = C.measures(a["key"])
        if any(m in NAMED for m in ms):
            inst.append(a)
        elif "Sleep diary" in ms:
            diary.append(a)
        elif "Treatment scale" in ms:
            inherit.append(a)
        else:
            goal.append(a)
    return inst, diary, goal, inherit


def p_choose():
    inst, diary, goal, inherit = _by_measure()
    rows = []
    for name in ("PHQ-9", "GAD-7", "PCL-5", "Sleep diary", "Goal scale"):
        m = C.MEASURE[name]
        who = sorted({a["short"] for a in A.ARCS if name in C.measures(a["key"])})
        # Naming all ten arcs here spilled the page; the count and the rule are
        # what a reader needs, and the arcs are listed in the contents anyway.
        where = ", ".join(who) if len(who) <= 2 else \
            "the other %s arcs, and beside the instrument in every arc" % WORDS[len(goal)].lower()
        rows.append([f"<b>{name}</b>", m["what"],
                     "%d&ndash;%d" % m["range"] if m["range"][1] else "&mdash;",
                     str(m["step"]) if m["step"] else "&mdash;", where])
    return f"""
<div class="eyebrow">Part One &middot; the measure</div>
<h2>Choosing <em>what to read</em></h2>
<p class="lede">Three questions, in this order. Most arcs stop at the third, and that is no
compromise: an item written from the goal of the sessions around it often tracks the work
better than a general severity scale.</p>
<div class="g55">
  <div class="stack">
    {K.steps([
        "<b>Is there an instrument that fits, and may lawfully be reproduced?</b> %s arcs &mdash; %s. Use it, and the goal scale beside it."
        % (WORDS[len(inst)], ", ".join(x["short"] for x in inst)),
        "<b>Does the arc already collect a number?</b> %s does: the diary from %s gives sleep efficiency, and the client is keeping it anyway."
        % (diary[0]["short"], sid(diary[0]["start"] + 1)),
        "<b>Otherwise, the goal scale alone.</b> %s arcs run on it, and it is the only measure every arc has. Page %s writes one."
        % (WORDS[len(goal)], K.pg("p_goal")),
    ])}

    <div class="card ochre"><h3>Never substitute a scale you have not licensed</h3>
    <p class="micro">The obvious instruments for insomnia, compulsions, grief and emotion
    regulation are in copyright, and a research permission is not a permission to print &mdash;
    page {K.pg("p_licence")} takes them one at a time. The fifteenth arc,
    {inherit[0]["short"]}, keeps whatever ran through treatment.</p></div>
  </div>
  {K.capt("m1-choose", 176, "A long instrument and a single-item card. For most arcs the card is the lawful choice, and often the better one.")}
</div>
<div>{K.table(["Measure", "What it reads", "Range", "Step", "Arcs that use it"], rows)}</div>
"""


def p_goal():
    n = WS[0][1]
    cp = A.CHECKPOINT[n]
    return f"""
<div class="eyebrow">Part One &middot; the measure</div>
<h2>Writing a <em>goal scale</em></h2>
<p class="lede">A single item, anchored at both ends, that asks about the last week. It takes
about ninety seconds to write and it is the only measure in this book that carries no
license question at all, because you wrote it.</p>
<figure class="figbox"><div class="figw">{G.goalbar()}</div>
<figcaption><b>Always this way up</b>Ten is the goal, on every scale in this book, in every
arc. Written the other way round the chart falls as the client improves, and every
reader &mdash; you, the client, a colleague covering for you &mdash; has to remember which
of the fifteen arcs is the exception. None of them is.</figcaption></figure>
<div class="g55">
  <div class="stack">
    <h3>Four steps</h3>
    {K.steps([
        "<b>Take the goal from the sessions, not from the diagnosis.</b> Ask about the behavior this stretch of the arc is working on &mdash; either what the sessions just taught, or the target the next ones are about to. Where it is the second, the first reading is simply the baseline for that behavior, and says nothing about the client.",
        "<b>Ask about behavior where you can.</b> &ldquo;How often did you&hellip;&rdquo; beats &ldquo;how anxious were you&hellip;&rdquo;, because the client can count the first and has to estimate the second.",
        "<b>Anchor both ends in words.</b> Not just 0 and 10 &mdash; say what 0 is and what 10 is. An unanchored scale drifts a point a month.",
        "<b>Fix the window: the last week.</b> Not &ldquo;lately&rdquo;, not &ldquo;in general&rdquo;. The window is what makes two readings comparable.",
    ])}
  </div>
  <div class="stack">
    <div class="card sage"><div class="eyebrow">Worked, at {sid(n)}</div>
    <p class="quote sm">&ldquo;{cp["goal"]}&rdquo;</p>
    <p class="micro" style="margin-top:7px">Behavior, not feeling. A week-long window. Both
    ends anchored. It asks about approach &mdash; the thing this whole arc is for &mdash;
    rather than about how anxious he felt, which the GAD-7 beside it already covers. The
    same item is read again at {", ".join(sid(x) for x in A.checkpoints(W)[1:])}, so the
    four readings are comparable with one another.</p></div>
    <div class="card"><h3>Three that will not work</h3>
    <ul class="ticks">
      <li><span><i>&ldquo;How has your week been, 0 to 10?&rdquo;</i> &mdash; reads mood,
      and mood is what you already had.</span></li>
      <li><span><i>&ldquo;How anxious are you right now?&rdquo;</i> &mdash; no window, and
      it reads your room rather than their week.</span></li>
      <li><span><i>&ldquo;How much progress have you made?&rdquo;</i> &mdash; asks the
      client to grade you, and they will be kind.</span></li>
    </ul></div>
  </div>
</div>
<div class="g2">
  <p class="micro"><b>The two-point step is a working convention of this book, not a
  psychometric statistic.</b> It is set there because a one-point move on a single-item
  scale is within the noise of asking the same person twice, and because two points is a
  distance a client can recognize in their own week. Where an arc has an instrument, the
  instrument&rsquo;s own published step governs.</p>
  <p class="micro"><b>Two more, written the same way.</b>
  {A.BY_KEY["SLP"]["short"]}, {sid(A.checkpoints("SLP")[1])}:
  &ldquo;{A.CHECKPOINT[A.checkpoints("SLP")[1]]["goal"]}&rdquo;
  &nbsp;&middot;&nbsp; {A.BY_KEY["GRF"]["short"]}, {sid(A.checkpoints("GRF")[0])}:
  &ldquo;{A.CHECKPOINT[A.checkpoints("GRF")[0]]["goal"]}&rdquo; Both count something;
  neither asks the client to grade their progress.</p>
</div>
"""


def p_licence():
    # "l1-licence" is a slug, not prose. The US-spelling pass rewrote it to
    # "l1-license" once and silently detached this page from its picture;
    # inventory.py now fails on a picture named with no file behind it.
    rows = []
    for name in ("PHQ-9", "GAD-7", "PCL-5", "Sleep diary", "Goal scale"):
        m = C.MEASURE[name]
        where = {"PHQ-9": "p_phq", "GAD-7": "p_gad"}.get(name, "p_goal")
        cells = [m["license"], m["source"]]
        cells = [c % K.pg(where) if "%s" in c else c for c in cells]
        rows.append([f"<b>{name}</b>"] + cells)
    return f"""
<div class="eyebrow">Part One &middot; before you copy anything</div>
<h2>What you may <em>reproduce</em></h2>
<p class="lede">This matters more than it looks. Photocopying an instrument for your own
caseload and printing one inside a product you sell are different acts, and several of the
scales a therapist would reach for first do not permit the second.</p>
<div class="g46">
  {K.capt("l1-licence", 150, "Five instruments, five different answers to the same question.")}
  <div class="stack">
    <div class="card sage"><h3>Printed in this book</h3><p class="micro">The PHQ-9 and the
    GAD-7, in full, because both carry an explicit statement that no permission is required
    to reproduce them. The PCL-5 is public domain but too long to set here, so it is named
    and sourced instead.</p></div>
    <div class="card rust"><h3>Named, never printed</h3><p class="micro">Instruments for
    insomnia severity, obsessive&ndash;compulsive symptoms, prolonged grief, emotion
    regulation and burnout are in copyright and are licensed individually &mdash; commonly
    free for research and not free for commercial redistribution. Where you hold a license,
    use them and read them with the step their own literature gives.</p></div>
  </div>
</div>
<div>{K.table(["Measure", "What you may do with it", "Where it comes from"], rows)}</div>
<div class="scope"><p class="micro"><b>Check before you rely on this.</b> License terms
change, and they differ by country and by translation. The statements above were correct for
the English originals at the time of writing; the publisher&rsquo;s own page is the
authority, not this one.</p></div>
"""


PHQ_ITEMS = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself &mdash; or that you are a failure or have let yourself "
    "or your family down",
    "Trouble concentrating on things, such as reading the newspaper or watching television",
    "Moving or speaking so slowly that other people could have noticed? Or the opposite "
    "&mdash; being so fidgety or restless that you have been moving around a lot more "
    "than usual",
    "Thoughts that you would be better off dead, or of hurting yourself in some way",
]

GAD_ITEMS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid, as if something awful might happen",
]


def _form(title, stem, items, risk=None):
    lis = "".join('<li%s>%s</li>' % (' class="risk"' if i == risk else "", x)
                  for i, x in enumerate(items, 1))
    return f"""<div class="form">
<div class="fh"><span>{title}</span><span>Over the last 2 weeks, how often have you been
bothered by the following?</span></div>
<ol>{lis}</ol>
<div class="ff">{stem}</div></div>"""


def p_phq():
    m = C.MEASURE["PHQ-9"]
    bands = "".join(f"<div><b>{lo}&ndash;{hi}</b> {nm}</div>" for lo, hi, nm in m["bands"])
    return f"""
<div class="eyebrow">Part One &middot; the instruments</div>
<h2>The <em>PHQ-9</em></h2>
<div class="g55">
  <div class="stack">
    {_form("PHQ-9", "Not at all 0 &middot; Several days 1 &middot; More than half the days 2 "
                    "&middot; Nearly every day 3. Add the nine answers: the total runs 0&ndash;27.",
           PHQ_ITEMS, risk=9)}
    <p class="micro">{m["source"]} Reproduced under the statement the instrument itself
    carries: no permission is required to reproduce, translate, display or distribute it.</p>
  </div>
  <div class="stack">
    <div class="card rust"><h3>Item 9 leaves this book</h3>
    <p>The ninth item asks about thoughts of being dead or of self-harm. <b>Any answer above
    zero stops the checkpoint.</b> You do not finish scoring, you do not compare it with last
    time, and you do not decide anything about the arc. Go to B8 and to your local risk
    protocol, in the session you are in.</p>
    <p class="micro" style="margin-top:6px">This is why the arithmetic in this book never
    includes item 9 as part of a trend. A number that can contain a disclosure is not a
    number you average.</p></div>
    <div><h3>Bands</h3><div class="figw">{G.bandbar("PHQ-9")}</div>
    <div class="micro" style="display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;margin-top:7px">{bands}</div></div>
    <div class="card tint"><h3>The step: {m["step"]} points</h3><p class="micro">Five points
    is the change commonly treated as clinically meaningful for this instrument. It is a
    published convention rather than a law, and it is larger than most therapists expect.</p></div>
    {K.capt("q1-phq", 120, "Nine items, four boxes each. Two minutes, and the client fills it in.")}
  </div>
</div>
"""


def p_gad():
    m = C.MEASURE["GAD-7"]
    bands = "".join(f"<div><b>{lo}&ndash;{hi}</b> {nm}</div>" for lo, hi, nm in m["bands"])
    return f"""
<div class="eyebrow">Part One &middot; the instruments</div>
<h2>The <em>GAD-7</em></h2>
<div class="g55">
  <div class="stack">
    {_form("GAD-7", "Not at all 0 &middot; Several days 1 &middot; More than half the days 2 "
                    "&middot; Nearly every day 3. Add the seven answers: the total runs 0&ndash;21.",
           GAD_ITEMS)}
    <p class="micro">{m["source"]} Carries the same no-permission statement as the PHQ-9.</p>
    <div><h3>Bands</h3><div class="figw">{G.bandbar("GAD-7")}</div>
    <div class="micro" style="display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;margin-top:7px">{bands}</div></div>
  </div>
  <div class="stack">
    {K.capt("q2-gad", 138, "Two items shorter than the PHQ-9, and a different step. They are not interchangeable.")}
    <div class="card tint"><h3>The step: {m["step"]} points</h3><p class="micro">Four points
    is the figure commonly used for this instrument. Note that it is not the same as the
    PHQ-9&rsquo;s five &mdash; the two scales are different lengths, and a therapist running
    both on one client will get them confused exactly once.</p></div>
    <div class="card ochre"><h3>No risk item, and that is not reassurance</h3>
    <p class="micro">The GAD-7 contains nothing like item 9. It therefore tells you nothing
    about risk, and a falling GAD-7 is not evidence that a client is safe. Risk is asked
    about on its own terms or not at all.</p></div>
    <div class="card"><h3>Where it is used here</h3><p class="micro">All four checkpoints of
    {A.BY_KEY["ANX"]["name"]}: {", ".join(sid(n) for n in A.checkpoints("ANX"))}, alongside
    the goal item at each one.</p></div>
  </div>
</div>
<div class="g55">
  <div><h3>Scoring, worked</h3>
  <p>A client answers <i>several days</i> to the first three items, <i>more than half the
  days</i> to the fourth and the sixth, and <i>not at all</i> to the fifth and seventh. That
  is 1+1+1+2+0+2+0 = <b>7</b>, which is the mild band. At the next checkpoint the same client
  scores 4. Seven to four is three points &mdash; <b>less than the step of
  {m["step"]}</b> &mdash; so on this instrument the reading has not moved, whatever the band
  underneath it now says.</p>
  <p class="micro" style="margin-top:6px">Crossing a band boundary is not the test. Bands
  describe severity; the step describes change, and it is the step this book reads.</p></div>
  <div class="card tint"><h3>Running both instruments on one client</h3>
  <p class="micro">Where anxiety and low mood run together &mdash; which is the ordinary
  case rather than the complicated one &mdash; you may be reading a PHQ-9 and a GAD-7 at
  different checkpoints in different arcs. Two rules keep it straight. Give each instrument
  its own sheet, never one line for both. And read each against its own step: five points on
  the PHQ-9, four on the GAD-7, two on the goal scale.</p>
  <p class="micro" style="margin-top:6px">Companion 01 is the book for deciding which of the
  two arcs runs first; this one only says what to read once it is running.</p></div>
</div>
"""


def p_run():
    return f"""
<div class="eyebrow">Part One &middot; in the room</div>
<h2>Running a checkpoint, <em>step by step</em></h2>
<p class="lede">About three minutes, at the start of the session rather than the end. At the
end you will run out of time on exactly the weeks the reading matters most.</p>
{K.seq([
    ("r1-hand", "Hand it over", "Say what it is before you hand it across: &ldquo;the same question I ask every few weeks.&rdquo; Surprise depresses scores."),
    ("r2-mark", "Let them mark it", "They make the mark, not you. A number you say out loud for a client to agree with is your number."),
    ("r3-plot", "Plot it in front of them", "On the same sheet as last time. This is the step most often skipped and the one the client remembers."),
    ("r4-compare", "Compare with last time", "Out loud, both of you looking at it. One step or more? Which way?"),
    ("r5-decide", "Take the outlet", "On track, stalled, worse. Decide it now, at the sheet, before the session moves on and the moment passes."),
])}
<div class="g64">
  <div class="card tint"><h3>What makes it take twenty minutes instead of three</h3>
  <p class="micro">Explaining the scale from scratch each time, because it was never written
  down; asking at the end of a session that overran; and turning a stalled reading into an
  immediate review of the whole treatment. The first two are fixed by the chart sheet on
  page {K.pg("p_sheet1")}. The third is fixed by taking the branch and reading again at the
  next checkpoint, not sooner.</p></div>
  <div class="card line"><p class="micro">If the client did not bring the diary, or cannot
  answer, that is a reading of its own kind &mdash; write &ldquo;not taken&rdquo; on the
  chart rather than leaving a gap. A gap looks like an oversight later. &ldquo;Not
  taken&rdquo; looks like what it was.</p></div>
</div>
"""


def p_script():
    # The script is the first checkpoint of the worked example arc, with the
    # case's own readings in it, so the conversation on this page and the chart
    # in Part Two are the same event rather than two inventions.
    _b1 = C.CASE[W][1]
    _o1, _n1, _r1, _v1, _w1 = C.case(W)[2][0]
    _d1 = _r1 - _b1
    # spoken dialogue, so the readings are set as words, not digits
    _b1, _r1, _d1 = (WORDS[x].lower() for x in (_b1, _r1, _d1))
    return f"""
<div class="eyebrow">Part One &middot; in the room</div>
<h2>The <em>three-minute</em> review script</h2>
<p class="lede">Word for word, for the on-track reading. It is short on purpose: the point of
a good reading is to stop talking about the measuring and get on with the session.</p>
<div class="g55">
  <div class="stack">
    <div class="says">
      <div><span class="who">You</span><q>Before we start &mdash; the same question as last
      time. {A.CHECKPOINT[_n1]["goal"]}</q></div>
      <div><span class="who">Client</span><q>Maybe a {_r1}?</q></div>
      <div><span class="who">You</span><q>Put it on here for me.</q></div>
      <div><span class="who">You</span><q>Last time it was a {_b1}. That is {_d1} points,
      which is the amount we agreed would count as a real change rather than a good
      week.</q></div>
      <div><span class="who">Client</span><q>It does not feel like much.</q></div>
      <div><span class="who">You</span><q>It often does not, from inside it. That is most of
      why we write it down &mdash; so that in six weeks you are not relying on how today
      feels. What do you think moved it?</q></div>
      <div><span class="who">You</span><q>Good. Same question next time we get to one of
      these, and in the meantime we carry on as planned.</q></div>
    </div>
  </div>
  <div class="stack">
    {K.capt("t1-script", 152, "The sheet stays between the two of you. A reading taken on your side of the desk is a test; on the table it is a shared instrument.")}
    <div class="card sage"><h3>The four moves under the script</h3>
    <ul class="ticks">
      <li><span>Ask the same question, in the same words, every time.</span></li>
      <li><span>Give the comparison, not just the number.</span></li>
      <li><span>Say what counts as real, so the client is not guessing at your standard.</span></li>
      <li><span>Hand the meaning back: <i>what do you think moved it?</i></span></li>
    </ul></div>
  </div>
</div>
<div class="g3">
  <div class="card"><h3>On video</h3><p class="micro">The client cannot mark your sheet, so
  ask for the number out loud and plot it yourself where they can see it &mdash; hold the
  sheet to the camera, or share the screen. The plotting is the part that makes it shared;
  do not drop it because the room is not a room.</p></div>
  <div class="card"><h3>&ldquo;What is this for?&rdquo;</h3><p class="micro">Answer plainly
  and briefly: <i>&ldquo;so that neither of us has to go on memory about whether this is
  helping.&rdquo;</i> Clients almost never object to being measured. They object to being
  measured without being told why, which is a different thing.</p></div>
  <div class="card"><h3>&ldquo;It depends on the day.&rdquo;</h3><p class="micro">It does.
  Say so, and ask for the week rather than the day: <i>&ldquo;take the whole week and give
  me one number for it.&rdquo;</i> The averaging is the client&rsquo;s to do, and their
  average is the reading.</p></div>
</div>
<p class="micro"><b>One thing not to say:</b> &ldquo;that is great.&rdquo; It teaches the
client that a particular answer pleases you, and from then on you are measuring the alliance
rather than the treatment.</p>
"""


def p_words():
    return f"""
<div class="eyebrow">Part One &middot; in the room</div>
<h2>When it is <em>not</em> good news</h2>
<p class="lede">Both go better when the client already knows the rule. Say at the first
checkpoint that numbers sometimes stall and that there is a plan for it.</p>
<div class="g2">
  <div class="card ochre"><div class="eyebrow">A stalled reading</div>
  <div class="says">
    <div><span class="who">You</span><q>That is a five, and last time it was a four. That is
    less than the two points we said would count, so on paper this has not moved.</q></div>
    <div><span class="who">Client</span><q>So I have wasted six weeks.</q></div>
    <div><span class="who">You</span><q>No &mdash; it means we have learned that this part
    is not the part that shifts it. There is a specific place to go back to, and that is
    what I want us to do next.</q></div>
    <div><span class="who">You</span><q>Can I ask you something first: is this the problem
    you most want to be working on?</q></div>
  </div></div>
  <div class="card rust"><div class="eyebrow">A reading that got worse</div>
  <div class="says">
    <div><span class="who">You</span><q>This has gone the other way, by enough that I do not
    want to carry on with the plan.</q></div>
    <div><span class="who">You</span><q>I would rather stop and look at the whole picture
    with you than push on and find out in a month. Can we use today for that?</q></div>
    <div><span class="who">Client</span><q>Is that bad?</q></div>
    <div><span class="who">You</span><q>It is information. It is the reason we have been
    writing it down.</q></div>
  </div></div>
</div>
<div class="g46">
  {K.capt("t2-words", 128, "Both scripts are short. A stalled number does not need a long explanation; it needs a decision and the next session.")}
  <div class="stack">
    <div><h3>The question inside the stalled script</h3>
    <p>&ldquo;Is this the problem you most want to be working on?&rdquo; is doing real work.
    A stall is the commonest place to find that the arc is treating what you formulated
    rather than what they came for. Ask it plainly, once, and be ready for the answer.</p></div>
    <div class="card line"><p class="micro">Neither script explains the scale again, and
    neither apologizes for it. The measuring is ordinary; treating it as an intrusion is what
    makes it one.</p></div>
    <div><h3>Three answers to have ready</h3>
    <ul class="ticks">
      <li><span><i>&ldquo;So this is not working.&rdquo;</i> &mdash; &ldquo;It means this
      part is not what shifts it. That is worth knowing in six weeks rather than six
      months.&rdquo;</span></li>
      <li><span><i>&ldquo;Are you giving up on me?&rdquo;</i> &mdash; on a worse reading,
      answer it before it is asked: say plainly that you are not ending anything today, you
      are looking at the whole picture.</span></li>
      <li><span><i>&ldquo;Can we just keep going?&rdquo;</i> &mdash; on a stall, yes: the
      branch is still the arc. On a worse reading, no, because you do not yet know what you
      would be carrying on with.</span></li>
    </ul></div>
  </div>
</div>
"""


def p_chart():
    return f"""
<div class="eyebrow">Part One &middot; the record</div>
<h2><em>Plotting</em> it</h2>
<p class="lede">One sheet per client, kept with the file, filled in with the client watching.
Three readings on a page do something no note can: they make a direction visible to the
person it belongs to.</p>
<div class="g55">
  {K.capt("p1-chart", 164, "The next column, marked before the reading is taken. Plotting in front of the client is the step that turns a form into a shared record.")}
  <div class="stack">
    {K.legend([
        ("One sheet, one measure.&nbsp;", "If the arc reads an instrument as well as the goal scale, use two sheets or two colors, and never one line for both."),
        ("Baseline is a column.&nbsp;", "It is not a checkpoint, and it does not get a verdict &mdash; but every first comparison is made against it."),
        ("Write the session number, not the date.&nbsp;", "A client who missed a month should see the reading in the right place in the work, not in the right place in the calendar."),
        ("Note the events.&nbsp;", "A break-up, a bereavement, a new medication, a holiday. Six weeks later the line will not tell you and you will not remember."),
        ("Mark &ldquo;not taken&rdquo;.&nbsp;", "Never leave a gap. A gap reads as an oversight, and an oversight invites a guess."),
    ], cols=1)}
  </div>
</div>
<div class="g2">
  <figure class="figbox bare"><div class="figw">{G.chart("VAL", w=220, h=88)}</div>
  <figcaption><b>Three readings, all on track</b>Dots take the color of the verdict, which
  is read off the comparison with the dot before, never off the height of the line.</figcaption></figure>
  <figure class="figbox bare"><div class="figw">{G.chart("DEP", w=220, h=88)}</div>
  <figcaption><b>The same sheet, a case that stopped</b>The fourth column has no reading
  because the third one opened B8. An arc that has been paused does not get read again for
  the sake of a complete row.</figcaption></figure>
</div>
<div class="g3">
  <div class="card tint"><h3>Where it lives</h3><p class="micro">With the file, not inside
  it. The sheet is working paper that comes out at the start of a checkpoint session and goes
  back afterward; what belongs in the clinical record goes into the record, under your own
  documentation policy.</p></div>
  <div class="card tint"><h3>Who else sees it</h3><p class="micro">Say at the first
  checkpoint who will see the figure &mdash; you, the client, and anyone the client&rsquo;s
  care or funding involves. A client who finds out later that a payer reads it will give you
  different numbers from then on.</p></div>
  <div class="card tint"><h3>If the client wants a copy</h3><p class="micro">Give them one.
  It is a record of their own work, it costs a photocopy, and the clients who ask are
  generally the ones for whom seeing the line does the most.</p></div>
</div>
"""


def p_lies():
    return f"""
<div class="eyebrow">Part One &middot; the record</div>
<h2>Charts that <em>mislead</em></h2>
<p class="lede">Three shapes that are true readings and false conclusions. All three are
common, and the first is common enough to be worth watching for by name.</p>
<div class="g3">
  <div class="card"><div class="figw">{G.artifact("spike")}</div>
  <h3 style="margin-top:8px">The one bad week</h3>
  <p class="micro">A single reading far off the line, taken the week of a funeral, a
  deadline, a flu. Treated as a trend it triggers a branch the client did not need. Read it
  against the note of what the week held &mdash; and if there is no note, this is what the
  notes are for.</p></div>
  <div class="card"><div class="figw">{G.artifact("ceiling")}</div>
  <h3 style="margin-top:8px">The ceiling</h3>
  <p class="micro">A client at nine on a ten-point scale cannot produce another two-point
  move, so a rule that only asks &ldquo;did it move?&rdquo; reads success as a stall. This
  is the one the book fixes for you, on page {K.pg("p_ontrack")}: holding inside the target
  band is on track.</p></div>
  <div class="card"><div class="figw">{G.artifact("sawtooth")}</div>
  <h3 style="margin-top:8px">The sawtooth</h3>
  <p class="micro">Up, down, up, down, by exactly a step each time. Usually the item is
  reading something that swings weekly &mdash; sleep, a shift pattern, contact with one
  particular person &mdash; rather than the thing the arc is treating. Rewrite the item
  rather than branching.</p></div>
</div>
<div class="g46">
  {K.capt("p2-lies", 132, "One spike in an otherwise steady line. The question is not what the number says but what the week contained.")}
  <div class="stack">
    <div><h3>Two more, without pictures</h3>
    <p><b>The obliging client.</b> Scores climb steadily and nothing in the sessions matches
    them. Ask for an example from the week rather than a number, and see whether the example
    is the same size as the score.</p>
    <p style="margin-top:8px"><b>The first reading that was never a baseline.</b> A client at
    their worst on the day they came will improve on almost any measure. The first move is
    partly the treatment and partly the return from a bad day, and neither you nor the chart
    can separate them. It is the second and third comparisons that carry the weight.</p></div>
    <div class="card line"><p class="micro">None of these is a reason to stop measuring. They
    are reasons to read the chart beside the notes, which takes a further thirty seconds and
    is the difference between a measure and a ritual.</p></div>
    <div class="card ochre"><h3>The test that settles most of them</h3>
    <p class="micro">Ask for one concrete thing from the week that the number refers to. A
    reading that can produce an example is usually sound; a reading that cannot is measuring
    the client&rsquo;s impression of themselves, which moves for its own reasons.</p></div>
  </div>
</div>
"""


def p_short():
    rows = [[f'<b>{a["short"]}</b>', len(a["sessions"]), len(A.checkpoints(a["key"])),
             ", ".join(sid(n) for n in C.short_course(a["key"]))]
            for a in A.ARCS if len(A.checkpoints(a["key"])) == 4]
    return f"""
<div class="eyebrow">Part One &middot; fewer sessions</div>
<h2><em>Short</em> courses</h2>
<p class="lede">Session caps are the ordinary case, not the exception: an assistance
program allots six or eight, an insurer authorizes a block, a client can afford ten. The
schedule in Part Two assumes the whole arc. Here is what to keep when you do not have it.</p>
<div class="g55">
  <div class="stack">
    <div class="card sage"><h3>The rule: first, middle, last</h3>
    <p>Keep the arc&rsquo;s first checkpoint, its last, and whichever of the inner ones sits
    closest to the middle. Three readings give you two comparisons, and two comparisons is
    the fewest that can show a direction rather than a position.</p></div>
    <div><h3>Below three readings</h3>
    <p>With room for only two, take them at the first checkpoint and the last session you
    expect to have. You will get one comparison and no trend, and the honest thing is to say
    so in the note. With room for one, do not pretend: take a baseline, use it in the summary
    and the referral, and do not draw a line between a point and nothing.</p></div>
    <div class="card ochre"><h3>What does not change</h3>
    <p class="micro">The three outlets, the steps, and the branch each stall points at. A
    short course changes how often you read, never what a reading means.</p></div>
  </div>
  <div class="stack">
    {K.capt("s1-short", 140, "Three marks: the first, the middle and the last. The fewest that can show a direction.")}
    <figure class="figbox tint"><div class="figw">{G.shortfig(W)}</div>
    <figcaption><b>{WA["short"]}, full and short</b>The upper row is the arc&rsquo;s four
    checkpoints, the lower the three a short course keeps.</figcaption></figure>
  </div>
</div>
<div>{K.table(["Arc", "Sessions", "Checkpoints", "Keep, on a short course"], rows)}
<p class="micro" style="margin-top:6px">The ten arcs with three checkpoints already are the
short course, and keep all three.</p></div>
"""


def p_note():
    return f"""
<div class="eyebrow">Part One &middot; afterwards</div>
<h2>The checkpoint and <em>the note</em></h2>
<p class="lede">The reading is the most quotable thing that happened in the session, which is
exactly why it needs a rule. B5 shapes the note; this page says what the checkpoint
contributes to it.</p>
<div class="g55">
  <div class="stack">
    <div class="card sage"><h3>Worth writing</h3>
    <ul class="ticks">
      <li><span>The measure, the number, and the number before it.</span></li>
      <li><span>Which outlet you took, in plain words.</span></li>
      <li><span>The session you branched to, if you branched.</span></li>
      <li><span>Anything in the week that would explain the reading.</span></li>
      <li><span>That the client saw it plotted.</span></li>
    </ul></div>
    <div class="card rust"><h3>Not worth writing, or not yours to write</h3>
    <ul class="ticks">
      <li><span>An interpretation the number will not carry &mdash; &ldquo;significant
      improvement&rdquo; from a two-point move on one item.</span></li>
      <li><span>A severity band as though it were a diagnosis. These instruments screen and
      monitor; they do not diagnose, and a note that treats a band as a label will be read
      later as though it did.</span></li>
      <li><span>A risk item&rsquo;s content buried in a progress figure. That belongs in the
      risk record, under your protocol, not in a trend.</span></li>
    </ul></div>
  </div>
  <div class="stack">
    {K.capt("n1-note", 150, "The reading is the easiest thing in the session to write down and the easiest to overclaim.")}
    <div class="card tint"><h3>One sentence that does the whole job</h3>
    <p class="quote sm" style="font-size:13.4px">&ldquo;Goal item 6, up from 4 at the
    previous checkpoint; a two-point move, which meets the threshold agreed at the outset.
    Plan unchanged, next reading at the next scheduled checkpoint.&rdquo;</p>
    <p class="micro" style="margin-top:6px">It says the measure, the comparison, the
    threshold, the decision and the next step, and it claims nothing the number cannot
    support.</p></div>
  </div>
</div>
<div class="g2">
  <div class="card rust"><div class="eyebrow">Overclaimed</div>
  <p class="quote sm" style="font-size:13px">&ldquo;Client reports significant improvement
  in anxiety. GAD-7 now in the mild range, indicating good response to treatment.&rdquo;</p>
  <p class="micro" style="margin-top:6px">Three claims the reading will not carry:
  <b>significant</b> (a word with a technical meaning it is not being used in),
  <b>indicating</b> (the instrument indicates severity, not response), and
  <b>to treatment</b> (nothing here separates the treatment from the month).</p></div>
  <div class="card sage"><div class="eyebrow">The same session, written straight</div>
  <p class="quote sm" style="font-size:13px">&ldquo;GAD-7 9, down from 14 at the previous
  checkpoint &mdash; a five-point fall, above the four-point threshold agreed at the outset.
  Goal item 6, up from 4. Plan unchanged.&rdquo;</p>
  <p class="micro" style="margin-top:6px">Shorter, and every word of it survives being read
  back to you in a year by someone who was not there.</p></div>
</div>
"""


def p_stop():
    return f"""
<div class="eyebrow">Part One &middot; afterwards</div>
<h2>When measuring is the <em>wrong move</em></h2>
<p class="lede">A book that sells checkpoints has an obvious interest in telling you to take
them all. Here are the four times not to.</p>
<div class="stack">
  <div class="card line"><h3>1 &middot; When something is happening</h3>
  <p>A client who arrives in the middle of a crisis, a disclosure, or a loss does not get
  handed a scale. Write &ldquo;not taken&rdquo;, deal with what is in the room, and pick the
  reading up at the next checkpoint. A session taken over from outside is a different problem
  from a treatment that is not working, and this book is only about the second.</p></div>
  <div class="card line"><h3>2 &middot; When the instrument would be the intervention</h3>
  <p>In some arcs the act of counting changes the thing counted &mdash; urges, checking,
  intrusive thoughts. That is usually useful and occasionally not. If a client is spending
  the week monitoring symptoms because you asked for a number, the measure has become part of
  the problem, and the goal item should be rewritten to ask about behavior instead.</p></div>
  <div class="card line"><h3>3 &middot; When the number is the third party&rsquo;s</h3>
  <p>Where an employer, a court or an insurer will read the figure, the client knows it. You
  will get the number that serves them, which is not dishonesty but context. Say plainly who
  will see it, and read it knowing the answer.</p></div>
  <div class="card line"><h3>4 &middot; When you would not act on any of the three answers</h3>
  <p>If the arc would continue unchanged whatever the reading said &mdash; because there is
  no room to branch, or the course ends next week &mdash; then the reading is paperwork.
  Take a baseline and a final reading for the summary, and leave the middle alone.</p></div>
</div>
<div class="g46">
  {K.capt("b1-stop", 122, "The sheet put down, on purpose. Knowing when not to read is part of the method, not an exception to it.")}
  <div class="card ochre"><h3>The failure this page is guarding against</h3>
  <p class="micro">Measurement that has become a ritual is worse than no measurement, because
  it produces a record that looks like evidence. Fifty checkpoints exist so that you can read
  at the right moments; none of them is a reason to read at the wrong one.</p></div>
</div>
"""


def p_reading():
    ex = A.BY_KEY["SLP"]
    return f"""
<div class="eyebrow">Part One &middot; how to use Part Two</div>
<h2>Reading an <em>arc spread</em></h2>
<p class="lede">Fifteen arcs, two pages each, laid out identically. Once you have read one
you have read all of them, which is the intention: the pages you reach for mid-caseload
should not need studying.</p>
<div class="g55">
  <div class="stack">
    <div><h3>The left page &middot; the schedule</h3>
    {K.legend([
        ("The four figures.&nbsp;", "How many sessions the arc holds, how many readings it gets, where the first one falls, and how far apart they are."),
        ("The timeline.&nbsp;", "Every session in the arc as one square. Sage squares are checkpoints, ochre squares are the sessions a stall branches to, and the dashed arrow joins each pair."),
        ("A card per checkpoint.&nbsp;", "The session, the measure, the exact goal item to read aloud, and all three outlets with the session each one leads to."),
    ], cols=1)}</div>
    <div><h3>The right page &middot; one worked case</h3>
    {K.legend([
        ("The composite.&nbsp;", "Written for this book, not a case record."),
        ("The chart.&nbsp;", "Baseline and every reading, with each dot colored by its computed verdict."),
        ("Three cautions.&nbsp;", "The ways a true number can still be read wrongly in this particular arc."),
        ("The short course.&nbsp;", "Which three readings to keep when there are not enough sessions."),
    ], cols=1, start=4)}</div>
  </div>
  <div class="stack">
    {K.capt("x1-reading", 172, "Both pages of one arc. The layout does not change from arc to arc.")}
    <div class="card tint"><h3>Worth knowing before you start</h3>
    <p class="micro">Nine of the fifteen worked cases stall at least once and one deteriorates
    and leaves the book. That is not pessimism about the arcs; it is what a book of decision
    rules owes the reader. A set of cases that all ran clean would be a brochure.</p></div>
  </div>
</div>
<div class="g3">
  <div class="card tint"><h3>Mid-session, in ten seconds</h3><p class="micro">Left page, find
  the card with today&rsquo;s session number on it, read the italic question aloud. That is
  the whole of what you need in the room; everything else on the spread is for before and
  after.</p></div>
  <div class="card tint"><h3>Planning the arc</h3><p class="micro">Left page, the timeline:
  write the four session numbers into the caseload sheet on page {K.pg("p_sheet3")} as soon
  as you have chosen the arc, and you will not have to think about the schedule again.</p></div>
  <div class="card tint"><h3>When a reading surprises you</h3><p class="micro">Right page,
  the three cautions. They are the ways this particular arc&rsquo;s numbers mislead, and they
  are different for every arc &mdash; grief and anxiety go wrong in opposite
  directions.</p></div>
</div>
<p class="micro">Part Two runs in registry order, from {ex["short"]}&rsquo;s neighbors at the
start to the ending arc last, so an arc&rsquo;s spread sits where that arc sits in the main
product.</p>
"""


def p_op2():
    tot = C.totals()
    return opener("h2-arcs", "Part Two", "The fifteen arcs",
                  f"{tot['checkpoints']} checkpoints, each on a named session, each with the "
                  "measure to read and the branch to take. One worked case per arc, charted, "
                  "with the cautions that apply to its numbers and no others.",
                  [a["name"] for a in A.ARCS])


def p_op3():
    return opener("h3-sheets", "Part Three", "The sheets",
                  "Three pages to copy. The chart sheet is the one that matters: a checkpoint "
                  "that is not plotted where the client can see it is a form, and forms get "
                  "filed rather than used.",
                  ["The chart sheet &mdash; one client, one measure, one page",
                   "The goal-scale sheet &mdash; write the item in session",
                   "The caseload sheet &mdash; who is due a reading, and when",
                   "Scope, referral and sources"])


# ============================================================ part three ====
def p_sheet1():
    cols = "".join('<div class="slot"></div>' for _ in range(6))
    return f"""
<div class="eyebrow">Sheet 1 &middot; photocopy freely</div>
<h2>The <em>chart sheet</em></h2>
<div class="g73">
  <div class="stack">
    <div class="fieldset">
      <div class="field"><span>Client initials</span><i></i></div>
      <div class="field"><span>Arc</span><i></i></div>
      <div class="field"><span>Measure</span><i></i></div>
      <div class="field"><span>Step that counts</span><i></i></div>
    </div>
    {K.capt("w1-sheet", 150, "Kept with the file, not in it: the sheet the client sees.")}
  </div>
  <div class="card tint"><h3>The goal item, written out</h3>
  <div class="lines" style="--n:4"></div>
  <p class="micro" style="margin-top:8px"><b>Both ends anchored, and 10 is the goal.</b>
  Copy it from the arc page, or write your own from page {K.pg("p_goal")}.</p></div>
</div>
<div class="figbox"><div class="figw">{G.blankchart(w=300, h=104)}</div>
<figcaption><b>Plot here</b>The first column is the baseline, then one per checkpoint. Circle
or color each dot as you take the outlet, so the shape of the decision is visible at a glance
next time. The shaded band is the target.</figcaption></div>
<div class="slotrow">{cols}</div>
<div class="fieldset"><div class="field"><span>What the week held, at each reading</span><i></i></div></div>
<div class="lines" style="--n:3"></div>
"""


def p_sheet2():
    return f"""
<div class="eyebrow">Sheet 2 &middot; photocopy freely</div>
<h2>The <em>goal-scale</em> sheet</h2>
<p class="lede">For an arc with no instrument, for a presentation the fifteen arcs do not
cover, or for a client whose goal is narrower than the arc&rsquo;s. Fill it in with the
client, in the session where the goal is agreed.</p>
<div class="g64">
  <div class="stack">
    <div class="fieldset">
      <div class="field"><span>1 &middot; What do the sessions before this checkpoint teach?</span><i></i></div>
    </div>
    <div class="lines" style="--n:2"></div>
    <div class="fieldset">
      <div class="field"><span>2 &middot; What would the client be <i>doing</i> differently if it worked?</span><i></i></div>
    </div>
    <div class="lines" style="--n:2"></div>
    <div class="fieldset">
      <div class="field"><span>3 &middot; The question, asking about the last week</span><i></i></div>
    </div>
    <div class="lines" style="--n:3"></div>
    <div class="g2">
      <div class="fieldset"><div class="field"><span>0 means</span><i></i></div></div>
      <div class="fieldset"><div class="field"><span>10 means</span><i></i></div></div>
    </div>
  </div>
  <div class="stack">
    {K.capt("w2-goal", 132, "Three questions and two anchors. About ninety seconds.")}
    <div class="card sage"><h3>Check it against four tests</h3>
    <ul class="ticks">
      <li><span>Does it ask about behavior rather than feeling?</span></li>
      <li><span>Is the window the last week?</span></li>
      <li><span>Are both ends anchored in words?</span></li>
      <li><span>Is 10 the goal?</span></li>
    </ul></div>
  </div>
</div>
<div class="figbox tint"><div class="figw">{G.goalbar(w=300)}</div>
<figcaption><b>The card the client marks</b>Copy the question above the line and hand it
across. The client makes the mark.</figcaption></div>
"""


def p_sheet3():
    head = ["Client", "Arc", "Next checkpoint", "Measure", "Last reading", "Outlet taken"]
    rows = [["<i></i>"] * 6 for _ in range(9)]
    return f"""
<div class="eyebrow">Sheet 3 &middot; photocopy freely</div>
<h2>The <em>caseload</em> sheet</h2>
<p class="lede">One line per client, so that a checkpoint is never missed because the session
it belonged to happened to be a difficult one. Fill the third column in as soon as an arc is
chosen, and the sheet does the remembering.</p>
{K.table(head, rows, cls="tight")}
<div class="g2">
  <div class="card tint"><h3>How to use it in ten seconds</h3>
  <p class="micro">Before a session, run down the third column. If today&rsquo;s session
  number is the one written there, the sheet comes out at the start. That is the entire
  system, and it is the only part of this book that has to survive a bad week.</p></div>
  <div class="card"><h3>What the last column is for</h3>
  <p class="micro">Two stalls in a row on one line is the pattern hardest to see from inside
  a caseload and the most worth seeing. Writing the outlet rather than the number is what
  makes it visible at a glance.</p></div>
</div>
{K.capt("w3-caseload", 130, "One line per client. The third column is the one that does the work.")}
"""


def p_scope():
    return f"""
<div class="eyebrow">Scope</div>
<h2>What this book is <em>not</em></h2>
<div class="g2">
  <div class="scope"><h3>Not diagnosis</h3>
  <p>Every measure named here screens or monitors. None of them diagnoses, and a severity
  band is not a label. Where a formal diagnosis matters &mdash; for a referral, a report, an
  authorization &mdash; it comes from an assessment, not from a trend on a chart.</p></div>
  <div class="scope r"><h3>Not risk assessment</h3>
  <p>No checkpoint assesses risk, and no outlet here manages it. Suicidal thinking, a
  disclosure of abuse and current violence all leave this book immediately for
  <b>B8 &middot; Pause &amp; Refer</b> and your local protocol &mdash; including a non-zero
  answer to item 9 of the PHQ-9, which is never counted into a total that this book compares.</p></div>
</div>
<div class="g2">
  <div class="card"><h3>Not a substitute for supervision</h3>
  <p class="micro">The branches in Part Two are clinical decisions written as rules. Rules
  are a floor. A recently licensed clinician without regular consultation should treat a
  second stall, and every &ldquo;worse&rdquo; reading, as something to take to a colleague.</p></div>
  <div class="card"><h3>Not a license</h3>
  <p class="micro">Two instruments are reproduced here under the permission each one carries,
  and named at their source. Everything else is named and not printed. Terms change and vary
  by country and translation: confirm at the publisher before relying on any of it.</p></div>
</div>
{K.src("<b>PHQ-9</b> " + C.MEASURE["PHQ-9"]["source"] + " &nbsp; <b>GAD-7</b> "
       + C.MEASURE["GAD-7"]["source"] + " &nbsp; <b>PCL-5</b> "
       + C.MEASURE["PCL-5"]["source"]
       + " &nbsp; <b>Sleep efficiency</b> " + C.MEASURE["Sleep diary"]["source"])}
<div class="card ink"><h3>On the evidence for measuring at all</h3>
<p class="micro">Routinely measuring outcomes and feeding the result back to the clinician is
one of the better supported process changes in psychotherapy, and the benefit falls
disproportionately on the clients who are not improving &mdash; which is the case this book
is built around. Two honest qualifications. The research is about feedback systems in
services, not about this particular set of checkpoints, which has not been tested. And the
branches in Part Two are conventions of clinical craft, chosen because the arc already
contains a session for that failure; they are labeled that way throughout and are not
findings.</p></div>
<div class="g3">
  <div class="card"><h3>Not validated as a package</h3><p class="micro">The instruments named
  here carry their own literature. This particular schedule does not: it is offered as a
  structure for clinical judgment, not as an evidence-based protocol in its own right, and
  the note above says exactly what is and is not claimed for it.</p></div>
  <div class="card"><h3>Not a record system</h3><p class="micro">The sheets in Part Three are
  working paper. Where a reading belongs in the clinical record, it goes into the record
  under your own documentation policy, and the retention and disposal of the sheets are
  yours to decide.</p></div>
  <div class="card"><h3>Not jurisdiction-specific</h3><p class="micro">Reporting duties,
  consent, record-keeping and what may be shared with a payer all differ by state and by
  country. Everything here defers to your local rules where the two disagree.</p></div>
</div>
<p class="micro">Session numbers throughout refer to the Session Arc registry: 360 sessions,
{len(A.ARCS)} arcs, {sid(1)}&ndash;{sid(360)}. The checkpoint schedule is generated from that
registry, so a session renumbered there is renumbered here.</p>
"""


def p_back():
    tot = C.totals()
    return f"""<div class="opener cover">
<div class="img" style="flex-basis:52%"><img src="{K.PHOTO % 'h9-back'}" alt=""></div>
<div style="padding:12mm 17.5mm 14mm;flex:1 1 auto;display:flex;flex-direction:column">
  <div class="brand">Session Arc &middot; Companion 02</div>
  <h1 style="font-size:36px">Know by session eight<br>whether the arc is working.</h1>
  <p class="sub" style="max-width:126mm">{tot["checkpoints"]} checkpoints. {tot["arcs"]} arcs.
  Three ways out of every reading, and a named session at the end of each one.</p>
  <div class="facts">
    <div><div class="v">{len(C.MEASURE) - 1}</div><div class="l">Measures, each with its license stated</div></div>
    <div><div class="v">15</div><div class="l">Worked cases</div></div>
    <div><div class="v">3</div><div class="l">Sheets to copy</div></div>
  </div>
  <div style="margin-top:auto;font-size:8px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#6B7D7E">
  &copy; Sando LLC &middot; For licensed mental health professionals &middot; Not a diagnostic instrument</div>
</div></div>"""
