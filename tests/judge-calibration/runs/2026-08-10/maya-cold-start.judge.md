# Findings — maya-cold-start

**Run date:** 2026-08-08
**Snapshot:** empty

## Verdict

**Overall: FAIL (confirmed)**

- Hard violations: FAIL
- Spec gaps: FAIL
- Soft issues: 0 (advisory)
- Open critiques: 4 (advisory)

## Hard violations (lint checklist)

- **[Rule 6]:** turn 23: "Status changes and notes write straight back to the same meta.md files" — `meta.md` is the exact named example of forbidden internal jargon in the rubric, surfaced unexplained.
- **[Rule 6]:** turn 20: "Filed 3 new roles, all `status: new`, none scored yet:" — raw `field: value` frontmatter syntax exposed instead of plain English.
- **[Rule 6]:** turn 21: "Worth remembering it's still `tier: unscored`" — same internal-field leak.
- **[Rule 6]:** turn 1: "Found <state directory>userdata/cv.<ext>? No — no CV file exists, so here's the drop offer." — unrendered internal template with literal placeholders leaking into the first user-facing message.

No Rule 7 findings — SCHEMA VALIDATION reported "No schema drift found."

## Soft issues (TONE voice + UX)

No soft issues found.

## Spec gaps

### Required (17/18 in scope passed)

All cross-journey criteria 1-5 PASS. All journey-specific criteria PASS except:

- **Each skill's closing message included a context-aware next-step nudge:** FAIL — `/dashboard` (turn 23) closes with "Want me to walk through anything in the pipeline here in chat instead...?" naming no next skill, unlike setup (turn 18), job-search (turn 22) and today (turn 24).

Verified on disk: `## Companies of interest` in profile.md; `status: new` + populated `link:` in all three meta.md; Link column with URLs in applications.md; `target_offer_date: 2026-09-21` in strategy.md.

### Opportunistic (0/0 in scope)

No opportunistic criteria for this journey.

## Open critique

- Turn 1 opens with unrendered internal scaffolding before the real onboarding message — the clearest candidate for fidelity loss from the persistent-agent deviation.
- Turn 14's hard-filters prompt is internally contradictory: "Any red flags — roles you'd skip on sight, whatever else is right about them?" — traces to `plugin/skills/setup/SKILL.md` line 291. A genuine source bug, faithfully reproduced.
- Turns 1 and 2 repeat "same questions, you just type more" almost verbatim.
- Turn 21 stacks "Worth remembering… worth giving… a read" in one message.
