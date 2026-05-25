---
name: setup
description: This skill should be used when the user asks for "start", "/setup", "set up the plugin", "first-time setup", "install pm-job-search", "configure my profile", "create my profile", or wants to onboard onto pm-job-search for the first time (or re-run onboarding to update a field). Conducts a 12-question conversational install that writes userdata/profile.md, a placeholder userdata/strategy.md, an empty userdata/journal.md, three .gitkeep files, and a CLAUDE.md at the workspace root resolved from the plugin template.
---

# /setup — first-run install and re-configure

Onboard the user onto pm-job-search by filling in `userdata/profile.md` and scaffolding the rest of the userdata tree. Idempotent — safe to re-run.

**Voice:** every prompt and message in this skill follows the plugin's tone-of-voice + low-effort-first guidelines in `${CLAUDE_PLUGIN_ROOT}/TONE.md`. The exact wording for each question below is locked-in — use it verbatim, not paraphrased.

**Opening line** (after mode detection, before Q1, fresh install only):

> "OK, let's get you set up. Twelve quick questions — none of it locked in, you can rerun anytime. Ready?"

Wait for a one-word confirmation, then start Q1.

## Mode detection

Run this BEFORE asking the first question:

1. If `userdata/profile.md` exists → enter **re-run mode**: read the file, ask "keep current / update / skip" per field, never wipe existing answers.
2. If `userdata/profile.md` does NOT exist → enter **fresh-install mode**: ask all 12 questions in order.
3. `--refresh` flag → re-run mode, but only re-resolve the workspace-root `CLAUDE.md` from the template using the current `profile.md` content. Skip all questions. Useful after manual edits to profile.md.

Also detect CV presence (only relevant in fresh-install mode). This shapes how Q6 (Positioning) is offered — see Q6 below for the full flow:

- `userdata/cv.md`, `userdata/cv.txt`, or `userdata/cv.pdf` exists → Q6 goes straight to Mode B (CV draft) without prompting.
- `userdata/cv.docx` or any other non-md/txt/pdf file → print one line: `Found userdata/cv.<ext>. Readable formats are .md, .txt, or .pdf — convert your CV first if you want me to draft from it.` Then Q6 offers all three options (CV-drop, skip, paste).
- No cv.* file → Q6 offers all three options with CV-drop as the recommended default.

## Templates

Read these from the plugin install dir (use `${CLAUDE_PLUGIN_ROOT}` if available):

- `${CLAUDE_PLUGIN_ROOT}/templates/profile.template.md` — source for `userdata/profile.md`.
- `${CLAUDE_PLUGIN_ROOT}/templates/strategy.template.md` — source for `userdata/strategy.md`.
- `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.template.md` — source for workspace-root `CLAUDE.md`.

Do not edit these template files. Always treat them as read-only inputs.

## The 12 questions

Ask one at a time. Use AskUserQuestion only when a question has a clear set of options (Q5, Q6); otherwise plain conversational ask. Skipping is allowed on Q4 (LinkedIn), Q9 (salary band), Q10 (hard filters), Q11 (companies of interest) — see the "skipped placeholders" rule under "File writes" for the exact YAML form to write.

Each question below shows the EXACT user-facing prompt in quotes. Use the wording verbatim — don't paraphrase. The voice is locked per `TONE.md`.

1. **Name** (`{{NAME}}`) — required.
   > "What's your name?"

2. **City** (`{{CITY}}`) + auto-detect timezone — required.
   > "Where are you based? City + country works (e.g. London, UK)."

   After the user answers, auto-detect IANA timezone via `realpath /etc/localtime | sed 's|.*/zoneinfo/||'` (returns e.g. `Europe/London`). Do NOT use `date +%Z` — that returns abbreviations like `BST` / `CEST`, not IANA strings. Fill `{{TIMEZONE}}` automatically and confirm in one line:
   > "I'm seeing your timezone as `<detected>` — that right? Override if not."

3. **Email** (`{{EMAIL}}`) — required.
   > "What's the best email for you?"

4. **LinkedIn URL** (`{{LINKEDIN_URL}}`) — skippable.
   > "LinkedIn URL? Or skip."

5. **Geography** (`{{GEOGRAPHY_MODE}}` + `{{GEOGRAPHY_DETAIL}}`) — single-select via AskUserQuestion. Ask:
   > "Where are you looking?"

   Options (in this order): `On-site in <city-from-Q2>` / `Remote` / `Both` / `Other (free text)`. The first option dynamically uses the city captured in Q2. If the user picks "Other", capture free-text into `mode_detail` and set `mode: other`.

6. **Positioning** (`{{POSITIONING}}` + `{{PROOF_POINTS}}` + `{{MOAT}}`) — three paths. **The default order matters**: present them in the order below, with CV as the recommended first option. Writing positioning by hand is 5-10 minutes of real reflection — don't force it during onboarding when the user has a faster path.

   Auto-detect first: if `userdata/cv.md`, `userdata/cv.txt`, or `userdata/cv.pdf` already exists, go straight to **Mode B (CV draft)** below and skip the prompt.

   If no CV file exists, ask via AskUserQuestion. Use this exact opener and three options:

   > "Positioning next — who you are and what you're best at. Three ways to handle this:"

   - **A. Drop your CV (recommended)** — first, create the following directories and files if not already present: `userdata/`, `userdata/companies/.gitkeep`, `userdata/stories/.gitkeep`, `userdata/outputs/.gitkeep`. Then print: *"I've created `userdata/` for you — drop your CV there as `cv.md`, `cv.txt`, or `cv.pdf`. Say 'ready' when it's in."* When the user says ready, re-detect the CV file. If present → Mode B. If still absent → re-offer the three options.
   - **B. Write it now** → **Mode A** (paste 1-3 sentences and walk the conversational draft).
   - **C. Skip for now** — print: *"Fill in later — `/pm-job-search:setup --refresh` picks up where you leave it."* Write `userdata/profile.md` with the three positioning sections empty under a `<!-- TODO: fill in via /pm-job-search:setup --refresh, or paste your CV at userdata/cv.md and re-run --refresh -->` comment. Onboarding finishes fast.

   ### Mode A (paste-now)

   Ask the user to paste 1-3 sentences of self-positioning. Draft a 2-paragraph `## Positioning` from it; ask for 3-5 numbered wins to draft `## Proof Points`; ask for one sentence answering "what's the rare thing you bring?" to draft `## Moat`. Apply the **Drafting tone rules** below.

   ### Mode B (CV draft)

   Read the CV file. Draft a positioning paragraph (≤4 sentences) + 5-7 proof points (each ≤2 sentences) + a one-sentence moat candidate. Show to user. Ask them to edit / accept / discard. Never save without explicit user review.

   ### Drafting tone rules (apply to BOTH Mode A and Mode B drafts)

   The goal is positioning that reads as senior, specific, and unbluffed. Senior PMs don't recognise themselves in fluffy drafts and bin them.

   **Voice — four core principles:**

   - **Casual but professional.** No stiff openers, no corporate boilerplate.
   - **Direct and short.** One idea per sentence. No padding. If a sentence runs longer than ~20 words, cut it.
   - **Honest about gaps, then reframe — never oversell.** If the CV reveals a stretch claim, surface the nuance rather than paper over it.
   - **Specific over general.** Concrete nouns beat abstract ones.

   **The "Not X — Y" reframing pattern.** Sharpen positioning by explicitly naming the lazy framing the writer is NOT making, then anchoring the specific one. Shape: `Not "<generic claim>" — <specific past-tense fact>.` Use this pattern at least once in the drafted `## Positioning` if the CV implies a stretch claim the writer would want to disown.

   **Proof point format.** Each bullet follows the shape: `**<Anchor>:** <specific work> → <specific outcome>. (<role>)`. The anchor is usually the company or product. The work is past-tense and concrete. The outcome carries the number when one exists. The role is in parentheses at the end. If a metric isn't in the CV, the bullet stays qualitative — don't invent the figure to make it land.

   **Phrases to BAN outright:**

   - **Superlatives:** "rare", "deep", "elite", "world-class", "exceptional", "uniquely positioned", "best-in-class"
   - **Abstract adjective stacks:** any 3-noun rhythm of capability claims (pick ONE, anchored to a specific outcome instead)
   - **Clichés:** "move the needle", "drive impact", "compound", "10x", "north star", "first principles", "the metrics that actually [verb]"
   - **LinkedIn closers:** "equally at home in X, Y, Z", "passionate about", "obsessed with", "thrives in ambiguity"
   - **Present-tense capability framing:** "lets me", "allows me to", "able to" — replace with the past-tense outcome that demonstrates it
   - **Filler phrases:** "I wanted to reach out", "As you may know", "I am writing to express", "I hope this email finds you well"
   - **Formal/corporate language** generally

   **Past tense for outcomes.** "Shipped X, lifted Y by Z%" beats "drives growth through experimentation".

   **Don't invent numbers.** If a metric isn't in the CV, don't add one. Don't round up. Don't aggregate without checking the math.

   **Don't overclaim involvement.** If the CV describes the writer's role on a project narrowly ("defined success criteria with a team", "supported the migration"), don't promote it to leadership framing ("led", "shipped end-to-end"). Use the writer's own scoping verbs.

   When showing the draft to the user, append: *"Edit anything that doesn't sound like you — drafts are starting points, not finished copy."* Always let the user rewrite before save.
7. **Target titles** (`{{TARGET_TITLES}}`) — comma-separated list from the user. Ask:
   > "What roles are you targeting? Typical senior-PM examples: Director of Product, Principal PM, Group PM, Staff PM. List as many as you'd take, comma-separated."

   Substitute as a YAML inline list: `[Director of Product, Principal PM, Group PM]` (keeps the template's trailing inline comment intact; the user can reformat to block form later if they prefer).

8. **Target industries** (`{{TARGET_INDUSTRIES}}`) — comma-separated. Ask:
   > "What industries are you looking at? E.g. healthcare, climate tech, education, enterprise SaaS. Comma-separated."

   Substitute as YAML inline list (same form as Q7).

9. **Salary band** (`{{SALARY_BAND}}`) — single open string. Skippable. Ask:
   > "What salary band are you aiming for? Whatever shape works — '£90-110K' or '$190-230K base + equity', or skip if you'd rather not anchor a number yet."

   No validation — accept whatever currency / phrasing the user gives.

10. **Hard filters** (`{{HARD_FILTERS}}`) — ONE question, skippable. Ask:

    > "Any red flags? Roles you'd skip immediately regardless of other fit. E.g. 'no companies under 50 people', 'no GM or business-owner roles', 'no five-day in-office', 'no relocation'. List a few, or skip."

    Parse the user's response into a YAML inline list of quoted strings: `["no companies under 50 people", "no five-day in-office"]`. If skipped or empty, write `[]`. (Inline form keeps the trailing template comment intact, same reasoning as Q7.)

11. **Companies of interest** — skippable. Ask:
    > "Any companies you have in mind already? List a few, or skip."

    Persist the answer to `userdata/profile.md` under a new section heading:

    ```markdown
    ## Companies of interest

    - <Co 1>
    - <Co 2>
    ```

    If the user skips, write the heading with an empty list (so `/job-search` can distinguish "asked, none given" from "never asked"):

    ```markdown
    ## Companies of interest

    ```

12. **Target offer date** — skippable. Ask:
    > "When do you want the offer signed by? Concrete date — even a best guess. Vague dates make `/today`'s countdown noisy."

    Parse as `YYYY-MM-DD`. If skipped, set `target_offer_date: null` in strategy.md and skip the cadence derivation below — strategy.md will only have the auto-headline-goal populated; `/today` degrades gracefully (no countdown, no progress section).

After Q12 (only if target date was set), silently derive cadence targets based on weeks-to-target. Compute `W = (target_offer_date − today) / 7`, then:

| W | weekly_targets.applications | weekly_targets.warm_outreach | pipeline_targets.active_interview_threads | pipeline_targets.p0_pipeline_size |
|---|---|---|---|---|
| W < 8 (under 2 mo) | 12 | 10 | 5 | 8 |
| W = 8-16 (2-4 mo) | 8 | 8 | 4 | 6 |
| W ≥ 16 (4+ mo) | 5 | 5 | 3 | 5 |

Rationale (don't surface to user unless asked): shorter timeline → higher concurrent activity needed to hit ~2 offers in hand by deadline, assuming ~30% offer rate on active interview threads and ~15% interview rate on applications.

Also silently auto-compose `## Headline goal` for strategy.md from profile.md frontmatter. Format:

> "Sign a `<target_titles joined by ' / '>` role at a `<target_industries joined by ', '>` company by `<target_offer_date>`. `<geography phrasing — 'Fully remote', 'London hybrid', etc.>`. Base `<salary_band>`."

Skip clauses where the source field is unset (e.g. if salary skipped, drop the base clause).

Leave `## Anti-goals` empty and `checkpoints: []` — those need deeper reflection and belong to the user's later editing or to a `career-coach` conversation.

After Q12: proceed straight to file writes. Do NOT prompt the user about the tier rubric.

The senior-PM-default `tier_weights` + `tier_thresholds` get written into `profile.md` from the template automatically. Tier rubric terms (P0/P1/P2, role_fit, etc.) are too technical to introduce here without context — the user encounters them organically the first time `/evaluate-position` runs and shows a scoring breakdown. That's the right teach-moment.

If the user wants to tune the rubric, they edit `profile.md` directly. The re-run mode of `/setup` (where field-by-field keep/update/skip is offered) does NOT include the tier rubric either — same reason.

## Re-run mode question loop

When `userdata/profile.md` exists, iterate fields in the same order (Q1-Q12 + tier rubric). For each:

1. Show the current value (one line).
2. Ask: `keep / update / skip` (skip means "leave as-is for now, ask again next /setup").
3. If `update`: prompt for the new value using the same conversational pattern as fresh-install.

Never overwrite a non-empty field with an empty answer in re-run mode. If the user updates a field but provides empty input, ask once more; if still empty, treat as `skip` and leave the current value.

The user's freeform body sections (`## Tone of Voice`, `## What NOT to Frame As`, and any `##` section they added below the documented ones) are NEVER touched in re-run mode — they belong to the user.

## File writes

After all questions are answered, do these writes in order:

### 1. `userdata/profile.md`

Read the profile template, substitute every `{{PLACEHOLDER}}`, write to `userdata/profile.md`. Preserve all HTML comments and free-form prompt blocks (the `<!-- … -->` sections after each `##` header) verbatim. Substitute placeholders only.

For skipped placeholders: write an empty YAML value, never the literal `{{NAME}}` string. Specifically:
- `{{LINKEDIN_URL}}` skipped → `linkedin_url:` (empty value parses as null).
- `{{SALARY_BAND}}` skipped → `salary_band: ""` (explicit empty string — keeps the quoted-string shape the template intends).
- `{{HARD_FILTERS}}` skipped → `hard_filters: []`.
- `{{TARGET_TITLES}}` cannot be skipped (required).
- `{{GEOGRAPHY_DETAIL}}` skipped → `mode_detail:` (empty).

Do NOT write `# unset` comments — they look like noise in the final file. An empty value is self-explanatory.

### 2. `userdata/strategy.md` (only if file does not already exist)

Read the strategy template. Populate:
- `target_offer_date`: from Q12. If Q12 was skipped, leave as `null`.
- `weekly_targets.*` + `pipeline_targets.*`: from the cadence-derivation table above. If Q12 was skipped, leave all as `null` (`/today` skips them gracefully).
- `checkpoints: []` (empty list — user adds later via `career-coach` or by hand).
- `## Headline goal`: the auto-composed paragraph (from profile.md fields + target date). If Q12 was skipped, omit the date clause and drop the countdown wording.
- `## Anti-goals`: leave the section empty (the template's HTML comment prompts the user to fill in later).

Write to `userdata/strategy.md`.

If `userdata/strategy.md` already exists, skip this write. /setup never overwrites a user's existing strategy file.

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
2. For each of `Positioning`, `Proof Points`, `Moat` (in that order):
   - Find the `## <Section>` heading line in profile.md.
   - Capture everything between that line and the next `## ` line (or EOF).
   - Strip any HTML comment blocks (`<!-- … -->`, possibly multi-line) from the captured content — those are authoring helpers for profile.md, not content meant for CLAUDE.md.
   - Trim leading and trailing blank lines from what's left.
3. Build the replacement block. The `{{INCLUDE}}` marker sits BELOW a `## About me` heading in the template, so each section must be DEMOTED from `##` to `###` to nest correctly. For each captured section, emit:
   - `### <Section>` (e.g. `### Positioning`)
   - blank line
   - the captured body
   - blank line
4. Replace the entire `{{INCLUDE: …}}` line (including its surrounding blank lines if any) with the concatenated block. The result is a clean `## About me` followed by three `###` subsections.

Skip a section if its content (after comment-stripping and trimming) is empty — better to omit `### Moat` entirely than render an empty header.

Write the result to `CLAUDE.md` at the workspace root (one level above `userdata/`). Overwrite any existing `CLAUDE.md` at the root only if it begins with the same `<!--` template-header comment as the template (signature of a previously generated file). If it doesn't, ask the user before overwriting: `CLAUDE.md exists at workspace root and was not generated by pm-job-search. Overwrite (y/N)?`

## Closing offers

First, print a brief summary of what was written — one line per file. If Q12 set a target date, include the derived cadence summary so the user can spot-check the numbers. Example with target date set:

> "You're set up. Wrote:
> - `userdata/profile.md` — identity, target role, salary, hard filters
> - `userdata/strategy.md` — headline goal + derived weekly targets (8 apps/wk, 8 outreach/wk, 4 active interview threads floor) based on your 18-week timeline. Edit these in `userdata/strategy.md` if they feel off — or ask `pm-job-search:career-coach` to help you set anti-goals and checkpoints.
> - `userdata/journal.md` — empty (append daily notes here)
> - `CLAUDE.md` — workspace root, loads your profile into every Claude Code session"

If Q12 was skipped, omit the cadence summary line — just say `userdata/strategy.md — headline goal drafted; targets unset (skipped target date)`.

Then offer ONE follow-up (only if Q6 produced a draft via Mode A or Mode B):

> "Want to sharpen your positioning before we wrap? I can pull in the `pm-job-search:career-coach` agent — quick 5-min back-and-forth, it'll suggest a tighter version. Or skip and edit `profile.md` whenever."

If yes, invoke the `career-coach` agent. If no or Q6 was skipped, continue to the automation offer below.

**Automation offer (split per TONE.md Rule A — one ask per message):**

Step 1 — ask:
> "Want `/pm-job-search:today` to run automatically every day? (y / n)"

Use `AskUserQuestion` with two options: **Yes** / **No, I'll run it manually**.

If No → skip to closing nudge.

Step 2 (only if Yes) — ask:
> "What time? (e.g. 9am)"

Free-text answer. Parse to HH:MM.

Step 3 (only if Yes) — write the schedule via `/schedule` automatically and reply:
> "Done — scheduled daily at <HH:MM> via /schedule. If you'd rather not keep a Claude Code session open, ask me to set up a launchd plist (macOS) or cron entry (Linux) instead."

**Closing nudge:**

After all setup files are written (and after the automation step completes or is skipped), read `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md` and compose a single one-line context-aware next-step nudge based on the user's current state. For a fresh setup with no companies yet, the nudge should be:

> "Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first."

Do not list all three steps as numbered bullets; the recommended-flow reference handles ordering.

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
