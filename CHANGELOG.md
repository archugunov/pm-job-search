# Changelog

All notable changes to pm-job-search are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims for
[Semantic Versioning](https://semver.org/).

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

[0.3.0]: https://github.com/archugunov/pm-job-search/releases/tag/v0.3.0
[0.2.1]: https://github.com/archugunov/pm-job-search/releases/tag/v0.2.1
