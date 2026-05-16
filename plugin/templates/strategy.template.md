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
target_offer_date: {{TARGET_OFFER_DATE}}

# Outreach + applications per week. Either can be null to skip tracking.
weekly_targets:
  warm_outreach: {{WEEKLY_WARM_OUTREACH}}
  applications: {{WEEKLY_APPLICATIONS}}

# Leading indicators — the floor below which something is off. Either can be null.
pipeline_targets:
  active_interview_threads: {{PIPELINE_ACTIVE_THREADS}}
  p0_pipeline_size: {{PIPELINE_P0_SIZE}}

# Pre-committed if-then decisions. /today surfaces any whose date is within
# the next 14 days. Shape:
#   - date: 2026-06-15
#     condition: "<2 active final-round threads"
#     action: "expand search criteria; lower domain-fit floor"
checkpoints: {{CHECKPOINTS}}
---

## Headline goal

{{HEADLINE_GOAL}}

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
