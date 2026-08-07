# Schema — `userdata/companies/<Company>/[<slug>/]research-brief.md`

The ~200-250 word research brief written alongside `meta.md` by `/evaluate-position`. Read by `/apply`, `/interview-prep`, and the dashboard. Full structural spec (section order, word count, tone) lives in `plugin/skills/evaluate-position/SKILL.md` under `### research-brief.md` — this file documents only the two machine-checkable rules `scripts/validate_userdata.py` enforces.

Checked by `scripts/validate_userdata.py` (rules `brief.source-line`, `brief.link-mismatch`), which the test-personas harness runs in Phase 3.5 and CI runs over `tests/snapshots/`.

## Validation rules

1. **`brief.source-line`** — the first content line must be `**Source:** <url>`, and `<url>` must start with `http://` or `https://`. Missing or malformed → schema drift finding.
2. **`brief.link-mismatch`** — when a sibling `meta.md` exists with a non-empty `link`, the brief's `**Source:**` URL must match it exactly (fragments and query strings included). A mismatch means the brief was generated against a different posting than the one `meta.md` tracks → schema drift finding.

## When to update this schema

`/evaluate-position`'s SKILL.md changes the `**Source:**` line format or the source/meta-link relationship → update both this file and `scripts/validate_userdata.py`'s `_check_brief` in the same change.
