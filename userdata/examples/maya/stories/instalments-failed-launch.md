---
title: Instalments failed launch
story_type: failed-launch
themes: [failed-launch, instalments, postmortem, judgment]
role_lens: [strategy, execution, analytics]
companies_used_in: [Lendable]
last_practised: 2026-04-30
---

# Instalments failed launch

## Situation

Consumer fintech, post-Series B. I led the build of a 4-month instalment
product — split-purchase for online retail, letting users spread a transaction
over 3 or 6 months at checkout. The commercial case was clear: merchant fees +
interest on the spread, with a take-rate target of 25% of eligible transactions
by week 4. The team had conviction. We had conjoint research showing 35%
stated intent-to-use among the target segment. The engineering build was
clean. We launched on schedule.

Week 4 actual take-rate: 12%. Week 8: declining to 8%. Week 10: I called it.
Week 12: product killed.

## Task

I was the PM owning the product end to end — strategy, build, launch, and the
kill decision. Once take-rate underperformed at week 4, the task was to
diagnose the failure quickly and make a clean recommendation: keep trying, pivot
the approach, or shut it down. I owned all three options and the recommendation.

## Action

- At week 5, ran qualitative interviews with 12 users who had been eligible but
  had not taken up the offer. The pattern: users understood the product but
  found the real-money trade-off (committing to a 3-month obligation at a
  checkout moment) harder than the conjoint research had suggested. The 35%
  stated intent did not survive the friction of actual cash commitment.
- At week 7, commissioned a price-test against real live traffic — the test we
  should have run in beta. Three variants: 0% APR for 3 months, 9.9% APR for
  6 months, and a fee-based flat charge. Results by week 9: no variant moved
  take-rate materially. The conversion problem was not price; it was user intent
  at the decision moment.
- Between weeks 8 and 10, the team ran two late-flight pivots: lowering the
  minimum purchase threshold from £80 to £40, and simplifying the checkout flow
  from 4 steps to 2. Both required engineering changes to a codebase that had
  been built for the original spec. Neither moved the metric. The second pivot
  created integration debt that made the eventual product kill harder to execute
  cleanly.
- At week 10, wrote a one-page recommendation to the CPO: take-rate is
  structurally below the threshold needed for the unit economics to work; the
  conjoint signal did not predict real-money behaviour; two pivot attempts have
  confirmed the conversion problem is not addressable by price or flow
  simplification alone. Recommendation: kill at week 12.

## Result

- Product killed at week 12. No recoverable business case at observed take-rate.
- Postmortem named three specific failure modes: (1) conjoint research measuring
  intent, not real-money commitment — we should have run a beta with real
  transactions before building the full product; (2) price-test not run until
  week 8, when it should have been a beta-phase prerequisite; (3) late-flight
  pivots created engineering debt that made the kill harder — a faster kill at
  week 8 would have been cleaner.
- The postmortem produced a concrete process change: any product with a >£50K
  build investment now requires a 2-week real-money beta (not conjoint-based
  intent measurement) before engineering investment is committed.
- The "shut it down at week 10" call was the correct one. The team had genuine
  conviction in the product — making the kill recommendation required naming
  that clearly: the team's belief was reasonable, the market had given us the
  answer, and continuing would have cost 8 more weeks of engineering time for
  a business case that wasn't there.

## Angles for different prompts

**"Tell me about a failure."** Lead with the week 10 call, not the product performance. The metric story is simple — take-rate missed. The harder story is the kill decision against a team with genuine conviction. Name what made it hard: the team wasn't wrong to believe in it; the conjoint data was real; the build was clean. The evidence said stop and the right call was to name it cleanly rather than run another pivot cycle.

**"Tell me about your judgment."** Lead with the conjoint-to-real-money gap. The failure wasn't that take-rate underperformed — it was that we trusted an intent signal (35% stated) as a conversion predictor without testing it against real-money friction first. Judgment is knowing the difference between "intent" and "behaviour" in a consumer finance context, and knowing to run a real-money beta before committing engineering resources to a full build.

**"Tell me about a time you killed something."** Lead with the process: what I needed to see to recommend a kill, how I framed the recommendation, and why I called it at week 10 rather than running to week 12. The discipline is being able to name the specific evidence threshold that would change your recommendation — not "we'll give it more time" but "we ran a price-test, take-rate didn't move, therefore the problem is intent not price, therefore the fix is not within our control."

**"Tell me about a postmortem."** Lead with the three named failure modes — and be specific that the most important one was running the price-test at week 8 instead of beta. Every postmortem produces a lesson; the test is whether the lesson produced a process change that would actually catch the same failure mode next time. The 2-week real-money beta requirement is the process change. It exists because of this postmortem.
