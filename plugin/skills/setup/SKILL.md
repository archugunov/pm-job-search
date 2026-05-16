---
name: setup
description: This skill should be used when the user asks for "/setup", "set up the plugin", "first-time setup", "install pm-job-search", "configure my profile", "create my profile", or wants to onboard onto pm-job-search for the first time (or re-run onboarding to update a field). Conducts a 10-question conversational install that writes userdata/profile.md, a placeholder userdata/strategy.md, an empty userdata/journal.md, three .gitkeep files, and a CLAUDE.md at the workspace root resolved from the plugin template.
---

# /setup — first-run install and re-configure

Onboard the user onto pm-job-search by filling in `userdata/profile.md` and scaffolding the rest of the userdata tree. Idempotent — safe to re-run.

## Mode detection

Run this BEFORE asking the first question:

1. If `userdata/profile.md` exists → enter **re-run mode**: read the file, ask "keep current / update / skip" per field, never wipe existing answers.
2. If `userdata/profile.md` does NOT exist → enter **fresh-install mode**: ask all 10 questions in order.
3. `--refresh` flag → re-run mode, but only re-resolve the workspace-root `CLAUDE.md` from the template using the current `profile.md` content. Skip all questions. Useful after manual edits to profile.md.

Also detect CV presence (only relevant in fresh-install mode):

- `userdata/cv.md` or `userdata/cv.txt` exists → Mode B available for question 6 (positioning).
- `userdata/cv.pdf`, `userdata/cv.docx`, or any non-md/txt file → print one line: `Found userdata/cv.<ext>. v1 only reads .md or .txt — convert your CV first, or skip and paste positioning instead.` Then proceed with Mode A only.
- No cv.* file → Mode A only (paste positioning).

## Templates

Read these from the plugin install dir (use `${CLAUDE_PLUGIN_ROOT}` if available):

- `${CLAUDE_PLUGIN_ROOT}/templates/profile.template.md` — source for `userdata/profile.md`.
- `${CLAUDE_PLUGIN_ROOT}/templates/strategy.template.md` — source for `userdata/strategy.md`.
- `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.template.md` — source for workspace-root `CLAUDE.md`.

Do not edit these template files. Always treat them as read-only inputs.

## The 10 questions

Ask one at a time. Use AskUserQuestion only when a question has a clear set of options (Q5); otherwise plain conversational ask. Skipping is allowed on Q4 (LinkedIn), Q9 (salary band), Q10 (hard filters) — for skipped fields, leave the placeholder unfilled (write `# unset` or a blank YAML value, not the literal `{{PLACEHOLDER}}` string).

1. **Name** (`{{NAME}}`) — full name. Required.
2. **City** (`{{CITY}}`) — e.g. "London, UK". Required. Also auto-detect timezone via `date +%Z` (or `readlink /etc/localtime` parsed) and fill `{{TIMEZONE}}` without asking; tell the user the detected value and offer to override.
3. **Email** (`{{EMAIL}}`) — required.
4. **LinkedIn URL** (`{{LINKEDIN_URL}}`) — skippable.
5. **Where are you looking?** (`{{GEOGRAPHY_MODE}}` + `{{GEOGRAPHY_DETAIL}}`) — single-select via AskUserQuestion: `On-site in <city-from-Q2>` / `Remote` / `Both` / `Other (free text)`. The first option dynamically uses the city captured in Q2. If the user picks "Other", capture free-text into `mode_detail` and set `mode: other`. For "Both", optionally capture mode_detail (e.g. "London hybrid or EMEA remote") via a follow-up prompt.
6. **Positioning** (`{{POSITIONING}}` + `{{PROOF_POINTS}}` + `{{MOAT}}`) — two modes:
   - **Mode A**: ask the user to paste 1-3 sentences of self-positioning. Draft a 2-paragraph `## Positioning` from it; ask for 3-5 numbered wins to draft `## Proof Points`; ask for one sentence answering "what's the rare thing you bring?" to draft `## Moat`.
   - **Mode B** (if `userdata/cv.md` or `userdata/cv.txt` present): read the CV, draft a positioning paragraph + 5-7 proof points by extracting bullets with numbers, draft a one-sentence moat candidate, show the draft to the user, ask them to edit before save. Never save without explicit user review.
7. **Target titles** (`{{TARGET_TITLES}}`) — comma-separated list from the user. Examples to offer: `Head of Product, Lead PM, Senior PM, VP Product`. Substitute as a YAML inline list: `[Head of Product, Lead PM, Senior PM]` (keeps the template's trailing inline comment intact; the user can reformat to block form later if they prefer).
8. **Target industries** (`{{TARGET_INDUSTRIES}}`) — comma-separated. Examples: `fintech, B2C SaaS, PLG SaaS, DevTools`. Substitute as YAML inline list (same form as Q7).
9. **Salary band** (`{{SALARY_BAND}}`) — single open string. Show two example shapes: `"£90-110K"` and `"$190-230K base + equity"`. Skippable. No validation — accept whatever currency / phrasing the user gives.
10. **Hard filters** (`{{HARD_FILTERS}}`) — sequence of three sub-prompts, each skippable:
    - "Company-size cap? (e.g. 'no more than 500 ppl', or skip)"
    - "Scope cap? (e.g. 'no role with >8 direct reports', or skip)"
    - "Geo cap? (e.g. 'no relocation outside Europe', or skip)"
    Collect non-empty answers into a YAML inline list, with each string quoted: `["no more than 500 ppl", "no role with >8 direct reports"]`. If all three skipped, write `[]`. (Inline form keeps the trailing template comment intact, same reasoning as Q7.)

After Q10: show the senior-PM-tuned tier rubric defaults (the `tier_weights` and `tier_thresholds` blocks from the template, inline) and ask: "Edit any of these now, or use as-is and edit later in profile.md?" If edit, take diffs one rubric line at a time. Default = use as-is.

## Re-run mode question loop

When `userdata/profile.md` exists, iterate fields in the same order (Q1-Q10 + tier rubric). For each:

1. Show the current value (one line).
2. Ask: `keep / update / skip` (skip means "leave as-is for now, ask again next /setup").
3. If `update`: prompt for the new value using the same conversational pattern as fresh-install.

Never overwrite a non-empty field with an empty answer in re-run mode. If the user updates a field but provides empty input, ask once more; if still empty, treat as `skip` and leave the current value.

The user's freeform body sections (`## Tone of Voice`, `## What NOT to Frame As`, and any `##` section they added below the documented ones) are NEVER touched in re-run mode — they belong to the user.

## File writes

After all questions are answered, do these writes in order:

### 1. `userdata/profile.md`

Read the profile template, substitute every `{{PLACEHOLDER}}`, write to `userdata/profile.md`. Preserve all HTML comments and free-form prompt blocks (the `<!-- … -->` sections after each `##` header) verbatim. Substitute placeholders only.

For skipped placeholders: write a sensible empty form, not the literal `{{NAME}}` string. Examples:
- `{{LINKEDIN_URL}}` skipped → `linkedin_url:` (empty value, no quotes).
- `{{SALARY_BAND}}` skipped → `salary_band: ""` (empty string).
- `{{HARD_FILTERS}}` skipped → `hard_filters: []`.
- `{{TARGET_TITLES}}` cannot be skipped (required).

### 2. `userdata/strategy.md` (only if file does not already exist)

Read the strategy template, leave all `{{PLACEHOLDERS}}` AS-IS (do NOT prompt for strategy values during /setup — `/strategy` owns that). Write to `userdata/strategy.md`.

If `userdata/strategy.md` already exists, skip this write. /setup never overwrites strategy.

### 3. `userdata/journal.md` (only if file does not already exist)

Write a minimal journal file:

```markdown
# Journal

<!--
  Free-form notes you write yourself. Date each entry as `## YYYY-MM-DD`.
  /today scans the last 7 days for outreach keywords (DM, outreach, coffee,
  intro, reached out, messaged, connect) to count warm-outreach attempts.
-->
```

### 4. Three `.gitkeep` files

Create these empty files (only if the directory does not already contain a real file — never overwrite content):
- `userdata/companies/.gitkeep`
- `userdata/stories/.gitkeep`
- `userdata/outputs/.gitkeep`

### 5. `CLAUDE.md` at workspace root

Read `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.template.md`. Resolve the single `{{INCLUDE: userdata/profile.md sections=positioning,proof_points,moat}}` marker by:

1. Read the just-written `userdata/profile.md`.
2. Extract the body content under `## Positioning`, `## Proof Points`, and `## Moat` (stop at the next `##` heading).
3. Concatenate them in that order, each preceded by its heading line, separated by one blank line.
4. Replace the entire `{{INCLUDE: …}}` line with that concatenated block.

Write the result to `CLAUDE.md` at the workspace root (one level above `userdata/`). Overwrite any existing `CLAUDE.md` at the root only if it begins with the same `<!--` template-header comment as the template (signature of a previously generated file). If it doesn't, ask the user before overwriting: `CLAUDE.md exists at workspace root and was not generated by pm-job-search. Overwrite (y/N)?`

## Closing offers

Print a brief summary of what was written (one line per file), then offer, in this order:

1. **Positioning refinement.** Say: `Want to refine your positioning before we wrap? I can hand off to the tech-career-coach agent for a ~5-minute interview that rewrites your positioning paragraph. Skip if you'd rather edit profile.md yourself.` If yes, invoke the `tech-career-coach` agent with the just-written `userdata/profile.md` as input. If no, move on.

2. **Strategy.** Say: `Ready to set your strategy? /strategy walks you through goals, weekly targets, and anti-goals in ~15-20 minutes — and unlocks the progress-tracking part of /today. Skip and you can run /strategy anytime.` If yes, suggest the user invoke /strategy next. If no, move on.

Either offer is fully skippable. The install is valid without them.

## What /setup never does

- Never edits `.claude/settings.json` or any Claude Code system config.
- Never runs `git init` or `git commit`. The repo lives in the user's workspace; the user manages it.
- Never validates any external service (no MCP, no API).
- Never writes `userdata/companies/*`, `userdata/stories/*`, or `userdata/outputs/daily-brief-*.md` — those belong to other skills.
- Never overwrites `userdata/strategy.md` if it exists. `/strategy` owns updates.
- Never overwrites `userdata/profile.md`'s body sections in re-run mode (only frontmatter fields the user explicitly updates).
- Never invents proof-point numbers. If the CV in Mode B doesn't have a metric for a bullet, surface it as a draft bullet without numbers and ask the user to fill in.

## Smoke test against the Maya example

Treat `userdata/examples/maya/` as a synthetic install root. Re-running /setup against it should:

- Detect existing `profile.md` → enter re-run mode.
- Show current values (Maya Patel, London UK, Europe/London, etc.) — each as `keep / update / skip`.
- If user picks `keep` for all: only re-resolve workspace-root `CLAUDE.md`. No other files change. Profile body sections (Positioning, Proof Points, Moat, Tone of Voice, What NOT to Frame As) untouched.
- The tier rubric in profile.md is unchanged (the values in Maya's file are the same as the template defaults).

A fresh-install run (against an empty userdata/) should produce a profile.md whose frontmatter shape is identical to Maya's, only with the user's own answers in place of placeholders.
