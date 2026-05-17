---
name: evaluate-position
description: This skill should be used when the user asks to "/evaluate-position", "evaluate this role", "score this job", "should I apply for this", "rate this posting", "tier this company", or pastes / links a job description and wants a tier score + research brief written. Reads userdata/profile.md (for the tier rubric), takes a URL or pasted JD as input, scores against tier_weights + tier_thresholds + company_shape_adjustment, writes userdata/companies/<Co>/meta.md and a ~200-word research-brief.md, handles the 1→2 role folder migration, and enforces the (company, position) dedup rule.
---

# /evaluate-position — score a job posting against the tier rubric

Single-role discovery. Takes one posting (URL or pasted JD), produces a tier score and a research brief, files them under `userdata/companies/<Co>/` per the §I.4 folder layout. Idempotent against re-evaluation of the same role; never duplicates an existing `(company, position)` pair.

**Voice:** every prompt (hard-filter bypass, score override, re-evaluation choice) and the chat output / written brief follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — accept defaults where they work, only ask the user when input changes the outcome.

## Inputs

- The user's input — one of:
  - A URL (the user typed `/evaluate-position https://example.com/jobs/123` or similar). Use the WebFetch tool to retrieve the page content. If WebFetch fails or returns boilerplate (login wall, JS-only render), tell the user and ask them to paste the JD instead.
  - Pasted JD text (the user pasted the posting body). Use as-is.
  - Nothing — prompt: `Paste the job description, or give me a URL to fetch.`
- `userdata/profile.md` — read frontmatter for `tier_weights`, `tier_thresholds`, `company_shape_adjustment`, `target_industries`, `target_titles`, `hard_filters`, and the `## Positioning` body. Skill cannot run without profile.md — if missing, tell the user to run `/setup` first.
- All existing `userdata/companies/*/meta.md` AND `userdata/companies/*/*/meta.md` — needed for dedup detection and folder-layout decisions.

## Extract from the JD

Parse and pin down, in order:

1. **Company name.** Prefer the JD's own statement ("About <Company>"); fall back to URL domain if pasted text omits it. Use the company's canonical name (e.g. `Stripe`, not `stripe.com`). Title-case.
2. **Position title** (the role name as posted, e.g. `Senior PM, Consumer Credit`). Keep the company's exact phrasing — do NOT normalize to your own ladder. This is what `meta.md` stores as `position` and what the dedup rule keys on.
3. **Location** — on-site city, hybrid days, or remote-region.
4. **Reports-to** (if disclosed) and team-size (if disclosed).
5. **Compensation band** (if disclosed). Most JDs don't disclose; note "not disclosed" when absent.
6. **Notable signals**: funding stage (Series A/B/etc.), team size at the company (LinkedIn count or "About us" mention), founder-led status, PLG/sales-led, scope (IC vs people-management).

If any of items 1-2 cannot be determined, ask the user before proceeding — do NOT guess on the identifying fields.

## Hard-filter gate (before scoring)

Walk `hard_filters` from profile.md against the extracted signals. If any filter matches, do NOT score — instead write a one-paragraph rejection note to chat, ask the user `Score anyway and file as P2 / monitor / drop` and proceed per their answer. Hard filters are explicit user pre-commitments; bypassing them silently defeats the point.

If `drop`: don't write any files; print "Dropped — matched filter: <filter>."

## Anti-goals soft warning (after hard-filter gate, before scoring)

ALSO read `userdata/strategy.md` if present and walk its `## Anti-goals` bullet list against the extracted signals. Anti-goals are time-bounded situational exclusions that EXTEND `hard_filters` (per the strategy.template.md guidance) — they're advisory, not blocking. Different treatment from hard_filters:

- If any anti-goal matches, print a one-line soft warning before scoring: `Heads-up: matches anti-goal "<verbatim text>". Score and file anyway?` Wait for explicit user confirmation (`yes` / `skip` / `update anti-goal`). Defaults to score-anyway if the user just continues — but the warning was surfaced.
- If the user picks `update anti-goal`, suggest they edit `userdata/strategy.md` `## Anti-goals` directly or ask `pm-job-search:career-coach` to help — then exit this run without writing files.
- Multiple anti-goals can match — surface all of them in one warning message before asking.

This catches the case where a hard_filter would have blocked the role but the user only stated the rule in strategy.md (time-bounded "during this search") rather than profile.md (permanent rule). Strategy anti-goals catch the recently-added preferences; hard_filters catch the always-true preferences. Both deserve respect.

If `strategy.md` is missing entirely, skip this step silently.

## Tier scoring

Score each of the five dimensions 1, 2, or 3 using the rubric from profile.md's `tier_weights`. Use the rubric STRINGS literally — they're the user's words for what each level means. Don't substitute your own judgement of "what 3 should mean."

The five dimensions (each must be scored):
- `role_fit`
- `domain_fit`
- `business_health`
- `location_fit`
- `competitive_edge`

Sum the five into a raw score (3-15 range).

Apply `company_shape_adjustment` (single ±1 to `role_fit` only, capped at 1-3):
- If the company matches the `bonus` description, `role_fit += 1` (max 3).
- If the company matches the `penalty` description, `role_fit -= 1` (min 1).
- The two cannot both apply; if both seem to, prefer the one with the stronger evidence.

Recompute the sum after the adjustment. That's the final `score`.

Apply `tier_thresholds`:
- `score >= p0` (default 13) → `tier: P0`
- `p1 <= score < p0` (default 11-12) → `tier: P1`
- `score < p1` (default <11) → `tier: P2`

Show the scoring breakdown to the user before writing files: a 5-row table of `dimension | score | rubric-string-matched | one-line justification`. Ask `Use this score, adjust manually, or rescore with my override?` Accept their override on any dimension — never strong-arm the user; the rubric is a tool, not a verdict.

## Posting legitimacy verdict

Before scoring, run a quick legitimacy check on the JD itself — separate from the role-fit score. Saves the user from chasing dead or zombie postings.

Emit one of three verdicts:

- 🟢 **high** — recent posting (date stamp or "posted N days ago" within last 30d), Apply / Submit button visible, JD content is substantive (≥300 chars, names a hiring manager or specific team scope, not generic boilerplate).
- 🟡 **caution** — at least one yellow signal: missing date stamp, JD is mostly boilerplate language, no named team or scope, or has been live >60 days.
- 🔴 **suspicious** — multiple yellow signals OR: JD says "always hiring" / "evergreen", Apply button is missing or links offsite to a third-party recruiter, content is < 200 chars, or URL redirects to a generic careers landing.

If pulled via WebFetch, infer from the fetched page content. If pasted JD, infer from the text (no URL liveness signal — default to 🟡 caution unless the user provides freshness info).

Surface the verdict in:
1. The scoring breakdown shown to the user before file writes.
2. `meta.md.legitimacy` frontmatter field.
3. The closing chat output (see "Output to chat").

If the verdict is 🔴 suspicious, ASK the user before scoring/filing: `Posting looks suspicious (<reason>). Score and file anyway, file as monitoring-only, or skip?`

## Folder layout (per §I.4)

Walk the discovery in this order:

1. **No `userdata/companies/<Company>/` directory exists** → fresh company. Use FLAT layout: create the directory and place `meta.md` + `research-brief.md` directly inside it.
2. **Directory exists in FLAT layout** (i.e. `userdata/companies/<Company>/meta.md` is present at top level) → company already tracks 1 role.
   - **Dedup check**: read the existing `meta.md`'s `position` field. If it exactly matches the new role's `position`, this is a re-evaluation — see "Re-evaluation" below; do NOT add a duplicate row.
   - **Different position** → 1→2 migration. Steps:
     a. Compute a slug for the EXISTING role from its `position` field (kebab-case, ASCII-safe, e.g. `Senior PM, Consumer Credit` → `senior-pm-consumer-credit`).
     b. Compute a slug for the NEW role similarly.
     c. Create `userdata/companies/<Company>/<existing-slug>/` and MOVE the existing `meta.md` + `research-brief.md` + any other skill-authored files (`interview-prep-*.md`, `interview-debrief-*.md`, `review-*.md`) into it. Leave user-authored top-level files (anything the skill did not create — e.g. `company-notes.md`) untouched at the top level.
     d. Create `userdata/companies/<Company>/<new-slug>/` and write the new `meta.md` + `research-brief.md` inside.
3. **Directory exists in SUBFOLDER layout** (i.e. role-slug subfolders, no top-level `meta.md`) → company already multi-role.
   - **Dedup check**: glob `userdata/companies/<Company>/*/meta.md`, compare each `position` against the new role's `position`. Match → re-evaluation, see below.
   - **Different position** → compute slug, create `<new-slug>/` subfolder, write inside.
4. **Mixed (rare)**: both a top-level `meta.md` AND subfolder `meta.md` files exist (likely from an interrupted migration). Print a warning and ask the user to clean up manually before proceeding. Do not write.

Slug rule: lowercase, ASCII letters/numbers/hyphens only, collapse runs of non-alphanum to single `-`, strip leading/trailing `-`. Examples: `Lead PM, Growth` → `lead-pm-growth`; `Head of Product` → `head-of-product`.

## Re-evaluation (existing `(company, position)` pair)

When a match is found:

1. Read the existing `meta.md`. Show its current `status`, `tier`, `score`, `date_added`.
2. Ask the user: `This is already tracked — overwrite (re-score), refresh research brief only, or cancel?`
3. `overwrite` → re-score fully, write the new score / tier into `meta.md`, preserve existing `status` and date fields, regenerate `research-brief.md`.
4. `refresh research brief only` → regenerate `research-brief.md`; don't touch `meta.md` at all.
5. `cancel` → no writes.

**Never** overwrite a `closed` or `rejected` row's status — those are real history. Re-evaluation of a closed role can update score/research but leaves status as-is.

## File writes

### `meta.md` frontmatter (required keys)

```yaml
---
company: <Company>
status: new
tier: <P0|P1|P2>
score: <int 3-15>
position: <exact position title from JD>
link: <URL if provided, otherwise blank>
date_added: <YYYY-MM-DD today>
monitoring: false
---
```

Optional keys to include when known:
- `location`: free-string (e.g. `London, hybrid 2d/wk`)
- `reports_to`: free-string
- `team_size`: int or string range
- `comp_band`: free-string
- `legitimacy`: one of `high` / `caution` / `suspicious` (see "Posting legitimacy verdict" below)

Body (below frontmatter): a short title-cased `# <Company>` heading + one paragraph orienting the company. Do NOT duplicate the research brief here — that's a separate file.

### `research-brief.md` (~200 words, structured)

Three fixed sections, no preamble:

```markdown
# <Company> — <Position title>

## Company snapshot
<2-3 sentences. Stage, scale, what they actually sell, who runs the team
the role sits in. Anchored to facts from the JD or your shortlist research,
not speculation.>

## Why this fits
- <Bullet — concrete fit to a tier_weights dimension or to the user's positioning.>
- <Bullet — same.>
- <Bullet — same. Aim for 3-5 bullets.>

## Open questions
- <Bullet — something the JD didn't answer that the user should ask in the
  first call.>
- <Bullet — same. Aim for 2-4 questions.>
```

Hard rules:
- Maximum ~200 words total. If the brief grows, cut "Open questions" first, then trim "Why this fits."
- Quote / paraphrase the JD or profile only — don't invent details about funding, headcount, or recent news that weren't in the inputs.
- Use the user's `## Tone of Voice` from profile.md if it's set; otherwise default to direct, short sentences.

## Output to chat

After files are written, print to chat (compact):

```
Filed: <Company> / <Position> — tier <P0/P1/P2>, score <N>, legitimacy <🟢|🟡|🔴>.
  meta.md         → userdata/companies/<Company>/[<slug>/]meta.md
  research-brief  → userdata/companies/<Company>/[<slug>/]research-brief.md
  Status: new. Move to to_apply / applied as you act.
```

If a migration happened, add: `Migrated existing role into <existing-slug>/ subfolder.`

If a hard-filter bypass was used: `Note: bypassed hard filter "<filter>" at your request.`

## What /evaluate-position never does

- Never invents tier-rubric values. Reads them from profile.md only.
- Never writes outside `userdata/companies/<Company>/`. No edits to profile, strategy, journal, or outputs.
- Never overwrites `closed` or `rejected` status during re-evaluation.
- Never moves user-authored files during 1→2 migration. Only skill-authored files (meta.md, research-brief.md, interview-prep-*.md, interview-debrief-*.md, review-*.md) get moved into the new slug subfolder.
- Never bypasses a hard filter without an explicit user override.
- Never sets `status` to anything other than `new` on a fresh write. Status transitions are user-driven (or `/today`-surfaced as nudges, not state changes).

## Smoke test against the Maya example

Synthetic test: paste a JD for "Klarna — Senior PM, Consumer Credit" against `userdata/examples/maya/` as the install root.

- Hard-filter check: none of Maya's hard_filters match (Klarna is not >500ppl crypto with no PLG signal; not >8 reports; in Europe). Proceed.
- Score: domain_fit 3 (consumer credit, fintech), role_fit 2 (Senior PM matches level), business_health 3 (well-funded, growing), location_fit 2 (assume EMEA remote), competitive_edge 3 (direct domain) = 13. company_shape_adjustment: Klarna is ~5000 ppl, outside the 20-80 sweet spot → no bonus; not penalty either (it IS in target industries). Final 13 = P0.
- Folder layout: `userdata/examples/maya/companies/Klarna/` doesn't exist → flat layout. Write `Klarna/meta.md` + `Klarna/research-brief.md`.

Synthetic test for 1→2 migration: paste a JD for "Plaid — Lead PM, Risk Platform". Plaid folder already has flat layout with `Senior PM, Consumer Credit`. Different position → migrate existing files into `Plaid/senior-pm-consumer-credit/`, create `Plaid/lead-pm-risk-platform/` with the new files.
