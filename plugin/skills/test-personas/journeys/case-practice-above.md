---
name: case-practice-above
persona: maya
snapshot: maya-active
max_turns: 30
---

## Goal

Exercise `/case-practice` (drill 1, MC rapid-recognition) end-to-end
on a no-arg run where the user clears the 80% readiness gate.
Confirms the **gate-met** nudge variant fires (suggesting drill 2
free-form generation or the interviewer-simulator live mock).

Paired with `case-practice-below`; together they cover both nudge
branches without re-exercising the rest of the drill flow.

## Opening message

`/pm-job-search:case-practice`

## Mid-journey instructions to the simulator

You're Maya — a Senior PM with 9 years of experience who has
prepped extensively for her upcoming Head of Product interviews.
You've internalised the failure-mode vocabulary from
`references/case-interviews/case-types-reference.md` and know what
to look for: named trade-offs in behavioural answers, MECE-clean
decompositions in metric trees, the correct diagnostic fork
(drop-to-diagnose vs goal-to-hit) in metric movement questions, and
stakes-in-the-so-clause for JTBD needs.

1. After the skill's one-line mix statement + format line, it will
   present the first MC question. Answer with a letter or number.
2. **Read each scenario carefully.** For each option:
   - On behavioural questions, pick the option that names a
     rejected alternative, surfaces a trade-off, or operates at
     org/portfolio altitude (capital allocation, hire-fire
     judgement) — NOT the option that describes individual
     feature craft, heroic execution, or a victory with no failure
     mentioned.
   - On metric-movement questions, pick the option with the
     correct first diagnostic fork (is this drop-to-diagnose or
     goal-to-hit?) and MECE-clean decomposition.
   - On metric-tree questions, pick the option matching the
     4-part NSM form (unit + behaviour + threshold + cadence) and
     correctly distinguishing guardrail / counter-metric / vanity.
   - On prioritisation questions, pick the option that defines
     value BEFORE scoring, matches lens to situation, and avoids
     the spreadsheet-obeying / sycophancy traps.
   - On product-sense questions, pick the option with a clear NSM,
     a specific segment + pick-reason, and JTBD framed with stakes
     in the "so [...]" clause.
3. After **batch 1**'s scoring + running score, reply `another`.
4. **Batch 2** — same careful approach.
5. After batch 2's scoring + running score is reported, reply
   `wrap up` (or `stop here`). You want to see the close, anchors,
   and the gate verdict.
6. When the close confirms you've cleared the 80% gate and offers
   a next-drill suggestion, ack with "thanks" or "ok" and stop.

## Termination

Stop when the transcript contains a line mentioning the log file
path (e.g. `userdata/case-practice/<YYYY-MM-DD>-mc-drill.md`) AND
the simulator has acknowledged.

Backstop: if the score after batch 2 is **<80%**, the gate-met
nudge variant won't fire — note this in the transcript footer and
continue to termination anyway. The journey's primary purpose
(testing the gate-met nudge variant) is unexercised but the rest of
the drill flow still gets covered.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass)
or `[opportunistic]` (advisory). See
`${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md`
for verdict aggregation rules.

Most criteria are identical to `case-practice-below`. The two
journeys share the bulk of the spec; the differentiator is the
end-of-run nudge variant.

- **[required]** Opens with one line stating the context-weighted mix + one line stating the format (batches of 4, single-select, scored after each batch). No multi-line preamble, no question about scope or depth before the first batch.
- **[required]** Each MC question presents a scenario + 4 distinct options. Exactly one option is the strongest; the other 3 are plausible distractors (no obviously-wrong filler).
- **[required]** Pattern-1 feedback structure after each batch: ✓ why the right answer is right (one line), ✗ the specific named failure mode each distractor demonstrates (one line each), and the batch-level senior pattern (one line). The distractor diagnoses must use named failure modes (e.g. "vanity metric", "MECE-violating decomposition", "wrong diagnostic fork", "junior behavioural tell — heroics / no failure", not generic "this is wrong").
- **[required]** Running score is reported after each batch (e.g. `7/8 so far`). Score is cumulative across batches in the session.
- **[required]** Skill offers stop at each batch boundary (`Another batch, or wrap up?` or equivalent phrasing).
- **[required]** On close: extracts 4-6 short verbatim **anchors to lock** (5-15 words each).
- **[required]** On close: reports the final score against the **≥80% readiness gate** (met / not yet).
- **[required]** Writes a session log to `userdata/case-practice/<YYYY-MM-DD>-mc-drill.md` matching the template in the SKILL.md (Score line / Anchors to lock / Missed or shaky / Suggested next).
- **[required]** End-of-run nudge fires the **gate-met** variant when the final score is ≥80%: a line acknowledging the recognition gate is cleared and suggesting either a free-form generation drill or running the interviewer-simulator agent for a live product-case mock. Must not fire the gate-not-met variant in the same close.
  *Applies when:* the final reported score is `≥80%`.
- **[required]** No fabricated company internals. The drill is a no-arg run, so products in scenarios must be drawn from the public domain.
- **[opportunistic]** Mix statement reflects the right-answer weighting toward Head of Product altitude (Maya's `target_titles` includes "Head of Product").
- **[opportunistic]** Skill degrades gracefully when `AskUserQuestion` is unavailable in sub-agent context.
- **[opportunistic]** Anchors are verbatim phrases the user could actually memorise (concrete language, not abstractions).
- **[opportunistic]** The gate-met nudge mentions both the free-form generation drill option AND the interviewer-simulator option (rather than only one), giving the user a meaningful choice.
