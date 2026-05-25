---
name: help
description: This skill should be used when the user asks for "/help", "/pm-job-search:help", "what does this plugin do", "how do I navigate this", "list the skills", "show me all skills", "give me a tour", "what agents are available", "where do I start", or wants a scannable map of pm-job-search's skills, agents, and recommended order. Prints a one-page reference card to chat covering the 5-phase workflow, all 11 skills with use-when triggers, all 6 agents grouped by purpose, and a recommended first-week flow. Also writes the same card to `userdata/help.md` so it's available for quick reference later. No questions.
---

# /help — print the reference card and save a copy

The canonical user flow and the rules each skill follows for end-of-run nudges live in `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. Read that file to understand what to suggest next based on the user's current state.

The card lives at `${CLAUDE_PLUGIN_ROOT}/skills/help/help.md`. On every run, do all three of these in order:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/help/help.md` and print its contents to chat verbatim. Render exactly as written — headings, tables, code spans. Do not summarise, expand, or paraphrase.

2. Copy the same file to `userdata/help.md`, overwriting. Create `userdata/` first if it doesn't exist. Use `cp` so plugin updates propagate.

3. After the card, print exactly one closing line:

   > Also saved to `userdata/help.md` — open that file anytime for the same reference.

Then stop. No follow-up offers, no questions, no other file reads or writes.
