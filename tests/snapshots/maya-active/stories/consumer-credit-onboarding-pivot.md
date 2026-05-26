---
title: Consumer credit onboarding pivot
story_type: strategic-pivot
themes: [strategy, pivot, conversion, growth]
role_lens: [strategy, execution, analytics]
companies_used_in: [Cleo, Lendable, Plaid]
last_practised: 2026-05-15
---

# Consumer credit onboarding pivot

## Situation

UK consumer lender, ~40K active borrowers, thin-file credit focus. We shipped
a 7-step KYC funnel for new credit applicants: ID upload, income verification,
employer callout, open banking link, credit-bureau consent, loan-amount
selection, and offer confirmation. The redesign was 14 weeks in build;
stakeholders across Risk, Compliance, and Engineering had signed off on every
step. We launched in February. Conversion dropped 18% against the pre-launch
baseline within the first 30 days. The HM's instinct was to hold the funnel
stable and wait for a "settling in" effect. My read was different.

## Task

I owned the credit applicant funnel as Senior PM. The conversion drop was mine
to diagnose and mine to resolve. I had a mandate to propose a fix within two
weeks of the signal emerging, with a recommendation that Risk and Compliance
could sign off on. The constraint was real: any step removed had to clear a
brief fraud-risk impact assessment before we could ship the change.

## Action

- Ran session-replay and drop-off analysis step by step. Three steps accounted
  for 71% of abandonment: income verification (manual upload), employer callout
  (free-text field with no autocomplete), and the ID re-check mid-funnel (a
  duplicate of the document already submitted at step 1). The other four steps
  had negligible incremental drop-off.
- Modelled the LTV impact of removing those three steps against a range of
  fraud-rate uplifts. At the observed income band (£22K–£38K median), a fraud
  uplift of up to 8 basis points would still produce a positive net portfolio
  NPV given the conversion recovery. The Risk team's concern was whether the
  uplift would stay within that band.
- Proposed a staged removal: drop the ID re-check first (zero fraud signal
  added, purely duplicate), then remove employer callout (low incremental
  signal per Risk's own model), then park income verification for a structured
  30-day test against a manual-review fallback. Wrote the recommendation as a
  one-page fraud-impact brief, not a product spec.
- Got Risk sign-off in five days. Shipped ID re-check removal in week 3,
  employer callout removal in week 4, income verification test started week 6.

## Result

- Conversion recovered and reached 8% above the pre-launch baseline by week 8
  of the revised funnel.
- Fraud rate moved from 12 bps to 17 bps — within the 20 bps tolerance band
  agreed with Risk before the experiment.
- Net portfolio NPV increased ~£2.1M annualised on the cohort passing through
  the simplified funnel, accounting for the higher fraud bps.
- Risk team adopted the fraud-impact brief format as the standard template for
  subsequent funnel changes — they asked for it to be embedded in our product
  spec process.

## Angles for different prompts

**"Tell me about a time you made a call your stakeholders were uncomfortable with."** Lead with the HM's instinct to hold the funnel and wait. The discomfort was real — 14 weeks of build, Compliance sign-off on every step, and I was proposing to remove three of them within 30 days of launch. Name the decision structure that made it possible: the fraud-impact brief gave Risk a concrete threshold to approve against, rather than an open-ended ask to trust the PM's gut.

**"Tell me about leading through ambiguity."** Lead with the "settling in" effect argument — it was plausible, not obviously wrong, and there was real organisational pressure to give the funnel more time. The ambiguity was: how do you distinguish a launch-noise dip from a structural conversion problem? Frame the answer as the session-replay analysis that made the signal concrete enough to act on.

**"Tell me about a strategy pivot."** Lead with the LTV math. The pivot wasn't "remove steps because users found them annoying" — it was "the risk-adjusted NPV of the simplified funnel is better than the risk-adjusted NPV of the full funnel, and here's the number." The pivot was a business decision, not a UX preference.

**"Tell me about working with a risk or compliance team."** Lead with the fraud-impact brief, not the conversion outcome. The thing that unlocked Risk buy-in was giving them a decision structure they could own — a tolerance band they had agreed to, an incremental removal order that let them observe each step independently, and a fallback for income verification. The result was that they became a co-owner of the format, not a veto on the outcome.
