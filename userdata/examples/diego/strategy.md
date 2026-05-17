<!-- Example file. -->
<!--
  pm-job-search — strategy template.

  /setup writes a populated copy of this file to userdata/strategy.md when you
  install: target_offer_date from Q11, weekly_targets + pipeline_targets
  auto-derived from your timeline (see /setup SKILL.md for the cadence table),
  and the headline goal auto-composed from your profile.md.

  Deeper sections (## Anti-goals, checkpoints) start empty. To fill them in:
  - Edit this file directly, OR
  - Ask `pm-job-search:career-coach` ("help me think through my anti-goals",
    "set my checkpoints", "rebalance my weekly cadence") — the agent walks
    you through one theme at a time and proposes edits for you to paste.

  This file drives the progress-tracking behaviour of /today. Any unset value
  (null) is gracefully skipped — /today doesn't report against numbers you
  haven't committed to.

  This example file shows Diego's strategy after he ran /setup, edited the
  auto-derived cadences slightly (more outreach, fewer applications to fit
  his fully-remote US-search shape), and set anti-goals + checkpoints via
  the career-coach agent.
-->
---
# YYYY-MM-DD — when "done" should happen.
target_offer_date: 2026-09-15

# Outreach + applications per week. Either can be null to skip tracking.
weekly_targets:
  warm_outreach: 6
  applications: 2

# Leading indicators — the floor below which something is off. Either can be null.
pipeline_targets:
  active_interview_threads: 5
  p0_pipeline_size: 8

# Pre-committed if-then decisions. /today surfaces any whose date is within
# the next 14 days. Shape:
#   - date: 2026-06-15
#     condition: "<2 active final-round threads"
#     action: "expand search criteria; lower domain-fit floor"
checkpoints:
  - date: 2026-07-15
    condition: "fewer than 3 active threads with $190K+ base disclosed"
    action: "open conversations with two US-remote-focused exec recruiters; consider lowering base floor to $175K"
  - date: 2026-08-15
    condition: "no offers in hand"
    action: "open advisory-engagement conversations to bridge income; extend timeline by 6 weeks"
---

## Headline goal

Sign a Head of Product or VP Product offer at a P0-tier B2B SaaS or DevTools company by 15 September 2026, base ≥$190K, fully remote with Americas overlap. The target shape is Series B/C, 30-100 ppl, founder still in product, measurable PLG motion. Six months of runway is the floor — comfortable extending the search to early Q4 if the right founder shows up at the end of Q3.

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

- No on-site or 3-day hybrid roles. Setup is built around fully remote.
- No sales-led B2B with bolted-on "PLG" labelling — the underlying revenue motion has to be self-serve at the top of the funnel.
- No companies still negotiating their seed-to-Series-A — too early, wrong shape.
- No US-East-Coast-only working hours; need at least 4 hours of midday overlap from Mexico City.

<!-- Last edited by /strategy on 2026-05-15 -->
