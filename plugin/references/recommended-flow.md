# Recommended flow

This file is the canonical source for the pm-job-search happy path. Every skill consults it to compose a context-aware next-step nudge at the end of its run.

## Canonical sequence

```
setup → job-search → dashboard → today (daily, ongoing)
                                  ↓
                            evaluate-position (per role, when a link comes in)
                                  ↓
                            apply (when a role moves to "to apply")
                                  ↓
                            interview-prep (when interview is scheduled)
                                  ↓
                            interview-analysis (after the interview)

story-builder runs ad-hoc, whenever the user wants to capture a new STAR story or fill a gap.
evaluate-offer runs when an offer arrives.
career-coach runs on-demand for reflection, positioning, anti-goals, offer evaluation.
integrations runs once during onboarding (or whenever wiring changes).
```

## State → suggested next step

When a skill finishes, look at current filesystem and journal state, then pick the most useful next step. The list below is ordered: first matching rule wins. If nothing matches, suggest `/pm-job-search:today`.

| Current state | Suggested next step | Wording hint |
|---|---|---|
| `userdata/profile.md` just written, no companies in `userdata/companies/` | `/pm-job-search:job-search` | "Run /pm-job-search:job-search now to seed your applications list." |
| Companies exist with `status: new` and no `userdata/outputs/applications.md` (or applications.md is stale) | `/pm-job-search:dashboard` | "Open the dashboard to triage your new roles — or say `mark <Co> to apply` here." |
| At least one company `status: interview` and no `interview-prep-<date>.md` for it | `/pm-job-search:interview-prep <Co>` | "You have an interview coming up at <Co> with no prep doc yet." |
| At least one company `status: to apply` for 14+ days with no movement | Nudge in chat, no command | "<Co> has been in 'to apply' for 2+ weeks. Time to move or drop it." |
| A daily brief was just generated and journal entries exist from the prior ISO week, and this is the first /today of the new ISO week | Weekly reflection prompt | "It's the start of a new week. Want a 5-min reflection on last week?" |
| Default | `/pm-job-search:today` | "Run /pm-job-search:today tomorrow morning (or right now) for your daily brief." |

## Why founder outreach

A few skills reference founder outreach (e.g. `/today` heads-up, strategy.md weekly targets). The why: founder outreach is a discovery channel for early-stage roles where the founder is the hiring decision-maker — it surfaces opportunities that don't appear on public job boards. Surface this only when the user has opted into a founder-outreach target in `strategy.md`.

## Conventions for the nudge

- One line, plain prose. Not a bulleted list.
- Specific to context — not a generic parrot of the canonical order.
- Skip the nudge entirely if there's no useful next step (e.g. the user just finished `/today` and there's nothing notable to flag).
