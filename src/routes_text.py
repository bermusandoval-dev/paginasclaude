# -*- coding: utf-8 -*-
"""The words on the thirty route pages. Everything countable lives in
routes.py; this file holds only what a clinician has to write: who tends to
walk in, what to tell them about the order, and what to watch for.

Client sketches are composites written for this book, not case records.
{w1} and {w2} are replaced with the week each seam falls in.
"""

FAMILIES = [
    ("Mood and energy", "Low mood with something else pulling at it."),
    ("Fear and habit", "Avoidance, worry and loops that keep themselves going."),
    ("Load and the body", "Too much to carry, and a body that is paying for it."),
    ("Loss", "Something ended, and the rest of life is reacting."),
    ("Self and others", "The critic, the temper, and the people who meet both."),
    ("Safety first", "Routes that begin by making the ground steady."),
]

ROUTES = [
    # ------------------------------------------------------------ mood
    {"keys": ["ANX", "DEP"], "family": 0,
     "who": "Marisol, 41, came in for panic on the drive to work. By the third session it was clear "
            "the panic sat on top of two years of flatness: she has stopped cooking, stopped calling "
            "her sister, and sleeps through Saturdays.",
     "say": "You told me two things: the dread, and the flatness underneath it. We start with the "
            "flatness, because the fear work needs energy to push against. The dread is not parked. "
            "Around week {w1} we turn toward it directly.",
     "watch": ["The client asks to start with the panic because it is louder. Borrow one session "
               "(the override) and keep the order.",
               "Anxiety drops a little during the Depression arc. That is activation working, not "
               "a reason to skip the ladder.",
               "Avoidance inside the activity log: planned actions that are all safe. Name it when "
               "you review the week."]},
    {"keys": ["DEP", "SLP"], "family": 0,
     "who": "Ray, 58, retired early and says he is tired all the time. He falls asleep in front of "
            "the television, wakes at 3 a.m. and lies there, and has stopped seeing the friends he "
            "used to golf with.",
     "say": "Before we work on the mood, we fix the nights. A brain that is not sleeping cannot "
            "learn much, and nearly everything in the mood work is learning. Around week {w1} we "
            "start on the days.",
     "watch": ["Daytime naps undo the sleep window. Ask about them every week, not only when the "
               "diary looks bad.",
               "Snoring, gasping or leg movements at night go to a physician before the sleep "
               "window is tightened.",
               "The activity log is taught in the Sleep arc here; in the Depression arc it becomes a "
               "ten-minute review, not a new lesson."]},
    {"keys": ["GRF", "DEP"], "family": 3,
     "who": "Denise, 63, lost her husband fourteen months ago. Her daughter booked the appointment "
            "because Denise has stopped leaving the house except for church, and says she does not "
            "see the point of much anymore.",
     "say": "We start with him, and with the loss. The heaviness you feel grew out of it, and "
            "working on the mood without the grief would feel like being asked to move on. When "
            "there is more room around the loss, around week {w1}, we work on getting your days "
            "moving again.",
     "watch": ["Energy lifting during the Grief arc is not a sign grief is finished. Keep the order.",
               "Anniversaries and holidays can land in the middle of the Depression arc. Expect a "
               "dip and name it in advance.",
               "Hopelessness that includes not wanting to be alive goes to Pause &amp; Refer and your "
               "risk protocol, not to the next session on the route."]},
    {"keys": ["SW", "DEP"], "family": 0,
     "who": "Tomas, 29, describes himself as lazy and a disappointment. He has missed deadlines at a "
            "job he used to like, spends evenings on his phone in bed, and speaks about himself as if "
            "reading a charge sheet.",
     "say": "The voice that calls you lazy is loud, and we will deal with it. First we get some "
            "movement back into your days, so we have evidence to argue with. Around week {w1} we "
            "turn to the critic itself.",
     "watch": ["The critic will grade the activity log. Set the rule early: we record, we do not score.",
               "Self-compassion is taught in the Depression arc here. In the Self-Worth arc it is "
               "reviewed and deepened, not introduced.",
               "If shame blocks the log entirely, borrow Meeting the inner critic early (the override)."]},
    {"keys": ["DEP", "VAL"], "family": 0,
     "who": "Priya, 36, has a good job, a partner and a new apartment, and cannot understand why "
            "she feels empty. She is not sad so much as switched off, and keeps asking what any of "
            "it is for.",
     "say": "We start by getting some life back into ordinary days. Big questions about meaning are "
            "hard to answer from a flat place. Around week {w1} we take those questions seriously, "
            "on steadier ground.",
     "watch": ["The values compass is taught in the Depression arc here; the Values arc builds on it "
               "instead of starting it again.",
               "Clients in this route often want to jump to meaning. Use one Values session as the "
               "override if it keeps them coming.",
               "Watch for big life decisions made in the middle of the mood work. Suggest waiting "
               "until the Values arc."]},
    {"keys": ["ANX", "DEP", "SLP"], "family": 0,
     "who": "Jordan, 33, a night-shift nurse moved to days, lies awake worrying, drags through the "
            "day, and has started calling in sick before shifts they dread. They describe themselves "
            "as wired and empty at the same time.",
     "say": "Three things are tangled here, and they have an order. Nights first, because "
            "everything else needs sleep. Then the days, around week {w1}. Then the dread, around "
            "week {w2}, when you have the fuel to face it.",
     "watch": ["Worry time is taught once, in the Sleep arc. In Anxiety it returns as a ten-minute "
               "review before the ladder.",
               "Shift-work sleep problems may need a medical opinion before the sleep window.",
               "Long routes lose people. Mark the seams with the client as milestones, not as "
               "starting over."]},
    {"keys": ["GRF", "DEP", "SLP"], "family": 3,
     "who": "Luis, 52, whose son died in an accident last year, sleeps three or four hours, has lost "
            "weight, and has gone back to work because he does not know what else to do with the "
            "days.",
     "say": "Your body has been carrying this without rest. We start with sleep so you have "
            "something to carry it with. Around week {w1} we make room for your son and the loss. "
            "Around week {w2} we work on the days that feel empty.",
     "watch": ["Sleep work in early grief is gentle. Do not tighten the sleep window hard while the "
               "loss is this recent.",
               "The activity log is taught in Sleep; it returns in Grief and Depression as review only.",
               "Any talk of joining his son goes to Pause &amp; Refer and your risk protocol immediately."]},
    {"keys": ["DEP", "SW", "VAL"], "family": 0,
     "who": "Hannah, 45, has spent twenty years looking after everyone else. Her youngest has left "
            "home, she feels useless and low, and she keeps saying she never really knew what she "
            "wanted.",
     "say": "We go in three steps. Get your days moving. Then quiet the voice that says you only "
            "count when you are useful, around week {w1}. Then, around week {w2}, work out what you "
            "want the next part of your life to be about.",
     "watch": ["The values compass is taught in Depression; in Self-Worth and Values it is built on.",
               "Values over approval is where old family roles surface. Allow it a session more if needed.",
               "Resist letting the Values arc turn into career coaching. Keep it about direction."]},
    # ------------------------------------------------------------ fear and habit
    {"keys": ["ANX", "SLP"], "family": 1,
     "who": "Mei, 27, a law student, lies awake rehearsing tomorrow, sleeps with the light on, and "
            "gets up exhausted. Her worry about exams has spread into worry about her health.",
     "say": "We start with sleep. Worry is much harder to face on four hours. Around week {w1}, "
            "with steadier nights, we go after the worry itself.",
     "watch": ["Worry time is taught in the Sleep arc here. Its return in Anxiety is a short review.",
               "Health worries can look like sleep complaints. Note the checking behaviors now; they "
               "go on the ladder later.",
               "Exam season can land mid-route. Plan the ladder around it rather than through it."]},
    {"keys": ["ANX", "CMP"], "family": 1,
     "who": "Ben, 38, checks the stove and locks until he is late for everything, and spends an hour "
            "a night reading about illnesses. He knows it makes no sense and cannot stop.",
     "say": "Your checking and your worry run on the same engine. We start with the anxiety, where "
            "you learn to build a ladder and stay with fear. Around week {w1} we use that same ladder "
            "on the habits.",
     "watch": ["The ladder is taught once, in Anxiety. In the Habits arc it is applied, not re-taught.",
               "Reassurance-seeking from you counts as checking. Agree how you will answer it early.",
               "A full compulsive pattern with rituals taking hours a day may need a specialist "
               "exposure program. Check scope with Pause &amp; Refer."]},
    {"keys": ["ANX", "WRK"], "family": 1,
     "who": "Aaron, 31, freezes before meetings, rewrites emails for an hour, and has turned down a "
            "promotion because it involves presenting. He is starting to wonder if he chose the "
            "wrong career.",
     "say": "We start with the fear, because it is making career decisions for you. Around week "
            "{w1}, once it is quieter, we look at the work questions with a clear head.",
     "watch": ["Do not let the Work arc decide the career question while avoidance is still steering.",
               "Presenting and meetings belong on the ladder; use real work situations as rungs.",
               "Values are taught in Anxiety here. In Work &amp; Money they are applied to the job."]},
    {"keys": ["ANX", "CMP", "EMO"], "family": 1,
     "who": "Sasha, 24, picks at her skin when anxious, until it bleeds, then feels so ashamed she "
            "cancels plans. Her feelings go from zero to overwhelming with nothing in between.",
     "say": "First we give you a way to handle feelings that go from zero to a hundred. Then, "
            "around week {w1}, the anxiety. Around week {w2}, the picking, using everything you "
            "have learned by then.",
     "watch": ["Riding the urge is taught in Emotion Regulation. In Habits it is a review, then practice.",
               "Shame and secrecy often keep the habit hidden for weeks. Ask about it gently at each seam.",
               "Skin injury that needs medical care is noted and referred, not managed in session."]},
    {"keys": ["CMP", "EMO"], "family": 1,
     "who": "Kevin, 35, spends money he does not have when he is upset, then hides the statements. "
            "He describes the urge as the only thing that switches the bad feeling off.",
     "say": "The spending is doing a job: switching off a feeling. We start by giving you other "
            "ways to do that job. Around week {w1} we map the habit and take it apart.",
     "watch": ["Money consequences may need practical help alongside therapy. Note it early.",
               "Riding the urge is taught once, in Emotion Regulation.",
               "Gambling that meets criteria for a disorder may need a specialist service. Check scope."]},
    # ------------------------------------------------------------ load
    {"keys": ["STR", "SW"], "family": 2,
     "who": "Grace, 39, a school principal, says yes to everything, works until midnight, and "
            "believes that if she stops she will be found out. She came in after crying in her car "
            "in the parking lot.",
     "say": "We start with the load, because you cannot do deep work on a week with no room in it. "
            "Around week {w1} we look at the voice that says you have to earn your place.",
     "watch": ["Boundaries are taught in the Stress arc here. In Self-Worth they are reframed as "
               "self-respect, not re-taught.",
               "Expect the critic to show up in the load plan. Note it for the second arc.",
               "Clients in this route cancel when they are busiest. Agree a shorter session instead."]},
    {"keys": ["STR", "SLP"], "family": 2,
     "who": "Omar, 47, runs a restaurant, sleeps five hours, drinks coffee until three, and cannot "
            "switch his head off at night. His doctor told him his blood pressure is up.",
     "say": "Your nights and your load are feeding each other. We start with sleep, because it is "
            "the quickest thing to change and it makes everything else easier. Around week {w1} we "
            "work on the load itself.",
     "watch": ["Wind-down and worry time are taught in Sleep; in Stress they come back as review.",
               "Blood pressure and alcohol use belong with the physician. Ask, note and refer.",
               "The client may improve fast on sleep alone. Keep the load arc; the pressure is still there."]},
    {"keys": ["WRK", "STR"], "family": 2,
     "who": "Rachel, 44, was restructured into a job twice the size, is terrified of losing it "
            "because of her mortgage, and snaps at her kids in the evenings.",
     "say": "We start with the load and the limits, because that pressure is running the house. "
            "Around week {w1} we look at work and money directly, including what you want from them.",
     "watch": ["Problem-solving steps are taught in Stress; in Work &amp; Money they are used on real decisions.",
               "Money fear is often concrete. Practical steps (a budget, a conversation) are part of the work.",
               "Irritability at home may point to the Anger arc later. Note it, do not add it yet."]},
    {"keys": ["ANG", "STR"], "family": 2,
     "who": "Mike, 50, a site manager, has had two complaints about shouting at his crew. He says "
            "the job has doubled and nobody listens unless he raises his voice.",
     "say": "We start with the pressure, because a full bucket overflows. Around week {w1} we work "
            "on the anger itself, so you can see it coming.",
     "watch": ["Asking clearly is taught in Stress; in Anger it is practiced under heat.",
               "A workplace disciplinary process may run alongside. Keep notes factual.",
               "Any threat or violence goes to Pause &amp; Refer and your safety protocol."]},
    {"keys": ["STR", "SW", "SLP"], "family": 2,
     "who": "Chloe, 32, a junior doctor, works long shifts, sleeps badly, and cannot forgive herself "
            "for mistakes that her supervisors call ordinary.",
     "say": "Three steps. Sleep first. Then the load and the limits, around week {w1}. Then the "
            "voice that treats every mistake as a verdict, around week {w2}.",
     "watch": ["Rotas can make a sleep window impossible. Adapt it to the shift pattern; do not abandon it.",
               "Boundaries are taught in Stress and reframed in Self-Worth.",
               "Professional health programs may be a better fit if impairment is involved. Check scope."]},
    {"keys": ["WRK", "STR", "VAL"], "family": 2,
     "who": "Daniel, 55, has worked for the same company for thirty years, is burned out, and has "
            "been offered early retirement. He does not know who he would be without the job.",
     "say": "First we lower the load so you can think. Around week {w1} we work out what matters to "
            "you apart from the job. Around week {w2} we bring that back to the decision about work.",
     "watch": ["Values are taught in the Values arc here; in Work &amp; Money they are applied to the offer.",
               "Do not rush the retirement decision. The route is designed to reach it last.",
               "Problem-solving is taught in Stress and used on the real decision in Work &amp; Money."]},
    # ------------------------------------------------------------ loss
    {"keys": ["GRF", "SLP"], "family": 3,
     "who": "Anita, 70, whose sister died in the spring, cannot sleep in the bedroom they shared on "
            "visits, and naps in a chair during the day.",
     "say": "We start with your nights, gently, because you are exhausted. Around week {w1} we "
            "make room to talk about your sister and what the loss has changed.",
     "watch": ["Keep sleep work gentle in recent loss; comfort matters more than a strict window.",
               "The activity log is taught in Sleep and reviewed in Grief.",
               "Older adults: check medications and health changes that affect sleep with their physician."]},
    {"keys": ["GRF", "REL"], "family": 3,
     "who": "Nadia, 34, ended an eight-year relationship. She grieves it, and at the same time keeps "
            "texting him, and has started dating someone who treats her the same way.",
     "say": "We start with the ending, because it has not been grieved yet. Around week {w1} we look "
            "at the pattern with people, so the next relationship is a choice.",
     "watch": ["Naming what you feel is taught in Grief; in Relationships it is reviewed.",
               "Contact with the ex will keep reopening the loss. Agree what you will track.",
               "If the new relationship involves control or violence, safety comes before the route."]},
    # ------------------------------------------------------------ self and others
    {"keys": ["REL", "ANG"], "family": 4,
     "who": "Chris, 42, says his marriage is one argument away from over. He goes quiet, then "
            "explodes, then apologizes, and his wife has stopped accepting the apologies.",
     "say": "We start with the anger, so you can see it coming before it speaks for you. Around week "
            "{w1} we work on the relationship pattern that it has been running inside.",
     "watch": ["This is individual work. If couples work is needed, refer rather than convert the route.",
               "Asking clearly is taught in Anger; in Relationships it is reviewed and applied.",
               "Screen for intimate partner violence before and during. Safety overrides the route."]},
    {"keys": ["REL", "SW"], "family": 4,
     "who": "Leah, 28, picks partners who make her feel lucky to be there, and stays long after she "
            "is unhappy. She says she is too much and not enough at the same time.",
     "say": "We start with how you see yourself, because that is what you bring into every "
            "relationship. Around week {w1} we look at the patterns with people.",
     "watch": ["Boundaries and asking clearly are taught in Self-Worth; in Relationships they are reviewed.",
               "The client may end a relationship mid-route. Treat it as material, not a derailment.",
               "Attachment work stirs family history. Keep Trauma Groundwork in mind if it floods."]},
    {"keys": ["REL", "ANG", "EMO"], "family": 4,
     "who": "Jess, 26, has lost two friendships and a job over outbursts she regrets immediately. "
            "Her feelings flood fast, and she is terrified of being left.",
     "say": "Three steps. First, a way to handle feelings that flood. Then the anger, around week "
            "{w1}. Then the fear of being left and the pattern it creates, around week {w2}.",
     "watch": ["Naming, grounding and riding the urge are taught in Emotion Regulation and reviewed after.",
               "Self-harm or suicidal behavior goes to Pause &amp; Refer and your risk protocol.",
               "A pattern this intense may fit a specialist program. Check scope before committing to the route."]},
    {"keys": ["EMO", "ANG"], "family": 4,
     "who": "Andre, 19, punched a wall at college and was referred by student services. He says "
            "anger is the only feeling he has, and he does not know where it comes from.",
     "say": "We start by finding the feelings under the anger, and ways to bring them down. Around "
            "week {w1} we work on the anger directly.",
     "watch": ["Grounding, naming and riding the urge are taught once, in Emotion Regulation.",
               "College processes may require attendance records. Clarify what is shared.",
               "Weapons, threats or violence go to Pause &amp; Refer and your safety protocol."]},
    {"keys": ["EMO", "REL"], "family": 4,
     "who": "Sofia, 37, feels everything too much in relationships: a late reply ruins her day, and "
            "she has ended things before the other person could.",
     "say": "We start with the feelings, so a late text does not have to ruin the day. Around week "
            "{w1} we look at the pattern with people that the feelings have been driving.",
     "watch": ["Naming what you feel is taught in Emotion Regulation; in Relationships it is reviewed.",
               "Expect the pattern to show up with you. Name it kindly when it does.",
               "If attachment history includes trauma, keep Trauma Groundwork available."]},
    # ------------------------------------------------------------ safety
    {"keys": ["EMO", "TRA"], "family": 5,
     "who": "Kim, 40, was in a serious car crash two years ago. Loud noises send her heart racing, "
            "she avoids driving, and she swings between numb and overwhelmed.",
     "say": "This work is about safety and steadiness in your life now, not about going back into "
            "the crash. We start with ways to bring big feelings down. Around week {w1} we build "
            "the footing around reminders.",
     "watch": ["Trauma Groundwork is stabilization. Memory processing is a referral, not the next arc.",
               "Grounding, naming and the window of tolerance are taught in Emotion Regulation.",
               "Driving avoidance can go on a ladder only after stabilization, and within scope."]},
    {"keys": ["TRA", "SLP"], "family": 5,
     "who": "Eli, 45, a veteran, sleeps with the television on, wakes from nightmares, and is so "
            "tired he has started missing work.",
     "say": "We start with safety and steadiness in the present, so the nights have something to "
            "stand on. Around week {w1} we work on sleep itself.",
     "watch": ["Nightmares: first steps is groundwork only. Specialist treatment for nightmares is a referral.",
               "Grounding is taught in Trauma Groundwork and reviewed in Sleep.",
               "Alcohol used to sleep is common in this route. Ask, and refer when needed."]},
    {"keys": ["TRA", "REL"], "family": 5,
     "who": "Aisha, 31, grew up in a chaotic home. She wants closeness and pulls away the moment she "
            "has it, and does not trust anyone who is kind to her.",
     "say": "We start with safety and steadiness, without going into the past. Around week {w1} we "
            "look at the pattern with people, with that footing under you.",
     "watch": ["Attachment work can bring memories forward. Return to Groundwork skills; refer for processing.",
               "Naming what you feel is taught in Groundwork and reviewed in Relationships.",
               "Trust in you will be tested. Repair after a rupture may be needed earlier than planned."]},
    {"keys": ["EMO", "TRA", "SLP"], "family": 5,
     "who": "Marcus, 36, a paramedic, has stopped sleeping more than a few hours since a call that "
            "went badly. He is irritable, flat and jumpy, and does not want to talk about the call.",
     "say": "You do not have to talk about the call. We start with ways to bring the feelings down. "
            "Around week {w1}, the footing in the present. Around week {w2}, the nights.",
     "watch": ["Grounding and the breath is taught once, in Emotion Regulation, and reviewed twice after.",
               "First-responder peer programs and occupational health may be part of the plan.",
               "Any sign of intrusive memories worsening goes to Pause &amp; Refer for a specialist opinion."]},
]


def selftest():
    import routes as R
    seen = set()
    for i, r in enumerate(ROUTES, 1):
        k = tuple(sorted(r["keys"]))
        assert k not in seen, k
        seen.add(k)
        b = R.build(r["keys"])
        need = len(b["seams"])
        for w in ("{w1}", "{w2}"):
            if w in r["say"]:
                assert int(w[2]) <= need, (i, w)
        assert ("{w%d}" % need) in r["say"], (i, "say must name the last seam")
        assert len(r["watch"]) == 3, i
    assert len(ROUTES) == 30, len(ROUTES)
    return len(ROUTES)


if __name__ == "__main__":
    print(selftest(), "routes ok")
