<!--
  pm-job-search — strategy template.
  /setup writes a populated copy to userdata/strategy.md. Revisit this file
  every 2-3 weeks (or at any retrospective). It drives the progress-tracking
  behaviour of /today.
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

checkpoints:                               # pre-committed if-then decisions
  - date: {{CHECKPOINT_DATE_1}}            # YYYY-MM-DD — when to revisit
    condition: "<2 active final-round threads"
    action: "expand search to include Senior PM at P0 companies"
  # add more checkpoints as you set them. /today will surface any within
  # the next 14 days.
---

## Headline goal

{{HEADLINE_GOAL}}

<!--
  One paragraph. What success looks like, by when, why it matters now.
  Be concrete about role level, comp floor, and timing — vague goals
  produce vague /today reports.
-->

## Anti-goals

- Add situational exclusions here that extend `profile.md`'s `hard_filters`.
- Examples: "no role with >150 ppl during this search", "no relocation outside Europe in next 6 months", "no companies still pre-PMF".
- Skills check drafts and outreach against this list. Keep it short.
