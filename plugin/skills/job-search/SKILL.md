---
name: job-search
description: This skill should be used when the user asks to "/job-search", "weekly job search", "find new roles", "discover postings", "recheck monitoring companies", "any new jobs at <companies>", or wants a sweep of new job postings matching their profile plus a recheck of companies they're tracking. Three-phase architecture: pre-flight extracts dedup sets from existing meta.md, Phase 1 runs Recheck-A / Recheck-B / Discovery in parallel via subagents (Recheck uses public ATS APIs — Ashby GraphQL, Greenhouse REST, Lever REST; Discovery uses site:-scoped WebSearch to skip aggregators, seeded by Companies of interest in profile.md), Phase 2 scores every surviving candidate and auto-files them directly (writes meta.md + research-brief.md with status: new, no manual pick step). Optional Playwright MCP for link-liveness verification.
---

# /job-search — three-phase discovery and monitoring sweep

Architecture lifted from the predecessor workflow with two changes: storage is md files (not Notion); Playwright is optional (not required). Three phases: pre-flight, parallel work, final merge.

**Voice:** every prompt (search-query review, recheck-failure handling) and the chat summary follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Phase 2 auto-files every surviving candidate (no pick step, no preview table). Run summaries and failure messages follow TONE.md — plain prose, no fenced blocks.

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

Build the exclusion set from two sources so a role stays suppressed even after its company folder is deleted:

1. **Existing meta.md.** Walk both glob patterns and collect every role's `(company, position)` pair plus every non-empty `link`.
2. **The seen-ledger** at `userdata/outputs/seen-roles.jsonl` (append-only, one JSON object per line). If it exists, read every line and fold its `strict_key` / `base_key` / `url_key` into the set. This is what remembers a role the user archived by deleting its folder rather than marking it `not_interested`. If the file is absent, skip — first run creates it in Phase 2.

Derive the identity keys (`company_key`, `strict_key`, `base_key`, `url_key`) for every source role using `${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md` — the single authority both this skill and `/evaluate-position` share. Do not re-implement the rules here.

Output schema:

```json
{
  "exclusion_pairs": [{"company_key": "plaid", "strict_key": "plaid senior product manager consumer credit", "base_key": "plaid senior product manager"}, ...],
  "exclusion_urls": ["https://example.com/plaid-jobs/spm-consumer-credit", ...]
}
```

Match rules (hard duplicate → drop silently; soft duplicate → surface as a likely repeat; new → file) are defined in `${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md` and applied in Phase 2. Same company + a genuinely different position is never a hard duplicate.

### B. `/tmp/pmjs-recheck.json`

Build the recheck watchlist. Include any company that has `monitoring: true` on any of its meta.md entries, OR has any role with status `new` / `to_apply`. Exclude companies whose only roles are in `applied` / `interviewing` / `offer` / `rejected` / `not_interested` AND not monitored.

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

## Phase 2 — Score and file every surviving candidate (no manual step)

1. Read all three Phase 1 output files.
2. Re-read the existing companies/*/meta.md (the recheck agents may have surfaced new candidates that overlap with discovery — re-derive the exclusion set to be safe).
3. With `--with-playwright`, verify P0/P1 candidate URLs are live (`browser_navigate` + `browser_snapshot`; expired = redirect / "no longer available" / content < ~300 chars). Without Playwright, skip verification and tag each candidate `link_verified: false`.

For each candidate from Phase 1 (Discovery) and the Recheck passes:

1. **Dedup** using `${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md` against the exclusion set (existing meta.md + the seen-ledger):
   - **Hard duplicate** (`url_key` OR `strict_key` matches): if a matching meta.md entry exists, touch its `last_seen:`. Skip filing. Do not duplicate.
   - **Soft duplicate** (`base_key` matches at the same company, but not `url_key`/`strict_key`): do NOT file. Add it to a `skipped_repeats` list (title + link) for the run summary, so the user can ask to file it if it's a genuinely distinct role. Same company + different position still reaches `/evaluate-position`'s 1→2 migration when the user opts in.
   - **New** (no match): proceed to score and file.
2. **Record every candidate in the seen-ledger.** For each candidate evaluated in this step (filed, hard-dup, or soft-dup), if its `strict_key` is not already present in `userdata/outputs/seen-roles.jsonl`, append one line: `{"company_key": ..., "strict_key": ..., "base_key": ..., "url_key": ..., "raw_title": <original position>, "first_surfaced": <today ISO>}`. This is what stops the same role resurfacing after its folder is deleted. Append once per key — never rewrite existing lines.
3. Score each new candidate using the tier rubric in `userdata/profile.md` (same logic as `/evaluate-position`). If scoring fails (JD fetch error, malformed page), file a stub with `tier: unscored` and continue — do not abort the run.
4. Write `userdata/companies/<Co>/[<slug>/]meta.md` and `research-brief.md` with `status: new`. Frontmatter of `meta.md` must include `position:` (never `role:`), a `status:` from the enum, and `link:` set to the live JD URL. `research-brief.md` must include a `**Source:** <url>` line as the first content line after the H1.
5. **Validation gate (mandatory, before the run summary).** Re-read every meta.md just written and assert against `${CLAUDE_PLUGIN_ROOT}/schemas/meta.md.schema.md`: required keys present (`company`, `position`, `status`, `link`); `status` in the enum; non-empty `link` starts with `http(s)`; no forbidden keys (`role:`, `target_date:`); `tier` (if present) is one of `P0` / `P1` / `P2` / `unscored`. On any failure, **rewrite the offending field from the candidate data** (e.g. rename a stray `role:` to `position:`, replace an invented `link:` with the real one or blank-with-comment) rather than trusting the sub-agent output. Never emit a placeholder like `(url not captured)` — if the link is genuinely unknown, leave `link:` blank with an explanatory comment per the schema.

## Recheck subagent prompt

You are running a recheck batch (`{BATCH_ID}`) for a weekly job sweep.

You receive `{BATCH}` — JSON array of `{company, link, tier}` entries.

For each company, extract the ATS slug from `link` (or guess from company name if no link). Detailed slug-extraction and API-call instructions are in `references/ats-apis.md` — read that file before processing any company.

**PM title keywords** (case-insensitive substring match): pulled from the user's `target_titles` in profile.md, expanded to include common variants. For a Maya-shaped profile (Head of Product, Lead PM, Senior PM) the match set is:
`head of product`, `lead product manager`, `lead pm`, `group product manager`, `group pm`, `senior product manager`, `senior pm`, `principal product manager`, `principal pm`, `director of product`, `staff product manager`.

**Negative filter** (skip titles containing): `junior`, `intern`, `associate`, `.net`, `java`, `blockchain`, `data engineer`, `software engineer`, `qa`, `sales`.

For each matched role, emit one entry to the output:

```json
{"company": "Plaid", "position": "Head of Product, Risk", "link": "https://jobs.lever.co/plaid/...", "source_tier": "P0"}
```

**Output contract (do not deviate):** every entry has exactly these keys — `company` (canonical casing), `position` (the exact JD title — the key is `position`, NEVER `role`), `link` (a live `http(s)` URL), `source_tier` (one of `P0` / `P1` / `P2`). Do not invent companies, positions, or links — emit only roles the ATS API actually returned. If a field is unknown, omit the entry rather than guessing.

Write all entries to `/tmp/pmjs-recheck-{BATCH_ID}.json`.

Return one line: `Recheck-{BATCH_ID}: checked N companies, found K new PM roles.`

## Discovery subagent prompt

You are running the discovery phase of a weekly job sweep.

**Seed Discovery with `## Companies of interest` from `userdata/profile.md`.** If that section exists and has entries, include those companies as additional discovery targets (e.g. `site:<company>.com/careers senior product manager`). Treat them as candidates like any other — they still go through scoring and dedup. After the first run, they remain in `profile.md` but discovery does not need to re-treat them as seeds — they'll be tracked under `userdata/companies/` going forward.

You receive `exclusion_pairs` and `exclusion_urls` from `/tmp/pmjs-exclusion.json`. Drop any candidate whose normalised `url_key` OR `(company, position)` `strict_key` matches (keys per `${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md`).

You also receive the user's `target_titles`, `target_industries`, `geography.mode` + `mode_detail` from profile.md, and the location preference (city name or "remote").

Build and run 8-10 WebSearch queries that combine titles, industries, and geography, ALL scoped via `site:` operators to public ATS job-board domains. Domain set: `ashbyhq.com`, `jobs.lever.co`, `jobs.eu.lever.co`, `job-boards.greenhouse.io`, `job-boards.eu.greenhouse.io`, `apply.workable.com`, `careers.ashbyhq.com`. Full query templates in `references/site-queries.md`.

Each query returns search results — extract `{title, url, company}` from each result. Title regex: `(.+?)(?:\s*[@|—–\-]\s*|\s+at\s+)(.+?)$`.

Filter:
1. Dedup by URL across queries (case-insensitive).
2. Title must contain at least one PM keyword from the title-match set.
3. Skip titles containing any negative-filter word.
4. Apply the exclusion normalisation (`${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md`); drop if `url_key` OR `strict_key` matches.

Write filtered results to `/tmp/pmjs-discovery.json`:

```json
[{"company": "Acme", "position": "Head of Product", "url": "https://jobs.ashbyhq.com/acme/..."}]
```

**Output contract (do not deviate):** every entry has exactly `company`, `position` (the JD title — the key is `position`, NEVER `role` or `title`), and `url` (the live `http(s)` link the search returned). Emit only roles that appeared in real search results — never invent a company, position, or URL. If the title regex fails to split a result cleanly, drop it rather than guessing a company or position.

Return one line: `Discovery: found N candidates across M queries.`

## Final merge prompt (Phase 2, main conversation)

After both phases complete:

1. Read `/tmp/pmjs-recheck-a.json`, `/tmp/pmjs-recheck-b.json`, `/tmp/pmjs-discovery.json`. Every entry keys `position` (not `role`).
2. Merge discovery + recheck-a + recheck-b into one candidate list. Dedup by `url_key` again (`${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md`).
3. For each candidate, run a light tier estimate: walk profile.md's `tier_weights` rubric mentally — score 1-3 per dimension based on the JD title + URL + (optionally) a lightweight WebFetch of the first 500 chars of the page. Sum, apply `tier_thresholds`, get a `P0?` / `P1?` / `P2?` / `skip?` tag.
4. Discard `P2?` unless fewer than 3 P0/P1 total are surviving.
5. If `--with-playwright` and Playwright MCP is available, navigate each P0?/P1? URL, check liveness (see "Playwright integration" below). Update or null the link.
6. For each surviving candidate, apply the full auto-file logic from Phase 2 above: dedup (hard/soft) → record in the seen-ledger → score → write `meta.md` + `research-brief.md` with `status: new` → validation gate. The 1→2 folder migration for existing companies follows the same rules as `/evaluate-position`.

## Playwright integration (optional)

If `--with-playwright` AND the Playwright MCP is installed in the user's Claude Code config:

- Use `browser_navigate` to load each P0/P1 candidate URL.
- Use `browser_snapshot` to read the rendered page.
- **Active:** job title visible in main content + Apply/Submit button present → `link_verified: true`.
- **Expired indicators:** redirect to `/jobs` root with path < 8 chars; URL has `?error=true`; page contains "no longer available" / "position has been filled" / "this job has expired"; content < ~300 chars → `link_verified: false`, blank the link.

If Playwright MCP is NOT installed (or `--with-playwright` not passed), skip verification entirely. Set `link_verified: false` on every candidate — the user can verify manually before applying.

NEVER fail the whole skill because Playwright is unavailable. It's a nice-to-have.

## Output to chat

**Run summary (chat output):**

Plain prose (TONE.md Rule B — no fenced code blocks, no key-value dumps). Template:

> "Filed N new roles. <tier-1 count> tier-1 (<top names>), <tier-2 count> tier-2. All set to status `new`. <Stub count, if any> couldn't be scored automatically — listed below.
>
> <If stubs exist, list them as bullets with their links.>
>
> <If any soft-duplicates were skipped: "Skipped as likely repeats (<count>): <Company> — <Position> — <url>". These share a base title with a role you've already seen; say 'file <Company>' if it's genuinely a different role.>
>
> Open the dashboard to triage — or tell me here which to mark `to apply`, `not interested`, or archive."

Each application row printed in chat (when the user asks to see roles, when stubs are listed, etc.) includes the JD URL inline. Format: `- <Company> — <Position> — <status> — <url>`. Long URLs are fine; do not shorten or wrap.

Close the chat output with a context-aware next-step nudge per `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. For a fresh filing pass, the typical nudge is to open `/pm-job-search:dashboard`.

If nothing surfaces: "No new roles this week. Pipeline state unchanged."

## Dedup rule (recap)

Identity keys and match rules live in `${CLAUDE_PLUGIN_ROOT}/references/dedup-normalization.md`; this is the recap. A candidate is matched against the union of existing meta.md entries and the seen-ledger (`userdata/outputs/seen-roles.jsonl`), so a role stays suppressed even after its company folder is deleted.

- **Hard duplicate** — `url_key` or `strict_key` matches. Never duplicated, regardless of the existing entry's status: a `rejected` Stripe Lead PM stays as history, and the same Lead PM posting resurfacing next quarter is dropped silently (touch `last_seen:`). The seen-ledger records every candidate ever surfaced so this holds across deletions.
- **Soft duplicate** — same `base_key` at the same company but a different qualifier (e.g. "Lead PM, Payments" vs "Lead PM — Growth"). Not filed automatically, but surfaced under "Skipped as likely repeats" so a genuinely distinct second role is never silently buried.
- Same company + a genuinely different position = NOT a duplicate. Goes through `/evaluate-position`'s 1→2 migration logic.

## What /job-search never does

- Never flips `monitoring`, `status`, or any other field on existing entries — the only write to an existing meta.md is touching `last_seen:` when a dedup match is found.
- Never rewrites the seen-ledger — it is append-only. New keys are added; existing lines are never edited or removed.
- Never auto-applies or sends outreach.
- Never requires Playwright. Optional only.
- Never invents postings, companies, positions, or links. If ATS APIs return nothing and WebSearch is thin, the run is a no-op. The Phase 2 validation gate rewrites any field a sub-agent drifted (e.g. `role:` → `position:`) rather than trusting it.

## Additional resources

- **`references/ats-apis.md`** — full API specs for Ashby (GraphQL), Greenhouse (REST), Lever (REST). Slug extraction rules. Read before processing any company in a Recheck batch.
- **`references/site-queries.md`** — the query-bucket template, 8-10 standard queries derived from profile fields, how to mix titles × industries × geography.

## Smoke test against the Maya example

- **Pre-flight**: scans Maya's 2 companies (Plaid, Stripe). Exclusion set from meta.md — `strict_key`s `plaid senior product manager consumer credit`, `stripe lead product manager growth` (`base_key`s `plaid senior product manager`, `stripe lead product manager`), plus each meta.md `link` as a `url_key`. Then folds in `userdata/outputs/seen-roles.jsonl` if present (absent on a first run — created in Phase 2). Recheck watchlist: Stripe (monitoring: true) + Plaid (status:interviewing — only included if it has another non-active role; in Maya's case it doesn't). Watchlist = `[Stripe]`. Tier P1.
- **Second run (no new postings)**: the Phase 1 candidates all match a `strict_key` in the seen-ledger from run 1 → all hard-duplicates → "No new roles this week." A reposted Stripe Lead PM with a reworded title ("Lead PM — Growth EMEA") shares the `stripe lead product manager` base_key → surfaced under "Skipped as likely repeats", not filed as new.
- **Recheck on Stripe**: extract slug from Stripe meta link (`example.com/stripe-jobs/...` → can't infer ATS, guess `stripe`); try Greenhouse → 200, get jobs list. Filter to PM keywords. Any new Consumer Credit role → emit candidate.
- **Discovery**: 8-10 site:-scoped queries built from Maya's profile (`"head of product" fintech London site:ashbyhq.com`, etc.). Returns direct ATS URLs, not aggregator pages. Filter and emit candidates.
- **Phase 2**: merge, light tier-estimate, auto-file every surviving candidate (dedup → score → write meta.md + research-brief.md with status: new). Print plain-prose run summary to chat.
