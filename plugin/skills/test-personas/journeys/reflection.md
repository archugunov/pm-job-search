---
name: reflection
persona: diego
snapshot: diego-reflection
max_turns: 20
---

## Goal

A user on Monday morning runs `/today`, sees the weekly-reflection
nudge fire (because Diego's snapshot has prior-week journal entries),
engages with career-coach.

## Opening message

`/pm-job-search:today`

## Mid-journey instructions to the simulator

1. `/today` should ask whether to log updates (binary prompt). Diego
   would answer: pick "Share updates" then mention one thing — "had
   a good prep session for the Retool panel, feel ready".
2. After `/today` prints its brief, the brief should include a weekly-
   reflection nudge ("It's the start of a new week. Want a 5-min
   reflection?"). Diego would answer: "yes".
3. If the skill hands off to career-coach (or invites the
   conversation), Diego would say: "I want to think about whether
   pushing Retool harder or diversifying is the right move this week".

## Termination

Stop when career-coach has had at least one substantive exchange
(transcript contains career-coach reading Diego's profile + strategy
and asking a strategic question or proposing a frame) AND Diego has
replied with at least one substantive answer.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass) or `[opportunistic]` (advisory). See `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md` for verdict aggregation rules.

- **[required]** `/today` showed the binary update prompt (Share updates / Skip), not a "press enter to skip" prompt
- **[required]** `/today` rendered Heads-up section above Pipeline
- **[required]** `/today`'s heads-up surfaced non-obvious risks (not just static reminders)
- **[required]** The weekly-reflection nudge fired (Diego is on Monday with prior-week entries)
- **[required]** Founder-outreach line either omitted (if not in strategy) or matched the strategy's `weekly_targets.founder_outreach` value
- **[required]** The handoff to career-coach was a clear dispatch (not just a suggestion the user has to invoke manually)
- **[required]** career-coach grounded its first message in Diego's profile + strategy
- **[required]** career-coach did NOT just echo a generic framework — referenced Diego's specific situation
