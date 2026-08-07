# Findings — maya-cold-start

**Run date:** 2026-06-04
**Snapshot:** empty

## Verdict

**Overall: FAIL (confirmed)**

- Hard violations: FAIL
- Spec gaps: FAIL
- Soft issues: 2 (advisory)
- Open critiques: 4 (advisory)

_Confirmation re-run dispatched; second judge also returned FAIL. Verdict is confirmed; not a single-call false positive._

## Hard violations (lint checklist)

- **[Rule 6 — Internal jargon leaking into user-facing copy]:** quoting Turn 9: "Q7: What roles are you targeting?" — leaks internal question numbering, matching the 2026-05-27 memory note about sub-agents leaking Q1/Q5/Q7 labels (transcript quote, not memory alone).
- **[Rule 4 — Hardcoded numbers in instructions]:** quoting Turn 1: "Twelve quick questions" — hardcodes a count in user-facing copy; brittle if the question list changes.

## Soft issues (TONE voice + UX)

- **[Voice — no hedging or preambles]:** quoting Turn 1: "OK, let's get you set up. Twelve quick questions — none of it locked in, you can rerun anytime. Ready?" — preamble plus a confirmation gate before the first real question; could open with Q1 directly.
- **[Rule C smell — prior-state implication on first run]:** quoting Turn 4: "I'm seeing your timezone as `Europe/London` — that right? Override if not." — framing implies system state on a cold-start first run; would read more naturally as a direct ask or genuine derivation.

## Spec gaps

### Required (1/3 in scope passed; 15 not exercised due to early termination)

Cross-journey:
- **End-of-run nudge:** FAIL — journey was supposed to reach termination but transcript stopped mid-/setup at Q7.
- **No prior-state leak in messaging:** PASS — no references to past activity in turns 1–10.
- **No dead ends:** FAIL — Turn 9 references `--refresh` flag with no documented support path; user could be stranded if they try to resume.
- **Profile + strategy not silently overwritten:** NOT EXERCISED — setup never reached the write step; counts as FAIL because the journey was supposed to reach it.
- **JD link present in three places:** NOT EXERCISED — /job-search never ran; counts as FAIL.

Cold-start journey-specific:
- **/setup precreated userdata/ before the CV prompt:** FAIL — no scaffolding message before the CV ask at Turn 8.
- **/setup asked one residence question and one geography question — distinct asks:** PASS — Turn 3 (residence) and Turn 7 (geography) are distinct.
- **/setup included a "Companies in mind?" question:** NOT EXERCISED — transcript ended before this; counts as FAIL.
- **/setup did NOT show the weekly-reflection nudge:** PASS — no nudge in turns 1–10.
- **/setup's automation prompt was 2-step:** NOT EXERCISED — counts as FAIL.
- **/job-search auto-filed at least one role with status: new:** NOT EXERCISED — counts as FAIL.
- **/job-search set link: in every new meta.md frontmatter:** NOT EXERCISED — counts as FAIL.
- **applications.md GENERATED block contains a Link column:** NOT EXERCISED — counts as FAIL.
- **Chat rendering of application row included URL inline:** NOT EXERCISED — counts as FAIL.
- **/today's first run skipped the input-loop prompt entirely:** NOT EXERCISED — counts as FAIL.
- **/today's brief rendered Heads-up section above Pipeline:** NOT EXERCISED — counts as FAIL.
- **/today did NOT include a hardcoded founder-outreach number:** NOT EXERCISED — counts as FAIL.
- **Each skill's closing message included a context-aware next-step nudge:** FAIL — no skill closed in this transcript.

### Opportunistic (0/1 in scope passed)

- **/setup offered the positioning draft (Mode A or Mode B) if persona dropped a CV:** NOT EXERCISED — persona chose Mode C (skip) at Turn 9; out of scope.

## Open critique

- The opening "Twelve quick questions" miscounts — the skill description specifies a 12-question install, but if it changes the hardcoded text lies. Should be phrased as "a handful of quick questions" or derived dynamically.
- "Q7:" surfaced at Turn 9 reveals the script's internal numbering — exact failure mode flagged in the 2026-05-27 memory note about sub-agents leaking Q1/Q5/Q7 labels. The user sees scaffolding instead of conversation.
- Turn 9's offer to resume via `--refresh` is presented as a known flag with no fallback; if the persona later types it and it fails, they're stranded mid-onboarding with no recovery path.
- The transcript terminates mid-setup (after Q7) so the bulk of the cold-start journey — Companies-in-mind, automation prompt, /job-search, /today, /dashboard — is wholly unverified. The verdict reflects the spec's instruction to treat missed required criteria as FAIL when the journey was supposed to cover them, but the underlying issue is test-harness coverage, not necessarily skill defects.
