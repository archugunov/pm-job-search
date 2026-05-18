---
name: interview-prep
description: This skill should be used when the user asks for "/interview-prep <Company>", "prep for my <Company> interview", "interview prep for <Company>", "get me ready for <Company>", or names an upcoming interview at a specific company and wants a tailored prep doc. Reads userdata/profile.md, all userdata/stories/*.md, and userdata/companies/<Co>/*.md (meta + research brief + any prior debriefs). Writes userdata/companies/<Co>/interview-prep-<YYYY-MM-DD>.md with the 3-5 most relevant stories adapted for this company's signals, founder-vetting questions for late-stage rounds, and a recap of company-specific anchors. Appends to each used story's `companies_used_in` and updates `last_practised` in the universal bank.
---

# /interview-prep — adapt the story bank for a specific interview

Produces a single per-interview prep doc that combines: the company's signals (from `meta.md` + `research-brief.md` + any prior debriefs), the user's positioning, the 3-5 most-relevant stories adapted for THIS interview, founder-vetting questions when the round warrants, and a short "anchors" section the user can scan before the call.

**Voice:** the company-disambiguation prompt, story-pick confirmation, take-home draft-or-not offer, and all written prep content follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — auto-detect stage from `meta.md.status` + last debrief; only ask if genuinely ambiguous.

## Inputs

- `<Company>` argument — required, e.g. `/interview-prep Plaid` or `/interview-prep "Plaid"`. Case-insensitive lookup against `userdata/companies/<Co>/` folder names. If no exact match, fuzzy-suggest: `No 'Plad' folder. Did you mean Plaid? (y/n)`. If multi-role company (subfolder layout), ask which role: `Plaid tracks 2 roles — pick: 1) senior-pm-consumer-credit, 2) lead-pm-risk-platform`.
- `userdata/companies/<Co>/[<slug>/]meta.md` — frontmatter (position, tier, status, location), body.
- `userdata/companies/<Co>/[<slug>/]research-brief.md` — Company snapshot / Why this fits / Open questions.
- `userdata/companies/<Co>/[<slug>/]interview-debrief-*.md` if present (prior rounds) — read the most recent 2; use to avoid repeating stories the user already told and to surface unanswered open questions.
- `userdata/profile.md` — `## Positioning`, `## Proof Points`, `## Moat`, `## Tone of Voice`.
- All `userdata/stories/*.md` — full STAR + angles + frontmatter (including `story_type` if set).
- Story taxonomy: `userdata/references/story-taxonomy.md` if present, else `${CLAUDE_PLUGIN_ROOT}/references/story-taxonomy.md` (userdata override per TONE.md convention). Used for the story-selection tiebreaker — see "Story selection" below.

Optional flags:
- `--stage <stage-name>` — e.g. `--stage cpo-round`, `--stage take-home`, `--stage final-loop`. Shapes the prep doc emphasis (see "Stage shaping" below).
- `--date <YYYY-MM-DD>` — override the filename date (defaults to today).

If `<Company>` folder doesn't exist, tell the user: `No userdata/companies/<Co>/ — run /evaluate-position first to add it.`

## Stage shaping

The doc adapts to the round's character. If `--stage` is omitted, infer from `meta.md.status` + last debrief stage; ask the user if uncertain.

| Stage | Emphasis |
|---|---|
| `recruiter` / `intro` | Why-us narrative + 1-2 high-level stories, no deep STAR. Compensation anchoring. |
| `hiring-manager` / `1st-round` | 3 stories aligned to the position's core remit, plus 5 thoughtful questions. |
| `panel` / `working-session` | 4-5 stories with deep STAR, plus a take-home-style framing for the working portion. |
| `cpo-round` / `final-loop` | 3-5 stories + the three founder-vetting questions (from `/today` heads-up section). Explicit prep for strategy / business-model questions. |
| `take-home` | Skip the story prep entirely. Produce a working-doc skeleton instead with the prompt parsed (see "Take-home variant" below). |

**Founder-as-HM override (applies to `hiring-manager` / `1st-round` only).** At small founder-led companies the HM round IS the founder round — the same questions matter even though the stage label suggests early-pipeline. Detect by reading `meta.md`:

- `team_size` is set AND `< 50`, AND
- `reports_to` matches `/(?i)\b(ceo|founder|co-?founder|cto)\b/` (case-insensitive).

When both conditions hold under `hiring-manager` stage, include the three founder-vetting questions verbatim in the "Questions to ask THEM" section (same wording as the `cpo-round` block) and add a one-line callout at the top of "Anchors": `**Note:** HM here is the founder — treat as a late-stage signal round.` Do NOT bump the story count up — the HM-stage shape (3 stories) still fits; the founder context shapes the questions and the framing, not the depth.

If only one condition holds (e.g. small company but `reports_to` is a VP, or founder-led but >50 ppl) the override does not fire. Skill never asks the user to confirm — the heuristic either fires cleanly from meta.md or doesn't.

## Story selection (3-5 stories)

Algorithm:

1. **Hard match on `themes` and `role_lens`**: from `meta.md.position` and `research-brief.md`, extract topic signals (e.g. consumer credit, pricing, growth, leadership). Rank all stories by overlap with these signals.
2. **De-prioritize used-here stories**: if a story's `companies_used_in` already includes this company, demote it (it was used in a prior round at this company — pick a different one unless the user explicitly invokes `--include-repeats`). Don't exclude entirely; if a story was used in an earlier-stage round and is still the strongest fit, surface it but flag: `Already used at <Company> on <last_practised date> — consider freshening the angle.`
3. **Cover distinct angles**: the final 3-5 stories should collectively cover at least 3 distinct `role_lens` values across the set (don't pick 4 stories that all only show `analytics`).
4. **Story-type tiebreaker (when ties remain after steps 1-3)**: read the story-taxonomy reference's coverage matrix for the round's `--stage`. Prefer stories whose `story_type` is marked as `heavily probed` (X) at this stage over `likely probed` (·) over `unlikely`. Stories with `unclassified` or missing `story_type` get neutral weight — neither penalised nor preferred. Skip this step silently if the taxonomy reference is unreadable or all candidate stories are unclassified.
5. **Show the user the picks before writing the doc**: `Picked these 4 — swap any? <numbered list with one-line justifications>`. If a tiebreaker fired, justifications mention it (e.g. "ambiguity-0-to-1, heavily probed at HM rounds per the story-taxonomy"). Honor swaps.

For each picked story:
- Lift the title and the ONE angle from "Angles for different prompts" that best matches the company's signals (not all angles — be opinionated).
- Write a tailored 4-6 sentence retelling that leads with the chosen angle, then summarises Situation → Action → Result with the company-specific framing woven in (e.g. "If they ask about pricing, this is where I'd land the cost-of-decision-error point — Plaid's underwriting cohort is structurally similar to the Series B thin-file population").

Do NOT copy the full STAR body from the universal bank into the prep doc. The prep doc is the *adaptation*; the universal bank stays canonical.

## Prep doc structure

```markdown
# Interview prep — <Company> / <Position>
**Date:** <YYYY-MM-DD>  **Stage:** <stage>  **Tier:** <P0|P1|P2>

## Anchors
- **Why this company:** <one sentence from research-brief.md "Why this fits", tightened.>
- **Why this role:** <one sentence pointing at the specific surface / scope from meta.md.>
- **Salary anchor:** <from meta.md.comp_band or profile.md.salary_band — what number to aim for, what floor to push back from.>
- **Open questions from research:** <verbatim from research-brief.md's "Open questions" section, lightly pruned to the 2-3 most stage-appropriate.>

**If `research-brief.md` is missing** (the company was added manually rather than via `/evaluate-position`): print a one-line warning to chat (`No research-brief.md at <path> — Anchors derived from meta.md only`), drop the "Why this company" bullet (you don't have a research-grounded summary), and skip the "Open questions from research" bullet (the user will need to derive those manually). The remaining anchors (Why this role from meta.md, Salary anchor) still render. Don't fabricate research content.

## Stories to land
### 1. <Story title>
**Angle:** <prompt-quote from the story's "Angles for different prompts">
<4-6 sentences: the tailored retelling, leading with the angle. Include the
specific company-tie at the end — why this story matters HERE.>

### 2. <Story title>
…

(3-5 entries total)

## Questions to ask THEM
- <Question — drawn from research-brief.md's open questions, sharpened.>
- <Question — drawn from the chosen stage's emphasis.>
- <Question — if late-stage, include one founder-vetting question.>

(Late-stage rounds — final-loop, cpo-round, or any interviewing-status with
last_inbound within 7 days — automatically include the three founder-vetting
questions verbatim:)
- "What does a typical week look like — product vs meetings?"
- "Where has the last HoP spent most political capital internally?"
- "When something underperforms — who's in the debrief room?"

## Anti-patterns to avoid this round
<Lift `## What NOT to Frame As` bullets from profile.md, filtered to ones
likely relevant to this interview's themes. Keep ≤4 bullets.>

## Notes from prior rounds
<If prior debriefs exist, summarise in 2-4 bullets: what stories the user
already used, what open questions surfaced, any interviewer-specific cues
(e.g. "CPO asked twice about activation — keep the pricing story but lean
into activation framing in the loop").>
```

If a section has no content (e.g. no prior debriefs, no anti-patterns hit), omit it entirely. Don't render empty headers.

## Take-home variant

When `--stage take-home` (or the user describes a take-home prompt in chat):

Skip story selection. Produce a working-doc skeleton at `userdata/companies/<Co>/take-home-<date>.md` (note: different filename pattern — take-home is a working doc, not a prep doc). Structure:

```markdown
# Take-home — <Company> / <Position>
**Date:** <date>  **Prompt:** <one-line summary of what they asked for>

## Brief recap
<2-3 sentence summary of the prompt, what they're trying to learn.>

## Frame
<3-4 sentences on the *approach* — what problem are you actually solving,
what's out of scope, what's the rubric you'll be graded on.>

## Outline
- <Section heading 1>
- <Section heading 2>
- ...

## Open questions for the user before drafting
- <Question — what's the implicit constraint?>
- <Question — what's the time budget?>
```

Then offer: `Want me to draft the full doc, or are you taking it from here?` Take-home drafting is a separate workflow — the prep skill seeds the outline.

## Universal bank updates (the only writes outside `companies/<Co>/`)

After the prep doc is written, for each story used in "Stories to land":
1. Append `<Company>` to that story's `companies_used_in` list (if not already present).
2. Set `last_practised: <YYYY-MM-DD>` (overwrite previous value — this is the most recent use).

These are the ONLY edits /interview-prep makes outside the company folder. Preserve all other frontmatter and body content of the story file.

## What /interview-prep never does

- Never writes to `userdata/profile.md` or `userdata/strategy.md`.
- Never edits a story's STAR body or angles — only the two frontmatter fields above.
- Never invents company facts. If a claim isn't in `meta.md` / `research-brief.md` / debriefs, don't put it in the prep doc.
- Never auto-invokes reviewer agents — the user can do that separately on the prep doc if they want a CPO / interview-coach lens.
- Never deletes prior prep docs at the same company. Each round gets its own dated file.

## Smoke test against the Maya example

### Founder-as-HM override

To exercise the override, add a synthetic small founder-led company to Maya's install (e.g. a Sprive-style 35-ppl Series A with `reports_to: CEO (Jinesh Vohra)` and `team_size: 35`), then run `/interview-prep <Co> --stage hiring-manager`. The output must include the three founder-vetting questions and the "HM here is the founder" note. Run the same prompt without those frontmatter fields and the override must NOT fire — the doc renders as a standard HM-stage prep.

### Standard run

Run `/interview-prep Plaid --stage cpo-round` against `userdata/examples/maya/`:

- Reads `companies/Plaid/meta.md` (status interviewing, position Senior PM Consumer Credit, tier P0, last_inbound 2026-05-13) and `companies/Plaid/research-brief.md`.
- No prior debriefs to read.
- Selects stories: only one exists in Maya's bank (`payments-pricing-experiment`). Skill should handle "<3 stories in bank" gracefully — surface the one available + a note: `Only 1 story in bank — pick others via /story-builder or proceed with one.` User picks: proceed.
- Writes `userdata/examples/maya/companies/Plaid/interview-prep-2026-05-15.md` with the one story adapted, late-stage founder-vetting questions included (cpo-round triggers them), and anchors lifted from research-brief.
- Updates `userdata/examples/maya/stories/payments-pricing-experiment.md`: appends `Plaid` to `companies_used_in` (currently `[Plaid]` already — no-op), sets `last_practised: 2026-05-15`.
