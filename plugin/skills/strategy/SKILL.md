---
name: strategy
description: This skill should be used when the user asks for "/strategy", "set my strategy", "set my goals", "update my strategy", "weekly targets", "set targets", "anti-goals", "checkpoints", or wants to revisit their job-search goals and the cadence they're holding themselves to. Conducts a 15-20 minute conversational reflection that writes userdata/strategy.md (target offer date, weekly_targets, pipeline_targets, checkpoints, headline goal, anti-goals). Idempotent — re-run anytime to update fields without losing the rest.
---

# /strategy — set or refresh your job-search strategy

Walk the user through a structured ~15-20 minute reflection that produces or updates `userdata/strategy.md`. This is the file `/today` reads to convert pipeline state into progress tracking. Conversational, not a form — every value asked for is meant to make the user think, not just type.

## Inputs

- `userdata/profile.md` — read frontmatter for context (`target_titles`, `target_industries`, `salary_band`) so the conversation can reference what the user already committed to. Do NOT echo it back wholesale; use it to ground questions ("Given you're targeting Head of Product roles in fintech…").
- `userdata/strategy.md` if present. /setup writes a placeholder file; treat any field whose value still matches `{{…}}` as **unfilled** (ask for it). Treat any field with a substituted value as **set** (offer keep/update/skip).
- `${CLAUDE_PLUGIN_ROOT}/templates/strategy.template.md` — only used to recreate the file from scratch if `strategy.md` is missing entirely. Normally /setup will have placed the placeholder version, so a "missing" strategy.md is a rare edge case.

## Mode detection

1. **`userdata/strategy.md` missing** → write a fresh copy from the template, then proceed as if every field were unfilled (skip nothing).
2. **All fields are still `{{PLACEHOLDER}}`** (fresh post-/setup state) → first-time strategy reflection. Ask every theme below in full.
3. **Some fields filled, some `{{PLACEHOLDER}}`** → ask only for unfilled fields. Show filled fields as context ("Your current target offer date is 2026-08-01 — keeping that for this pass").
4. **All fields filled** → full re-run. Walk every theme but show current values and ask `keep / update / skip` for each.

`--theme <theme-name>` flag (optional) lets the user jump to a single theme (e.g. `/strategy --theme checkpoints`). Useful for quick mid-search updates.

## The five themes

Walk them in this order. Don't batch — ask one theme at a time, let the user reply, then move on. The whole flow is ~15-20 min; rushing it defeats the purpose. If the user pushes back ("just ask me everything at once"), comply — but lose the reflection value.

### Theme 1 — Destination and timeline (target_offer_date, headline goal)

Frame the open question: *"Picture the search done. What does the offer letter look like — role, level, comp floor, location — and by when?"*

Capture two outputs:
- `target_offer_date`: a specific `YYYY-MM-DD`. Push back if the user gives a vague window ("sometime in summer") — ask for a concrete date even if it's their best guess; vague dates make countdown noise.
- `## Headline goal`: one paragraph in their own words. Encourage concrete nouns (role level, comp floor, geo, runway floor). Discourage adjectives like "great" or "challenging" — useless for `/today` to surface back. Aim for 3-5 sentences.

Re-run mode: show current values, ask `keep / update / skip`.

### Theme 2 — Weekly cadence (weekly_targets)

Frame: *"What pace can you actually keep, week after week — not what you wish you could? Two numbers: warm-outreach attempts (DMs, intro asks, coffees scheduled), and formal applications submitted."*

Capture:
- `weekly_targets.warm_outreach`: integer. Typical range 3-10 for active search; 1-2 for passive. If the user gives a wildly ambitious number (>15) push back once: *"That's three a day every weekday. Is that sustainable or is that a stretch goal?"* — accept whatever they confirm.
- `weekly_targets.applications`: integer. Typical 1-5 for senior roles (where curation matters more than volume). Don't push on this one; accept the answer.

Either can be skipped (write `null` or omit the key); /today will skip that bullet rather than report against 0.

### Theme 3 — Pipeline floor (pipeline_targets)

Frame: *"What's the floor below which you'd say 'something's off — I need to act'? Two numbers: active interview threads at any time, and total P0 companies in any active status."*

Capture:
- `pipeline_targets.active_interview_threads`: integer. Typical 2-5. Lower than that = thin pipeline; higher = probably overcommitted.
- `pipeline_targets.p0_pipeline_size`: integer. Typical 3-8. This is the leading indicator — drops here predict drops in active threads by 4-6 weeks.

### Theme 4 — Pre-committed decisions (checkpoints)

Frame: *"Pre-commit two or three if-then decisions. 'If by date X I'm in state Y, then I'll do Z.' This is the part of the strategy that protects you from sunk-cost reasoning when the search drags."*

Capture `checkpoints` as a YAML list of `{date, condition, action}` objects. Walk one at a time:
- *Date* (`YYYY-MM-DD`) — usually 4-8 weeks out from today.
- *Condition* (string) — what observable state would trigger the action (e.g. `<2 active final-round threads`).
- *Action* (string) — the specific move (e.g. `expand search to include Senior PM at P0 companies; lower domain-fit threshold one notch`).

Aim for 2-3 checkpoints total. After each one, ask "Another, or are we good?" — don't drag this past the user's tolerance.

Re-run mode: show existing checkpoints, ask per checkpoint `keep / update / remove / add another`.

### Theme 5 — Anti-goals

Frame: *"What WON'T you do during this search — even if you'd consider it in general? These extend the hard_filters in profile.md with situational, time-bounded exclusions."*

Capture `## Anti-goals` as a free-form bullet list (3-7 items). Useful seed prompts (offer one at a time if the user stalls):
- *Company shapes that burned you before that you're avoiding now?*
- *Compromises that would make this role the wrong job even if it pays?*
- *Timing constraints (relocation, family, runway) that cap the choice?*

Re-run mode: show current anti-goals. Offer to add to the list, remove items, or rewrite. Never silently overwrite — the user's body content here is theirs.

## File write

Write to `userdata/strategy.md`. Preserve the template header HTML comment block at the top verbatim. Field-by-field rules:

- **Frontmatter scalars** (`target_offer_date`, `weekly_targets.*`, `pipeline_targets.*`): substitute each `{{PLACEHOLDER}}` with the user's answer. For skipped optional targets (the two `weekly_targets` and two `pipeline_targets` keys are individually skippable), write the literal YAML value `null` rather than leaving the placeholder. Example:
  ```yaml
  weekly_targets:
    warm_outreach: 5
    applications: null
  ```
- **`checkpoints`**: substitute `{{CHECKPOINTS}}` with a YAML block list, indented two spaces. For an empty list (user skipped all), write `[]` inline. Example:
  ```yaml
  checkpoints:
    - date: 2026-06-15
      condition: "<2 active final-round threads"
      action: "expand search to include Senior PM at P0 companies; lower domain-fit threshold one notch"
    - date: 2026-07-15
      condition: "no offers in hand"
      action: "open conversations with two specialist fintech recruiters"
  ```
- **`## Headline goal`**: substitute `{{HEADLINE_GOAL}}` with the captured paragraph. Preserve the surrounding HTML comment block.
- **`## Anti-goals`**: replace the body of this section with the captured bullet list. PRESERVE the section's HTML comment block (the prompt hints) — they stay above the bullet list for re-run reference. New bullets go after the closing `-->` of the comment.

Idempotent rules:
- Never overwrite a field the user picked `keep` for in re-run mode.
- Never wipe the body of `## Headline goal` or `## Anti-goals` without an explicit user `update`. If a re-run picks `skip` for these, leave them untouched.
- If the file existed and is being updated, append `<!-- Last edited by /strategy on YYYY-MM-DD -->` at the very bottom of the file (after the last section). On subsequent runs, replace that line in place rather than stacking new ones.

## Closing

Print a one-line summary of what changed (e.g. `Updated: target_offer_date, weekly_targets.warm_outreach, +1 checkpoint. Kept: pipeline_targets, anti-goals.`).

Offer: *"Run `/today` to see this strategy reflected in your daily brief."* Skip the offer if the user invoked /strategy via `/strategy --theme`.

## What /strategy never does

- Never reads or modifies `userdata/companies/*`, `userdata/stories/*`, or any outputs.
- Never touches `userdata/profile.md` — strategy and identity are separate files for a reason.
- Never invents target numbers. If the user says "I don't know" for a weekly target, write `null` and tell them /today will skip that bullet until they set it.
- Never adds anti-goals the user didn't say (even if they seem obviously sensible). The list is theirs.
- Never auto-fills `checkpoints` from a template. The point of pre-committed decisions is that the user wrote them; defaults defeat the purpose.

## Smoke test against the Maya example

Treat `userdata/examples/maya/` as a synthetic install root. Re-running /strategy there should:

- Detect existing strategy.md → enter full re-run mode (all fields set).
- Show current values per theme: target 2026-08-01, warm_outreach 5, applications 3, active_threads 4, p0_pipeline 6, two checkpoints (2026-06-15 and 2026-07-15), 5 anti-goal bullets.
- If user picks `keep` for everything: append the `<!-- Last edited by /strategy on YYYY-MM-DD -->` line at file bottom, no other changes.
- A `/strategy --theme checkpoints` invocation against Maya should jump straight to Theme 4, show both checkpoints, ask keep/update/remove per checkpoint + "add another?". No other themes visited.

A fresh-install run (against a userdata/ where /setup just wrote a placeholder strategy.md) should ask every theme, capture answers, substitute all `{{…}}` markers, and leave the template header HTML comment intact at the top.
