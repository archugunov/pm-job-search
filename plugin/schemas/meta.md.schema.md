# Schema — `userdata/companies/<slug>/meta.md`

The canonical state file per `(company, position)` pair. Read by `/today`, `/apply`, `/interview-prep`, `/job-search`, and the dashboard. Schema drift here propagates silently into downstream skills.

Used by the test-personas Phase 3.5 schema check. If you change the schema, update every reader's SKILL.md and re-run cold-start verification.

## Required frontmatter keys

Every meta.md MUST have these keys with non-empty values:

- **`company`** — company name as the user refers to it (canonical casing). Example: `Plaid`, `AcmeCorp`, `iwoca`.
- **`position`** — role title. **Use `position:` NOT `role:`** — `role:` is a known sub-agent drift pattern that breaks downstream readers.
- **`status`** — current pipeline state. Allowed values (enum):
  - `new` — discovered but not triaged
  - `to_apply` — triaged, application not yet submitted
  - `applied` — application submitted, no response yet
  - `interviewing` — at least one interview scheduled or completed
  - `offer` — offer extended
  - `rejected` — closed by the company
  - `not_interested` — closed by the user (withdrew, declined)
- **`link`** — live JD URL. Must start with `http://` or `https://`. Allowed empty only when paired with a comment explaining why (e.g. `link:  # closed listing, retained for reference`).

## Optional frontmatter keys

These are commonly present and read by some skills; absence is allowed but flagged in opportunistic schema findings:

- **`tier`** — tier rubric score result. One of `P0`, `P1`, `P2`, or `unscored`. (`P0` = strongest fit.) This is the canonical notation the skills write and the dashboard renders; do not use bare `1`/`2`/`3`.
- **`score`** — numeric score from the tier rubric. Integer.
- **`first_seen`** — date the role was first surfaced. ISO 8601 `YYYY-MM-DD`.
- **`last_seen`** — date the role was most recently confirmed live (e.g. by recheck). ISO 8601.
- **`last_activity`** — date of most recent state change. ISO 8601. Used by `/today`'s heads-up for stale-pipeline flagging.
- **`monitoring`** — boolean, `true` for companies the user wants to be re-checked on `/job-search` runs even when no role is active.
- **`source`** — discovery source. Examples: `discovery`, `recheck`, `user`, `evaluate-position`.
- **`location`** — optional one-line location/remote flag.

## Forbidden keys (sub-agent drift signals)

If any of these appear, treat as schema drift:

- **`role:`** — use `position:` instead. Documented as drift pattern 2026-06-07 in `plugin/memory.md`.
- **`target_date:`** — does not exist in this schema. Strategy.md uses `target_offer_date:`. If found in meta.md, sub-agent invented it.

## Phase 3.5 validation rules

The orchestrator (`plugin/skills/test-personas/SKILL.md` Phase 3.5) checks each meta.md in `userdata/companies/*/meta.md` and `userdata/companies/*/*/meta.md` after the conversation loop terminates. For each file:

1. **Required keys present:** missing any of `company`, `position`, `status`, `link` → schema drift finding.
2. **Status enum:** `status` value not in the allowed list → schema drift finding.
3. **Link format:** non-empty `link` that doesn't start with `http://` or `https://` → schema drift finding.
4. **Forbidden keys absent:** any of `role:`, `target_date:` present → schema drift finding.

Schema findings are surfaced to the judge as a 6th input block. The judge treats each finding as a Hard violation under Rule 7 (schema drift), independent of conversation transcript evidence — schema drift is provable from file contents alone.

## When to update this schema

- A skill adds a new required field to meta.md → add it here AND update every reader.
- A skill's SKILL.md uses a new field name (rename or addition) → reconcile here first.
- A new test journey starts auto-filing meta.md files → confirm its outputs match this schema before merging.

Keep this file lean. Optional-key list will grow; trim aggressively when keys fall out of use.
