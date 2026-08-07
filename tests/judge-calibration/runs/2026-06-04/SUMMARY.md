# Test run — 2026-06-04 (verification run)

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| cold-start | FAIL (confirmed) | FAIL | FAIL (1/3 in scope passed; 15 not exercised) | 2 | 4 |

See per-journey `.judge.md` files for details.

## Files in this run

- maya-cold-start.md (transcript, 10 turns)
- maya-cold-start.judge.md (findings, with FAIL confirmed by re-run)

## Candidate memory entries

Patterns worth promoting into `plugin/memory.md` if they reflect a real lesson rather than a one-off:

- **2026-06-04** — Plugin sub-agents leak `Q<N>:` prefixes even with anti-leak rule in orchestrator prompt
  - Journey: cold-start
  - Surfaced in: this test run (re-confirmed; same pattern as 2026-05-27 entry)
  - Watch for: re-occurrence after the anti-leak rule landed in commit d0b09f1 — the rule may need strengthening or be ineffective with current sub-agent behavior. Already in memory.md from 2026-05-27 — no new entry needed; this is a regression signal.

## Notes

This was a VERIFICATION run, not a release-gating run. The transcript was reused from the 2026-05-27 smoke test to exercise the new verdict + memory + confirmation re-run machinery without paying the cost of a fresh conversation loop. Both judge calls were dispatched on the same transcript; both returned FAIL → `FAIL (confirmed)`.
