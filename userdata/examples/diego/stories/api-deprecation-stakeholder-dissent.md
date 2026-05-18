---
title: API deprecation stakeholder dissent
themes: [cross-functional, deprecation, dissent, stakeholder-management]
role_lens: [strategy, execution, design-partnership]
companies_used_in: [Linear]
last_practised: 2026-05-04
---

# API deprecation stakeholder dissent

## Situation

B2B dev-tools company, public, API platform team. A legacy v1 endpoint had been
in production for four years with documented deprecation notices that had never
been enforced. Eng estimated maintenance cost at roughly 0.5 eng per quarter and
rising — the v1 auth model blocked a security initiative the CTO had prioritised.
Two factions had formed: eng wanted a 12-month sunset (cautious, low-risk); GTM
wanted 18 months minimum and had written the timeline into a renewal proposal
already sent to a named enterprise account.

## Task

I was PM on the API platform team. My remit: own the deprecation timeline and
migration strategy end-to-end. No one had given me authority to override either
eng's preference or GTM's commitment — I had to build a cross-functional
position that would hold under dissent from both sides.

## Action

- Ran 8 customer interviews specifically on migration willingness and timeline
  sensitivity. I didn't ask "what timeline do you want?" — I asked "what would
  you need to exist for migration to be low-risk on your end?" The distinction
  mattered: customers kept asking about tooling, not time.
- Surfaced the pattern: 90% of remaining v1 usage came from 5 customers. All 5
  said they'd accept a 6-month timeline if a CLI migration tool existed to
  automate the auth-token swap — they didn't want months, they wanted a tool.
- Proposed the negotiated position to eng and GTM in a joint session: 6-month
  sunset (not 12 or 18) + invest 4 weeks of eng time upfront in a migration CLI.
  Eng saw reduced maintenance risk on a shorter timeline. GTM got a concrete
  deliverable to offer named accounts instead of an indefinite extension.
- Wrote the migration guide jointly with one engineer and one technical writer.
  Ran a dedicated partner call with the top 5 affected accounts before the public
  deprecation announcement.

## Result

- 95% of customers migrated by month 5 — one month ahead of the 6-month
  deadline.
- Legacy endpoint shut down on schedule with zero escalations and zero customer
  defections on renewal.
- The GTM renewal proposal that had referenced 18 months was quietly updated;
  the account renewed without pushback.
- The eng manager subsequently advocated for the "shorter sunset + migration
  investment" pattern as the default for future deprecations — the 4-week
  migration CLI investment created more goodwill than six extra months of
  maintenance window would have.

## Angles for different prompts

**"Tell me about a time you disagreed with a stakeholder."** Lead with the
disagreement between the two factions (12 months vs 18 months) and how you
used customer interviews to reframe the question. The dissent wasn't about
timeline — it was about risk tolerance. Surfacing that customers wanted tooling
over time broke the deadlock.

**"Tell me about analytics depth."** Lead with the usage concentration finding:
90% of v1 traffic coming from 5 customers. Explain how that changed the
entire migration strategy — you weren't solving a broad long-tail problem,
you were solving a 5-customer logistics problem.

**"Tell me about working with engineering."** Lead with the joint proposal session
and the "shorter sunset + migration investment" framing. Eng didn't want the
12-month timeline because they liked it — they wanted it because they didn't
trust the alternative. The migration CLI investment was the thing that made
a shorter timeline acceptable to them.

**"Tell me about a 0-to-1."** Lead with the migration CLI — it didn't exist before
this project. The spec came directly from customer interviews; without those
8 conversations, the team would have defaulted to "more time" instead of
"better tooling."
