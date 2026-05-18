---
name: today
description: This skill should be used when the user asks for "/today", "my daily brief", "today's brief", "where am I in my job search", "what should I work on today", "pipeline state", or wants a snapshot of weekly progress against targets and a sorted view of every active company. Two-phase: input phase captures fresh facts since the last journal entry (via wired Calendar/Gmail/Granola integrations + an open catch-all prompt), then writes them to userdata/journal.md and relevant userdata/companies/*/meta.md; output phase reads userdata/strategy.md + all meta.md + last 7 days of journal.md, writes a 5-section daily brief to userdata/outputs/daily-brief-<date>.md, regenerates the GENERATED block of userdata/outputs/applications.md, and on the first run of each ISO week offers a hand-off to pm-job-search:career-coach for a weekly reflection.
---

# /today — daily brief

Produce a short (~half a screen) snapshot that combines: where the user is against their stated strategy, what to actually do next, and a sorted view of the pipeline. Save the brief, regenerate the applications.md index, then print the brief to chat.

**Voice:** all chat output and drafted content (the daily brief, summary lines, warnings) follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`.

## Input phase (runs before brief generation)

Capture fresh facts since the last journal entry. Each confirmed fact gets appended to `userdata/journal.md` and — when it has structured implications — pushed to the relevant `userdata/companies/<Co>/meta.md`. Then the output phase runs against the just-written state.

This phase always runs (even with no integrations wired) but degrades gracefully — inference and confirms are skipped when there is nothing to scan, and the catch-all prompt becomes the only input surface.

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

```
Since your last entry (2026-05-15), I see:

From calendar:
1. Plaid — Round 2 panel scheduled Fri 2026-05-22 14:00
2. Klarna — Recruiter call moved from Wed to Thu

From gmail:
3. Lendable — Reply from Sarah at Lendable (likely rejection — want me to read it?)
4. Stripe — New inbound from a recruiter named James (no company match yet)

From granola:
5. Klarna recruiter call transcript captured Mon 2026-05-15

Confirm 1-5 ('all', '1 3 5', or describe corrections). Anything I should edit or skip?
```

User response handling:
- `all` / `yes` → confirm every inferred item as-is.
- Numbered subset (`1 3 5`) → confirm only those.
- `1 wrong — that was R3 not R2` → confirm with edit applied before write.
- `skip 3` → drop item 3 from this run.
- `4 is for company X` → re-route the unmatched inbound to company X before write.

If the user response is ambiguous, ask one clarifying question rather than guessing. Never write an item the user has not explicitly confirmed.

### Step 4 — open catch-all

After targeted confirms (or in place of them when step 2 produced nothing), print one prompt:

> Anything else that moved? Mock interviews, prep work, energy notes, new leads, structural thoughts — anything you want logged. (Press enter to skip.)

User responds in free text. Parse for company tags: explicit `[Plaid]`, `Plaid:`, or first-token match against the company list. Lines without a company tag are logged to `journal.md` only (no meta.md write, no guessing). Lines WITH a company tag are also logged to `journal.md` only — catch-all input is free text and never writes to meta.md, even when the tag matches a known company. Only integration-sourced facts that pass through the Step 3 confirm flow may update meta.md.

### Step 5 — write phase

Commit the confirmed facts. See "Write contracts" section below for the exact journal.md and meta.md formats.

Writes are idempotent per `/today` run: if the user runs `/today` twice the same day with no new facts (step 2 finds nothing new, step 4 skipped), no journal write occurs and no `## YYYY-MM-DD` heading is added or modified.

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

Per-company meta.md uses (or gains, if not already present) three fields written by the input phase. Existing fields owned by other skills — `company`, `position`, `tier`, `link`, `date_applied`, `date_added`, `monitoring`, `last_inbound`, `rejection_stage`, `date_rejected`, `date_closed` — are untouched.

- **`next_event:`** — string, free-form. Examples: `"R2 panel Fri 2026-05-22 14:00"`, `"Recruiter call Thu 2026-05-21 10:00"`. Cleared (set to empty string or removed) when the input phase confirms the event passed without follow-up OR when it was cancelled. Updated in-place when an event is rescheduled.
- **`status:`** — enum, one of: `new`, `to_apply`, `applied`, `interviewing`, `offer`, `rejected`, `closed`. The input phase only transitions OUT of an active state when a fact unambiguously implies it: a confirmed rejection → `rejected`, a confirmed offer → `offer`. Confirmed scheduling events do NOT auto-promote `applied` → `interviewing` (other skills own that transition based on richer signal).
- **`## History` block** — chronological list of state transitions, one line per change. Format: `2026-05-18: status → rejected (seniority mismatch — Sarah at Lendable, gmail confirmed)`. Append to the end of the block; create the `## History` heading at the bottom of meta.md if it doesn't exist.

Rules:
- When an event is rescheduled, update `next_event` AND append a History line: `2026-05-18: next_event → "R2 panel Fri 2026-05-22 14:00" (rescheduled from Wed, calendar confirmed)`.
- When an event passes without action (e.g. yesterday's recruiter call happened), clear `next_event` and append: `2026-05-18: next_event cleared (passed, no follow-up captured yet)`.
- When the input phase has no implication for a given company in meta.md, do not touch that file at all.
- Frontmatter changes are YAML-safe: preserve other fields, preserve quoting style, preserve trailing comments.

## Inputs

Read in this order. Skip gracefully if a file is missing — the brief degrades section-by-section, never errors out wholesale.

1. `userdata/strategy.md` — frontmatter (`target_offer_date`, `weekly_targets`, `pipeline_targets`, `checkpoints`) and the `## Headline goal` paragraph.
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
2. On Mondays only, additionally fetch events from the last 7 days using the same keyword + company-name filter — feeds the Monday retrospective.
3. For each kept event, capture: `{Day D Mon, HH:MM}`, matched company (or `unmatched` for keyword-only hits), event type (`interview`, `recruiter`, etc.).

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

Five sections, in this order, ~half a screen total. Never longer. Skip a whole section (do not pad with "N/A") when the underlying data is unavailable.

### 1. `## Where you are`

One line summarising `strategy.md ## Headline goal` — compress to a single sentence, ≤25 words. Lift the concrete nouns (role level, comp floor, deadline, geo); drop the rationale and qualifiers.
One countdown line: `N days to target_offer_date YYYY-MM-DD`.

Skip the whole section if strategy.md is missing or has no headline goal.

### 2. `## This week's progress`

Three bullets, only those whose target is set in strategy.md:
- `warm_outreach: <count> / <target> (<gap>)` — count is the number of distinct warm-outreach mentions in the last 7 days of `journal.md`. Match on keywords: `DM`, `outreach`, `coffee`, `intro`, `intro ask`, `reached out`, `messaged`, `connect`. Each dated journal entry contributes at most one count per matched bullet (do not double-count).
- `applications: <count> / <target> (<gap>)` — count is the number of meta.md files with `date_applied` in the last 7 days (today minus 6 inclusive).
- `active_interview_threads: <count> / <floor> (<delta>)` — count of meta.md with `status: interviewing` (regardless of date).

`<gap>` is `target - count` framed as `+N to go` if behind, `met` if hit, `+N over` if exceeded. For active_threads, frame as `<delta>` (e.g. `-1` if below floor, `+2` if above).

If a target is unset in strategy.md (line missing or value is null/blank), omit that bullet. Do not show `0/0`.

If strategy.md has no targets set at all (all three unset), replace the entire section body with:
> Strategy targets not set. Re-run `/pm-job-search:setup --refresh` to add a target date (auto-derives weekly cadences), or edit `userdata/strategy.md` directly to enable progress tracking.

**Monday retrospective extension.** On Mondays only, append a one-line week-over-week summary below the three bullets. Compute the previous 7-day window (`today - 13` to `today - 7`) and compare:

> Last week → this week: applications <prev>→<curr>, warm <prev>→<curr>, new threads <prev>→<curr>.

`new threads` counts meta.md entries that transitioned INTO `status: interviewing` during each window (inferable from `last_inbound` falling within the window if no prior debrief exists). If any of the three deltas is materially worse (drop ≥50%), add a single italic sentence after the line, e.g. *Applications halved week-over-week — momentum at risk.* Tue-Sun: omit the retrospective entirely (no Monday-only noise other days).

**Calendar fold-in (Monday + calendar wired).** If the Calendar fetch returned ≥1 last-week event, append one additional line under the retrospective:

> Interviews held last week: <N> — <Day> <Company> (<type>), <Day> <Company> (<type>), … (max 3 listed; if more, append `+ K more`).

Skip the line entirely if N=0 or Calendar is not wired.

### 3. `## Top 3 actions today`

At most three bullets. Each bullet is concrete and anchored to a company name or a strategy element. Surface bullets by running the trigger rules below, in this priority order, and stopping at three:

1. **Imminent calendar event (when calendar wired)** — any matched event within the next 48 hours → `<Day HH:MM> — <Company> <event-type>: prep with /interview-prep <Company>` (cap at two; most-soonest first).
2. **Checkpoint due in ≤14 days** → `Review checkpoint due <date>: <condition> → <action>` (one bullet per upcoming checkpoint; cap at one if multiple).
3. **Recruiter email needing reply (when gmail wired)** — any matched email from the Gmail fetch where the from-address is recruiter/talent AND the company is in `status: interviewing` or `status: applied` AND no reply has gone out (cannot fully verify; use it as a prompt regardless) → `Reply to <name> at <Company> re: "<subject>"` (cap at one).
4. **Active interview thread** — any meta.md with `status: interviewing` AND `last_inbound` within the last 7 days → `Prep for <Company> — pull stories with /interview-prep <Company>` (one bullet per qualifying company, most recent inbound first; cap at two).
5. **Stale `applied`** — any meta.md with `status: applied` AND `date_applied` more than 14 days ago AND no `last_inbound` (or last_inbound also >14d) → `Chase or close <Company> — applied <N>d ago, no response` (cap at one).
6. **Weekly-target gap >50%** (warm_outreach OR applications, whichever is further behind) → `Send <N> more <warm outreach|applications> this week (<count>/<target>)`. Skip if no target set.
7. **Monday + no warm_outreach Sat-Sun** — when today is Monday AND the warm-outreach count for Saturday + Sunday is 0 AND a warm_outreach target is set → `Monday founder-touchpoint batch — DM N founders today` (N = the gap).

If fewer than three triggers fire, output fewer bullets. Do not invent filler. If zero triggers fire, replace the body with: `Nothing forcing action today — pick from the pipeline below.`

### 4. `## Pipeline state`

A markdown table sorted by status group then tier then most recent activity within each group:

| Status | Company | Tier | Position | Last activity | Next event |
|---|---|---|---|---|---|

The "Next event" column only renders when Calendar is wired AND at least one row has a matched future event. If absent or empty, drop the column entirely (revert to the 5-column shape).

Group order: `interviewing` → `applied` → `to_apply` → `new`. Within each group, P0 first, then P1, then P2. Within each tier, most recent `last_inbound` first; if no `last_inbound`, fall back to `date_applied`, then `date_added`.

"Last activity" is the most recent date among `last_inbound`, `date_applied`, `date_added`, rendered as `Nd ago` (e.g. `2d ago`, `today`). For "today", use `today` not `0d ago`.

"Next event" is the nearest matched future Calendar event for that company within 14 days, rendered as `<Day D Mon HH:MM>` (e.g. `Wed 21 May 14:00`). If multiple events match, show the earliest. If none, leave the cell blank.

Below the table, one summary line for closed history (NOT a table — keep terse):
> N closed this search; M rejected, K withdrew.

Where `N = M + K`, `rejected` = meta.md with `status: rejected`, and `withdrew` = `status: closed`. Drop zero-count clauses: if K=0, render `N closed this search; M rejected.`; if M=0, render `N closed this search; K withdrew.`; if both zero, skip the line entirely.

### 5. `## Heads-up`

Seven bullet types, in this order; omit any bullet whose list is empty:

- **Integration auth failures (when applicable):** single line per failed integration, e.g. `Calendar fetch failed (token expired) — heads-up missing event data this run. Re-auth via your calendar MCP.` These appear FIRST in heads-up so degradation is visible.
- **Upcoming events this week (when calendar wired):** matched events within the next 7 days, sorted soonest first, e.g. `Wed 21 May 14:00 — Plaid (cpo-round), Fri 23 May 11:00 — N26 (recruiter)`. Skip if none.
- **New inbound (when gmail wired):** unmatched relevant emails (recruiter/talent senders or pipeline-keyword subjects) where no company in `userdata/companies/` matches. Format: `<count> — <Company-guess from sender domain> ("<subject>")`. Each is a prompt to evaluate adding to the pipeline. Skip if none.
- **Checkpoints due within 14d:** comma-separated list of `<date> (<condition>)`. Skip if none.
- **Stale items (>14d in `applied` with no movement):** count and inline list, e.g. `2 — Klarna (16d), Monzo (21d)`. Skip if none.
- **Shape-mismatch warning on active interviews.** Trigger: any meta.md with `status: interviewing` AND (`team_size > 150` OR the company body/research-brief mentions ">150 ppl") AND the company is NOT in any `target_industries` entry from profile.md AND no explicit equity / brand signal in research-brief. When triggered: `Shape mismatch — <Company> is interviewing but <signal recap>. Re-read the role-fit verdict before next round.` This is the hollowing-risk check: a big-co interview proceeding without the shape signals the user actually wants. Skip if no qualifying meta.
- **Coach nudge.** Surfaces when a multi-week pattern suggests `pm-job-search:career-coach` would help diagnose. Three independent triggers — fire at most ONE per /today run. **Trigger C is highest severity; if C fires, suppress A and B.** Skip if no trigger fires.
  - **Trigger A — cadence drift.** Weekly targets (`applications` AND/OR `warm_outreach`) missed by >50% for 3 weeks running. Compute by counting `date_applied` per 7-day window AND keyword-scanning journal per window across the last 21 days. When triggered: `Cadence under 50% three weeks running — pm-job-search:career-coach can help work out if the targets or the search itself needs a rethink.`
  - **Trigger B — closing without applying.** ≥3 meta.md files have `status: closed` AND `strategy.md ## Anti-goals` section body is empty. (User is closing roles without applying — pattern suggests an unstated rule worth naming.) When triggered: `Closed <N> roles without applying — there's probably a pattern worth naming. Ask pm-job-search:career-coach to walk you through it.`
  - **Trigger C — sunk-cost / structural rethink.** Highest-severity trigger. Suppresses A and B if it fires. Three OR-conditions, ANY one fires it:
    1. **Long search, thin pipeline.** weeks-since-`/setup` ≥ 8 (compute from the earliest `date_added` across all meta.md OR from `target_offer_date` if available) AND companies in `status: interviewing` count < 2 AND companies in `status: offer` count = 0.
    2. **Pattern-of-rejection.** ≥3 meta.md files with `status: rejected` AND the same `rejection_stage` value (e.g. 3 rejections at `take-home`, or 3 rejections at `panel`).
    3. **Cadence-drift escalation.** Trigger A has fired in 4+ consecutive `/today` runs (would require persistent state; if not implementable, fall back to: weeks-since-/setup ≥ 4 AND weekly targets missed by >50% for 4 weeks running).

    When triggered, the message must **cite specific data** (which counts, which dates, which stage) — not abstract framing. Examples:
    - Condition 1: `9 weeks since /setup, 1 active interview thread, 0 offers. This isn't a cadence problem — pm-job-search:career-coach can help work out whether the strategy itself needs restarting, not tweaking.`
    - Condition 2: `3 rejections at the <stage> stage. Same stage, different companies — pm-job-search:career-coach can help work out what specifically is happening there.`
    - Condition 3: `Cadence under 50% for 4 weeks running. The targets or the search shape probably need a structural change, not another push — pm-job-search:career-coach can help diagnose.`
- **Late-stage interview prompts.** Trigger: any company with `status: interviewing` AND `last_inbound` within the last 7 days. When triggered, list the company names on one line, then surface the three founder-vetting questions verbatim:
  - "What does a typical week look like — product vs meetings?"
  - "Where has the last HoP spent most political capital internally?"
  - "When something underperforms — who's in the debrief room?"

  Companies in `interviewing` whose `last_inbound` is older than 7 days do NOT trigger this — they belong to the "stale items" treatment above with a slightly different framing if needed.

## Save behaviour

Default: write the full brief to `userdata/outputs/daily-brief-<YYYY-MM-DD>.md` (today's date in the user's timezone — assume system local). Overwrite if the file already exists for today (no merge — the brief is a single-shot snapshot).

Also regenerate `userdata/outputs/applications.md` (see next section).

If invoked with `--ephemeral`, skip BOTH saves and print the brief to chat only. Useful for quick spot-checks. `--ephemeral` suppresses the brief and applications.md writes only — the input phase still runs and writes confirmed facts to journal.md + meta.md. Skip the catch-all (press enter) for a fully no-side-effect spot-check.

Always print the brief to chat regardless of save mode.

## First-run automation nudge

After the brief renders, check whether to surface a one-shot nudge asking the user to set up daily auto-runs.

**Trigger conditions (ALL must be true):**

1. The run is non-ephemeral (the `--ephemeral` flag was NOT passed).
2. The marker file `userdata/outputs/.automation-nudge-shown` does NOT exist.

**When triggered:** append the following block to the chat output (NOT to the saved daily-brief file — the nudge is a one-time chat surface, not part of the brief history). Then create the marker file with `touch userdata/outputs/.automation-nudge-shown` so the nudge never fires again on this install.

```
---

First daily brief filed. Want this to run automatically at 9am every day?

- **Inside Claude Code (cross-platform, easiest):** run `/schedule` and follow the prompt for a daily 09:00 trigger on `/pm-job-search:today`.
- **macOS launchd (no Claude Code session needed):** ask Claude Code to draft a `~/Library/LaunchAgents/com.<you>.pm-job-search-today.plist` for a headless `claude -p "/pm-job-search:today"` daily run. Survives reboots, no terminal needed.
- **Linux / generic cron:** add `0 9 * * * cd <workspace> && claude -p "/pm-job-search:today"` to `crontab -e`.

Skip this if you'd rather drive it manually. This nudge fires once — delete `userdata/outputs/.automation-nudge-shown` to see it again.
```

The nudge is informational. /today does NOT attempt to set up scheduling itself — different OSes, different shells, permission considerations. The user picks the path that fits their setup.

If the marker file write fails (read-only filesystem, etc.) print one line to chat: `Couldn't write nudge marker — automation prompt will repeat on next /today run.` and continue without erroring. The nudge resurfacing is annoying, not destructive.

## Weekly reflection trigger

After the brief renders (and after the first-run automation nudge has been considered), check whether to offer a weekly reflection hand-off to `pm-job-search:career-coach`.

**Trigger conditions (ALL must be true):**

1. The run is non-ephemeral (the `--ephemeral` flag was NOT passed).
2. Today is the first `/today` run of the current ISO week. Determined by reading the marker file `userdata/outputs/.last-weekly-reflection`:
   - If the file does not exist → trigger fires.
   - If the file exists, read the single ISO date on the first line. If that date falls in a prior ISO week (compare ISO week numbers, not just day counts), trigger fires. Otherwise it does not.
   - "ISO week" = ISO-8601 week (Monday is day 1, Sunday is day 7). A Sunday belongs to the ISO week that STARTED on the preceding Monday — not the upcoming one. So `isoweek(Sunday)` equals `isoweek(the preceding Monday)`; the next Monday starts a new ISO week. Compare ISO week numbers, not raw day counts.

**When triggered:** append the following block to the chat output (NOT to the saved daily-brief file — the offer is a one-time chat surface, not part of the brief history):

```
---

It's the start of a new week. Want a 5-min reflection on last week? (y / skip)
```

Wait for user response.

- If user replies `y` (or any affirmative) → invoke the `pm-job-search:career-coach` agent with the mode hint `weekly-reflection`. The agent reads journal.md + strategy.md, runs 3-4 reflection prompts, and appends a `## Weekly reflection <YYYY-MM-DD>` block to journal.md. See `plugin/agents/career-coach.md` for the mode's behaviour.
- If user replies `skip` (or any negative / non-affirmative) → do not invoke career-coach.
- In BOTH cases (accept and skip), update the marker file by writing today's ISO date as the only line:

  ```bash
  date +%Y-%m-%d > userdata/outputs/.last-weekly-reflection
  ```

  This ensures the offer fires at most once per ISO week regardless of whether the user took it.

If the marker file write fails (read-only filesystem, etc.) print one line to chat: `Couldn't write weekly-reflection marker — offer may repeat later this week.` and continue without erroring.

The weekly reflection is invoked by the user explicitly accepting the offer; /today never invokes career-coach silently.

## `applications.md` regeneration

`applications.md` is a hybrid file: /today owns one HTML-comment-delimited block; the user owns everything outside it. Spec is in plan §I.2.

The GENERATED block looks like:

```markdown
<!-- BEGIN GENERATED — /today regenerates this block. Edit outside the markers, not within. -->

# Applications
Last regenerated: <YYYY-MM-DD HH:MM>

## Active
<table of all status: new | to_apply | applied | interviewing>

## Decided
<table of all status: offer | rejected | closed, last 30 days only — older rolls off by date_rejected | date_closed | date_added>

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

Active table columns: `| Company | Status | Tier | Position | Last activity |` — same sort as the pipeline_state table in the brief. Company cell links to the company folder: `[Plaid](../companies/Plaid/)` for flat layouts, `[Plaid](../companies/Plaid/<role-slug>/)` for multi-role.

Decided table columns: `| Company | Status | Tier | Position | Closed |` where `Closed` is the most recent of `date_rejected` / `date_closed` / `date_added`. Sort by Closed descending. Cap at items closed within the last 30 days.

Summary line counts use the same data the brief uses; the warm-outreach line mirrors the brief's "This week's progress" entry.

## Dedup and discovery rules

Two glob patterns expose all roles:
- `userdata/companies/*/meta.md` — single-role companies (flat).
- `userdata/companies/*/*/meta.md` — multi-role companies (role-slug subfolders).

A company may appear in BOTH globs if a 1→2 migration is mid-way; in practice the migration code (other skills) ensures only one layout per company. If both layouts exist for the same company, prefer the role-slug-subfolder entries and print one warning line: `<Company>: both flat and subfolder meta.md present — using subfolder entries.`

Each meta.md represents one `(company, position)` pair. Counts (active threads, applications-this-week, etc.) are over distinct meta.md files. Two different positions at the same company count as two rows in pipeline_state and applications.md.

## Date handling

- "Today" is the system local date. Format dates as `YYYY-MM-DD`.
- "Within last N days" means `today - (N-1) <= date <= today` (inclusive — last 7 days includes today and the prior 6).
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

When debugging this skill, run it against `userdata/examples/maya/` as a synthetic install (treat that subdirectory as if it were the userdata/ root). Maya's snapshot has NO `userdata/integrations.md`.

### Input phase against Maya

- Step 1 (window): last journal entry is `## 2026-05-15` (after Task 7's example refresh). If today is 2026-05-18 in the harness, gap = 3 days → print `Last entry was 3 days ago — pulling the full window.`
- Step 2 (inference): integrations.md absent → skipped silently. No items rendered.
- Step 3 (targeted confirms): skipped (step 2 produced nothing).
- Step 4 (open catch-all): single prompt printed. If the user replies with free text mentioning a company, that line should be parsed and routed; if they press enter / skip, the input phase exits cleanly with no writes.
- Step 5 (write phase): only runs if the catch-all returned content. With no input from the user, journal.md is not touched and no `## 2026-05-18` heading is created.

To exercise the integration-fold-in code paths AND the targeted-confirms flow, create a temporary `userdata/examples/maya/integrations.md` with `## calendar` / `## gmail` sections wired, dispatch /today, and verify the input phase renders inferred deltas grouped by source.

### Output phase against Maya (after input phase)

The existing output-phase expectations still hold when the input phase makes no writes (the catch-all skip path). Quick recap:

- "Where you are": pulls Maya's headline goal, countdown to 2026-08-01.
- "This week's progress": warm_outreach 1/5, applications 0/3, active_threads 1/4 (Plaid). No "Interviews held last week" line — Calendar not wired.
- "Top 3 actions": Plaid prep nudge + applications gap nudge. No checkpoint trigger, no Monday batch (if today is not Monday), no imminent-event or recruiter-reply bullets (no integrations).
- "Pipeline state": Plaid row only. 5-column shape (no "Next event" column). Closed summary: `1 closed this search; 1 rejected.`
- "Heads-up": no checkpoints, no stale `applied`, no integration bullets, late-stage prompts triggered by Plaid with the three founder-vetting questions printed verbatim.

If the catch-all DOES return content (e.g. the user types `[Plaid] CPO round confirmed Thu` during step 4), verify that:
- journal.md gains a `## 2026-05-18` heading (if not already present today) with the bullet `- [Plaid] CPO round confirmed Thu (source: user)`.
- `userdata/examples/maya/companies/Plaid/meta.md` is NOT modified by step 4 alone (free-text doesn't imply a structured field; only inferred + confirmed integration facts update meta.md per the contract).

### Weekly reflection trigger against Maya

- If today is Monday AND `userdata/examples/maya/outputs/.last-weekly-reflection` does not exist → offer block prints after the brief.
- If today is Monday AND the marker file dates to the prior ISO week → offer block prints.
- If today is Tuesday AND the marker file dates to Monday (same ISO week) → offer block does NOT print.
- On accept (`y`) → career-coach invoked with `weekly-reflection` mode; on skip → marker file updated, no agent invocation. In both cases, the marker file's content reads today's ISO date as the only line.

### First-run automation nudge

The first-run automation nudge still fires on the first non-ephemeral run against Maya (the marker file isn't checked into the example). Subsequent runs against Maya will suppress it once `userdata/examples/maya/outputs/.automation-nudge-shown` exists; delete that file to re-trigger.

If the output diverges materially from any of the above against the Maya snapshot, the skill has a bug — fix before promoting.
