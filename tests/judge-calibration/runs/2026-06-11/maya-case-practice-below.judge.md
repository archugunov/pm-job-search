# Findings — maya-case-practice-below

**Run date:** 2026-06-11
**Snapshot:** maya-active

## Verdict

**Overall: PASS**

- Hard violations: PASS
- Spec gaps: PASS
- Soft issues: 2 (advisory)
- Open critiques: 3 (advisory)

## Hard violations (lint checklist)

No hard violations found.

- Rule 1 (fenced blocks as chat summaries): clean — Turn 8 uses a `##` heading "Batch 2 — 4/4", no triple-backtick summary blocks. The only backticks render inline file paths (`<workspace>/userdata/case-practice/2026-06-11-mc-drill.md`, `interviewer-simulator`) which is permitted.
- Rule 2 (two unrelated asks): clean — every assistant message ends with a single ask ("Reply with your four picks", "Another batch, or wrap up?").
- Rule 3 (non-existent skill/file): clean — `interviewer-simulator` agent and the session log path both resolve.
- Rule 4 (hardcoded numbers): the 80% gate is a methodology constant for this skill, not a cadence sourced from strategy.md — not a violation.
- Rule 5 (prior-state on first run): clean — opens with mix + format, no "since last time" framing.
- Rule 6 (internal jargon leak): clean — "NSM", "JTBD", "RICE", "HoP altitude" are domain terms a PM target audience reads natively, not plugin-internal labels like `meta.md` or `tier_weights`.
- Rule 7 (schema drift): SCHEMA VALIDATION block reports "No schema drift found."

## Soft issues (TONE voice + UX)

- **Turn 4 distractor analysis for Q2 misaligns with the options actually shown.** The question's options were A (brainstorm hypotheses), C (interview 10 free users), D (compare premium feature usage between converters/non-converters). The feedback in Turn 4 critiques "A (run an A/B test on a simpler flow)" and "D (compare engaged-vs-churned usage)" — neither matches the option text the user read. A user re-reading the question and feedback would notice the mismatch and lose trust. Same pattern in Turn 8 Q7 feedback ("B is the App Store change story") referring to a "competitor cashback promotion" option — close but not verbatim. Voice issue: precision broke.
- **Turn 10 closer ends on a recommendation chain ("free-form generation drill (roadmap), or run the `interviewer-simulator` agent")** which is two next-step options rather than one direct nudge. Not a Rule A violation (it's a single sentence offering a choice, like "another batch or wrap up?"), but borderline — the closer could have committed to one.

## Spec gaps

### Required (10/10 in scope passed)

- End-of-run nudge: PASS — Turn 10 offers "free-form generation drill (roadmap), or run the `interviewer-simulator` agent for a live product-case mock", context-aware off the cleared gate.
- No prior-state leak: PASS — first run, no past-activity references.
- No dead ends: PASS — every turn ends with a clear ask or a written artefact + nudge.
- Profile/strategy not silently overwritten: NOT EXERCISED — skill didn't write to those files.
- JD link in three places: NOT EXERCISED — /job-search did not run.
- Opens with mix + format, no preamble: PASS — Turn 2 opens with "Mix: weighting product-sense and metric calls heaviest…" + "Format: batches of 4, single-select."
- Scenario + 4 distinct options, one strongest: PASS — all 8 questions follow this shape.
- Pattern-1 feedback (✓ right, ✗ named failure mode per distractor, batch-level senior pattern): PASS — every batch uses ✓/✗ glyphs with named failure modes ("vanity surface metric", "gameable volume", "setup-event metric", "solution-disguised-as-need", "leaf-that-isn't-a-lever", "junior tell", "oracle trap"). Batch-level pattern stated in Turn 4 ("you've locked NSM form and diagnostic discipline cleanly. The altitude gap is the one to watch") and Turn 8 ("Anchors locking in: RICE-as-input-not-oracle…").
- Running score after each batch: PASS — Turn 4 "Running score: 3/4 (75%). Gate is 80%." and Turn 8 "Running score: 7/8 (87.5%) — gate met (≥80%)."
- Stop offered at each batch boundary: PASS — Turn 4 and Turn 8 both close with "Another batch, or wrap up?"
- On close: 4-6 verbatim anchors: PASS — Turn 10 lists 6 anchors (NSM form, drop-to-diagnose, RICE-as-input, JTBD stakes, HoP altitude, disagree-with-CEO modelling), each 8-15 words.
- On close: final score vs 80% gate: PASS — "Final score: 7/8 (87.5%) — gate met."
- Session log written matching template: PASS — Turn 10 confirms write to `userdata/case-practice/2026-06-11-mc-drill.md`.
- Gate-not-met nudge variant: NOT EXERCISED — per judge note, final score 87.5% is above the 80% gate, so the gate-not-met branch precondition does not fire.
- No fabricated company internals: PASS — Monzo savings pots, Strava RICE, Revolut card volume, Spotify JTBD are all framed as scenarios ("You're picking the north star metric for…", "You're Head of Product at Strava") not as factual claims about those companies' internal state.

### Opportunistic (3/3 in scope passed)

- Mix statement reflects HoP-altitude weighting: PASS — Turn 2 explicitly names "prioritisation and behavioural-altitude calls layered in for the Head-of-Product / Lead PM end of your target range" — directly maps to Maya's target range in profile.md.
- AskUserQuestion fallback: PASS — used lettered list with single-string reply format ("reply with picks (a letter or number per question)"), graceful degradation.
- Anchors are concrete and memorisable: PASS — "A drop is a diagnosis, not a roadmap — segment before you solve" and "RICE is an input to judgement, not the oracle" are quotable, not abstract.

## Open critique

- The Q2 and Q7 distractor-feedback drift (critiquing options that don't match the option text presented) is the one real crack in this run. It doesn't break the journey but it would erode a careful reader's confidence — the assistant looks like it's pattern-matching its critique template rather than reading the options it just wrote.
- Turn 4's "Senior pattern across the batch" framing is strong and earns its altitude observation about Q4. Turn 8's equivalent ("Anchors locking in:") is shorter and reads more like a list dump than a synthesis — slight tonal drop between batches.
- The Q4 post-mortem in Turn 10 is genuinely good — it does the work of explaining WHY HoP altitude differs from Senior PM altitude ("capital, headcount, and the rules the org runs by — not the surface area of a single product"). That's the kind of close that justifies the gate-met framing.
