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
