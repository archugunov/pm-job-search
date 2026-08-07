# Transcript — maya-cold-start

**Date:** 2026-08-04
**Snapshot:** empty
**Max turns:** 30
**Code under test:** working tree at `b3a4b44` (v0.4.0 + verification fixes), NOT the installed 0.3.0-beta.5 cache.

**Orchestration note:** run manually rather than via the installed `/test-personas`
skill, because the installed copy is a June snapshot. `${CLAUDE_PLUGIN_ROOT}` is
resolved to the working tree. The plugin agent reads each SKILL.md fresh from disk
as a mandatory action, and is kept as one continuous session via SendMessage
rather than re-dispatched per turn.

**Known-good baseline:** `cold-start` passed 13/13 required against 0.3.0-beta.6
on 2026-07-11. A failure here is a v0.4.0 regression, not a pre-existing red.

---

## Turn 1 — USER

/pm-job-search:setup

## Turn 1 — ASSISTANT

I've created `userdata/` and you don't have a CV file there yet. Drop your CV as `cv.md`, `cv.txt`, or `cv.pdf` into `userdata/` — or just say "no CV" and we'll do it the long way.

> **Orchestrator note — FIDELITY DEVIATION.** `cv-extraction.md` § "Finding the CV"
> locks this prompt as: "I've created userdata/ for you — drop your CV there as
> cv.md, cv.txt, or cv.pdf. Say 'ready' when it's in." The agent paraphrased it and
> merged in a "no CV" escape that the locked wording does not offer. Verified
> correct in the same turn: `userdata/` plus all three `.gitkeep` files WERE created
> before the prompt, satisfying the precreation criterion.

## Turn 2 — USER

I don't have a CV handy — let's just do it the long way.

## Turn 2 — ASSISTANT

No CV — we'll do it the long way then. Same questions, you just type more.

OK, let's get you set up. Nine quick steps — none of it's locked in, you can rerun anytime. Ready?

## Turn 3 — USER

Ready.

## Turn 3 — ASSISTANT

What's your name?

## Turn 4 — USER

Maya Patel

## Turn 4 — ASSISTANT

Where are you based? City + country works (e.g. London, UK).

## Turn 5 — USER

London, UK

## Turn 5 — ASSISTANT

What's the best email for you?

## Turn 6 — USER

maya.patel@example.com

## Turn 6 — ASSISTANT

LinkedIn URL? Or skip.

## Turn 7 — USER

linkedin.com/in/mayapatel-pm

## Turn 7 — ASSISTANT

I'm seeing your timezone as `Europe/Madrid` — that right? Override if not.

## Turn 8 — USER

No — should be Europe/London.

## Turn 8 — ASSISTANT

Got it — Europe/London.

What roles are you targeting? Typical senior-PM examples: Director of Product, Principal PM, Group PM, Staff PM. List as many as you'd take, comma-separated.

## Turn 9 — USER

Head of Product, Lead PM, Senior PM

## Turn 9 — ASSISTANT

What industries are you looking at? E.g. healthcare, climate tech, education, enterprise SaaS. Comma-separated.

## Turn 10 — USER

Fintech, consumer credit

## Turn 10 — ASSISTANT

Positioning next — who you are and what you're best at. Two ways to handle this:

This is a single-choice question — pick one:

- A. Write it now — paste 1-3 sentences of self-positioning and we'll draft it together
- B. Skip for now — fill it in later via `/pm-job-search:setup --refresh`

> **Orchestrator note:** the no-CV Step 4 branch fires correctly with the locked
> opener and exactly two options in the documented order. This is the branch that
> commit 0932390 fixed after a three-options/two-items mismatch; it is now
> consistent.


## Turn 11 — USER

A. Senior PM, nine years in consumer credit and growth-stage B2C SaaS, currently running growth pricing at a Series B fintech. Looking for Head of Product or senior Lead PM scope.

## Turn 11 — ASSISTANT

[Mode A positioning draft — 2 paragraphs, uses the "Not X — Y" pattern: "Not a
generalist chasing a bigger title — a specialist in consumer credit and pricing
mechanics." Then asks for 3-5 numbered wins.]

## Turn 12 — USER

That's fine, keep it. [Supplies only TWO proof points, both from the persona.]

## Turn 12 — ASSISTANT

[Drafts both proof points in the documented `**Anchor:** work → outcome. (role)`
shape. Did NOT invent a third to reach the requested 3-5. Both numbers preserved
exactly (+18% MRR Q3; 12% decline rate on thin-file).]

> **FINDING — invented attribution.** The user stated a company for proof point 1
> only ("at my current Series B fintech"). Proof point 2 was given with no employer.
> The draft anchored BOTH to "Current fintech (Series B)", inventing the employer for
> #2. This is the fabrication class the state guardrails exist to prevent.

## Turn 13 — USER

Depth in consumer credit and thin-file underwriting most PMs never touch — I know the pricing/risk trade-offs cold.

## Turn 13 — ASSISTANT

## Moat

Consumer credit and thin-file underwriting — most PMs haven't worked the pricing/risk trade-offs first-hand. I have.

> **Orchestrator note — correct behaviour.** The user's own wording led with "Depth",
> a banned superlative per the Drafting tone rules. The draft stripped it and
> reframed without it. Good catch by the skill.

## Turn 14 — USER

That's good, keep it.

## Turn 14 — ASSISTANT

Where are you looking? [single-choice: On-site in London / Remote / Both / Other]

## Turn 15 — USER

Other — London hybrid, or remote within EMEA.

## Turn 15 — ASSISTANT

What salary band are you aiming for? [locked wording, free text — the one step by design]

## Turn 16 — USER

£90-110K IC, £115-140K for leadership scope

## Turn 16 — ASSISTANT

When do you want the offer signed? [single-choice, five buckets in spec order]

## Turn 17 — USER

Under 2 months — aiming to land by September.

## Turn 17 — ASSISTANT

Last one. Any red flags — roles you'd skip on sight, whatever else is right about them? [multi-select, six fixed options + Other]

## Turn 18 — USER

Other — no relocation outside EMEA, no sales-led enterprise B2B without a PLG signal, no more than 8 direct reports.

## Turn 18 — ASSISTANT

CLAUDE.md exists at workspace root and was not generated by pm-job-search. Overwrite (y/N)?

## Turn 19 — USER

n

## Turn 19 — ASSISTANT

You're set up. Wrote:
- `userdata/profile.md` — identity, target role, salary, hard filters
- `userdata/strategy.md` — headline goal + target offer date `2026-09-15` (from your "Under 2 months" answer) + derived weekly targets (12 apps/wk, 10 outreach/wk, 5 active interview threads floor). Edit these in `userdata/strategy.md` if they feel off — or ask `pm-job-search:career-coach` to help you set anti-goals and checkpoints.
- `userdata/journal.md` — empty (append daily notes here)
- `CLAUDE.md` — left as-is at your call; still your existing file, not the generated one

Want to sharpen your positioning before we wrap? [positioning-refinement offer]

## Turn 20 — USER

Skip that for now, thanks.

## Turn 20 — ASSISTANT

Want `/pm-job-search:today` to run automatically every day? (y / n) [2-step, not bundled with the time question]

## Turn 21 — USER

No, I'll run it manually.

## Turn 21 — ASSISTANT

Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first.

## Turn 22 — USER

/pm-job-search:job-search

## Turn 22 — ASSISTANT

Before I sweep — any companies you already have in mind? I'll seed the search with them. Or skip.

> **Orchestrator note:** verbatim match to the locked Phase 0 step C case-1 wording.
> Heading was absent (verified: `/setup` wrote no such section), so case 1 is the
> correct branch.

## Turn 23 — USER

Plaid, Klarna, Lendable, Mercury

## Turn 23 — ASSISTANT

I've added the `## Companies of interest` section to your profile with Plaid, Klarna, Lendable, and Mercury.

Ready to kick off the sweep — I'll recheck any tracked companies and run discovery seeded with those four plus your target titles/industries. Say go whenever.

> **Orchestrator note:** verified on disk — `profile.md` now carries
> `## Companies of interest` with one `- <Company>` bullet per entry, exactly the
> documented shape. Criterion "job-search asked the companies question on its first
> run and wrote the section to profile.md" PASSES in both halves.

## Loop paused before the live discovery sweep

Paused here by the orchestrator, not by a termination condition. Everything from
`/setup` through `/job-search` Phase 0 is verified. The remaining criteria
(auto-filing roles with `link:`, the `applications.md` Link column, the chat row
rendering) need the live Discovery sweep, which issues real web searches and
depends on live job postings.

## Turn 24 — USER

go

## Turn 24 — ASSISTANT (sweep + filing)

Discovery returned 51 real candidates across 10 site-scoped queries. Scoring ran in
three batches. 25 candidates were fetchable and scorable; the rest were dropped.
Filed 25 roles across 21 companies, regenerated `applications.md`.

> **Orchestrator note — two infrastructure failures, not plugin faults.** The sweep
> turn died twice: once on "Connection closed mid-response", once on a 600s stall
> watchdog, by which point the plugin agent's context held the entire setup
> conversation plus 51 candidates plus three batch results. The filing step was
> completed by a fresh, narrowly-scoped agent given the existing scoring output.
> Nothing was re-discovered or re-scored.

> **Verified on disk after filing:**
> - 25/25 `meta.md` carry a real `http(s)` `link:` — no placeholders, no "(url not captured)"
> - 25/25 carry all required keys (`company`, `position`, `status`, `link`)
> - 25/25 `status: new`; zero forbidden drift keys (`role:`, `target_date:`)
> - `applications.md` GENERATED block carries a populated Link column with real URLs
> - Chat rows rendered with the URL inline
> - Two-roles-at-one-company correctly used role-slug subfolders (FINN, Mercury, Plaid, Remote)

## Loop ended: journey complete

`/setup` → `/job-search` covered. `/dashboard` and `/today` were not re-run in this
journey — `/today` against a freshly-written profile was already verified
independently as release-handoff check §4.7.
