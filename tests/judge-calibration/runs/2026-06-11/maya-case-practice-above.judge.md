# Findings — maya-case-practice-above

**Run date:** 2026-06-11
**Snapshot:** maya-active

## Verdict

**Overall: PASS**

- Hard violations: PASS
- Spec gaps: PASS
- Soft issues: 2 (advisory)
- Open critiques: 4 (advisory)

## Hard violations (lint checklist)

No hard violations found.

- No fenced code blocks used as chat summaries (Turn 4, 8, 10 use plain prose with bullets).
- No two-unrelated-asks pattern; each batch terminates with a single "Reply with your four picks" or "Another batch, or wrap up?"
- No reference to non-existent skills/files; Turn 10 cites `<workspace>/userdata/case-practice/2026-06-11-mc-drill.md`, matching the spec's session-log template path.
- No hardcoded cadence numbers; the 80% gate is the methodology constant, not a strategy.md cadence.
- No prior-state prompts on first run.
- No internal jargon leak (e.g., no "Pattern-1 feedback," "MC-able," "drill 1" leaking into user copy).
- SCHEMA VALIDATION confirms no drift; case-practice writes no meta.md.

## Soft issues (TONE voice + UX)

- **Sub-agent quote-fidelity drift in Turn 8 scoring (recurring).** The scoring re-writes option text rather than quoting verbatim from Turn 6. Concrete examples:
  - Q7 option B was posed as "Ship the second-ranked item (a permissions overhaul, RICE 180) instead of the top-ranked Slack integration (RICE 240), because the enterprise sales team has lost three deals this quarter to permissions gaps..." (Turn 6) but scored against an entirely different invented text: "Push back: the RICE 'reach' for enterprise admin features is wrongly scoped — it counts admins, not the dollar-weighted accounts they gate. Re-score with revenue-at-risk; the admin feature likely jumps. Also flag to the team that we just lost two enterprise deals citing this gap." (Turn 8). Distinct framing, distinct numbers (three deals → two deals), invented "AI" reference.
  - Q8 option B in Turn 6: "collapsing two squads into a single activation pod ... 60% of our roadmap items were duplicative cross-squad work. Six months in, activation moved 8 points and platform velocity doubled." Turn 8 paraphrased: "Collapsed two squads into one after realising both were building duplicative onboarding flows ... activation rose 18% the following quarter." Different metric (8 points → 18%), different framing (activation ownership → onboarding flows), different time horizon (six months → following quarter).
  - Q5 option D drift: "Number of templates published to the gallery per week" (Turn 6) → "Number of templates published in the gallery" (Turn 8).
  - Q6 option C drift: "Users want more gamification because gamification drives engagement, so we should add more streaks, leagues, and badges" (Turn 6) → "Learners want to feel engaged and motivated through gamification mechanics" (Turn 8). Completely re-framed.
  This is a TONE precision issue — the user is being scored on options that look unfamiliar versus what they answered against, which undermines anchor-locking. Recurring per memory notes on sub-agent fidelity drift.

- **Q2 Turn 4 distractor D scoring is muddled.** Turn 4: "directionally plausible and not wrong, but it's one specific hypothesis without segmentation behind it. You arrive at D *after* B's cut, not instead of it." Naming a distractor "not wrong" reads as hedging given the spec's "exactly one strongest" requirement; it weakens the cleanliness of the failure-mode framing the rest of the batch holds.

## Spec gaps

### Required (10/10 in scope passed)

- One-line mix statement + one-line format statement, no preamble: PASS. Turn 2 opens "Mix this round: two product-sense calls, one prioritisation, one behavioural-altitude — weighted for the senior/Head-of-Product end of your target range. / Format: four questions, single-select A-D, scored after you reply with all four picks."
- Scenario + 4 distinct options, exactly one strongest: PASS across Q1–Q8.
- Pattern-1 feedback after each batch: PASS. Turn 4 and Turn 8 both name the failure mode per distractor (e.g., "feature-maturity fatalism," "single-hypothesis anchoring," "spreadsheet-obeying," "process-fiddling") and surface a batch-level senior pattern.
- Running score after each batch: PASS. Turn 4 "Running score: 4/4 (100%)"; Turn 8 "Running score: 8/8 (100%). Gate met."
- Stop offered at each batch boundary: PASS. Turn 4 and Turn 8 close with "Another batch, or wrap up?"
- On close: 4-6 short verbatim anchors (5-15 words each): PASS. Turn 10 lists 6 anchors, each 7-12 words.
- Final score vs ≥80% gate: PASS. Turn 10 "Final score: 8/8 (100%) — gate met."
- Session log written: PASS per Turn 10 path reference.
- Gate-met nudge variant fires: PASS. Turn 10 closes "You've cleared the recognition gate. Next: a free-form generation drill (roadmap construction end-to-end), or run the interviewer-simulator agent for a live product-case mock with pushback."
- No fabricated company internals: PASS. Examples are scenario-shaped (Monzo round-ups, Spotify UK WoW drop, Notion NSM, Duolingo streak) without claiming specific internal metrics as real.

### Opportunistic (4/4 in scope passed)

- Mix statement reflects HoP altitude weighting: PASS — Turn 2 explicitly says "weighted for the senior/Head-of-Product end of your target range" and the behavioural Q8 is named "altitude (capital allocation / org design)".
- AskUserQuestion fallback to numbered/lettered list: PASS — A-D lettering used cleanly throughout.
- Anchors are concrete and memorisable: PASS — Turn 10 anchors are punchy and tactical ("RICE is an input to judgement, not an oracle").
- Gate-met nudge mentions BOTH free-form drill AND interviewer-simulator: PASS — Turn 10 includes both options.

## Open critique

- The Q7 scoring is the worst quote-fidelity break in the run — it doesn't just paraphrase, it invents a different intellectual move (input-correction-plus-business-context-override) than option B actually presented (a sales-loss-driven re-prioritisation). A senior user catching this would lose trust mid-session.
- Q8 scoring metric drift (8 points → 18%) is the kind of detail a Maya-altitude reader actually notices and will undermine the anchor "HoP altitude = capital allocation + exec alignment" because the example just got rewritten under them.
- Turn 4's Q2-D commentary ("directionally plausible and not wrong") is the only soft moment in otherwise crisp scoring. A stricter MC framing would commit: D fails because it skips diagnosis, full stop.
- The Turn 10 closer is good and on-spec, but the phrase "Recognition is locked — time to put it under load" leans slightly motivational-coach. A flatter "Recognition gate cleared; the open question is whether you can generate, not just recognise" would land harder in Maya's voice.
