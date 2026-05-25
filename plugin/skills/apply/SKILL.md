---
name: apply
description: This skill should be used when the user asks to "/apply <Company>", "tailor my CV for <Company>", "draft an application CV for <Company>", "prepare my application for <Company>", or names a company they're applying to and wants a tailored CV. Reads userdata/cv.md (master CV), userdata/profile.md (positioning, tone, what-NOT-to-frame-as), and userdata/companies/<Co>/[<slug>/]{meta,research-brief}.md. Runs a 3-phase process — silent analyse, upfront Q&A capped at 5 questions, single-pass draft — and writes userdata/companies/<Co>/[<slug>/]cv-<YYYY-MM-DD>.md. Hard rule: every claim in the tailored CV traces to the master CV, profile.md, or a user answer. Never invents facts. Never touches meta.md status or the master CV.
---

# /apply — tailor a CV for a specific role

Single-purpose skill: produces a tailored CV file for one role at one company, by reading the user's master CV and rewriting it against the company's JD signals (from `research-brief.md`). Sits between `/evaluate-position` (which creates the company folder) and `/interview-prep` (which assumes an interview is already booked).

**Voice:** every prompt (multi-role disambiguation, Phase B clarifications, re-run choice) and the chat output follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — only ask the user when the answer changes the output.

## Inputs

- `<Company>` argument — required, e.g. `/apply Plaid` or `/apply "Plaid"`. Case-insensitive folder lookup against `userdata/companies/`. If no exact match, fuzzy-suggest: `No 'Plad' folder. Did you mean Plaid? (y/n)`. If the company tracks multiple roles (subfolder layout), ask which: `Plaid tracks 2 roles — pick: 1) senior-pm-consumer-credit, 2) lead-pm-risk-platform`.
- `userdata/cv.md` (or `userdata/cv.txt`) — **the master CV**, canonical source of truth for every factual claim in the tailored output. Skill cannot run without it.
- `userdata/profile.md` — read `## Positioning`, `## Proof Points`, `## Moat`, `## Tone of Voice`, `## What NOT to Frame As`.
- `userdata/companies/<Co>/[<slug>/]meta.md` — read frontmatter for `position`, `comp_band`, `location`. Used for the tailored CV header context and the chat output.
- `userdata/companies/<Co>/[<slug>/]research-brief.md` — JD-grounded signals (Company snapshot, Why this fits, Open questions). Used to extract JD requirements for tailoring.

Optional flag:

- `--from-url <URL>` — re-fetch the live JD via WebFetch instead of relying on `research-brief.md`. Use when the brief is stale or thin. If WebFetch fails or returns boilerplate, fall back to `research-brief.md` and warn the user.

**Missing-input handling** (one-line errors, point to the fix, exit cleanly):

- No `userdata/cv.md` or `.txt` → tell the user: `No userdata/cv.md or .txt — drop one or run /setup --refresh to create it.` Exit.
- No `userdata/companies/<Co>/` folder → tell the user: `No userdata/companies/<Co>/ — run /evaluate-position first.` Exit.
- No `research-brief.md` (company was added manually rather than via `/evaluate-position`) → soft warning: `No research-brief.md — tailoring will be looser. Continue?` Default yes; if yes, proceed using only `meta.md.position` to infer JD signals.

**Status guardrail** (after missing-input handling, before Phase A):

Read `meta.md.status`. The natural target stages for `/apply` are `new`, `to_apply`, and `applied` (the last covers re-applies or refreshed CVs). For any other status, the application phase is past or moot — warn the user before proceeding:

- `interviewing` / `offer` → `<Company>'s status is '<status>' — /apply is for the application phase. Continue anyway?` (e.g. you might want an updated CV for reference checks, or to archive a tailored version)
- `rejected` / `not_interested` → `<Company>'s status is '<status>' — /apply usually isn't useful here. Continue anyway?`

Default: ask, don't auto-skip. If the user says no, exit cleanly without writing. If yes, proceed normally.

For `new`, `to_apply`, `applied`: proceed silently (no warning needed — these are the natural target stages).

## Process

Three phases. The first is silent (no chat output until the skill has something to say), the second surfaces clarifications in one batch, the third produces the file.

### Phase A — Read & analyse (silent)

Read all inputs listed above. Build an internal map covering:

- Which JD requirements (from `research-brief.md` or the fetched JD) map to which master-CV bullets.
- Which JD keywords have **no** supporting evidence in the master CV. These will NOT be injected — they'll be surfaced in the chat output instead.
- Where ambiguity exists in how a master-CV bullet could be framed for this JD.
- Whether the master CV is over-long for the JD's level (rough heuristic: master CV >2 pages AND JD targets a junior level relative to the user's seniority).

Do not write anything to the user yet.

### Phase B — Upfront Q&A (visible)

Surface a **single batch** of clarifications before drafting. Three categories, prioritised in this order:

1. **Verifiable gaps** — JD asks for something not explicitly in master CV.
   Example: *"JD lists GraphQL as required. Master CV mentions REST APIs but not GraphQL — did you use it at NorthLoop?"*
   Record the user's answer verbatim. If yes, the answer becomes a permitted fact (Phase C may use it). If no, the keyword joins the "did NOT inject" list.

2. **Ambiguous mapping** — a master-CV bullet could be framed multiple ways.
   Example: *"For the activation funnel work — JD emphasises 'experimentation velocity'. Lead the bullet with the A/B test cadence, or the conversion outcome?"*

3. **Length / structure choices** — only ask when the master CV exceeds two pages AND the role would normally take a shorter CV.
   Example: *"Master CV runs ~3 pages. Cut older roles to one line each, or keep full bullets?"*

**Cap the batch at 5 questions.** If more would help, ask the top 5 and tell the user: `Drafting with what I have; flagging <N> remaining ambiguities inline as [CONFIRM: ...] in the output.`

If Phase A surfaced **zero** questions, skip Phase B entirely and go straight to Phase C without telling the user (no "I have no questions" message — that's noise).

Use AskUserQuestion when the answer fits 2-4 discrete options. Use a plain chat prompt when it's free-text (e.g. "Did you use X? If yes, what was the scope?").

### Phase C — Draft once

Produce the full tailored CV in one pass. Follow the drafting rules below. Do **not** show the user partial drafts — write the file, then describe what changed in the chat output.

## Drafting rules

**Preserve structure.** Same section order as master CV (typically: header, summary, experience, education, skills). Do not introduce sections the master doesn't have. Do not promote bullets into new section types.

**Preserve length.** Total length within ±15% of master CV. Per-role bullet counts within ±1 of master. *Exception:* if the user picked "cut older roles" in Phase B Q3, that choice overrides this rule for the affected roles.

**Preserve voice.** Follow `## Tone of Voice` from `profile.md`. Do not introduce filler ("results-driven", "passionate about", "proven track record"). Do not make every bullet start with a power verb — varied openings. Match the master CV's register; if the master writes in past tense for prior roles, the tailored CV does too.

**Tailoring moves, in priority order:**

1. **Rewrite the summary** to lead with the positioning angle that matches the JD's top 2-3 signals (extracted from `research-brief.md`'s "Why this fits" and the JD body if fetched).
2. **Reorder bullets within each role** to put JD-relevant work first.
3. **Reword existing bullets** to surface matching keywords/skills, but only where the underlying fact supports it. Example: master CV says "shipped pricing experiments"; JD asks for "A/B testing experience" → reword to "designed and shipped A/B pricing experiments". Do not reword if the fact doesn't support the keyword.
4. **Inject ATS keywords** from the JD into existing bullets only where they describe real work. If a JD keyword has no supporting evidence in the master CV, do NOT inject it — surface it in the chat output's "Did NOT inject" line instead.

**Hard rule — every claim traces.** Every sentence in the tailored CV must trace to one of:

- (a) A bullet in master CV
- (b) A section in `profile.md`
- (c) A user answer in Phase B

Anything else is fabrication and must not be written.

**`## What NOT to Frame As` enforcement.** Read those bullets from `profile.md`. If any drafted sentence violates one (e.g. "deeply passionate about" when the rule says "Don't use superlatives"), rewrite or drop it. Surface the count in the chat output: `Removed N anti-pattern phrases.`

**Unresolved ambiguities.** Phase B questions that didn't get asked because of the 5-cap appear inline as `[CONFIRM: <question>]` markers in the draft. The user resolves them manually before submitting. The chat output names the count.

## File write

Always one file:

```
userdata/companies/<Co>/[<slug>/]cv-<YYYY-MM-DD>.md
```

Pure markdown, no frontmatter. Structure mirrors master CV exactly. The file is ready for the user to copy into their CV editor of choice, or to PDF-export via the future Playwright skill (out of scope here).

### Re-run behavior

- If `cv-<today>.md` already exists at the target path → ask: `cv-<today>.md already exists. Overwrite, or save as cv-<today>-v2.md?` Default: `-v2`. Continue suffixing if `v2` exists (`v3`, `v4`, etc.).
- If only older `cv-<earlier-date>.md` exists → write today's dated file silently. Don't touch the older one.
- Never delete or rename previous CV files.

## Output to chat

**Chat summary (TONE Rule B — plain prose, no fenced code, no key-value dumps):**

Template:

> Drafted your tailored CV for **<Company> — <Role>** and saved it to `<path>`.
>
> What I leaned on:
> - Positioning angle: <one phrase from profile.md>
> - Strongest proof points: <2–3 short references, comma-separated>
> - Dropped: <one line on what was cut and why>
>
> Open the file and edit anything that doesn't sound like you before you send it. <Closing question — one only, per TONE Rule A — typically: "Want me to draft a short cover note next?">

Rules:
- Plain prose opener and closer.
- One short bulleted recap (3–5 lines).
- Never a `key: value` block, never fenced.
- One closing question only (TONE Rule A).
- End with a context-aware next-step nudge per `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md` — but the closing question often already serves this role; only add a separate nudge if it points somewhere different.

**Tailoring summary line rules** — only emit lines for changes that actually fired. Skip lines that would be zero/empty. This avoids misleading the user when the master CV was already well-shaped for the JD.

- **Summary rewrite:** if you rewrote the summary, emit `- Rewrote summary to lead with <one-phrase reason>`.
- **Bullet reorders:** if you reordered bullets within N>0 roles, emit `- Reordered bullets in <N> role(s)`. If N=0 because master bullets were already in JD-relevant order, emit `- Bullets not reordered — master CV already had JD-relevant work first per role`.
- **Bullet rewords:** if you reworded N>0 bullets to inject keywords, emit `- Reworded <N> bullet(s) to surface matching keywords`. Skip if N=0.
- **Skills reorder:** if you reordered the Skills section, emit `- Reordered Skills line N to lead with <new-first-items>`. Skip if no reorder.
- **Injected JD keywords:** always emit `- Injected JD keywords: <list, ≤5>`. If the list is empty (you injected no new keywords), emit `- Injected JD keywords: none — master CV already covered the JD vocabulary`.
- **Did NOT inject:** always emit `- Did NOT inject (no supporting evidence): <list>` if the list is non-empty. Skip the line entirely if you injected everything the JD asked for. This list is the skill's main honesty signal — never collapse it into "various keywords skipped."
- **`[CONFIRM: ...]` markers:** if N>0 markers were left inline, emit `- Flagged <N> [CONFIRM: ...] marker(s) inline — resolve before submitting`. Skip if N=0.
- **Anti-pattern removals:** if `## What NOT to Frame As` flagged anything during drafting, add `- Removed <N> anti-pattern phrase(s)`. Skip if zero.

If WebFetch was tried via `--from-url` and fell back to research-brief, add a separate line after the bulleted recap: `Note: --from-url fetch failed, used research-brief.md instead.`

## What /apply never does

- Never invents facts, dates, metrics, technologies, team sizes, or project outcomes. If a JD keyword has no supporting evidence, surface it in the chat output, never in the CV.
- Never touches `meta.md` — no status flip, no date update, nothing. Status transitions stay user-driven, consistent with `/evaluate-position` and `/interview-prep`.
- Never edits `userdata/cv.md` (the master) or `userdata/profile.md`. Read-only on both.
- Never writes a cover note or outreach message. Suggests them as next steps in chat output.
- Never deletes prior `cv-*.md` files. Each re-run produces a new dated/versioned file.
- Never exports PDF. That's the backlog Playwright skill's job.
- Never bypasses `## What NOT to Frame As` — those bullets are hard guardrails, not suggestions.
- Never asks the user to confirm something the skill can already determine from inputs.

## Smoke test against the Maya example

Run `/apply Plaid` against `userdata/examples/maya/` (Plaid has subfolder layout — `consumer-credit/` and `growth-loops/`):

1. **Disambiguate:** `Plaid tracks 2 roles — pick: 1) consumer-credit, 2) growth-loops`. Pick 1 (consumer-credit).
2. **Read** `userdata/examples/maya/cv.md` (the master CV — must exist; created in the same PR as this skill).
3. **Read** `userdata/examples/maya/profile.md` — positioning ("messy middle, post-PMF products"), tone ("direct, short sentences, no filler"), what-NOT ("no superlatives, no process-PM framing").
4. **Read** `userdata/examples/maya/companies/Plaid/consumer-credit/research-brief.md` — signals: "consumer credit", "thin-file applicants", "underwriting integration".
5. **Phase B Q&A** — likely 1-3 questions, e.g.: *"JD mentions Python data tooling — master CV lists Python (basic). Frame as 'comfortable with Python' or skip?"* User answers; skill records.
6. **Phase C** — draft the tailored CV. Summary leads with the consumer-credit / thin-file angle (matching the Plaid JD). Underwriting integration bullet (from Brightline Credit) moves above the activation funnel bullet for relevance.
7. **Write** `userdata/examples/maya/companies/Plaid/consumer-credit/cv-2026-05-18.md`.
8. **Chat output** names which keywords were injected, which weren't, and how many roles got reordered.

Pass criteria for the smoke test:

- The file is created at the correct path.
- Every CV claim traces back to `userdata/examples/maya/cv.md` (no fabricated companies, dates, or metrics).
- The summary leads with thin-file / consumer-credit, not the SaaS activation angle.
- The chat output includes both "Injected" and "Did NOT inject" lines.
- No status field was modified in `userdata/examples/maya/companies/Plaid/consumer-credit/meta.md` (diff it against HEAD before the test — should be unchanged).
