# Test run — 2026-06-11

Two case-practice journeys exercised end-to-end. Both PASS.

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| case-practice-below | PASS | PASS | 10/10 required, 3/3 opportunistic | 2 | 3 |
| case-practice-above | PASS | PASS | 10/10 required, 4/4 opportunistic | 2 | 4 |

See per-journey `.judge.md` files for details.

## Files in this run

- `maya-case-practice-below.md` — transcript
- `maya-case-practice-below.judge.md` — findings
- `maya-case-practice-above.md` — transcript
- `maya-case-practice-above.judge.md` — findings

## Notable findings — both journeys

### Recurring soft issue: sub-agent quote-fidelity drift in scoring

Both judges independently flagged the same pattern: in Turn 4 / Turn 8 scoring, the plugin sub-agent paraphrases option text from the question-presentation turn rather than quoting verbatim. The drift is sometimes minor (Q5 "to the gallery per week" → "in the gallery") but sometimes substantial — case-practice-above Q7 option B was completely re-written ("permissions overhaul, RICE 180 ... three deals lost ... ~12% on paid Slack workspaces" → "enterprise admin features ... dollar-weighted accounts ... revenue-at-risk ... two enterprise deals"), and Q8 option B's metric changed from "8 points + platform velocity doubled" to "rose 18% the following quarter."

The explicit reminder I added to the case-practice-above scoring prompt ("quote the option text faithfully — don't paraphrase distractors") did not prevent the drift. This is a real architectural issue worth promoting to `plugin/memory.md` and considering a fix at the SKILL.md or orchestrator-prompt level.

### Journey-design issue: case-practice-below cannot reliably trigger the gate-not-met nudge

Final score landed at 7/8 (87.5%) — above the 80% gate — despite the journey's name and intent. Why: Maya is a Senior PM with 9 years of fintech experience. Even "picking fast and on instinct" she correctly identified vanity metrics, drop-to-diagnose discipline, and the 4-part NSM form. The single forced miss (the Q4 altitude trap) wasn't enough to push the cumulative score below 80%.

The journey's backstop fired cleanly (gate-not-met criterion dropped to NOT EXERCISED per its Applies-when clause, so verdict still PASS), but the journey's primary purpose is not validated. Three candidate fixes:
- (a) Different persona — a junior PM who'd genuinely miss more questions.
- (b) More forced misses in journey instructions — e.g. "lean toward A on metric questions if the option mentions DAU".
- (c) More questions per batch / batch — make a single miss less impactful so structured under-performance becomes possible.

### Plugin-correctness highlight: case-practice-above demonstrates the gate-met nudge works as designed

Final score 8/8 (100%), gate-met variant fired cleanly with both the free-form generation drill option AND the interviewer-simulator option mentioned ("free-form generation drill (roadmap construction end-to-end), or run the interviewer-simulator agent for a live product-case mock with pushback"). All 10 required + 4 opportunistic criteria PASS.

## Mechanism validation

| Component | Status |
|---|---|
| Plugin install at v0.3.0-beta.5 includes case-practice + new journeys | ✅ Cache resolved correctly |
| Phase 2 schema check (`target_titles` non-empty + active-loop checks) | ✅ Both journeys passed |
| Phase 3 conversation loop | ✅ Both journeys terminated cleanly within max_turns (11 turns each) |
| Phase 3.5 schema check on userdata/companies/*/meta.md | ✅ 19 files scanned, no drift |
| Phase 4 judge | ✅ Both judges returned PASS; no confirmation re-runs triggered |
| Session log written to `userdata/case-practice/<date>-mc-drill.md` | ✅ Both journeys produced compliant logs |
| Gate-met nudge variant | ✅ Fired cleanly in case-practice-above; incidentally also in case-practice-below |
| Gate-not-met nudge variant | ⚠️ NOT EXERCISED in either journey (case-practice-below intended to test it but landed above gate) |

## Candidate memory entries

Patterns worth promoting into `plugin/memory.md` if they reflect real lessons:

- **2026-06-11** — Sub-agent quote-fidelity drift: scoring re-writes option text instead of quoting verbatim, even with an explicit "quote faithfully" reminder
  - Journey: both case-practice-below and case-practice-above
  - Surfaced in: this test run
  - Watch for: in any multi-turn skill where one sub-agent presents content and a later sub-agent comments on it, expect drift unless the option/content text is structurally pasted in. The explicit-reminder strategy is insufficient. Candidate fix: orchestrator-prompt template gains a "verbatim-quote rule" for content presented in earlier turns, modelled after the state-guardrails rule.

- **2026-06-11** — `case-practice-below` cannot reliably trigger gate-not-met with a Senior-PM persona
  - Journey: case-practice-below
  - Surfaced in: this test run
  - Watch for: journey designs where "persona behaviour + drill difficulty" should produce a specific outcome but the persona is too competent to land it. Either provide more forced misses, switch to a junior persona, or design the drill to be harder. The backstop note in the journey file works, but the journey loses its core purpose when the backstop fires.

## Next moves

1. **Both journeys validated as PASS.** v0.3.0-beta.6 (case-practice harness coverage) is safe to tag.
2. **Promote the two candidate memory entries** into `plugin/memory.md`.
3. **Consider re-tuning `case-practice-below`** so the gate-not-met variant gets exercised. This is the journey's whole point; without exercising the variant, we don't know whether the SKILL.md's gate-not-met branch ("Run /case-practice again on a fresh batch before moving on — the gate is 80%") fires correctly.
4. **Investigate the quote-fidelity drift** at the orchestrator-prompt level — same architectural family as the 2026-06-07 state-guardrails fix.
5. **Merge to main as stable v0.3.0** after the above two refinements, or after deliberately accepting the open gap.
