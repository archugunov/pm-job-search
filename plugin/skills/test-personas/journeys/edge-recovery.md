---
name: edge-recovery
persona: contrarian
snapshot: contrarian-messy
max_turns: 25
---

## Goal

Stress test edge cases: duplicate company entries (same `company:` name
across two folders with different slugs), stale `to_apply` (20+ days),
missing strategy fields, incomplete profile. Tests whether the plugin
degrades gracefully or breaks.

## Opening message

`/pm-job-search:today`

## Mid-journey instructions to the simulator

1. `/today` should run end-to-end against the messy snapshot. Sam
   (contrarian) answers any update prompt with "skip".
2. After `/today` finishes, send: `/pm-job-search:dashboard`
3. After the dashboard launch, send: `/pm-job-search:job-search`
4. `/job-search` may ask clarifying questions (since strategy is
   sparse). Sam answers each with "skip" or "I don't know".
5. After `/job-search` completes (or fails gracefully), send:
   `/pm-job-search:evaluate-position https://example.com/some-role`
   (a fictional URL — the skill should handle the unreachable URL
   gracefully).

## Termination

Stop when 5 skills have been invoked (`/today`, `/dashboard`, `/job-search`,
`/evaluate-position`, plus one follow-up the plugin nudged toward) OR
max_turns is reached, whichever comes first.

## Spec criteria (judge checks)

- `/today` ran without crashing despite missing profile sections
- `/today` skipped the founder-outreach line entirely (strategy has
  no `weekly_targets.founder_outreach`)
- `/today` flagged StaleCorp in heads-up (20+ days in to_apply)
- `/today` either flagged the duplicate AcmeCorp entries (two folder
  slugs `acmecorp/` and `acme-corp/` sharing `company: AcmeCorp` in
  frontmatter) or handled the near-duplicate without error
- `/job-search`'s candidate sourcing handled the empty "Companies of
  interest" gracefully (no error, no infinite loop)
- `/evaluate-position` with an unreachable URL produced a clear error
  message, not a stack trace or hung session
- No skill prompted Sam for previously-skipped fields again in the
  same session (no nag loop)
- Every skill closed with a usable next-step nudge despite the messy
  state
