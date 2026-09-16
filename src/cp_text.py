# -*- coding: utf-8 -*-
"""The written part of The Progress Checkpoints: what cannot be computed.

checkpoints.py knows where the checkpoints fall and what the arithmetic says.
It cannot know that a rising PCL-5 in a stabilization arc is the reading you
most want, or that grief does not fall on your schedule. That is here.

Three cautions per arc. Each one names a way the number can be true and the
conclusion still wrong, because a book that teaches a therapist to trust a
number owes them the list of times not to.
"""

WATCH = {
    "INT": (
        "The first reading is a starting line, not a result. Nothing has been "
        "treated yet, so a low number at the first checkpoint says only that the "
        "client came.",
        "A client sent by someone else &mdash; a physician, a court, a spouse &mdash; often "
        "rates the goal the referrer wants. Ask whose goal it is before you write it down.",
        "If the goal item cannot be written at all, the trouble is the formulation, "
        "not the client. Go back and share the picture again.",
    ),
    "EMO": (
        "Clients rate regulation from the calm of your room. Ask for last week&rsquo;s "
        "worst hour, not for how they feel sitting with you.",
        "A worse reading here often means the client is noticing more, not coping less. "
        "Check whether naming has got sharper before you read the fall as deterioration.",
        "These skills go first under lost sleep and alcohol. Read the last checkpoint "
        "with the week&rsquo;s sleep in front of you.",
    ),
    "ANX": (
        "A falling GAD-7 beside a flat goal item usually means avoidance is working. "
        "The client has arranged a quiet week, and quiet weeks score well.",
        "Ask what they did, not how they felt. Anxiety ratings fall the moment exposure "
        "stops, which is the one time you least want to be reassured.",
        "At the second checkpoint the commonest cause of a flat line is a rung that was "
        "too big, not a client who would not climb.",
    ),
    "DEP": (
        "Item 9 of the PHQ-9 is not part of this checkpoint. Any answer above zero goes "
        "to B8 and your local protocol before the rest of the sheet is discussed at all.",
        "Behavioral activation moves the goal item weeks before it moves the PHQ-9. "
        "Expect the two lines to separate, and say so to the client when they do.",
        "A client who reports doing everything and feeling nothing is often protecting "
        "you from disappointment. Ask to see the log.",
    ),
    "STR": (
        "Load only falls when something is put down. If the number moved but nothing "
        "left the list, ask the question again a different way.",
        "A quiet week or a holiday flatters this arc badly. Read every number against "
        "what the week actually contained.",
        "Someone genuinely burned out often cannot rate anything by Friday. Take the "
        "reading mid-week where the schedule allows it.",
    ),
    "SW": (
        "Self-criticism scores fall when a client wants to please you, and this is the "
        "client most likely to want that. The item asks about the week, not about progress.",
        "A worse reading at the shame checkpoint is ordinary and is not deterioration: "
        "naming shame raises it before it settles.",
        "Watch for the client who scores well and describes a week you would not wish "
        "on anyone.",
    ),
    "REL": (
        "You are reading one side of a relationship. The number tells you what your "
        "client did, not whether things between them improved.",
        "A break-up in the middle of the arc moves every number at once. Write the event "
        "on the chart or the line will mislead you a month later.",
        "Clients rate &ldquo;asking clearly&rdquo; by whether they got what they asked "
        "for. Rate the asking.",
    ),
    "TRA": (
        "This arc is stabilization, not treatment of the memories. A rising PCL-5 is the "
        "reading this book most wants you to act on, not the one to wait out.",
        "Never take the reading in a session where reminders have been opened. Read it "
        "at the start, before anything is stirred.",
        "A flat score beside better daily function is a good outcome here. Ask about the "
        "week as well as the sheet.",
    ),
    "GRF": (
        "A flat line in the early weeks of grief is not a stall. Grief is not a symptom, "
        "and it does not fall on your schedule.",
        "Anniversaries and firsts move this number more than anything you do. Mark them "
        "on the chart in advance.",
        "Read &ldquo;no change&rdquo; against function &mdash; sleeping, eating, getting "
        "to work. Those move first, and they move before the feeling does.",
    ),
    "CMP": (
        "Urges appear to rise once a client starts counting them. The first reading after "
        "the loop is mapped is usually the most honest one, not the worst week.",
        "A falling count beside unchanged avoidance means the environment changed, not "
        "the habit. Ask what they stopped going near.",
        "Ask for the count. An impression of &ldquo;better&rdquo; is not a reading.",
    ),
    "VAL": (
        "This arc&rsquo;s number moves quickly and means little alone. Read it beside "
        "what the client actually did that week.",
        "A high score with no action is a conversation about willingness, not a result.",
        "A client raised to defer will name other people&rsquo;s values as their own and "
        "rate them honestly. Ask who in their life would disagree with the answer.",
    ),
    "ANG": (
        "Anger ratings drop after a calm week and tell you nothing about a bad one. Ask "
        "for the worst single incident, not the average.",
        "If anyone else is at risk, this is not a checkpoint at all. Go to B8 and your "
        "local protocol.",
        "Repair is far easier to rate well than restraint. Read the second checkpoint "
        "with the other person&rsquo;s account in mind, where you have one.",
    ),
    "SLP": (
        "Sleep efficiency is the diary divided, not the client&rsquo;s impression of the "
        "week. No diary, no reading &mdash; use the goal item alone and say so.",
        "Efficiency climbs as time in bed is cut, before total sleep rises at all. The "
        "client will feel worse first and will tell you so at exactly this checkpoint.",
        "One bad night cannot move a weekly average. If the average moved, something "
        "larger did.",
    ),
    "WRK": (
        "These numbers follow events &mdash; a review, a resignation, a bill. Write the "
        "event on the chart beside the dot.",
        "A client who cannot change the job may still move the goal item. Read it as fit, "
        "not as escape.",
        "Money stress does not answer to insight. If the number will not move, ask "
        "plainly what is owed and to whom.",
    ),
    "PRG": (
        "The last reading has to be comparable with the first. If the instrument changed "
        "during treatment, write that on the chart rather than joining the dots.",
        "Holding at target is the result this arc exists to produce. A flat line at nine "
        "is not a stall, and the rule on page %s says so.",
        "A number that falls as the ending approaches is usually about the ending. Name "
        "that, rather than quietly extending the work.",
    ),
}

# What the therapist did at the checkpoint that decided the case. The sessions
# are not named here -- the page computes them from the registry, so a branch
# renamed in arcs.py cannot leave a stale session number in this sentence.
CASE_NOTE = {
    "INT": "He had not done the between-session task and said so flatly. Rather than "
           "read that as refusal, the plan went back to a smaller experiment agreed "
           "in the room.",
    "EMO": "Nothing needed deciding: she was using a skill in the first ten minutes by "
           "the second checkpoint, and the last reading held under a genuinely bad week.",
    "ANX": "Two rungs in and the fear was not dropping, because she was leaving the "
           "restaurant at the first wave. The branch was the arc&rsquo;s own session "
           "for a ladder that has stopped moving.",
    "DEP": "The third reading fell four points below the second on the goal item and "
           "her PHQ-9 had climbed. That is the rule&rsquo;s third outlet, and it was "
           "taken the same day.",
    "STR": "Her first checkpoint moved nothing: she had agreed the plan and changed "
           "none of the week. The branch went back to what was actually inside her "
           "control before any more of it was scheduled.",
    "SW": "The stall came where it usually comes, at the point where values start to "
          "cost approval. Counter-evidence had been collected but never used out loud.",
    "REL": "He could describe the pattern and not interrupt it. The branch was repair, "
           "which gave him something to do after the pattern rather than instead of it.",
    "TRA": "Straightforward, and worth showing for that reason: three readings, each "
           "one better, in an arc where the book&rsquo;s main worry is the opposite.",
    "GRF": "Eleven months in, the first checkpoint did not move, and that was correct. "
           "The branch was the session on the waves themselves, not a change of plan.",
    "CMP": "Counting made the second reading look worse than the first felt. The branch "
           "was response prevention, begun small, and the last reading moved three points.",
    "VAL": "No decision needed. Worth reading anyway for how fast this arc&rsquo;s "
           "number rises, and how little that would mean without the actions beside it.",
    "ANG": "He caught it early twice in the week before the second checkpoint, which is "
           "what the item asks about. No branch was needed and none was invented.",
    "SLP": "Efficiency had not moved because time in bed had not been cut. The branch "
           "was the session that does exactly that, and the client felt worse for nine "
           "days before the number moved.",
    "WRK": "The first checkpoint was flat because nothing had happened yet: he had not "
           "had the conversation. The branch put the problem-solving steps back in "
           "front of him before the arc went on.",
    "PRG": "Two readings that did not move by two points, and both of them on track. "
           "This is the case the ceiling clause was written for.",
}
