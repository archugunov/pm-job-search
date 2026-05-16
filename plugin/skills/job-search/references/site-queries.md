# Site-scoped WebSearch queries for /job-search Discovery

The Discovery phase uses `site:` operators to constrain WebSearch results to **direct ATS posting pages**, sidestepping Glassdoor / Indeed / LinkedIn-jobs aggregators that block crawlers and return useless previews.

Without `site:`, a query like `senior product manager fintech London` returns mostly aggregator URLs. WITH `site:ashbyhq.com OR site:jobs.lever.co`, the same query returns direct JD URLs that WebFetch can actually read and `/evaluate-position` can score.

## The query bucket (8-10 queries per Discovery run)

Build queries by combining one element from each axis below. The Discovery subagent should generate 8-10 queries that COVER the user's `target_titles × target_industries × geography`, not all combinations.

### Axes

- **Title**: pulled from profile.md `target_titles`, expanded:
  - For "Head of Product" → also use `"lead product manager"`, `"group product manager"`
  - For "Senior PM" → also `"senior product manager"`, `"principal product manager"`
  - For "VP Product" → also `"vp of product"`, `"director of product"`
- **Industry / domain signal**: from profile.md `target_industries`, plus generic shape signals (`PLG`, `B2C`, `"product-led growth"`, `subscriptions`, `marketplace`, `mobile`, `creator tools`).
- **Geography**: from profile.md `geography.mode_detail` or `city`:
  - on-site/hybrid → use the city name (e.g. `London`, `Berlin`, `Amsterdam`, `Paris`)
  - remote → use `remote Europe`, `remote EMEA`, `remote UK`, `Germany remote` etc. depending on `mode_detail`
- **Site set**: always include `site:ashbyhq.com OR site:jobs.lever.co` minimum. Add `site:job-boards.greenhouse.io` and `site:job-boards.eu.greenhouse.io` for broader coverage. `site:apply.workable.com` and `site:careers.ashbyhq.com` are bonus.

### Template

```
"<title-1>" OR "<title-2>" [OR "<title-3>"]  site:<ats-1> [OR site:<ats-2>]  <geo>  [<industry-signal>]
```

### Worked examples (for a Maya-shaped profile: Head of Product / Lead PM / Senior PM, fintech / consumer credit / PLG SaaS, London hybrid or EMEA remote)

```
1.  "head of product" OR "lead product manager" OR "group product manager" site:ashbyhq.com London OR remote Europe
2.  "senior product manager" OR "principal product manager" site:ashbyhq.com PLG OR consumer credit OR fintech remote
3.  "head of product" OR "lead product manager" OR "senior product manager" site:jobs.lever.co London OR remote Europe
4.  "head of product" OR "senior product manager" site:job-boards.greenhouse.io London OR remote
5.  "head of product" OR "senior product manager" site:job-boards.eu.greenhouse.io
6.  "head of product" OR "lead product manager" OR "senior product manager" site:apply.workable.com London OR remote
7.  "head of product" OR "lead product manager" PLG OR "product-led growth" OR consumer credit site:ashbyhq.com OR site:jobs.lever.co remote
8.  "senior product manager" consumer credit OR fintech site:ashbyhq.com OR site:jobs.lever.co
9.  "head of product" OR "senior product manager" London site:careers.ashbyhq.com OR site:jobs.ashbyhq.com
10. "head of product" OR "founding product manager" OR "first product hire" Series A OR Series B "small team" London OR remote site:ashbyhq.com OR site:jobs.lever.co
```

### Generalisation rules

- Always anchor at least one query to founding-PM / Series A-B language (#10 above) — those signal the "small-team Head of Product" shape that's hard to find otherwise.
- Always include one query that pairs `target_industries` with the broadest site set (#7 above) — for breadth.
- If the user's profile only has `target_industries` (no specific shape language), drop queries #1, #2 and use the saved bandwidth for two more industry-specific ones.

## Result extraction

Each WebSearch result has `title`, `url`, and a snippet. Extract `{title, company}` from the result title using regex:

```
(.+?)(?:\s*[@|—–\-]\s*|\s+at\s+)(.+?)$
```

- LHS = role title
- RHS = company name

The ATS URL gives the canonical slug; use it for dedup-by-URL.

## Result filtering (Discovery subagent does this before writing output)

After running all 8-10 queries and merging results:

1. Dedup by URL (lowercase, strip `?...` and `#...`, remove trailing `/`).
2. Title must match at least one PM keyword (see `ats-apis.md` for the title-match set).
3. Drop titles containing negative-filter words (also in `ats-apis.md`).
4. Drop candidates whose normalised `(company, role)` pair OR `url` matches the exclusion set from `/tmp/pmjs-exclusion.json`.

The expected post-filter count is 10-30 candidates per Discovery run. If you have fewer than 5, the user's queries are too narrow — widen geography or industry on the next run.

## What WebSearch will NOT return

Even with `site:` operators, some companies aren't reachable:
- Companies using custom careers pages (Workday, in-house portals) — they're invisible to WebSearch's index of these specific domains.
- Brand-new postings (< 24-48 hrs old) — search indexing has lag.
- Companies whose ATS hides postings from search engines via `robots.txt`.

For these, the user's only path is direct knowledge or the `monitoring: true` recheck cycle (which uses the ATS APIs in `ats-apis.md`).
