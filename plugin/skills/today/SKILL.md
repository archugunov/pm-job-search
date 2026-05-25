---
name: today
description: This skill should be used when the user asks for "/today", "my daily brief", "today's brief", "where am I in my job search", "what should I work on today", "pipeline state", or wants a sorted view of every active company plus today's actions. Two-phase: input phase captures fresh facts since the last journal entry (via wired Calendar/Gmail/Granola integrations + an open catch-all prompt), then writes them to userdata/journal.md and relevant userdata/companies/*/meta.md; output phase reads userdata/strategy.md + all meta.md + the current ISO week of journal.md, writes a 3-section daily brief (top actions, heads-up, pipeline) to userdata/outputs/daily-brief-<date>.md, regenerates the GENERATED block of userdata/outputs/applications.md, and on the first run of each ISO week (when prior-week journal entries exist) offers a hand-off to pm-job-search:career-coach for a weekly reflection.
---

# /today — daily brief

Produce a short (~half a screen) snapshot that combines: where the user is against their stated strategy, what to actually do next, and a sorted view of the pipeline. Save the brief, regenerate the applications.md index, then print the brief to chat.

**Voice:** all chat output and drafted content (the daily brief, summary lines, warnings) follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`.

## Input phase (runs before brief generation)

Capture fresh facts since the last journal entry. Each confirmed fact gets appended to `userdata/journal.md` and — when it has structured implications — pushed to the relevant `userdata/companies/<Co>/meta.md`. Then the output phase runs against the just-written state.

This phase always runs (even with no integrations wired) but degrades gracefully — inference and confirms are skipped when there is nothing to scan, and the catch-all prompt becomes the only input surface.

**First-run detection (TONE Rule C — don't ask about prior state on first run):**

Before prompting for updates, check `userdata/journal.md`. If the file does not exist, is empty, or contains no entries, skip the entire input phase and go straight to output generation. Do not ask "anything that moved since last time?" — there is no last time.

### Step 1 — determine the input window

Read `userdata/journal.md`. Find the most recent dated heading (`## YYYY-MM-DD`).

- Gap < 24h → window = 24h. Print nothing; this is the normal daily case.
- Gap 1–6 days → window = the actual gap. Print one line: `Last entry was N days ago — pulling the full window.`
- Gap ≥ 7 days → window = the actual gap. Print: `You've been away N days — heavier sweep ahead, may take a moment.`
- `journal.md` absent or empty → window = 24h. Treat as a fresh install. Do not print anything special.

### Step 2 — inference pass (when integrations wired)

Read `userdata/integrations.md` to find which MCPs are wired. For each wired integration, scan the window. Same auth-error rule as the existing Integration-data section: surface one line per failed integration at the top of the input phase, do not silently skip, continue with the others.

- **Gmail (when wired).** Reuse the existing gmail filter (saved in integrations.md). Fetch subject + from + date metadata over the window (not the 7d hardcoded in the output-phase fetch). For each result, classify into one of: `recruiter-reply`, `rejection`, `scheduling`, `offer`, `unclear`. Match against `userdata/companies/*/meta.md` + `*/*/meta.md` by alias + domain + recruiter-name-in-journal as the output-phase fetch already does.
- **Calendar (when wired).** Fetch events in the window. Filter by the same keywords as the output-phase fetch (`interview`, `recruiter`, `screen`, `round`, `intro call`, `final loop`, `panel`, `take-home review`) plus matched company names. For each kept event, classify into: `new-event`, `rescheduled`, `cancelled` (rescheduled / cancelled requires comparing against any prior `next_event` value in the matched company's meta.md).
- **Granola (when wired).** Reuse the auto-Granola lookup pattern documented in `/interview-analysis`: call the wired Granola list_meetings tool over the window, match meeting titles against company names + interview/recruiter keywords. For each match, capture title + date.

Dedup across integrations: if the same fact surfaces via two sources (e.g. a calendar event + a gmail confirmation), present it ONCE in the confirms list with both sources noted (`source: calendar + gmail`).

### Step 3 — targeted confirms

Render inferred deltas as a numbered list, grouped by source. Skip this step entirely if step 2 produced no items. Example output shape:

> Since your last entry (2026-05-15), I see:
>
> From calendar:
> 1. Plaid — Round 2 panel scheduled Fri 2026-05-22 14:00
> 2. Klarna — Recruiter call moved from Wed to Thu
>
> From gmail:
> 3. Lendable — Reply from Sarah at Lendable (likely rejection — want me to read it?)
> 4. Stripe — New inbound from a recruiter named James (no company match yet)
>
> From granola:
> 5. Klarna recruiter call transcript captured Mon 2026-05-15
>
> Confirm 1-5 ('all', '1 3 5', or describe corrections). Anything I should edit or skip?

User response handling:
- `all` / `yes` → confirm every inferred item as-is.
- Numbered subset (`1 3 5`) → confirm only those.
- `1 wrong — that was R3 not R2` → confirm with edit applied before write.
- `skip 3` → drop item 3 from this run.
- `4 is for company X` → re-route the unmatched inbound to company X before write.

If the user response is ambiguous, ask one clarifying question rather than guessing. Never write an item the user has not explicitly confirmed.

### Step 4 — open catch-all

After targeted confirms (or in place of them when step 2 produced nothing):

**Input prompt (subsequent runs only):**

Use `AskUserQuestion` with two options:

Question: "Want to log updates since your last brief? Mock interviews, prep work, energy notes, new leads, anything structural."
Options: **Share updates** / **Skip**

If **Share updates** → open a free-text follow-up: "Go ahead — what's new?"
If **Skip** → proceed to output phase silently.

Do not rely on enter-to-skip. Do not chain a second question after this one (TONE Rule A — one ask per message).

User responds in free text. Parse for company tags: explicit `[Plaid]`, `Plaid:`, or first-token match against the company list. Lines without a company tag are logged to `journal.md` only (no meta.md write, no guessing). Lines WITH a company tag are also logged to `journal.md` only — catch-all input is free text and never writes to meta.md, even when the tag matches a known company. Only integration-sourced facts that pass through the Step 3 confirm flow may update meta.md.

### Step 5 — write phase

Commit the confirmed facts. See "Write contracts" section below for the exact journal.md and meta.md formats.

Writes are idempotent per `/today` run: if the user runs `/today` twice the same day with no new facts (step 2 finds nothing new, step 4 skipped), no journal write occurs and no `## YYYY-MM-DD` heading is added or modified.

**Dashboard nudge cross-reference.** When confirming an in-chat status change (e.g. user says "mark Plaid to apply"), check whether the "In-chat update nudge — fire once per session" rule in `${CLAUDE_PLUGIN_ROOT}/skills/dashboard/SKILL.md` should fire. If this is the first status-change-in-chat of the current Claude Code conversation, append the tip line per that rule. Track the once-per-session flag transiently in conversation context, not on disk.

After step 5 completes, proceed to the existing "Output: the daily brief" section.

## Write contracts (used by the input phase)

### journal.md format

The existing free-form append convention is preserved. The input phase adds two conventions on top:

- Bullets begin with `[<Company>]` when the fact is company-scoped. Bullets without a tag are global / personal (mock interviews, energy notes, structural reflections).
- Bullets end with `(source: <integration|user>[, confirmed])`. The `, confirmed` trailer applies only to integration-sourced facts that the user explicitly approved in Step 3 — never to user-sourced bullets from the catch-all (those are inherently the user's own input). So: `(source: calendar, confirmed)` is valid, `(source: user, confirmed)` is not — user-sourced bullets always read `(source: user)`.
- Provenance lets future skills filter by trust level.

One bullet per fact. Multi-fact compound entries get split into separate bullets.

Example block written by a single input phase:

```
## 2026-05-18
- [Plaid] Round 2 panel scheduled Fri 2026-05-22 14:00. (source: calendar, confirmed)
- [Lendable] Reply from Sarah, declined — seniority mismatch cited. (source: gmail, confirmed)
- Mock with Sasha on pricing story — felt rusty, need to re-practise. (source: user)
```

Rules:
- If today's `## YYYY-MM-DD` heading already exists in journal.md (e.g. a prior /today run today added entries), append the new bullets beneath the existing heading rather than creating a duplicate heading.
- If today's heading does not exist, create it at the end of the file (with a blank line before it).
- Never edit or remove bullets that were already in journal.md — the file is append-only from /today's perspective.

### meta.md updates

Per-company meta.md uses (or gains, if not already present) three fields written by the input phase. Existing fields owned by other skills — `company`, `position`, `tier`, `link`, `date_applied`, `date_added`, `monitoring`, `last_inbound`, `rejection_stage`, `date_rejected`, `date_not_interested` — are untouched.

- **`next_event:`** — string, free-form. Examples: `"R2 panel Fri 2026-05-22 14:00"`, `"Recruiter call Thu 2026-05-21 10:00"`. Cleared (set to empty string or removed) when the input phase confirms the event passed without follow-up OR when it was cancelled. Updated in-place when an event is rescheduled.
- **`status:`** — enum, one of: `new`, `to_apply`, `applied`, `interviewing`, `offer`, `rejected`, `not_interested`. The input phase only transitions OUT of an active state when a fact unambiguously implies it: a confirmed rejection → `rejected`, a confirmed offer → `offer`. Confirmed scheduling events do NOT auto-promote `applied` → `interviewing` (other skills own that transition based on richer signal).
- **`## History` block** — chronological list of state transitions, one line per change. Format: `2026-05-18: status → rejected (seniority mismatch — Sarah at Lendable, gmail confirmed)`. Append to the end of the block; create the `## History` heading at the bottom of meta.md if it doesn't exist.

Rules:
- When an event is rescheduled, update `next_event` AND append a History line: `2026-05-18: next_event → "R2 panel Fri 2026-05-22 14:00" (rescheduled from Wed, calendar confirmed)`.
- When an event passes without action (e.g. yesterday's recruiter call happened), clear `next_event` and append: `2026-05-18: next_event cleared (passed, no follow-up captured yet)`.
- When the input phase has no implication for a given company in meta.md, do not touch that file at all.
- Frontmatter changes are YAML-safe: preserve other fields, preserve quoting style, preserve trailing comments.

## Inputs

Read in this order. Skip gracefully if a file is missing — the brief degrades section-by-section, never errors out wholesale.

1. `userdata/strategy.md` — frontmatter (`weekly_targets`, `pipeline_targets`, `checkpoints`). Used by Top-3-actions trigger rules and the warm-outreach summary line in applications.md. The `## Headline goal` paragraph and `target_offer_date` are not read by the brief itself.
2. All company `meta.md` files. Use BOTH globs (companies are either flat or in role-slug subfolders):
   - `userdata/companies/*/meta.md`
   - `userdata/companies/*/*/meta.md`
3. `userdata/journal.md` — last 7 days of entries (entries are dated `## YYYY-MM-DD` headings; take everything with a date within the last 7 days).
4. `userdata/outputs/applications.md` if it exists (needed for the partition rewrite — see "applications.md regeneration" below).
5. `userdata/integrations.md` if it exists — parse the `## calendar` and `## gmail` sections for wired-status + tool prefix. See "Integration data" below. Skip silently if the file is absent — the brief still produces a complete output from markdown alone.

Do not read `userdata/profile.md`. /today does not need profile content; trust strategy.md and the per-company meta.

## Integration data (output-phase fold-in)

If `userdata/integrations.md` exists, this skill optionally folds in live data from Calendar and Gmail MCPs to make the brief richer. Both are fully optional — when absent or failing, /today degrades gracefully to the markdown-only flow.

### Calendar fetch (when calendar wired)

When `userdata/integrations.md ## calendar` shows status `wired` with a tool prefix:

1. Call the wired calendar tool to list events in the next 14 days. Match against all `userdata/companies/*/meta.md` (and `*/*/meta.md`) — extract company names + alias each title field — and against keywords: `interview`, `recruiter`, `screen`, `round`, `intro call`, `final loop`, `panel`, `take-home review`. Keep matches; discard the rest.
2. For each kept event, capture: `{Day D Mon, HH:MM}`, matched company (or `unmatched` for keyword-only hits), event type (`interview`, `recruiter`, etc.).

If the calendar tool returns an auth or quota error: do not silently skip. Surface one line at the top of the heads-up section: `Calendar fetch failed (<error type>) — heads-up missing event data this run. Re-auth via your calendar MCP.`

### Gmail fetch (when gmail wired)

When `userdata/integrations.md ## gmail` shows status `wired` with a tool prefix + filter string:

1. Call the wired gmail tool with the saved filter (typically: recruiter / talent / company-domain matches) over the last 7 days.
2. For each result, fetch the subject + from + date metadata (no body).
3. Match each email to a company in `userdata/companies/*/meta.md` (alias-checking the company name, domain in the from-address, and any explicit recruiter name from journal.md). Each email is either `matched-to-<Company>` or `new-inbound` (no company match).

Same auth-error rule as Calendar: surface a single line at the top of heads-up, don't silently skip.

### Granola fetch (when granola wired)

Granola data is consumed by the INPUT phase only — see `## Input phase` Step 2. The output phase (this section's brief enrichments) does not surface anything from Granola. If `userdata/integrations.md ## granola` shows status `wired`, the input phase will list interview / recruiter meeting transcripts captured in the window; the output phase ignores Granola entirely.

### What never happens

- /today never writes to integrations.md.
- /today never persists raw Calendar/Gmail responses verbatim. Only the user-confirmed facts that pass through the input phase land on disk (see `## Input phase` for the contract); the saved brief includes the rendered output, not raw API responses.
- /today never auto-updates `last_inbound` on company meta.md based on Gmail matches alone. The input phase may update `next_event`, `status`, and the `## History` block when the user confirms an inferred fact, but `last_inbound` is still maintained by other skills.

## Output: the daily brief

Three sections, in this order, ~half a screen total. Never longer. Skip a whole section (do not pad with "N/A") when the underlying data is unavailable. The brief intentionally does NOT restate the strategy headline goal or a weekly-progress meter — both were redundant with the pipeline-state table and the action triggers below, which already pull from strategy and journal data.

Section order: **Top 3 actions → Heads-up → Pipeline state.**

### 1. `## Top 3 actions today`

At most three bullets. Each bullet is concrete and anchored to a company name or a strategy element. Surface bullets by running the trigger rules below, in this priority order, and stopping at three:

1. **Imminent calendar event (when calendar wired)** — any matched event within the next 48 hours → `<Day HH:MM> — <Company> <event-type>: prep with /interview-prep <Company>` (cap at two; most-soonest first).
2. **Checkpoint due in ≤14 days** → `Review checkpoint due <date>: <condition> → <action>` (one bullet per upcoming checkpoint; cap at one if multiple).
3. **Recruiter email needing reply (when gmail wired)** — any matched email from the Gmail fetch where the from-address is recruiter/talent AND the company is in `status: interviewing` or `status: applied` AND no reply has gone out (cannot fully verify; use it as a prompt regardless) → `Reply to <name> at <Company> re: "<subject>"` (cap at one).
4. **Active interview thread** — any meta.md with `status: interviewing` AND `last_inbound` within the last 7 days → `Prep for <Company> — pull stories with /interview-prep <Company>` (one bullet per qualifying company, most recent inbound first; cap at two).
5. **Stale `applied`** — any meta.md with `status: applied` AND `date_applied` more than 14 days ago AND no `last_inbound` (or last_inbound also >14d) → `Chase or close <Company> — applied <N>d ago, no response` (cap at one).
6. **Weekly-target gap >50%** (warm_outreach OR applications, whichever is further behind) → `Send <N> more <warm outreach|applications> this week (<count>/<target>)`. Skip if no target set. "This week" = current ISO week, Monday → today inclusive; same window as the applications.md warm-outreach summary line.
7. **Founder outreach line (conditional on `strategy.md`)** — Read `userdata/strategy.md`. If `weekly_targets.founder_outreach` exists with a numeric target N, and today is Monday AND the warm-outreach count for Saturday + Sunday is 0, render: `Founder outreach — N this week (M done so far).` Where M is counted from journal entries tagged or describing founder DMs in the current ISO week. If `weekly_targets.founder_outreach` is absent, missing, or zero, do not render any founder line at all. Do not invent a target. (Rationale: founder outreach is a discovery channel for early-stage roles where the founder is the hiring decision-maker — see `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`.)

If fewer than three triggers fire, output fewer bullets. Do not invent filler. If zero triggers fire, replace the body with: `Nothing forcing action today — pick from the pipeline below.`

### 2. `## Heads-up`

**Heads-up section — what to surface:**

Non-obvious risks or opportunities — technical, tactical, or strategic — derived from current state across all `userdata/companies/*/meta.md`, recent journal entries (`userdata/journal.md`), and `userdata/strategy.md`. Valid surfaces include but are not limited to:

- **Integration auth failures (when applicable):** single line per failed integration, e.g. `Calendar fetch failed (token expired) — heads-up missing event data this run. Re-auth via your calendar MCP.` These appear FIRST in heads-up so degradation is visible.
- Interview scheduled within 48 hours with no `interview-prep-<date>.md` for that company.
- Company in status `to apply` for 14+ days with no journal movement.
- Offer-evaluation deadline within `strategy.md`'s walk-away window.
- Contradiction between two recent journal entries (e.g. "wants remote" vs "took the on-site interview").
- Strategy weekly_target with significant under/over-pace.
- **Upcoming events this week (when calendar wired):** matched events within the next 7 days, sorted soonest first, e.g. `Wed 21 May 14:00 — Plaid (cpo-round), Fri 23 May 11:00 — N26 (recruiter)`. Skip if none.
- **New inbound (when gmail wired):** unmatched relevant emails (recruiter/talent senders or pipeline-keyword subjects) where no company in `userdata/companies/` matches. Format: `<count> — <Company-guess from sender domain> ("<subject>")`. Each is a prompt to evaluate adding to the pipeline. Skip if none.
- **Checkpoints due within 14d:** comma-separated list of `<date> (<condition>)`. Skip if none.
- **Stale items (>14d in `applied` with no movement):** count and inline list, e.g. `2 — Klarna (16d), Monzo (21d)`. Skip if none.
- **Shape-mismatch warning on active interviews.** Trigger: any meta.md with `status: interviewing` AND (`team_size > 150` OR the company body/research-brief mentions ">150 ppl") AND the company is NOT in any `target_industries` entry from profile.md AND no explicit equity / brand signal in research-brief. When triggered: `Shape mismatch — <Company> is interviewing but <signal recap>. Re-read the role-fit verdict before next round.` This is the hollowing-risk check: a big-co interview proceeding without the shape signals the user actually wants. Skip if no qualifying meta.
- **Coach nudge.** Surfaces when a multi-week pattern suggests `pm-job-search:career-coach` would help diagnose. Three independent triggers — fire at most ONE per /today run. **Trigger C is highest severity; if C fires, suppress A and B.** Skip if no trigger fires.
  - **Trigger A — cadence drift.** Weekly targets (`applications` AND/OR `warm_outreach`) missed by >50% for 3 weeks running. Compute by counting `date_applied` per 7-day window AND keyword-scanning journal per window across the last 21 days. When triggered: `Cadence under 50% three weeks running — pm-job-search:career-coach can help work out if the targets or the search itself needs a rethink.`
  - **Trigger B — passing without applying.** ≥3 meta.md files have `status: not_interested` AND `strategy.md ## Anti-goals` section body is empty. (User is passing on roles without applying — pattern suggests an unstated rule worth naming.) When triggered: `Passed on <N> roles without applying — there's probably a pattern worth naming. Ask pm-job-search:career-coach to walk you through it.`
  - **Trigger C — sunk-cost / structural rethink.** Highest-severity trigger. Suppresses A and B if it fires. Three OR-conditions, ANY one fires it:
    1. **Long search, thin pipeline.** weeks-since-`/setup` ≥ 8 (compute from the earliest `date_added` across all meta.md OR from `target_offer_date` if available) AND companies in `status: interviewing` count < 2 AND companies in `status: offer` count = 0.
    2. **Pattern-of-rejection.** ≥3 meta.md files with `status: rejected` AND the same `rejection_stage` value (e.g. 3 rejections at `take-home`, or 3 rejections at `panel`).
    3. **Cadence-drift escalation.** Trigger A has fired in 4+ consecutive `/today` runs (would require persistent state; if not implementable, fall back to: weeks-since-/setup ≥ 4 AND weekly targets missed by >50% for 4 weeks running).

    When triggered, the message must **cite specific data** (which counts, which dates, which stage) — not abstract framing. Examples:
    - Condition 1: `9 weeks since /setup, 1 active interview thread, 0 offers. This isn't a cadence problem — pm-job-search:career-coach can help work out whether the strategy itself needs restarting, not tweaking.`
    - Condition 2: `3 rejections at the <stage> stage. Same stage, different companies — pm-job-search:career-coach can help work out what specifically is happening there.`
    - Condition 3: `Cadence under 50% for 4 weeks running. The targets or the search shape probably need a structural change, not another push — pm-job-search:career-coach can help diagnose.`
- **Late-stage interview prompts.** Trigger: any company with `status: interviewing` AND `last_inbound` within the last 7 days. When triggered, surface a context-aware prompt to review the interview thread and prepare for the next stage. Companies in `interviewing` whose `last_inbound` is older than 7 days do NOT trigger this — they belong to the "stale items" treatment above.

Two clauses max per bullet (per TONE.md "Briefs, heads-up, and bullet content"). Lead with the entity, bold it.

**If nothing flags:** render the literal line `Nothing flagged today.` Do not pad with low-value items.

### 3. `## Pipeline state`

A markdown table sorted by status group then tier then most recent activity within each group:

| Status | Company | Tier | Position | Last activity | Next event |
|---|---|---|---|---|---|

The "Next event" column only renders when Calendar is wired AND at least one row has a matched future event. If absent or empty, drop the column entirely (revert to the 5-column shape).

Group order: `offer` → `interviewing` → `applied` → `to_apply` → `new`. (`offer` ranks above `interviewing` because an offer in hand is the highest-signal Active state — a decision is imminent, surface it first.) Note: this is the `/today` brief's reading order — high-signal active states first. The dashboard accordion uses a funnel order (`new` → `to_apply` → … → `not_interested`) because that view is for browsing every status, not surfacing what's hottest. Within each group, P0 first, then P1, then P2. Within each tier, most recent `last_inbound` first; if no `last_inbound`, fall back to `date_applied`, then `date_added`.

"Last activity" is the most recent date among `last_inbound`, `date_applied`, `date_added`, rendered as `Nd ago` (e.g. `2d ago`, `today`). For "today", use `today` not `0d ago`.

"Next event" is the nearest matched future Calendar event for that company within 14 days, rendered as `<Day D Mon HH:MM>` (e.g. `Wed 21 May 14:00`). If multiple events match, show the earliest. If none, leave the cell blank.

Below the table, one summary line for decided history (NOT a table — keep terse):
> N decided this search; M rejected, K not interested.

Where `N = M + K`, `rejected` = meta.md with `status: rejected`, and `not interested` = `status: not_interested`. Drop zero-count clauses: if K=0, render `N decided this search; M rejected.`; if M=0, render `N decided this search; K not interested.`; if both zero, skip the line entirely.

## Save behaviour

Default: write the full brief to `userdata/outputs/daily-brief-<YYYY-MM-DD>.md` (today's date in the user's timezone — assume system local). Overwrite if the file already exists for today (no merge — the brief is a single-shot snapshot).

Also regenerate `userdata/outputs/applications.md` (see next section).

If invoked with `--ephemeral`, skip BOTH saves and print the brief to chat only. Useful for quick spot-checks. `--ephemeral` suppresses the brief and applications.md writes only — the input phase still runs and writes confirmed facts to journal.md + meta.md. Choose 'Skip' at the catch-all prompt for a fully no-side-effect spot-check.

Always print the brief to chat regardless of save mode.

## Weekly reflection trigger

**Weekly-reflection nudge (gated — TONE Rule C):**

After the daily brief has been written to `userdata/outputs/daily-brief-<date>.md`, check ALL of:

1. Is this the first `/today` run of the current ISO week? Determined by the marker file `userdata/outputs/.last-weekly-reflection` — if the file's ISO date is older than the current ISO week's Monday, this is the first run of this week.
   - If the file does not exist → condition met (first run of week).
   - If the file exists, read the single ISO date on the first line. If that date falls in a prior ISO week (compare ISO week numbers, not just day counts), condition met. Otherwise it does not.
   - "ISO week" = ISO-8601 week (Monday is day 1, Sunday is day 7). A Sunday belongs to the ISO week that STARTED on the preceding Monday — not the upcoming one. So `isoweek(Sunday)` equals `isoweek(the preceding Monday)`; the next Monday starts a new ISO week. Compare ISO week numbers, not raw day counts.
2. Are there at least one journal entry (`userdata/journal.md`) from the prior ISO week? If no, skip the nudge entirely — there's nothing to reflect on.

The run must also be non-ephemeral (the `--ephemeral` flag was NOT passed).

**If both yes:**

Use `AskUserQuestion` with **Yes, reflect** / **Skip**:

"It's the start of a new week. Want a 5-min reflection on last week? (y / skip)"

On **Yes, reflect** → invoke the `pm-job-search:career-coach` agent with mode hint `weekly-reflection`. The agent reads `journal.md` + `strategy.md`, runs 3-4 reflection prompts, and appends a `## Weekly reflection <YYYY-MM-DD>` block to `journal.md`. See `${CLAUDE_PLUGIN_ROOT}/agents/career-coach.md` for the mode's behaviour.
On **Skip** → do not invoke career-coach.

After the offer (whether accepted or declined), write today's ISO date to the marker file:

```bash
date +%Y-%m-%d > userdata/outputs/.last-weekly-reflection
```

This ensures the offer fires at most once per ISO week regardless of whether the user took it.

If marker write fails, print: "Couldn't write weekly-reflection marker — offer may repeat later this week." and continue.

The weekly reflection is invoked only by the user explicitly accepting the offer; /today never invokes career-coach silently.

## End-of-run nudge

After the brief renders and the weekly-reflection check completes, compose a single one-line context-aware next-step nudge per `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. Skip the nudge entirely if no useful next step is obvious (e.g. the pipeline is healthy and there's nothing time-sensitive to flag).

## `applications.md` regeneration

`applications.md` is a hybrid file: /today owns one HTML-comment-delimited block; the user owns everything outside it. Spec is in plan §I.2.

The GENERATED block looks like:

```markdown
<!-- BEGIN GENERATED — /today regenerates this block. Edit outside the markers, not within. -->

# Applications
Last regenerated: <YYYY-MM-DD HH:MM>

## Active
<table of all status: offer | interviewing | applied | to_apply | new>

## Decided
<table of all status: rejected | not_interested, last 30 days only — older rolls off by date_rejected | date_not_interested>

## Summary
- N active threads (M P0).
- K decided this search.
- Warm-outreach attempts this week: A / B.   (omit this line if no warm_outreach target set)

<!-- END GENERATED -->
```

Rules:

1. **Both markers present** → replace everything between them with a fresh GENERATED block. Preserve the rest of the file byte-for-byte (text above the begin marker, text below the end marker).
2. **File does not exist** → write a fresh file: GENERATED block + a `\n\n## Notes\n\nYour free-text area. /today never touches anything below this line.\n` footer.
3. **File exists but has neither marker** → also write a fresh complete file (same as case 2). The user's previous freeform notes are preserved only if they happen to sit below the new GENERATED block — but since this case implies the file pre-dates the partition convention, an overwrite is acceptable. Print a one-line warning to chat: `applications.md had no markers — regenerated as fresh file.`
4. **Exactly one of the two markers is present** → DO NOT WRITE. Print a clear error to chat: `applications.md has only the <BEGIN|END> marker. Refusing to regenerate to avoid destroying user content. Fix by either adding the missing marker or deleting both.` Continue with the rest of /today (save the daily brief, print to chat).

Active table columns: `| Company | Role | Status | Tier | Link | Last activity |` — same sort as the pipeline_state table in the brief. Company cell links to the company folder: `[Plaid](../companies/Plaid/)` for flat layouts, `[Plaid](../companies/Plaid/<role-slug>/)` for multi-role. The `Link` column contains the JD URL from the company's `meta.md` `link:` field; leave blank if absent.

Example row:

```markdown
| Company | Role | Status | Tier | Link | Last activity |
|---|---|---|---|---|---|
| Plaid | Senior PM | to apply | 1 | https://jobs.lever.co/plaid/… | 2026-05-25 |
```

Any chat output that prints application rows (pipeline section, status lists, brief output) must include the JD URL inline:

Format: `- <Company> — <Role> — <status> — <url>`. Long URLs are fine; do not shorten or wrap.

Decided table columns: `| Company | Status | Tier | Position | Decided |` where `Decided` is the most recent of `date_rejected` / `date_not_interested`. Sort by Decided descending. Cap at items decided within the last 30 days. (`offer` is intentionally NOT included here — an open offer is a high-signal Active state, not a decided one; surface it in the Active table at the top.)

Summary line counts:
- `N active threads (M P0).` — N = count of meta.md with `status` in `{new, to_apply, applied, interviewing, offer}`. M = subset of those with tier P0.
- `K decided this search.` — K = count of meta.md with `status` in `{rejected, not_interested}`.
- `Warm-outreach attempts this week: A / B.` — A = distinct warm-outreach mentions in the current ISO week of journal.md (window = `[Monday of this week, today]` inclusive; keywords: `DM`, `outreach`, `coffee`, `intro`, `intro ask`, `reached out`, `messaged`, `connect`; each dated entry contributes at most one). B = `warm_outreach` target from strategy.md. Omit the entire line if no warm_outreach target set. On Monday morning A is naturally near 0 — that's intentional, it surfaces a fresh week.

## Dedup and discovery rules

Two glob patterns expose all roles:
- `userdata/companies/*/meta.md` — single-role companies (flat).
- `userdata/companies/*/*/meta.md` — multi-role companies (role-slug subfolders).

A company may appear in BOTH globs if a 1→2 migration is mid-way; in practice the migration code (other skills) ensures only one layout per company. If both layouts exist for the same company, prefer the role-slug-subfolder entries and print one warning line: `<Company>: both flat and subfolder meta.md present — using subfolder entries.`

Each meta.md represents one `(company, position)` pair. Counts (active threads, applications-this-week, etc.) are over distinct meta.md files. Two different positions at the same company count as two rows in pipeline_state and applications.md.

## Date handling

- "Today" is the system local date. Format dates as `YYYY-MM-DD`.
- "Within last N days" means `today - (N-1) <= date <= today` (inclusive — last 7 days includes today and the prior 6). Used by triggers tied to recency (stale `applied`, late-stage interview prompts, active-interview-thread detection, integration fetch windows).
- "Current ISO week" / "this week" means `today - today.weekday() <= date <= today` (inclusive — Monday of this week through today; collapses to a single day on Monday, grows to 7 days by Sunday). Used by weekly-progress tracking (warm-outreach summary line, weekly-target gap trigger).
- A missing date field is "unknown" — treat as oldest (so it does NOT trigger "within N days" rules) and rank last when sorting "most recent activity".
- "Nd ago" rendering: `0` → `today`, `1` → `1d ago`, etc.

## What /today never does

- Never writes `userdata/profile.md`, `userdata/strategy.md`, or `userdata/integrations.md`.
- Never touches text outside the GENERATED markers in `applications.md`.
- Never invents data. If `last_inbound` is missing, do not guess; rank by what is available.
- Never persists Calendar / Gmail / Granola responses to disk verbatim. Integration data lives in-context for the run; only the user-confirmed facts written to journal.md and meta.md persist.
- Never writes to journal.md or meta.md without explicit user confirmation in the input phase. Inferred facts must be confirmed (or corrected) before they land — no silent writes from integration data.
- Never auto-fills meta.md fields beyond the input-phase contract (`next_event`, `status`, `## History` block). Other skills still own positions, tier, link, date_applied, date_added.

## Smoke test against the Maya example

When debugging this skill, run it against `userdata/examples/maya/` as a synthetic install (treat that subdirectory as if it were the userdata/ root). Maya's snapshot has NO `userdata/integrations.md`. The brief is the 3-section shape (Top 3 actions → Heads-up → Pipeline state) — there are no "Where you are" or "This week's progress" sections any more.

### Input phase against Maya

- Step 1 (window): Maya's journal currently opens with `## 2026-05-15`. If today is 2026-05-18 in the harness, gap = 3 days → print `Last entry was 3 days ago — pulling the full window.` (Update this assertion if the example install is refreshed with a different most-recent date.)
- Step 2 (inference): integrations.md absent → skipped silently. No items rendered.
- Step 3 (targeted confirms): skipped (step 2 produced nothing).
- Step 4 (open catch-all): single prompt printed. If the user replies with free text mentioning a company, that line should be parsed and routed; if they choose Skip, the input phase exits cleanly with no writes.
- Step 5 (write phase): only runs if the catch-all returned content. With no input from the user, journal.md is not touched and no `## 2026-05-18` heading is created.

To exercise the integration-fold-in code paths AND the targeted-confirms flow, create a temporary `userdata/examples/maya/integrations.md` with `## calendar` / `## gmail` sections wired, dispatch /today, and verify the input phase renders inferred deltas grouped by source.

### Output phase against Maya (after input phase)

With the catch-all skipped, the output phase against Maya's expanded install (8 status slots, Plaid multi-role, Lendable in `offer` status) should produce the 3-section brief:

- **Section 1 "Top 3 actions"**: (4) Plaid prep — `last_inbound: 2026-05-13` is 5d ago, within 7d → fires. (5) iwoca chase/close — `date_applied: 2026-04-22` is 26d ago, >14d → fires. (6) Applications gap — 1/3 = 67% gap, fires. If today is Monday, the Monday warm-outreach batch nudge may also fire (count is at 3/5 — depends on weekend warm-outreach activity). No checkpoint trigger (next is 2026-06-15 = 28d out). No imminent-event or recruiter-reply bullets (no integrations).
- **Section 2 "Heads-up"**: stale-applied bullet fires for iwoca (26d). Shape-mismatch warning fires for Cleo (180 ppl, no equity signal — though strict reading of the trigger requires the company NOT to be in `target_industries`; Cleo's consumer-finance vertical is borderline against Maya's `fintech` / `consumer credit` targets — an LLM may interpret either way). Late-stage prompts fire for Plaid CC (active interview thread with recent inbound). Trigger A coach nudge may fire (applications cadence under 50% for 3 weeks running — depends on journal counts per week).
- **Section 3 "Pipeline state"**: 7 active rows in this group order — Lendable (offer P0) → Plaid CC + Cleo (interviewing P0 then P1) → Marshmallow + iwoca (applied P0 then P1) → Plaid Growth Loops + Zopa (to_apply P1). Multi-role Plaid renders BOTH rows via the dual-glob; each linked to its role-slug subfolder. 5-column shape (no "Next event" column — Calendar not wired). Decided summary: `2 decided this search; 1 rejected, 1 not interested.` (Stripe rejected + Atom Bank not interested.)

If the catch-all DOES return content (e.g. the user types `[Plaid] CPO round confirmed Thu` during step 4), verify that:
- journal.md gains a `## 2026-05-18` heading (if not already present today) with the bullet `- [Plaid] CPO round confirmed Thu (source: user)`.
- `userdata/examples/maya/companies/Plaid/consumer-credit/meta.md` is NOT modified by step 4 alone (free-text doesn't imply a structured field; only inferred + confirmed integration facts update meta.md per the contract).

### Weekly reflection trigger against Maya

- If today is Monday AND `userdata/examples/maya/outputs/.last-weekly-reflection` does not exist AND Maya's journal has entries from the prior ISO week → offer block prints after the brief.
- If today is Monday AND the marker file dates to the prior ISO week AND prior-week journal entries exist → offer block prints.
- If today is Tuesday AND the marker file dates to Monday (same ISO week) → offer block does NOT print.
- If today is Monday AND Maya's journal has NO entries from the prior ISO week → offer block does NOT print (TONE Rule C gate).
- On accept (`y`) → career-coach invoked with `weekly-reflection` mode; on skip → marker file updated, no agent invocation. In both cases, the marker file's content reads today's ISO date as the only line.

### Weekly reflection trigger notes (updated)

The weekly-reflection nudge fires only when BOTH conditions are met: first run of the ISO week AND prior-week journal entries exist. Maya's journal currently has entries from the prior ISO week, so the nudge will fire on the first Monday run.

If the output diverges materially from any of the above against the Maya snapshot, the skill has a bug — fix before promoting.
