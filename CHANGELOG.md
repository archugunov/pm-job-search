# Changelog

All notable changes to pm-job-search are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims for
[Semantic Versioning](https://semver.org/).

## job-sweep

`job-sweep` is a second plugin in this repo and versions independently of
pm-job-search. Its releases are listed here under their own heading.

### job-sweep [0.1.0] — 2026-08-05

First release. A standalone weekly sweep for open product roles, installable
without adopting the pipeline tracker.

- Single skill, `/job-sweep:sweep`. Discovery only — no tracking, no scoring, no
  company folders.
- First run takes a CV or three questions; geography is always asked, never
  inferred, because a CV says where you have lived rather than where you want to
  work.
- Keeps `job-sweep/seen-roles.jsonl` so the second week does not re-surface the
  first week's roles. Schema is identical to the full plugin's ledger, so moving
  up loses nothing.
- Roles bucket into strong / possible / edge. No weighted rubric — there is no
  rubric in this profile.
- `/setup` in the full plugin now pre-fills from `job-sweep/profile.md`.
- Five reference files are shared with pm-job-search from a single source under
  `plugin/`; `make sync-sweep` copies them and CI fails the build on drift.

---

## [Unreleased]

Continues 0.5.0's inversion. Two independent judge readings of the same
transcript split 4:1 on hard violations, and every disagreement was about a
word list — whether `meta.md`, `status: new` and `tier: unscored` counted as
explained jargon. So the largest measured source of judge variance in the
corpus was a rule that never needed a judge.

- `scripts/lint_transcript.py` — deterministic lint over a journey transcript.
  Bare fenced blocks used as chat summaries, references to skills or files that
  don't resolve, banned internal jargon in user-facing copy, prior-state prompts
  on a first run, and cadence numbers that don't trace to the user's own plan.
  Stdlib only, like the schema validator it joins.
- Internal jargon is now a flat ban rather than "jargon without explanation".
  The judgement call was the whole disagreement; the flat ban is also the better
  product rule.
- Rules whose input is missing report `NOT CHECKED` rather than passing
  silently — a clean run must not be mistaken for full coverage.
- `rubrics/lint-checklist.md` deleted. Six of its seven rules are now scripts;
  the seventh ("two unrelated asks in one message") was already duplicated
  verbatim in `rubrics/tone.md` as Rule A.
- The judge no longer decides hard violations. It transcribes the two
  deterministic blocks — schema validation and lint findings — and is told
  explicitly not to add, drop or re-litigate them.
- 46 new tests, including a frozen-corpus baseline asserted as
  `(transcript, turn, rule)` triples so quote-formatting changes don't churn it.

The judged rubrics were rebuilt around what a judge is actually needed for.

- `rubrics/groundedness.md` (new, gating) — every fact, number, name, date,
  filename and URL must trace to a file read this run, a fetch this run, or an
  earlier user turn. Produces a claim table, one row per claim, rather than
  prose. Zero tolerance: one ungrounded claim fails the run. This is the
  plugin's most-repeated failure mode and had no rubric of its own.
- `rubrics/coherence.md` (new, advisory) — nothing arrives cold, recent context
  outweighs old, no repetition or self-contradiction, stable vocabulary across
  skills. Holistic verdict. Advisory until it calibrates; promotion needs human
  agreement >= 0.9 over >= 10 adjudicated runs.
- `rubrics/spec-criteria.md` renamed to `conformance.md`, and `tone.md` gains a
  holistic verdict rule. Every rubric now carries an explicit `## Verdict`
  aggregation rule and a `## Worked examples` section of borderline cases —
  both enforced by a test.
- `rubrics/open-critique.md` deleted. Around 40 bullets across 11 runs, no
  verdict power, nothing in `plugin/memory.md` traceable to it, and the one
  bullet ever human-checked was a confident false positive citing a real file
  and line. Its genuinely useful content — misquoted numbers, self-contradiction
  — is what groundedness and coherence now catch, with verdict power.
- The judge runs once per rubric instead of once per run, and each call sees
  only its own rubric. Verdicts come after evidence, not before. The
  confirmation re-run on FAIL now re-runs only the failing gating rubric.
- The report is five lines — Lint, Groundedness, Coherence, Conformance, Tone —
  with the gate stated separately as Lint AND Groundedness AND Conformance.
- New `tests/test_plugin_refs.py`: every `${CLAUDE_PLUGIN_ROOT}` path and
  `/pm-job-search:<skill>` reference in the plugin's own markdown must resolve.
  Written because the rubric rename left four journey files pointing at a
  deleted file and nothing caught it.

The judge was then measured against human labels for the first time.

- All eight live-journey transcripts re-judged under the new rubrics, one call
  per rubric. Two transcripts (`2026-08-04`, `2026-08-07`) had never been judged
  at all, so the set grew rather than being swapped.
- Groundedness immediately caught three fabricated claims that both prior judge
  readings had missed: a turn that reports a failed fetch for every posting it
  touches, then states one role's location and sector, three other openings on
  that same unfetched page, and a fourth company's only role with its
  geographic restriction. The same turn says "I didn't guess tiers from titles
  alone".
- Labelling tooling rebuilt around the rubric verdict rather than the finding:
  five verdicts per run, findings collapsed underneath and opened only on
  disagreement. `grade-judge.html` went from 1814 lines to ~700 — four tiers,
  the critique tier, criterion chips and the two-subverdict overall were all
  dead concepts.
- `stats.py` prints a confusion matrix per rubric (positive class = FAIL) with
  precision, recall and accuracy. Accuracy alone hid direction: groundedness and
  coherence both scored 0.86 while failing in opposite ways, one missing and one
  over-firing.
- `tests/test_grade_judge.py` — the labelling tool had zero automated coverage,
  which is how it once shipped a leak that exposed judge verdicts before the
  blind gate. Its DOM wiring now sits behind a `typeof document` guard so node
  can require the parser and run it over the real corpus. It immediately caught
  a zero-tolerance rubric reporting PASS alongside 13 findings.
- First calibration pass over 7 runs: tone agreement 0.43, every disagreement in
  the same direction — judge PASS, human FAIL. Precision 1.00, recall 0.33. It
  never invented a tone problem; it forgave nearly all of them.
- `tone.md` retuned in response: a recurring pattern is now a FAIL however small
  each instance, and the judge must group findings by cause before returning
  PASS. The four disagreements ship as worked examples. Recall went 0.33 → 1.00.
- `tests/judge-calibration/controls/` — two hand-repaired transcripts that are
  supposed to PASS. Every real run has defects, so nothing tested whether a
  rubric can recognise a clean run; after the tone change failed all seven runs,
  the controls were the only way to tell "correctly strict" from "broken".

Then the product itself, since three of the tone defects came from the
guidelines rather than from skills drifting.

- `TONE.md` listed "What's the best email for you?" under "Examples that match
  the voice" — the exact phrasing flagged in the blind pass — and
  `setup/SKILL.md` had copied it verbatim. Its hard-filters example offered "no
  GM roles", which contradicts the target titles of anyone aiming at a GM-shaped
  seat. Examples in that file get copied into skills, so a bad one ships
  everywhere.
- Principle 2 allowed technical terms if "explained the first time". Every skill
  decided its own case was the explained one, which is how `meta.md`,
  `--refresh`, "to triage", HTTP codes and "sub-agent context" reached users. Now
  a flat never-shown list, matching what `lint_transcript.py` enforces.
- Two rules added that nothing covered: a question must state what the product
  does with the answer or be cut, and the two-clauses-max limit now applies to
  questions, not only to briefs.
- Copy fixed to match: the "Ready?" gate removed from `/setup` (the user has
  already run the skill), "best email" → "your email", the LinkedIn ask now says
  why, `--refresh` and launchd/cron no longer surfaced, "triage" replaced in
  `/job-search` and `recommended-flow.md`, and `/apply`'s missing-CV error
  rewritten as a plain sentence.

Known gaps, stated rather than implied: roughly half the skills and none of the
six agents have end-to-end journey coverage; `active-loop`, `edge-recovery` and
`sweep-smoke` have not been run since these changes; and the calibration corpus
is spoiled for blind reads because its findings have been discussed in detail.

---

## [0.5.0] — 2026-08-10

The test strategy inverted. Almost all testing weight used to sit in an
expensive LLM-judged conversation harness that ran every few weeks; the
deterministic layer underneath barely existed. This release flips that.

### Changed
- Test harness restructured: journeys cut 8 → 3 (+ sweep-smoke, run-by-name);
  `cold-start-cv`, `reflection`, and both `case-practice` journeys retired.
- Judge calibration is now per rubric, not per run. Label files carry
  separate Hard-violations and Spec-gaps verdicts; the overall verdict is
  derived from those two rather than recorded by hand, and a mismatch
  between the judge's stated overall and its own sub-verdicts is reported
  as a self-contradiction.
- Phase 3.5 schema validation now runs `scripts/validate_userdata.py`
  (meta.md + profile.md + strategy.md + research-brief), shared with CI.

### Added
- `harness-checks` CI: deterministic pytest layer over snapshots, schemas,
  and golden-set labels — 73 tests, $0, every push.
- Golden set for `/evaluate-position` (12 labeled synthetic JDs) with a
  release-time agreement gate (`tests/golden/evaluate-position/`).
- Judge-calibration tooling: `tests/judge-calibration/grade-judge.html`, a
  single-file browser tool for grading the judge with a blind-pass gate and
  a live precision/recall readout, and `tests/judge-calibration/stats.py`,
  its command-line equivalent, with the adjudication protocol in
  `tests/judge-calibration/README.md`. The tool shows the transcript and the
  rubric beside the findings, and links a finding to the transcript turn it
  cites; the blind-pass gate keeps every judge-derived value — findings,
  verdicts, advisory counts and the sidebar readout — out of the page until
  you have written your own list.
- Frozen judge-calibration corpus: 31 files across 11 judged runs in 7
  dated directories, scrubbed and committed under
  `tests/judge-calibration/runs/`.
- `plugin/skills/test-personas/manual-checklist.md` — the four manual
  release checks, out of chat lore and into the repo.
- Schema docs: `plugin/schemas/profile.md.schema.md`,
  `plugin/schemas/strategy.md.schema.md`,
  `plugin/schemas/research-brief.md.schema.md`.

### Fixed
- Privacy blocklist gained one more city-name term surfaced during
  calibration-corpus scrubbing (`.github/workflows/privacy-check.yml`,
  `CONTRIBUTING.md`).
- 22 research briefs across the test snapshots gained the
  `**Source:** <url>` first line `plugin/skills/evaluate-position/SKILL.md`
  requires, and `tests/snapshots/contrarian-messy/profile.md` gained the
  tier rubric it was missing — fixture repairs the new schema validator
  surfaced.

## [0.4.0] — 2026-08-04

CV-first onboarding. `/setup` now reads a CV up front and pre-fills what it can,
so most steps are a confirmation rather than a blank box.

### Changed

- `/setup` is nine steps instead of twelve questions. When a CV is found, name,
  city, email and LinkedIn arrive as a single confirmation line, and target
  titles and industries are offered as multi-selects derived from the CV, each
  shown with the roles the inference came from.
- Timeline is a bucket choice (under 2 months / 2-4 / 4+ / exact date) rather than
  a typed date. A concrete `target_offer_date` is still what gets stored, so
  `/today`'s countdown is unaffected.
- Hard filters are a multi-select over common red flags, with a free-text escape.
- Salary band is the one step deliberately left as free text. Generating bands
  would mean inventing market data the plugin has no source for. Everywhere
  else offers structured input — though with no CV, the name/city/email,
  target-title and industry steps still fall back to typing, and several
  steps keep a free-text escape alongside their options.
- "Companies of interest" moved out of `/setup` and into the first `/job-search`
  run, where the context makes it answerable.

### Added

- `plugin/references/cv-extraction.md` — shared CV-reading rules, split by
  confidence: facts read off the page, inferences derived from the CV's shape.
  Carries the governing rule that a field the CV lacks is asked, never guessed.
- `cold-start-cv` test journey and its `empty-with-cv` snapshot, covering the
  CV-present path. `cold-start` now covers the no-CV path.

## [0.3.0] — 2026-07-11

First stable cut of the 0.3 line (developed across `v0.3.0-beta.1`…`beta.6`).
Adds a case-interview practice track, an end-to-end test harness, and a
structural fix for sub-agent data drift.

### Added
- `/case-practice [Company]` — multiple-choice rapid-recognition drill across the
  MC-able case types (product sense, metric movement, metric tree, prioritisation,
  behavioural-signal), scored against an 80% readiness gate, with an 8-type
  case-interview reference and a 5-drill practice-methodology guide.
- `test-personas` — maintainer-only end-to-end harness (5-phase pipeline, 3
  personas, 6 journeys, LLM judge with 4 rubrics, Phase 3.5 schema validation)
  plus `plugin/memory.md` as a regression-lessons log. Filtered from `/help`.
- `plugin/schemas/meta.md.schema.md` — canonical `meta.md` contract (required
  keys, status enum, forbidden drift keys) shared by every reader.
- `/job-search` anti-repeat: a persistent append-only seen-ledger
  (`userdata/outputs/seen-roles.jsonl`) plus a shared `dedup-normalization.md`
  reference so a role stays suppressed even after its folder is deleted, and
  near-duplicate titles surface as "likely repeats" instead of re-filing.

### Changed
- `tier:` notation is now canonically `P0` / `P1` / `P2` / `unscored` across the
  schema, templates, and skills, matching what the dashboard already renders.
- `/job-search` sub-agent contracts key `position` (never `role`) and dedup on
  `(company, position)`; both sub-agent prompts carry an explicit output contract.
- Docs corrected to the true inventory (13 user-facing skills + 6 agents) with the
  `case-practice` row added; `CONTRIBUTING.md` no longer claims integrations are
  out of scope (they ship opt-in via `/integrations`).

### Fixed
- Sub-agent fidelity drift — added post-write validation gates (`/job-search`) and
  read-back assertions (`/evaluate-position`, `/today`) that reject invented field
  names, bad status values, and placeholder links like `(url not captured)`.
- Privacy CI now scans all branches (not just `main`); the workspace `CLAUDE.md`
  and author-private files are gitignored so they can't be committed accidentally.

## [0.2.1] — 2026-05-25

First public release: the pure-markdown core (8 skills + 6 reviewer/coach agents),
the opt-in `/integrations` MCP layer (Granola / Calendar / Gmail), the browser
dashboard, and the TONE.md voice guidelines with a lint checklist.

[0.4.0]: https://github.com/archugunov/pm-job-search/releases/tag/v0.4.0
[0.3.0]: https://github.com/archugunov/pm-job-search/releases/tag/v0.3.0
[0.2.1]: https://github.com/archugunov/pm-job-search/releases/tag/v0.2.1
