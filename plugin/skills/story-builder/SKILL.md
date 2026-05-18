---
name: story-builder
description: This skill should be used when the user asks to "/story-builder", "build a story", "add a STAR story", "edit my story", "work on my story bank", "I want to capture a story", "what stories am I missing", "/story-builder --gap-check", or wants to maintain the universal STAR-story bank that /interview-prep draws from. Lists existing userdata/stories/*.md by title for the user to pick (edit), describes a new one, or with --gap-check reports which senior-PM story types are missing from the bank. Writes userdata/stories/<kebab-slug-from-title>.md with STAR sections + "Angles for different prompts" + frontmatter (title, story_type, themes, role_lens, companies_used_in, last_practised).

---

# /story-builder — maintain the universal STAR-story bank

Conversational skill that builds and maintains `userdata/stories/*.md` — the universal bank that `/interview-prep` adapts per-interview. One story per file. Filenames are auto-derived from titles; the user never types a filename.

**Voice:** every prompt (picker, STAR-section asks, angle drafting) follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — for a NEW story, accept the user's rough first draft, then ask one targeted question at a time only if the draft needs it. Don't force the full STAR conversation when the user clearly has the story in their head already.

## Inputs

- All `userdata/stories/*.md` files. Read frontmatter (`title`, `story_type`, `themes`, `role_lens`, `last_practised`) — body only when an existing story is selected for editing.
- `userdata/profile.md` — read `## Positioning`, `## Proof Points`, `## Tone of Voice`, `## What NOT to Frame As`. Use Tone of Voice to shape draft prose; check drafts against "What NOT to Frame As" before showing. Read `target_titles` from frontmatter for level-weighting in coverage analysis.
- Story taxonomy: `userdata/references/story-taxonomy.md` if present, else `${CLAUDE_PLUGIN_ROOT}/references/story-taxonomy.md` (userdata override per TONE.md convention). Provides the 12 story types + coverage matrix + level-differentiation patterns.
- Optional flags:
  - `--new <"title">` skips the picker and goes straight to new-story flow with the given title.
  - `--edit <slug>` loads a story by filename slug.
  - `--gap-check` runs coverage analysis only — no edit flow. See Mode 4 below.

If `userdata/profile.md` is missing, tell the user to run `/setup` first.

## Mode 1: Picker (default)

If no flag, build a picker. List every `userdata/stories/*.md` as:

```
1. Payments pricing experiment            [themes: growth, pricing, experimentation, post-PMF]  (last practised 2026-05-11)
2. Cross-functional review process        [themes: leadership, process]                           (last practised 2026-04-22)
3. Underwriting integration               [themes: 0-to-1, data, fintech]                         (never practised)
4. + New story (describe one)
5. Cancel
```

Sort by `last_practised` descending, with never-practised at the bottom but above the action items. Use AskUserQuestion for the pick if the list is ≤4; otherwise present as numbered text and ask for a number. Always include "+ New story" and "Cancel" as final options.

If picker is empty (no stories yet), skip straight to new-story flow.

**Coverage line.** Below the picker, print a single coverage summary line drawn from the story-taxonomy reference:

```
Coverage: <N>/12 story types covered. Missing: <comma list of missing type names, max 3 shown, "+ K more" if longer>. Run /story-builder --gap-check for details.
```

Stories without a `story_type:` frontmatter field count as `unclassified` and don't contribute to the N/12 count. If unclassified stories exist, append: `(<M> stories unclassified — edit to add story_type)`. Skip the coverage line entirely if zero stories exist (picker goes straight to new-story flow).

## Mode 2: New-story flow

Walk these steps in order:

### Step 1 — Title

Ask: *"Give the story a short title — 3-6 words, describing the work not the outcome (e.g. 'Payments pricing experiment', not '+18% MRR in Q3')."*

When you have it:
- Compute the filename slug: lowercase, ASCII letters/numbers/hyphens only, collapse runs of non-alphanum to single `-`, strip leading/trailing `-`. Examples: `Payments pricing experiment` → `payments-pricing-experiment`.
- Check `userdata/stories/<slug>.md` doesn't already exist. If it does, tell the user: `That slug collides with an existing story (<existing-title>). Pick a different title or use /story-builder to edit the existing one.` Bail if the user can't resolve.

### Step 2 — STAR body (one section at a time)

Ask one prompt per STAR section. Conversational, not a form. Use the user's `## Tone of Voice` from profile for the drafted prose:

- **Situation** — *"Set the scene: company, role, scope, what was true at the start. 1-2 paragraphs."*
- **Task** — *"What was YOUR remit specifically? Don't describe the team's task; describe yours. 1 paragraph."*
- **Action** — *"What did you actually do? 3-5 bullets, each a concrete step, with WHO you worked with and HOW."*
- **Result** — *"What measurably changed? 2-4 bullets with numbers where possible. Include the things that didn't go as planned, not just the wins."*

After each section, show the drafted version and ask `keep / rewrite / tweak`. Honor the user's tone. Don't pad prose to sound bigger than the work was.

### Step 3 — Angles for different prompts

The angles section is what makes a story reusable. Walk the user through 3-5 angle bullets. For each:
- Pick (or accept the user's nomination of) an interview-prompt type, formatted as a question in bold-quote form, e.g. `**"Tell me about a 0-to-1."**`.
- Write a 1-3-sentence framing instruction (NOT the answer itself — the *lead* to use). Example: `Lead with the *framework* as the 0-to-1, not the test results. The thing that didn't exist was the gating model.`

Common interview-prompt types to suggest if the user is unsure (don't add unless the story actually supports them):
- "Tell me about a 0-to-1."
- "Tell me about leading through ambiguity."
- "Tell me about working with the CEO / founder."
- "Tell me about working with engineering."
- "Tell me about a time you disagreed with a stakeholder."
- "Tell me about a failure."
- "Tell me about analytics depth."

Aim for 3-5 angles. Each must have a distinct *lead*; an angle that just reformulates the result isn't a new angle.

### Step 4 — Frontmatter

Build the YAML frontmatter from the conversation, asking only for what can't be inferred:

```yaml
---
title: <verbatim from Step 1>
story_type: <one of the 12 types from story-taxonomy.md, or unclassified>
themes: [<comma list, 3-6 tags>]
role_lens: [<comma list, subset of: strategy, execution, analytics, leadership, design, eng-collaboration>]
companies_used_in: []        # empty until /interview-prep uses it
last_practised:              # blank until /interview-prep marks it
---
```

- `story_type`: SUGGEST from the body. Read the story-taxonomy reference; match the body against the 12 type descriptions; offer the best 1-2 matches via AskUserQuestion (e.g., `This sounds like 'failed-launch' or 'crisis-management' — which fits better, or pick another from the taxonomy?`). Accept `unclassified` as a valid skip — better to ship a classified-later story than to force a bad classification. Canonical type slugs (kebab-case): `ambiguity-0-to-1`, `strategic-pivot`, `scope-contraction`, `stakeholder-dissent`, `failed-launch`, `hiring-decision`, `build-vs-buy`, `pricing-monetization`, `activation-retention`, `ethical-edge`, `crisis-management`, `bet-paid-off-or-didnt`.
- `themes`: ask the user. Suggest themes from the body (e.g. if Action mentions pricing tests → suggest `pricing, experimentation`). 3-6 tags is the sweet spot; reject 1-tag and 10-tag.
- `role_lens`: ask. Vocab is fixed to the six options above. Pick the 2-4 that best describe what the story *demonstrates*.
- `companies_used_in`: always start as `[]`. `/interview-prep` appends to this list when it adapts the story for a specific company.
- `last_practised`: always start blank. `/interview-prep` updates it.

### Step 5 — Save

Write `userdata/stories/<slug>.md` with frontmatter + body (full STAR + angles). Confirm to the user: `Saved as userdata/stories/<slug>.md.`

## Mode 3: Edit-existing flow

When the user picks an existing story:

1. Read the file. Print a one-line summary: `Editing 'Payments pricing experiment' (story_type: pricing-monetization; themes: growth, pricing, experimentation, post-PMF; last practised 2026-05-11).` If the story has no `story_type` field, append `— story_type unclassified, want to set it?` and offer to classify before the change menu.
2. Ask: `What do you want to change?` Offer (via AskUserQuestion):
   - Rewrite a STAR section
   - Add / edit an angle
   - Update themes / role_lens / story_type
   - Mark as practised today (set `last_practised: <today>`)
   - Done — save and exit
3. Loop on the change menu until the user picks Done.
4. Save the file in place, preserving frontmatter fields the user didn't touch. NEVER reset `companies_used_in` — that's owned by `/interview-prep`.

## Mode 4: --gap-check

Coverage analysis only — no edit flow. Output is read-only diagnostics.

1. Read all `userdata/stories/*.md` frontmatter. Bucket by `story_type` value (treat missing/blank as `unclassified`).
2. Read `target_titles` from `userdata/profile.md` frontmatter. If any target title contains "Head", "VP", "CPO", or "Director", treat as HoP-track; otherwise Senior-PM-track.
3. Read the story-taxonomy reference. Build a list of the 12 canonical types; mark each as `covered` (≥1 story has that type), `missing`, or `unclassified-only` (only unclassified stories with possibly-matching themes).
4. Rank missing types by relevance to user's track:
   - **HoP-track**: weight hiring-decision, strategic-pivot, ethical-edge, crisis-management, bet-paid-off-or-didnt higher (per story-taxonomy.md level-differentiation section)
   - **Senior-PM-track**: balanced weighting across all 12
5. Output:

```
Story-bank coverage check — <YYYY-MM-DD>

You have <N> stories: <M>/12 story types covered. <K> unclassified.

Covered: ambiguity-0-to-1, pricing-monetization, ...
Missing: hiring-decision, ethical-edge, crisis-management, ...
Unclassified: <list of story titles with no story_type>

For <target-title from profile.md>, the most leverage-gain is:
1. hiring-decision — HoP rounds probe this near-universally; you have no story.
2. strategic-pivot — feature-pivots count, but HoP rounds want whole-team pivots; what you have is too tactical.
3. ethical-edge — rarely probed at Senior PM rounds, but a load-bearing differentiator at HoP rounds.

Next steps:
- /story-builder --new "<suggested title>"
- /story-builder --edit <unclassified-slug>   (to classify what you already have)
```

The "most leverage-gain" prose draws specific justifications from the story-taxonomy reference's level-differentiation section. Each ranked item must cite the SPECIFIC reason from the taxonomy (e.g. "HoP rounds probe near-universally"), not generic "you should have this".

Cap at 3 ranked items. If fewer than 3 types are missing, list however many.

If all 12 are covered: `Story-bank coverage check — <date>. All 12 story types covered (<N> total stories). Look at last_practised dates — anything older than 90 days is worth refreshing before the next round.`

--gap-check writes nothing. It's a read-only diagnostic — the user runs the suggested commands themselves.

## Body shape (canonical)

Every story file follows this exact section ordering. Fixed for `/interview-prep` to parse against.

```markdown
---
title: <string>
story_type: <one of 12 canonical slugs, or unclassified>
themes: [<list>]
role_lens: [<list, subset of fixed vocab>]
companies_used_in: [<list, owned by /interview-prep>]
last_practised: <YYYY-MM-DD or blank>
---

# <Title>

## Situation
<1-2 paragraphs>

## Task
<1 paragraph>

## Action
- <bullet>
- <bullet>
- <bullet>

## Result
- <bullet with metric>
- <bullet>

## Angles for different prompts

**"<Prompt 1>"** <Framing instruction.>

**"<Prompt 2>"** <Framing instruction.>

**"<Prompt 3>"** <Framing instruction.>
```

`story_type` is optional for backwards compatibility — stories from before the taxonomy convention had no field, and re-running /story-builder on them prompts to classify. Blank lines between sections are part of the contract — don't compress.

## Hard rules

- Filename always derived from title slug. User never types a filename.
- If `## What NOT to Frame As` items in profile.md match a drafted bullet, flag it before save: `Your profile says don't frame as <X>. The draft has <quote> — rewrite or accept?`
- Don't invent metrics. If the user can't recall a number, leave the bullet as a qualitative outcome ("noticeable lift in conversion, exact number not recalled").
- Don't write angles that aren't backed by the body. Each angle's *lead* must be traceable to specific lines in Situation / Task / Action / Result.
- Tone of voice from profile.md is authoritative — don't override even if the standard "STAR voice" feels more polished.

## What /story-builder never does

- Never reads or writes `userdata/companies/<Co>/*`. Per-interview adaptations are `/interview-prep`'s job; this skill maintains the universal bank only.
- Never deletes stories. (Manual `rm` is the user's path.)
- Never edits frontmatter fields owned by other skills (`companies_used_in`, `last_practised`).
- Never sets `last_practised` itself except via explicit "mark as practised today" action in edit mode.

## Smoke test against the Maya example

- Picker against `userdata/examples/maya/stories/` shows one entry: `1. Payments pricing experiment [themes: growth, pricing, experimentation, post-PMF] (last practised 2026-05-11)`, then `+ New story` and `Cancel`. Coverage line: `Coverage: 0/12 story types covered. (1 story unclassified — edit to add story_type) Run /story-builder --gap-check for details.` (Maya's existing story pre-dates the story_type convention.)
- `--new "Activation funnel uplift"` flow: computes slug `activation-funnel-uplift`, no collision in Maya's bank, walks STAR + angles using Maya's `## Tone of Voice` (direct, short sentences, UK English, low-pressure CTAs). At Step 4, suggests `story_type: activation-retention` (or `pricing-monetization` if the body leans that way) — user confirms or picks another.
- `--edit payments-pricing-experiment` loads Maya's existing story; one-line summary appends `— story_type unclassified, want to set it?` and offers `pricing-monetization` as the likely match. "Mark as practised today" action updates `last_practised: 2026-05-15`, preserves everything else.
- `--gap-check` against Maya's bank with target_titles including "Head of Product": output reports `1/12 types covered (if user classifies the one story) / 0/12 if not, 1 unclassified`, surfaces missing types ranked by HoP-relevance — hiring-decision, strategic-pivot, ethical-edge as top 3, each with specific justification lifted from story-taxonomy.md.
