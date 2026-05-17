---
name: today
description: This skill should be used when the user asks for "/today", "my daily brief", "today's brief", "where am I in my job search", "what should I work on today", "pipeline state", or wants a snapshot of weekly progress against targets and a sorted view of every active company. Reads userdata/strategy.md, all userdata/companies/*/meta.md, and the last entries of userdata/journal.md; writes a 5-section daily brief to userdata/outputs/daily-brief-<date>.md; regenerates the GENERATED block of userdata/outputs/applications.md.
---

# /today — daily brief

Produce a short (~half a screen) snapshot that combines: where the user is against their stated strategy, what to actually do next, and a sorted view of the pipeline. Save the brief, regenerate the applications.md index, then print the brief to chat.

**Voice:** all chat output and drafted content (the daily brief, summary lines, warnings) follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`.

## Inputs

Read in this order. Skip gracefully if a file is missing — the brief degrades section-by-section, never errors out wholesale.

1. `userdata/strategy.md` — frontmatter (`target_offer_date`, `weekly_targets`, `pipeline_targets`, `checkpoints`) and the `## Headline goal` paragraph.
2. All company `meta.md` files. Use BOTH globs (companies are either flat or in role-slug subfolders):
   - `userdata/companies/*/meta.md`
   - `userdata/companies/*/*/meta.md`
3. `userdata/journal.md` — last 7 days of entries (entries are dated `## YYYY-MM-DD` headings; take everything with a date within the last 7 days).
4. `userdata/outputs/applications.md` if it exists (needed for the partition rewrite — see "applications.md regeneration" below).

Do not read `userdata/profile.md`. /today does not need profile content; trust strategy.md and the per-company meta.

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

### 3. `## Top 3 actions today`

At most three bullets. Each bullet is concrete and anchored to a company name or a strategy element. Surface bullets by running the trigger rules below, in this priority order, and stopping at three:

1. **Checkpoint due in ≤14 days** → `Review checkpoint due <date>: <condition> → <action>` (one bullet per upcoming checkpoint; cap at one if multiple).
2. **Active interview thread** — any meta.md with `status: interviewing` AND `last_inbound` within the last 7 days → `Prep for <Company> — pull stories with /interview-prep <Company>` (one bullet per qualifying company, most recent inbound first; cap at two).
3. **Stale `applied`** — any meta.md with `status: applied` AND `date_applied` more than 14 days ago AND no `last_inbound` (or last_inbound also >14d) → `Chase or close <Company> — applied <N>d ago, no response` (cap at one).
4. **Weekly-target gap >50%** (warm_outreach OR applications, whichever is further behind) → `Send <N> more <warm outreach|applications> this week (<count>/<target>)`. Skip if no target set.
5. **Monday + no warm_outreach Sat-Sun** — when today is Monday AND the warm-outreach count for Saturday + Sunday is 0 AND a warm_outreach target is set → `Monday founder-touchpoint batch — DM N founders today` (N = the gap).

If fewer than three triggers fire, output fewer bullets. Do not invent filler. If zero triggers fire, replace the body with: `Nothing forcing action today — pick from the pipeline below.`

### 4. `## Pipeline state`

A markdown table sorted by status group then tier then most recent activity within each group:

| Status | Company | Tier | Position | Last activity |
|---|---|---|---|---|

Group order: `interviewing` → `applied` → `to_apply` → `new`. Within each group, P0 first, then P1, then P2. Within each tier, most recent `last_inbound` first; if no `last_inbound`, fall back to `date_applied`, then `date_added`.

"Last activity" is the most recent date among `last_inbound`, `date_applied`, `date_added`, rendered as `Nd ago` (e.g. `2d ago`, `today`). For "today", use `today` not `0d ago`.

Below the table, one summary line for closed history (NOT a table — keep terse):
> N closed this search; M rejected, K withdrew.

Where `N = M + K`, `rejected` = meta.md with `status: rejected`, and `withdrew` = `status: closed`. Drop zero-count clauses: if K=0, render `N closed this search; M rejected.`; if M=0, render `N closed this search; K withdrew.`; if both zero, skip the line entirely.

### 5. `## Heads-up`

Four bullet types, in this order; omit any bullet whose list is empty:

- **Checkpoints due within 14d:** comma-separated list of `<date> (<condition>)`. Skip if none.
- **Stale items (>14d in `applied` with no movement):** count and inline list, e.g. `2 — Klarna (16d), Monzo (21d)`. Skip if none.
- **Shape-mismatch warning on active interviews.** Trigger: any meta.md with `status: interviewing` AND (`team_size > 150` OR the company body/research-brief mentions ">150 ppl") AND the company is NOT in any `target_industries` entry from profile.md AND no explicit equity / brand signal in research-brief. When triggered: `Shape mismatch — <Company> is interviewing but <signal recap>. Re-read the role-fit verdict before next round.` This is the hollowing-risk check: a big-co interview proceeding without the shape signals the user actually wants. Skip if no qualifying meta.
- **Late-stage interview prompts.** Trigger: any company with `status: interviewing` AND `last_inbound` within the last 7 days. When triggered, list the company names on one line, then surface the three founder-vetting questions verbatim:
  - "What does a typical week look like — product vs meetings?"
  - "Where has the last HoP spent most political capital internally?"
  - "When something underperforms — who's in the debrief room?"

  Companies in `interviewing` whose `last_inbound` is older than 7 days do NOT trigger this — they belong to the "stale items" treatment above with a slightly different framing if needed.

## Save behaviour

Default: write the full brief to `userdata/outputs/daily-brief-<YYYY-MM-DD>.md` (today's date in the user's timezone — assume system local). Overwrite if the file already exists for today (no merge — the brief is a single-shot snapshot).

Also regenerate `userdata/outputs/applications.md` (see next section).

If invoked with `--ephemeral`, skip BOTH saves and print the brief to chat only. Useful for quick spot-checks.

Always print the brief to chat regardless of save mode.

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

- Never edits `meta.md` files (status, dates, positions). Other skills own meta.md changes.
- Never writes `userdata/profile.md`, `userdata/strategy.md`, or `userdata/journal.md`.
- Never touches text outside the GENERATED markers in `applications.md`.
- Never invents data. If `last_inbound` is missing, do not guess; rank by what is available.

## Smoke test against the Maya example

When debugging this skill, run it against `userdata/examples/maya/` as a synthetic install (treat that subdirectory as if it were the userdata/ root). Expected output highlights:

- "Where you are": pulls Maya's headline goal, countdown to 2026-08-01.
- "This week's progress": warm_outreach 1/5 (`DM` keyword in 2026-05-13 entry), applications 0/3 (no `date_applied` in last 7d), active_threads 1/4 (Plaid).
- "Top 3 actions": Plaid prep nudge (Plaid is `interviewing`, `last_inbound: 2026-05-13` within 7d) + applications gap nudge (0/3, further behind than warm_outreach 1/5). No checkpoint trigger (next checkpoint 2026-06-15 is 31d out). 2026-05-15 is a Friday, so no Monday batch.
- "Pipeline state": Plaid row only. Closed summary: `1 closed this search; 1 rejected.` (the `0 withdrew` clause is dropped).
- "Heads-up": no checkpoints in 14d, no stale `applied`, late-stage prompts triggered by Plaid; three founder-vetting questions printed verbatim.

If the output diverges materially from the above against the Maya snapshot, the skill has a bug — fix before promoting.
