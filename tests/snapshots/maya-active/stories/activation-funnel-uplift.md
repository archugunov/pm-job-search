---
title: Activation funnel uplift
themes: [activation, conversion, funnel-optimization, B2C SaaS]
role_lens: [execution, analytics, leadership]
companies_used_in: []
last_practised:
---

# Activation funnel uplift

## Situation

SaaS unicorn (~£300M ARR at the time), B2C-leaning productivity product, freemium → paid conversion was the company's primary growth lever. By Q4 2022 the conversion rate had been stuck between 4.0-4.3% of weekly-active free workspaces for six quarters. Growth team had run twelve A/B tests on the in-app upgrade prompt and seen no movement. The CEO was openly skeptical there was anything left to find.

## Task

I'd just been promoted to Lead PM on the activation squad — three engineers, one designer, no analyst (I was the analyst). My remit: take a fresh look at why conversion was stuck and propose a plan to fix it. Six weeks to ship a diagnosis, then own the work if it landed.

## Action

- Started with cohort cuts the previous PM hadn't run. Pulled the data myself in SQL, segmented by signup source × team-size-at-signup × day-7-activity. Found that solo signups converted at 6.1% while team signups converted at 1.8% — the average hid two completely different funnels.
- Spent two weeks shadowing customer-success calls and reading 80 sales-team-handover notes. The qualitative pattern: team signups stalled because the inviter never invited their teammates in the first 48 hours — the product looked empty to them.
- Reframed the problem with the eng lead: not "improve conversion" but "fix the first-invite gap on team signups". This was a different product surface than the upgrade prompt the growth team had been A/B testing.
- Designed and shipped a three-part change: (a) a setup-flow nudge that scanned the user's email domain and suggested teammates to invite; (b) a 24-hour delayed nudge if no invites had been sent; (c) a redesigned "empty workspace" state for second-and-later teammates that pre-populated based on the inviter's setup.
- Killed the second nudge (the 24-hour delayed one) at week three after pre-registered guardrails showed it correlated with workspace abandonment on a small but real cohort. Shipped only (a) and (c).

## Result

- Team-signup conversion went from 1.8% to 4.6% over four months. Solo-signup conversion was unchanged (the change didn't target them).
- Blended conversion lifted from 4.1% to 6.8% on a base of ~200K monthly signups — the number leadership cared about.
- The reframing (segmenting team vs solo) is now standard practice across all growth experiments at the company.
- The killed nudge taught me the discipline of pre-registering kill conditions; I've carried that into every test I've run since.

## Angles for different prompts

**"Tell me about leading through ambiguity."** Lead with the moment I had to push back on the CEO's "there's nothing left to find" framing. The story is about how I gathered evidence (data + qual) before re-opening the question, not about the conversion lift itself.

**"Tell me about analytics depth."** Lead with the cohort segmentation that nobody had run. The story is the diagnosis — splitting team vs solo signups — not the fix. Bonus: shows I do my own SQL.

**"Tell me about working with engineering."** Lead with the eng-lead conversation where we reframed the problem from "improve the upgrade prompt" to "fix the first-invite gap". Shows that strong PM-eng partnership starts with re-defining the question.

**"Tell me about a failure."** Lead with the killed second nudge. Pre-registered guardrail, kill at week three, what I learned about cohort-specific harm that an aggregate metric would have missed.
