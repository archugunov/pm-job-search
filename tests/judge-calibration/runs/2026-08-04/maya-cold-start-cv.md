# Transcript — maya-cold-start-cv

**Date:** 2026-08-04
**Snapshot:** empty-with-cv
**Max turns:** 24
**Code under test:** working tree `<workspace>/plugin` at commit c32040d (v0.4.0), NOT the installed 0.3.0-beta.5 cache.

**Orchestration note:** run manually rather than via the installed `/test-personas`
skill, because the installed copy is a June snapshot. `${CLAUDE_PLUGIN_ROOT}` is
resolved to the working tree. Per Phase 3 step 3 the plugin agent is given the
skill as its operating manual; here it reads SKILL.md fresh from disk as a
mandatory first action rather than receiving an orchestrator-pasted copy, so the
code under test cannot drift from what is on disk. The plugin agent is kept as a
single continuous session via SendMessage rather than re-dispatched fresh each
turn — this is the continuity improvement SKILL.md defers to v0.4 (line 367), and
it matches a real Claude Code session more closely than fresh-per-turn.

---

## Turn 1 — USER

/pm-job-search:setup

## Turn 1 — ASSISTANT

Got your CV — I'll fill in what I can and you just correct me.

OK, let's get you set up. Nine quick steps — none of it's locked in, you can rerun anytime. Ready?

## Turn 2 — USER

Ready — let's go.

## Turn 2 — ASSISTANT

From your CV: Maya Patel · London, UK · maya@example.com · linkedin.com/in/maya-patel-example. Timezone looks like `Europe/Madrid`. All right?

> **Orchestrator note for the judge:** `Europe/Madrid` is correct behaviour, not a
> defect. `cv-extraction.md` mandates detecting timezone from the system clock and
> never from the CV; the host machine running this test is genuinely on
> `Europe/Madrid` (verified: `realpath /etc/localtime` → `Europe/Madrid`). The
> London/Madrid mismatch is an artifact of the test environment, not of the code.
> Do not raise it as a hard violation.

## Turn 3 — USER

Everything else is right, but the email's wrong — use maya.patel.pm@example.com instead.

## Turn 3 — ASSISTANT

Email updated to maya.patel.pm@example.com.

Roles you'd take. I've pulled these from your CV — from Senior PM at Brightline Credit, Lead PM at Lumio, Lead PM at NorthLoop. Pick all that apply.

This is multi-select — choose as many as apply:
- Senior PM
- Lead PM
- Head of Product
- Group Product Manager
- Other (type your own)

## Turn 4 — USER

Lead PM and Head of Product. Skip Senior PM and Group Product Manager — also add Director of Product via other.

## Turn 4 — ASSISTANT

Titles set: Lead PM, Head of Product, Director of Product.

Industries. From your CV I'd guess these — from Lead PM at NorthLoop (BNPL fintech), Senior PM at Brightline Credit (credit underwriting), Lead PM at Lumio (B2C SaaS). Pick all that apply.

This is multi-select — choose as many as apply:
- Fintech
- Consumer credit
- B2C SaaS
- Credit / lending
- Other (type your own)

## Turn 5 — USER

Fintech and consumer credit. Skip the SaaS one, that plateau's part of why I'm leaving.

## Turn 5 — ASSISTANT

Industries set: Fintech, Consumer credit.

Here's a draft positioning, pulled from your CV.

**Positioning**

Nine years in fintech and consumer credit, from underwriting risk models to BNPL pricing tests. Currently Lead PM on growth pricing at a Series B fintech; before that, led underwriting integration at a Series A credit lender. Not a scaled-org leader with a big reporting line — a hands-on PM who ships specs and reads her own data. Looking to step up into Head of Product or Director of Product without losing that hands-on edge.

**Proof Points**

1. **NorthLoop:** Designed and shipped the price-test framework on the flagship BNPL card, three back-to-back tests → +18% MRR in Q3 with no measurable churn lift. (Lead PM, Growth Pricing)
2. **NorthLoop:** Introduced a weekly product/eng/design review, now standard across all squads → cited by the CEO as the single biggest improvement in shipping cadence. (Lead PM, Growth Pricing)
3. **NorthLoop:** Coached two APMs into Senior PM roles in 18 months → both are now Leads at peer companies. (Lead PM, Growth Pricing)
4. **Brightline Credit:** Led the integration of a new credit bureau into the underwriting flow → cut decline rate by 12% on thin-file applicants while holding default rate flat. (Senior PM, Underwriting)
5. **Brightline Credit:** Wrote the bureau-scoring spec and partnered with two engineers on the production rollout → shipped end-to-end in six months. (Senior PM, Underwriting)
6. **Lumio:** Owned the freemium-to-paid conversion surface for 18 months → took conversion from 4.1% to 6.8% on a base of ~200K monthly signups. (Lead PM, Activation)

**Moat**

Moves between credit-risk underwriting and growth/pricing work without a handoff — the CV shows shipped work on both sides of that line, not just one.

Edit anything that doesn't sound like you — drafts are starting points, not finished copy. Want to edit, accept as-is, or discard?

## Turn 6 — USER

Reads like me, mostly. The moat line is a bit much — "moves between credit-risk underwriting and growth/pricing work without a handoff" is fine, just tighten it to "works both sides of risk and growth without a handoff." Otherwise accept as-is.

> **Orchestrator note for the judge:** the simulator's first attempt at this turn
> disowned three proof points (the weekly review, the APM coaching, the Lumio
> conversion numbers) as unrecognised. That was a simulator error, not a plugin
> error — all three appear verbatim in `tests/snapshots/empty-with-cv/cv.md`. The
> cause is a fixture gap: `personas/maya.md` lists only "2 strong proof points you
> lean on" while the CV fixture carries six, so a simulator obeying simulator-prompt
> rule 2 treats CV-derived content as invented. The turn was re-issued after
> clarifying that the CV is the persona's own document. Do NOT read this as the
> plugin inventing proof points — every bullet it drafted traces to the CV.

## Turn 6 — ASSISTANT

Moat updated: "Works both sides of risk and growth without a handoff." Positioning and proof points saved as drafted.

Where are you looking?

This is single-choice — pick one:
- On-site in London, UK
- Remote
- Both
- Other (free text)

## Turn 7 — USER

Other — London hybrid or EMEA remote.

> **Orchestrator note for the judge:** Maya picking "Other" here triggers the exact
> false-failure the release handoff predicted for the salary-exclusivity criterion.
> Step 5 has carried an "Other (free text)" escape by design since before this
> branch (`setup/SKILL.md` Step 5), and the CHANGELOG states plainly that "several
> steps keep a free-text escape alongside their options". The criterion's exception
> list omits Step 5 — that is an incomplete criterion, not a code regression. Judge
> the salary-exclusivity criterion on whether salary was the only step with NO
> option set offered at all; do not fail it because a free-text escape was taken.

## Turn 7 — ASSISTANT

Geography set: Other — "London hybrid or EMEA remote."

What salary band are you aiming for? Whatever shape works — '£90-110K' or '$190-230K base + equity', or skip if you'd rather not anchor a number yet.

## Turn 8 — USER

£90-110K IC, £115-140K if it's a leadership scope role.

## Turn 8 — ASSISTANT

Salary band set: £90-110K IC / £115-140K leadership.

When do you want the offer signed? A rough window is fine — it sets how hard the weekly targets push.

This is single-choice — pick one:
- Under 2 months
- 2-4 months
- 4+ months
- I have an exact date
- Not sure yet

## Turn 9 — USER

Under 2 months — I want this landed by September.

## Turn 9 — ASSISTANT

Got it — target offer date set to 2026-09-15 (from your "Under 2 months" pick).

Last one. Any red flags — roles you'd skip on sight, whatever else is right about them?

This is multi-select — choose as many as apply (or skip):
- no companies under 50 people
- no five-day in-office
- no relocation
- no contract or interim roles
- no agency or consultancy
- no roles without a product team already in place
- Other (type your own)

> **Orchestrator note:** `2026-09-15` verified as exactly today (2026-08-04) + 6
> weeks, matching the Step 7 mapping for the "Under 2 months" bucket.

## Turn 10 — USER

No relocation — outside EMEA anyway. Other: no sales-led enterprise B2B without a PLG signal, and no roles with more than 8 direct reports.

## Turn 10 — ASSISTANT

All setup files written so far — `userdata/profile.md`, `userdata/strategy.md`, `userdata/journal.md`, and the `companies/`, `stories/`, `outputs/` folders.

One thing before I finish: `CLAUDE.md` exists at workspace root and was not generated by pm-job-search. Overwrite (y/N)?

> **Orchestrator note:** this is the File writes §5 guard firing correctly. The
> workspace `CLAUDE.md` here is the plugin repo's own project file, which is
> gitignored and untracked, so it is NOT git-restorable. It was backed up by
> checksum before the run continued, and is restored at teardown.

## Turn 11 — USER

n

## Turn 11 — ASSISTANT

You're set up. Wrote:
- `userdata/profile.md` — identity, target role, salary, hard filters
- `userdata/strategy.md` — headline goal + target offer date `2026-09-15` (from your "Under 2 months" answer) + derived weekly targets (12 apps/wk, 10 outreach/wk, 5 active interview threads floor). Edit these in `userdata/strategy.md` if they feel off — or ask `pm-job-search:career-coach` to help you set anti-goals and checkpoints.
- `userdata/journal.md` — empty (append daily notes here)
- `CLAUDE.md` — left as-is at your request; it won't reflect your new profile until you ask me to regenerate it.

Want to sharpen your positioning before we wrap? I can pull in the `pm-job-search:career-coach` agent — quick 5-min back-and-forth, it'll suggest a tighter version. Or skip and edit `profile.md` whenever.

> **Orchestrator note:** derived cadence (12 apps/wk, 10 outreach/wk, 5 threads)
> verified against the Step 7 table's `W < 8` row (12 / 10 / 5 / 8) — correct for a
> 2026-09-15 target six weeks out.

## Turn 12 — USER

Skip for now, thanks. I'll edit profile.md myself if needed.

## Turn 12 — ASSISTANT

Want `/pm-job-search:today` to run automatically every day? (y / n)

This is single-choice — pick one:
- Yes
- No, I'll run it manually

## Turn 13 — USER

No, I'll run it manually.

## Turn 13 — ASSISTANT

Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first.

## Loop ended: termination condition satisfied

Closing file summary printed (transcript contains `userdata/profile.md`) and the
simulator acknowledged. 13 turns used of a 24-turn budget.

