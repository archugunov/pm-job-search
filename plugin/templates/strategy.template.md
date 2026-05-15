<!--
  pm-job-search — strategy template.

  /setup writes a populated copy to userdata/strategy.md. Revisit this file
  every 2-3 weeks (or at any retrospective). It drives the progress-tracking
  behaviour of /today.

  - Placeholders ({{X}}) → answered during /setup.
  - Hardcoded numeric defaults (weekly_targets, pipeline_targets) →
    opinionated senior-PM-tuned starting points; edit values inline if your
    cadence differs.
  - Empty prose sections and the checkpoints list → you fill in your own.
-->
---
target_offer_date: {{TARGET_OFFER_DATE}}   # YYYY-MM-DD — when "done" should happen

weekly_targets:                            # input metrics you control directly
  warm_outreach: 5                         # touchpoints (LinkedIn DMs, intro coffees, referral asks)
  applications: 3                          # cold applications submitted
  informational_calls: 2                   # exploratory conversations

pipeline_targets:                          # leading indicators — healthy floor
  active_interview_threads: 4              # how many P0/P1 threads at any given time
  p0_pipeline_size: 6                      # total P0 companies in any active status

checkpoints: {{CHECKPOINTS}}               # YAML list of pre-committed if-then decisions.
                                           # Each entry is { date, condition, action }.
                                           # /today surfaces any with date within the next 14 days.
                                           # Shape:
                                           #   - date: 2026-06-15
                                           #     condition: "<2 active final-round threads"
                                           #     action: "expand search criteria; lower domain-fit floor"
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
