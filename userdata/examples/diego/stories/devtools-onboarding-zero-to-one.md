---
title: DevTools onboarding zero to one
themes: [zero-to-one, dev-tools, onboarding, friction]
role_lens: [strategy, execution, analytics]
companies_used_in: [Linear]
last_practised: 2026-05-04
---

# DevTools onboarding zero to one

## Situation

B2B dev-tools company, 60 engineers, no existing onboarding instrumentation for
the CLI product. The install-to-first-meaningful-action path had never been
defined, let alone measured. Eng shipped a new CLI major version and marketing
was running paid acquisition — but no one could answer whether new signups were
actually activating. Weekly active users as a headline metric masked the problem:
the product counted "any CLI invocation" as active, which included failed installs.

## Task

I was Group PM. My remit: define what "activated" meant for the CLI, instrument
the funnel from install through first meaningful outcome, and ship an onboarding
flow that moved the activation rate — all within one quarter, using one engineer
and one technical writer.

## Action

- Defined activation as: complete first-deploy within 7 days of install. That
  was the moment the product delivered its core value promise; anything earlier
  was pipeline, not activation.
- Audited the existing CLI UX with three engineers who each ran through it cold —
  documented every friction point in a shared doc. No existing telemetry, so the
  first sprint was purely instrumentation: install, init, first-deploy as three
  named events with structured properties.
- Shipped a 3-step CLI-first onboarding flow: install → init (project scaffold) →
  first-deploy (live URL within 2 minutes). Wrote the init scaffolding copy
  myself with the technical writer; eng owned the plumbing.
- Ran 4 iteration cycles over 6 weeks, each driven by drop-off telemetry: where
  in the funnel were users exiting? Iterations targeted the highest-drop-off step
  each cycle — step 2 (init) was the biggest blocker in cycles 1-3; step 3
  (first-deploy) in cycle 4.

## Result

- Activation rate moved from 12% to 31% over 6 weeks — 4 shipped iterations,
  each measured against the same 7-day activation definition.
- Net new MAU +18% over baseline in the same period (after controlling for
  acquisition volume, which held flat).
- The activation metric — first-deploy within 7d — became the team's north-star
  input to the weekly sprint review. That framing outlasted my time on the team.
- One iteration made things worse before better: cycle 2 introduced a "getting
  started" prompt on init that increased time-to-first-deploy by 40 seconds and
  hurt completion. Rolled back in cycle 3 and reframed the copy.

## Angles for different prompts

**"Tell me about a 0-to-1."** Lead with the *measurement framework* as the 0-to-1,
not the activation lift. The thing that didn't exist was a shared definition of
"activated" and instrumentation to prove it.

**"Tell me about analytics depth."** Lead with the decision to define activation
specifically as first-deploy within 7d, not any CLI invocation. Explain why the
prior "WAU" metric masked the real funnel and how you isolated the activation
signal from acquisition volume.

**"Tell me about working with engineering."** Lead with the cold-walkthrough
session — three engineers running through the CLI as new users, documenting
friction in a shared doc. That framing got eng into the problem as co-owners,
not executors of a spec.

**"Tell me about a failure."** Lead with cycle 2 — the getting-started prompt
that slowed first-deploy by 40 seconds and hurt completion. Name the specific
mistake: optimising for "looks helpful" over "reduces time-to-value." Rolled back
in cycle 3; used it to establish a time-to-first-deploy guardrail for all future
onboarding copy.
