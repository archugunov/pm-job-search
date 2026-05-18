---
title: Risk team dissent
story_type: stakeholder-dissent
themes: [cross-functional, risk, dissent, stakeholder-management]
role_lens: [strategy, execution, design-partnership]
companies_used_in: [Lendable, Plaid]
last_practised: 2026-05-15
---

# Risk team dissent

## Situation

UK consumer lender, post-Series B, ~£80M loan book. I had designed a pricing
experiment to lower APR by 1.5 percentage points for a high-credit-quality
borrower cohort (FICO equivalent 720+, 12+ months on-book repayment history,
no missed payments). The hypothesis: the cohort was being overpriced relative
to its observed default rate, and a lower APR would improve retention and
application conversion without meaningful NPL impact. The Risk team blocked it.
Their concern was model drift: if macroeconomic conditions shifted mid-test,
the cohort's historical default behaviour might not hold, and we'd be exposed
with a repriced book and no quick route to reversal.

## Task

I owned the pricing surface as Senior PM. The experiment was within my remit to
design, but Risk had institutional authority over any change that touched
default exposure. I needed to get from "blocked" to "approved and running" —
without routing around Risk, without escalating to the CPO (which would have
burned the relationship for every future experiment), and without diluting the
experiment to the point where the signal would be uninterpretable.

## Action

- Requested a working session with the Head of Risk rather than sending email.
  Asked them to walk me through their model-drift concern specifically — what
  scenario would have to materialise, over what time horizon, to produce a
  default uplift that exceeded the experiment's risk envelope. Got them to name
  the number: >50bps NPL deviation from the control cohort over 12 weeks would
  be the threshold they'd call a problem.
- Proposed three structural changes to the experiment design based directly on
  what I'd heard: (1) staged rollout — 5% of eligible cohort first, expanding
  to 25% at week 4 if NPL was within tolerance, then full rollout at week 8;
  (2) a pre-registered kill switch on >50bps NPL deviation (the exact number
  they'd named); (3) a joint weekly review with Head of Risk as a named
  participant, not just a recipient of the results report.
- Wrote the revised experiment brief with Risk as a co-author on the design
  section — not a reviewer, a named author. That was deliberate: it gave them
  ownership of the kill switch trigger, which meant their concern was embedded
  in the experiment structure rather than sitting outside it.
- Got CPO sign-off on the joint-review cadence so it had organisational weight,
  not just PM-to-Risk goodwill.

## Result

- Experiment ran 12 weeks. NPL impact: +18bps above control (well within the
  50bps tolerance). Conversion on the repriced cohort: +6%. Portfolio NPV
  impact: +£1.4M annualised.
- The kill switch was never triggered. Risk team surfaced this unprompted in
  the retrospective as evidence the staged design had been worth the extra
  setup.
- Head of Risk proposed becoming a standing co-owner on all subsequent pricing
  experiments. That structure is now standard: every pricing brief has a Risk
  co-author on the design section before it goes to CPO.
- The relationship shifted from "Risk as approval gate" to "Risk as design
  input" — a change that accelerated the next two experiments by removing the
  back-and-forth approval cycle.

## Angles for different prompts

**"Tell me about a time you disagreed with a stakeholder."** Lead with the "blocked" moment — and be specific that the block was legitimate. The Risk team's concern about model drift wasn't wrong; it was a real possibility in a variable macro environment. The disagreement wasn't "I was right and they were wrong" — it was "we had different priors about the probability of the drift scenario, and I needed to structure the experiment so that their prior could be tested rather than argued away."

**"Tell me about stakeholder management."** Lead with the working session and the ask to have Risk name the specific threshold that would trigger a problem for them. The tactical move was getting them to articulate a concrete number (50bps) rather than a vague concern about model drift. Once the number existed, the kill switch was just encoding their own stated threshold into the experiment design — which is much harder to object to than a PM-designed guardrail imposed on them.

**"Tell me about cross-functional collaboration."** Lead with the co-authorship decision on the experiment brief. The distinction between "reviewer" and "co-author" is not cosmetic — it changes who owns the outcome if the experiment surfaces unexpected results. Making Risk a named co-author on the design section meant the experiment was theirs to defend as much as mine, which is why the retrospective went the way it did.

**"Tell me about a failure mode you've seen in product orgs."** Lead with the "routing around Risk" failure mode — and explain why I didn't do it even when it would have been faster. When PMs route around risk functions, the short-term win is a faster experiment; the medium-term cost is that risk functions become more defensive and approval cycles get longer for everyone. The discipline of going through rather than around was a deliberate choice about what kind of operating environment I wanted to work in.
