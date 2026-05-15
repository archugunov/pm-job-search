---
title: Payments pricing experiment
themes: [growth, pricing, experimentation, post-PMF]
role_lens: [strategy, execution, analytics]
companies_used_in: [Plaid]
last_practised: 2026-05-11
---

# Payments pricing experiment

## Situation

Series B fintech, ~£60M ARR, flagship product is a buy-now-pay-later card for
thin-file customers. By Q2 2025 our pricing surface (interchange share, late
fee, monthly cap) hadn't been touched in 18 months. CFO wanted +£8M ARR by
year-end; growth team wanted volume; risk team wanted margin protection. No
one had an experiment framework — every previous pricing change had been
shipped to 100% and rolled back twice.

## Task

I owned the pricing surface as the Senior PM on the growth squad. My remit:
build a programme that could test pricing changes safely and ship the wins.
Three months to prove the framework, then run continuously.

## Action

- Built a four-stage gating model with the risk lead: cohort selection, 90-day
  observation window per test, weekly safety review with risk + finance, and a
  pre-registered kill switch on default-rate drift.
- Designed the first three tests in collaboration with finance: late-fee
  reduction (test 1), monthly-cap raise on a behaviour-eligibility-screened
  cohort (test 2), interchange-share rebalance (test 3). Each was its own
  hypothesis with a primary metric + two guardrails.
- Wrote and shipped the in-app messaging for each variant myself, working
  directly with one engineer. Stayed close to the qualitative — read every
  support ticket for the first two weeks of each test.
- Reviewed weekly with the CFO; presented the gating-model design to the
  board at the Q3 review.

## Result

- +18% MRR over Q3 vs. Q2, no measurable churn lift, no measurable
  default-rate drift on any of the three test cohorts.
- Framework is now the standard pricing-test pattern across the company,
  including outside the credit product.
- One of the three tests was killed at week 4 by the pre-registered
  guardrail — that was a deliberate framework outcome, not a failure.

## Angles for different prompts

**"Tell me about a 0-to-1."** Lead with the *framework* as the 0-to-1, not the
test results. The thing that didn't exist was the gating model.

**"Tell me about leading through ambiguity."** Lead with the three competing
stakeholder asks (CFO, growth, risk) and how the framework absorbed the
disagreement by structure rather than by argument.

**"Tell me about working with engineering."** Lead with shipping the in-app
messaging myself with one engineer. Show the bias to small teams and direct
ownership.

**"Tell me about a failure."** Lead with the killed test — pre-registered
guardrail, kill at week 4, what we learned about cohort definition.
