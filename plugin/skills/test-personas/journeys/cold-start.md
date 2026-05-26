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

- `/setup` precreated `userdata/` (or confirmed it already existed) before the CV prompt
- `/setup` asked one geography question, not two
- `/setup` included a "Companies in mind?" question
- `/setup` did NOT show the weekly-reflection nudge (it was moved to `/today`)
- `/setup`'s automation prompt was 2-step (y/n first, then time) — not bundled
- `/job-search` auto-filed at least one role with `status: new` in `meta.md`
- `/job-search` set `link:` in every new `meta.md`'s frontmatter
- `applications.md` GENERATED block contains a `Link` column
- The chat rendering of the application row included the URL inline
- `/today`'s first run skipped the input-loop prompt entirely (no "anything that moved since last time")
- `/today`'s brief rendered Heads-up section ABOVE Pipeline state
- `/today` did NOT include a hardcoded founder-outreach number (no "10 founders")
- Each skill's closing message included a context-aware next-step nudge
