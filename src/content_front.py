# -*- coding: utf-8 -*-
"""Front matter, Part One (the method), Part Two (the atlas), the two
worksheets, scope and the back cover. The worked example that runs through
Part One is Route 05, computed live, so its numbers cannot drift from the
route pages."""
import arcs as A
import content_routes as CR
import figs as F
import kit as K
import routes as R
import routes_text as T

J = next(r for r in CR.ORDERED if set(r["keys"]) == {"SLP", "DEP", "ANX"})
JB = J["build"]
OWN = R.build(["GRF", "ANX"])


def s(n):
    return "S%03d" % n


def t(n):
    return A.title_of(n)


def opener(img, num, title, sub, inside, cls=""):
    items = "".join(f"<li>{x}</li>" for x in inside)
    return f"""<div class="opener {cls}">
<div class="img"><img src="{K.PHOTO % img}" alt=""></div>
<div class="txt" style="padding:12mm 17.5mm 16mm">
  <div><div class="chno">{num}</div><h1>{title}</h1><div class="rulec"></div><p class="sub">{sub}</p></div>
  <div class="inside"><h3>Inside</h3><ol>{items}</ol></div>
</div></div>"""


# ============================================================== front ===
def p_cover():
    return f"""<div class="opener cover">
<div class="img" style="flex-basis:60%"><img src="{K.PHOTO % 'h0-cover'}" alt=""></div>
<div style="padding:11mm 17.5mm 14mm;flex:1 1 auto;display:flex;flex-direction:column">
  <div class="brand">Session Arc &middot; Companion 01</div>
  <h1>The Combined Routes</h1>
  <p class="sub" style="max-width:128mm">Thirty ready-made routes for the client who walks in with more than one of the
  fifteen arcs &mdash; in the right order, with the repeated sessions already taken out.</p>
  <div class="facts">
    <div><div class="v">30</div><div class="l">Routes</div></div>
    <div><div class="v">13</div><div class="l">Arcs combined</div></div>
    <div><div class="v">7</div><div class="l">Ordering rules</div></div>
    <div><div class="v">1</div><div class="l">Overlap Atlas</div></div>
  </div>
  <div style="margin-top:auto;font-size:8px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#6B7D7E">
  For licensed mental health professionals &middot; &copy; Sando LLC</div>
</div></div>"""


def p_fits():
    return f"""
<div class="eyebrow">Before you start</div>
<h2>Session Arc gives you fifteen arcs. <em>Your clients rarely bring one.</em></h2>
<p class="lede">Each arc in Session Arc is written to stand on its own: it opens, it builds, it ends. That is right
for a client with one clear problem. It goes wrong the moment you run two arcs back to back as written.</p>
<div class="g64">
  <div class="stack">
    <p>Run Sleep and then Depression exactly as printed and the client meets <i>Activity and mood log</i> twice,
    sits through two endings, and may start the harder arc before the easier one has done its job. None of that
    is a flaw in either arc. It is what happens at the join.</p>
    <p>This book is about the joins. A <b>route</b> takes two or three arcs, puts them in an order that holds up
    clinically, removes the sessions that would repeat a skill already taught, keeps a single ending, and rewrites
    the bridge where one arc hands over to the next.</p>
    <p class="small muted">Nothing in the library changes. Every route points to Session Arc&rsquo;s sessions by
    number, and the route is chosen once the formulation is agreed in The First Six Sessions or the Intake arc.</p>
  </div>
  {K.capt("x2-binder", 340, "The library stays whole. A route is a reading order through it, not a rewrite of it.")}
</div>
<div class="g2">
  {K.card('<h3>A route is</h3>' + K.ticks([
      "An order for the arcs, and the rule that sets it.",
      "A list of the sessions to run and the ones to skip, by number.",
      "The sentence that joins one arc to the next.",
  ]), "sage")}
  {K.card('<h3>A route is not</h3>' + K.ticks([
      "A protocol for a diagnosis, or for two diagnoses at once.",
      "A promise of length: many clients finish before the end.",
      "A reason to keep going when the client needs a referral.",
  ]), "plum")}
</div>
<div class="scope"><h3>Scope</h3><p class="small" style="margin:0">Written for licensed clinicians using Session Arc.
The routes organize material; they do not replace assessment, clinical judgment or supervision. Trauma Groundwork
remains stabilization inside every route. When a presentation is beyond your scope or the client's safety is in
question, use Pause &amp; Refer and your local protocol before anything on these pages.</p></div>
"""


def p_contents():
    def rows(items):
        out = []
        for kind, label, ref in items:
            if kind == "part":
                out.append(f'<tr class="part"><td colspan="2">{label}</td></tr>')
            else:
                out.append(f'<tr><td>{label}</td><td class="pg">{K.pg(ref)}</td></tr>')
        return '<table class="toc">' + "".join(out) + "</table>"
    left = rows([
        ("part", "Start here", ""),
        ("", "Where this book sits", "p_fits"),
        ("", "One client, three arcs", "p_problem"),
        ("", "How a route is built", "p_build"),
        ("part", "Part One &middot; The method", ""),
        ("", "Choosing the route, step by step", "p_choose"),
        ("", "The layer ladder: rules one to four", "p_rules1"),
        ("", "Rules five to seven, and ties", "p_rules2"),
        ("", "The override: the first visible win", "p_override"),
        ("", "Teach once: the fifteen shared skills", "p_modules"),
        ("", "Cutting a repeat, step by step", "p_cut"),
    ])
    right = rows([
        ("part", "Part One, continued", ""),
        ("", "Seams: where one arc hands over", "p_seams"),
        ("", "The order conversation", "p_talk"),
        ("", "Reading a route page", "p_reading"),
        ("", "When the route stops fitting", "p_stop"),
        ("part", "Part Two &middot; The Overlap Atlas", ""),
        ("", "The atlas", "p_atlas"),
        ("", "Reading the atlas", "p_atlas_read"),
        ("", "A pair that is not in the book", "p_own"),
        ("", "Route finder", "p_finder"),
        ("part", "Working pages", ""),
        ("", "Sheet 1 &middot; Route builder", "p_sheet1"),
        ("", "Sheet 2 &middot; Seam planner", "p_sheet2"),
        ("", "Scope, referral and sources", "p_scope"),
    ])

    def rt(rs):
        return '<table class="toc sm">' + "".join(
            f'<tr><td><span class="sid">{r["num"]:02d}</span>&nbsp;&nbsp;{r["title"]}</td>'
            f'<td class="pg">{K.pg("ra%02d" % r["num"])}</td></tr>' for r in rs) + "</table>"
    return f"""
<div class="eyebrow">Contents</div>
<h2>Three parts, thirty routes, two working sheets</h2>
<div class="g2" style="gap:26px">{left}{right}</div>
<div><h3 style="border-bottom:1.1px solid #173C42;padding-bottom:5px;margin:4px 0 0">Part Three &middot; The thirty routes &middot; page {K.pg("p_op3")}</h3>
<div class="g2" style="gap:26px">{rt(CR.ORDERED[:15])}{rt(CR.ORDERED[15:])}</div></div>
"""


def p_problem():
    reps = [i for i in JB["items"] if i["status"] == "repeat"]
    closes = [i for i in JB["items"] if i["status"] == "close"]
    rep_list = ", ".join(f"{t(i['n'])} ({s(i['n'])})" for i in reps[:3])
    return f"""
<div class="eyebrow">Start here &middot; the problem this book solves</div>
<h2>One client, three arcs</h2>
<div class="g46">
  {K.capt("x1-dawn", 300, "Jordan, the composite client behind Route 05: awake at dawn before a shift they dread.")}
  <div class="stack">
    <p class="lede">Jordan, 33, lies awake worrying, drags through the day, and calls in sick before shifts they dread.</p>
    <p>By the end of intake you have three arcs on the table: <b>Sleep</b> (15 sessions), <b>Depression</b> (40) and
    <b>Anxiety</b> (40). Run them one after another as printed and you have a plan of {JB["total"]} sessions.
    It looks thorough. It has three problems, and each one costs you the client&rsquo;s trust.</p>
    {K.steps([
        f"<b>The order is left to chance.</b> Start with the anxiety ladder and you ask someone sleeping four hours to face their fear on purpose.",
        f"<b>Skills come round twice.</b> {len(reps)} sessions teach something an earlier arc already taught: {rep_list} and more. Clients hear &ldquo;we did this&rdquo; as &ldquo;we are not getting anywhere&rdquo;.",
        f"<b>Three endings.</b> Every arc closes with Pulling it together and The setback plan. That is {len(closes)} ending sessions in the middle of treatment, each one an invitation to stop.",
    ])}
  </div>
</div>
{K.figbox(F.stack_vs_route(JB), f"<b>Same three arcs, two plans</b>Top: the arcs stacked as written; the darkened sessions are the {len(reps)} repeats and {len(closes)} endings a route removes. Bottom: Route 05. The rust marks are the two seams, at weeks {JB['seams'][0]['week']} and {JB['seams'][1]['week']}.")}
<div class="stats">
  {K.stat(JB["total"], "Sessions if the three arcs are stacked as written")}
  {K.stat(JB["length"], "Sessions on Route 05, with nothing clinical lost")}
  {K.stat(len(reps), "Repeats removed, each folded into a ten-minute review")}
  {K.stat(len(JB["seams"]), "Seams, each with its bridge rewritten")}
</div>
"""


def p_build():
    o = JB["order"]
    names = [A.BY_KEY[k]["short"] for k in o]
    reps = [i for i in JB["items"] if i["status"] == "repeat"]
    rep_rows = "".join(
        f'<tr><td class="sid">{s(i["n"])}</td><td>{i["title"]}</td><td class="sid">{s(i["ref"])}</td></tr>' for i in reps)
    s1, s2 = JB["seams"]
    return f"""
<div class="eyebrow">Start here &middot; the method in one page</div>
<h2>How a route is built: <em>four moves</em></h2>
<p>Every route in Part Three was made with the same four moves, and you can make any other combination the same
way. Here they are on Jordan&rsquo;s three arcs.</p>
<div class="g2">
  <div class="card"><h3><span class="dot">1</span>&nbsp; Name the arcs</h3>
    <p class="small">From the agreed formulation, name no more than three arcs. Four means something has to wait.</p>
    <p class="small" style="margin:0"><b>Jordan:</b> Sleep, Depression, Anxiety.</p></div>
  <div class="card"><h3><span class="dot">2</span>&nbsp; Order them by layer</h3>
    <p class="small">Place each arc on the layer ladder (page {K.pg("p_rules1")}); lower layers go first.</p>
    <p class="small" style="margin:0"><b>Jordan:</b> {names[0]} {K.arrow()} {names[1]} by Rule {R.RULE[s1["rule"]]["n"]},
    then {K.arrow()} {names[2]} by Rule {R.RULE[s2["rule"]]["n"]}.</p></div>
  <div class="card"><h3><span class="dot">3</span>&nbsp; Cut the repeats and the extra endings</h3>
    <p class="small">A shared skill is taught once; later copies become ten-minute reviews. Only the last arc keeps its ending.</p>
    <table class="tbl tight" style="font-size:10.6px"><thead><tr><th>Cut</th><th>Session</th><th>Taught in</th></tr></thead>
    <tbody>{rep_rows}</tbody></table></div>
  <div class="card"><h3><span class="dot">4</span>&nbsp; Stitch the seams</h3>
    <p class="small">Where one arc ends and the next begins, rewrite the closing bridge so the client hears one
    treatment, not a new one.</p>
    <p class="small"><b>Jordan:</b> seams at week {s1["week"]} ({s(s1["last"]["n"])} {K.arrow()} {s(s1["first"]["n"])}) and week {s2["week"]} ({s(s2["last"]["n"])} {K.arrow()} {s(s2["first"]["n"])}).</p>
    <p class="small" style="margin:0;font-style:italic;border-left:1.6px solid #B8552F;padding-left:10px">&ldquo;{R.bridge(s1)}&rdquo;</p></div>
</div>
{K.figbox(F.ladder(JB, compact=True), "<b>Jordan on the ladder</b>Numbers show the order on the route; arcs in grey are not part of it.")}
"""


# ============================================================ part one ===
def p_op1():
    return opener("h1-method", "Part One", "The method",
                  "Seven rules decide the order. Two moves remove what repeats. One sentence joins the arcs. This part shows each of them, step by step, on real sessions.",
                  ["Choosing the route", "The layer ladder", "Rules five to seven", "The override",
                   "The fifteen shared skills", "Cutting a repeat", "Seams", "The order conversation",
                   "Reading a route page", "When the route stops fitting"])


def p_choose():
    return f"""
<div class="eyebrow">Part One &middot; when and how</div>
<h2>Choosing the route, <em>step by step</em></h2>
<p class="lede">Choose the route once, at the point where the formulation is agreed: session 6 of The First Six
Sessions, or {s(17)} <i>{t(17)}</i> in the Intake arc. Earlier than that you are guessing; later, the client has
already started an arc by default.</p>
{K.seq([
    ("c1-notes", "List what was named", "Underline every problem the client or you named in the formulation. Use the client&rsquo;s words."),
    ("c2-folders", "Match each to an arc", "Three arcs at most. If one problem is clearly the cause of another, keep the cause."),
    ("c3-atlas", "Find the route", "Look the combination up in the Route finder. Not listed? Use the atlas and Sheet 1."),
    ("c4-tell", "Tell the client the order", "Say what comes first and why, and when the rest arrives. The script is on page %d." % K.pg("p_talk")),
], h=170)}
<div class="g3">
  {K.card('<h3>Ask before you choose</h3>' + K.ticks([
      "Is anything here a safety or scope issue? That comes before any route.",
      "Did one problem start the others? Rule 3 puts a loss first.",
      "Which problem did the client come in for?",
  ]), "tint")}
  {K.card('<h3>Two arcs or three?</h3><p class="small" style="margin:0">Two arcs when the second problem is clearly smaller. Three when all three are keeping each other going &mdash; poor sleep feeding low mood feeding avoidance, as with Jordan. Never four.</p>', "tint")}
  {K.card('<h3>Write it down</h3><p class="small" style="margin:0">Copy the route number and the start date onto the running order page and file it. The seams are your review points: put their weeks in the calendar now, and tell the client the first one.</p>', "tint")}
</div>
"""


def p_rules1():
    items = [(r["name"], r["body"]) for r in R.RULES[:4]]
    return f"""
<div class="eyebrow">Part One &middot; the rules that set the order</div>
<h2>The layer ladder</h2>
<p class="lede">Every combinable arc sits on one of eight layers. On a route, the lower layer goes first. Rules one
to four explain the bottom half of the ladder: why some work has to come before the rest can be learned.</p>
<div class="g46">
  <div class="stack">{K.legend(items)}{K.capt("l1-stack", 95, "The order is decided once, from the bottom layer up, and written down before the route begins.")}</div>
  {K.figbox(F.ladder(), "<b>The eight layers</b>Read top to bottom: that is the order on any route. Two arcs on the same layer are ordered by Rule 7.")}
</div>
<div class="card line"><p class="small" style="margin:0"><b>These are rules of craft, not findings.</b> They
encode a common clinical order &mdash; stabilize, restore the basics, then ask for effort &mdash; and they are here
so the order is consistent and explainable. Your judgment about a specific client overrides every one of them, and
the override on page {K.pg("p_override")} is the usual way to do it without losing the route.</p></div>
"""


def p_rules2():
    items = [(r["name"], r["body"]) for r in R.RULES[4:]]
    ties = [("Emotion Regulation, then Trauma Groundwork", "Grounding, naming and the window of tolerance are taught in depth in Emotion Regulation."),
            ("Sleep, then Stress &amp; Burnout", "Wind-down and worry time are built into the Sleep arc&rsquo;s nightly routine."),
            ("Anxiety, then Habits &amp; Urges", "The ladder is built and climbed over fifteen sessions in Anxiety; Habits borrows it."),
            ("Self-Worth, then Anger", "The critic work steadies the self that anger defends."),
            ("Values &amp; Meaning, then Work &amp; Money", "The values compass is the core of Values; Work applies it to one decision.")]
    return f"""
<div class="eyebrow">Part One &middot; the rules that set the order</div>
<h2>Rules five to seven, <em>and what to do with a tie</em></h2>
<div class="g2">
  <div class="stack">{K.legend(items, start=5)}
  {K.card('<h3>Rule 5 in a sentence</h3><p class="quote sm" style="margin:0">&ldquo;Work on how you treat yourself, and then on how you treat the people around you.&rdquo;</p>', "sage")}
  {K.card('<h3>Rule 6 in a sentence</h3><p class="quote sm" style="margin:0">&ldquo;Big questions get better answers from solid ground.&rdquo;</p>', "plum")}
  {K.card('<h3>Rule 7 in a sentence</h3><p class="quote sm" style="margin:0">&ldquo;You learned this already; we&rsquo;ll use it, not relearn it.&rdquo;</p>', "blue")}
  </div>
  <div class="stack">
    <h3>Ties on the same layer</h3>
    <p class="small">When two arcs share a layer, the arc that <b>teaches</b> the shared skill in more depth goes
    first, and the other arc borrows it. That is the second half of Rule 7.</p>
    {K.table(["Order", "Why this way round"], ties, "small")}
    {K.capt("s1-seam", 150, "Rule 7 in practice: the skill was taught months ago, so today it is a short review at the table, not a new lesson.")}
  </div>
</div>
"""


def p_override():
    first = A.sessions("ANX")[0]
    return f"""
<div class="eyebrow">Part One &middot; bending the order without breaking it</div>
<h2>The override: <em>the first visible win</em></h2>
<p class="lede">Clients come in for the problem that hurts most, and it is often not the one the ladder puts first.
If week after week goes by without that problem being named in the room, they leave.</p>
<div class="g64">
  <div class="stack">
    <p>The override keeps the order and answers the complaint. Borrow <b>one</b> session &mdash; the first session of
    the arc the client came in for &mdash; and run it in week 2. It names their problem, explains how it works, and
    tells them when the full arc arrives. Then return to the route.</p>
    <p>On Route 05 Jordan came in for the dread. The route starts with Sleep, and Anxiety does not begin until
    week {JB["seams"][1]["week"]}. So {s(first[0])} <i>{first[1]}</i> moves to week 2. It is not repeated later: when
    the Anxiety arc opens, start at {s(first[0] + 1)} and give five minutes to recall what week 2 found.</p>
    {K.ticks([
        "Use it once per route, and only from the arc the client named first.",
        "Borrow the first session of that arc, nothing deeper: no ladder, no exposure, no core beliefs.",
        "Say out loud when the full arc starts. The week number is on the route page.",
    ])}
  </div>
  {K.capt("o1-borrow", 330, "One card moves to the front of the row. The row itself does not change.")}
</div>
{K.figbox(F.override_fig(JB, "ANX"), f"<b>Route 05, weeks 1 to 12</b>{s(first[0])} (slate blue, the third arc&rsquo;s colour on this route) is borrowed from week {JB['seams'][1]['week']} into week 2. Every Sleep session moves back one week.")}
<div class="card rust"><h3>Do not use the override when</h3><p class="small" style="margin:0">the named problem
is risk (that goes to Pause &amp; Refer, not to a borrowed session); the client is flooding and Rule 1 applies; or the
borrowed session would start exposure, trauma memories or grief work before the ground is ready.</p></div>
"""


def p_modules():
    return f"""
<div class="eyebrow">Part One &middot; Rule 7, in detail</div>
<h2>Teach once: <em>the fifteen shared skills</em></h2>
<p class="lede">Fifteen skills are taught in more than one arc. They are the only sessions a route ever cuts as a
repeat. Everything else in an arc is its own and always stays.</p>
{K.figbox(F.module_matrix(), "<b>Where each shared skill is taught</b>A dot and a session number mark every arc that teaches the skill. On a route, the first of those sessions to come up is taught in full; any later one is cut and folded into a review.")}
<div class="g3">
  {K.card('<h3>Why cut, not shorten</h3><p class="small" style="margin:0">A repeated session is not a waste of time only. It tells the client the plan does not know what they have already done, and that damages trust more than an hour lost.</p>')}
  {K.card('<h3>Why a review survives</h3><p class="small" style="margin:0">Skills fade. The later arc uses the skill in a new setting, so ten minutes at the start of its next session bring it back and connect it to the new work.</p>')}
  {K.card('<h3>Which copy stays</h3><p class="small" style="margin:0">Always the first one on the route, whichever arc it belongs to. That is why the order of arcs decides which sessions are cut.</p>')}
</div>
"""


def p_cut():
    it = next(i for i in JB["items"] if i["n"] == 83)
    nxt = next(i for i in JB["items"] if i["n"] == 84)
    return f"""
<div class="eyebrow">Part One &middot; Rule 7, by hand</div>
<h2>Cutting a repeat, <em>step by step</em></h2>
<p class="lede">On Route 05, Depression&rsquo;s {s(83)} <i>{it["title"]}</i> is a repeat: Sleep already taught the
same log in {s(it["ref"])}. Here is what happens to it, on paper and in the room.</p>
{K.seq([
    ("k1-find", "Find the earlier copy", f"The module matrix shows the log in Sleep ({s(it['ref'])}) and Depression ({s(83)}). Sleep comes first."),
    ("k2-strike", "Strike the later session", f"Draw a line through {s(83)} on the running order and write {s(it['ref'])} on its date line."),
    ("k3-note", "Fold in the review", f"Note &ldquo;+ review {s(it['ref'])}&rdquo; on {s(84)}, the next session kept in that arc."),
], h=170)}
<div class="g55">
  <div class="card"><h3>The ten-minute review, opening {s(84)}</h3>
  <div class="dialog">
    <span class="who">You</span><span class="t">&ldquo;Before today&rsquo;s topic: back in the sleep work you kept an activity log. Is it still going?&rdquo;</span>
    <span class="who">Client</span><span class="t">&ldquo;On and off. Mostly off since I slept better.&rdquo;</span>
    <span class="who">You</span><span class="t">&ldquo;That makes sense. We are going to use it differently now: to catch which activities lift your mood, not your energy.&rdquo;</span>
    <span class="note">Recall, check use, re-aim it at the new arc. Then start {s(84)} <i>{nxt["title"]}</i> as written.</span>
  </div></div>
  <div class="stack">
    <h3>Every cut on Route 05</h3>
    {K.table(["Cut", "Taught in", "Review opens"],
             [[f'<span class="sid">{s(i["n"])}</span> {i["title"]}', f'<span class="sid">{s(i["ref"])}</span>',
               f'<span class="sid">{s(next(k["n"] for k in JB["items"] if i["ref"] in k["reviews"] and k["arc"] == i["arc"]))}</span>']
              for i in JB["items"] if i["status"] == "repeat"], "small")}
    <p class="micro">Two cuts can fold into the same session: {s(49)} opens with both {s(90)} and {s(91)}.</p>
  </div>
</div>
"""


def p_seams():
    s1 = JB["seams"][0]
    return f"""
<div class="eyebrow">Part One &middot; the joins</div>
<h2>Seams: <em>where one arc hands over</em></h2>
<p class="lede">A seam is the last kept session of one arc and the first of the next. As printed, the first arc
ends as if treatment were over. On a route, its last few minutes are rewritten so the client hears a handover.</p>
<div class="g37">
  <div class="stack">
    {K.legend([
        ("Name what was built", "One concrete thing the client now has, in their words if you can."),
        ("Say what comes next needs it", "The next arc depends on that ability. This is the reason for the order, said again."),
        ("Name the first session", "Say what happens next week, so the change feels planned."),
    ])}
  </div>
  <div>
    <div class="orderline" style="margin-bottom:10px">
      <div class="arc a1"><div class="k">End of arc 1 &middot; week {s1["week"] - 1}</div><div class="nm">{s(s1["last"]["n"])} {s1["last"]["title"]}</div><div class="ct">Its printed bridge closes the arc.</div></div>
      <div class="join">Seam<br>{K.arrow(w=20)}</div>
      <div class="arc a2"><div class="k">Arc 2 opens &middot; week {s1["week"]}</div><div class="nm">{s(s1["first"]["n"])} {s1["first"]["title"]}</div><div class="ct">Starts as written.</div></div>
    </div>
    <div class="seamc"><div class="hd">Rewritten bridge, last five minutes of {s(s1["last"]["n"])}<span>Route 05 &middot; Seam 1</span></div>
    <p>&ldquo;{R.bridge(s1)}&rdquo;</p></div>
    <p class="micro" style="margin-top:8px">Every route page prints its seams this way. Say it in your own words;
    keep the three parts.</p>
  </div>
</div>
{K.capt("t1-listen", 200, "At a seam, let the client say what has changed before you say what comes next.")}
<div class="g2">
  {K.card('<h3>What the seam replaces</h3><p class="small" style="margin:0">The first arc&rsquo;s <i>Pulling it together</i> and <i>The setback plan</i> are cut (Rule 7). Their useful parts &mdash; a short look back and one warning sign to watch &mdash; fit in the rewritten bridge.</p>', "tint")}
  {K.card('<h3>Use the seam as a review point</h3><p class="small" style="margin:0">Book a slightly longer session or a check-in at each seam. It is the natural moment to ask whether the route still fits (page ' + str(K.pg("p_stop")) + ').</p>', "tint")}
</div>
"""


def p_talk():
    return f"""
<div class="eyebrow">Part One &middot; saying it</div>
<h2>The order conversation</h2>
<p class="lede">Clients accept an order they understand. The conversation takes five minutes, once, and it is easiest
with the route&rsquo;s arcs drawn as boxes on a sheet between you.</p>
<div class="g64">
  <div class="card"><h3>A worked version for Route 05</h3>
  <div class="dialog">
    <span class="who">You</span><span class="t">&ldquo;You told me three things: the nights, the flat days, and the dread before work. They are connected, so the order matters.&rdquo;</span>
    <span class="who">You</span><span class="t">&ldquo;We start with sleep. Almost everything else we will do is learning, and learning needs sleep.&rdquo;</span>
    <span class="note">Name the rule in plain words. Here: Rule 2, body before mind.</span>
    <span class="who">Client</span><span class="t">&ldquo;But the dread is the worst part.&rdquo;</span>
    <span class="who">You</span><span class="t">&ldquo;I hear that. Next week we spend a session on what the anxiety is doing, so it is on the table from the start. Then we build up to facing it, around week {JB["seams"][1]["week"]}, when you have the fuel for it.&rdquo;</span>
    <span class="note">The override: one borrowed session and a week number.</span>
    <span class="who">You</span><span class="t">&ldquo;Two points along the way, around weeks {JB["seams"][0]["week"]} and {JB["seams"][1]["week"]}, we will stop and check the plan still fits.&rdquo;</span>
  </div></div>
  <div class="stack">
    <h3>Five things the conversation must contain</h3>
    {K.steps([
        "The problems, in the client&rsquo;s words.",
        "What comes first.",
        "Why, in one plain sentence.",
        "When the rest starts, as a week.",
        "That the plan will be checked at the seams.",
    ])}
    <div class="card tint"><h3>If the client disagrees</h3>{K.ticks([
        "Ask what would make the first weeks feel worth it.",
        "Offer the override: one session on their problem in week 2.",
        "Agree a review at the first seam instead of arguing the order now.",
    ])}</div>
  </div>
</div>
{K.seq([
    ("t2-show", "Draw the boxes", "Three boxes in a row, left to right, one per arc. No labels needed until you say them."),
    ("t3-write", "Let them write the weeks", "The client notes when each part starts. Owning the dates makes the wait bearable."),
], h=175)}
"""


def p_reading():
    pins = [(5, "Route number and arcs", "The number the Route finder uses. On the right: sessions kept, repeats cut, endings folded."),
            (17, "The photograph and family", "The kind of presentation the route was written for."),
            (35, "Who walks in, what you say", "A composite sketch to test fit, and the words for the client with the weeks filled in."),
            (48, "The order", "Each arc in route order, its session range, and the rule and week at every join."),
            (61, "The whole route", "Every session as a square. Dashed squares are cuts; rust marks are seams; numbers are weeks."),
            (81, "Seams", "The rewritten bridge for each join, ready for the last minutes of the arc.")]
    marks = "".join(f'<span class="dot r" style="position:absolute;left:-8px;top:{y}%;">{i}</span>'
                    for i, (y, _, _) in enumerate(pins, 1))
    return f"""
<div class="eyebrow">Part One &middot; using Part Three</div>
<h2>Reading a route page</h2>
<p class="lede">Each route has two pages. The first explains it; the second is the running order you tick off and
keep in the file. This is the first page of Route 05, reduced.</p>
<div class="g55" style="align-items:start">
  <figure class="figbox"><div class="figw"><div style="position:relative;margin-left:8px">
    <img src="{K.PHOTO % 'snap-ra05'}" alt="" style="width:100%;display:block;border:0.8px solid #E3DACB">{marks}</div></div>
    <figcaption><b>Route 05, page one</b>The full page is on page {K.pg("ra05")}.</figcaption></figure>
  <div class="stack">{K.legend([(a, b) for _, a, b in pins], rust=range(1, 7))}
    <div class="card tint"><h3>The second page</h3><p class="small" style="margin:0">One line per session in route
    order, grouped by arc, with the seams between. Cut sessions stay on the list in grey &mdash; on the longest
    routes, in one line under it &mdash; so you can see where a skill was already taught. Tick as you go. Three things
    to watch for close the page.</p></div>
  </div>
</div>
<div class="g3">
  {K.card('<h3>Before the first session</h3><p class="small" style="margin:0">Read page one, put the seam weeks in your calendar, and file page two.</p>', "tint")}
  {K.card('<h3>At every session</h3><p class="small" style="margin:0">Open the next unticked line on page two. Check for a &ldquo;+ review&rdquo; note first.</p>', "tint")}
  {K.card('<h3>At every seam</h3><p class="small" style="margin:0">Say the bridge from page one, then ask the four questions on page ' + str(K.pg("p_stop")) + '.</p>', "tint")}
</div>
"""


def p_stop():
    return f"""
<div class="eyebrow">Part One &middot; when the plan meets the client</div>
<h2>When the route <em>stops fitting</em></h2>
<p class="lede">A route is an order, not a contract. Check it at every seam, and any time the client or the work
changes. Four questions, asked in this order, cover almost every case.</p>
<div class="dflow">
  <div class="q"><b>Question 1</b>Is there a new risk, or something beyond your scope?</div>
  <div class="a">Yes {K.arrow()}</div><div class="res">Stop the route. Pause &amp; Refer and your local protocol.</div>
  <div class="down">{K.arrow("down")} No</div><div></div><div></div>
  <div class="q"><b>Question 2</b>Has a new problem arrived that belongs to another arc?</div>
  <div class="a">Yes {K.arrow()}</div><div class="res">Finish the current arc to its next natural stop, then rebuild the route with the new arc on the ladder.</div>
  <div class="down">{K.arrow("down")} No</div><div></div><div></div>
  <div class="q"><b>Question 3</b>Is the current arc stuck for three sessions or more?</div>
  <div class="a">Yes {K.arrow()}</div><div class="res">Use the Arc Map branch for that arc. If no branch fits, bring the next seam forward.</div>
  <div class="down">{K.arrow("down")} No</div><div></div><div></div>
  <div class="q"><b>Question 4</b>Has the problem the next arc was meant for already eased?</div>
  <div class="a">Yes {K.arrow()}</div><div class="res">Run that arc&rsquo;s first session to check, then skip to its ending or close the route early.</div>
</div>
<div class="g55">
  {K.capt("f1-pause", 300, "After a seam session: five minutes with the file and the four questions, before the next client.")}
  <div class="stack">
    <h3>Ending early is a good outcome</h3>
    <p class="small">Most clients will not need every session on a long route. Improvement in one arc often eases the
    next &mdash; better sleep lifts mood, more activity lowers anxiety. When that happens, the route has done its job
    early. Close with the last arc&rsquo;s two ending sessions, or with the Progress arc if the work was long.</p>
    <h3>Rebuilding is not starting over</h3>
    <p class="small" style="margin:0">Sessions already run stay run. When you rebuild, strike them on the new
    running order exactly as if they were repeats, and begin at the first session not yet done.</p>
    <p class="small" style="margin:0">Record the decision on Sheet 2, the seam planner (page {K.pg("p_sheet2")}).</p>
  </div>
</div>
"""


# ============================================================ part two ===
def p_op2():
    return opener("h2-atlas", "Part Two", "The Overlap Atlas",
                  "One grid that shows how much any two arcs share, so you can build a route for a combination this book does not print.",
                  ["The atlas", "Reading the atlas", "A pair that is not in the book", "Route finder"])


def p_atlas():
    return f"""
<div class="eyebrow">Part Two &middot; the atlas</div>
<h2>The Overlap Atlas</h2>
<p>Each cell is the number of shared skills two arcs have in common: the sessions a route cuts from the later arc.
The dark diagonal gives each arc&rsquo;s length. Intake and Progress are left out: every route starts after Intake,
and Progress is where a long treatment ends.</p>
{K.figbox(F.atlas(), "<b>How to read a cell</b>Find the arc that goes first in the rows and the arc that follows in the columns. The number is how many of the second arc&rsquo;s sessions become ten-minute reviews. The grid is symmetrical: the count is the same either way round, but which sessions are cut depends on the order.")}
<div class="keyrow">
  <span class="kk"><span class="sw" style="background:#FFFCF6"></span>0 &middot; nothing shared</span>
  <span class="kk"><span class="sw" style="background:#EEF1EE"></span>1</span>
  <span class="kk"><span class="sw" style="background:#DCE3E1"></span>2</span>
  <span class="kk"><span class="sw" style="background:#C4D0CE"></span>3</span>
  <span class="kk"><span class="sw" style="background:#A6B6B4"></span>4 &middot; most shared</span>
</div>
"""


def p_atlas_read():
    top = sorted(((A.overlap(a, b), a, b) for i, a in enumerate(A.COMBINABLE)
                  for b in A.COMBINABLE[i + 1:]), reverse=True)[:5]
    rows = [[f'{A.BY_KEY[a]["short"]} + {A.BY_KEY[b]["short"]}', f'<b>{v}</b>',
             ", ".join(A.MODULES[m] for m in sorted(A.modules(a) & A.modules(b)))] for v, a, b in top]
    zero = [(a, b) for i, a in enumerate(A.COMBINABLE) for b in A.COMBINABLE[i + 1:] if A.overlap(a, b) == 0]
    return f"""
<div class="eyebrow">Part Two &middot; what the numbers tell you</div>
<h2>Reading the atlas</h2>
<p class="lede">The atlas answers two practical questions before you build anything: how much shorter will the route
be, and how much will the second arc feel familiar to the client?</p>
<div class="g2">
  <div class="stack">
    <h3>High numbers: 3 or 4</h3>
    <p class="small">The arcs teach several of the same skills. The route will be noticeably shorter, and the second
    arc will open with a run of reviews. Plan the seam carefully: the client may feel they are going over old ground
    unless you say why the skills come back.</p>
    <h3>Low numbers: 0 or 1</h3>
    <p class="small">The arcs barely share anything. The route is close to the two arcs added together, less one
    ending. The order still matters; the cutting does not. {len(zero)} of the 78 pairs share nothing at all.</p>
    <h3>The diagonal</h3>
    <p class="small" style="margin:0">Arc length. Add the two diagonals, take away the cell, take away two for the
    folded ending: that is the route length before you open a single page.</p>
  </div>
  <div class="stack">
    <h3>The five pairs that share the most</h3>
    {K.table(["Pair", "Shared", "Skills"], rows, "small")}
  </div>
</div>
{K.capt("a1-read", 190, "Row for the arc that goes first, column for the one that follows: the cell is the number of reviews the second arc will open with.")}
<div class="card sage"><h3>The arithmetic, on Route 05</h3><p class="small" style="margin:0">Sleep 15 + Depression 40 +
Anxiety 40 = 95. Cells: Sleep&ndash;Depression {A.overlap("SLP", "DEP")}, Sleep&ndash;Anxiety {A.overlap("SLP", "ANX")},
Depression&ndash;Anxiety {A.overlap("DEP", "ANX")}, total {A.overlap("SLP", "DEP") + A.overlap("SLP", "ANX") + A.overlap("DEP", "ANX")}.
The first two arcs each lose their two ending sessions = 4. Route: 95 &minus; 6 &minus; 4 = {JB["length"]} sessions, which is exactly what page
{K.pg("ra05")} prints. For three arcs, check that no skill is counted in two cells.</p></div>
"""


def p_own():
    rep = [i for i in OWN["items"] if i["status"] == "repeat"]
    sm = OWN["seams"][0]
    return f"""
<div class="eyebrow">Part Two &middot; building your own</div>
<h2>A pair that is <em>not</em> in the book</h2>
<p class="lede">A client lost her father in the spring and has had panic attacks since the funeral. Grief and Anxiety
is not one of the thirty routes. With the atlas and Sheet 1 it takes about ten minutes.</p>
{K.seq([
    ("b1-sheet", "Take Sheet 1", "Write the two arcs in the first box. Two arcs, so two slots."),
    ("b2-tick", "Order and count", f"Grief sits on the Loss layer, Anxiety on Approach: Grief first (Rule {R.RULE[sm['rule']]['n']}). The atlas cell says {A.overlap('GRF', 'ANX')}."),
    ("b3-row", "Cut and fold", f"The shared skill is the values compass: cut {s(rep[0]['n'])} in Anxiety, review {s(rep[0]['ref'])}."),
    ("b4-file", "Write the seam, file it", f"Seam at week {sm['week']}. Write the bridge, then file the sheet with the notes."),
], h=150)}
{K.figbox(F.strip(OWN, per_row=30), f"<b>The route you just built</b>Grief (sage) then Anxiety (plum): {OWN['total']} sessions become {OWN['length']}. One repeat cut, one ending folded, one seam at week {sm['week']}." + F.strip_key())}
<div class="seamc"><div class="hd">Your seam, written with the three parts<span>{s(sm["last"]["n"])} {K.arrow()} {s(sm["first"]["n"])}</span></div>
<p>&ldquo;{R.bridge(sm)}&rdquo;</p></div>
"""


def p_finder():
    trios = [r for r in CR.ORDERED if len(r["keys"]) == 3]
    tr = [f'<tr><td><span class="sid">{r["num"]:02d}</span> {r["title"]}</td><td class="pg">{K.pg("ra%02d" % r["num"])}</td></tr>' for r in trios]
    trio_rows_a, trio_rows_b = "".join(tr[:4]), "".join(tr[4:])
    return f"""
<div class="eyebrow">Part Two &middot; finding a route fast</div>
<h2>Route finder</h2>
<p>Pairs: find one arc in the rows and the other in the columns. A dark cell is the route number. A pale cell shows
the atlas count for a pair that is not printed &mdash; build it with Sheet 1. Trios are listed underneath.</p>
{K.figbox(F.finder(CR.NUM_OF_PAIR), "<b>Pairs</b>Only the upper half is filled: the order of arcs on a route comes from the ladder, not from which is row and which is column.")}
<div><h3>The eight trios</h3><div class="g2" style="gap:26px"><table class="toc sm">{trio_rows_a}</table><table class="toc sm">{trio_rows_b}</table></div></div>
<div>
  {K.card('<h3>Nothing fits?</h3><p class="small">Four or more arcs: choose the three that keep each other going and hold the rest. Intake and Progress are never part of a route: every route starts after Intake.</p><p class="small" style="margin:0">If the combination includes Trauma Groundwork and memory work is needed, that is a referral, not a longer route.</p>', "tint")}
</div>
"""


def p_op3():
    fams = []
    for fi, (fam, _) in enumerate(T.FAMILIES):
        nums = [r["num"] for r in CR.ORDERED if r["family"] == fi]
        fams.append(f"{fam} &middot; {nums[0]:02d}&ndash;{nums[-1]:02d}")
    return opener("h3-routes", "Part Three", "The thirty routes",
                  "Two pages each: the route explained, and the running order you keep in the file. Grouped by what tends to walk in.",
                  fams)


# ============================================================ sheets ===
def p_sheet1():
    arcs = "".join(f'<span style="white-space:nowrap;margin-right:14px;font-size:12px"><span class="cbx"></span>{A.BY_KEY[k]["short"]}</span>'
                   for k in A.COMBINABLE)
    rep_rows = "".join('<tr><td style="height:27px"></td><td></td><td></td><td></td></tr>' for _ in range(7))
    return f"""<div class="rpage">
<div class="runhead"><div><div class="eyebrow">Sheet 1 &middot; photocopy freely for your own clients</div>
<h2 style="margin:0">Route builder</h2></div>
<div class="rec"><span>Client initials</span><i></i><span>Date</span><i></i></div></div>
<div class="card"><h3><span class="dot">1</span>&nbsp; Tick the arcs (three at most)</h3><div style="line-height:2">{arcs}</div></div>
<div><h3><span class="dot">2</span>&nbsp; Put them in ladder order and write the rule at each join</h3>
<div class="slotrow">
  <div class="slot"><div class="k">Arc 1 &middot; layer</div></div>
  <div style="display:flex;flex-direction:column;justify-content:center;font-size:7.4px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;text-align:center;width:62px">Rule<br><span style="display:inline-block;width:40px;border-bottom:0.8px solid #9AA4A2;height:14px"></span></div>
  <div class="slot"><div class="k">Arc 2 &middot; layer</div></div>
  <div style="display:flex;flex-direction:column;justify-content:center;font-size:7.4px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;text-align:center;width:62px">Rule<br><span style="display:inline-block;width:40px;border-bottom:0.8px solid #9AA4A2;height:14px"></span></div>
  <div class="slot"><div class="k">Arc 3 &middot; layer</div></div>
</div></div>
<div><h3><span class="dot">3</span>&nbsp; Cut the repeats (use the module matrix on page {K.pg("p_modules")})</h3>
<table class="tbl"><thead><tr><th>Shared skill</th><th>Taught in (session)</th><th>Cut (session)</th><th>Review opens (session)</th></tr></thead>
<tbody>{rep_rows}</tbody></table></div>
<div class="g3">
  <div class="slot"><div class="k">Total sessions</div></div>
  <div class="slot"><div class="k">Minus repeats and endings</div></div>
  <div class="slot"><div class="k">Route length and seam weeks</div></div>
</div>
<div class="grow" style="display:flex;flex-direction:column"><h3><span class="dot">4</span>&nbsp; Write each seam: what was built, what comes next needs, the first session</h3>
<div class="lines"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
</div>"""


def p_sheet2():
    def block(n):
        return f"""<div class="card" style="flex:1 1 0;display:flex;flex-direction:column">
<h3>Seam {n}</h3>
<div class="g3" style="gap:10px">
  <div class="slot" style="min-height:46px"><div class="k">Week</div></div>
  <div class="slot" style="min-height:46px"><div class="k">Last session of arc {n}</div></div>
  <div class="slot" style="min-height:46px"><div class="k">First session of arc {n + 1}</div></div>
</div>
<p class="micro" style="margin:8px 0 0">1 &middot; What the client now has, in their words</p><div class="field"></div><div class="field"></div>
<p class="micro" style="margin:8px 0 0">2 &middot; What the next arc needs it for</p><div class="field"></div><div class="field"></div>
<p class="micro" style="margin:8px 0 0">3 &middot; What happens next week</p><div class="field"></div>
<p class="micro" style="margin:8px 0 0">Still fits? <span class="cbx" style="margin-left:6px"></span>Yes &nbsp; <span class="cbx"></span>Rebuild &nbsp; <span class="cbx"></span>Refer &nbsp; &middot; Notes</p>
<div class="lines" style="min-height:40px"><i></i><i></i><i></i></div>
</div>"""
    return f"""<div class="rpage">
<div class="runhead"><div><div class="eyebrow">Sheet 2 &middot; photocopy freely for your own clients</div>
<h2 style="margin:0">Seam planner</h2></div>
<div class="rec"><span>Client initials</span><i></i><span>Route</span><i></i></div></div>
<p class="small" style="margin:0">Fill one block before the last session of each arc. The four questions on page {K.pg("p_stop")} decide the tick box.</p>
<div class="grow" style="display:flex;flex-direction:column;gap:12px">{block(1)}{block(2)}</div>
</div>"""


def p_scope():
    return f"""
<div class="eyebrow">Scope, referral and sources</div>
<h2>What this book does, <em>and what it does not</em></h2>
<div class="g64">
  <div class="stack">
    <p>The Combined Routes organizes the sessions of Session Arc for clients who need more than one arc. It decides
    order, removes repetition and joins arcs. It does not diagnose, it does not assess risk, and it adds no
    intervention that is not already in Session Arc.</p>
    <div class="scope r"><h3>Stop the route and refer when</h3>{K.ticks([
        "there is suicidal thinking, self-harm, or risk to others;",
        "trauma memories intrude and processing is needed (Trauma Groundwork is stabilization only);",
        "compulsions, eating, substance use or gambling reach a level that needs a specialist program;",
        "sleep problems suggest a medical cause (snoring, gasping, leg movements, medication effects);",
        "intimate partner violence is present in a relationship route;",
        "the presentation is outside your license or competence.",
    ])}</div>
  </div>
  {K.capt("p1-refer", 290, "Pause &amp; Refer comes before any route: the call is made, the route waits.")}
</div>
<div class="g2">
  <div class="stack"><h3>Sources</h3>
    <p class="small">Kessler RC, Chiu WT, Demler O, Walters EE. Prevalence, severity, and comorbidity of 12-month
    DSM-IV disorders in the National Comorbidity Survey Replication. <i>Archives of General Psychiatry</i> 2005;62:617&ndash;627.
    Among adults with a disorder in the past year, close to half met criteria for two or more.</p>
    <p class="small" style="margin:0"><b>What it does not say:</b> it measures how often problems occur together.
    It does not say in which order to treat them.</p></div>
  <div class="stack"><h3>What is craft, not evidence</h3>
    <p class="small">The seven ordering rules, the layer ladder, the override and the seam wording are clinical
    conventions written for consistency. They reflect a common sequence in practice &mdash; stabilize, restore basics,
    then ask for effort &mdash; and they are labelled as craft wherever they appear.</p>
    <p class="small" style="margin:0">Client sketches are composites written for this book. Any resemblance to a
    real person is coincidental.</p></div>
</div>
"""


def p_back():
    return f"""<div class="opener">
<div class="img" style="flex-basis:64%"><img src="{K.PHOTO % 'h9-back'}" alt=""></div>
<div style="padding:12mm 17.5mm 14mm;display:grid;grid-template-columns:1.3fr 1fr;gap:24px;flex:1 1 auto">
  <div><div class="brand" style="font-size:9px;font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:#6B7D7E">Session Arc &middot; Companion 01</div>
  <p class="quote" style="font-size:24px;margin-top:10px">One treatment, not three. The right thing first, nothing
  taught twice, and a single ending.</p></div>
  <div style="border-left:0.8px solid #E3DACB;padding-left:18px;align-self:start">
  <p class="small">The Combined Routes is a companion to Session Arc and uses its session numbers throughout.</p>
  <p class="micro" style="margin:0">&copy; Sando LLC. For use by the purchasing clinician. Sheets 1 and 2 may be
  photocopied for that clinician&rsquo;s own clients. Not a substitute for clinical judgment, supervision or
  referral.</p></div>
</div></div>"""
