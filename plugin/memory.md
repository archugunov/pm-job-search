# Plugin memory — surfaced lessons

Reverse-chronological log of patterns and lessons surfaced while building, testing, or running the plugin. Entries here are CONTEXT, not a checklist. They feed into the `test-personas` judge so the harness has memory of past failure modes, but the judge is instructed never to surface a finding from memory alone — every finding still needs a transcript quote.

Add a new entry when a test-personas run, a code review, or real-world use surfaces something the static rules (`TONE.md`, lint checklist, rubrics) don't yet capture. Keep entries short — three to five labelled lines, not paragraphs.

When the file crosses ~6 months of entries or starts feeling unscannable in one screen, roll older entries into `plugin/memory-archive-<year>.md` and link them from the top of this file.

## Format

```
### YYYY-MM-DD — one-line headline

**Surfaced in:** <run reference, batch name, smoke test date>
**Skill(s):** <comma-separated skill names, or `cross-cutting` if it spans>
**Action:** <commit SHA or "TONE.md update" or "no fix yet — watch list">
**Watch for:** <one sentence — what pattern to flag in future runs>
```

---

### 2026-06-07 — Verification runs must `ls` snapshot directories before asserting contents to the judge

**Surfaced in:** v0.3.0-beta.4 verification run (`userdata/test-runs/2026-06-07-beta4-verify/SUMMARY.md`)
**Skill(s):** test-personas (orchestration and verification process)
**Action:** none code-level — this is a process discipline lesson for whoever runs the harness next. The 2026-06-07 baseline reflection FAIL verdict turned out to be a metadata error: the runner (me) told the judge the diego-reflection snapshot had 8 companies "Retool, Vercel, GitLab, Linear, Replit, Browserbase, Builder, Modal" without verifying. The actual snapshot had Fly.io, Linear, Railway, Render, Replit, Retool, Supabase, Vercel. The judge correctly flagged the discrepancy, but the discrepancy was the runner's mistake, not a plugin bug.
**Watch for:** any verification run where the metadata sent to the judge asserts state ("the snapshot has X companies", "the journal has Y entries", "the strategy has Z fields") without an explicit `ls`, `cat`, or schema check confirming it. Before composing the judge prompt, list the actual snapshot directory contents and read the actual files. The state-guardrails rule protects against sub-agent fabrication; this rule protects against runner fabrication. The reflection re-run on v0.3.0-beta.4 demonstrated the parallel: the sub-agent caught my metadata error by reading files and refusing my plausible-but-wrong assertion. Trust files, not memory.

### 2026-06-07 — Explicit state guardrails in sub-agent prompts are necessary AND sufficient to prevent fidelity drift

**Surfaced in:** 4-journey comparison this run (`userdata/test-runs/2026-06-07/SUMMARY.md`)
**Skill(s):** test-personas, cross-cutting (every sub-agent dispatch)
**Action:** `plugin/skills/test-personas/SKILL.md` Phase 3 plugin-prompt template gained an explicit "State guardrails" section directing sub-agents to actually Read userdata files and never invent companies, dates, people, or events.
**Watch for:** any new sub-agent dispatch (in test-personas or future skills) where the prompt doesn't tell the sub-agent EXACTLY which files to read and which fields to populate. Without that, sub-agents fabricate. With it, they're reliable. Empirical evidence: 2 PASS (active-loop, edge-recovery) vs 2 FAIL (cold-start, reflection) sorted cleanly by whether the prompt had state guardrails for the critical sub-agent.

### 2026-06-07 — /today brief-writer is the highest-leverage sub-agent for state guardrails

**Surfaced in:** cold-start "(url not captured)" + reflection's 4 fabricated companies (Fly.io, Render, Railway, Supabase) + invented "Tom" interviewer and "Anna 2026-05-04" message
**Skill(s):** today
**Action:** new state-guardrails rule in orchestrator prompt covers this; if drift recurs after the rule lands, fix candidate is to extend `plugin/skills/today/SKILL.md` itself with "Enumerate every meta.md before composing; do not mention companies not in the enumeration."
**Watch for:** /today's brief listing companies, statuses, URLs, or events not present in `userdata/companies/*/meta.md` or `userdata/journal.md`.

### 2026-06-07 — Maya-active snapshot needed `## Companies of interest` backfill

**Surfaced in:** active-loop journey Phase 2 schema check
**Skill(s):** test-personas (Phase 2 snapshot validation), setup (the section was added 2026-05-25 in quick-fixes)
**Action:** snapshot backfilled (commit 55a785e)
**Watch for:** any future SKILL.md change that adds a required section to /setup's output — update committed snapshots in lockstep. Phase 2 catches it but slows the run by one cycle.

### 2026-06-07 — Diego-reflection snapshot needed prior-week journal entries for the weekly-reflection nudge

**Surfaced in:** reflection journey trigger condition (Diego's existing journal entries were from 2026-05-16, 3 weeks before the test date 2026-06-07)
**Skill(s):** test-personas (Phase 2), today (weekly-reflection trigger)
**Action:** snapshot backfilled with 2026-06-01/03/05 entries (commit ffd8cbf)
**Watch for:** any time-sensitive trigger condition embedded in a snapshot. Phase 2 currently checks "≥3 dated entries" but doesn't check "entries within prior ISO week" — worth tightening Phase 2 specifically for the reflection journey if drift recurs.

### 2026-06-07 — Sub-agents do not inherit parent's plugin context (slash-command discoverability is NO)

**Surfaced in:** cold-start full-run via slash-command path (`userdata/test-runs/2026-06-07/`)
**Skill(s):** test-personas, cross-cutting (any future harness or sub-agent dispatch)
**Action:** orchestrator's plugin-prompt template updated to drop the "you may invoke directly if loaded" line; known-limits resolved.
**Watch for:** any future harness change that assumes sub-agents can call plugin slash commands. The inline-SKILL.md fallback IS the canonical runtime architecture in this Claude Code version. Sub-agents dispatched via the Agent tool see only their explicit prompt, not the parent's installed skills.

### 2026-06-07 — Sub-agent fidelity drift: invented field names, skipped tail steps, didn't read downstream files

**Surfaced in:** cold-start full-run (Turn 16 + Turn 19)
**Skill(s):** test-personas (orchestration), cross-cutting (any skill called via sub-agent)
**Action:** none yet — documented as architectural concern in SKILL.md known-limits. Post-Phase-3 schema check on `userdata/` is the strongest candidate fix; investigation deferred to v0.3.x.
**Watch for:** sub-agent inventing field names (e.g. `role:` where SKILL.md says `position:`), skipping documented tail steps (/setup automation prompt + closing nudge skipped despite SKILL.md spec), or failing to actually Read downstream state files (/today rendered "(url not captured)" because sub-agent didn't read meta.md frontmatter `link:`). Full SKILL.md inlining + step-at-a-time discipline + anti-leak rule are necessary but not sufficient — they don't prevent fidelity drift on details.

### 2026-06-07 — Judge can mis-read blockquotes as fenced-code Rule B violations

**Surfaced in:** cold-start full-run, judge call 1 vs call 2 disagreement
**Skill(s):** test-personas (rubric + judge prompt)
**Action:** `rubrics/lint-checklist.md` rule 1 tightened to explicitly state blockquotes are NOT a violation; added "allowed exceptions" list. Resolved by the rubric edit.
**Watch for:** judge call 1 flagging `> ` blockquote summaries as Rule B violations. Confirmation re-run currently catches this; if it persists after the rubric edit, tighten the judge prompt itself.

### 2026-06-07 — Confirmation re-run on FAIL works as designed

**Surfaced in:** cold-start full-run (judge 1 and judge 2 both returned FAIL → `FAIL (confirmed)`)
**Skill(s):** test-personas
**Action:** none — documented as validated behavior.
**Watch for:** judges agreeing on overall but disagreeing on per-rubric verdicts (judge 1 said Hard FAIL, judge 2 said Hard PASS in the 2026-06-07 run). The final-judge-file convention should surface this disagreement clearly when it happens, not just collapse to overall.

### 2026-06-07 — /today brief renders fabricated heads-up items when state is sparse

**Surfaced in:** cold-start full-run, Turn 19 brief
**Skill(s):** today
**Action:** none yet — flagged as soft issue in judge findings. Worth investigating whether /today SKILL.md needs an explicit "do not invent items beyond what state.md justifies" rule.
**Watch for:** /today's heads-up surfacing items like "founder-outreach cadence missing" or "anti-goals not set" when strategy.md was just initialized minutes ago. Brief should respect freshness — first-run /today especially should be sparse, not preachy about gaps in just-created files.

### 2026-05-27 — Sub-agents leak internal labels into user-facing output

**Surfaced in:** cold-start smoke test (`userdata/test-runs/2026-05-27/`)
**Skill(s):** test-personas, cross-cutting (any skill with numbered SKILL.md sections)
**Action:** anti-leak rule added to orchestrator's plugin-prompt template (commit d0b09f1)
**Watch for:** any assistant message containing `Q1:`, `Q5:`, `Step 3 of`, or other internal numbering that should be invisible to the user.

### 2026-05-27 — Sub-agents improvise question order when given SKILL.md by path

**Surfaced in:** cold-start smoke test (initial attempt, before the SKILL.md inlining fix)
**Skill(s):** test-personas
**Action:** orchestrator now reads relevant skills' SKILL.md and inlines verbatim in the plugin-under-test prompt (commit d0b09f1)
**Watch for:** plugin-under-test sub-agent skipping questions, paraphrasing locked-in wording, or executing a different flow than the SKILL.md prescribes.

### 2026-05-26 — `target_offer_date` is the canonical strategy.md key (not `target_date`)

**Surfaced in:** final code review of test-personas branch
**Skill(s):** test-personas (Phase 2 schema validation), setup, today, evaluate-offer
**Action:** rubric / orchestrator updates landed in commit a321db2
**Watch for:** any new skill that reads strategy.md frontmatter using `target_date` — that key does not exist.

### 2026-05-26 — macOS APFS is case-insensitive; "case-only collision" test snapshots don't work

**Surfaced in:** Task 5 of test-personas implementation (contrarian-messy snapshot)
**Skill(s):** test-personas, cross-cutting (any snapshot work)
**Action:** contrarian-messy uses `acmecorp/` and `acme-corp/` (different folder slugs sharing `company: AcmeCorp` in frontmatter) instead of a case collision
**Watch for:** any new snapshot or test fixture that assumes case-distinct paths can coexist on a default-config macOS dev box.

### 2026-05-25 — Brief / heads-up content follows two-clauses-max rule

**Surfaced in:** quick-fixes batch
**Skill(s):** today, interview-analysis, cross-cutting (any skill emitting brief-style bullets)
**Action:** rule codified in `TONE.md` (commit b125bd7)
**Watch for:** any bullet in a brief, heads-up, or scannable list that uses three or more clauses, parentheticals as afterthoughts, or paragraph-shaped lines where short ones would scan better.
