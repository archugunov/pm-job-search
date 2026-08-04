---
name: cold-start-cv
persona: maya
snapshot: empty-with-cv
max_turns: 24
---

## Goal

A new user who dropped their CV before running `/setup`. Tests the CV-first
path: extraction, the one-line facts confirmation, and the inferred
titles/industries steps. Stops after `/setup` — the downstream loop is already
covered by `cold-start`.

## Opening message

`/pm-job-search:setup`

## Mid-journey instructions to the simulator

The simulator stays in persona throughout. Two scripted behaviours:

1. When `/setup` presents the facts line for confirmation, correct exactly one
   field — reply that the email is wrong and give a different one. This tests
   that a correction is applied inline without re-asking the whole line.
2. When `/setup` presents inferred target titles, deselect one of the offered
   options and add one of your own via the "Other" escape.

## Termination

Stop when `/setup` has printed its closing file summary (transcript contains
`userdata/profile.md`) AND the simulator has acknowledged it with a brief reply.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass) or `[opportunistic]` (advisory). See `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md` for verdict aggregation rules.

- **[required]** `/setup` detected the existing `userdata/cv.md` without asking the user to drop one
- **[required]** `/setup` presented name, city, email and LinkedIn as a SINGLE confirmation line, not as four separate questions
- **[required]** The corrected email was applied and `/setup` did not re-ask the whole facts line
- **[required]** Target titles were offered as a multi-select with an evidence line naming roles from the CV
- **[required]** Target industries were offered as a multi-select with an evidence line
- **[required]** The deselected title is absent from `profile.md`'s `target_titles`, and the user-added one is present
- **[required]** `/setup` never asked for name, city or email as standalone questions when the CV supplied them
- **[required]** No value in `profile.md` is absent from the CV and unconfirmed by the user — nothing was invented to fill a field
- **[required]** `/setup` did NOT ask about companies of interest
- **[required]** `profile.md` frontmatter contains every documented key, with the same names and shapes as `userdata/examples/maya/profile.md`
- **[required]** Salary was the only step requiring free-text input
- **[opportunistic]** The positioning draft (Mode B) ran without re-prompting for a CV
