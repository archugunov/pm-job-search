# Findings — maya-cold-start (confirmation judge, independent second reading)

**Overall: FAIL**

- Hard violations: FAIL (1)
- Spec gaps: FAIL (16/18 required in scope passed)

## Hard violations
- **[Rule 6]** Turn 1: unresolved template placeholders `<state directory>` / `<ext>` plus a narrated self-check leaked into the first user-facing message. Judge 2 notes `plugin/references/cv-extraction.md` reserves that "Found …" line for an UNREADABLE-format CV; with no CV at all the spec's only line is "No CV — we'll do it the long way then."

Judge 2 did NOT flag the three jargon findings judge 1 raised (`meta.md`, `status: new`, `tier: unscored`).

## Spec gaps — the two FAILs
- **Cross-journey 4 — profile/strategy not silently overwritten:** FAIL. `/job-search` wrote `## Companies of interest` to profile.md (verified on disk) but no chat line confirms the write. `/setup`'s writes ARE confirmed at turn 16, so the gap is specific to `/job-search`.
- **Context-aware next-step nudge per skill:** FAIL on `/dashboard` (turn 23) — agrees with judge 1.

## Open critique (judge 2 only)
- `/dashboard` never performs its documented action; the SKILL.md says start the server and open a browser. Possible artifact of the persistent-agent deviation.
- The dashboard SKILL.md's documented first-status-change nudge ("Tip: you can also click the company row…") never fired at turn 21, which was the first in-chat status change.
- Same caveat repeated across turns 20 and 21.
- Run-date drift: transcript header says 2026-08-08, plugin computed 2026-08-10 dates. Orchestration artifact (run dir created before midnight rollover), not a plugin defect.
