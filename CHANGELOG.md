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
