# ATS APIs — public, no-auth endpoints used by /job-search recheck

Three job-board APIs cover the majority of startup hiring: Ashby, Greenhouse, Lever. All three expose **public, unauthenticated endpoints** that return the company's current open roles as structured JSON. No tokens, no MCP, no scraping.

Use these in the Recheck phase of `/job-search`. Slug extraction first, then API call.

## Slug extraction

For each company in the recheck batch, derive the ATS slug from its `meta.md.link` field:

| URL pattern | Platform | Slug |
|---|---|---|
| `jobs.ashbyhq.com/{slug}/...` | Ashby | `{slug}` |
| `jobs.lever.co/{slug}/...` | Lever | `{slug}` |
| `jobs.eu.lever.co/{slug}/...` | Lever (EU) | `{slug}` |
| `job-boards.greenhouse.io/{slug}/...` | Greenhouse | `{slug}` |
| `job-boards.eu.greenhouse.io/{slug}/...` | Greenhouse (EU) | `{slug}` |
| `boards.greenhouse.io/{slug}/...` | Greenhouse (legacy) | `{slug}` |

For custom domains (e.g. `careers.acme.com`) or empty links, **guess the slug** from the company name:
- lowercase
- spaces → hyphens
- drop special chars (e.g. "Happy Scribe" → `happyscribe`, "n8n" → `n8n`, "tl;dv" → `tldv`)
- try the slug across all three APIs in order: Ashby → Greenhouse → Lever
- stop at the first HTTP 200 with valid job data
- if all three return 404 / 500 / non-JSON, mark the company as "ATS not detected" and skip

## Ashby — GraphQL POST

```
POST https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams
Content-Type: application/json

Body:
{
  "operationName": "ApiJobBoardWithTeams",
  "variables": {"organizationHostedJobsPageName": "{slug}"},
  "query": "{ jobBoard { jobPostings { id title } } }"
}
```

Response shape:
```json
{
  "data": {
    "jobBoard": {
      "jobPostings": [
        {"id": "abc-123", "title": "Head of Product"},
        ...
      ]
    }
  }
}
```

Build URLs as: `https://jobs.ashbyhq.com/{slug}/{id}`.

Note: Ashby's GraphQL endpoint may return an empty `jobPostings` array if the company recently switched ATS or paused hiring. Don't error — just emit zero candidates for that company.

## Greenhouse — REST GET

```
GET https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
```

Response shape:
```json
{
  "jobs": [
    {
      "title": "Head of Product",
      "absolute_url": "https://job-boards.greenhouse.io/{slug}/jobs/xxxxxxx",
      "location": {"name": "Remote — EMEA"},
      "departments": [{"name": "Product"}]
    },
    ...
  ]
}
```

Use `jobs[].title` and `jobs[].absolute_url`.

EU variant: `https://boards-api.eu.greenhouse.io/v1/boards/{slug}/jobs`.

## Lever — REST GET

```
GET https://api.lever.co/v0/postings/{slug}?mode=json
```

Response shape (array, not object):
```json
[
  {
    "text": "Head of Product",
    "hostedUrl": "https://jobs.lever.co/{slug}/xxxxxxx",
    "categories": {
      "location": "Remote — Europe",
      "team": "Product"
    }
  },
  ...
]
```

Use `[].text` and `[].hostedUrl`.

EU variant: same endpoint, different URL pattern in `hostedUrl`.

## Combined fallback pseudocode

```
function fetch_ats_jobs(company, link):
    slug = extract_slug_from_link(link) || guess_slug_from_name(company.name)

    if slug came from explicit ATS URL:
        platform = inferred from URL
        return call_platform(platform, slug)

    for platform in [ashby, greenhouse, lever]:
        result = call_platform(platform, slug)
        if result.status == 200 and result.jobs.length > 0:
            return result

    return null   // ATS not detected
```

## Filter the job list

After fetching, run this filter on each job title:

**Title-match set** (case-insensitive substring — at least ONE must match):
- `head of product`
- `lead product manager`, `lead pm`
- `group product manager`, `group pm`
- `senior product manager`, `senior pm`
- `principal product manager`, `principal pm`
- `director of product`
- `staff product manager`

**Negative filter** (drop title if it contains ANY of these):
- `junior`, `intern`, `associate`
- `.net`, `java`, `blockchain`, `data engineer`, `software engineer`, `qa`, `sales`

Customise the title-match set based on the user's `target_titles` in profile.md — those are the canonical role levels the user is hunting. The defaults above suit a senior-PM / Head-of-Product hunt; adapt for other levels by editing the rubric.

## Rate limiting

- Ashby tolerates ~1 req/sec — add a 1s delay between companies.
- Greenhouse and Lever are more permissive (~5 req/sec each).
- 40 companies × 3 platforms-tried = 120 calls worst case. Run sequentially within a batch (Recheck-A and Recheck-B run in parallel as two separate subagents, but inside one agent the calls are serial).

## When ATS detection fails

Some companies use custom careers pages not backed by Ashby/Greenhouse/Lever (Workday, SmartRecruiters, Personio, in-house). For those:

- Skip the ATS recheck.
- Optionally fall back to a `WebFetch` on the company's careers page if known, parse roles from the HTML.
- Or just rely on the Discovery phase to surface the company via WebSearch (their roles will show up if they have any).

Mark these companies in the recheck output as `ats_detection: failed` so the user knows the recheck didn't fully cover them.
