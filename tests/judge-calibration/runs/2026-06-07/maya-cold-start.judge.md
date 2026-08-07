# Findings — maya-cold-start

**Run date:** 2026-06-07
**Snapshot:** empty
**Plugin install:** v0.3.0-beta.2 (from `<home>/.claude/plugins/cache/pm-job-search/pm-job-search/0.3.0-beta.2/`)

## Verdict

**Overall: FAIL (confirmed)**

- Hard violations: judges disagreed — judge 1 FAIL (mistook blockquotes for fenced code), judge 2 PASS (correctly noted blockquotes are explicitly allowed per Rule B). Treating as PASS on the rule's actual wording.
- Spec gaps: FAIL (both judges agreed — 5 required criteria failed)
- Soft issues: 3 (advisory)
- Open critiques: 4 (advisory)

_Both judge runs returned FAIL on overall verdict. Confirmed: not a single-call false positive._

## Hard violations (lint checklist)

No hard violations found.

Note on judge 1's findings: judge 1 flagged Turns 15, 17, 19 blockquote summaries as Rule B violations. This is incorrect — Rule B's text reads "Fenced code blocks (triple-backtick) as chat summaries" and explicitly names "blockquotes (`>` lines)" as the allowed alternative. Judge 2 correctly excluded these. Logged for future judge-prompt tuning.

## Soft issues (TONE voice + UX)

- **[Voice — hedging]:** Turn 19 heads-up bullets use "typically close within 2-3 weeks" and "may already be tightening" — speculative softeners that the TONE rubric flags as hedging.
- **[Voice — fabricated content]:** Turn 19 brief invents "Pipeline is thin — `/job-search` this week to widen the funnel" and the founder-outreach observation despite strategy.md being freshly initialized with no anti-goals/founder-outreach captured. Soft because not technically a rule violation, but the brief is fabricating recommendations beyond what state warrants.
- **[Voice — meta-leak]:** Turn 1 leaked internal state ("Fresh-install mode, no CV detected.") to user-facing copy. The SKILL.md says run mode detection BEFORE asking; implies silent, not surfaced.

## Spec gaps

### Required (8/13 in scope passed, 5 failed)

Cross-journey:
- **End-of-run nudge:** PASS — Turn 19 closes with "Next move: open the Plaid posting and run `/apply Plaid`."
- **No prior-state leak in messaging:** PASS — no references to past activity.
- **No dead ends:** PASS — every assistant turn offers a forward path.
- **Profile + strategy not silently overwritten:** PASS — Turn 15 names each file written.
- **JD link present in three places:** FAIL — chat row inline (Turn 16) ✓, but meta.md frontmatter `link:` not persisted (evidenced by Turn 19 "(url not captured)"), research-brief.md Source line presumed missing on the same basis.

Cold-start journey-specific:
- **/setup precreated userdata/ before CV prompt:** PASS — CV option offered at Turn 8 after directory scaffolding (workspace already had `userdata/` from prior state).
- **/setup asked one residence question and one geography question — distinct:** PASS — Turn 3 (residence "Where are you based?") + Turn 7 (geography "Where are you looking?") distinct.
- **/setup included "Companies in mind?":** PASS — Turn 13.
- **/setup did NOT show the weekly-reflection nudge:** PASS — no weekly-reflection nudge in Turn 15.
- **/setup's automation prompt was 2-step (y/n first, then time) — not bundled:** FAIL — plugin sub-agent skipped the automation prompt entirely. Went straight from file-write summary to accepting `/pm-job-search:job-search` from the simulator. Required + in-scope + not exercised → FAIL.
- **/job-search auto-filed at least one role with status: new:** PASS — Turn 16 filed 3 roles, all with `status: new`.
- **/job-search set `link:` in every new meta.md frontmatter:** FAIL — Turn 19's /today brief shows "(url not captured)" for all three pipeline rows, indicating `link:` was not written to meta.md during /job-search. (Sub-agent invented `role:` instead of `position:`; may have similar drift on `link:` placement.)
- **applications.md GENERATED block contains a Link column:** NOT EXERCISED — /today did not regenerate applications.md in this run; not visible in transcript.
- **Chat rendering of application row included URL inline:** FAIL — Turn 19 pipeline rows say "(url not captured)" for all three roles despite Turn 16 having URLs. Failed at the /today rendering step.
- **/today's first run skipped the input-loop prompt entirely:** PASS — Turn 19 went straight to brief output.
- **/today's brief rendered Heads-up section above Pipeline:** PASS — Turn 19 has Heads-up before Pipeline.
- **/today did NOT include a hardcoded founder-outreach number:** PASS — no specific number cited.
- **Each skill's closing message included a context-aware next-step nudge:** FAIL — /setup's closing (Turn 15) skipped the documented closing recommended-flow nudge ("Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first."). Required + in-scope + not exercised.

### Opportunistic (0/0 in scope — 1 not applicable)

- **/setup offered the positioning draft (Mode A or Mode B) if persona dropped a CV:** NOT APPLICABLE — persona chose Mode C (skip) at Turn 9; out of scope.

## Open critique

- **Biggest functional failure: link-persistence chain.** /job-search displayed URLs in chat (Turn 16) but didn't persist them to meta.md frontmatter, which surfaces as "(url not captured)" in /today's pipeline (Turn 19). Three required criteria fail from a single root cause — sub-agent didn't write the `link:` field consistently with what other skills read.
- **Schema drift in /job-search meta.md.** Sub-agent wrote `role:` instead of `position:` (the established field). The contrarian-messy snapshot uses `position:`; the new auto-filed roles use `role:`. /today and other skills reading meta.md will trip on this inconsistency.
- **/setup tail behavior incomplete.** The plugin sub-agent skipped both the 2-step automation prompt AND the documented closing recommended-flow nudge — went straight from file writes to accepting the next slash command. Consistent with the 2026-05-27 memory note about sub-agents improvising; suggests the /setup SKILL.md's closing/automation sections may not be making it into the inlined prompt with enough emphasis to override the sub-agent's instinct to wrap quickly.
- **Sub-agent discoverability for slash commands: NO.** The plugin sub-agent dispatched at Turn 1 did NOT invoke `/pm-job-search:setup` as a slash command despite being instructed to if possible. The response came from inlined SKILL.md execution. This is the answer to the Priority 1 gap: sub-agents do not inherit the parent's plugin context. The fallback (inline SKILL.md) IS the runtime mechanism — the slash-command path in the prompt template should be removed or framed as conditional/optional in v0.3.x.
