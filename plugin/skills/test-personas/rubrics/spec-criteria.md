# Rubric: Cross-journey common criteria

These criteria apply to every journey. The journey file's own `## Spec criteria` section adds journey-specific items on top.

1. **End-of-run nudge.** The final skill in the journey closes with a context-aware next-step nudge derived from `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. Not a generic parrot of the canonical order — a state-aware suggestion.
2. **No prior-state leak in messaging.** Skill outputs that mention "since last time" or "your previous run" must correspond to actual prior state (file existing, journal entry present).
3. **No dead ends.** Every skill terminates with one of: a clear next action, an offered skip, or a "you're done" acknowledgement. No transcript should end mid-prompt awaiting input the journey didn't provide.
4. **Profile + strategy not silently overwritten.** If a skill writes to `userdata/profile.md` or `userdata/strategy.md`, the transcript must show a confirmation message naming what changed.
5. **JD link present in three places** (when /job-search runs):
   - `meta.md` frontmatter `link:` field
   - `research-brief.md` Source line
   - Chat row rendering (e.g. `- Plaid — Senior PM — to apply — https://...`)

## How to report findings under this rubric

For each criterion not met: name the criterion number (1-5) and explain what the transcript showed (or didn't show) that violates it.

For each criterion met: name the criterion number and briefly cite the transcript line(s) that satisfy it.
