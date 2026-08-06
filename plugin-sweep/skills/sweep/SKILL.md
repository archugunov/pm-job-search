---
name: sweep
description: This skill should be used when the user asks to "/job-sweep:sweep", "sweep for jobs", "find me open product roles", "run my weekly job sweep", "any new product roles", or wants a list of currently-open roles matching their profile without adopting a full job-search tracker. Reads job-sweep/profile.md (or creates it on first run from a CV or three questions), runs site-scoped discovery, suppresses anything already in job-sweep/seen-roles.jsonl, and writes job-sweep/roles-<date>.md with roles bucketed strong / possible / edge.
---

# /job-sweep:sweep — find open product roles that match you

Discovery, and nothing else. This plugin does not track applications, score
against a rubric, or keep company folders. It finds roles and remembers what it
already showed you.

**Voice:** every prompt and message in this skill follows
`${CLAUDE_PLUGIN_ROOT}/references/TONE.md` — plain prose not fenced blocks, one
ask per message, no "since last time" prompts on a first run. The exact wording of
each question below is locked-in; use it verbatim, not paraphrased.

## State

Two files, in a `job-sweep/` folder in the user's working directory:

- `job-sweep/profile.md` — frontmatter only. Keys: `target_titles`,
  `target_industries`, `geography: {mode, mode_detail}`, and optional
  `companies_of_interest`.
- `job-sweep/seen-roles.jsonl` — append-only, one JSON object per line.

Never write anywhere else. No `userdata/`, no company folders.

## Mode detection

Run before anything else:

1. `job-sweep/profile.md` exists → **sweep mode**. Read it and go straight to
   "Running the sweep". Do NOT re-ask the onboarding questions, and do NOT ask
   what changed since last time — the profile is the answer.
2. It does not exist → **first-run mode**. Walk the onboarding below, then sweep
   in the same session.

## First run

Create `job-sweep/` first, so there is somewhere to drop a CV, then ask:

> "First sweep — I need three things: what roles you want, what industries, and where you'll work. Drop a CV into `job-sweep/` as cv.md, cv.txt or cv.pdf and I'll read them off it, or just answer three questions. Which?"

Use `AskUserQuestion` with two options: **I'll drop a CV** / **Ask me the three questions**.

### CV path

Follow `${CLAUDE_PLUGIN_ROOT}/references/cv-extraction.md` § "Finding the CV",
checking `job-sweep/cv.md`, `job-sweep/cv.txt`, `job-sweep/cv.pdf` in that order.
Its § "The governing rule" applies in full: **never fill a field the CV does not
contain.** A CV with no clear location means you ask where they'll work — it does
not mean guessing from the most recent employer's address.

Extract only what a sweep needs:

- **target_titles** — per § "Tier 2 — inferences". Read the last two or three
  roles and the trajectory between them; propose the current level plus the
  natural next one. Propose 3-5, never more.
- **target_industries** — per the same section. Industries with two or more roles
  behind them, plus any single role that was the most recent. 3-5, never more.
- **geography** — the CV states where someone has lived, not where they want to
  work. Per § "What is NOT extractable" this is NOT inferable. Ask it.

Show both inferred lists for confirmation as multi-selects, each with the
evidence line § "Tier 2" requires — the roles the inference came from, most
recent first:

> "Roles to sweep for. I pulled these from your CV — <evidence line>. Pick all that apply."

> "Industries. From your CV I'd guess these — <evidence line>. Pick all that apply."

Then ask geography (see below). Never auto-accept an inferred list: a wrong
target title poisons every future sweep.

### Three-question path

Ask each separately — one ask per message, per TONE.md Rule A.

> "What roles are you after? Typical senior-PM examples: Head of Product, Lead PM, Group PM, Principal PM. Comma-separated."

> "What industries? E.g. fintech, healthcare, climate tech, enterprise SaaS. Comma-separated."

### Geography — asked on both paths

> "Where will you work?"

`AskUserQuestion`, single-select, options in this order: `On-site in <city>` (only
if a city is known from the CV — omit this option entirely otherwise) / `Remote` /
`Both` / `Other (free text)`. Store as `mode: onsite|remote|both|other` plus
`mode_detail` free text when the user picks Other.

### Writing the profile

Write `job-sweep/profile.md`:

```markdown
---
target_titles: [Head of Product, Lead PM, Senior PM]
target_industries: [fintech, consumer credit]
geography:
  mode: other
  mode_detail: London hybrid or EMEA remote
---

<!--
  job-sweep's whole profile. Edit any line and the next sweep picks it up.
  Delete this file to start over.

  The full pm-job-search plugin reads this file too — if you ever install it,
  /setup pre-fills from here rather than asking again.
-->
```

Substitute the real answers. Both lists are inline YAML lists. Omit
`companies_of_interest` entirely until it has been asked — never write an empty
key.

Then confirm in one line what was written, and continue straight into the sweep.
Do not make the user re-invoke the command.

## Running the sweep

### 1. Build the queries

Read `${CLAUDE_PLUGIN_ROOT}/references/site-queries.md` and build 8-10 site-scoped
queries from the profile's `target_titles × target_industries × geography`. If
`companies_of_interest` is present, add one `site:` query per company on top.

The `site:` operators are the point — without them WebSearch returns aggregator
previews that cannot be read. Do not drop them to "get more results".

### 2. Filter what comes back

Per `site-queries.md` § "Result filtering", then:

- Title must match at least one entry in the title-match set —
  `${CLAUDE_PLUGIN_ROOT}/references/role-filters.md`.
- Drop any title containing a negative-filter word, same file.
- Never drop a title the user listed verbatim in `target_titles`.

### 3. Suppress what they have already seen

Derive the four identity keys for every candidate per
`${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md` — `company_key`,
`strict_key`, `base_key`, `url_key`. Read every line of
`job-sweep/seen-roles.jsonl` (absent on first run — treat as empty) and:

- `url_key` OR `strict_key` matches a ledger line → **suppress silently.** Already shown.
- `base_key` matches at the same `company_key`, but neither `url_key` nor
  `strict_key` → **show it under a "Possible repeats" heading**, not in the main
  buckets. Same base title, different qualifier; it might be a reworded repost or
  a genuinely different team's role, and only the user can tell.
- No match → new. Include it.

This suppression is the whole reason the ledger exists. A sweep that re-shows
last week's roles is a novelty.

### 4. Verify the posting is live before showing it

Fetch each surviving URL. `site:`-scoped search returns stale index entries and a
large share of results are already closed — in a 2026-08-04 run of the full
plugin's Discovery, 26 of 51 URLs were dead.

- Board's own API or the page says the posting is gone (Ashby's org job list omits
  the ID; Greenhouse/Lever 404 or return an empty posting list; the page says "no
  longer available" / "position has been filled") → **drop it, and still write it
  to the ledger** so it never resurfaces.
- Fetch failed ambiguously (403, bot wall, JS-only shell, timeout) → keep it, and
  mark the row `link unverified` so the user knows to check.
- **Never infer a role's content from the search snippet.** If you could not read
  the posting, you do not know what it says.

### 5. Bucket what survives

Three buckets, from title-match closeness and geography match. There is no
weighted rubric in this profile and you must not invent one.

- **strong** — title matches a `target_titles` entry closely (same level, same
  family) AND geography is compatible with `geography`.
- **possible** — one of those two holds, not both. A right-level role in the wrong
  place, or an adjacent level in the right place.
- **edge** — matched the filters but neither holds strongly. Worth a glance, not a
  plan.

Judge geography from what the posting actually says. If it does not state a
location, it is `possible` at best — never `strong`.

### 6. Write the ledger

Append one line per candidate **evaluated this run** — shown, suppressed, or
dropped as dead. One JSON object per line, keys exactly:

```json
{"company_key": "...", "strict_key": "...", "base_key": "...", "url_key": "...", "raw_title": "...", "first_surfaced": "2026-08-05"}
```

Never rewrite or reorder existing lines; append only. Skip a candidate whose
`strict_key` is already present. `first_surfaced` is today's date, ISO.

This schema is byte-identical to the full plugin's
`userdata/outputs/seen-roles.jsonl` on purpose — it is what lets someone move up
without losing their history.

### 7. Write the output file

`job-sweep/roles-<YYYY-MM-DD>.md`:

```markdown
# Roles — <YYYY-MM-DD>

<N> new since your last sweep. <M> already-seen roles suppressed.

## Strong

| Company | Role | Where | Link |
|---|---|---|---|

## Possible

| Company | Role | Where | Link |
|---|---|---|---|

## Edge

| Company | Role | Where | Link |
|---|---|---|---|

## Possible repeats

Same base title as something you've seen, different qualifier — might be a repost.

| Company | Role | Link |
|---|---|---|
```

Drop any bucket that is empty rather than rendering an empty table. If every
bucket is empty, write the heading and one line saying nothing new came back this
week, and suggest widening geography or industries — do not pad the file.

### 8. Report in chat

Plain prose per TONE.md — not a fenced block, not a repeat of the whole table.
Name the count per bucket, the single most interesting role, and where the file
went. Then close with one line on what the full plugin adds:

> "That's discovery. If you get to the point of tracking applications, scoring fit and prepping interviews, the full `pm-job-search` plugin does that — and its `/setup` reads this profile, so you won't re-answer any of this."

Say that once, at the end of a run. Never mid-sweep, and never twice.

## What this skill never does

- Never writes outside `job-sweep/`.
- Never tracks an application, scores a tier, or creates a company folder — that
  is the full plugin's job, and duplicating it here is how this becomes the thing
  it was built to avoid.
- Never invents a company, role, URL or location. A hallucinated posting is worse
  than an empty sweep.
- Never re-asks onboarding once `job-sweep/profile.md` exists.
