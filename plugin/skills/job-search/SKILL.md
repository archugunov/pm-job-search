---
name: job-search
description: This skill should be used when the user asks to "/job-search", "weekly job search", "find new roles", "discover postings", "recheck monitoring companies", "any new jobs at <companies>", or wants a sweep of new job postings matching their profile plus a recheck of companies they're tracking. Three-phase architecture: pre-flight extracts dedup sets from existing meta.md, Phase 1 runs Recheck-A / Recheck-B / Discovery in parallel via subagents (Recheck uses public ATS APIs — Ashby GraphQL, Greenhouse REST, Lever REST; Discovery uses site:-scoped WebSearch to skip aggregators), Phase 2 scores candidates and delegates filing to /evaluate-position. Optional Playwright MCP for link-liveness verification.
---

# /job-search — three-phase discovery and monitoring sweep

Architecture lifted from the predecessor workflow with two changes: storage is md files (not Notion); Playwright is optional (not required). Three phases: pre-flight, parallel work, final merge.

**Voice:** every prompt (search-query review, candidate pick, recheck-failure handling) and the chat summary follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — surface candidates with a short preview table, accept "all"/"none" shortcuts, don't make the user evaluate every row.

## Inputs

- `userdata/profile.md` — `target_titles`, `target_industries`, `geography`, `hard_filters`, `tier_thresholds`.
- All `userdata/companies/*/meta.md` AND `userdata/companies/*/*/meta.md` — needed for the exclusion sets AND for the monitoring watchlist.
- Optional flags:
  - `--no-parallel` — run Recheck and Discovery sequentially in the main conversation, no subagents (slower but easier to debug).
  - `--discovery-only` / `--recheck-only` — skip the other phase.
  - `--companies <Co1,Co2>` — when combined with `--recheck-only`, scope the recheck.
  - `--with-playwright` — use Playwright MCP for link-liveness verification in Phase 2. If the MCP isn't installed, fall back gracefully and note `link_verified: false`.

If `userdata/profile.md` is missing, tell the user to run `/setup` first; do not proceed.

## Phase 0 — Pre-flight (always sequential, in main conversation)

Produce two artefacts on disk for the parallel agents to consume:

### A. `/tmp/pmjs-exclusion.json`

Walk both glob patterns and collect every role's `(company, position)` pair plus every non-empty `link`. Normalise each:

- **company**: lowercase, strip punctuation, collapse whitespace.
- **position**: same plus the substitutions `pms` → `product managers`, `pm` → `product manager` (catches the "Senior PM" vs "Senior Product Manager" duplicate).
- **link**: lowercase, strip `?...` and `#...`, remove trailing `/`.

Output schema:

```json
{
  "exclusion_pairs": [{"company": "plaid", "position": "senior product manager consumer credit"}, ...],
  "exclusion_urls": ["https://example.com/plaid-jobs/spm-consumer-credit", ...]
}
```

URL match alone is enough to drop a candidate (different title parse, same role). Pair match alone is enough (same role, no link). Either match = dedup. Same company + different position is NOT a duplicate.

### B. `/tmp/pmjs-recheck.json`

Build the recheck watchlist. Include any company that has `monitoring: true` on any of its meta.md entries, OR has any role with status `new` / `to_apply`. Exclude companies whose only roles are in `applied` / `interviewing` / `offer` / `rejected` / `closed` AND not monitored.

For each company, capture: name, primary `link` (most recent meta.md's `link` field, used to infer the ATS slug), highest tier across its roles (`P0` > `P1` > `P2`).

Sort by tier (P0 first, P1, P2, unranked last). Split in half: first half → batch `a`, second half → batch `b`.

Output schema (one file with both batches):

```json
{
  "recheck_a": [{"company": "Plaid", "link": "https://...", "tier": "P0"}, ...],
  "recheck_b": [{"company": "Stripe", "link": "https://...", "tier": "P1"}, ...]
}
```

Cap the total watchlist at 40 companies per run (P0/P1 prioritised).

## Phase 1 — Parallel work (3 subagents, run in one message)

Unless `--no-parallel`, dispatch three Agent calls in a SINGLE message with `run_in_background: true`:

1. **Recheck-A** — uses the "Recheck subagent prompt" below with `{BATCH}` = `recheck_a`, `{BATCH_ID}` = `a`. Writes `/tmp/pmjs-recheck-a.json`.
2. **Recheck-B** — same prompt, `{BATCH}` = `recheck_b`, `{BATCH_ID}` = `b`. Writes `/tmp/pmjs-recheck-b.json`.
3. **Discovery** — uses the "Discovery subagent prompt" below with the pre-flight exclusion data and the profile-derived query bucket. Writes `/tmp/pmjs-discovery.json`.

Wait for all three to finish (notifications) before moving to Phase 2. With `--no-parallel`, just run each step inline.

## Phase 2 — Merge, score, verify, file (main conversation)

1. Read all three Phase 1 output files.
2. Re-read the existing companies/*/meta.md (the recheck agents may have surfaced new candidates that overlap with discovery — re-derive the exclusion set to be safe).
3. For each candidate, run the scoring rubric (the same logic `/evaluate-position` uses) — but lightly, to assign a rough tier estimate. Final scoring + write happens via `/evaluate-position` per candidate.
4. With `--with-playwright`, verify P0/P1 candidate URLs are live (`browser_navigate` + `browser_snapshot`; expired = redirect / "no longer available" / content < ~300 chars). Without Playwright, skip verification and tag each candidate `link_verified: false`.
5. Show a preview table to the user grouped by tier-estimate. Ask which to file.
6. For each picked candidate, invoke `/evaluate-position` with the URL — that handles real scoring, folder layout, and writing. /job-search never writes to companies/<Co>/ directly.

## Recheck subagent prompt

You are running a recheck batch (`{BATCH_ID}`) for a weekly job sweep.

You receive `{BATCH}` — JSON array of `{company, link, tier}` entries.

For each company, extract the ATS slug from `link` (or guess from company name if no link). Detailed slug-extraction and API-call instructions are in `references/ats-apis.md` — read that file before processing any company.

**PM title keywords** (case-insensitive substring match): pulled from the user's `target_titles` in profile.md, expanded to include common variants. For a Maya-shaped profile (Head of Product, Lead PM, Senior PM) the match set is:
`head of product`, `lead product manager`, `lead pm`, `group product manager`, `group pm`, `senior product manager`, `senior pm`, `principal product manager`, `principal pm`, `director of product`, `staff product manager`.

**Negative filter** (skip titles containing): `junior`, `intern`, `associate`, `.net`, `java`, `blockchain`, `data engineer`, `software engineer`, `qa`, `sales`.

For each matched role, emit one entry to the output:

```json
{"company": "Plaid", "role": "Head of Product, Risk", "link": "https://jobs.lever.co/plaid/...", "source_tier": "P0"}
```

Write all entries to `/tmp/pmjs-recheck-{BATCH_ID}.json`.

Return one line: `Recheck-{BATCH_ID}: checked N companies, found K new PM roles.`

## Discovery subagent prompt

You are running the discovery phase of a weekly job sweep.

You receive `exclusion_pairs` and `exclusion_urls` from `/tmp/pmjs-exclusion.json`. Drop any candidate whose normalised URL OR `(company, role)` pair matches.

You also receive the user's `target_titles`, `target_industries`, `geography.mode` + `mode_detail` from profile.md, and the location preference (city name or "remote").

Build and run 8-10 WebSearch queries that combine titles, industries, and geography, ALL scoped via `site:` operators to public ATS job-board domains. Domain set: `ashbyhq.com`, `jobs.lever.co`, `jobs.eu.lever.co`, `job-boards.greenhouse.io`, `job-boards.eu.greenhouse.io`, `apply.workable.com`, `careers.ashbyhq.com`. Full query templates in `references/site-queries.md`.

Each query returns search results — extract `{title, url, company}` from each result. Title regex: `(.+?)(?:\s*[@|—–\-]\s*|\s+at\s+)(.+?)$`.

Filter:
1. Dedup by URL across queries (case-insensitive).
2. Title must contain at least one PM keyword from the title-match set.
3. Skip titles containing any negative-filter word.
4. Apply the exclusion normalisation; drop if URL OR pair matches.

Write filtered results to `/tmp/pmjs-discovery.json`:

```json
[{"title": "Head of Product", "url": "https://jobs.ashbyhq.com/acme/...", "company": "Acme"}]
```

Return one line: `Discovery: found N candidates across M queries.`

## Final merge prompt (Phase 2, main conversation)

After both phases complete:

1. Read `/tmp/pmjs-recheck-a.json`, `/tmp/pmjs-recheck-b.json`, `/tmp/pmjs-discovery.json`.
2. Merge discovery + recheck-a + recheck-b into one candidate list. Dedup by URL again.
3. For each candidate, run a light tier estimate: walk profile.md's `tier_weights` rubric mentally — score 1-3 per dimension based on the JD title + URL + (optionally) a lightweight WebFetch of the first 500 chars of the page. Sum, apply `tier_thresholds`, get a `P0?` / `P1?` / `P2?` / `skip?` tag.
4. Discard `P2?` unless fewer than 3 P0/P1 total are surviving.
5. If `--with-playwright` and Playwright MCP is available, navigate each P0?/P1? URL, check liveness (see "Playwright integration" below). Update or null the link.
6. Build preview table:

```
| # | Company | Role | Tier? | Source | Link verified? |
|---|---|---|---|---|---|
| 1 | Lendable | Head of Product | P0? | site:ashbyhq.com | yes |
| 2 | OakNorth | Group PM, Credit | P0? | site:greenhouse.io | unverified (no Playwright) |
| 3 | Plaid (existing) | Lead PM, Risk Platform | P1? | ATS recheck | yes |
```

7. Ask: `Which to file? (numbers, "all", "none")`.
8. For each picked candidate, invoke `/evaluate-position` (or, in batch mode, invoke per-candidate sequentially). The 1→2 folder migration for existing companies happens naturally inside `/evaluate-position`.

## Playwright integration (optional)

If `--with-playwright` AND the Playwright MCP is installed in the user's Claude Code config:

- Use `browser_navigate` to load each P0/P1 candidate URL.
- Use `browser_snapshot` to read the rendered page.
- **Active:** job title visible in main content + Apply/Submit button present → `link_verified: true`.
- **Expired indicators:** redirect to `/jobs` root with path < 8 chars; URL has `?error=true`; page contains "no longer available" / "position has been filled" / "this job has expired"; content < ~300 chars → `link_verified: false`, blank the link.

If Playwright MCP is NOT installed (or `--with-playwright` not passed), skip verification entirely. Set `link_verified: false` on every candidate — the user can verify manually before applying.

NEVER fail the whole skill because Playwright is unavailable. It's a nice-to-have.

## Output to chat

After Phase 2 completes:

```
Job sweep — <YYYY-MM-DD>
  Discovery: <N> candidates from <M> site:-scoped queries
  Monitoring recheck: <K> companies checked, <L> new roles found
  After dedup + filters: <X> surviving candidates
  Filed via /evaluate-position: <Y> roles (<p0> P0, <p1> P1)
```

If nothing surfaces: `No new roles this week. Pipeline state unchanged.`

## Dedup rule (recap)

The `(company, position)` exact pair is never duplicated, regardless of either entry's status. A `rejected` Stripe Lead PM stays as history; a new Stripe Lead PM posting next quarter is flagged as dup. URL match is the safety net for when title/company parsing slips.

Same company + different position = NOT a duplicate. Goes through `/evaluate-position`'s 1→2 migration logic.

## What /job-search never does

- Never writes `meta.md` or `research-brief.md` directly — delegates to `/evaluate-position`.
- Never flips `monitoring`, `status`, or any field on existing entries (read-only against existing meta.md).
- Never auto-applies or sends outreach.
- Never requires Playwright. Optional only.
- Never invents postings. If ATS APIs return nothing and WebSearch is thin, the run is a no-op.

## Additional resources

- **`references/ats-apis.md`** — full API specs for Ashby (GraphQL), Greenhouse (REST), Lever (REST). Slug extraction rules. Read before processing any company in a Recheck batch.
- **`references/site-queries.md`** — the query-bucket template, 8-10 standard queries derived from profile fields, how to mix titles × industries × geography.

## Smoke test against the Maya example

- **Pre-flight**: scans Maya's 2 companies (Plaid, Stripe). Exclusion pairs: `(plaid, senior product manager consumer credit)`, `(stripe, lead product manager growth)`. URLs from each meta.md `link`. Recheck watchlist: Stripe (monitoring: true) + Plaid (status:interviewing — only included if it has another non-active role; in Maya's case it doesn't). Watchlist = `[Stripe]`. Tier P1.
- **Recheck on Stripe**: extract slug from Stripe meta link (`example.com/stripe-jobs/...` → can't infer ATS, guess `stripe`); try Greenhouse → 200, get jobs list. Filter to PM keywords. Any new Consumer Credit role → emit candidate.
- **Discovery**: 8-10 site:-scoped queries built from Maya's profile (`"head of product" fintech London site:ashbyhq.com`, etc.). Returns direct ATS URLs, not aggregator pages. Filter and emit candidates.
- **Phase 2**: merge, light tier-estimate, ask user to pick, delegate each pick to `/evaluate-position`.
