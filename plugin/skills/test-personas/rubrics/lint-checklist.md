# Rubric: Lint checklist (hard violations)

These are unambiguous structural violations. If present in the transcript, flag as a hard violation.

1. **Fenced code blocks (triple-backtick ` ``` `) used as chat summaries.** Triple-backtick blocks rendering a summary to the user (rendered, not stored on disk) are a violation. **Markdown blockquotes (`> ` lines) are explicitly NOT a violation — they are the documented allowed alternative.** Convert fenced code summaries to blockquote or plain prose. Allowed exceptions: fenced blocks for files-on-disk content, shell commands, and inline-rendered file contents that the user is meant to copy verbatim.
2. **Two unrelated questions or decisions in one assistant message.** Rule A. Split into sequential prompts.
3. **Reference to a non-existent skill or file.** A `/pm-job-search:<name>` slash command that doesn't resolve to a directory under `plugin/skills/`, or a `${CLAUDE_PLUGIN_ROOT}/<path>` that doesn't resolve to a real file.
4. **Hardcoded numbers in instructions** (e.g. "DM 10 founders", "every 9am"). Cadences should come from `userdata/strategy.md` or `userdata/profile.md`.
5. **Prior-state prompts on a skill's first run.** Rule C. The skill asks "anything that moved since last time?" when no prior state exists (e.g. empty `userdata/journal.md`).
6. **Internal jargon leaking into user-facing copy** ("frontmatter", "tier_weights", "P0/P1/P2", "meta.md") without explanation, in a user-visible message.
7. **Schema drift in files written by the plugin during the run.** Sourced from the Phase 3.5 schema validation block, NOT from the transcript. Each schema finding (missing required key, wrong field name like `role:` instead of `position:`, status outside the allowed enum, malformed link) is a Hard violation. Schema drift propagates silently into downstream skills, so it's flagged here rather than under Soft issues. See `${CLAUDE_PLUGIN_ROOT}/schemas/meta.md.schema.md` for the canonical schema definitions.

## How to report findings under this rubric

For each violation: quote the exact line from the transcript (with turn number) OR cite the Phase 3.5 schema finding verbatim (for Rule 7), name the violation number (1-7), and quote the rule text.

Rule 7 findings come from the `--- SCHEMA VALIDATION ---` block in the judge input, not from transcript quotes. Each schema finding in that block translates to one Rule 7 hard violation.
