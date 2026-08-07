# Schema — `userdata/profile.md`

The user's identity + tier rubric. Read by `/evaluate-position`, `/job-search`, `/apply`, `/interview-prep`, `/today`, and the reviewer agents. Written by `/setup`.

Checked by `scripts/validate_userdata.py` (rules `profile.required`, `profile.positioning`), which the test-personas harness runs in Phase 3.5 and CI runs over `tests/snapshots/`.

## Required frontmatter keys

Every profile.md MUST have these top-level keys with non-empty values:

- **`name`** — the user's name.
- **`target_titles`** — block list of role titles. At least one item.
- **`tier_weights`** — the five-dimension scoring rubric (`role_fit`, `domain_fit`, `business_health`, `location_fit`, `competitive_edge`), each with rubric strings for scores 1–3. `/evaluate-position` cannot run without it.
- **`tier_thresholds`** — `p0` and `p1` integer cut-offs.

## Required body sections

- **`## Positioning`** — may hold placeholder text after a minimal `/setup`, but the heading must exist; `/apply` and the reviewer agents anchor on it.

## Common optional keys (absence allowed, never flagged as drift)

`city`, `timezone`, `email`, `linkedin_url`, `target_industries`, `geography`, `salary_band`, `hard_filters`, `company_shape_adjustment`, and the `## Proof Points`, `## Moat`, `## Tone of Voice`, `## What NOT to Frame As`, `## Companies of interest` body sections.

## When to update this schema

A skill starts requiring a new profile key → add it here AND to `scripts/validate_userdata.py` AND to `/setup`'s writes, in the same change.
