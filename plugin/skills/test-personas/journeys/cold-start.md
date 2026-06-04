---
name: cold-start
persona: maya
snapshot: empty
max_turns: 30
---

## Goal

A new user goes from empty userdata to a working daily loop. Tests
the onboarding spine: `/setup` → `/job-search` → `/dashboard` → first `/today`.

## Opening message

`/pm-job-search:setup`

## Mid-journey instructions to the simulator

The simulator follows these scripted hand-offs when the plugin reaches
each checkpoint, otherwise stays in persona.

1. After `/setup` wraps (look for "Saved as profile.md", "Let's wrap",
   or a clear closing nudge), send: `/pm-job-search:job-search`
2. After `/job-search` finishes its run summary (look for "Filed N new
   roles" or similar), pick the top-listed role from the run summary
   and say: `mark <Company> to apply` (substitute the actual company
   name from the summary).
3. After the status-change confirmation, send: `/pm-job-search:dashboard`
4. After the dashboard launch message, send: `/pm-job-search:today`

## Termination

Stop when `/today`'s brief has printed (transcript contains `## Heads-up`
or `Nothing flagged today.`) AND the simulator has acknowledged it
with a brief reply.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass) or `[opportunistic]` (advisory). See `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md` for verdict aggregation rules.

- **[required]** `/setup` precreated `userdata/` (or confirmed it already existed) before the CV prompt
- **[required]** `/setup` asked one residence question (Q2 "city + country") and one geography question (Q5 "where are you looking") — distinct asks, not redundant
- **[required]** `/setup` included a "Companies in mind?" question
- **[required]** `/setup` did NOT show the weekly-reflection nudge (it was moved to `/today`)
- **[required]** `/setup`'s automation prompt was 2-step (y/n first, then time) — not bundled
- **[required]** `/job-search` auto-filed at least one role with `status: new` in `meta.md`
- **[required]** `/job-search` set `link:` in every new `meta.md`'s frontmatter
- **[required]** `applications.md` GENERATED block contains a `Link` column
- **[required]** The chat rendering of the application row included the URL inline
- **[required]** `/today`'s first run skipped the input-loop prompt entirely (no "anything that moved since last time")
- **[required]** `/today`'s brief rendered Heads-up section ABOVE Pipeline state
- **[required]** `/today` did NOT include a hardcoded founder-outreach number (no "10 founders")
- **[required]** Each skill's closing message included a context-aware next-step nudge
- **[opportunistic]** `/setup` offered the positioning draft (Mode A or Mode B) if the persona dropped a CV
