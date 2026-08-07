# Test run — 2026-07-11

Plugin version under test: 0.3.0-beta.6 (workspace branch `test-personas`)
Scope: two journeys — `cold-start` then `reflection` — run sequentially to verify the sub-agent-fidelity fix (/job-search keys `position` not `role`, output contracts + Phase 2 validation gate; /today asserts `link:` is read, never "(url not captured)").

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| cold-start | PASS | PASS | PASS (13/13 req) | 2 | 3 |
| reflection | PASS | PASS | PASS (12/12 in-scope req; 2 NOT EXERCISED) | 3 | 3 |

See per-journey `.judge.md` files for details.

## Phase 3.5 schema validation

- **cold-start:** No schema drift found. 8 meta.md files filed by /job-search (Creditstar, Finom/head-of-product-cards, Finom/lead-pm-sme-lending, Klarna, Lendable/senior-product-manager, Lendable/uk-cards, Plaid, YouLend) — all have required keys company/position/status/link, status in enum, link starts with https://, no forbidden role:/target_date: keys. applications.md Link column populated with real URLs; no "(url not captured)" anywhere in the run.
- **reflection:** No schema drift found. 9 meta.md files scanned — all clean, no forbidden keys. /today's regenerated applications.md Link column populated from real link: values; no "(url not captured)" anywhere in the run.

## Fix verification (why this run mattered)

Both previously-FAILED journeys now PASS.
- /job-search wrote every new role with position: (never role:), a live https link:, and status: new; the Phase 2 validation gate held (8/8 files clean). Multi-role companies (Finom, Lendable) correctly used role-slug subfolders.
- /today read each link: from disk and rendered real URLs in the applications.md Link column — the string "(url not captured)" appeared NOWHERE in either run's userdata or transcripts. The only occurrences of that string in the repo are in the historical 2026-06-07 (failed) run files.
- No invented role: key in any meta.md across either run.
- reflection /today read real state and did NOT fabricate companies/people/events (the earlier failure invented Fly.io/Render/Railway/Supabase + a "Tom" interviewer; here those names are genuinely in the fixture and were quoted, not invented).

## Files in this run

- maya-cold-start.md (transcript)
- maya-cold-start.judge.md (findings)
- diego-reflection.md (transcript)
- diego-reflection.judge.md (findings)

## Notes

Both judges returned PASS on first call (no confirmation re-run needed; re-run fires only on FAIL).

Harness note: plugin-under-test agents were dispatched fresh per turn with the relevant SKILL.md inlined verbatim (swapped at each skill hand-off: setup -> job-search -> dashboard -> today for cold-start; today -> career-coach for reflection), per the orchestrator spec. Sub-agents occasionally leaked internal reasoning preambles before their user-facing message; the orchestrator recorded only the user-facing line in the transcript (harness artifacts, not plugin output).

Fixture note (reflection): the committed diego-reflection snapshot's newest journal entries (2026-06-01/03/05) predate the 2026-07-11 run date by ~5 weeks, so the weekly-reflection trigger's "prior-ISO-week entry" precondition could not fire as-is. Per the documented precedent (plugin/memory.md 2026-06-07 / commit ffd8cbf on time-sensitive snapshot triggers), the WORKING copy userdata/journal.md had its three newest entries re-dated into the prior ISO week (2026-06-29 / 07-01 / 07-03) and Retool's next_event/last_inbound refreshed for coherence. The committed snapshot under tests/snapshots/ was NOT modified. Candidate to fix at the snapshot level before the next release run.

No candidate memory entries (no FAIL).
