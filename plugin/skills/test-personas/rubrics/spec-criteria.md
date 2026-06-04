# Rubric: Cross-journey common criteria

These criteria apply to every journey. The journey file's own `## Spec criteria` section adds journey-specific items on top.

## Required vs opportunistic convention

Every criterion in this rubric and in every journey file is annotated with one of two tags:

- **`[required]`** — must be exercised AND pass for the journey to PASS verdict. If a required criterion is "not exercised" when it was in scope (its preconditions were met), the journey's spec-gaps verdict is FAIL.
- **`[opportunistic]`** — nice to have. Can be "not exercised" or "fail" without affecting the verdict. Surfaced for awareness but never blocks a release.

Some criteria are conditional — they only apply when a specific skill ran or a specific state was reached. Each conditional criterion has an `Applies when:` line. If the precondition wasn't met, the criterion drops to "not exercised" and the [required] tag doesn't trigger a fail.

## Cross-journey criteria

1. **[required] End-of-run nudge.** The final skill in the journey closes with a context-aware next-step nudge derived from `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. Not a generic parrot of the canonical order — a state-aware suggestion.
   *Applies when:* the journey reached termination (transcript didn't max-out turns).

2. **[required] No prior-state leak in messaging.** Skill outputs that mention "since last time" or "your previous run" must correspond to actual prior state (file existing, journal entry present).
   *Applies when:* any skill in the journey wrote messaging referencing past activity.

3. **[required] No dead ends.** Every skill terminates with one of: a clear next action, an offered skip, or a "you're done" acknowledgement. No transcript should end mid-prompt awaiting input the journey didn't provide.
   *Applies when:* always.

4. **[required] Profile + strategy not silently overwritten.** If a skill writes to `userdata/profile.md` or `userdata/strategy.md`, the transcript must show a confirmation message naming what changed.
   *Applies when:* a skill in the journey wrote to one of those files.

5. **[required] JD link present in three places.**
   - `meta.md` frontmatter `link:` field
   - `research-brief.md` Source line
   - Chat row rendering (e.g. `- Plaid — Senior PM — to apply — https://...`)

   *Applies when:* `/job-search` ran in the journey AND filed at least one new role.

## How to report findings under this rubric

For each criterion: name the criterion number (1-5), state `PASS`, `FAIL`, or `NOT EXERCISED`, and provide evidence — a quote when PASS or FAIL, a one-line reason ("`/job-search` did not run") when NOT EXERCISED.

When in doubt about scope, prefer `NOT EXERCISED` over `FAIL`. Verdict aggregation only penalises [required] criteria that were in scope.
