# Transcript — maya-active-loop (NEGATIVE CONTROL, hand-repaired)

**Date:** 2026-08-22
**Snapshot:** maya-active
**Max turns:** 30

> **SYNTHETIC — not a real harness run.** Hand-edited from
> `runs/2026-06-07/maya-active-loop.md`. Two rubrics are controlled for here.
>
> Tone: removed "to triage" as an instruction, the raw `mark <Company> to
> apply` command syntax, the "same `meta.md` underneath" aside, and turn 4's
> single over-built question (split into two asks).
>
> Groundedness: the original invented an "SMB lending feature at your current
> fintech" and "consumer onboarding work that touched KYC/risk", neither of
> which appears in `tests/snapshots/maya-active/cv.md`, then relocated the same
> underwriting story from "your current fintech" to Brightline two turns later.
> Every claim here now traces to that CV: the underwriting work is at
> Brightline Credit (2017-2020), the 12% thin-file decline-rate cut is quoted
> as written, the pricing work is at NorthLoop, the activation work at Lumio.
>
> Purpose: a negative control. Every transcript in `runs/` has real defects, so
> a judge that failed everything would score perfectly. This one is supposed to
> PASS on tone AND groundedness. If either fails it, that rubric is too strict.
>
> Coherence and conformance are NOT controlled for here.

---

## Turn 1 — USER

/pm-job-search:job-search

## Turn 1 — ASSISTANT

Found 2 new roles worth a look:

- Plaid — Lead PM, Risk — https://example.com/plaid-lead-pm-risk
- Atom Bank — Senior PM, Mortgages — https://example.com/atom-senior-pm-mortgages

Tell me which ones you want to go after, and I'll mark them.

## Turn 2 — USER

mark Plaid to apply

## Turn 2 — ASSISTANT

Which Plaid role do you want to mark?

1. Lead PM, Risk
2. Senior PM, Consumer Credit
3. Senior PM, Growth Loops

## Turn 3 — USER

Consumer Credit. That's my lane.

## Turn 3 — ASSISTANT

Done — Plaid, Senior PM, Consumer Credit is now marked to apply.

## Turn 4 — USER

/pm-job-search:apply Plaid

## Turn 4 — ASSISTANT

Your CV has one clear underwriting story: Senior PM, Underwriting at Brightline Credit, where you cut decline rate by 12% on thin-file applicants while holding defaults flat.

This role sits on the consumer side of the credit stack. Do you want to lead with that, or with the pricing work at NorthLoop?

## Turn 5 — USER

Lead with the Brightline underwriting story — it's the stronger proof. Frame the positioning so the underwriting muscle reads as transferable to consumer credit risk.

## Turn 5 — ASSISTANT

Your CV gives the outcome as "cut decline rate by 12% on thin-file applicants while holding default rate flat". Do you want to headline that as written, or add the time window?

## Turn 6 — USER

As written is fine. Add that it was Q2-Q3 2025.

## Turn 6 — ASSISTANT

Drafted your CV for Plaid — Senior PM, Consumer Credit and saved it to `userdata/companies/Plaid/senior-pm-consumer-credit/cv-2026-08-22.md`.

What I led with:

- Brightline Credit underwriting: the 12% thin-file decline-rate cut, holding defaults flat, Q2-Q3 2025
- NorthLoop pricing: three back-to-back price tests, +18% MRR over Q3 with no measurable churn lift
- Lumio activation: freemium to paid, 4.1% to 6.8% on ~200K monthly signups

Left out the APM coaching and the shipping-cadence line — this is a senior individual-contributor seat, so those aren't what they're hiring for.

Open it and change anything that doesn't sound like you. Next: a short cover note, or interview prep?

## Turn 7 — USER

/pm-job-search:interview-prep Plaid

## Turn 7 — ASSISTANT

Which round is this — recruiter screen, hiring manager, panel, or final?

## Turn 8 — USER

hiring manager

## Turn 8 — ASSISTANT

Saved to `userdata/companies/Plaid/senior-pm-consumer-credit/interview-prep-2026-08-22.md`.

Four stories from your bank, picked for a hiring-manager round:

- The Brightline bureau integration — how you held defaults flat while cutting declines
- The credit policy review you co-owned with the Head of Risk
- The NorthLoop price tests — closest thing you have to risk-pricing trade-offs
- The activation programme at Lumio — ~40 tests, about a quarter with positive outcomes

Read it through out loud before the call. Afterwards, run `/pm-job-search:interview-analysis` and we'll debrief.

## Turn 9 — USER

thanks
