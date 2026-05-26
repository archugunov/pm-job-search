---
title: Enterprise bet failed launch
themes: [failed-launch, enterprise, postmortem, judgment]
role_lens: [strategy, execution, analytics]
companies_used_in: []
last_practised: 2026-04-18
---

# Enterprise bet failed launch

## Situation

B2B SaaS, Series C, ~$26M ARR. The product had a strong self-serve motion among
SMB and mid-market customers, but enterprise deals were closing slowly and
requiring heavy sales-assist. Product leadership had been asking whether an
enterprise tier could convert self-serve accounts upward without requiring
dedicated SDR involvement. I had data showing that a subset of self-serve "Team"
customers were already at 10+ seats and had SSO requests open in support — the
hypothesis felt sound.

## Task

I was VP Product. My remit: design, ship, and evaluate an enterprise pricing
experiment — a "Team Plus" tier at +$50/seat/month that bundled SSO and RBAC.
Success target: 12 enterprise opt-ins in 8 weeks from the self-serve base,
measurable without sales involvement.

## Action

- Scoped the experiment as a self-serve upgrade path only: in-app upgrade prompt
  for Team-tier workspaces above 8 seats, pointing to a Team Plus trial. No
  outbound. No sales-assist fallback — I explicitly chose not to include one,
  reasoning that the experiment needed to measure self-serve intent cleanly.
- Named the tier "Team Plus." Didn't test the name; chose it to be a legible
  extension of the existing "Team" tier.
- Shipped in week 2 after a 2-week build cycle. Monitored upgrade clicks, trial
  starts, and conversion to paid weekly.
- At week 8: 3 confirmed conversions against a 12-conversion target.

## Result

- 3 conversions in 8 weeks — 25% of the 12-conversion target. Killed the
  experiment at week 9.
- Postmortem findings: (1) Self-serve-first orgs don't make buying-committee
  decisions in 8-week windows — the sales-cycle assumption was wrong. Enterprise
  SSO requires IT, security, and a champion; self-serve accounts at 10+ seats
  still have a buying process that doesn't happen inside the product. (2) The
  absence of a sales-assist fallback meant there was no capture path for leads
  who were interested but not ready to convert self-serve. Should have shipped
  with a "Talk to us" path before measuring against a pure self-serve target.
  (3) "Team Plus" confused existing Team-tier customers — 14 support tickets in
  the first week from customers asking whether their Team plan was changing.
- Postmortem output: a checklist now required for any enterprise pricing test —
  "must ship with sales-assist fallback, must validate tier name with ≥5 existing
  customers, must confirm sales-cycle length assumption with sales lead before
  setting conversion target."
- The 3 conversions that did happen were eventually closed with sales-assist
  after the experiment ended — evidence the demand existed, just not in the
  assumed form.

## Angles for different prompts

**"Tell me about a failure."** Lead with the specific decision to exclude a
sales-assist fallback path. Name it as a judgment error, not a methodology error:
I had the data that enterprise deals required buying-committee alignment — I
chose to run the experiment anyway against a pure self-serve hypothesis. The
checklist is the evidence I updated.

**"Tell me about judgment under uncertainty."** Lead with the original hypothesis
and what made it feel sound — real support data on SSO requests, real seat count
data. The lesson wasn't that the data was wrong; it was that the inference was
wrong. Good signal doesn't eliminate the need to pressure-test the sales-cycle
assumption before setting a target.

**"Tell me about working with a founder or CEO."** Lead with the decision to kill
the experiment at week 9 rather than extend. The CEO wanted to extend. I argued
for the kill based on the week-5 trajectory — by week 5, the gap between target
and actual was clear enough that weeks 6-8 were adding noise, not signal. The
decision to kill early was harder than the launch decision.

**"Tell me about a postmortem."** Lead with the checklist as the output. A
postmortem that produces principles no one can act on is a post-mortem in name
only. The checklist is actionable — any PM running an enterprise pricing test
runs it through the checklist before the experiment launches, not after.
