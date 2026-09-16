# -*- coding: utf-8 -*-
"""The 360 sessions of Session Arc, as data.

Every route, every count in the Overlap Atlas and every cut list in this book is
computed from this file. Each session is (title, module) where module names a
skill that is taught in more than one arc. A module is taught once per arc at
most. None means the session belongs to its arc alone.

The two CLOSE sessions at the end of every arc are the arc's own ending.
"""

MODULES = {
    "NAME": "Naming what you feel",
    "BODY": "Grounding and the breath",
    "WINDOW": "The window of tolerance",
    "CATCH": "Catching the thought",
    "TRAPS": "Thinking traps",
    "VALUES": "Values compass",
    "ACT": "Activity and mood log",
    "SELFC": "Self-compassion",
    "BOUND": "Boundaries",
    "ASK": "Asking clearly",
    "URGE": "Riding the urge",
    "WIND": "Wind-down routine",
    "WORRY": "Worry time",
    "PS": "Problem-solving steps",
    "LADDER": "Building the ladder",
}

ARCS = [
    {
        "key": "INT", "name": "Intake, Alliance & Formulation", "short": "Intake", "start": 1,
        "frame": True,
        "sessions": [
            ("First contact: what brings you here", None), ("The story so far", None),
            ("What a good outcome looks like", None), ("Safety and scope check", None),
            ("History and context", None), ("Strengths and resources", None),
            ("Patterns you have noticed", None), ("A shared picture of the problem", None),
            ("Choosing a first goal", None), ("How we will work together", None),
            ("A first small experiment", None), ("Reviewing the experiment", None),
            ("Values in brief", None), ("The people around you", None),
            ("What gets in the way", None), ("Refining the picture", None),
            ("Agreeing the plan", None), ("Measuring change", None),
            ("The first review", None), ("Setting the course", None),
        ],
    },
    {
        "key": "EMO", "name": "Emotion Regulation", "short": "Emotion Regulation", "start": 21,
        "builds": "a way to name a feeling and bring it down before it runs the day",
        "needs": "enough steadiness to feel something strongly without being swept away",
        "opens": "we start with what emotions are actually for",
        "sessions": [
            ("What emotions are for", None), ("Naming what you feel", "NAME"),
            ("Where it lives in the body", None), ("The window of tolerance", "WINDOW"),
            ("Grounding and the breath", "BODY"), ("The wave: how feelings rise and fall", None),
            ("Triggers and vulnerabilities", None), ("Lowering the baseline", None),
            ("Opposite action", None), ("Riding the urge", "URGE"),
            ("Checking the facts", None), ("The first ten minutes of distress", None),
            ("Soothing with the senses", None), ("Emotions in conversation", None),
            ("After the storm: repair", None), ("Building good experiences", None),
            ("A plan for the hard hours", None), ("Practicing under pressure", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "ANX", "name": "Anxiety & Avoidance", "short": "Anxiety", "start": 41,
        "builds": "a ladder, and proof that fear drops when you stay",
        "needs": "a willingness to move toward discomfort on purpose, one rung at a time",
        "opens": "we look at what the anxiety has been doing for you",
        "sessions": [
            ("What anxiety is doing", None), ("The anxiety cycle", None),
            ("Your alarm map", None), ("Grounding and the breath", "BODY"),
            ("Sensations as signals", None), ("Safety behaviors", None),
            ("Catching the anxious thought", "CATCH"), ("Thinking traps", "TRAPS"),
            ("Probability and cost", None), ("The worst, the best, the likely", None),
            ("Worry time", "WORRY"), ("Living with uncertainty", None),
            ("Mapping what you avoid", None), ("Building the ladder", "LADDER"),
            ("The first rung", None), ("Staying long enough", None),
            ("Rung two: review and adjust", None), ("Dropping one safety behavior", None),
            ("Rung three", None), ("When the ladder stalls", None),
            ("Rung four", None), ("Practicing with body sensations", None),
            ("Being seen: social fears", None), ("Social experiments", None),
            ("Health and body worries", None), ("Panic: understanding the spike", None),
            ("Panic: riding it out", None), ("Rung five", None),
            ("The top of the ladder", None), ("Anxious self-talk", None),
            ("Perfectionism and checking", None), ("Making room for fear", None),
            ("Values as the reason to approach", "VALUES"), ("Unplanned exposures", None),
            ("Anxiety between people", None), ("When stress spills over", None),
            ("Keeping the gains", None), ("Your approach plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "DEP", "name": "Depression & Low Drive", "short": "Depression", "start": 81,
        "builds": "days with some movement in them again, and a log that shows it",
        "needs": "enough energy to act before the mood agrees",
        "opens": "we map how low mood has been keeping itself going",
        "sessions": [
            ("How low mood keeps itself going", None), ("The downward spiral", None),
            ("Activity and mood log", "ACT"), ("What used to matter", None),
            ("Values compass", "VALUES"), ("Small scheduled actions", None),
            ("Mastery and pleasure", None), ("Breaking tasks down", None),
            ("Reviewing the week", None), ("Catching the low thought", "CATCH"),
            ("Thinking traps", "TRAPS"), ("The rumination loop", None),
            ("Getting out of the loop", None), ("Evidence for and against", None),
            ("Balanced thoughts", None), ("Energy and the body", None),
            ("Sleep and mood", None), ("Movement at your pace", None),
            ("Connection when you want to hide", None), ("Asking for support", None),
            ("Problem-solving steps", "PS"), ("Hopelessness", None),
            ("The critic in low mood", None), ("Self-compassion", "SELFC"),
            ("When nothing feels good", None), ("Savoring", None),
            ("Routine as scaffolding", None), ("Avoidance in low mood", None),
            ("Approaching what was postponed", None), ("Core beliefs", None),
            ("Testing a core belief", None), ("Meaning and purpose", None),
            ("Mood and relationships", None), ("Early warning signs", None),
            ("When mood dips again", None), ("The good-day list", None),
            ("Keeping momentum", None), ("Your wellbeing plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "STR", "name": "Stress, Burnout & Boundaries", "short": "Stress & Burnout", "start": 121,
        "builds": "a lighter load and a few limits that actually hold",
        "needs": "some room in the week, so there is space for deeper work",
        "opens": "we measure the load before we try to carry it better",
        "sessions": [
            ("The stress bucket", None), ("Stress in the body", None),
            ("Grounding and the breath", "BODY"), ("The three signs of burnout", None),
            ("Mapping your load", None), ("What you can and cannot control", None),
            ("Thinking traps under pressure", "TRAPS"), ("Problem-solving steps", "PS"),
            ("Boundaries", "BOUND"), ("Saying no", None),
            ("Asking clearly", "ASK"), ("Budgeting time and energy", None),
            ("Recovery activities", None), ("Rest without guilt", None),
            ("Worry time", "WORRY"), ("Wind-down routine", "WIND"),
            ("People-pleasing", None), ("Perfectionism at work and home", None),
            ("Caring without disappearing", None), ("Micro-breaks", None),
            ("Reconnecting with what matters", None), ("Values at work", None),
            ("Renegotiating a role", None), ("Digital load", None),
            ("A recovery week", None), ("Early burnout signals", None),
            ("A sustainable pace", None), ("Your load plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "SW", "name": "Self-Worth & Self-Criticism", "short": "Self-Worth", "start": 151,
        "builds": "a quieter critic and a second, kinder voice to answer it",
        "needs": "a steadier sense of your own worth to bring into the room with other people",
        "opens": "we meet the inner critic and ask what it thinks it is protecting",
        "sessions": [
            ("Where self-worth comes from", None), ("Meeting the inner critic", None),
            ("What the critic protects", None), ("Catching the critical thought", "CATCH"),
            ("Thinking traps about yourself", "TRAPS"), ("Double standards", None),
            ("Self-compassion", "SELFC"), ("The compassionate voice", None),
            ("Core beliefs about yourself", None), ("Collecting counter-evidence", None),
            ("Comparison", None), ("Shame and guilt", None),
            ("Perfectionism", None), ("Mistakes and repair", None),
            ("Body image", None), ("Taking a compliment", None),
            ("Boundaries as self-respect", "BOUND"), ("Asking clearly", "ASK"),
            ("A strengths inventory", None), ("Acting as if", None),
            ("Values over approval", "VALUES"), ("Old family roles", None),
            ("Self-worth in relationships", None), ("Self-care as practice", None),
            ("A new rule to live by", None), ("Testing the new rule", None),
            ("The critic under stress", None), ("Your self-respect plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "REL", "name": "Relationships & Attachment", "short": "Relationships", "start": 181,
        "builds": "a map of your patterns with people and a few secure moves to replace them",
        "needs": "a self that can stay steady when someone else is not",
        "opens": "we draw the map of the people in your life",
        "sessions": [
            ("Your relationship map", None), ("Attachment patterns", None),
            ("What you learned about closeness", None), ("Needs and fears in connection", None),
            ("Naming what you feel", "NAME"), ("The protest cycle", None),
            ("Pursuit and withdrawal", None), ("Reading the other person", None),
            ("Listening to understand", None), ("Asking clearly", "ASK"),
            ("Boundaries", "BOUND"), ("Conflict styles", None),
            ("Repair after a rupture", None), ("Trust", None),
            ("Jealousy and insecurity", None), ("Family of origin", None),
            ("Parents as adults", None), ("Friendships", None),
            ("Loneliness", None), ("New connections", None),
            ("Endings and breakups", None), ("Losing yourself in others", None),
            ("Giving and receiving care", None), ("Vulnerability", None),
            ("Criticism and defensiveness", None), ("Apologizing", None),
            ("Forgiveness", None), ("Intimacy and distance", None),
            ("Relationships and screens", None), ("Family and cultural expectations", None),
            ("People at work", None), ("Choosing your people", None),
            ("Relationship values", "VALUES"), ("Old patterns under stress", None),
            ("Practicing secure moves", None), ("A difficult conversation", None),
            ("Reviewing the map", None), ("Your connection plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "TRA", "name": "Trauma-Informed Groundwork", "short": "Trauma Groundwork", "start": 221,
        "builds": "safety skills and a present-day footing, without going into the memories",
        "needs": "a footing solid enough that reminders do not knock you off it",
        "opens": "we agree what safety means here, and what this work will not do",
        "sessions": [
            ("What trauma-informed means here", None), ("Safety in the room", None),
            ("The window of tolerance", "WINDOW"), ("Grounding and the breath", "BODY"),
            ("Naming what you feel", "NAME"), ("Triggers and reminders", None),
            ("The stress response explained", None), ("Containment skills", None),
            ("A safe-place practice", None), ("Nightmares: first steps", None),
            ("Self-compassion", "SELFC"), ("Shame is not the truth", None),
            ("Trust and people", None), ("Routine as safety", None),
            ("Your support network", None), ("Present-day skills", None),
            ("When memories intrude", None), ("Knowing when to refer", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "GRF", "name": "Grief, Loss & Transition", "short": "Grief", "start": 241,
        "builds": "room for the loss, and a way to carry it into ordinary days",
        "needs": "enough space around the loss that other work does not feel like forgetting",
        "opens": "we start by telling the story of the loss, at your pace",
        "sessions": [
            ("Grief is not a problem to fix", None), ("Telling the story of the loss", None),
            ("Naming what you feel", "NAME"), ("Waves of grief", None),
            ("Activity and mood log", "ACT"), ("Guilt and what-ifs", None),
            ("Anger in grief", None), ("Continuing bonds", None),
            ("Anniversaries and firsts", None), ("Self-compassion", "SELFC"),
            ("Changed roles", None), ("Loss that is not death", None),
            ("Other people's reactions", None), ("Meaning after loss", None),
            ("Values compass", "VALUES"), ("Transitions and identity", None),
            ("Rituals", None), ("Moving with the loss", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "CMP", "name": "Compulsions, Urges & Habit Loops", "short": "Habits & Urges", "start": 261,
        "builds": "a map of the loop and a way to ride an urge without obeying it",
        "needs": "the ability to sit with an urge long enough to choose",
        "opens": "we map the loop: the cue, the urge, the payoff",
        "sessions": [
            ("How habit loops work", None), ("Mapping the loop", None),
            ("Cues and triggers", None), ("The payoff", None),
            ("Riding the urge", "URGE"), ("Grounding and the breath", "BODY"),
            ("Building the ladder", "LADDER"), ("Delay and substitute", None),
            ("Changing the environment", None), ("Response prevention: first steps", None),
            ("Catching the permission thought", "CATCH"), ("A lapse is not a relapse", None),
            ("Shame and secrecy", None), ("Replacement routines", None),
            ("High-risk situations", None), ("Values as the reason to change", "VALUES"),
            ("Support and accountability", None), ("Your habit plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "VAL", "name": "Values, Meaning & Change", "short": "Values & Meaning", "start": 281,
        "builds": "a direction that is yours, and small actions that point at it",
        "needs": "a clear sense of what the effort is for",
        "opens": "we separate what you value from what you have been told to want",
        "sessions": [
            ("What values are, and are not", None), ("Values compass", "VALUES"),
            ("Where life and values drift apart", None), ("Goals versus values", None),
            ("Committed action", None), ("Barriers: fusion and avoidance", None),
            ("Willingness", None), ("Readiness for change", None),
            ("Small experiments", None), ("Choices and trade-offs", None),
            ("Meaning in ordinary days", None), ("Legacy", None),
            ("Your direction plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "ANG", "name": "Anger & Conflict", "short": "Anger", "start": 296,
        "builds": "an early read on anger and a calm plan that works in the moment",
        "needs": "a temper you can see coming before it speaks for you",
        "opens": "we look at what anger is trying to protect",
        "sessions": [
            ("What anger is for", None), ("Your anger map", None),
            ("Naming what you feel", "NAME"), ("The body in anger", None),
            ("Grounding and the breath", "BODY"), ("Catching the hot thought", "CATCH"),
            ("A time-out done right", None), ("Riding the urge", "URGE"),
            ("Asking clearly", "ASK"), ("Conflict without escalation", None),
            ("Repair after an outburst", None), ("Resentment", None),
            ("Your calm plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "SLP", "name": "Sleep, Body & Energy", "short": "Sleep", "start": 311,
        "builds": "steadier nights and a body with some fuel in it",
        "needs": "enough sleep that the brain can learn something new",
        "opens": "we start a sleep diary, because guesses about sleep are usually wrong",
        "sessions": [
            ("How sleep works", None), ("The sleep diary", None),
            ("Your sleep window", None), ("Wind-down routine", "WIND"),
            ("The bed is for sleep", None), ("Worry time", "WORRY"),
            ("Grounding and the breath", "BODY"), ("Energy through the day", None),
            ("Activity and mood log", "ACT"), ("Light, caffeine and screens", None),
            ("Nights that go wrong", None), ("Resting when sleep will not come", None),
            ("Your sleep plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "WRK", "name": "Work, Money & Purpose", "short": "Work & Money", "start": 326,
        "builds": "a working life that fits the person, not the other way round",
        "needs": "a reason to go back into the week that belongs to you",
        "opens": "we look at how work and money became part of who you are",
        "sessions": [
            ("Work, money and who you are", None), ("Mapping the pressure", None),
            ("Money stress", None), ("Problem-solving steps", "PS"),
            ("Boundaries", "BOUND"), ("Values compass", "VALUES"),
            ("Purpose beyond the job", None), ("Career crossroads", None),
            ("Job loss and the search", None), ("Talking with a manager", None),
            ("Imposter feelings", None), ("Money conversations at home", None),
            ("Your work plan", None),
            ("Pulling it together", "CLOSE"), ("The setback plan", "CLOSE"),
        ],
    },
    {
        "key": "PRG", "name": "Progress, Relapse Prevention & Ending", "short": "Progress & Ending", "start": 341,
        "frame": True,
        "sessions": [
            ("How far you have come", None), ("What changed, and what helped", None),
            ("Your early warning signs", None), ("Triggers ahead", None),
            ("The setback plan in detail", None), ("Spacing sessions out", None),
            ("Practicing without the therapist", None), ("Handling a lapse", None),
            ("Changes on the horizon", None), ("Keeping skills alive", None),
            ("Support after therapy", None), ("Unfinished business", None),
            ("Feelings about ending", None), ("A booster plan", None),
            ("Your maintenance plan", None), ("Reviewing the goals", None),
            ("A letter to your future self", None), ("The last month", None),
            ("Saying goodbye well", None), ("After the final session", None),
        ],
    },
]

BY_KEY = {a["key"]: a for a in ARCS}
COMBINABLE = [a["key"] for a in ARCS if not a.get("frame")]


def sid(n):
    return "S%03d" % n


def sessions(key):
    """[(number, title, module)] for one arc."""
    a = BY_KEY[key]
    return [(a["start"] + i, t, m) for i, (t, m) in enumerate(a["sessions"])]


def title_of(n):
    for a in ARCS:
        if a["start"] <= n < a["start"] + len(a["sessions"]):
            return a["sessions"][n - a["start"]][0]
    raise KeyError(n)


def arc_of(n):
    for a in ARCS:
        if a["start"] <= n < a["start"] + len(a["sessions"]):
            return a["key"]
    raise KeyError(n)


def modules(key):
    return {m for _, _, m in sessions(key) if m and m != "CLOSE"}


def overlap(a, b):
    return len(modules(a) & modules(b))


# ---------------------------------------------------------------------------
# The five order-bump columns
#
# One registry, five outputs. Each order bump reads one column below and
# computes its pages, the way OB1 computes its 30 routes from `sessions` and
# MODULES. Nothing is written by hand into a PDF.
#
#   column               keyed by   feeds
#   ------------------------------------------------------------------------
#   sessions[i][1]       session    OB1  The Combined Routes  (shared skill)
#   REQUIRES             session    OB1  prerequisites
#   CHECKPOINT           session    OB2  The Progress Checkpoints
#   BLOCKS               arc        OB3  The Detour Protocols
#   CARD                 session    OB4  Off the Page
#   TRAP                 arc        OB5  The Clinician's Mirror
#
# The four new columns start empty. `selftest` validates whatever is present,
# so they can be filled one arc at a time without breaking a build, and
# `coverage` reports how far along each one is.
#
# Note on authorship: BLOCKS is structural and is computed here. The other
# three carry clinical judgement (what to measure, which line is load-bearing,
# which trap an arc sets) and are left empty on purpose - they are not
# Claude's to invent, and OB2's column needs licensed clinical review before
# it ships.
# ---------------------------------------------------------------------------

# --- OB1: prerequisites ----------------------------------------------------
# session -> tuple of sessions that must land first, within the same arc.
# A shared skill (MODULES) is already an implicit prerequisite handled by the
# route cutter; REQUIRES is for the rest - a session that only works once an
# earlier one has been done. Cross-arc dependencies are expressed as modules,
# not here, because a route may not carry the other arc at all.
#   REQUIRES = {54: (53,)}   "Building the ladder" needs "Mapping what you avoid"
REQUIRES = {}

# --- OB2: checkpoints ------------------------------------------------------
# session -> {"measure": str, "stalled": session, "worse": "B8"}
# Three or four per arc, on real sessions of that arc. `measure` names the
# brief scale or the 0-10 goal-attainment item; `stalled` is the session to
# branch to when the number has not moved; `worse` is always the referral
# route, never a branch inside the arc.
#   CHECKPOINT = {48: {"measure": "GAD-7", "stalled": 46, "worse": "B8"}}
CHECKPOINT = {}

# --- OB3: re-entry blocks --------------------------------------------------
# A detour returns the client to the start of the block they were in, so the
# blocks are what OB3's 24 x 15 table points at. Default: runs of ten, with a
# trailing run kept whole when it reaches half a block. Override an arc here
# when its shape wants different cuts.
BLOCK_SIZE = 10
BLOCK_OVERRIDES = {}   # arc key -> [(letter, first, last), ...]

# --- OB4: glance cards -----------------------------------------------------
# session -> {"anchor": str, "move": str, "bridge": str, "load": (str, ...)}
# The three lines of the card, plus the one or two load-bearing lines that
# have to be said close to verbatim because the exercise depends on that
# exact wording. Everything not in `load` prints as "say it your way".
CARD = {}

# --- OB5: the trap each arc sets -------------------------------------------
# arc key -> {"trap": str, "tell": str, "pauses": (session, session, session)}
# Three review pauses: opening the arc, the middle, and before the close.
# They are pauses, not checkpoints - Mirror measures nothing.
TRAP = {}


def blocks(key):
    """[(letter, first, last)] for one arc. Computed unless overridden."""
    if key in BLOCK_OVERRIDES:
        return list(BLOCK_OVERRIDES[key])
    a = BY_KEY[key]
    n = len(a["sessions"])
    cuts, i = [], 0
    while i < n:
        take = BLOCK_SIZE
        if 0 < n - i - BLOCK_SIZE < BLOCK_SIZE / 2.0:
            take = n - i
        take = min(take, n - i)
        cuts.append((chr(65 + len(cuts)), a["start"] + i, a["start"] + i + take - 1))
        i += take
    return cuts


def block_of(n):
    """(arc key, letter, first, last) for the block a session sits in."""
    key = arc_of(n)
    for letter, first, last in blocks(key):
        if first <= n <= last:
            return (key, letter, first, last)
    raise KeyError(n)


def record(n):
    """Every column for one session, as one dict."""
    key = arc_of(n)
    _, letter, first, last = block_of(n)
    a = BY_KEY[key]
    return {
        "sid": sid(n), "n": n, "arc": key,
        "title": a["sessions"][n - a["start"]][0],
        "module": a["sessions"][n - a["start"]][1],
        "requires": REQUIRES.get(n, ()),
        "checkpoint": CHECKPOINT.get(n),
        "block": (letter, first, last),
        "card": CARD.get(n),
        "trap": TRAP.get(key),
    }


def coverage():
    """(done, total) per column, so a half-filled registry reports itself."""
    every = [n for a in ARCS for n in range(a["start"], a["start"] + len(a["sessions"]))]
    return {
        "REQUIRES": (len(REQUIRES), len(every)),
        "CHECKPOINT": (len(CHECKPOINT), len(every)),
        "BLOCKS": (len(ARCS), len(ARCS)),
        "CARD": (len(CARD), len(every)),
        "TRAP": (len(TRAP), len(ARCS)),
    }


def _text(d, field, where):
    v = d.get(field)
    assert isinstance(v, str) and v.strip(), ("empty or missing text", field, where)


def _check_columns():
    """Validate whatever the five columns hold. Empty is valid; wrong is not."""
    span = {a["key"]: (a["start"], a["start"] + len(a["sessions"]) - 1) for a in ARCS}

    for n, reqs in REQUIRES.items():
        key = arc_of(n)
        assert isinstance(reqs, tuple), ("REQUIRES not a tuple", n)
        for r in reqs:
            assert arc_of(r) == key, ("REQUIRES crosses arcs", n, r)
            assert r < n, ("REQUIRES points forward", n, r)

    seen = {}
    for n, cp in CHECKPOINT.items():
        key = arc_of(n)
        _text(cp, "measure", n)
        st = cp.get("stalled")
        assert arc_of(st) == key, ("CHECKPOINT stalled leaves the arc", n, st)
        assert st != n, ("CHECKPOINT stalls on itself", n)
        assert cp.get("worse") == "B8", ("CHECKPOINT worse must route to B8", n)
        seen[key] = seen.get(key, 0) + 1
    for key, count in seen.items():
        assert 3 <= count <= 4, ("CHECKPOINT wants 3 or 4 per arc", key, count)

    for a in ARCS:
        first, last = span[a["key"]]
        cuts = blocks(a["key"])
        assert cuts[0][1] == first and cuts[-1][2] == last, ("BLOCKS miss the arc", a["key"])
        for (_, _, prev_last), (_, nxt_first, _) in zip(cuts, cuts[1:]):
            assert nxt_first == prev_last + 1, ("BLOCKS not contiguous", a["key"])

    for n, card in CARD.items():
        arc_of(n)
        for field in ("anchor", "move", "bridge"):
            _text(card, field, n)
        load = card.get("load", ())
        assert 1 <= len(load) <= 2, ("CARD wants 1 or 2 load-bearing lines", n, len(load))

    for key, tr in TRAP.items():
        assert key in BY_KEY, ("TRAP on an unknown arc", key)
        _text(tr, "trap", key)
        _text(tr, "tell", key)
        pauses = tr.get("pauses", ())
        assert len(pauses) == 3, ("TRAP wants 3 pauses", key, len(pauses))
        assert list(pauses) == sorted(pauses), ("TRAP pauses out of order", key)
        for p in pauses:
            assert arc_of(p) == key, ("TRAP pause leaves the arc", key, p)


def selftest():
    total, expect = 0, 1
    for a in ARCS:
        assert a["start"] == expect, (a["key"], a["start"], expect)
        expect += len(a["sessions"])
        total += len(a["sessions"])
        mods = [m for _, m in a["sessions"] if m and m != "CLOSE"]
        assert len(mods) == len(set(mods)), ("module twice in", a["key"])
        for m in mods:
            assert m in MODULES, m
    assert total == 360, total
    sizes = {a["key"]: len(a["sessions"]) for a in ARCS}
    assert sizes == {"INT": 20, "EMO": 20, "ANX": 40, "DEP": 40, "STR": 30, "SW": 30,
                     "REL": 40, "TRA": 20, "GRF": 20, "CMP": 20, "VAL": 15, "ANG": 15,
                     "SLP": 15, "WRK": 15, "PRG": 20}, sizes
    _check_columns()
    return total


if __name__ == "__main__":
    print(selftest(), "sessions")
    for m in MODULES:
        print("%-7s %s" % (m, [a["key"] for a in ARCS if m in modules(a["key"])]))
    print()
    for col, (done, total) in coverage().items():
        bar = "#" * round(24 * done / total)
        print("%-11s %3d/%-3d %s" % (col, done, total, bar))
