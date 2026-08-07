# Findings — maya-cold-start

**Run date:** 2026-07-11
**Snapshot:** empty

## Verdict

**Overall: PASS**

- Hard violations: PASS
- Spec gaps: PASS
- Soft issues: 2 (advisory)
- Open critiques: 3 (advisory)

## Hard violations (lint checklist)
No hard violations found.
- Rule 1 (fenced chat summaries): none. The /today brief (Turn 23) renders as native markdown headers; the dashboard `python3 ${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py ...` line (Turn 22) is an allowed shell command.
- Rule 2 (two asks per message): setup runs strictly one question per turn; the automation prompt (Turn 18) and positioning offer (Turn 17) are single asks.
- Rule 3 (non-existent skill/file): all references (`career-coach`, `/apply`, `/job-search`, `/today`, dashboard `serve.py`) resolve.
- Rule 4 (hardcoded cadence numbers): the "8 applications/week, 8 warm outreaches/week, floor of 4 threads / 6 P0 roles" (Turn 17) are presented as derived from the "~11-week timeline to 30 Sep" and written to strategy.md — derivation, not a hardcoded instruction. No "10 founders".
- Rule 5 (prior-state prompt on first run): /today (Turn 23) skipped the input loop and went straight to the brief.
- Rule 6 (jargon): `P0/P1/P2` appears (Turns 17, 23) but is the canonical `tier` value in meta.md and sits under a "Tier" column header — treated as borderline, see Soft.
- Rule 7 (schema drift): SCHEMA VALIDATION reports clean across 8 meta.md files; independently confirmed link present in all meta.md, research-brief `**Source:**` lines, and applications.md Link column.

## Soft issues (TONE voice + UX)
- Tier vocabulary inconsistency: /job-search chat (Turn 20) labels roles "tier-1 / tier-2 / tier-3", while /today's brief (Turn 23) labels the same roles "P0 / P1 / P2" in the Tier column and inline ("Finom is showing two P0 openings"). For a cold-start user, P0 is never defined and the two skills disagree on naming. Borderline Rule 6, filed Soft since P0/P1/P2 is the canonical stored value under a "Tier" header.
- Turn 17: "so I left it untouched per the guardrail" exposes internal process language ("the guardrail") to the user; a plainer phrasing would read better.

## Spec gaps
### Required (13/13 in scope passed)
- /setup precreated userdata/ before CV prompt: PASS — Turn 9 "I've created `userdata/` for you — drop your CV there".
- One residence Q + one geography Q, distinct: PASS — Turn 3 "Where are you based? City + country" vs Turn 7 "Where are you looking?".
- "Companies in mind?" question: PASS — Turn 15 "Any companies you have in mind already?".
- No weekly-reflection nudge in /setup: PASS — closing (Turns 17–19) offers only career-coach positioning + automation, no reflection nudge.
- Automation prompt 2-step (y/n then time): PASS — Turn 18 asks y/n first; user answered "No" (Turn 19) so the time step correctly did not fire.
- /job-search auto-filed at least one role status: new: PASS — Turn 20 "Filed 8 new roles, all set to status new"; confirmed in meta.md.
- link: in every new meta.md: PASS — schema validation + direct check.
- applications.md GENERATED block has Link column: PASS — schema validation confirms populated Link column, real URLs.
- Chat application row includes URL inline: PASS — Turn 20 rows carry full URLs.
- /today first run skipped input loop: PASS — Turn 23 opens directly with the brief.
- /today Heads-up ABOVE Pipeline state: PASS — Turn 23 order is Top actions -> Heads-up -> Pipeline state.
- /today no hardcoded founder-outreach number: PASS — no "10 founders"; only "Applications this week: 0 of 8" (from strategy).
- Each skill's closing had context-aware next-step nudge: PASS — setup (Turn 19), job-search (Turn 20), dashboard (Turn 22), today (Turn 23) each end with a next action.

Cross-journey [required]: (1) End-of-run nudge PASS — Turn 23 "start with `/apply Lendable`... then run through the two Finom P0s". (2) No prior-state leak PASS — job-search "this is your first sweep, so the pipeline started empty" correctly reflects empty state. (3) No dead ends PASS. (4) Profile/strategy not silently overwritten PASS — Turn 17 itemizes every file written. (5) JD link in three places PASS — meta.md link:, research-brief `**Source:**`, and chat row inline all confirmed.

### Opportunistic (1/1 in scope passed)
- /setup offered positioning draft (Mode A/B) after CV drop: PASS — Turn 8 offered A/B/C; persona chose A; Turn 10 produced a Mode-A positioning draft with explicit accept/edit/discard prompt.

## Open critique
- Tier naming is not stable across skills: a first-time user meets "tier-1/2/3" in /job-search (Turn 20) then "P0/P1/P2" in /today (Turn 23) with no bridge explaining they are the same scale.
- Turn 17's "per the guardrail" leaks internal build-logic vocabulary into an otherwise clean setup summary.
- Turn 23's top-actions list mixes a genuine action ("Tailor your CV with `/apply Lendable`") with a status readout ("Applications this week: 0 of 8"); the latter reads as a metric more than a "top action", though minor.
- No persona character break, no preachy/hedging patterns; the graceful cv.pdf->cv.md handling (Turn 10) is a nice touch.
