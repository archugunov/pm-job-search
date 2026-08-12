# Judge calibration

Frozen corpus of harness runs (`runs/`, scrubbed) + human labels (`labels/`) +
`stats.py`. Purpose: know the judge's error rate so a FAIL means something, and
replay a rubric edit in minutes instead of a full journey sweep.

## What you are labelling

Five verdicts per run. That is the whole job.

    Lint:          PASS          scripts, no judge involved
    Groundedness:  FAIL  (3)     gating, zero-tolerance
    Coherence:     PASS          advisory, holistic
    Conformance:   FAIL  (1)     gating, zero-tolerance
    Tone:          PASS          advisory, holistic

    Gate: Lint AND Groundedness AND Conformance  →  Overall

Read the five, set your own five, and open a rubric's findings only when you
disagree with its verdict. This is the mainstream shape in judge calibration —
binary rather than scaled, one judge per dimension — and it is why the corpus
now yields ~40 comparisons instead of the old hard tier's two findings across
eleven runs, which could never reach the minimum sample size to gate on.

Three things that change how you read a row:

- **Lint is not a judge.** It comes from `scripts/validate_userdata.py` and
  `scripts/lint_transcript.py`, and the judge only transcribes them. Marking it
  FAIL when the judge said PASS grades the *rule*; the fix is a change to the
  script, not a worked example.
- **Zero-tolerance vs holistic.** Groundedness and conformance fail on one
  finding. Coherence and tone are a judgement about the whole transcript —
  findings can and do sit alongside a PASS, and that is correct, not sloppy.
  (`2026-08-07` tone is exactly this case.)
- **Never set an overall verdict.** There is no control for it. Overall is
  derived: PASS iff your lint, groundedness and conformance are all PASS.
  Coherence and tone never enter the gate.

## Labelling with the tool (primary path)

Open `grade-judge.html` in a browser. No build step, no server, no network;
everything stays in the tab and is checkpointed to `localStorage`.

1. Drop the `runs/` folder onto the dropzone (and optionally
   `plugin/skills/test-personas/rubrics/` to read rubric text alongside).
   **Use the folder picker or drag-and-drop, not "Choose files"** — a flat
   picker discards directory names, and four runs share the filename
   `maya-cold-start.judge.md`.
2. Each run starts behind a **blind pass**: write your own findings before
   seeing the judge's, then reveal. Skip it if you only care about precision.
   The blind pass is the only source of recall data, and the only mechanism
   that has ever produced a *new rubric rule* — both restructures of this
   harness came out of one.
3. Set PASS/FAIL on each of the five rows. The judge's call sits next to yours,
   read-only, with its finding count.
4. Findings are collapsed under each rubric. Open one when you disagree.
   Groundedness carries its claim table; conformance carries every criterion
   assessment behind a second fold, since most of its bullets are PASSes rather
   than violations.
5. Export with "Download label JSON" per run, or "Download all" from the
   sidebar. Move the files into `labels/`.

The sidebar mirrors `stats.py` live. Label there, cross-check with the script.

## Labelling by hand (fallback)

Copy `labels/TEMPLATE.json` to `labels/<date>-<persona>-<journey>.json` and fill
`verdicts.<rubric>.human` for each of the five. Leave `overall.human` null —
`stats.py` exits 2 if you set it, because a hand-set overall silently competes
with the derivation. Findings are optional; add entries only where you drilled in.

A `null` judge verdict is missing data, not a FAIL. Adjudicate the human side
anyway; both `stats.py` and the tool report it as an excluded run rather than
coercing it.

## Reading the numbers

    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/
    python3 tests/judge-calibration/stats.py tests/judge-calibration/labels/ --gate

Verdict agreement per rubric is the primary number. Finding precision appears
only where you drilled in. Bars: agreement >= 0.9 per rubric with >= 5
adjudicated runs, precision >= 0.9 per rubric with >= 5 adjudicated findings,
recall >= 0.8 when any blind data exists. Thin rubrics report but never gate.

`stats.py` also prints whether **coherence** now clears the promotion bar
(agreement >= 0.9 over >= 10 adjudicated runs). Clearing it makes coherence
*eligible* for the gate; promoting it is a deliberate one-line change in
`test-personas/SKILL.md`, never automatic and never because a single run
obviously should have failed on it.

### The honest limitation

Every run in the corpus currently comes back **FAIL overall**, and no run has
ever passed the gate. Per-rubric pass rates:

    Lint          3/8      Conformance   2/8   (gating)
    Groundedness  3/8      Tone          6/8   (advisory)
    Coherence     3/8

Three consequences, in increasing order of how much they should bother you.

Overall agreement carries almost no signal — a judge that said FAIL to
everything scores 8/8. Never quote it as evidence the judge works.

**The gate has never been observed to fire green.** Each gating rubric has
passed on its own, but never all three on the same run, so the PASS path is an
untested code path in the most important place. Nothing here demonstrates these
rubrics *can* clear a good run.

**Verdict-level labelling cannot detect over-firing while everything fails.**
If a judge invents a finding, a zero-tolerance rubric still returns FAIL, you
tick "agree", and the fabricated reasoning survives untouched. The periodic
drill-down into a rubric you *agree* with is therefore not optional on this
corpus — it is the only thing standing between you and a judge that is right
for entirely invented reasons.

Conformance at 2/8 deserves the hardest look. Two of its failures are legitimate
(runs that terminated early, so required criteria were never reached — scored as
FAIL by design, not a product defect). Whether the remaining five are real or the
rubric is simply too strict is exactly what labelling decides.

Verdict agreement is also not *reasoning* agreement. A FAIL can be right for
the wrong reason — three tone findings where two are real and one is invented
still yields a correct FAIL you would tick and move past. Periodically open a
rubric you agree with and check the findings underneath. Cheap insurance, not a
routine.

## Acting on a disagreement

- Ambiguous criterion → rewrite the criterion. That is a spec bug, not a judge bug.
- Mechanically checkable → move it into `scripts/lint_transcript.py` or
  `scripts/validate_userdata.py`; it leaves the judged pool permanently.
- Genuinely subjective judge error → add it to that rubric's
  `## Worked examples` section. Pick borderline cases, never obvious ones. Every
  rubric is required by test to carry that section, because without it labelling
  produces a number and nothing changes.

## Replaying after a rubric edit

Re-run the judge for the edited rubric only, over the transcripts in `runs/`
(judge-prompt + that one rubric + transcript; no conversation loop, no
simulator). One rubric edit costs ~8 cheap single-dimension calls, which is the
main reason the judge is split per rubric.

## Corpus notes

- Eight transcripts carry restructured judge files. Six more
  (`diego-reflection` ×3, `maya-case-practice` ×2, `maya-cold-start-cv`) are
  from retired journeys and were deliberately **not** re-judged; their judge
  files are still the old four-tier hard/soft/spec/critique format. The tool and
  `test_grade_judge.py` both skip them by format. Don't label them.
- The two `2026-06-07-beta4-verify/` files have zero assistant turns — they are
  verification reports, not transcripts, and cannot be judged at all.
- `2026-06-07/diego-reflection`'s old FAIL was a runner metadata error, not a
  plugin bug (see `plugin/memory.md`, 2026-06-07).
- Judges format the conformance section three different ways. Verdicts are
  comparable across runs; conformance finding **counts** are not — the tool
  counts only bullets containing FAIL, which is why a "13 findings" PASS was a
  parser bug rather than a judge one.
