# Rubric: Coherence

Each turn builds on the ones before it. This is about conversational logic, not
voice — tone cannot catch it, because every sentence flagged here can be
perfectly well written on its own.

## The rule

1. **Nothing arrives cold.** Do not introduce a concept, skill, file or term
   with no prior grounding and no stated reason it matters to this user right
   now. If the user has never heard of `/today`, do not justify a decision by
   what `/today` will do with it.

2. **Recent context outweighs old context.** The user's latest few turns are
   the live thread. Do not keep pushing an earlier topic they have not signalled
   they still care about, and do not answer the question they asked three turns
   ago instead of the one they just asked.

3. **Do not repeat yourself.** The same point, caveat or phrasing landing twice
   across adjacent turns reads as not having tracked what was already said.

4. **Do not contradict yourself.** Two turns asserting incompatible things about
   the same subject. Where the contradiction is factual, it is also a
   groundedness violation — file it in both, they measure different things:
   groundedness asks whether a claim had a source, coherence asks whether the
   conversation held together.

5. **Vocabulary stays stable.** The same concept keeps the same name across
   skills. Introducing a second name for something already named, without
   bridging them, is a coherence failure even when both names are defensible.

## How to report findings under this rubric

One bullet per instance: the turn number, the quote, the rule number, and one
sentence on what the user is left holding. Where the problem is a relationship
between two turns, quote both.

## Verdict

Holistic, not a count. Ask the question directly: reading this as the user,
would the conversation have felt disjointed?

Three small nitpicks can be a **PASS**. One genuinely disorienting moment — a
term the user cannot resolve, a thread that jumps without warning, a
contradiction they would have to stop and reread — is a **FAIL**.

State the reasoning in one sentence alongside the verdict, so a disagreement
can be resolved without re-reading the whole transcript.

## Worked examples

**Violation — a concept arriving with no grounding.**
"Vague dates make `/today`'s countdown noisy." At this point in the run the
user has never seen `/today` and has no idea what countdown means. The sentence
is clear, correct and useless: it justifies a request with machinery the user
cannot evaluate. (Rule 1.)

**Violation — two undefined terms plus an unmentioned file.**
"Lock the first week of your strategy — set anti-goals and a founder-outreach
cadence in `strategy.md`." Strategy has not come up, anti-goals are undefined,
founder outreach is undefined, and the user is being asked to act on all three.
(Rule 1.)

**Violation — a second name for the same thing.**
`/job-search` labels roles tier-1 / tier-2 / tier-3; `/today` labels the same
roles P0 / P1 / P2, with no line connecting them. Each skill is internally
consistent, which is why tone passes it and coherence does not. (Rule 5.)

**Violation — the same beat twice.**
Turns 1 and 2 both land "same questions, you just type more" almost verbatim.
Individually fine; adjacent, it reads as not having noticed. (Rule 3.)

**Not a violation — a deliberate recap.**
Restating where things stand after a long branch, or before asking the user to
decide, is orientation rather than repetition. The test is whether it adds
something at the point it appears.

**Not a violation — introducing a term you then define.**
Naming a concept and immediately explaining why it matters to this user is
exactly rule 1 being satisfied, not a near miss. Do not flag it.
