<!-- Example file. Replace with your own via /setup. -->
<!--
  pm-job-search — strategy template.

  /setup writes a copy of this file to userdata/strategy.md with placeholders
  intact. /strategy walks you through a 15-20 minute reflection that
  substitutes the placeholders. Revisit /strategy every 2-3 weeks (or at any
  retrospective) — strategy.md drives the progress-tracking behaviour of /today.

  - Placeholders ({{X}}) → filled by /strategy from your answers.
  - Numeric targets (weekly_targets, pipeline_targets) are personal cadence —
    no defaults shipped. If a target is unset (null), /today skips that
    comparison rather than reporting against an arbitrary number.
-->
---
# YYYY-MM-DD — when "done" should happen.
target_offer_date: 2026-08-01

# Outreach + applications per week. Either can be null to skip tracking.
weekly_targets:
  warm_outreach: 5
  applications: 3

# Leading indicators — the floor below which something is off. Either can be null.
pipeline_targets:
  active_interview_threads: 4
  p0_pipeline_size: 6

# Pre-committed if-then decisions. /today surfaces any whose date is within
# the next 14 days. Shape:
#   - date: 2026-06-15
#     condition: "<2 active final-round threads"
#     action: "expand search criteria; lower domain-fit floor"
checkpoints:
  - date: 2026-06-15
    condition: "<2 active final-round threads"
    action: "expand search to include Senior PM at P0 companies; lower domain-fit threshold one notch"
  - date: 2026-07-15
    condition: "no offers in hand"
    action: "open conversations with two specialist fintech recruiters; one interim/contract enquiry"
---

## Headline goal

Sign a Head of Product or senior Lead PM offer at a P0-tier company by 1 August 2026, base ≥£115K, in London hybrid or EMEA-remote. The target shape is Series A-B fintech or consumer credit, founder-led, 20-80 ppl. Three months of runway after that is the financial floor — anything tighter pushes me toward accepting a fit-compromised role and that's a worse outcome than extending the search.

<!--
  One paragraph. What success looks like, by when, why it matters now.
  Be concrete about role level, comp floor, and timing — vague goals
  produce vague /today reports.
-->

## Anti-goals

<!--
  Bullet list. Situational exclusions that extend profile.md's hard_filters.
  Things you won't do during THIS search even if you might consider them in
  general. Skills check outreach and evaluations against this list.

  Useful prompts to seed this section:
  - What company shapes have burned you before that you're avoiding now?
  - What compromises would make this role the wrong job even if it pays?
  - What timing constraints (relocation, family, runway) cap the choice?
-->

- No role with >150 ppl during this search (founder-distance kills the work I'm best at).
- No relocation outside Europe in next 6 months.
- No crypto-native companies (out of scope by preference).
- No company still pre-PMF — that's a different job to the one I want.
- No more than 6 direct reports — that's GM scope, not the IC-lead I'm targeting.

<!-- Last edited by /strategy on 2026-05-15 -->
