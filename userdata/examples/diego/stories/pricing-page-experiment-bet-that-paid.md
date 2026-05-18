---
title: Pricing page experiment bet that paid
themes: [pricing, experimentation, growth, bet-that-paid-off]
role_lens: [strategy, execution, analytics]
companies_used_in: [Retool]
last_practised: 2026-05-15
---

# Pricing page experiment bet that paid

## Situation

B2B SaaS, post-Series B, strong PLG motion. The public pricing page showed four
tiers: Free, Starter, Team, Enterprise. Organic traffic from SEO and content was
the primary acquisition channel — roughly 60% of new signups came from
search-to-pricing-page. The problem: 80% of those signups converted to the Free
tier and almost none upgraded within the first 30 days. The CEO had always
treated the Free tier as a brand statement — "developer-first, no credit card,
no friction." It was a product value, not just a pricing decision, and touching
it was politically sensitive.

## Task

I was Head of Product. My conviction: visitors landing on the pricing page from
organic traffic were not the right cohort to seed the Free tier. They were
high-intent comparison shoppers, not exploratory developers. Removing Free from
the public pricing page — keeping it available via direct URL — would push
organic traffic toward the paid trial without touching the developer brand or
the product itself. The CEO was unconvinced; the decision required running it
as a reversible test.

## Action

- Built the traffic-source segmentation first: broke down signups by acquisition
  source (organic search, direct, referral, in-product invite). Isolated the
  organic-search cohort — this was the treatment group. Direct and referral
  traffic kept seeing the unchanged pricing page as the control.
- Ran a 4-week test: organic traffic landing on /pricing saw a page without the
  Free tier card. Free tier still accessible via /pricing/free. Conversion goal:
  paid trial start within 7 days.
- Presented the test design to the CEO with explicit rollback criteria defined in
  advance: if paid trial conversion didn't move by ≥30% in 2 weeks, or if total
  new signups dropped by ≥15%, revert and postmortem. The pre-registered
  criteria were the thing that made the founder comfortable with the test.
- Monitored weekly with the analyst: traffic-source breakdown, conversion to paid
  trial, churn rate on the new trial cohort vs the historical Free-tier cohort.

## Result

- Conversion to paid trial 2.3× in the first month on the treated organic cohort,
  against a 30% lift target — significantly exceeded the pre-registered threshold.
- Churn on the new trial cohort was stable (within 2pp of the historical Free-tier
  churn at 90 days) — the prediction that removing Free from the public page
  wouldn't attract lower-quality customers held.
- MRR +14% by month 3, attributed via cohort comparison to the pricing page
  change.
- The CEO moved from "unconvinced" to "this should be permanent" after seeing
  the week-2 data — the pre-registered rollback criteria created trust in the
  experiment, which made the result credible rather than convenient.
- One thing that didn't work: the /pricing/free direct URL saw a 40% drop in
  organic traffic within two weeks — developers who found the old Free-tier card
  via search didn't find the direct URL naturally. Fixed by adding a "Free tier
  available" text link on the main page in week 3; traffic to /pricing/free
  recovered to 70% of baseline.

## Angles for different prompts

**"Tell me about a high-conviction bet."** Lead with the traffic-source segmentation
insight — the 80% organic-to-Free conversion rate was the signal. The conviction
came from understanding *who* was landing on the pricing page, not just *what*
they were doing there. Most people would have optimised the Free-to-paid upgrade
flow; this story is about deciding that was the wrong problem.

**"Tell me about working with a founder or CEO."** Lead with the rollback criteria
as the design move that unlocked the test. The CEO's objection wasn't irrational
— Free was a brand value. Pre-registering the rollback criteria gave him a
defined exit without requiring him to trust the outcome in advance. The
experiment design was the relationship management.

**"Tell me about analytics depth."** Lead with the traffic-source segmentation
methodology — why organic search was the treatment group and direct was the
control. Explain the churn guardrail: if removing Free attracted lower-quality
customers, churn would show it within 90 days. Both predictions held; the
discipline was building the guardrails before seeing the results.

**"Tell me about a failure."** Lead with the /pricing/free direct-URL drop —
the 40% traffic loss to the free-tier page that wasn't anticipated. Name the
assumption that failed: that developers who previously found the Free card on
the pricing page would navigate to a direct URL if the card was removed. They
didn't; they bounced. Fixed in week 3, but it was a meaningful gap in the
test design.
