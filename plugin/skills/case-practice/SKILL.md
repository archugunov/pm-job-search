---
name: case-practice
description: This skill should be used when the user asks for "/case-practice", "/pm-job-search:case-practice", "drill me on product cases", "practice PM case interviews", "MC case drill", or "test my case-interview recognition". Runs drill 1 of the case-practice methodology — a multiple-choice (MC) rapid-recognition drill that samples scenario questions across the MC-able case types (product sense, metric movement, metric tree, prioritisation, behavioural-signal), scores each pick with the specific failure mode every distractor demonstrates, tracks a running score against an 80% readiness gate, extracts anchors to lock, and writes a session log to userdata/case-practice/<date>-mc-drill.md. Optional <Company> argument themes products and weights the mix toward that company's likely rounds.
---

# /case-practice — MC rapid-recognition drill

This is drill 1 — MC rapid-recognition — of the case-practice methodology, and it's the first rung of a five-drill ladder. Its job is to lock the *recognition* of senior-vs-junior answers and build the vocabulary every later drill needs: you can't fix a gap you don't have the language to name. It runs as batches of single-select questions, scores each pick with the specific failure mode behind every wrong option, tracks a running score against an 80% readiness gate, and extracts anchors to memorise. See `${CLAUDE_PLUGIN_ROOT}/references/case-interviews/practice-methodology.md` for the full five-drill ladder (recognition → generation → performance) and why the order matters. The live mock (drill 4) runs via the `interviewer-simulator` agent — only after the user clears the ≥80% gate here.

**Voice:** follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Low-effort-first — start on context-weighted defaults; don't interrogate the user about scope, depth, or case types before the first batch. If a `<Company>` argument is given, theme from it silently (read the company's files, weight the mix, theme products) — no confirmation question.

## MC-able case types (what the drill draws from)

MC recognition only fits *atomic, discriminable* judgement calls — "pick the strongest of four" where exactly one option is right and the rest each fail for a nameable reason. It does NOT fit open-ended strategy, technical / system-design, or estimation cases: those are free-form / live-mock territory (drills 2 and 4) and are out of scope for this drill. Don't generate MC questions for them.

The drill samples from:

- **Product sense** — strongest NSM; the right segment + a clean pick-reason; JTBD need quality. This is the richest seam — weight it heaviest by default.
- **Metric movement** — the correct first diagnostic fork (drop-to-diagnose vs goal-to-hit); MECE-clean vs overlapping decomposition.
- **Metric tree** — the 4-part NSM form (unit + behaviour + threshold + cadence); guardrail vs counter-metric vs vanity metric.
- **Prioritisation** — which lens fits the situation; "define value before you score"; spotting the sycophancy / spreadsheet-obeying trap.
- **Behavioural** — spotting the seniority signal (rejected-options / named trade-off / honest retrospective) vs the junior tell (heroics, no failure named, wrong altitude).

## Inputs

No topic-selection argument. The drill samples a broad mix across the MC-able types above, **context-weighted**. Read with the userdata-override convention (mirror story-builder): for each reference doc, read `userdata/references/case-interviews/<doc>.md` if it exists, else `${CLAUDE_PLUGIN_ROOT}/references/case-interviews/<doc>.md`.

- **`practice-methodology.md`** — the MC drill format, the Pattern-1 feedback structure, and the ≥80% readiness gate. This skill operationalises that doc.
- **`case-types-reference.md`** — the failure-mode vocabulary. Lean on the Product Sense / Metric Movement / Metric Tree sections most of all (their "common traps" tables are the source of named distractors), plus the Prioritisation and Behavioural "common traps".
- **`userdata/profile.md`** — `target_titles` weights the mix and calibrates which option counts as "right":
  - A Head-of-Product / Lead / Director / VP / CPO candidate gets more prioritisation and behavioural-altitude calls, and their "right" answers weight org/portfolio judgement higher (e.g. the strongest behavioural option is the one showing capital-allocation or hire/fire judgement, not feature craft).
  - An IC / Senior PM candidate gets more product-sense and metric calls, with "right" answers weighting craft and execution.
  - `## Tone of Voice` shapes all prose (question stems, feedback, the close).
- **Optional `<Company>` argument:** if `userdata/companies/<Co>/` exists, read its `[<slug>/]research-brief.md` and `[<slug>/]meta.md` (the `position` field). If the company tracks multiple roles (subfolder layout), ask which role first — e.g. `Plaid tracks 2 roles — pick: 1) senior-pm-consumer-credit, 2) senior-pm-growth-loops` — then read that slug's files. Weight the mix toward that role's likely rounds using the "When each case type shows up" table in `case-types-reference.md` (e.g. an infra/payments company leans metric-tree + prioritisation; a FAANG consumer role leans product-sense + metric-movement). Theme the products in the questions to an **adjacent** public domain (not the company's own internals). Default (no company argument): assorted well-known public products, mix weighted by `target_titles` only.

If `userdata/profile.md` is missing → tell the user to run `/setup` first, then stop.

## Drill flow

1. **Open.** State the context-weighted mix chosen (and the company theme, if any) in one line — e.g. "Weighting toward product-sense and metric calls for a Senior PM, products themed around payments infra." Then state the format in one line: batches of 4, single-select, scored after each batch.
2. **Generate a batch of 4 questions** sampled across the MC-able types per the weighting. Each question = a scenario + 4 options; exactly one option is the strongest; the **three distractors each demonstrate a specific, named failure mode** — drawn from the relevant type's "common traps" in `case-types-reference.md`: vanity metric, gameable metric, wrong segmentation lens, solution-disguised-as-need, wrong diagnostic fork (drop vs goal), MECE-violating decomposition, leaf-that-isn't-a-lever, mixing equation/ratio form, lens-misfit (RICE where value isn't defined), spreadsheet-obeying, sycophancy pick, junior behavioural tell (heroics / no failure / wrong altitude), and so on. For product-sense **needs** questions past the first batch, use the harder design from `practice-methodology.md`: 4 JTBD-formatted options forcing discrimination on stakes-in-the-so-clause, non-obviousness, and segment-specificity — NOT 1 good option plus 3 obviously-wrong ones.
3. **Collect the answer** via `AskUserQuestion` (4 options fits cleanly) or a numbered list. Accept a letter or a number.
4. **Score + teach the batch** — Pattern-1, roughly 150 words per question:
   - ✓ why the right answer is right (one line).
   - ✗ the specific failure mode each distractor shows (one line each).
   - the batch-level senior pattern being taught (one line).
   The distractors carry the lesson — teach every one, not just the right pick.
5. **Track the running score** and report it after each batch (e.g. "6/8 so far"). Score is cumulative over the whole session: `M` = questions asked, `N` = questions where the user picked the single strongest option (a skipped question doesn't count toward either). The ≥80% gate is evaluated on the full-session `N/M`, not per batch.
6. **Continue** until the user stops or reaches ~30 questions / ~7-8 batches. Offer to stop at each batch boundary ("Another batch, or wrap up?").
7. **Close.** Extract the 4-6 **anchors to lock** — short verbatim phrases (5-15 words each) the user should memorise. Report the final score against the **≥80% readiness gate** (met / not yet). Give the end-of-run nudge.

## Output — session log

Always write `userdata/case-practice/<YYYY-MM-DD>-mc-drill.md` (path relative to the active install root — e.g. `userdata/examples/maya/case-practice/...` when running against the Maya example). Create the `userdata/case-practice/` directory on first run. If a log for the same date already exists, **prepend** a new section (don't overwrite — spaced-practice history matters). Use this exact template:

```markdown
# MC case drill — <YYYY-MM-DD>
**Score:** <N>/<M> (<pct>%)  **Readiness gate (≥80%):** met | not yet

## Anchors to lock
- <4-6 short verbatim phrases>

## Missed / shaky
- <question stem> — picked <X>, strongest was <Y>. Failure mode: <named>.

## Suggested next
<free-form drill, or interviewer-simulator live mock once gate met>
```

## End-of-run nudge

Per `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`, compose one context-aware next-step line:

- Score **<80%** → "Run /case-practice again on a fresh batch before moving on — the gate is 80%."
- Score **≥80%** → "You've cleared the recognition gate. Next: a free-form generation drill (roadmap), or run the interviewer-simulator agent for a live product-case mock."

## What /case-practice never does

- Never claims to record, listen to, or play audio. This drill is text-only; voice-memo steps in the methodology are the user's own phone, not Claude.
- Never writes outside `userdata/case-practice/`. No edits to `profile.md`, company files, or the story bank.
- Never invents company facts when themed to a `<Company>`. Products in the questions are drawn from the public domain (adjacent, well-known products), never from claims about the company's internal roadmap, metrics, or org.

## Smoke test against the Maya example

### No-arg run

Run `/case-practice` against `userdata/examples/maya/`:

- Reads `userdata/examples/maya/profile.md` — `target_titles` includes "Head of Product", so the mix weights up prioritisation + behavioural-altitude calls (alongside product-sense / metric calls), and "right" answers on behavioural questions weight org/portfolio judgement.
- Opens with a one-line mix statement and the format (batches of 4, single-select, scored after each batch).
- Generates a batch of 4 across the MC-able types, collects answers via AskUserQuestion, scores with Pattern-1 feedback (✓ right answer + ✗ each distractor's named failure mode + the batch's senior pattern), reports the running score.
- On stop: extracts 4-6 anchors, reports the score vs the ≥80% gate, and writes `userdata/examples/maya/case-practice/<date>-mc-drill.md` (creating the `case-practice/` dir on first run).

### Company run

Run `/case-practice Mercury` against `userdata/examples/maya/` (a single-role company — files at the company root):

- Reads `userdata/examples/maya/companies/Mercury/{research-brief,meta}.md`. Mercury is fintech/business-banking — weights the mix toward the rounds that type of company runs (metric-tree, prioritisation, product-judgement) per the "When each case type shows up" table.
- Themes products to an adjacent public domain (e.g. a well-known consumer-fintech or payments product), NOT Mercury's internal product details — no fabricated company internals.
- Same flow and same log path (`userdata/examples/maya/case-practice/<date>-mc-drill.md`).
- Multi-role check: `/case-practice Plaid` (Maya's Plaid tracks two roles in subfolders) must first ask which role — `Plaid tracks 2 roles — pick: 1) senior-pm-consumer-credit, 2) senior-pm-growth-loops` — then read that slug's files. It must NOT try to read `companies/Plaid/meta.md` at the top level (it doesn't exist there).
