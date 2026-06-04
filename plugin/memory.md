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
