---
name: job-search
description: This skill should be used when the user asks to "/job-search", "weekly job search", "find new roles", "discover postings", "recheck monitoring companies", "any new jobs at <companies>", or wants a sweep of new job postings matching their profile plus a recheck of companies they're tracking. Reads userdata/profile.md (target_titles / target_industries / hard_filters), reads all userdata/companies/*/meta.md for dedup, uses WebSearch to surface new postings and WebFetch to inspect candidates, then delegates to /evaluate-position for scoring and filing.
---

# /job-search — weekly discovery sweep + monitoring recheck

Two-mode batch skill: surface new postings that fit the profile (discovery), and re-scan careers pages of companies the user flagged `monitoring: true` (recheck). Each candidate that survives the user's pick step gets scored and filed via the same logic as `/evaluate-position`.

## Inputs

- `userdata/profile.md` — read frontmatter for `target_titles`, `target_industries`, `geography`, `hard_filters`. Also read `tier_thresholds` so the discovery pre-filter can roughly estimate whether a posting is likely P0/P1/P2 before deep scoring.
- All existing `userdata/companies/*/meta.md` AND `userdata/companies/*/*/meta.md` — needed for dedup AND for the monitoring recheck pass.
- Optional flags:
  - `--discovery-only` — skip the monitoring recheck pass.
  - `--recheck-only` — skip discovery, run only the monitoring pass.
  - `--companies <Co1,Co2>` — when combined with `--recheck-only`, scope the recheck to specific companies.
  - No flags → run both passes, discovery first.

If `userdata/profile.md` is missing, tell the user to run `/setup` first; do not proceed.

## Mode 1: Discovery

Goal: surface a small (5-15) candidate list of postings the user hasn't seen, score the ones the user approves, file them.

### Step 1 — Derive search queries from profile

Build 2-4 search queries by combining one `target_titles` entry with one `target_industries` entry plus a geo qualifier from `geography`. Examples for a Maya-shaped profile:
- `"Head of Product" fintech London 2026`
- `"Senior PM" "consumer credit" Europe remote`
- `"Lead PM" "PLG SaaS" hybrid London`

Generate the list, show it to the user, ask: `Search with these queries, edit, or replace?` Accept their edits before searching.

### Step 2 — Run WebSearch and collect candidates

For each approved query, run a WebSearch. Collect URLs of job postings (filter out Glassdoor reviews, salary aggregators, news articles — keep only what looks like an actual JD page). De-dup by URL across queries.

### Step 3 — Dedup against existing pipeline

For each candidate URL, check whether the `(company, position)` pair is already in `userdata/companies/`. The check sequence:
1. Extract the company name from URL domain or page title (lightweight — Step 4 will refine).
2. If the company has no folder → not a dup; keep candidate.
3. If the company has a folder, glob its `meta.md` (or all role subfolders' `meta.md`) and compare `position` field against any role-name hint extractable from the URL/title.
4. If a match looks likely → mark as "possible dup, skip"; if uncertain → keep candidate and let the user decide in Step 5.

### Step 4 — Lightweight inspection

For each remaining candidate, WebFetch the JD page (or just its title + first 500 chars via the search result snippet, to save tokens). Extract: company name, position title, location. Build a one-row preview:

```
| # | Company | Position | Location | Tier-est |
|---|---|---|---|---|
| 1 | Klarna | Senior PM, Consumer Credit | London hybrid | P0? |
| 2 | Curve | Lead PM, Growth | Remote EU | P1? |
```

The `Tier-est` column is a quick eyeball estimate against target_titles / target_industries / hard_filters — not the real score. Use `P0?` / `P1?` / `P2?` / `skip?` to signal confidence.

### Step 5 — User picks

Show the preview table. Ask: `Which to evaluate fully? (comma-separated row numbers, "all", or "none")`. Accept any subset.

### Step 6 — Delegate to /evaluate-position

For each picked candidate, invoke the `/evaluate-position` workflow with the URL. That handles scoring, folder layout, dedup-on-write, and the meta.md + research-brief.md writes. Do not duplicate that logic here.

If multiple roles at the same company are picked in one batch, evaluate them sequentially — the 1→2 migration logic in `/evaluate-position` triggers naturally on the second one.

## Mode 2: Monitoring recheck

Goal: scan careers pages of companies the user flagged `monitoring: true` for new postings.

### Step 1 — Build the watchlist

Glob all `meta.md` files. Filter to those with `monitoring: true` in frontmatter. Group by company (some companies may have multiple roles, each flagged; the watchlist is per-company, not per-role).

For each company, attempt to derive its careers URL:
- If any `meta.md` for that company has a `link` field, infer the careers root from the URL pattern (e.g. `stripe.com/jobs/listings/foo` → `stripe.com/jobs`). Save the inferred root for re-use.
- If no link in any meta, ask the user: `What's <Company>'s careers page URL? (or skip)`.

### Step 2 — Fetch and scan

For each watchlist company, WebFetch its careers page. Extract role names + URLs. For each new role:
- Run the hard_filter gate (Step 1 from `/evaluate-position`, abbreviated).
- Match against `target_titles` (case-insensitive substring or close match).
- If it survives both, add to a candidate list.

### Step 3 — Dedup + present + delegate

Same as discovery Steps 3, 5, 6. Show one preview table per company (or one combined table tagged by source), let the user pick, delegate to `/evaluate-position`.

### Step 4 — Monitoring stays true

The `monitoring: true` flag on each company's existing `meta.md` is NEVER changed by `/job-search`. New roles added at a monitored company are filed under the company folder per the layout rule; the monitoring flag belongs to the existing meta entries, not the new ones. (The new role's `meta.md` gets `monitoring: false` by default — the user can flip it manually.)

## Combined-mode output

After both passes complete, print one consolidated summary:

```
Discovery: 12 candidates → 3 picked → 3 filed (2 P0, 1 P1).
Monitoring: 4 companies rechecked → 1 new role at Stripe (Consumer Credit Lead PM) → filed as P0.
Skipped: 8 candidates (5 dup, 3 hard-filter).
```

If no candidates surface in either pass, print: `No new candidates this week. Pipeline state unchanged. Consider running /strategy if you've been searching > 6 weeks with thin results.`

## Failure modes (handle explicitly)

- **WebSearch returns nothing useful.** Many job boards aggressively block search crawlers. If the result set is < 3 items across all queries, tell the user: `WebSearch returned thin results — most job boards block search. Paste 3-10 JD URLs you've gathered yourself and I'll run them through /evaluate-position.`
- **WebFetch blocked on a JD page (login wall, JS render, 403).** Skip the candidate, list it in the summary as `<Company> — <URL> — fetch failed (paste content if you want it scored)`.
- **Careers page can't be inferred from a `link`** (e.g. the link was a recruiter email). Ask the user once per company; if they skip, drop that company from this recheck pass (don't repeatedly re-ask in future runs — that's a user-fix-once issue).

## Dedup rule (recap, applies in both modes)

The `(company, position)` exact pair is never duplicated regardless of either entry's status. A `rejected` Stripe Lead PM stays as history forever; a new Stripe Lead PM posting next quarter would be flagged as dup (same company, same position) — the user gets to decide overwrite vs treat as separate (e.g. by appending a year suffix to position: `Lead PM, Growth (2026 reopen)`).

## What /job-search never does

- Never writes `meta.md` or `research-brief.md` directly — always delegates to `/evaluate-position`. Single source of writing-truth for company files.
- Never flips `monitoring`, `status`, or any field on EXISTING entries. The recheck pass is read-only against existing meta.md.
- Never auto-applies, sends outreach, or contacts companies. Pure discovery + filing.
- Never invents postings. If WebSearch / WebFetch fail, the user pastes URLs.

## Smoke test against the Maya example

Synthetic run against `userdata/examples/maya/`:

- **Discovery queries** built from Maya's profile: e.g. `"Head of Product" fintech London`, `"Lead PM" "consumer credit" Europe`. Show, accept, search.
- **Dedup**: any result mentioning Plaid Senior PM Consumer Credit → flagged as dup (already in pipeline). Stripe Lead PM Growth (rejected) → also flagged as dup; user can choose treat-as-new with renamed position.
- **Monitoring recheck**: Stripe is the only `monitoring: true` company in Maya's install. Infer careers URL from Stripe's existing `link` field, WebFetch it, scan for new roles matching `target_titles`. If a Consumer Credit role exists → preview row → user picks → `/evaluate-position` files it under `Stripe/<slug>/` (triggers 1→2 migration since Stripe currently has flat layout).
- **Combined summary** printed at end.

If WebSearch returns < 3 useful items for Maya's queries, fall through to the "paste URLs" prompt — that's a normal v1 outcome.
