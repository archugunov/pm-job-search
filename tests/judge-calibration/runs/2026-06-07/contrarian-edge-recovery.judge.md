# Findings — contrarian-edge-recovery

**Run date:** 2026-06-07
**Snapshot:** contrarian-messy

## Verdict

**Overall: PASS**

- Hard violations: PASS (0 transcript + 0 schema)
- Spec gaps: PASS (all required in-scope criteria met)
- Soft issues: 0 (advisory)
- Open critiques: 5 (advisory)

## Hard violations (lint checklist)

No hard violations found. Schema validation clean.

## Soft issues (TONE voice + UX)

None.

## Spec gaps

### Required (all in-scope passed)

Cross-journey:
- **End-of-run nudge:** PASS — Turn 5 closes with two concrete recovery paths.
- **No prior-state leak:** PASS.
- **No dead ends:** PASS — every turn offers a next move.
- **Profile/strategy not silently overwritten:** PASS — no writes to those files.
- **JD link in three places:** NOT EXERCISED (Recheck-only, no new roles filed).

Edge-recovery journey-specific:
- **/today ran without crashing despite missing profile sections:** PASS — brief rendered, placeholders called out explicitly.
- **/today skipped founder-outreach line:** PASS — no founder line in brief.
- **/today flagged StaleCorp 20+ days in to_apply:** PASS — "37 days in to_apply".
- **/today flagged duplicate AcmeCorp:** PASS — explicit in top actions + heads-up.
- **/job-search handled empty Companies of interest gracefully:** PASS — asked one clarifying question, no crash.
- **/evaluate-position with unreachable URL produced clear error:** PASS — named IANA reserved domain, offered two concrete recovery paths.
- **No nag loop:** PASS — profile gaps mentioned once in Turn 1, never re-prompted.
- **Every skill closed with usable next-step nudge:** PASS — all 4 skill turns had context-aware closing nudges.

### Opportunistic
- None applicable.

## Open critique

- Turn 5 is the strongest moment: names the actual failure mode (IANA reserved domain) instead of generic "couldn't fetch". Diagnostic without lecturing.
- Turn 1 top action 1 ("kill the duplicate AcmeCorp entry") is the single highest-leverage instruction — frames the messy state as a five-minute cleanup.
- `meta.md` and `userdata/profile.md` references in user-facing copy are acceptable here — they're folder identifiers the user needs to act on, not config-internals.
- The `target_offer_date` vs `target_date` heads-up is good plugin transparency — tells Sam exactly which key name the plugin reads so he can fix his strategy.md.
- One state inconsistency unflagged: Turn 1 Pipeline shows AcmeCorp Senior PM as `to_apply` despite journal recording the application on 2026-05-20. Brief catches it via "update status on the survivor" but a future enhancement could auto-reconcile journal-stated applies with meta.md status.
