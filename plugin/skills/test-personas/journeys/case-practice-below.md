---
name: case-practice-below
persona: maya
snapshot: maya-active
max_turns: 30
---

## Goal

Exercise `/case-practice` (drill 1, MC rapid-recognition) end-to-end
on a no-arg run where the user lands below the 80% readiness gate.
Verifies the full drill flow (open → batches → Pattern-1 scoring →
running score → anchors + log → end-of-run nudge) and confirms the
**gate-not-met** nudge variant fires.

## Opening message

`/pm-job-search:case-practice`

## Mid-journey instructions to the simulator

You're Maya — a Senior PM with 9 years of experience who hasn't
done much explicit case-prep before this session. You're treating
this drill as a baseline check.

1. After the skill's one-line mix statement + format line, it will
   present the first MC question. Answer with a letter or number.
2. **Pick fast and on instinct.** Read each scenario once, pick the
   option that *sounds* senior at first glance, and move on. Don't
   re-read. This will produce some misses — that's the point of a
   baseline.
3. When the skill presents a behavioural-altitude question, lean
   toward the option that mentions individual feature craft or
   metric wins rather than capital allocation / hire-fire judgement
   — Maya defaults to her current Senior PM altitude, not the Head
   of Product altitude her target role demands.
4. After the **first batch of 4 questions** is scored, if the skill
   asks "Another batch, or wrap up?" reply `another`.
5. In **batch 2**, slow down slightly and read each option — you're
   getting calibrated. Pick what looks correct.
6. After batch 2's scoring + running score is reported, reply
   `wrap up` (or `stop here`) regardless of where the score landed.
   You want to see the close, the anchors, and the gate verdict.
7. If the close reports the score is below the 80% gate, ack with
   "ok" or "thanks" and stop. The journey is done.

## Termination

Stop when the transcript contains a line mentioning the log file
path (e.g. `userdata/case-practice/<YYYY-MM-DD>-mc-drill.md`) AND
the simulator has acknowledged.

Backstop: if the running score reported after batch 2 is **≥80%**,
the gate-not-met nudge variant won't fire — note this in the
transcript footer and continue to termination anyway. The journey
hasn't failed; only its primary purpose (testing the below-gate
nudge variant) is not exercised this run.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass)
or `[opportunistic]` (advisory). See
`${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md`
for verdict aggregation rules.

- **[required]** Opens with one line stating the context-weighted mix + one line stating the format (batches of 4, single-select, scored after each batch). No multi-line preamble, no question about scope or depth before the first batch.
- **[required]** Each MC question presents a scenario + 4 distinct options. Exactly one option is the strongest; the other 3 are plausible distractors (no obviously-wrong filler).
- **[required]** Pattern-1 feedback structure after each batch: ✓ why the right answer is right (one line), ✗ the specific named failure mode each distractor demonstrates (one line each), and the batch-level senior pattern (one line). The distractor diagnoses must use named failure modes (e.g. "vanity metric", "MECE-violating decomposition", "wrong diagnostic fork", "junior behavioural tell — heroics / no failure", not generic "this is wrong").
- **[required]** Running score is reported after each batch (e.g. `5/8 so far`). Score is cumulative across batches in the session.
- **[required]** Skill offers stop at each batch boundary (`Another batch, or wrap up?` or equivalent phrasing).
- **[required]** On close: extracts 4-6 short verbatim **anchors to lock** (5-15 words each).
- **[required]** On close: reports the final score against the **≥80% readiness gate** (met / not yet) — exact phrasing per the SKILL.md template.
- **[required]** Writes a session log to `userdata/case-practice/<YYYY-MM-DD>-mc-drill.md` matching the template in the SKILL.md (Score line / Anchors to lock / Missed or shaky / Suggested next). Path is relative to active install root; for the test harness this is `userdata/case-practice/...` (NOT `userdata/examples/maya/case-practice/...`).
- **[required]** End-of-run nudge fires the **gate-not-met** variant when the final score is <80%: a line directing the user to run /case-practice again on a fresh batch before moving on. Must not fire the gate-met variant in the same close.
  *Applies when:* the final reported score is `<80%`.
- **[required]** No fabricated company internals. The drill is a no-arg run, so products in scenarios must be drawn from the public domain (well-known consumer or B2B products). No claims about a specific company's internal roadmap, metrics, or org.
- **[opportunistic]** Mix statement reflects the right-answer weighting toward Head of Product altitude (since Maya's `target_titles` includes "Head of Product"). E.g. mentions prioritisation + behavioural-altitude calls in the mix, or weights "right" behavioural answers toward capital-allocation / hire-fire judgement rather than feature craft.
- **[opportunistic]** Skill degrades gracefully when `AskUserQuestion` is unavailable in sub-agent context: falls back to a numbered list (1-4) or lettered list (A-D) for option presentation. Accepts both letter and number inputs without a parse error.
- **[opportunistic]** Anchors are verbatim phrases the user could actually memorise (concrete language, not abstractions like "be senior" or "think strategically"). E.g. "define value before you score" passes; "use good judgement" fails.
