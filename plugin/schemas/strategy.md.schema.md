# Schema — `userdata/strategy.md`

The user's plan. Read by `/today` (progress tracking), `/evaluate-position` (anti-goals), and `career-coach`. Written by `/setup` (basic) and edited via `career-coach`.

Checked by `scripts/validate_userdata.py` (rules `strategy.required`, `strategy.date-format`, `strategy.forbidden-key`).

## Required frontmatter keys

- **`target_offer_date`** — `YYYY-MM-DD`, or `null` (the `/setup` Step 7 "Not sure yet" path). Key must be present either way.
- **`weekly_targets`** — block with `warm_outreach` and/or `applications` (either may be null). Key must be present.

## Forbidden keys (drift signals)

- **`target_date:`** — the documented sub-agent drift misspelling of `target_offer_date:`. Deliberately present in the `contrarian-messy` snapshot as test material.

## Common optional keys / sections

`pipeline_targets`, `checkpoints`, `## Headline goal`, `## Anti-goals`, `## Checkpoints` prose.
