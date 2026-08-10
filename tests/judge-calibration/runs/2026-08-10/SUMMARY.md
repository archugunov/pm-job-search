# Test run — 2026-08-08 (dates in output are 2026-08-10; run spanned midnight)

Run against the WORKING TREE, not the installed plugin. First execution of the
restructured harness (journeys 8 → 3, Phase 3.5 delegating to validate_userdata.py).

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| cold-start | FAIL (confirmed) | FAIL | judge1 17/18 · judge2 16/18 | 0 | 4 |

Both judges returned FAIL independently, so the verdict is confirmed. They agree on
two findings and disagree on three — see "Judge variance" below.

## What the run validated (the reason it was commissioned)

The harness rewiring works end to end. All four skills ran and handed off correctly:
/setup → /job-search → /dashboard → /today, with live web search and real file writes.

Phase 3.5 ran `python3 scripts/validate_userdata.py userdata/` at four checkpoints —
empty state, after /setup, after the sweep, after /today — and returned
"No schema drift found." every time. Critically, the generated profile.md opens with a
multi-line HTML comment before its frontmatter: the exact shape of the parser bug that
shipped twice and was fixed twice. On live output the fix holds. Had it not, Phase 3.5
would have injected false "missing required key" hard violations into the judge input
on a clean run.

## Agreed findings

- **Hard, Rule 6 — turn 1.** "Found <state directory>userdata/cv.<ext>? No — no CV file
  exists, so here's the drop offer." Unresolved template placeholders and a narrated
  internal check in the first user-facing message. Judge 2 traced it: cv-extraction.md
  reserves that line for an unreadable-format CV; with no CV the only scripted line is
  "No CV — we'll do it the long way then."
- **Spec — /dashboard's closing lacked a context-aware next-step nudge** (turn 23).

## Judge variance (the most useful output of this run)

Two independent readings of one transcript:

- Judge 1: 4 hard violations. Judge 2: 1. The three extra are jargon leaks — `meta.md`,
  `status: new`, `tier: unscored` shown to the user. Rule 6 names `meta.md` explicitly,
  so judge 1 has a literal case; judge 2 silently declined all three.
- Judge 2 found a spec FAIL judge 1 passed: /job-search wrote `## Companies of interest`
  to profile.md without any chat line confirming the write (cross-journey 4). Verified on
  disk. Judge 1 marked the same criterion PASS on /setup's confirmation alone.

That is a 4:1 split on hard violations and a disagreement on a required criterion, on the
same evidence. It is exactly what the calibration corpus exists to quantify, and it argues
the per-rubric split shipped in 0.5.0 was the right call — one overall verdict would have
hidden all of it.

## Known judge error (do not fix the source)

Judge 1's open critique called setup/SKILL.md:291 internally contradictory:
"Any red flags — roles you'd skip on sight, whatever else is right about them?"
It is not. "Whatever else is right about them" means *regardless of their other merits* —
idiomatic and correct. Advisory only, so it did not move the verdict. Label this
"disagree" when the corpus is adjudicated.

## New findings worth acting on

- /dashboard never attempts its documented action (start server, open browser). May be an
  artifact of the sub-agent context rather than a product defect — the 2026-06-07 run
  recorded the same graceful degradation.
- The dashboard SKILL.md's documented first-status-change tip never fired at turn 21.
- /setup asked target titles and target industries as free text, two steps running. The
  journey only requires option-based shape for steps 5/7/8, so it passed — but the 0.4.0
  rework describes step 2 as a multi-select.

## Corpus contamination risk (new, introduced by 0.5.0)

The Klarna URL and its exact position title that the sweep "found" appear verbatim in
tests/judge-calibration/runs/2026-07-11/maya-cold-start.md — committed to the repo by the
0.5.0 corpus freeze. Lever UUIDs are stable per posting, so a live search of a still-open
req would legitimately return the same URL; Plaid's and Lendable's URLs are not in the
corpus. So this is unresolvable from the output alone, and that is the problem: a
plugin-under-test agent with repo read access can now see past transcripts full of role
listings, and "found it live" is indistinguishable from "read it in a fixture". Mitigation:
tell the plugin agent the corpus is off-limits, or exclude it during runs.

## Orchestration deviations (disclosed to both judges)

- Plugin agent Read each SKILL.md from its working-tree path instead of having it pasted
  in every turn; ONE persistent agent across turns instead of fresh-per-turn. Both are the
  improvements plugin/memory.md's testing note already recommends. Judge 2 suspects the
  turn-1 leak may trace to this; judge 1 called it the clearest sign of fidelity loss.
  Unresolved — worth one fresh-per-turn control run to settle.
- Sweep capped at 3-5 roles with an explicit "file nothing rather than invent" instruction.
- Simulator picked Lendable over the top-listed Plaid at turn 21, off-script but in-persona.

## Files in this run

- maya-cold-start.md (transcript, 25 turns)
- maya-cold-start.judge.md (judge 1)
- maya-cold-start.judge2.md (judge 2, confirmation)

## Candidate memory entries

- **2026-08-10** — Committing the calibration corpus into the repo created a contamination
  vector for plugin-under-test agents.
  - Journey: cold-start
  - Watch for: a "discovered" role whose URL and title already appear in tests/judge-calibration/runs/.
