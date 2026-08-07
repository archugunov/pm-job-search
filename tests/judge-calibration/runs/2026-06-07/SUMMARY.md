# Test run — 2026-06-07 (all four journeys)

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| cold-start | FAIL (confirmed) | PASS | FAIL (8/13 required passed; 5 failed) | 3 | 4 |
| active-loop | **PASS** | PASS | PASS (all required passed) | 2 | 5 |
| reflection | FAIL (confirmed) | PASS | FAIL (heads-up risks fabricated) | 0–1 | 5 |
| edge-recovery | **PASS** | PASS | PASS (all required passed) | 0 | 5 |

See per-journey `.judge.md` files for details.

## Files in this run

- `maya-cold-start.md` / `.judge.md` — cold-start (19 plugin turns, FAIL confirmed)
- `maya-active-loop.md` / `.judge.md` — active-loop (8 plugin turns, PASS)
- `diego-reflection.md` / `.judge.md` — reflection (3 plugin turns, FAIL confirmed)
- `contrarian-edge-recovery.md` / `.judge.md` — edge-recovery (5 plugin turns, PASS)

## Headline result

**All four journeys exercised end-to-end. 2 PASS, 2 FAIL — both PASS journeys had explicit schema/state reminders in their sub-agent prompts; both FAIL journeys lacked them for their critical sub-agent (`/today` brief-writer).**

This is now a high-signal result. The harness is mature and the failure mode is concrete.

## The pattern (across all 4 journeys)

| Journey | Schema/state reminder in prompt? | Verdict |
|---|---|---|
| cold-start /job-search | No | Created `role:` drift |
| cold-start /today | No | Rendered "(url not captured)" |
| active-loop /job-search | **Yes** (canonical schema cited) | Clean |
| active-loop /apply, /interview-prep | Implicit (specific file paths given) | Clean |
| reflection /today | No | Fabricated 4 companies |
| edge-recovery /today | **Yes** (explicit "read meta.md, don't fabricate") | Clean |
| edge-recovery /job-search | Implicit (sparse state spelled out) | Clean |
| edge-recovery /evaluate-position | Implicit | Clean |

The contrast is unambiguous: **sub-agents that get explicit state guardrails behave reliably; sub-agents that don't fabricate.**

## Phase 2 snapshot fixes landed this run

- `55a785e` — backfill maya-active with `## Companies of interest` section (for active-loop)
- `ffd8cbf` — backfill diego-reflection with current-week journal entries (for reflection nudge)

Both committed; future runs will use the corrected snapshots.

## Mechanism validation summary

| Component | Status |
|---|---|
| Parent slash-command discoverability | ✅ Works |
| Sub-agent slash-command discoverability | ❌ Confirmed NO (closed as documented) |
| Anti-leak `Q<N>:` rule | ✅ Held across all 4 journeys |
| Phase 2 schema validation | ✅ Caught 2 real snapshot drift cases |
| Phase 3.5 schema validation | ✅ Caught cold-start `role:` drift; clean on active-loop/reflection/edge-recovery |
| Verdict mechanism (PASS / FAIL / FAIL confirmed) | ✅ Verified across 2 PASS + 2 FAIL outcomes |
| Confirmation re-run on FAIL | ✅ Fired correctly on cold-start + reflection; did NOT fire on PASS runs (cost saved) |
| Memory.md as context not checklist | ✅ Judges referenced but grounded findings in evidence |
| Judge accepting 6th schema-validation input | ✅ Surfaced Rule 7 findings cleanly |
| All 4 journey types exercised | ✅ |

## Candidate memory entries

Patterns worth promoting into `plugin/memory.md`:

- **2026-06-07** — Explicit state guardrails in sub-agent prompts are necessary AND sufficient to prevent fidelity drift
  - Surfaced in: 4-journey comparison this run
  - Watch for: any sub-agent dispatch (test-harness or real) that doesn't tell the sub-agent EXACTLY which files to read and EXACTLY what schema/format to write. Without that, sub-agents fabricate. With it, they're reliable.
  - Action candidate: orchestrator's plugin-prompt template should be extended with a "state guardrails" section per skill — list of files the sub-agent MUST read, fields it MUST populate, fields it MUST NOT invent.

- **2026-06-07** — /today brief-writer is the highest-leverage sub-agent to harden
  - Surfaced in: cold-start (url not captured), reflection (4 fabricated companies)
  - Watch for: /today's brief inventing pipeline rows or events not in meta.md/journal.md
  - Fix candidate: same prompt pattern as /job-search — "Enumerate every meta.md file. Do not mention companies not in the enumeration. Quote status and link verbatim."

- **2026-06-07** — Maya-active snapshot needed `## Companies of interest` backfill (committed 55a785e)
- **2026-06-07** — Diego-reflection snapshot needed prior-week journal entries backfill (committed ffd8cbf)

## Next moves

1. **Apply the state-guardrails pattern to /today's brief-writer prompt** in the orchestrator. Most leveraged remaining fix.
2. **Tag v0.3.0-beta.4** with the snapshot backfills + the /today fix.
3. **Consider merging to main.** The harness is mature, has caught and validated real bugs, and the failure mode is now concrete and addressable.
4. **Promote candidate memory entries** from this SUMMARY into `plugin/memory.md` proper.
