# Judge calibration

> **STALE — being rewritten.** On 2026-08-12 the rubrics were restructured
> (lint extracted to scripts; groundedness and coherence added; open critique
> deleted; one judge call per rubric; five-line verdict block) and the seven
> live-journey transcripts were re-judged under the new set. Everything below
> describing four tiers named hard / soft / spec / critique, and the
> transcript-only list, predates that. `stats.py`, `grade-judge.html` and
> `labels/TEMPLATE.json` still expect the OLD shape and are reshaped next —
> don't start labelling against this document. Plan:
> `docs/superpowers/2026-08-11-rubric-restructure-plan.md`.

Frozen corpus of harness runs (`runs/`, scrubbed) + human labels
(`labels/`) + `stats.py`. Purpose: know the judge's error rate so a FAIL
means something, and replay rubric edits in minutes instead of a full
journey sweep.

Not every transcript in `runs/` was judged — three are transcript-only,
with no `.judge.md` sibling to diff against:
`2026-06-07-beta4-verify/diego-reflection.md`,
`2026-08-04/maya-cold-start.md`, `2026-08-07/maya-cold-start.md`. Don't
pick these for a blind pass; there's nothing to diff your findings
against — `grade-judge.html` knows this and skips the blind-pass gate for
them automatically, with a note on the card.

`2026-08-10/` is the newest run and the only one produced by the current
code. It is also the only run judged **twice** — `maya-cold-start.judge.md`
and `maya-cold-start.judge2.md` are two independent readings of the same
transcript, and they disagree: 4 hard violations against 1, plus a
required spec criterion one passed and the other failed. Label both. That
disagreement is the cleanest measurement of judge variance in the corpus,
and its `SUMMARY.md` names one finding already known to be wrong (judge 1
calls `setup/SKILL.md:291` self-contradictory; it isn't) — a free
calibration data point to start on.

## Labelling with the tool (primary path)

Open `tests/judge-calibration/grade-judge.html` directly in a browser —
no build step, no server, no network calls; everything stays in the tab
and is checkpointed to `localStorage` as you go.

1. Drop the `runs/` folder and `plugin/skills/test-personas/rubrics/`
   folder onto the dropzone (or use "Choose a folder" for each). **Use the
   folder picker or drag-and-drop, not "Choose files"** — the flat file
   picker hands back bare filenames with no directory, and the corpus has
   four different `maya-cold-start.judge.md` files in four dated folders.
   The tool refuses to load a same-named file over one already loaded from
   a bare path rather than silently overwriting it, but the folder picker
   avoids the problem entirely.
2. Each run renders as a card: transcript pane on the right (tabbed
   Transcript / Rubric), findings in the middle, a live readout in the
   sidebar. For judged runs, findings and verdicts start hidden behind a
   **blind pass** — type your own findings first, then "Reveal judge
   findings" (or "Skip blind pass" if you're only adjudicating precision,
   not recall). Transcript-only runs skip this gate; there's nothing to
   reveal.
3. Once revealed: set `Hard violations` and `Spec gaps` to PASS/FAIL
   yourself (a bare `judge: —` chip next to each shows what the judge
   said, for comparison, but stays read-only). Do **not** set an overall
   verdict — there's no control for it. `Overall` is derived from your two
   sub-verdicts (PASS iff both PASS) and shown as "Derived overall: … —
   (judge stated: …)"; a mismatch there is what the sidebar's "verdict
   agreement" numbers measure. If the judge's own stated `Overall`
   disagrees with what its own Hard+Spec verdicts imply, a
   self-contradiction note appears on the card and in the sidebar — that's
   a defect in the judge's output, not something to fix in your labelling.
4. Each finding is a card grouped by tier (Hard / Soft / Spec / Critique).
   Spec-gap findings carry a coloured chip showing the judge's own
   per-criterion call (PASS / FAIL / NOT EXERCISED / NOT APPLICABLE) —
   you're grading whether *that* call was right, not re-deriving it from
   the prose. Click a finding's `turn N →` link to jump the context pane's
   Transcript tab straight to that turn, highlighted.
5. Export via each card's "Download label JSON", or "Download all" /
   "Copy all as JSON" from the sidebar. Downloads land named
   `<date>-<persona>-<journey>.json` — move them into `labels/` if your
   browser didn't save them there directly.

The sidebar's Readout panel mirrors `stats.py`'s maths live: per-tier
precision, recall, verdict agreement (with excluded-run counts called out
the same way `stats.py` does — see below), self-contradiction, advisory
totals, and the gate line. Label there, cross-check with `stats.py` after.

## Labelling by hand (fallback)

If you'd rather edit JSON directly, or need to fix up something the tool
got wrong:

1. Copy `labels/TEMPLATE.json` to `labels/<date>-<persona>-<journey>.json`.
2. Open the run's `.judge.md`. For each finding, add a `findings[]` entry:
   its tier, a one-line copy, and your call — `agree` (real), `disagree`
   (not real), `borderline` (defensible either way; excluded from
   precision, reported separately).
3. Adjudicate `verdicts.hard.human` and `verdicts.spec.human` separately —
   what each sub-verdict should have been (`PASS` or `FAIL`). Do NOT set
   an overall verdict yourself: `verdicts.overall.human` stays `null`.
   Overall is derived from the two sub-verdicts by the judge's own
   aggregation rule (`Overall` passes only when both Hard violations and
   Spec gaps pass); soft issues and open critiques are advisory counts
   and never affect it. `stats.py` computes the derived overall for you
   when comparing against the judge's stated `Overall`.
4. Some judge verdicts are `null`, not `PASS`/`FAIL` — two runs in this
   corpus write `- Hard violations: judges disagreed — …` instead of
   calling it, because the harness ran two judge passes and they split.
   That's legitimate: still adjudicate `verdicts.hard.human` (what it
   *should* have been), leave `verdicts.hard.judge` as `null`. `stats.py`
   and the tool both treat a `null` judge verdict as missing data, not a
   FAIL, and report it as an excluded run rather than crashing or
   silently dropping it.

## Blind pass (recall) — do for >= 6 transcripts BEFORE reading their judge files

1. Read the transcript against the three rubrics. Write your own findings
   list with turn numbers — do not open the `.judge.md` first.
2. Then diff against the judge file. Fill `blind`:
   `{"human_found": <your count>, "judge_matched": <of yours it also found>}`.

## Reading the numbers

    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/
    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/ --gate

Bars: precision >= 0.9 per tier (tiers with >= 5 adjudicated findings),
recall >= 0.8. Below the bars, a lone journey FAIL is "go look", not a
release blocker. Verdict agreement (hard, spec, derived overall) and
advisory counts are reported alongside the bars but never gate at this
corpus size.

If a `judge self-contradiction` line appears, the judge's own stated
`Overall` disagreed with what its own `Hard violations` and `Spec gaps`
verdicts should have produced — that's a defect in the judge's output
contract, not something to fix in your labelling. Note it and move on.

`grade-judge.html` computes the same maths live in the browser while you
label; the one cosmetic difference is that if blind data exists but every
run's `human_found` is 0, the browser prints "Recall: n/a" while `stats.py`
omits the recall line entirely — both agree the gate never fails on it.
When a run's judge verdict is `null`, both report it the same way: e.g.
`hard verdict agreement: 9/9 (2 runs excluded: judge verdict unavailable)`.

### What the numbers actually mean, at this corpus size

Say the quiet part out loud: across the 11 judged runs measured when
these bars were set, the finding pools were **hard 2, soft 18, spec 154,
critique 41**. (The corpus has since grown — `2026-08-10` adds a twelfth
run, judged twice, which on its own contributes 4-5 hard findings and so
shifts the hard pool materially. Re-measure before leaning on these
numbers.) `MIN_N` is
5, so the hard tier can *never* gate on this corpus — there simply aren't
enough hard-violation findings to reach the precision-gate's minimum
sample size, ever, regardless of how the judge performs. In practice the
precision gate is a spec-only gate.

And "spec precision" is a narrower question than it sounds. It's not
"was this reported violation real" (that's what hard-tier precision
measures) — it's "was this criterion adjudication correct", over roughly
114 PASS / 9 FAIL / 22 not-exercised-or-applicable spec-criteria bullets
(145 of the 154 spec bullets carry a parseable per-criterion verdict; the
rest are prose that never resolved to one). Answering "is the judge
accurate" from the spec number alone conflates two different failure
modes: the judge missing a real violation, versus the judge mis-calling
an individual criterion it did check. `stats.py`'s CLI
output labels this line `spec: criterion-adjudication precision` rather
than plain `precision` so the difference stays visible at a glance.

## Acting on a disagreement

- Ambiguous criterion → rewrite the criterion (spec bug, not judge bug).
- Mechanically checkable → move it into `scripts/validate_userdata.py`
  or pytest; it leaves the judged pool permanently.
- Genuinely subjective judge error → add the case as a worked example in
  `plugin/skills/test-personas/judge-prompt.md` (pick borderline cases,
  not obvious ones).

## Replaying after a rubric edit

Re-run the judge over `runs/<date>/<persona>-<journey>.md` transcripts
(judge-prompt + rubrics + transcript, per test-personas Phase 4 — no
conversation loop, no simulator). Diff new verdicts against
`verdicts.hard.human` / `verdicts.spec.human` in the labels. ~11 LLM
calls, minutes.

## Known corpus caveats

- 2026-06-07 `diego-reflection` FAIL was a runner metadata error, not a
  plugin bug (see plugin/memory.md 2026-06-07). Label it accordingly.
- Judge output format drifts between runs (some print "No hard
  violations found" plus per-rule confirmation bullets) — that's why
  labelling is manual, not parsed for precision purposes. `grade-judge.html`
  does a best-effort structural parse of the same drifting format to
  surface findings and chips for you to grade — treat any obviously
  mis-parsed bullet as a labelling-tool bug to report, not a precision
  number to trust blindly.
- Two runs (`2026-06-07/diego-reflection`, `2026-06-07/maya-cold-start`)
  have a `null` Hard-violations judge verdict because the harness's two
  judge passes disagreed and the judge file records "judges disagreed"
  instead of calling it. Adjudicate `verdicts.hard.human` anyway; both
  `stats.py` and `grade-judge.html` exclude these from hard verdict
  agreement (reported, not hidden) rather than crashing or coercing the
  `null` into a FAIL.
- `2026-06-07-beta4-verify/maya-cold-start.judge.md` has no tier sections
  at all (it's an abridged verification report, not a full findings
  file) — `grade-judge.html` shows a plain note rather than rendering it
  as a silently-empty run.
