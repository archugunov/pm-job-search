# Judge calibration

Frozen corpus of harness runs (`runs/`, scrubbed) + human labels
(`labels/`) + `stats.py`. Purpose: know the judge's error rate so a FAIL
means something, and replay rubric edits in minutes instead of a full
journey sweep.

Not every transcript in `runs/` was judged — three are transcript-only,
with no `.judge.md` sibling to diff against:
`2026-06-07-beta4-verify/diego-reflection.md`,
`2026-08-04/maya-cold-start.md`, `2026-08-07/maya-cold-start.md`. Don't
pick these for a blind pass; there's nothing to diff your findings
against.

## Adjudication (precision) — do for every judged run

1. Copy `labels/TEMPLATE.json` to `labels/<date>-<persona>-<journey>.json`.
2. Open the run's `.judge.md`. For each finding, add a `findings[]` entry:
   its tier, a one-line copy, and your call — `agree` (real), `disagree`
   (not real), `borderline` (defensible either way; excluded from
   precision, reported separately).
3. Set `verdict_human` to what the verdict should have been.

## Blind pass (recall) — do for >= 6 transcripts BEFORE reading their judge files

1. Read the transcript against the four rubrics. Write your own findings
   list with turn numbers — do not open the `.judge.md` first.
2. Then diff against the judge file. Fill `blind`:
   `{"human_found": <your count>, "judge_matched": <of yours it also found>}`.

## Reading the numbers

    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/
    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/ --gate

Bars: precision >= 0.9 per tier (tiers with >= 5 adjudicated findings),
recall >= 0.8. Below the bars, a lone journey FAIL is "go look", not a
release blocker.

`grade-judge.html` computes the same maths live in the browser while you
label; the one cosmetic difference is that if blind data exists but every
run's `human_found` is 0, the browser prints "Recall: n/a" while `stats.py`
omits the recall line entirely — both agree the gate never fails on it.

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
`verdict_human` in the labels. ~11 LLM calls, minutes.

## Known corpus caveats

- 2026-06-07 `diego-reflection` FAIL was a runner metadata error, not a
  plugin bug (see plugin/memory.md 2026-06-07). Label it accordingly.
- Judge output format drifts between runs (some print "No hard
  violations found" plus per-rule confirmation bullets) — that's why
  labelling is manual, not parsed.
