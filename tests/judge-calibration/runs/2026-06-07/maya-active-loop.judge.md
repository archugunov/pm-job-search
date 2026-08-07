# Findings — maya-active-loop

**Run date:** 2026-06-07
**Snapshot:** maya-active (after Phase 2 backfill fix)

## Verdict

**Overall: PASS**

- Hard violations: PASS (0 transcript violations, 0 schema findings)
- Spec gaps: PASS (all required in-scope criteria met)
- Soft issues: 2 (advisory)
- Open critiques: 5 (advisory)

## Hard violations (lint checklist)

No hard violations found.

## Soft issues (TONE voice + UX)

- **[Borderline Rule A]:** Turn 4 assistant message is a single sentence packed with multiple sub-questions and parenthetical asides. It technically resolves to one decision (SMB-lead vs consumer-lead), but the prose density is high. Quote: "do you want the CV to lead with the SMB lending work (deeper credit-model proof, but B2B-flavoured) or reframe the consumer onboarding/risk work as the headline (better audience fit, but thinner on actual underwriting depth)?"
- **[Borderline Rule A]:** Turn 6 closing offers two next-steps in one breath ("want me to draft a short cover note, or move on to interview-prep?"). Acceptable as a menu but borders on Rule A — two unrelated decisions presented together.

## Spec gaps

### Required (all in-scope passed)

Cross-journey:
- **End-of-run nudge:** PASS — Turn 8 ends with "interviewer-simulator (mock round) ... Debrief after with /pm-job-search:interview-analysis."
- **No prior-state leak in messaging:** PASS.
- **No dead ends:** PASS — every assistant turn ends with a clear next move.
- **Profile + strategy not silently overwritten:** PASS — Turn 3 names what changed ("Plaid → Senior PM, Consumer Credit → to_apply").
- **JD link in three places:** PASS — Turn 1 chat row includes inline URLs; new meta.md frontmatter includes `link:` (confirmed by Phase 3.5 zero drift); research-brief.md Source line present (verified by file inspection).

Active-loop journey-specific:
- **/job-search run summary uses plain prose:** PASS — Turn 1 bulleted role list, no fence.
- **/job-search tier counts bucketed:** PASS — "2 new roles: 2 tier-1".
- **Status change dashboard nudge once per session:** PASS — Turn 3 fired once, no repeat.
- **/apply did NOT exceed 5 questions:** PASS — only 2 questions asked (Turns 4 and 5).
- **/apply chat summary uses plain prose + bulleted recap:** PASS — Turn 6 no fenced block.
- **/apply summary cites positioning angle + proof points:** PASS — "underwriting depth at Brightline reframed as the direct analogue to Plaid Consumer Credit's thin-file decisioning work" + proof points + dropped material.
- **/apply closing offered clear next-step nudge:** PASS — cover note or interview-prep.
- **/interview-prep adapted 3-5 stories:** PASS — 4 stories adapted.
- **/interview-prep closing nudge context-aware:** PASS — interviewer-simulator + interview-analysis named.

### Opportunistic

- **/setup positioning draft if CV dropped:** NOT APPLICABLE — /setup not invoked in this journey.

## Open critique

- Full active loop (job-search → status change → apply → interview-prep) flows cleanly through in 9 turns with zero rework. This is what a clean recurring loop should look like.
- Turn 4's prose density is the only real weak spot. Tighter version would be: "Lead with SMB lending (deeper underwriting proof, B2B-flavoured) or consumer onboarding (better audience fit, thinner underwriting)?"
- Turn 6 closing "edit anything that doesn't sound like you before you send it" is a trust-building beat without preachiness.
- Phase 2 catch-and-fix on the snapshot drift is reflected in metadata; harness hygiene worked as designed.
- "meta.md" surfaces in Turn 3 as a transparency aside ("same meta.md underneath") rather than a jargon leak — defensible since it explicitly ties the dashboard to the file users can inspect. Soft signal but not a violation.
